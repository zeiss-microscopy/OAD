"""Assign stage positions to wells, then clone and save an experiment in ZEN.

Run with zen_api_utils installed:
    python python_examples\\assign_stage_positions_to_wells.py

The source experiment supplies positions; the empty experiment supplies carrier
geometry. Source well labels are not used to determine the assignments.
Requires running ZEN with the empty experiment installed under its file stem
and matching the local reference geometry. CONFIG_PATH supplies the connection.
Only the clone is cleared/modified; no acquisition or stage move is requested.
The clone is saved by ZEN as <empty-stem>_with_positions. Set OVERWRITE_EXPERIMENT
to True to replace an existing experiment with that output name, or False to
reject an existing name.
The original empty experiment is never overwritten.
This does not write a CZEXP beside the local reference file.
XY values must be micrometers in the same calibrated stage coordinate frame
and plate placement as that experiment. All physical wells are considered.
Only the supported unrotated rectangular geometry is accepted; unsupported
geometry and non-finite coordinates raise errors. Rectangle edges are included.
Gaps/outside points return None; assignment does not check image footprints.
Set SELECTED_WELL to a label such as "B2" to add only matching positions.
None adds all positions and rejects unassigned points. With a well selected,
other wells and unassigned points are excluded. Invalid wells or no matches
raise ValueError before connecting; all source XYZ values must still be valid.
"""

import asyncio
import math
from pathlib import Path

from zen_api.acquisition.v1beta import (
    ExperimentServiceCloneRequest,
    ExperimentServiceLoadRequest,
    ExperimentServiceSaveRequest,
    ExperimentServiceStub,
)
from zen_api.lm.acquisition.v1 import (
    Position3D,
    TilesServiceAddPositionsRequest,
    TilesServiceClearRequest,
    TilesServiceIsTilesExperimentRequest,
    TilesServiceStub,
)
from zen_api_utils.extract_czexp_plan import (
    load_carrier_geometry,
    load_experiment_positions,
    parse_well_id,
    well_id,
)
from zen_api_utils.misc import initialize_zenapi

# User settings
ROOT_FOLDER = Path(__file__).resolve().parent
EXPERIMENT_WITH_POSITIONS = ROOT_FOLDER / "data" / "ZEN_API_Test_CD7_Random_Positions.czexp"
EMPTY_EXPERIMENT = ROOT_FOLDER / "data" / "ZEN_API_Test_CD7_empty_W96.czexp"
CONFIG_PATH = ROOT_FOLDER / "my_config.ini"

SELECTED_WELL: str | None = None  # For example, "B2"; None includes all wells.
OVERWRITE_EXPERIMENT: bool = True


async def main() -> None:
    """Validate locally, then configure and save only a clone of the empty experiment."""
    carrier = load_carrier_geometry(EMPTY_EXPERIMENT)
    selected_well = None

    # Normalize labels such as "b02" to "B2" before comparing assignments.
    if SELECTED_WELL is not None:
        row, column = parse_well_id(SELECTED_WELL.strip())
        if row is None or column is None or not (row < carrier.rows and column < carrier.columns):
            raise ValueError(f"Selected well {SELECTED_WELL!r} is invalid for this carrier.")
        selected_well = well_id(row, column)

    positions = load_experiment_positions(EXPERIMENT_WITH_POSITIONS)

    if not positions:
        raise ValueError(f"No acquisition positions found in {EXPERIMENT_WITH_POSITIONS}")

    print(f"Carrier: {carrier.rows} rows x {carrier.columns} columns")
    print(f"Source: {EXPERIMENT_WITH_POSITIONS.name}; {len(positions)} positions")
    print("XY units: micrometers; row/column indices: zero-based")

    stage_xy_um: list[tuple[float, float]] = []
    api_positions: list[Position3D] = []

    # Validate every source position before any ZEN connection or clone is created.
    for position in positions:
        x, y, z = position.x, position.y, position.z

        if x is None or y is None or z is None:
            raise ValueError(
                f"Missing stage XYZ for block {position.block_index}, scene {position.scene_index} "
                f"in {EXPERIMENT_WITH_POSITIONS}"
            )

        if not all(math.isfinite(value) for value in (x, y, z)):
            raise ValueError(f"Non-finite stage XYZ for block {position.block_index}, scene {position.scene_index}")

        stage_xy_um.append((x, y))

        # Persisted CZEXP coordinates are micrometers; the Tiles API uses meters.
        api_positions.append(Position3D(x=x * 1e-6, y=y * 1e-6, z=z * 1e-6))

    # Use only XY geometry for well assignment, not the source experiment's well labels.
    print("Assigning stage positions to wells...")
    assignments = carrier.assign_positions(stage_xy_um)

    for position, (x, y), assignment in zip(positions, stage_xy_um, assignments, strict=True):
        if assignment is None:
            result = "unassigned (gap or outside plate)"
        else:
            result = f"{assignment.well_id}: row={assignment.well_row}, column={assignment.well_column}"
        print(
            f"Block={position.block_index}, scene={position.scene_index}, "
            f"position={position.position_name!r}: X={x:.3f}, Y={y:.3f} -> {result}"
        )

    if selected_well is not None:
        # A selected well excludes other wells and unassigned points, preserving order.
        api_positions = [
            api_position
            for api_position, assignment in zip(api_positions, assignments, strict=True)
            if assignment is not None and assignment.well_id == selected_well
        ]
        if not api_positions:
            raise ValueError(f"No positions fall in selected well {selected_well}; no ZEN connection was made.")

        print(f"Selected well: {selected_well}; adding {len(api_positions)} of {len(positions)} positions")

    elif any(assignment is None for assignment in assignments):
        raise ValueError("Some positions are outside the configured wells; no ZEN connection was made.")

    output_name = f"{EMPTY_EXPERIMENT.stem}_with_positions"

    # ZEN loads installed experiments by name, not from the local reference path.
    channel, metadata = initialize_zenapi(CONFIG_PATH)

    try:
        experiments = ExperimentServiceStub(channel=channel, metadata=metadata)
        tiles = TilesServiceStub(channel=channel, metadata=metadata)

        original = await experiments.load(ExperimentServiceLoadRequest(experiment_name=EMPTY_EXPERIMENT.stem))
        tiles_info = await tiles.is_tiles_experiment(
            TilesServiceIsTilesExperimentRequest(experiment_id=original.experiment_id)
        )

        if not tiles_info.is_tiles_experiment:
            raise ValueError(f"Tiles/positions dimension is not activated in {EMPTY_EXPERIMENT.stem}")

        # All edits target the clone; the installed template remains unchanged.
        clone = await experiments.clone(ExperimentServiceCloneRequest(experiment_id=original.experiment_id))
        await tiles.clear(TilesServiceClearRequest(experiment_id=clone.experiment_id))
        await tiles.add_positions(
            TilesServiceAddPositionsRequest(experiment_id=clone.experiment_id, positions=api_positions)
        )

        await experiments.save(
            ExperimentServiceSaveRequest(
                experiment_id=clone.experiment_id,
                experiment_name=output_name,
                allow_override=OVERWRITE_EXPERIMENT,
            )
        )

        print(f"Saved ZEN experiment: {output_name} ({len(api_positions)} positions)")
    finally:
        # Release the connection even if adding or saving fails.
        channel.close()


if __name__ == "__main__":
    asyncio.run(main())
