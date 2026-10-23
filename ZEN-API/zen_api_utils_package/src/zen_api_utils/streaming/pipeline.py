"""Headless ZEN-API pixel streaming and OME-Zarr writing pipeline.

The module exposes reusable async functions and retains a command-line entry
point for the example launcher and the installed package console script.
"""

import argparse
import asyncio
import contextlib
import itertools
import json
import sys
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import numpy as np
import zarr
from grpclib.const import Cardinality
from grpclib.exceptions import GRPCError, ProtocolError, StreamTerminatedError

# ome-writers
from ome_writers import AcquisitionSettings, Dimension, Plate, Position, create_stream

# ZEN API auto-generated stubs
from zen_api.acquisition.v1beta import (
    ExperimentServiceGetStatusRequest,
    ExperimentServiceLoadRequest,
    ExperimentServiceStub,
    ExperimentStreamingServiceMonitorAllExperimentsRequest,
    ExperimentStreamingServiceMonitorAllExperimentsResponse,
    PixelType,
)
from zen_api_utils.misc import initialize_zenapi, set_logging
from zen_api_utils.experiment_acquisition import (
    AcquisitionDimensions,
    ExperimentAcquisition,
    query_experiment_acquisition,
)
from zen_api_utils.streaming.geometry import (
    TileGeometry,
    calculate_scene_geometry,
)
from zen_api_utils.streaming.omezarr import (
    ExperimentConfig,
    build_progress_bar,
    load_experiment_config,
    open_in_napari_viewer,
    open_in_ndv_viewer,
    start_loaded_experiment,
)

logger = set_logging()

# Default data type for pixel streaming
DEFAULT_DTYPE = np.dtype(np.uint16)

_GRAYSCALE_PIXEL_DTYPES: dict[PixelType, np.dtype] = {
    PixelType.GRAY8: np.dtype(np.uint8),
    PixelType.GRAY16: np.dtype(np.uint16),
}

# Inactivity timeout for matching pixel frames, in seconds.
_STATUS_POLL_TIMEOUT: float = 30.0

__all__ = [
    "IncompleteAcquisitionError",
    "generate_omezarr_pyramids",
    "main",
    "stream_to_omezarr",
    "stream_to_omezarr_with_config",
]


class IncompleteAcquisitionError(RuntimeError):
    """Expected acquisition frames are missing; partial output is retained."""

    def __init__(
        self,
        zarr_path: Path,
        received_frames: int,
        expected_frames: int,
        report_path: Path,
    ) -> None:
        self.zarr_path = zarr_path
        self.received_frames = received_frames
        self.expected_frames = expected_frames
        self.report_path = report_path
        super().__init__(
            f"Incomplete acquisition: received {received_frames}/{expected_frames} frames. "
            f"Completion report: {report_path}"
        )


async def _prepare_acquisition(
    service: ExperimentServiceStub,
    experiment_name: str,
) -> tuple[str, ExperimentAcquisition]:
    """Load and export the selected experiment without starting acquisition."""
    loaded = await service.load(ExperimentServiceLoadRequest(experiment_name=experiment_name))
    if not loaded.experiment_id:
        raise ValueError("ZEN returned an empty experiment ID.")
    acquisition = await query_experiment_acquisition(service, loaded.experiment_id, experiment_name)
    dimensions = acquisition.dimensions
    if (
        min(
            dimensions.time_points,
            dimensions.channels,
            dimensions.z_planes,
            dimensions.scenes,
            dimensions.tiles,
        )
        < 1
    ):
        raise ValueError("Experiment dimensions must be positive.")
    return loaded.experiment_id, acquisition


async def _live_dimensions(
    service: ExperimentServiceStub,
    experiment_id: str,
    fallback: AcquisitionDimensions,
) -> AcquisitionDimensions:
    """Query dimensions for the pinned experiment, falling back to its XML."""
    try:
        response = await service.get_status(ExperimentServiceGetStatusRequest(experiment_id=experiment_id))
    except (GRPCError, OSError, asyncio.TimeoutError) as exc:
        logger.warning(f"Could not query live dimensions; using exported metadata: {exc}")
        return fallback
    status = response.status
    return replace(
        fallback,
        time_points=(status.time_points_count if status.time_points_count > 0 else fallback.time_points),
        channels=(status.channels_count if status.channels_count > 0 else fallback.channels),
        z_planes=(status.zstack_slices_count if status.zstack_slices_count > 0 else fallback.z_planes),
        scenes=status.scenes_count if status.scenes_count > 0 else fallback.scenes,
        tiles=status.tiles_count if status.tiles_count > 0 else fallback.tiles,
    )


def _coordinate_map(
    dimensions: AcquisitionDimensions,
    channel_index: int | None,
) -> dict[tuple[int, int, int, int, int], int]:
    """Map the expected T/S/M/C/Z coordinates to writer order."""
    if channel_index is not None and not 0 <= channel_index < dimensions.channels:
        raise ValueError(f"Channel index {channel_index} is outside the experiment's {dimensions.channels} channels.")
    channels = dimensions.channels if channel_index is None else 1
    return {
        coordinate: index
        for index, coordinate in enumerate(
            itertools.product(
                range(dimensions.time_points),
                range(dimensions.scenes),
                range(dimensions.tiles),
                range(channels),
                range(dimensions.z_planes),
            )
        )
    }


def _record_completion(
    zarr_path: Path,
    experiment_id: str | None,
    coordinates: dict[tuple[int, int, int, int, int], int],
    received: set[int],
    *,
    store_created: bool,
) -> None:
    """Persist completion evidence and reject partial or empty acquisitions."""
    missing = [coordinate for coordinate, index in coordinates.items() if index not in received]
    complete = bool(coordinates) and not missing
    report = {
        "complete": complete,
        "experiment_id": experiment_id,
        "expected_frames": len(coordinates),
        "received_frames": len(received),
        "coordinate_axes": ["t", "s", "m", "c", "z"],
        "missing_coordinates": missing,
    }
    report_path = (
        zarr_path / "acquisition_status.json"
        if store_created
        else zarr_path.with_name(f"{zarr_path.name}.acquisition_status.json")
    )
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if not complete:
        raise IncompleteAcquisitionError(zarr_path, len(received), len(coordinates), report_path)


def _runtime_grayscale_dtype(
    pixel_type: PixelType,
    payload_size: int,
    width: int,
    height: int,
) -> np.dtype:
    """Return and validate the dtype reported by a streamed frame."""
    try:
        dtype = _GRAYSCALE_PIXEL_DTYPES[pixel_type]
    except KeyError as exc:
        name = getattr(pixel_type, "name", str(pixel_type))
        raise ValueError(f"Unsupported streamed pixel type for OME-ZARR: {name}") from exc

    expected_size = width * height * dtype.itemsize
    if payload_size != expected_size:
        raise ValueError(
            "Streamed pixel payload size does not match its runtime "
            f"metadata: got {payload_size} bytes, expected "
            f"{expected_size} for {width}x{height} {pixel_type.name}."
        )
    return dtype


def _plate_row_name(row: int) -> str:
    """Convert a one-based plate row number to its alphabetic name."""
    name = ""
    while row > 0:
        row, remainder = divmod(row - 1, 26)
        name = chr(ord("A") + remainder) + name
    return name


