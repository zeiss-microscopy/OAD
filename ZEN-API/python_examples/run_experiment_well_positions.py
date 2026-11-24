"""Acquire one CZI per planned position, count objects, and collect run outputs.

Requires a running ZEN instance. Executing main() configures experiments and,
when run_experiment is enabled, moves microscope hardware and acquires images.
"""

import asyncio
import shutil
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from czitools.read_tools import read_tools
from extract_experiment_positions import extract_positions, print_positions
from processing_tools import ArrayProcessor
from skimage.filters import threshold_otsu
from zen_api.acquisition.v1beta import (
    ExperimentServiceCloneRequest,
    ExperimentServiceExportRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceLoadRequest,
    ExperimentServiceRunExperimentRequest,
    ExperimentServiceStub,
)
from zen_api.lm.acquisition.v1 import (
    Position3D,
    TilesServiceAddPositionsRequest,
    TilesServiceClearRequest,
    TilesServiceStub,
)
from zen_api_utils.misc import initialize_zenapi, set_logging

# User settings: paths refer to the machine running this script.
exp_name = Path(
    "C:\\Users\\m1srh\\Documents\\Carl Zeiss\\ZEN\\Documents\\Experiment Setups\\ZEN_API_Wellplate_Positionlist.czexp"
)

config_path: Path = Path("F:\\Pixi_Projects\\zen_czi\\smartmicroscopy\\examples\\control_zen_via_zenapi\\my_config.ini")
run_experiment: bool = True
target_folder: Path = Path("f:\\Zen_Output\\zenapi_wellpositions")
save_cloned_experiment: bool = False  # export each configured clone before acquisition
max_objects_per_well: int = 100  # cumulative target; skip further positions once reached


logger = set_logging()


def count_czi_objects(filepath: Path, *, planes: dict[str, tuple[int, int]] | None = None) -> int:
    """Count bright objects in one selected XY plane using Otsu thresholding.

    planes uses inclusive, zero-based STCZ ranges, selecting one index per axis.
    Omitted axes default to (0, 0); for example, planes={"C": (1, 1)}
    selects channel 1 at S=0, T=0, Z=0. Multi-plane data is rejected.
    Uses the existing labeling helper: remove objects of at most 10 pixels,
    fill small holes, and exclude border-touching objects. RGB is not supported.
    """
    selected_planes = {"S": (0, 0), "T": (0, 0), "C": (0, 0), "Z": (0, 0)}

    if planes is not None:
        selected_planes.update(planes)

    data, _ = read_tools.read_6darray(
        filepath,
        planes=selected_planes,
        use_dask=False,
        use_xarray=False,
    )
    if not isinstance(data, np.ndarray):
        raise TypeError(f"Expected a NumPy image array from {filepath}, got {type(data).__name__}")

    if data.ndim not in (6, 7) or data.shape[:4] != (1, 1, 1, 1):
        raise ValueError(f"Expected a single STCZ plane from {filepath}, got shape {data.shape}")
    # Remove only acquisition/sample axes; keep Y and X even for one-pixel images.
    image = data[0, 0, 0, 0]

    if image.ndim == 3 and image.shape[-1] == 1:
        image = image[..., 0]

    if image.ndim != 2:
        raise ValueError(f"Expected a grayscale YX plane from {filepath}, got shape {image.shape}")

    # Strict comparison keeps a constant background from becoming foreground.
    mask = image > threshold_otsu(image)
    _, count, _ = ArrayProcessor(mask).label_objects(max_size_remove=10, label_rgb=False)
    return int(count)


async def save_diagnostic_experiment(exp_service: ExperimentServiceStub, experiment_id: str, destination: Path) -> None:
    """Export the configured clone locally without overwriting an earlier snapshot."""
    exported = await exp_service.export(ExperimentServiceExportRequest(experiment_id=experiment_id))
    if not exported.xml.strip():
        raise ValueError(f"ZEN returned empty diagnostic experiment XML for {destination}")
    with destination.open("x", encoding="utf-8") as stream:
        stream.write(exported.xml)
    logger.info(f"Saved configured experiment before acquisition: {destination}")


def move_acquired_files(acquired_files: list[Path], destination_folder: Path) -> None:
    """Check all paths before moving any CZI; never sweep unrelated output files."""
    # Preflight the complete batch so a missing file cannot cause a partial move.
    for source in acquired_files:
        if not source.is_file():
            raise FileNotFoundError(f"Acquired CZI not found: {source}. No run files have been moved.")
        destination = destination_folder / source.name
        if destination.exists():
            raise FileExistsError(f"Refusing to overwrite {destination}. No run files have been moved.")
    for source in acquired_files:
        destination = destination_folder / source.name
        logger.info(f"Moving acquired CZI: {source} -> {destination}")
        shutil.move(str(source), str(destination))
    logger.info(f"Moved {len(acquired_files)} acquired CZI files to: {destination_folder}")


