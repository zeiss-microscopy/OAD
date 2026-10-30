#################################################################
# File        : cd7_workflow.py
# Institution : Carl Zeiss Microscopy GmbH
#
# CellDiscoverer 7 — per-well acquisition + parallel image analysis workflow.
#
# Optional steps are controlled in workflow_config.py. A fully enabled well
# follows this sequence:
#   1. Move to well (SampleCarrier)
#   2. Find surface (Definite Focus)
#   3. Switch to SWAF objective
#   4. Run SWAF → best-focus Z
#   5. Switch to acquisition objective
#   6. Update the reusable acquisition clone's Z-stack center from SWAF
#   7. Run acquisition → save CZI as <well_id>_<timestamp>.czi
#   8. Schedule file-readiness polling and continue with the next well
#
# File polling and queue consumption run as background asyncio tasks. This lets
# analysis of well N overlap microscope operations for well N+1; blocking image
# processing runs in a worker thread. See README.md.
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
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Make the parent directory (python_examples) importable so that
# processing_tools is found when running from the cd7_workflow subfolder.
# zen_api_utils and zen_api must be installed in the active environment.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import the tutorial modules only after python_examples is on sys.path.
import workflow_config as cfg
from analysis_queue import analysis_worker, enqueue_when_ready
from grpclib.exceptions import GRPCError
from well_tasks import (
    clone_acquisition_experiment,
    find_surface,
    get_image_output_folder,
    move_to_well,
    optimize_well_order,
    run_acquisition,
    run_swaf,
    switch_objective,
    update_zstack_experiment,
)
from zen_api.acquisition.v1beta import (
    ExperimentServiceLoadRequest,
    ExperimentServiceStub,
)

# Acquisition service stubs
from zen_api.lm.acquisition.v1 import (
    DefiniteFocusServiceStub,
    ExperimentSwAutofocusServiceStub,
    ZStackServiceGetZStackInfoRequest,
    ZStackServiceStub,
)

# Hardware service stubs
from zen_api.lm.hardware.v1 import (
    SampleCarrierServiceGetInfoRequest,
    SampleCarrierServiceStub,
)
from zen_api.lm.hardware.v2 import (
    FocusServiceStub,
    FocusServiceGetPositionRequest,
    ObjectiveChangerServiceStub,
)