def _build_position_layout(
    ecfg: ExperimentConfig,
    num_s: int,
    num_m: int,
) -> tuple[list[Position], Plate | None]:
    """Build generic positions or an HCS plate layout from ZEN XML metadata."""
    if not ecfg.use_hcs_layout:
        return (
            [
                Position(
                    name=f"S{scene}_M{tile}",
                    grid_row=scene,
                    grid_column=tile,
                )
                for scene in range(num_s)
                for tile in range(num_m)
            ],
            None,
        )

    positions_by_scene = {
        position.get("scene_index"): position
        for position in ecfg.positions
        if isinstance(position.get("scene_index"), int)
    }
    if set(positions_by_scene) != set(range(num_s)):
        if ecfg.positions:
            logger.warning(
                "ZEN XML scene-to-well metadata does not match the live scene count; "
                "writing a generic multiposition OME-ZARR dataset."
            )
        return (
            [
                Position(name=f"S{scene}_M{tile}", grid_row=scene, grid_column=tile)
                for scene in range(num_s)
                for tile in range(num_m)
            ],
            None,
        )

    hcs_positions: list[Position] = []
    max_row = 0
    max_column = 0
    for scene in range(num_s):
        metadata = positions_by_scene[scene]
        row = metadata.get("well_row")
        column = metadata.get("well_column")
        field_index = metadata.get("field_index")
        if not isinstance(row, int) or row < 1 or not isinstance(column, int) or column < 1:
            logger.warning(
                f"ZEN XML contains an invalid well coordinate for scene {scene}; "
                "writing a generic multiposition OME-ZARR dataset."
            )
            return (
                [Position(name=f"S{s}_M{m}", grid_row=s, grid_column=m) for s in range(num_s) for m in range(num_m)],
                None,
            )

        max_row = max(max_row, row)
        max_column = max(max_column, column)
        field = field_index - 1 if isinstance(field_index, int) and field_index > 0 else scene
        for tile in range(num_m):
            name = str(field * num_m + tile)
            hcs_positions.append(
                Position(
                    name=name,
                    plate_row=_plate_row_name(row),
                    plate_column=f"{column:02d}",
                )
            )

    plate = Plate(
        name=ecfg.experiment_name,
        row_names=[_plate_row_name(row) for row in range(1, max_row + 1)],
        column_names=[f"{column:02d}" for column in range(1, max_column + 1)],
    )
    return hcs_positions, plate


def _materialize_hcs_row_groups(zarr_path: Path) -> None:
    """Create explicit Zarr v3 groups for rows referenced by plate wells."""
    root = zarr.open_group(zarr_path, mode="a")
    ome_metadata = root.attrs.get("ome", {})
    plate_metadata = ome_metadata.get("plate", {}) if isinstance(ome_metadata, dict) else {}
    wells = plate_metadata.get("wells", []) if isinstance(plate_metadata, dict) else []
    row_names = {
        well["path"].split("/", maxsplit=1)[0]
        for well in wells
        if isinstance(well, dict) and isinstance(well.get("path"), str) and "/" in well["path"]
    }
    for row_name in row_names:
        root.require_group(row_name)


def _get_multiscale_metadata(
    image_group: Any,
) -> tuple[list[dict[str, Any]], list[float]]:
    """Read axis and scale metadata from an ome-writers image group."""
    ome_metadata = image_group.attrs.get("ome", {})
    multiscales = ome_metadata.get("multiscales", [])
    if not multiscales:
        raise ValueError("Raw tile image has no multiscales metadata")

    multiscale = multiscales[0]
    axes = multiscale.get("axes", [])
    datasets = multiscale.get("datasets", [])
    if not axes or not datasets:
        raise ValueError("Raw tile multiscales metadata is incomplete")

    transformations = datasets[0].get("coordinateTransformations", [])
    scale = next(
        (transformation.get("scale") for transformation in transformations if transformation.get("type") == "scale"),
        None,
    )
    if not isinstance(scale, list) or len(scale) != len(axes):
        raise ValueError("Raw tile image has no valid axis scale")
    return [dict(axis) for axis in axes], [float(value) for value in scale]


