#################################################################
# File        : well_tasks.py
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
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from zen_api.acquisition.v1beta import (
    ExperimentServiceCloneRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceRunExperimentRequest,
    ExperimentServiceStub,
)

# gRPC service stubs and request types — acquisition
from zen_api.lm.acquisition.v1 import (
    DefiniteFocusServiceFindSurfaceRequest,
    DefiniteFocusServiceStub,
    ExperimentSwAutofocusServiceFindAutoFocusRequest,
    ExperimentSwAutofocusServiceStub,
    ZStackServiceModifyZStackCenterRangeRequest,
    ZStackServiceStub,
)

# gRPC service stubs and request types — hardware
from zen_api.lm.hardware.v1 import (
    SampleCarrierServiceMoveToContainerRequest,
    SampleCarrierServiceStub,
)
from zen_api.lm.hardware.v2 import (
    FocusServiceGetPositionRequest,
    FocusServiceStub,
    ObjectiveChangerServiceMoveToRequest,
    ObjectiveChangerServiceStub,
)

# zen_api_utils
from zen_api_utils.misc import set_logging
from zen_api_utils.sample_carrier import WellPlate

logger = set_logging()


# ---------------------------------------------------------------------------
# Stage / sample carrier
# ---------------------------------------------------------------------------


def optimize_well_order(plate: WellPlate, wells: Sequence[str]) -> list[str]:
    """
    Reduce stage travel with a deterministic nearest-neighbor heuristic.

    The first configured well is kept as the starting point. From there, the
    function repeatedly chooses the unvisited well with the smallest squared
    row/column distance from the current well::

        distance_squared = (next_row - row) ** 2 + (next_col - col) ** 2

    Squared distance gives the same ordering as Euclidean distance while
    avoiding an unnecessary square-root calculation. If two wells are equally
    distant, their original positions in *wells* break the tie. The result is
    therefore stable and reproducible.

    This greedy method reduces unnecessary travel for scattered worklists, but
    it does not guarantee the globally shortest possible route. It also treats
    row and column spacing as equal; use physical stage coordinates instead if
    the plate geometry requires a more accurate distance model.

    Args:
        plate: Plate used to validate labels and convert them to zero-based
            ``(row, column)`` coordinates.
        wells: Well labels in user-configured order. Duplicate labels are
            retained and treated as separate work items.

    Returns:
        A new list containing every input well exactly once per occurrence.
        The input sequence is not modified.

    Raises:
        ValueError: If any label is invalid or outside the plate layout.

    Complexity:
        Time is :math:`O(n^2)` and additional space is :math:`O(n)`, which is
        appropriate for typical microplate worklists.
    """
    if len(wells) < 2:
        # Always return a new list so callers can safely modify the result even
        # when the input is already a list.
        return list(wells)

    # Store the original index for deterministic tie-breaking. Expanding the
    # coordinate tuple produces records shaped as:
    # (original_index, well_id, row, column).
    indexed_wells = [
        (original_index, well_id, *plate.well_to_index(well_id)) for original_index, well_id in enumerate(wells)
    ]

    # The user controls the initial stage destination; optimization begins only
    # after that first well has been selected.
    ordered = [indexed_wells.pop(0)]

    while indexed_wells:
        _, _, current_row, current_col = ordered[-1]

        # min() compares tuple elements from left to right: distance first,
        # then original input index when distances are equal.
        next_index = min(
            range(len(indexed_wells)),
            key=lambda index: (
                (indexed_wells[index][2] - current_row) ** 2 + (indexed_wells[index][3] - current_col) ** 2,
                indexed_wells[index][0],
            ),
        )
        ordered.append(indexed_wells.pop(next_index))

    # Strip the bookkeeping fields before returning the optimized worklist.
    return [well_id for _, well_id, _, _ in ordered]


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
    # The helper translates a human-readable label (for example B3) into the
    # zero-based row and column expected by the sample-carrier service.
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
) -> float:
    """
    Run Definite Focus *Find Surface* and return the resulting Z position.

    Args:
        definite_focus_service: gRPC stub for the Definite Focus service.

    Returns:
        Z position in **metres** as reported by the focus drive after the
        surface search completes.

    Raises:
        GRPCError: If the hardware call fails.
    """
    logger.info("Running Definite Focus — Find Surface ...")
    # The response already contains the detected position in metres; no
    # additional focus-drive query is needed here.
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
    await objchanger_service.move_to(ObjectiveChangerServiceMoveToRequest(position_index=position))


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
    # SWAF moves the focus drive but does not return the final position. Read
    # the drive after the search to obtain the actual Z coordinate in metres.
    z_response = await focus_service.get_position(FocusServiceGetPositionRequest())
    z_focus_m = z_response.value
    logger.info(f"SWAF found focus at Z = {z_focus_m * 1e6:.3f} µm")
    return z_focus_m