# zen_api_utils helpers
from zen_api_utils.misc import initialize_zenapi, set_logging
from zen_api_utils.experiment import show_zstack_info_LM
from zen_api_utils.sample_carrier import WellPlate

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main() -> None:
    """Run the configured plate acquisition and collect image-analysis results."""

    # -----------------------------------------------------------------------
    # Connect to ZEN
    # -----------------------------------------------------------------------
    # CONFIG_FILE may be absolute. pathlib keeps an absolute right-hand path
    # unchanged; a relative value is resolved below python_examples.
    config_path = Path(__file__).parent.parent / cfg.CONFIG_FILE
    channel, metadata = initialize_zenapi(config_path)

    logger.info("=" * 60)
    logger.info("CD7 Workflow — starting")
    logger.info("=" * 60)

    try:
        # -------------------------------------------------------------------
        # Create lightweight clients for the ZEN services used by this example.
        # Every stub shares the same gRPC channel and authentication metadata.
        # -------------------------------------------------------------------
        sample_carrier_service = SampleCarrierServiceStub(channel=channel, metadata=metadata)
        focus_service = FocusServiceStub(channel=channel, metadata=metadata)
        objchanger_service = ObjectiveChangerServiceStub(channel=channel, metadata=metadata)
        definite_focus_service = DefiniteFocusServiceStub(channel=channel, metadata=metadata)
        swaf_service = ExperimentSwAutofocusServiceStub(channel=channel, metadata=metadata)
        zstack_service = ZStackServiceStub(channel=channel, metadata=metadata)
        exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

        # -------------------------------------------------------------------
        # Discover the plate layout from the hardware instead of assuming a
        # fixed format such as 96 or 384 wells.
        # -------------------------------------------------------------------
        info = await sample_carrier_service.get_info(SampleCarrierServiceGetInfoRequest())
        logger.info(f"Sample carrier: {info.name}  " f"({info.rows} rows × {info.columns} columns)")
        plate = WellPlate(info.rows, info.columns)

        # Validate the complete worklist before the first hardware movement.
        invalid = [w for w in cfg.WELLS if w not in plate]
        if invalid:
            raise ValueError(
                f"The following wells are outside the plate layout " f"({info.rows}×{info.columns}): {invalid}"
            )

        # if cfg.MODIFY_ZSTACK and not cfg.RUN_SWAF:
        #     raise ValueError("MODIFY_ZSTACK requires RUN_SWAF so each well has a focus position")

        well_ids = optimize_well_order(plate, cfg.WELLS) if cfg.OPTIMIZE_WELL_ORDER else list(cfg.WELLS)
        if well_ids != cfg.WELLS:
            logger.info(f"Optimized well order: {' → '.join(well_ids)}")

        # -------------------------------------------------------------------
        # Experiment IDs can be reused, so load each template only once.
        # -------------------------------------------------------------------
        if cfg.RUN_SWAF:
            logger.info(f"Loading SWAF experiment: '{cfg.SWAF_EXPERIMENT}' ...")
            swaf_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=cfg.SWAF_EXPERIMENT))

        logger.info(f"Loading acquisition experiment: '{cfg.ACQ_EXPERIMENT}' ...")
        acq_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=cfg.ACQ_EXPERIMENT))

        # Cache ZEN's global output folder instead of querying it for every well.
        zen_output_folder = await get_image_output_folder(exp_service)
        if cfg.USE_ZEN_OUTPUT_FOLDER_DIRECTLY:
            run_output_folder = zen_output_folder
            acquisition_move_folder = None
            logger.info(f"Using ZEN output folder directly: {run_output_folder}")
        else:
            run_output_folder = cfg.EXPERIMENT_SUBFOLDER
            acquisition_move_folder = run_output_folder
            logger.info(f"Completed CZI files will be moved to: {run_output_folder}")

        # A mutable clone is created once, then its Z-stack center is updated
        # before each sequential acquisition.
        acquisition_experiment_id = acq_exp.experiment_id
        if cfg.MODIFY_ZSTACK:
            acquisition_experiment_id = await clone_acquisition_experiment(
                exp_service,
                acq_exp.experiment_id,
            )

        # -------------------------------------------------------------------
        # Start the producer/consumer analysis pipeline
        # -------------------------------------------------------------------
        analysis_queue: asyncio.Queue[Path] = asyncio.Queue()

        # The worker appends one dictionary per (well, Z-plane). No lock is
        # needed because these asyncio tasks share one event-loop thread.
        analysis_results: list[dict[str, str | int]] = []

        # Each completed or failed CZI analysis advances this bar once.
        analysis_pbar = tqdm(
            total=len(well_ids),
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
        # Per-well acquisition loop
        # -------------------------------------------------------------------
        enqueue_tasks: list[asyncio.Task[None]] = []

        for well_id in tqdm(
            well_ids,
            desc="Acquisition    ",
            unit="well",
            position=0,
            leave=True,
            colour="cyan",
        ):
            logger.info("-" * 60)
            logger.info(f"Well: {well_id}")
            logger.info("-" * 60)

            # Microscope operations for one well are intentionally sequential.
            await move_to_well(
                sample_carrier_service,
                plate,
                well_id,
                settle_s=cfg.MOVE_SETTLE_S,
            )

            # Surface detection and SWAF are optional, but they provide the
            # focus position required when MODIFY_ZSTACK is enabled.
            if cfg.RUN_SWAF:
                try:
                    z_surface = await find_surface(definite_focus_service)
                except GRPCError as exc:
                    logger.error(f"[{well_id}] Definite Focus failed: {exc.message}. " "Skipping well.")
                    continue

                logger.info(f"[{well_id}] Surface Z = {z_surface * 1e6:.3f} µm")

                # A lower-magnification objective can make autofocus faster and
                # more robust. Leave the current objective unchanged if disabled.
                if cfg.CHANGE_TO_SWAF_OBJECTIVE:
                    await switch_objective(objchanger_service, cfg.OBJECTIVE_POS_SWAF)

                # If SWAF cannot find focus, the detected surface is still a
                # useful fallback for centering the acquisition Z-stack.
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

            if not cfg.RUN_SWAF:
                # use the current z-position as fallback for the focus when SWAF is not run
                z_focus_response = await focus_service.get_position(FocusServiceGetPositionRequest())
                z_focus = z_focus_response.value

            logger.info(f"[{well_id}] Focus  Z = {z_focus * 1e6:.3f} µm")

            if cfg.CHANGE_TO_ACQ_OBJECTIVE:
                # Restore the objective intended for the actual image acquisition.
                await switch_objective(objchanger_service, cfg.OBJECTIVE_POS_ACQ)

            if cfg.MODIFY_ZSTACK:
                # Reuse one clone and change only its center for this well.
                await update_zstack_experiment(
                    zstack_service=zstack_service,
                    experiment_id=acquisition_experiment_id,
                    z_center_m=z_focus,
                    z_range_m=cfg.ZSTACK_RANGE_M,
                    z_interval_m=cfg.ZSTACK_INTERVAL_M,
                )

                # show update Z-Stack parameters for debugging
                # get the information about the stack
                zstack_info = await zstack_service.get_z_stack_info(
                    ZStackServiceGetZStackInfoRequest(experiment_id=acquisition_experiment_id)
                )

                show_zstack_info_LM(zstack_info)

            # ZEN first writes <well>_<timestamp>.czi to its configured output
            # path. run_acquisition moves it only when a destination is set.
            try:
                czi_path = await run_acquisition(
                    exp_service=exp_service,
                    experiment_id=acquisition_experiment_id,
                    well_id=well_id,
                    zen_output_folder=zen_output_folder,
                    timestamp_format=cfg.FILENAME_TIMESTAMP_FORMAT,
                    output_folder=acquisition_move_folder,
                )
            except GRPCError as exc:
                logger.error(f"[{well_id}] Acquisition failed: {exc.message}. Skipping.")
                continue

            if cfg.RUN_IMAGE_ANALYSIS:
                # Scheduling, rather than awaiting, keeps file-readiness polling
                # off the sequential microscope path. The loop can start moving
                # to the next well while this task prepares the previous CZI.
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
        # The producer phase ends only after every successful CZI is ready and
        # has been placed on the queue.
        # -------------------------------------------------------------------
        logger.info("All wells acquired. Waiting for remaining files to be enqueued ...")
        await asyncio.gather(*enqueue_tasks, return_exceptions=True)

        # -------------------------------------------------------------------
        # queue.join() pairs with task_done() in analysis_worker and therefore
        # waits for processing, not merely for the queue to become empty.
        # -------------------------------------------------------------------
        logger.info("All files enqueued. Waiting for analysis jobs to complete ...")
        await analysis_queue.join()
        analysis_pbar.close()
        logger.info("All analysis jobs completed.")

        # The worker is intentionally persistent, so cancel it once no more
        # queue items can arrive.
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

        # -------------------------------------------------------------------
        # Export accumulated analysis results to CSV
        # -------------------------------------------------------------------
        if cfg.RUN_IMAGE_ANALYSIS and analysis_results:
            df = pd.DataFrame(analysis_results)

            # Stable ordering makes the CSV easy to scan and compare between runs.
            df.sort_values(["well_id", "z_plane"], inplace=True)

            ts = datetime.now(timezone.utc).strftime(cfg.FILENAME_TIMESTAMP_FORMAT)
            csv_path = run_output_folder / f"analysis_results_{ts}.csv"
            run_output_folder.mkdir(parents=True, exist_ok=True)
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