def _assemble_scene_mosaics(
    zarr_path: Path,
    tile_geometries: list[TileGeometry],
    keep_source_tiles: bool = False,
    hcs_positions: tuple[dict[str, object], ...] | None = None,
    hcs_tile_count: int | None = None,
) -> None:
    """Create one viewer-compatible image per scene.

    A single spatial tile is finalized in place without copying pixel data.
    Multi-tile scenes are assembled from streamed stage coordinates in
    ascending M-index order, so the highest overlapping M index wins.
    Uncovered regions retain the array fill value. Raw tile images are
    removed after multi-tile assembly unless explicitly retained.

    Args:
        zarr_path: Completed ome-writers Zarr store.
        tile_geometries: First-frame geometry for each observed ``(S, M)``.
        keep_source_tiles: Retain raw tile groups after mosaic assembly.
        hcs_positions: Optional scene-to-well metadata. When provided, scenes
            are created inside their HCS wells.
        hcs_tile_count: Configured number of tiles per HCS scene.
    """
    if not tile_geometries:
        logger.warning("No tile positions were captured; scene assembly skipped.")
        return

    root = zarr.open_group(zarr_path, mode="a")
    hcs_mode = hcs_positions is not None
    if hcs_mode:
        ome_group = None
        ome_metadata: dict[str, Any] = {}
        raw_series: list[str] = []
        positions_by_scene = {
            position.get("scene_index"): position
            for position in hcs_positions
            if isinstance(position.get("scene_index"), int)
        }
    else:
        ome_group = root["OME"]
        ome_metadata = dict(ome_group.attrs.get("ome", {}))
        raw_series = ome_metadata.get("series", [])
        if not isinstance(raw_series, list):
            raise ValueError("OME series metadata is not a path list")

    scenes: dict[int, list[TileGeometry]] = {}
    for tile in tile_geometries:
        scenes.setdefault(tile.scene_index, []).append(tile)

    scene_paths: list[str] = []
    assembled_source_paths: set[str] = set()
    scene_moves: list[tuple[str, str]] = []
    for scene_index in sorted(scenes):
        scene_tiles = sorted(
            scenes[scene_index],
            key=lambda tile: tile.tile_index,
        )
        single_tile = len(scene_tiles) == 1
        geometry = calculate_scene_geometry(scene_tiles)
        source_paths: list[str] = []
        source_arrays: list[Any] = []
        source_names: list[str] = []
        well_path = ""
        scene_name = f"scene_{scene_index}"
        final_scene_name = scene_name
        if hcs_mode:
            position = positions_by_scene.get(scene_index)
            if position is None:
                raise ValueError(f"HCS metadata missing for scene {scene_index}")
            row = position.get("well_row")
            column = position.get("well_column")
            field_index = position.get("field_index")
            if not isinstance(row, int) or not isinstance(column, int):
                raise ValueError("HCS scene has no valid well coordinate")
            field = field_index - 1 if isinstance(field_index, int) and field_index > 0 else scene_index
            well_path = f"{_plate_row_name(row)}/{column:02d}"
            tile_count = hcs_tile_count or max(tile.tile_index for tile in scene_tiles) + 1
            source_names = [str(field * tile_count + placed_tile.tile.tile_index) for placed_tile in geometry.tiles]
            source_paths = [f"{well_path}/{source_name}" for source_name in source_names]
            if single_tile:
                final_scene_name = source_names[0]
            else:
                final_field = len(hcs_positions) * tile_count + field if keep_source_tiles else field
                final_scene_name = str(final_field)
        else:
            for placed_tile in geometry.tiles:
                position_index = placed_tile.tile.position_index
                if position_index >= len(raw_series):
                    raise ValueError("Tile position index exceeds the OME series metadata")
                source_paths.append(raw_series[position_index])
        source_arrays = [root[source_path]["0"] for source_path in source_paths]

        first_array = source_arrays[0]
        source_shape = tuple(first_array.shape)
        source_dtype = np.dtype(first_array.dtype)
        for source_array in source_arrays[1:]:
            if tuple(source_array.shape) != source_shape:
                raise ValueError("All tiles in a scene must have one shape")
            if np.dtype(source_array.dtype) != source_dtype:
                raise ValueError("All tiles in a scene must have one dtype")

        source_group = root[source_paths[0]]
        axes, scale = _get_multiscale_metadata(source_group)
        axis_names = tuple(axis["name"] for axis in axes)
        if axis_names[-2:] != ("y", "x"):
            raise ValueError("Scene tile arrays must end in Y and X axes")

        final_scene_path = f"{well_path}/{final_scene_name}" if hcs_mode else scene_name
        temporary_scene_path = f"{well_path}/{scene_name}" if hcs_mode else scene_name
        reuse_source_group = single_tile and (not keep_source_tiles or source_paths[0] == final_scene_path)
        mosaic_shape_values = list(source_shape)
        mosaic_shape_values[-2:] = [geometry.height, geometry.width]
        z_offsets = [0] * len(geometry.tiles)
        if "z" in axis_names:
            z_axis = axis_names.index("z")
            z_scale = scale[z_axis]
            if z_scale <= 0:
                raise ValueError("Scene Z scale must be positive")
            z_origin = min(placed_tile.tile.position_z for placed_tile in geometry.tiles)
            z_offsets = [
                int(round((placed_tile.tile.position_z - z_origin) / z_scale)) for placed_tile in geometry.tiles
            ]
            mosaic_shape_values[z_axis] = max(z_offset + source_shape[z_axis] for z_offset in z_offsets)
        else:
            z_axis = None
            z_origin = min(placed_tile.tile.position_z for placed_tile in geometry.tiles)
        mosaic_shape = tuple(mosaic_shape_values)
        if reuse_source_group:
            scene_group = source_group
            if source_paths[0] != final_scene_path:
                scene_moves.append((source_paths[0], final_scene_path))
        else:
            if temporary_scene_path in root:
                del root[temporary_scene_path]
            scene_group = root.create_group(temporary_scene_path)
            chunks = tuple(1 for _ in source_shape[:-2]) + (
                min(512, geometry.height),
                min(512, geometry.width),
            )
            mosaic_array = scene_group.create_array(
                "0",
                shape=mosaic_shape,
                dtype=source_dtype,
                chunks=chunks,
                fill_value=0,
                dimension_names=axis_names,
            )

            for plane_index in np.ndindex(mosaic_shape[:-2]):
                mosaic_plane = np.zeros(
                    (geometry.height, geometry.width),
                    dtype=source_dtype,
                )
                for placed_tile, source_array, z_offset in zip(
                    geometry.tiles,
                    source_arrays,
                    z_offsets,
                    strict=True,
                ):
                    source_plane_index = list(plane_index)
                    if z_axis is not None:
                        source_z = plane_index[z_axis] - z_offset
                        if source_z < 0 or source_z >= source_shape[z_axis]:
                            continue
                        source_plane_index[z_axis] = source_z
                    y_slice = slice(
                        placed_tile.y_offset,
                        placed_tile.y_offset + placed_tile.tile.height,
                    )
                    x_slice = slice(
                        placed_tile.x_offset,
                        placed_tile.x_offset + placed_tile.tile.width,
                    )
                    tile_plane = source_array[tuple(source_plane_index) + (slice(None), slice(None))]
                    mosaic_plane[y_slice, x_slice] = tile_plane
                mosaic_array[plane_index + (slice(None), slice(None))] = mosaic_plane

        translation = [0.0] * len(axes)
        if z_axis is not None:
            translation[z_axis] = z_origin
        translation[axis_names.index("y")] = geometry.origin_y
        translation[axis_names.index("x")] = geometry.origin_x
        scene_group.attrs["ome"] = {
            "version": "0.5",
            "multiscales": [
                {
                    "name": f"Scene {scene_index}",
                    "axes": axes,
                    "datasets": [
                        {
                            "path": "0",
                            "coordinateTransformations": [
                                {"type": "scale", "scale": scale},
                                {
                                    "type": "translation",
                                    "translation": translation,
                                },
                            ],
                        }
                    ],
                }
            ],
        }
        scene_group.attrs["zen_scene"] = {
            "scene_index": scene_index,
            "source_tiles_retained": keep_source_tiles,
            "source_tiles": [
                {
                    "path": source_path,
                    "tile_index": placed_tile.tile.tile_index,
                    "stage_position_xyz": [
                        placed_tile.tile.center_x,
                        placed_tile.tile.center_y,
                        placed_tile.tile.position_z,
                    ],
                    "translation_yx": [
                        placed_tile.translation_y,
                        placed_tile.translation_x,
                    ],
                }
                for source_path, placed_tile in zip(
                    source_paths,
                    geometry.tiles,
                    strict=True,
                )
            ],
            "overlap_policy": "higher_m_index",
        }
        if not reuse_source_group:
            assembled_source_paths.update(source_paths)
        if hcs_mode:
            well_group = root[well_path]
            well_ome = dict(cast(dict[str, Any], well_group.attrs.get("ome", {})))
            well_metadata = dict(cast(dict[str, Any], well_ome.get("well", {})))
            images = well_metadata.get("images", [])
            source_name_set = set(source_names)
            well_metadata["images"] = [
                image for image in images if isinstance(image, dict) and image.get("path") not in source_name_set
            ] + [{"path": final_scene_name}]
            well_ome["well"] = well_metadata
            well_group.attrs["ome"] = well_ome
            if not reuse_source_group:
                scene_moves.append(
                    (
                        temporary_scene_path,
                        final_scene_path,
                    )
                )
        else:
            scene_paths.append(final_scene_path)
        if reuse_source_group:
            logger.info(
                f"Finalized scene {scene_index} from 1 spatial tile " f"without pixel copy: shape={mosaic_shape}"
            )
        elif single_tile:
            logger.info(
                f"Copied scene {scene_index} from 1 spatial tile to preserve " f"the source group: shape={mosaic_shape}"
            )
        else:
            logger.info(
                f"Assembled scene {scene_index} from {len(scene_tiles)} " f"spatial tiles: shape={mosaic_shape}"
            )

    if not hcs_mode:
        ome_metadata["series"] = scene_paths
        assert ome_group is not None
        ome_group.attrs["ome"] = ome_metadata
    if not keep_source_tiles:
        for source_path in assembled_source_paths:
            if source_path in root:
                del root[source_path]
        if assembled_source_paths:
            logger.info(f"Removed {len(assembled_source_paths)} source tile groups " "after scene assembly.")
    for source_path, final_path in scene_moves:
        if final_path in root:
            del root[final_path]
        (zarr_path / source_path).replace(zarr_path / final_path)


def _find_omezarr_image_paths(zarr_path: Path) -> list[Path]:
    """Find regular or HCS image groups containing multiscales metadata."""
    root = zarr.open_group(zarr_path, mode="r")
    if "OME" in root:
        ome_metadata = root["OME"].attrs.get("ome", {})
        series = ome_metadata.get("series", []) if isinstance(ome_metadata, dict) else []
        if isinstance(series, list) and series:
            return [zarr_path / path for path in series if isinstance(path, str)]

    image_paths: list[Path] = []

    def visit(group: zarr.Group, group_path: Path) -> None:
        ome_metadata = group.attrs.get("ome", {})
        if isinstance(ome_metadata, dict) and isinstance(ome_metadata.get("multiscales"), list):
            image_paths.append(group_path)
            return
        for name, subgroup in group.groups():
            visit(subgroup, group_path / name)

    visit(root, zarr_path)
    return image_paths


