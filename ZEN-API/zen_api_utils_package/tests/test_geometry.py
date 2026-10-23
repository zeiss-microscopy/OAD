import numpy as np

from zen_api_utils.streaming.geometry import TileGeometry, assemble_channel_scene_mosaics, calculate_scene_geometry


def tile(tile_index: int, center_x: float) -> TileGeometry:
    return TileGeometry(
        scene_index=0,
        tile_index=tile_index,
        position_index=tile_index,
        center_x=center_x,
        center_y=0.0,
        position_z=0.0,
        scale_x=1.0,
        scale_y=1.0,
        height=2,
        width=2,
    )


def test_scene_geometry_places_tiles_by_stage_position() -> None:
    result = calculate_scene_geometry([tile(0, 0.0), tile(1, 2.0)])

    assert (result.height, result.width) == (2, 4)
    assert [placed.x_offset for placed in result.tiles] == [0, 2]


def test_assemble_channel_scene_mosaics_combines_tiles() -> None:
    geometries = {(0, 0): tile(0, 0.0), (0, 1): tile(1, 2.0)}
    frames = [
        (0, 0, 0, 0, np.ones((2, 2), dtype=np.uint16)),
        (0, 0, 1, 0, np.full((2, 2), 2, dtype=np.uint16)),
    ]

    result = assemble_channel_scene_mosaics(frames, geometries)

    np.testing.assert_array_equal(result[0, 0, 0], [[1, 1, 2, 2], [1, 1, 2, 2]])
