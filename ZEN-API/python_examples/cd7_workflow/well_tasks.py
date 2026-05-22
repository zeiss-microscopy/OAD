# -*- coding: utf-8 -*-

#################################################################
# File        : well_tasks.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# One async function per acquisition step executed at every well.
# All functions are thin wrappers around ZEN-API calls and return
# typed values so they can be unit-tested in isolation.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
import shutil
from datetime import datetime
from pathlib import Path

from grpclib.exceptions import GRPCError

# zen_api_utils
from zen_api_utils.misc import set_logging
from zen_api_utils.sample_carrier import WellPlate

# gRPC service stubs and request types — hardware
from zen_api.lm.hardware.v1 import (
    SampleCarrierServiceStub,
    SampleCarrierServiceMoveToContainerRequest,
)
from zen_api.lm.hardware.v2 import (
    FocusServiceStub,
    FocusServiceGetPositionRequest,
    FocusServiceMoveToRequest,
    ObjectiveChangerServiceStub,
    ObjectiveChangerServiceMoveToRequest,
)

# gRPC service stubs and request types — acquisition
from zen_api.lm.acquisition.v1 import (
    DefiniteFocusServiceStub,
    DefiniteFocusServiceFindSurfaceRequest,
    ExperimentSwAutofocusServiceStub,
    ExperimentSwAutofocusServiceFindAutoFocusRequest,
    ZStackServiceStub,
    ZStackServiceModifyZStackCenterRangeRequest,
)
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceCloneRequest,
    ExperimentServiceRunExperimentRequest,
    ExperimentServiceGetImageOutputPathRequest,
)

logger = set_logging()


# ---------------------------------------------------------------------------
# Stage / sample carrier
# ---------------------------------------------------------------------------


async def move_to_well(
    sample_carrier_service: SampleCarrierServiceStub,
    plate: WellPlate,
    well_id: str,
    settle_s: float = 0.5,
) -> None:
    """
    Move the sample carrier so that *well_id* is under the objective.

    Args:
        sample_carrier_service: gRPC stub for the sample carrier service.
        plate: WellPlate instance describing the plate layout.
        well_id: Well label, e.g. ``"B3"``.
        settle_s: Optional pause after the move to let vibrations decay.
    """
    row, col = plate.well_to_index(well_id)
    logger.info(f"Moving to well {well_id}  (row={row}, col={col})")
    await sample_carrier_service.move_to_container(SampleCarrierServiceMoveToContainerRequest(row, col))
    if settle_s > 0:
        await asyncio.sleep(settle_s)


# ---------------------------------------------------------------------------
# Z-surface detection (Definite Focus)
# ---------------------------------------------------------------------------


async def find_surface(
    definite_focus_service: DefiniteFocusServiceStub,
    focus_service: FocusServiceStub,
) -> float:
    """
    Run Definite Focus *Find Surface* and return the resulting Z position.

    Returns:
        Z position in **metres** as reported by the focus drive after the
        surface search completes.

    Raises:
        GRPCError: If the hardware call fails.
    """
    logger.info("Running Definite Focus — Find Surface ...")
    df_response = await definite_focus_service.find_surface(DefiniteFocusServiceFindSurfaceRequest())
    z_surface_m = df_response.zposition
    logger.info(f"Surface found at Z = {z_surface_m * 1e6:.3f} µm")
    return z_surface_m


# ---------------------------------------------------------------------------
# Objective changer
# ---------------------------------------------------------------------------


async def switch_objective(
    objchanger_service: ObjectiveChangerServiceStub,
    position: int,
) -> None:
    """
    Move the objective changer to *position*.

    Args:
        objchanger_service: gRPC stub for the objective changer service.
        position: 1-based changer position to move to.
    """
    logger.info(f"Switching objective to changer position {position} ...")
    await objchanger_service.move_to(ObjectiveChangerServiceMoveToRequest(position=position))


# ---------------------------------------------------------------------------
# Software Autofocus (SWAF)
# ---------------------------------------------------------------------------