def generate_omezarr_pyramids(
    zarr_path: str | Path,
    pyramid_levels: int,
    spatial_shard_size_chunks: int | None = 2,
) -> None:
    """Append Y/X pyramid levels after acquisition without rewriting level 0."""
    if pyramid_levels < 1:
        raise ValueError("pyramid_levels must be at least 1")

    import ngff_zarr as nz

    zarr_path = Path(zarr_path)
    image_paths = _find_omezarr_image_paths(zarr_path)
    if not image_paths:
        raise RuntimeError(f"No OME-Zarr image groups found in: {zarr_path}")

    chunks_per_shard = (
        {"y": spatial_shard_size_chunks, "x": spatial_shard_size_chunks}
        if spatial_shard_size_chunks is not None
        else None
    )

    logger.info(f"Generating {pyramid_levels} pyramid level(s) for {len(image_paths)} image(s) ...")
    for image_index, image_path in enumerate(image_paths, start=1):
        existing = nz.from_ngff_zarr(image_path, validate=True)
        base_image = existing.images[0]
        if not {"y", "x"}.issubset(base_image.dims):
            raise RuntimeError(f"OME-Zarr image has no Y/X axes: {image_path}")

        spatial_dims = [dim for dim in base_image.dims if dim in {"z", "y", "x"}]
        scale_factors = [
            {dim: 2**level if dim in {"y", "x"} else 1 for dim in spatial_dims}
            for level in range(1, pyramid_levels + 1)
        ]
        chunks = tuple(int(chunk) for chunk in base_image.data.chunksize)
        multiscales = nz.to_multiscales(
            base_image,
            scale_factors=scale_factors,
            method=nz.Methods.ITKWASM_GAUSSIAN,
            chunks=chunks,
            cache=True,
        )
        for level, dataset in enumerate(multiscales.metadata.datasets):
            dataset.path = str(level)

        # start_level=1 binds the existing array at path "0" as read-only.
        # Sharding is configured only on the newly written levels.
        nz.to_ome_zarr(
            image_path,
            multiscales,
            version="0.5",
            overwrite=False,
            start_level=1,
            chunks_per_shard=chunks_per_shard,
        )
        logger.info(f"Pyramid image {image_index}/{len(image_paths)} complete: {image_path}")

    logger.info(f"OME-Zarr pyramid generation completed: {zarr_path}")


async def _merge_channel_streams(
    streams: list[tuple[int, AsyncIterable[Any]]],
) -> AsyncIterator[tuple[int, Any]]:
    """Merge explicit channel subscriptions into one asynchronous stream."""
    iterators = [(output_channel, stream.__aiter__()) for output_channel, stream in streams]
    tasks = {
        asyncio.create_task(stream_iter.__anext__()): (output_channel, stream_iter)
        for output_channel, stream_iter in iterators
    }
    try:
        while tasks:
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                output_channel, stream_iter = tasks.pop(task)
                try:
                    response = task.result()
                except StopAsyncIteration:
                    continue
                tasks[asyncio.create_task(stream_iter.__anext__())] = (output_channel, stream_iter)
                yield output_channel, response
    finally:
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


async def _close_async_iterator(iterator: AsyncIterator[Any]) -> None:
    """Close an asynchronous iterator when its implementation supports it."""
    close = getattr(iterator, "aclose", None)
    if close is not None:
        await close()


async def _cancel_channel_stream(stream: Any) -> None:
    """Cancel a persistent monitor before its context waits for trailers."""
    with contextlib.suppress(ProtocolError, StreamTerminatedError):
        await stream.cancel()


async def _open_channel_streams(
    channel: Any,
    metadata: Any,
    source_channels: list[int],
    resources: contextlib.AsyncExitStack,
) -> list[tuple[int, AsyncIterable[Any]]]:
    """Send monitoring requests before returning control to acquisition."""
    streams = []
    for output_channel, source_channel in enumerate(source_channels):
        request = ExperimentStreamingServiceMonitorAllExperimentsRequest(
            channel_index=source_channel,
            enable_raw_data=False,
        )
        stream = await resources.enter_async_context(
            channel.request(
                "/zen_api.acquisition.v1beta.ExperimentStreamingService/MonitorAllExperiments",
                Cardinality.UNARY_STREAM,
                type(request),
                ExperimentStreamingServiceMonitorAllExperimentsResponse,
                metadata=metadata,
            )
        )
        await stream.send_message(request, end=True)
        resources.push_async_callback(_cancel_channel_stream, stream)
        streams.append((output_channel, stream))
    return streams


async def stream_to_omezarr(
    zenapi_config: str | Path,
    experiment_name: str,
    output_dir: str | Path,
    dtype: np.dtype | None = None,
    start_experiment_from_script: bool = False,
    czi_name: str = "zenapi_stream",
    overwrite_czi: bool = True,
    channel_index: int | None = None,
    overwrite_zarr: bool = True,
    compression: str | None = "blosc-zstd",
    spatial_shard_size_chunks: int | None = 2,
    inactivity_timeout: float = _STATUS_POLL_TIMEOUT,
) -> Path:
    """Stream ZEN pixel data into an OME-ZARR file.

    Args:
        zenapi_config: Path to the ZEN-API gateway config.ini.
        experiment_name: ZEN experiment name (without .czexp).
        output_dir: Folder where the OME-ZARR will be created.
        dtype: Pixel data type (must match the experiment output).
        start_experiment_from_script: If True, start the experiment via API.
            If False, the user starts the experiment from the ZEN UI.
        czi_name: CZI output name when starting experiment from script.
        overwrite_czi: Allow overwriting an existing CZI.
        channel_index: Optional channel filter index (None = all channels).
        overwrite_zarr: Overwrite an existing OME-ZARR at the output path.
        compression: Compression for ZARR
            ('blosc-zstd', 'blosc-lz4', 'zstd', 'none', or None).
        spatial_shard_size_chunks: Number of chunks per Y/X shard, or None
            to disable Zarr v3 sharding.
        inactivity_timeout: Maximum wait for another matching frame.
            Missing expected coordinates fail the acquisition.

    Returns:
        Path to the created OME-ZARR directory.

    Raises:
        IncompleteAcquisitionError: Expected frames are missing. Partial
            data and a completion report are retained, without finalization.
    """
    channel, metadata = initialize_zenapi(zenapi_config)
    try:
        async with contextlib.AsyncExitStack() as resources:
            return await _stream_to_omezarr_connected(
                zenapi_config=zenapi_config,
                experiment_name=experiment_name,
                output_dir=output_dir,
                dtype=dtype,
                start_experiment_from_script=start_experiment_from_script,
                czi_name=czi_name,
                overwrite_czi=overwrite_czi,
                channel_index=channel_index,
                overwrite_zarr=overwrite_zarr,
                compression=compression,
                spatial_shard_size_chunks=spatial_shard_size_chunks,
                inactivity_timeout=inactivity_timeout,
                channel=channel,
                metadata=metadata,
                resources=resources,
            )
    finally:
        channel.close()


