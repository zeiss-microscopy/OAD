"""Coordinate-based geometry for streamed image tiles."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TileGeometry:
    """Physical geometry for one streamed image tile."""

    scene_index: int
    tile_index: int
    position_index: int
    center_x: float
    center_y: float
    position_z: float
    scale_x: float
    scale_y: float
    height: int
    width: int


@dataclass(frozen=True)
class PlacedTile:
    """Tile geometry resolved against a scene mosaic canvas."""

    tile: TileGeometry
    y_offset: int
    x_offset: int
    translation_y: float
    translation_x: float


@dataclass(frozen=True)
class SceneGeometry:
    """Shape and physical origin of a rasterized scene mosaic."""

    height: int
    width: int
    origin_y: float
    origin_x: float
    scale_y: float
    scale_x: float
    tiles: tuple[PlacedTile, ...]


def calculate_scene_geometry(tiles: list[TileGeometry]) -> SceneGeometry:
    """Calculate mosaic placement from arbitrary tile center positions."""
    if not tiles:
        raise ValueError("Cannot calculate scene geometry without tiles")

    scale_y = tiles[0].scale_y
    scale_x = tiles[0].scale_x
    if scale_y <= 0 or scale_x <= 0:
        raise ValueError("Tile pixel scales must be positive")

    for tile in tiles[1:]:
        if not math.isclose(tile.scale_y, scale_y) or not math.isclose(tile.scale_x, scale_x):
            raise ValueError("All tiles in a scene must use the same pixel scale")

    tile_origins = [
        (
            tile.center_y - ((tile.height - 1) * scale_y / 2.0),
            tile.center_x - ((tile.width - 1) * scale_x / 2.0),
        )
        for tile in tiles
    ]
    origin_y = min(tile_y for tile_y, _ in tile_origins)
    origin_x = min(tile_x for _, tile_x in tile_origins)

    placed_tiles: list[PlacedTile] = []
    mosaic_height = 0
    mosaic_width = 0
    for tile, (tile_y, tile_x) in zip(tiles, tile_origins, strict=True):
        y_offset = int(round((tile_y - origin_y) / scale_y))
        x_offset = int(round((tile_x - origin_x) / scale_x))
        mosaic_height = max(mosaic_height, y_offset + tile.height)
        mosaic_width = max(mosaic_width, x_offset + tile.width)
        placed_tiles.append(
            PlacedTile(
                tile=tile,
                y_offset=y_offset,
                x_offset=x_offset,
                translation_y=tile_y,
                translation_x=tile_x,
            )
        )

    return SceneGeometry(
        height=mosaic_height,
        width=mosaic_width,
        origin_y=origin_y,
        origin_x=origin_x,
        scale_y=scale_y,
        scale_x=scale_x,
        tiles=tuple(placed_tiles),
    )


def assemble_channel_scene_mosaics(
    channel_frames: list[tuple[int, int, int, int, np.ndarray]],
    tile_geometries: dict[tuple[int, int], TileGeometry],
) -> np.ndarray:
    """Merge ``(scene, time, tile, z, image)`` records into an ``STZYX`` array."""
    if not channel_frames:
        raise ValueError("Cannot assemble scene mosaics without frames")

    unique_s = sorted({scene for scene, _, _, _, _ in channel_frames})
    unique_t = sorted({time for _, time, _, _, _ in channel_frames})
    unique_z = sorted({z_index for _, _, _, z_index, _ in channel_frames})
    scene_geometries: dict[int, SceneGeometry] = {}
    for scene_index in unique_s:
        tile_indices = sorted({tile for scene, _, tile, _, _ in channel_frames if scene == scene_index})
        missing = [tile for tile in tile_indices if (scene_index, tile) not in tile_geometries]
        if missing:
            raise ValueError(f"Missing geometry for scene {scene_index} tiles {missing}")
        scene_geometries[scene_index] = calculate_scene_geometry(
            [tile_geometries[(scene_index, tile)] for tile in tile_indices]
        )

    first_image = channel_frames[0][4]
    output_shape = (
        len(unique_s),
        len(unique_t),
        len(unique_z),
        max(geometry.height for geometry in scene_geometries.values()),
        max(geometry.width for geometry in scene_geometries.values()),
    )
    output = np.zeros(output_shape, dtype=first_image.dtype)
    s_map = {value: index for index, value in enumerate(unique_s)}
    t_map = {value: index for index, value in enumerate(unique_t)}
    z_map = {value: index for index, value in enumerate(unique_z)}
    placements = {
        (scene_index, placed.tile.tile_index): placed
        for scene_index, geometry in scene_geometries.items()
        for placed in geometry.tiles
    }

    for scene, time, tile, z_index, image in sorted(channel_frames, key=lambda frame: frame[2]):
        placed = placements[(scene, tile)]
        y_slice = slice(placed.y_offset, placed.y_offset + image.shape[0])
        x_slice = slice(placed.x_offset, placed.x_offset + image.shape[1])
        plane_index = (s_map[scene], t_map[time], z_map[z_index])
        output[plane_index + (y_slice, x_slice)] = image

    return output