async def main() -> None:
    """Configure each position, optionally save/acquire, then collect completed CZIs."""
    if max_objects_per_well < 1:
        raise ValueError("max_objects_per_well must be positive")
    positions = extract_positions(exp_name)
    print_positions(positions, title=exp_name.name)

    save_path = None
    if run_experiment or save_cloned_experiment:
        timestamp_folder = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
        save_path = target_folder / f"{exp_name.stem}_wellpositions_{timestamp_folder}"
        save_path.mkdir(parents=True, exist_ok=False)
        logger.info(f"Run output folder: {save_path}")

    channel, metadata = initialize_zenapi(config_path)
    acquired_files: list[Path] = []
    objects_per_well: dict[str, int] = {}
    try:
        exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)
        tile_service = TilesServiceStub(channel=channel, metadata=metadata)
        image_output_folder = None
        if run_experiment:
            output = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
            image_output_folder = Path(output.image_output_path)

        my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=exp_name.stem))

        logger.info("Cloning Experiment ...")
        my_exp_cloned = await exp_service.clone(ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id))

        # Reuse one clone, replacing its position list before each acquisition.
        for index, position in enumerate(positions, start=1):
            well_id = position.well_id
            if well_id and objects_per_well.get(well_id, 0) >= max_objects_per_well:
                logger.info(
                    f"Skipping P{index:03d} | Well {well_id}: "
                    f"{objects_per_well[well_id]} objects counted (target {max_objects_per_well})"
                )
                continue

            logger.info(f"Processing position P{index:03d}: {position}")

            logger.info("Clearing TileRegions or Positions...")
            await tile_service.clear(TilesServiceClearRequest(experiment_id=my_exp_cloned.experiment_id))

            # CZEXP coordinates are micrometers; the ZEN API requires meters.
            api_position = Position3D(x=position.x * 1e-6, y=position.y * 1e-6, z=position.z * 1e-6)
            logger.info(
                f"Position {index:04d}: source XYZ (um)=({position.x}, {position.y}, {position.z}); "
                f"API XYZ (m)=({api_position.x}, {api_position.y}, {api_position.z})"
            )

            await tile_service.add_positions(
                TilesServiceAddPositionsRequest(experiment_id=my_exp_cloned.experiment_id, positions=[api_position])
            )

            if save_cloned_experiment and save_path is not None:
                await save_diagnostic_experiment(
                    exp_service, my_exp_cloned.experiment_id, save_path / f"position_{index:04d}.czexp"
                )

            # With acquisition disabled, only configure/export the clone.
            if image_output_folder is None:
                continue

            well = position.well_id or "Unassigned"
            cziname = f"{exp_name.stem}_wellpositions_{well}_P{index:03d}"

            if (image_output_folder / f"{cziname}.czi").exists():
                raise FileExistsError(f"Refusing to overwrite an existing acquisition: {cziname}.czi")

            exp_result = await exp_service.run_experiment(
                ExperimentServiceRunExperimentRequest(experiment_id=my_exp_cloned.experiment_id, output_name=cziname)
            )

            # ZEN may adjust the requested filename, so always use its response.
            output_name = exp_result.output_name

            if not output_name or Path(output_name).name != output_name:
                raise ValueError(f"ZEN returned an invalid output name: {output_name!r}")

            source = image_output_folder / f"{output_name}.czi"

            if source in acquired_files:
                raise ValueError(f"ZEN reused an acquisition output path: {source}")

            acquired_files.append(source)

            object_count = count_czi_objects(source)
            logger.info(f"Object count: {object_count} | Well {well} | P{index:03d} | CZI: {source}")

            # Keep totals by well even if its positions are not adjacent in the list.
            if well_id:
                objects_per_well[well_id] = objects_per_well.get(well_id, 0) + object_count
                logger.info(
                    f"Well {well_id}: cumulative object count {objects_per_well[well_id]} / {max_objects_per_well}"
                )

    finally:
        channel.close()

    # Reached only if every acquisition and analysis succeeded; failures leave CZIs in ZEN's output folder.
    if save_path is not None:
        move_acquired_files(acquired_files, save_path)


if __name__ == "__main__":
    asyncio.run(main())