async def run_swaf(
    swaf_service: ExperimentSwAutofocusServiceStub,
    focus_service: FocusServiceStub,
    swaf_experiment_id: str,
    timeout_s: int = 15,
) -> float:
    """
    Execute SWAF on a previously-loaded experiment and return the best-focus Z.

    After SWAF the stage is already at the focus position, so the Z value is
    read back from the focus drive for a consistent unit (metres).

    Args:
        swaf_service: gRPC stub for the SW autofocus service.
        focus_service: gRPC stub for the focus drive service.
        swaf_experiment_id: ``experiment_id`` of the already-loaded SWAF experiment.
        timeout_s: Maximum time (seconds) allowed for the autofocus search.

    Returns:
        Best-focus Z position in **metres**.

    Raises:
        GRPCError: If the autofocus call fails (e.g. no signal found).
    """
    logger.info("Running SWAF ...")
    await swaf_service.find_auto_focus(
        ExperimentSwAutofocusServiceFindAutoFocusRequest(
            experiment_id=swaf_experiment_id,
            timeout=timeout_s,
        )
    )
    # Read back the actual Z position from the drive (consistent metres unit)
    z_response = await focus_service.get_position(FocusServiceGetPositionRequest())
    z_focus_m = z_response.value
    logger.info(f"SWAF found focus at Z = {z_focus_m * 1e6:.3f} µm")
    return z_focus_m


# ---------------------------------------------------------------------------
# Acquisition experiment — clone + modify z-stack
# ---------------------------------------------------------------------------


async def prepare_zstack_experiment(
    exp_service: ExperimentServiceStub,
    zstack_service: ZStackServiceStub,
    base_experiment_id: str,
    z_center_m: float,
    z_range_m: float,
    z_interval_m: float,
) -> str:
    """
    Clone *base_experiment_id* and update its z-stack center to *z_center_m*.

    The clone is kept in memory only (never saved to disk) so the ZEN
    experiment folder is not polluted with per-well files.

    Args:
        exp_service: gRPC stub for the experiment service.
        zstack_service: gRPC stub for the z-stack service.
        base_experiment_id: ``experiment_id`` of the template experiment.
        z_center_m: New z-stack center in **metres** (typically from SWAF).
        z_range_m: Total z-stack range in **metres**.
        z_interval_m: Slice-to-slice interval in **metres**.

    Returns:
        ``experiment_id`` of the cloned, modified experiment — pass this to
        :func:`run_acquisition`.
    """
    logger.info(f"Cloning experiment and setting z-stack center to {z_center_m * 1e6:.3f} µm ...")
    clone_response = await exp_service.clone(ExperimentServiceCloneRequest(experiment_id=base_experiment_id))
    well_exp_id = clone_response.experiment_id

    await zstack_service.modify_z_stack_center_range(
        ZStackServiceModifyZStackCenterRangeRequest(
            experiment_id=well_exp_id,
            center=z_center_m,
            interval=z_interval_m,
            range=z_range_m,
        )
    )
    return well_exp_id


# ---------------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------------


async def run_acquisition(
    exp_service: ExperimentServiceStub,
    experiment_id: str,
    well_id: str,
    timestamp_format: str = "%Y%m%d_%H%M%S",
    output_folder: Path | None = None,
) -> Path:
    """
    Run the experiment and return the full path to the saved CZI file.

    The output filename is ``<well_id>_<timestamp>.czi``, e.g.
    ``A1_20260225_143022.czi``.

    Note: ``ExperimentServiceRunExperimentRequest`` only accepts
    ``experiment_id`` and ``output_name`` — there is no output-path field.
    ZEN always writes the file to its own configured image output path.
    If *output_folder* is provided the file is **moved** there after ZEN
    finishes writing, and the new path is returned.  The destination folder
    is created automatically if it does not yet exist.

    Args:
        exp_service: gRPC stub for the experiment service.
        experiment_id: ``experiment_id`` of the (cloned) experiment to run.
        well_id: Well label used as the filename prefix (e.g. ``"A1"``).
        timestamp_format: :func:`datetime.strftime` format string for the
            timestamp suffix.
        output_folder: Optional destination folder.  When ``None`` the file
            stays in ZEN's configured image output path.

    Returns:
        :class:`~pathlib.Path` pointing to the final CZI file location.
    """
    timestamp = datetime.now().strftime(timestamp_format)
    output_name = f"{well_id}_{timestamp}"

    # Retrieve ZEN's image output directory
    path_response = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    zen_folder = Path(path_response.image_output_path)

    logger.info(f"Acquiring well {well_id} → {zen_folder / output_name}.czi ...")
    await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(
            experiment_id=experiment_id,
            output_name=output_name,
        )
    )

    czi_path = zen_folder / f"{output_name}.czi"
    logger.info(f"Acquisition complete: {czi_path}")

    # Optionally move the file to a caller-defined output folder
    if output_folder is not None and output_folder != zen_folder:
        output_folder.mkdir(parents=True, exist_ok=True)
        dest = output_folder / czi_path.name
        shutil.move(str(czi_path), dest)
        logger.info(f"Moved to: {dest}")
        czi_path = dest

    return czi_path
