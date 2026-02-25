# -*- coding: utf-8 -*-

#################################################################
# File        : cd7_workflow.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# CellDiscoverer 7 — per-well acquisition + parallel image analysis workflow.
#
# Workflow per well:
#   1. Move to well (SampleCarrier)
#   2. Find surface (Definite Focus)
#   3. Switch to SWAF objective
#   4. Run SWAF → best-focus Z
#   5. Switch to acquisition objective
#   6. Clone acquisition experiment, set z-stack center to Z from SWAF
#   7. Run acquisition → save CZI as <well_id>_<timestamp>.czi
#   8. Fire-and-forget: wait for file to be written, then submit to analysis queue
#
# The analysis worker consumes the queue independently so analysis of well N
# overlaps with the acquisition of well N+1.
#
# Usage:
#   Activate your Python environment (e.g. conda activate smartmic), then:
#       python cd7_workflow.py
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Make the parent directory (python_examples) importable so that
# zen_api_utils and zen_api packages are found when running this script
# from inside the cd7_workflow subfolder.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from grpclib.exceptions import GRPCError

# Local modules
import workflow_config as cfg
from well_tasks import (
    move_to_well,
    find_surface,
    switch_objective,
    run_swaf,
    prepare_zstack_experiment,
    run_acquisition,
)
from analysis_queue import enqueue_when_ready, analysis_worker

# zen_api_utils helpers
from zen_api_utils.misc import set_logging, initialize_zenapi
from zen_api_utils.sample_carrier import WellPlate

# Hardware service stubs
from zen_api.lm.hardware.v1 import (
    SampleCarrierServiceStub,
    SampleCarrierServiceGetInfoRequest,
)
from zen_api.lm.hardware.v2 import (
    FocusServiceStub,
    ObjectiveChangerServiceStub,
)