async def _stream_to_omezarr_connected(
    zenapi_config: str | Path,
    experiment_name: str,
    output_dir: str | Path,
    dtype: np.dtype | None,
    start_experiment_from_script: bool,
    czi_name: str,
    overwrite_czi: bool,
    channel_index: int | None,
    overwrite_zarr: bool,
    compression: str | None,
    spatial_shard_size_chunks: int | None,
    inactivity_timeout: float,
    channel: Any,
    metadata: Any,
    resources: contextlib.AsyncExitStack,
) -> Path:
    """Implement buffered streaming using an exception-safe connection."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # derive OME-ZARR name from experiment + timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zarr_name = f"{experiment_name}_{timestamp}.ome.zarr"
    zarr_path = output_dir / zarr_name
    logger.info(f"OME-ZARR output path: {zarr_path}")

    experiment_service = ExperimentServiceStub(channel=channel, metadata=metadata)
    loaded_id, acquisition = await _prepare_acquisition(experiment_service, experiment_name)
    acquired_dimensions = acquisition.dimensions
    coord_to_linear = _coordinate_map(acquired_dimensions, channel_index)
    source_channels = [channel_index] if channel_index is not None else list(range(acquired_dimensions.channels))
    streams = await _open_channel_streams(channel, metadata, source_channels, resources)
    async_iter = _merge_channel_streams(streams)
    resources.push_async_callback(_close_async_iterator, async_iter)
    target_experiment_id = loaded_id if start_experiment_from_script else None

    # ----- now optionally start the experiment -----
    if start_experiment_from_script:
        logger.info(f"Starting experiment '{experiment_name}' via ZEN-API ...")
        czi_path = await start_loaded_experiment(
            service=experiment_service,
            experiment_id=loaded_id,
            czi_name=czi_name,
            overwrite=overwrite_czi,
        )
        logger.info(f"Experiment ID: {loaded_id}")
        logger.info(f"CZI file will be saved to: {czi_path}")
    else:
        logger.info(
            "Waiting for experiment to be started from ZEN UI. "
            f"Stream stops after {inactivity_timeout:.0f}s of inactivity."
        )

    frames: list[np.ndarray] = []
    frame_coords: list[dict] = []  # list of {t, z, c, m, s} per frame
    frame_metadata_list: list[dict] = []
    tile_geometry_data: dict[
        tuple[int, int],
        tuple[float, float, float, float, float, int, int],
    ] = {}

    received_indices: set[int] = set()

    frame_height: int | None = None
    frame_width: int | None = None
    scale_x: float | None = None
    scale_y: float | None = None

    frame_count = 0

    logger.info("Receiving pixel stream ...")

    # We iterate the gRPC stream manually (via __aiter__ + __anext__)
    # instead of `async for` so we can wrap each step in wait_for() to
    # detect inactivity (no frame for `inactivity_timeout` seconds).
    # Experiment status is intentionally not used for completion because
    # ZEN can report "finished" before all pixel data reaches this stream.
    deadline = asyncio.get_running_loop().time() + inactivity_timeout
    while True:
        try:
            remaining = max(0.0, deadline - asyncio.get_running_loop().time())
            stream_c, response = await asyncio.wait_for(async_iter.__anext__(), timeout=remaining)
        except asyncio.TimeoutError:
            logger.warning(f"No matching frames for {inactivity_timeout:.0f}s; checking acquisition completeness.")
            break
        except StopAsyncIteration:
            break

        fd = response.frame_data
        if not fd.experiment_id:
            continue
        if target_experiment_id is None:
            target_experiment_id = fd.experiment_id
        if fd.experiment_id != target_experiment_id:
            continue
        fp = fd.frame_position

        if frame_height is None:
            acquired_dimensions = await _live_dimensions(experiment_service, target_experiment_id, acquired_dimensions)
            if channel_index is None and acquired_dimensions.channels != len(source_channels):
                raise ValueError(
                    "Live channel count differs from the exported experiment metadata: "
                    f"{acquired_dimensions.channels} != {len(source_channels)}. "
                    "Acquisition cannot be recorded safely."
                )
            coord_to_linear = _coordinate_map(acquired_dimensions, channel_index)

        # Extract 5-D acquisition coordinate of this frame.
        t = fp.t
        z = fp.z
        c = stream_c
        m = fp.m  # tile index
        s = fp.s  # scene index
        linear_index = coord_to_linear.get((t, s, m, c, z))
        if linear_index is None:
            raise ValueError(f"Frame coordinate {(t, s, m, c, z)} is outside the expected acquisition.")
        if linear_index in received_indices:
            continue

        full_size = fd.frame_size
        frame_dtype = _runtime_grayscale_dtype(
            fd.pixel_data.pixel_type,
            len(fd.pixel_data.raw_data),
            full_size.width,
            full_size.height,
        )
        if dtype is None:
            dtype = frame_dtype
            logger.info(f"Using runtime stream pixel type " f"{fd.pixel_data.pixel_type.name} ({dtype}).")
        elif np.dtype(dtype) != frame_dtype:
            raise ValueError(
                "Configured dtype does not match the streamed pixel type: " f"{np.dtype(dtype)} != {frame_dtype}."
            )

        # ZEN API reports scaling in metres; convert to µm for OME metadata.
        sx = fd.scaling.x * 1e6  # m -> µm
        sy = fd.scaling.y * 1e6

        # Stage positions also in metres -> µm.
        # type: ignore[operator]: stubs declare float | None but values are
        # always numeric during an active acquisition.
        stage_x = fd.frame_stage_position.x * 1e6  # type: ignore[operator]
        stage_y = fd.frame_stage_position.y * 1e6  # type: ignore[operator]
        stage_z = fd.frame_stage_position.z * 1e6  # type: ignore[operator]

        # pixel_data.raw_data is a flat bytes buffer; reshape to (H, W).
        frame = np.frombuffer(fd.pixel_data.raw_data, dtype=dtype).reshape((full_size.height, full_size.width))

        if frame_height is not None and frame.shape != (frame_height, frame_width):
            raise ValueError(
                "Streamed frame shape changed during acquisition: " f"{(frame_height, frame_width)} to {frame.shape}."
            )

        # ZEN payloads are already row-major (height, width). Keep the
        # payload orientation so OME-Zarr Y/X match the frame metadata.
        frame = np.ascontiguousarray(frame, dtype=dtype)

        # Accumulate frames and coordinates for the second-pass write.
        frames.append(frame)
        frame_coords.append({"t": t, "z": z, "c": c, "m": m, "s": s})
        frame_metadata_list.append(
            {
                "position_x": stage_x,
                "position_y": stage_y,
                "position_z": stage_z,
            }
        )
        tile_key = (s, m)
        if tile_key not in tile_geometry_data or z == 0:
            tile_geometry_data[tile_key] = (
                stage_x,
                stage_y,
                stage_z,
                sx,
                sy,
                frame.shape[0],
                frame.shape[1],
            )

        # Capture pixel dimensions and physical scale from the first frame.
        if frame_height is None:
            frame_height = frame.shape[0]
            frame_width = frame.shape[1]
            scale_x = sx
            scale_y = sy

        received_indices.add(linear_index)
        frame_count = len(received_indices)

        # progress
        sys.stdout.write(build_progress_bar(frame_count, None))
        sys.stdout.flush()
        deadline = asyncio.get_running_loop().time() + inactivity_timeout
        if frame_count == len(coord_to_linear):
            break

    # newline after progress bar
    sys.stdout.write("\n")
    logger.info(f"Stream finished. Total frames received: {frame_count}")

    if frame_count == 0:
        _record_completion(
            zarr_path,
            target_experiment_id,
            coord_to_linear,
            received_indices,
            store_created=False,
        )

    num_t = acquired_dimensions.time_points
    num_z = acquired_dimensions.z_planes
    num_c = acquired_dimensions.channels if channel_index is None else 1
    num_m = acquired_dimensions.tiles
    num_s = acquired_dimensions.scenes

    # Total positions = scenes * tiles
    num_positions = num_s * num_m
    tile_geometries = [
        TileGeometry(
            scene_index=scene_index,
            tile_index=tile_index,
            position_index=scene_index * num_m + tile_index,
            center_x=geometry[0],
            center_y=geometry[1],
            position_z=geometry[2],
            scale_x=geometry[3],
            scale_y=geometry[4],
            height=geometry[5],
            width=geometry[6],
        )
        for (scene_index, tile_index), geometry in sorted(tile_geometry_data.items())
    ]

    # Build the dimension list
    dimensions: list[Dimension] = []

    if num_t > 1:
        dimensions.append(Dimension(name="t", count=num_t, chunk_size=1, type="time"))

    # positions (scenes x tiles)
    if num_positions > 1:
        pos_coords = []
        for s_idx in range(num_s):
            for m_idx in range(num_m):
                pos_coords.append(Position(name=f"S{s_idx}_M{m_idx}", grid_row=s_idx, grid_column=m_idx))
        dimensions.append(Dimension(name="p", type="position", coords=pos_coords))  # type: ignore[arg-type]

    if num_c > 1:
        dimensions.append(Dimension(name="c", count=num_c, chunk_size=1, type="channel"))

    if num_z > 1:
        # compute z_spacing from stage positions of the first Z-stack
        z_stage_positions: dict[int, float] = {}
        for fc, fmeta in zip(frame_coords, frame_metadata_list):
            z_idx = fc["z"]
            if z_idx not in z_stage_positions:
                z_stage_positions[z_idx] = fmeta["position_z"]
            if len(z_stage_positions) == num_z:
                break
        if len(z_stage_positions) >= 2:
            sorted_z = sorted(z_stage_positions.items())
            z_spacing = abs(sorted_z[1][1] - sorted_z[0][1])
            if z_spacing == 0:
                z_spacing = 1.0
        else:
            z_spacing = 1.0
        logger.info(f"Z spacing from stage positions: {z_spacing:.4f} µm")

        dimensions.append(
            Dimension(
                name="z",
                count=num_z,
                chunk_size=max(1, num_z),
                type="space",
                scale=z_spacing,
                unit="um",
            )
        )

    # Y and X (always present, must be last two).
    # frame_height/width are guaranteed non-None since frame_count > 0.
    assert frame_height is not None and frame_width is not None
    dimensions.append(
        Dimension(
            name="y",
            count=frame_height,
            chunk_size=min(512, frame_height),
            shard_size_chunks=spatial_shard_size_chunks,
            type="space",
            scale=scale_y,
            unit="um",
        )
    )
    dimensions.append(
        Dimension(
            name="x",
            count=frame_width,
            chunk_size=min(512, frame_width),
            shard_size_chunks=spatial_shard_size_chunks,
            type="space",
            scale=scale_x,
            unit="um",
        )
    )

    settings = AcquisitionSettings(
        root_path=str(zarr_path),
        dimensions=tuple(dimensions),
        dtype=str(dtype),
        format="ome-zarr",  # type: ignore[arg-type]  # ome-writers accepts str
        compression=compression,  # type: ignore[arg-type]  # ome-writers accepts str
        overwrite=overwrite_zarr,
    )

    logger.info(f"AcquisitionSettings created: shape={settings.shape}")
    total_expected = settings.num_frames
    logger.info(f"Total expected frames: {total_expected}")

    # ----- sort frames into acquisition order (t, p, c, z) -----
    # ome-writers expects frames in the order defined by the dimensions list.
    # Build a mapping from (t, s, m, c, z) -> frame index, then iterate in order.

    coord_to_idx: dict[tuple, int] = {}
    for idx, fc in enumerate(frame_coords):
        key = (fc["t"], fc["s"], fc["m"], fc["c"], fc["z"])
        coord_to_idx[key] = idx

    # ----- write to OME-ZARR -----
    # itertools.product generates (t, s, m, c, z) tuples in the same
    # T→S→M→C→Z order as the dimension list.
    logger.info(f"Writing {frame_count} frames to OME-ZARR ...")
    written = 0

    with create_stream(settings) as stream:
        coords = itertools.product(range(num_t), range(num_s), range(num_m), range(num_c), range(num_z))
        for t_idx, s_idx, m_idx, c_idx, z_idx in coords:
            key = (t_idx, s_idx, m_idx, c_idx, z_idx)
            if key in coord_to_idx:
                fidx = coord_to_idx[key]
                stream.append(
                    frames[fidx],
                    frame_metadata=frame_metadata_list[fidx],
                )
            else:
                stream.append(np.zeros((frame_height, frame_width), dtype=dtype))
                logger.warning(f"Missing frame at " f"T={t_idx} S={s_idx} M={m_idx} C={c_idx} Z={z_idx}")

            written += 1
            sys.stdout.write(build_progress_bar(written, total_expected))
            sys.stdout.flush()

    sys.stdout.write("\n")
    _record_completion(
        zarr_path,
        target_experiment_id,
        coord_to_linear,
        received_indices,
        store_created=True,
    )
    if num_positions > 1:
        _assemble_scene_mosaics(zarr_path, tile_geometries)
    logger.info(f"OME-ZARR written successfully: {zarr_path}")
    return zarr_path


async def stream_to_omezarr_with_config(
    ecfg: ExperimentConfig,
    inactivity_timeout: float = _STATUS_POLL_TIMEOUT,
) -> Path:
    """Stream ZEN pixel data into OME-ZARR using exported experiment dimensions.

    Export the selected experiment before opening channel subscriptions.
    The first matching frame supplies its pixel size and live dimensions;
    subsequent frames are written with bounded out-of-order buffering.

    Args:
        ecfg: Writer and experiment settings. Exported metadata replaces
            dimension hints without mutating this configuration object.
        inactivity_timeout: Maximum wait for another matching frame.

    Returns:
        Path to the created OME-ZARR directory.

    Raises:
        IncompleteAcquisitionError: Expected frames are missing. Partial
            data and a completion report are retained, without finalization.
    """
    channel, metadata = initialize_zenapi(ecfg.zenapi_config)
    try:
        async with contextlib.AsyncExitStack() as resources:
            return await _stream_to_omezarr_with_config_connected(
                ecfg,
                inactivity_timeout,
                channel,
                metadata,
                resources,
            )
    finally:
        channel.close()


async def _stream_to_omezarr_with_config_connected(
    ecfg: ExperimentConfig,
    inactivity_timeout: float,
    channel: Any,
    metadata: Any,
    resources: contextlib.AsyncExitStack,
) -> Path:
    """Implement configured streaming using an exception-safe connection."""
    dtype: np.dtype | None = None
    configured_dtype = np.dtype(ecfg.dtype)
    output_dir = Path(ecfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zarr_name = f"{ecfg.experiment_name}_{timestamp}.ome.zarr"
    zarr_path = output_dir / zarr_name
    logger.info(f"OME-ZARR output path: {zarr_path}")

    experiment_service = ExperimentServiceStub(channel=channel, metadata=metadata)
    loaded_id, acquisition = await _prepare_acquisition(experiment_service, ecfg.experiment_name)
    acquired_dimensions = acquisition.dimensions
    ecfg = replace(
        ecfg,
        time_points=acquired_dimensions.time_points,
        channels=acquired_dimensions.channels,
        z_planes=acquired_dimensions.z_planes,
        z_spacing=acquired_dimensions.z_spacing,
        tiles=acquired_dimensions.tiles,
        scenes=acquired_dimensions.scenes,
        positions=acquisition.positions,
    )
    num_t, num_c, num_z = ecfg.time_points, ecfg.channels, ecfg.z_planes
    num_m, num_s = ecfg.tiles, ecfg.scenes
    coord_to_linear = _coordinate_map(acquired_dimensions, ecfg.channel_index)
    source_channels = [ecfg.channel_index] if ecfg.channel_index is not None else list(range(num_c))
    streams = await _open_channel_streams(channel, metadata, source_channels, resources)
    async_iter = _merge_channel_streams(streams)
    resources.push_async_callback(_close_async_iterator, async_iter)
    target_experiment_id = loaded_id if ecfg.start_from_script else None
    logger.info(
        "Pixel streams opened for "
        + (
            f"selected channel {ecfg.channel_index}."
            if ecfg.channel_index is not None
            else f"all {len(source_channels)} channels."
        )
    )

    # ----- now optionally start the experiment -----
    if ecfg.start_from_script:
        logger.info(f"Starting experiment '{ecfg.experiment_name}' via ZEN-API ...")
        czi_path = await start_loaded_experiment(
            service=experiment_service,
            experiment_id=loaded_id,
            czi_name=ecfg.czi_name,
            overwrite=ecfg.overwrite_czi,
        )
        logger.info(f"Experiment ID: {loaded_id}")
        logger.info(f"CZI file will be saved to: {czi_path}")
    else:
        logger.info(
            "Waiting for experiment to be started from ZEN UI. "
            f"Stream stops after {inactivity_timeout:.0f}s of inactivity."
        )

    # We receive frames in the order ZEN sends them which may differ from
    # the dimension iteration order above.  Buffer out-of-order frames in
    # a small look-ahead window and flush in-order as soon as possible.
    pending: dict[int, tuple[np.ndarray, dict]] = {}
    received_indices: set[int] = set()
    tile_geometries: dict[tuple[int, int], TileGeometry] = {}
    next_write = 0
    frame_count = 0

    # The OME-ZARR stream and settings are created lazily after the first
    # frame arrives (we need its size and pixel scaling).
    zarr_stream = None
    zarr_resources = contextlib.ExitStack()
    resources.callback(zarr_resources.close)
    settings = None
    plate = None
    total_expected = len(coord_to_linear)

    logger.info("Waiting for first frame to determine frame size ...")

    # We iterate the gRPC stream manually (via __aiter__ + __anext__)
    # instead of `async for` so we can wrap each step in wait_for() to
    # detect inactivity (no frame for `inactivity_timeout` seconds).
    # Live status supplies the authoritative stream dimensions after the
    # first frame, so completion is based on unique expected coordinates.
    # Intentionally NO status-monitor stop_event here: ZEN delivers the
    # experiment-finished status *before* all pixel data has been pushed
    # through gRPC, so reacting to it would truncate the write.
    deadline = asyncio.get_running_loop().time() + inactivity_timeout
    while True:
        try:
            remaining = max(0.0, deadline - asyncio.get_running_loop().time())
            stream_c, response = await asyncio.wait_for(async_iter.__anext__(), timeout=remaining)
        except asyncio.TimeoutError:
            logger.warning(f"No matching frames for {inactivity_timeout:.0f}s; checking acquisition completeness.")
            break
        except StopAsyncIteration:
            break
        fd = response.frame_data
        if not fd.experiment_id:
            continue
        if target_experiment_id is None:
            target_experiment_id = fd.experiment_id
        if fd.experiment_id != target_experiment_id:
            continue
        fp = fd.frame_position

        t, z, m, s = fp.t, fp.z, fp.m, fp.s
        c = stream_c

        full_size = fd.frame_size
        frame_dtype = _runtime_grayscale_dtype(
            fd.pixel_data.pixel_type,
            len(fd.pixel_data.raw_data),
            full_size.width,
            full_size.height,
        )
        if dtype is None:
            dtype = frame_dtype
            logger.info(f"Using runtime stream pixel type " f"{fd.pixel_data.pixel_type.name} ({dtype}).")
            if dtype != configured_dtype:
                logger.warning(
                    f"Configured dtype {configured_dtype} differs from runtime "
                    f"dtype {dtype}; using the runtime value."
                )
        elif frame_dtype != dtype:
            raise ValueError("Streamed pixel type changed during acquisition: " f"{dtype} to {frame_dtype}.")

        sx = fd.scaling.x * 1e6
        sy = fd.scaling.y * 1e6
        stage_x = fd.frame_stage_position.x * 1e6  # type: ignore[operator]  # ZEN API stubs type x/y/z as float | None
        stage_y = fd.frame_stage_position.y * 1e6  # type: ignore[operator]
        stage_z = fd.frame_stage_position.z * 1e6  # type: ignore[operator]

        frame = np.frombuffer(fd.pixel_data.raw_data, dtype=dtype).reshape((full_size.height, full_size.width))
        # ZEN payloads are already row-major (height, width). Keep the
        # payload orientation so OME-Zarr Y/X match the frame metadata.
        frame = np.ascontiguousarray(frame, dtype=dtype)

        frame_meta = {
            "position_x": stage_x,
            "position_y": stage_y,
            "position_z": stage_z,
        }

        # ----- on the very first frame, build the OME-ZARR settings & open the stream -----
        if zarr_stream is None:
            live = await _live_dimensions(experiment_service, target_experiment_id, acquired_dimensions)
            if ecfg.channel_index is None and live.channels != len(source_channels):
                raise ValueError(
                    "Live channel count differs from the exported experiment metadata: "
                    f"{live.channels} != {len(source_channels)}. Acquisition cannot be recorded safely."
                )
            coord_to_linear = _coordinate_map(live, ecfg.channel_index)
            num_t, num_z, num_m, num_s = (
                live.time_points,
                live.z_planes,
                live.tiles,
                live.scenes,
            )
            num_c = live.channels if ecfg.channel_index is None else 1
            num_positions = num_s * num_m
            frame_height, frame_width = frame.shape
            scale_x = sx
            scale_y = sy

            logger.info(
                f"Frame size from stream: {frame_height}x{frame_width}, "
                f"pixel scale: {scale_x:.4f} x {scale_y:.4f} µm"
            )
            logger.info(
                f"Known dimensions: T={num_t}, C={num_c}, Z={num_z}, "
                f"Tiles(M)={num_m}, Scenes(S)={num_s}, "
                f"Frame={frame_height}x{frame_width}"
            )

            dimensions: list[Dimension] = []
            pos_coords, plate = _build_position_layout(ecfg, num_s, num_m)

            if num_t > 1:
                dimensions.append(Dimension(name="t", count=num_t, chunk_size=1, type="time"))

            if num_positions > 1 or plate is not None:
                dimensions.append(Dimension(name="p", type="position", coords=pos_coords))  # type: ignore[arg-type]

            if num_c > 1:
                dimensions.append(Dimension(name="c", count=num_c, chunk_size=1, type="channel"))

            if num_z > 1:
                dimensions.append(
                    Dimension(
                        name="z",
                        count=num_z,
                        chunk_size=max(1, num_z),
                        type="space",
                        scale=ecfg.z_spacing,
                        unit="um",
                    )
                )

            dimensions.append(
                Dimension(
                    name="y",
                    count=frame_height,
                    chunk_size=min(512, frame_height),
                    shard_size_chunks=ecfg.spatial_shard_size_chunks,
                    type="space",
                    scale=scale_y,
                    unit="um",
                )
            )
            dimensions.append(
                Dimension(
                    name="x",
                    count=frame_width,
                    chunk_size=min(512, frame_width),
                    shard_size_chunks=ecfg.spatial_shard_size_chunks,
                    type="space",
                    scale=scale_x,
                    unit="um",
                )
            )

            settings = AcquisitionSettings(
                root_path=str(zarr_path),
                dimensions=tuple(dimensions),
                dtype=str(dtype),
                format="ome-zarr",  # type: ignore[arg-type]  # ome-writers accepts str
                compression=ecfg.compression,  # type: ignore[arg-type]  # ome-writers accepts str
                plate=plate,
                overwrite=ecfg.overwrite_zarr,
            )

            if plate is not None:
                logger.info(
                    "OME-ZARR HCS layout enabled for wells: "
                    + ", ".join(
                        dict.fromkeys(f"{position.plate_row}{position.plate_column}" for position in pos_coords)
                    )
                )

            total_expected = settings.num_frames
            logger.info(f"AcquisitionSettings: shape={settings.shape}  total_frames={total_expected}")
            logger.info("Receiving & writing pixel stream on-the-fly ...")

            zarr_stream = zarr_resources.enter_context(create_stream(settings))

        # ----- process the current frame -----
        key = (t, s, m, c, z)
        lin_idx = coord_to_linear.get(key)
        if lin_idx is None:
            raise ValueError(f"Frame coordinate {key} is outside the expected acquisition.")

        tile_key = (s, m)
        if tile_key not in tile_geometries or z == 0:
            tile_geometries[tile_key] = TileGeometry(
                scene_index=s,
                tile_index=m,
                position_index=s * num_m + m,
                center_x=stage_x,
                center_y=stage_y,
                position_z=stage_z,
                scale_x=sx,
                scale_y=sy,
                height=frame.shape[0],
                width=frame.shape[1],
            )

        if lin_idx in received_indices:
            logger.warning(f"Duplicate coordinate {key} – ignoring frame.")
            continue

        received_indices.add(lin_idx)
        frame_count = len(received_indices)

        # Buffer the frame; flush everything we can write in order
        pending[lin_idx] = (frame, frame_meta)

        while next_write in pending:
            frm, fmeta = pending.pop(next_write)
            zarr_stream.append(frm, frame_metadata=fmeta)
            next_write += 1
            sys.stdout.write(build_progress_bar(next_write, total_expected))
            sys.stdout.flush()

        if len(pending) > ecfg.max_pending_frames:
            raise BufferError(
                "Out-of-order pixel buffer exceeded "
                f"max_pending_frames={ecfg.max_pending_frames}; "
                f"next expected linear index is {next_write}."
            )
            deadline = asyncio.get_running_loop().time() + inactivity_timeout

        # All expected frames received – break out of the gRPC stream
        # (monitor_all_experiments does not terminate on its own).
        if len(received_indices) == len(coord_to_linear):
            logger.info(
                f"Closing pixel stream (received {frame_count}/{total_expected} frames, "
                f"last linear index={lin_idx})."
            )
            break

    if zarr_stream is not None:
        missing_frame = np.zeros((frame_height, frame_width), dtype=dtype)
        while next_write < len(coord_to_linear):
            if next_write in pending:
                frm, fmeta = pending.pop(next_write)
                zarr_stream.append(frm, frame_metadata=fmeta)
            else:
                zarr_stream.append(missing_frame)
                logger.warning(f"Missing frame at linear index {next_write}; recorded in completion report.")
            next_write += 1
            sys.stdout.write(build_progress_bar(next_write, total_expected))
            sys.stdout.flush()

        # Finalize the writer before moving image groups or rewriting HCS
        # metadata. ExitStack.close() is idempotent after its callbacks run.
        zarr_resources.close()
    _record_completion(
        zarr_path,
        target_experiment_id,
        coord_to_linear,
        received_indices,
        store_created=zarr_stream is not None,
    )
    if zarr_stream is not None:
        if plate is not None:
            _materialize_hcs_row_groups(zarr_path)
            _assemble_scene_mosaics(
                zarr_path,
                list(tile_geometries.values()),
                keep_source_tiles=ecfg.keep_source_tiles,
                hcs_positions=ecfg.positions,
                hcs_tile_count=num_m,
            )
        elif num_s * num_m > 1:
            _assemble_scene_mosaics(
                zarr_path,
                list(tile_geometries.values()),
                keep_source_tiles=ecfg.keep_source_tiles,
            )

    sys.stdout.write("\n")
    logger.info(f"OME-ZARR written successfully: {zarr_path}")
    logger.info(f"Frames received: {frame_count} / {total_expected} expected")
    return zarr_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Stream ZEN pixel data into OME-ZARR via ZEN-API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--experiment-config",
        type=str,
        default=None,
        help=(
            "Path to an experiment config INI file (see experiment_config.ini). "
            "When provided, dimensions are known upfront and frames are written "
            "on-the-fly. Most other CLI flags are ignored except "
            "--start-experiment / --no-start-experiment which override the INI."
        ),
    )
    parser.add_argument(
        "--zenapi-config",
        type=str,
        default="config.ini",
        help="Path to the ZEN-API configuration file.",
    )
    parser.add_argument(
        "--experiment",
        type=str,
        required=False,
        default=None,
        help="ZEN experiment name (without .czexp extension). Required unless --experiment-config is used.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to store the OME-ZARR output.",
    )
    parser.add_argument(
        "--dtype",
        type=str,
        default="uint16",
        choices=["uint8", "uint16", "float32"],
        help="Pixel data type (must match experiment output).",
    )
    parser.add_argument(
        "--start-experiment",
        action=argparse.BooleanOptionalAction,
        default=None,
        help=(
            "Start the ZEN experiment from the script. "
            "Use --no-start-experiment to wait for the user to start from ZEN UI. "
            "In config mode this overrides the INI 'start_from_script' setting."
        ),
    )
    parser.add_argument(
        "--czi-name",
        type=str,
        default="zenapi_stream",
        help="CZI output name when starting experiment from script (without .czi).",
    )
    parser.add_argument(
        "--channel-index",
        type=int,
        default=None,
        help="Filter pixel stream by channel index (None = all channels).",
    )
    parser.add_argument(
        "--compression",
        type=str,
        default="blosc-zstd",
        choices=["blosc-zstd", "blosc-lz4", "zstd", "none"],
        help="Compression algorithm for the OME-ZARR store.",
    )
    parser.add_argument(
        "--no-overwrite-zarr",
        action="store_true",
        default=False,
        help="Do not overwrite an existing OME-ZARR at the output path.",
    )
    parser.add_argument(
        "--spatial-shard-size-chunks",
        type=int,
        default=2,
        help="Chunks per Y/X shard; use 0 to disable Zarr v3 sharding.",
    )
    parser.add_argument(
        "--inactivity-timeout",
        type=float,
        default=_STATUS_POLL_TIMEOUT,
        help="Seconds without a frame before acquisition is considered complete.",
    )
    parser.add_argument(
        "--pyramid-levels",
        type=int,
        default=0,
        help="Number of 2x Y/X pyramid levels to generate after acquisition; use 0 to disable.",
    )
    parser.add_argument(
        "--viewer",
        type=str,
        default=None,
        choices=["ndv", "napari"],
        help=(
            "Open the OME-ZARR in a viewer after acquisition. "
            "'ndv' uses the ndv viewer (requires ndv, zarr, dask, xarray). "
            "'napari' uses napari (requires napari, napari-ome-zarr). "
            "Omit to skip."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Entry point: parse arguments, run the appropriate streaming mode, and open the viewer."""
    args = parse_args()

    if args.experiment_config:
        # ---------- config-file mode (known dimensions, on-the-fly write) ----------
        ecfg = load_experiment_config(args.experiment_config)
        # CLI --start-experiment / --no-start-experiment overrides the INI value
        if args.start_experiment is not None:
            ecfg.start_from_script = args.start_experiment
        logger.info(f"Loaded experiment config: {args.experiment_config}")
        zarr_path = asyncio.run(
            stream_to_omezarr_with_config(
                ecfg,
                inactivity_timeout=args.inactivity_timeout,
            )
        )
        spatial_shard_size_chunks = ecfg.spatial_shard_size_chunks
    else:
        # ---------- CLI mode (unknown dimensions, buffered write) ----------
        if not args.experiment:
            logger.error("Either --experiment-config or --experiment must be provided.")
            sys.exit(1)

        compression = args.compression if args.compression != "none" else None

        zarr_path = asyncio.run(
            stream_to_omezarr(
                zenapi_config=args.zenapi_config,
                experiment_name=args.experiment,
                output_dir=args.output_dir,
                dtype=np.dtype(args.dtype),
                start_experiment_from_script=bool(args.start_experiment),
                czi_name=args.czi_name,
                channel_index=args.channel_index,
                overwrite_zarr=not args.no_overwrite_zarr,
                compression=compression,
                spatial_shard_size_chunks=args.spatial_shard_size_chunks or None,
                inactivity_timeout=args.inactivity_timeout,
            )
        )
        spatial_shard_size_chunks = args.spatial_shard_size_chunks or None

    if args.pyramid_levels:
        generate_omezarr_pyramids(
            zarr_path,
            pyramid_levels=args.pyramid_levels,
            spatial_shard_size_chunks=spatial_shard_size_chunks,
        )

    logger.info(f"Done. OME-ZARR: {zarr_path}")

    if args.viewer == "ndv":
        open_in_ndv_viewer(zarr_path)
    elif args.viewer == "napari":
        open_in_napari_viewer(zarr_path)


if __name__ == "__main__":
    main()