# ---------------------------------------------------------------------------
# Acquisition experiment — reusable clone + per-well z-stack update
# ---------------------------------------------------------------------------


async def clone_acquisition_experiment(
    exp_service: ExperimentServiceStub,
    base_experiment_id: str,
) -> str:
    """Clone the loaded acquisition template once for per-well modifications.

    Args:
        exp_service: gRPC stub for the experiment service.
        base_experiment_id: ID of the loaded acquisition template.

    Returns:
        ID of the reusable acquisition clone.
    """
    logger.info("Cloning acquisition experiment for reusable Z-stack updates ...")
    clone_response = await exp_service.clone(ExperimentServiceCloneRequest(experiment_id=base_experiment_id))
    return clone_response.experiment_id


async def update_zstack_experiment(
    zstack_service: ZStackServiceStub,
    experiment_id: str,
    z_center_m: float,
    z_range_m: float,
    z_interval_m: float,
) -> None:
    """
    Update the reusable acquisition clone's Z-stack for the current well.

    Args:
        zstack_service: gRPC stub for the z-stack service.
        experiment_id: ``experiment_id`` of the reusable clone.
        z_center_m: New z-stack center in **metres** (typically from SWAF).
        z_range_m: Total z-stack range in **metres**.
        z_interval_m: Slice-to-slice interval in **metres**.
    """
    logger.info(f"Setting reusable experiment Z-stack center to {z_center_m * 1e6:.3f} µm ...")
    await zstack_service.modify_z_stack_center_range(
        ZStackServiceModifyZStackCenterRangeRequest(
            experiment_id=experiment_id,
            center=z_center_m,
            interval=z_interval_m,
            range=z_range_m,
        )
    )


# ---------------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------------


async def get_image_output_folder(exp_service: ExperimentServiceStub) -> Path:
    """Query ZEN's image output folder once for reuse by every acquisition.

    Args:
        exp_service: gRPC stub for the experiment service.

    Returns:
        Image output directory configured in ZEN.
    """
    response = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    return Path(response.image_output_path)


async def run_acquisition(
    exp_service: ExperimentServiceStub,
    experiment_id: str,
    well_id: str,
    zen_output_folder: Path,
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
        zen_output_folder: Cached image output folder reported by ZEN.
        timestamp_format: :func:`datetime.strftime` format string for the
            timestamp suffix.
        output_folder: Optional destination folder.  When ``None`` the file
            stays in ZEN's configured image output path.

    Returns:
        :class:`~pathlib.Path` pointing to the final CZI file location.
    """
    timestamp = datetime.now(timezone.utc).strftime(timestamp_format)
    output_name = f"{well_id}_{timestamp}"

    logger.info(f"Acquiring well {well_id} → {zen_output_folder / output_name}.czi ...")
    await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(
            experiment_id=experiment_id,
            output_name=output_name,
        )
    )

    czi_path = zen_output_folder / f"{output_name}.czi"
    logger.info(f"Acquisition complete: {czi_path}")

    # Grouping files after acquisition keeps all data from one plate run in a
    # dedicated folder without changing ZEN's global output configuration.
    if output_folder is not None and output_folder != zen_output_folder:
        output_folder.mkdir(parents=True, exist_ok=True)
        dest = output_folder / czi_path.name
        await asyncio.to_thread(shutil.move, str(czi_path), dest)
        logger.info(f"Moved to: {dest}")
        czi_path = dest

    return czi_path