# Acquisition service stubs
from zen_api.lm.acquisition.v1 import (
    DefiniteFocusServiceStub,
    ExperimentSwAutofocusServiceStub,
    ZStackServiceStub,
)
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main() -> None:
    # -----------------------------------------------------------------------
    # 1. Connect
    # -----------------------------------------------------------------------
    config_path = Path(__file__).parent.parent / cfg.CONFIG_FILE
    channel, metadata = initialize_zenapi(config_path)

    logger.info("=" * 60)
    logger.info("CD7 Workflow — starting")
    logger.info("=" * 60)

    try:
        # -------------------------------------------------------------------
        # 2. Instantiate all services
        # -------------------------------------------------------------------
        sample_carrier_service = SampleCarrierServiceStub(channel=channel, metadata=metadata)
        focus_service = FocusServiceStub(channel=channel, metadata=metadata)
        objchanger_service = ObjectiveChangerServiceStub(channel=channel, metadata=metadata)
        definite_focus_service = DefiniteFocusServiceStub(channel=channel, metadata=metadata)
        swaf_service = ExperimentSwAutofocusServiceStub(channel=channel, metadata=metadata)
        zstack_service = ZStackServiceStub(channel=channel, metadata=metadata)
        exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

        # -------------------------------------------------------------------
        # 3. Discover plate layout from the hardware
        # -------------------------------------------------------------------
        info = await sample_carrier_service.get_info(SampleCarrierServiceGetInfoRequest())
        logger.info(f"Sample carrier: {info.name}  " f"({info.rows} rows × {info.columns} columns)")
        plate = WellPlate(info.rows, info.columns)

        # Validate all requested wells before starting any movement
        invalid = [w for w in cfg.WELLS if w not in plate]
        if invalid:
            raise ValueError(
                f"The following wells are outside the plate layout " f"({info.rows}×{info.columns}): {invalid}"
            )

        # -------------------------------------------------------------------
        # 4. Pre-load experiments once (avoids repeated disk I/O per well)
        # -------------------------------------------------------------------
        if cfg.RUN_SWAF:
            logger.info(f"Loading SWAF experiment: '{cfg.SWAF_EXPERIMENT}' ...")
            swaf_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=cfg.SWAF_EXPERIMENT))

        logger.info(f"Loading acquisition experiment: '{cfg.ACQ_EXPERIMENT}' ...")
        acq_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=cfg.ACQ_EXPERIMENT))

        # -------------------------------------------------------------------
        # 5. Start background analysis worker
        # -------------------------------------------------------------------
        analysis_queue: asyncio.Queue[Path] = asyncio.Queue()

        # Shared list — analysis_worker appends one dict per (well, z-plane).
        # Safe without a lock because asyncio is single-threaded.
        analysis_results: list[dict] = []

        # Progress bar for image analysis — total is set to the number of
        # wells; each completed analysis job advances it by 1.
        analysis_pbar = tqdm(
            total=len(cfg.WELLS),
            desc="Image analysis",
            unit="well",
            position=1,
            leave=True,
            colour="green",
        )

        worker_task = asyncio.create_task(
            analysis_worker(
                queue=analysis_queue,
                results=analysis_results,
                pbar=analysis_pbar,
            )
        )
        logger.info("Analysis worker started.")

        # -------------------------------------------------------------------
        # 6. Per-well acquisition loop
        # -------------------------------------------------------------------
        enqueue_tasks = []

        for well_id in tqdm(
            cfg.WELLS,
            desc="Acquisition    ",
            unit="well",
            position=0,
            leave=True,
            colour="cyan",
        ):
            logger.info("-" * 60)
            logger.info(f"Well: {well_id}")
            logger.info("-" * 60)

            # 6a. Move to well
            await move_to_well(
                sample_carrier_service,
                plate,
                well_id,
                settle_s=cfg.MOVE_SETTLE_S,
            )

            # 6b. Find surface with Definite Focus
            if cfg.RUN_SWAF:
                try:
                    z_surface = await find_surface(definite_focus_service, focus_service)
                except GRPCError as exc:
                    logger.error(f"[{well_id}] Definite Focus failed: {exc.message}. " "Skipping well.")
                    continue

                logger.info(f"[{well_id}] Surface Z = {z_surface * 1e6:.3f} µm")

                # 6c. Switch to SWAF objective (low magnification)
                if cfg.CHANGE_TO_SWAF_OBJECTIVE:
                    await switch_objective(objchanger_service, cfg.OBJECTIVE_POS_SWAF)

                # 6d. Run SWAF
                try:
                    z_focus = await run_swaf(
                        swaf_service,
                        focus_service,
                        swaf_exp.experiment_id,
                        timeout_s=cfg.SWAF_TIMEOUT_S,
                    )
                except GRPCError as exc:
                    logger.error(f"[{well_id}] SWAF failed: {exc.message}. " "Using surface Z as fallback.")
                    z_focus = z_surface

                logger.info(f"[{well_id}] Focus  Z = {z_focus * 1e6:.3f} µm")

            if cfg.CHANGE_TO_ACQ_OBJECTIVE:
                # 6e. Switch to acquisition objective (high magnification)
                await switch_objective(objchanger_service, cfg.OBJECTIVE_POS_ACQ)

            if cfg.MODIFY_ZSTACK:
                # 6f. Clone acquisition experiment, update z-stack center to SWAF focus
                well_exp_id = await prepare_zstack_experiment(
                    exp_service=exp_service,
                    zstack_service=zstack_service,
                    base_experiment_id=acq_exp.experiment_id,
                    z_center_m=z_focus,
                    z_range_m=100.0 * 1e-6,
                    z_interval_m=3.0 * 1e-6,
                )
            else:
                well_exp_id = acq_exp.experiment_id

            # 6g. Run acquisition — CZI filename: <well>_<timestamp>.czi
            #     ZEN saves to its own output path; the file is then moved to
            #     cfg.EXPERIMENT_SUBFOLDER (one timestamped folder per run).
            try:
                czi_path = await run_acquisition(
                    exp_service=exp_service,
                    experiment_id=well_exp_id,
                    well_id=well_id,
                    timestamp_format=cfg.FILENAME_TIMESTAMP_FORMAT,
                    output_folder=cfg.EXPERIMENT_SUBFOLDER,
                )
            except GRPCError as exc:
                logger.error(f"[{well_id}] Acquisition failed: {exc.message}. Skipping.")
                continue

            if cfg.RUN_IMAGE_ANALYSIS:
                # 6h. Submit file to analysis queue as soon as it is fully written.
                #     create_task() returns immediately — the acquisition loop
                #     continues to the next well while this waits in the background.
                task = asyncio.create_task(
                    enqueue_when_ready(
                        queue=analysis_queue,
                        czi_path=czi_path,
                        poll_interval_s=cfg.POLL_INTERVAL_S,
                        file_settle_s=cfg.FILE_SETTLE_S,
                    )
                )
                enqueue_tasks.append(task)

        # -------------------------------------------------------------------
        # 7. Wait for all CZI files to be enqueued …
        # -------------------------------------------------------------------
        logger.info("All wells acquired. Waiting for remaining files to be enqueued ...")
        await asyncio.gather(*enqueue_tasks, return_exceptions=True)

        # -------------------------------------------------------------------
        # 8. … then wait for all analysis jobs to finish.
        # -------------------------------------------------------------------
        logger.info("All files enqueued. Waiting for analysis jobs to complete ...")
        await analysis_queue.join()
        analysis_pbar.close()
        logger.info("All analysis jobs completed.")

        # Stop the worker cleanly
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

        # -------------------------------------------------------------------
        # 9. Export accumulated analysis results to CSV
        # -------------------------------------------------------------------
        if cfg.RUN_IMAGE_ANALYSIS and analysis_results:
            df = pd.DataFrame(analysis_results)

            # Sort for readability: well → z-plane
            df.sort_values(["well_id", "z_plane"], inplace=True)

            ts = datetime.now().strftime(cfg.FILENAME_TIMESTAMP_FORMAT)
            csv_path = cfg.EXPERIMENT_SUBFOLDER / f"analysis_results_{ts}.csv"
            cfg.EXPERIMENT_SUBFOLDER.mkdir(parents=True, exist_ok=True)
            df.to_csv(csv_path, index=False)
            logger.info(f"Results exported to: {csv_path}")
            logger.info(f"\n{df.to_string(index=False)}")

    except Exception as exc:
        logger.error(f"Workflow aborted with error: {exc}")
        raise

    finally:
        channel.close()
        logger.info("=" * 60)
        logger.info("CD7 Workflow — finished")
        logger.info("=" * 60)


if __name__ == "__main__":
    logger = set_logging()
    asyncio.run(main())
