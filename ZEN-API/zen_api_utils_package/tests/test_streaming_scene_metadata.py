"""Tests for scene and tile metadata used by OME-Zarr streaming."""

from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import zarr
from zen_api.acquisition.v1beta import PixelType
from zen_api_utils.extract_czexp_plan import extract_plan_xml
from zen_api_utils.streaming.geometry import (
    TileGeometry,
    assemble_channel_scene_mosaics,
    calculate_scene_geometry,
)
from zen_api_utils.streaming.omezarr import load_experiment_config
from zen_api_utils.streaming.pipeline import (
    _assemble_scene_mosaics,
    _build_position_layout,
    _find_omezarr_image_paths,
    _runtime_grayscale_dtype,
)


def _tile(
    tile_index: int,
    center_x: float,
    center_y: float,
    *,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
) -> TileGeometry:
    """Build a 10 by 10 tile for geometry tests."""
    return TileGeometry(
        scene_index=0,
        tile_index=tile_index,
        position_index=tile_index,
        center_x=center_x,
        center_y=center_y,
        position_z=0.0,
        scale_x=scale_x,
        scale_y=scale_y,
        height=10,
        width=10,
    )


def test_keep_source_tiles_defaults_false_and_can_be_enabled(
    tmp_path: Path,
) -> None:
    """Raw tile retention is opt-in through the experiment config."""
    config_path = tmp_path / "experiment.ini"
    config_path.write_text("[experiment]\nname=test\n", encoding="utf-8")

    default_config = load_experiment_config(config_path)

    assert default_config.keep_source_tiles is False

    config_path.write_text(
        "[experiment]\nname=test\n[output]\nkeep_source_tiles=true\n",
        encoding="utf-8",
    )
    enabled_config = load_experiment_config(config_path)

    assert enabled_config.keep_source_tiles is True


def test_tile_regions_map_to_scenes_and_per_scene_tiles() -> None:
    """Two active 3 by 2 regions describe two scenes of six tiles."""
    xml = """
    <Experiment>
      <ExperimentBlocks>
        <AcquisitionBlock IsActivated="true">
          <SubDimensionSetups>
            <RegionsSetup IsActivated="true">
              <SampleHolder>
                <TileRegions>
                  <TileRegion>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
                    <Columns>3</Columns>
                    <Rows>2</Rows>
                  </TileRegion>
                  <TileRegion>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
                    <Columns>3</Columns>
                    <Rows>2</Rows>
                  </TileRegion>
                </TileRegions>
              </SampleHolder>
            </RegionsSetup>
          </SubDimensionSetups>
        </AcquisitionBlock>
      </ExperimentBlocks>
    </Experiment>
    """

    plan = extract_plan_xml(xml)
    dimensions = plan["acquisition_blocks"][0]["dimensions"]

    assert dimensions["S"] == 2
    assert dimensions["M"] == 6


def test_tile_regions_map_to_b2_and_c3_wells() -> None:
    """Explicit TileRegion well identifiers are exported for HCS output."""
    xml = """
        <Experiment>
            <ExperimentBlocks>
                <AcquisitionBlock IsActivated="true">
                    <SubDimensionSetups>
                        <RegionsSetup IsActivated="true">
                            <SampleHolder>
                                <TileRegions>
                                    <TileRegion Name="B2">
                                        <CenterPosition>13500,17500</CenterPosition>
                                        <Columns>4</Columns><Rows>2</Rows>
                                        <TemplateShapeId>2-2</TemplateShapeId>
                                        <IsUsedForAcquisition>true</IsUsedForAcquisition>
                                    </TileRegion>
                                    <TileRegion Name="C3">
                                        <CenterPosition>22500,26500</CenterPosition>
                                        <Columns>2</Columns><Rows>4</Rows>
                                        <TemplateShapeId>3-3</TemplateShapeId>
                                        <IsUsedForAcquisition>true</IsUsedForAcquisition>
                                    </TileRegion>
                                </TileRegions>
                                <SingleTileRegionArrays />
                            </SampleHolder>
                        </RegionsSetup>
                    </SubDimensionSetups>
                </AcquisitionBlock>
            </ExperimentBlocks>
        </Experiment>
        """

    plan = extract_plan_xml(xml)
    positions = plan["acquisition_blocks"][0]["positions"]

    assert [position["well_id"] for position in positions] == ["B2", "C3"]


def test_hcs_layout_can_be_enabled_or_disabled() -> None:
    """The same explicit wells support HCS and generic scene output."""
    positions = (
        {
            "scene_index": 0,
            "well_row": 2,
            "well_column": 2,
            "field_index": 1,
        },
        {
            "scene_index": 1,
            "well_row": 3,
            "well_column": 3,
            "field_index": 1,
        },
    )
    hcs_config = SimpleNamespace(
        positions=positions,
        use_hcs_layout=True,
        experiment_name="wells",
    )
    generic_config = SimpleNamespace(
        positions=positions,
        use_hcs_layout=False,
        experiment_name="wells",
    )

    _, plate = _build_position_layout(hcs_config, num_s=2, num_m=8)
    generic_positions, generic_plate = _build_position_layout(
        generic_config,
        num_s=2,
        num_m=8,
    )

    assert plate is not None
    assert generic_plate is None
    assert generic_positions[0].name == "S0_M0"
    assert generic_positions[-1].name == "S1_M7"


@pytest.mark.parametrize(
    ("pixel_type", "bytes_per_pixel", "expected"),
    [
        (PixelType.GRAY8, 1, np.dtype(np.uint8)),
        (PixelType.GRAY16, 2, np.dtype(np.uint16)),
    ],
)
def test_runtime_grayscale_dtype(
    pixel_type: PixelType,
    bytes_per_pixel: int,
    expected: np.dtype,
) -> None:
    """Runtime stream metadata selects and validates the pixel dtype."""
    assert (
        _runtime_grayscale_dtype(
            pixel_type,
            payload_size=12 * bytes_per_pixel,
            width=4,
            height=3,
        )
        == expected
    )


def test_asymmetric_eight_tile_scenes_expect_48_frames() -> None:
    """A 4x2 plus 2x4 acquisition with three Z planes has 48 frames."""
    xml = """
        <Experiment>
            <ExperimentBlocks>
                <AcquisitionBlock IsActivated="true">
                    <SubDimensionSetups>
                        <RegionsSetup IsActivated="true">
                            <SampleHolder>
                                <TileRegions>
                                    <TileRegion>
                                        <IsUsedForAcquisition>true</IsUsedForAcquisition>
                                        <Columns>4</Columns>
                                        <Rows>2</Rows>
                                    </TileRegion>
                                    <TileRegion>
                                        <IsUsedForAcquisition>true</IsUsedForAcquisition>
                                        <Columns>2</Columns>
                                        <Rows>4</Rows>
                                    </TileRegion>
                                </TileRegions>
                            </SampleHolder>
                        </RegionsSetup>
                        <ZStackSetup IsActivated="true">
                            <First><Distance><Value>-0.008003</Value></Distance></First>
                            <Last><Distance><Value>-0.007997</Value></Distance></Last>
                            <Interval><Distance><Value>0.000003</Value></Distance></Interval>
                        </ZStackSetup>
                    </SubDimensionSetups>
                </AcquisitionBlock>
            </ExperimentBlocks>
        </Experiment>
        """

    plan = extract_plan_xml(xml)
    dimensions = plan["acquisition_blocks"][0]["dimensions"]

    assert dimensions["S"] == 2
    assert dimensions["M"] == 8
    assert dimensions["Z"] == 3
    assert dimensions["T"] * dimensions["C"] * dimensions["Z"] * dimensions["M"] * dimensions["S"] == 48


def test_scene_geometry_places_overlapping_tiles() -> None:
    """Overlapping tiles share pixels without duplicating their footprint."""
    geometry = calculate_scene_geometry([_tile(0, 4.5, 4.5), _tile(1, 12.5, 4.5)])

    assert (geometry.height, geometry.width) == (10, 18)
    assert [(tile.y_offset, tile.x_offset) for tile in geometry.tiles] == [
        (0, 0),
        (0, 8),
    ]


def test_scene_geometry_preserves_irregular_gaps() -> None:
    """Stage-position gaps remain empty space in the mosaic canvas."""
    geometry = calculate_scene_geometry([_tile(0, 4.5, 4.5), _tile(1, 19.5, 16.5)])

    assert (geometry.height, geometry.width) == (22, 25)
    assert [(tile.y_offset, tile.x_offset) for tile in geometry.tiles] == [
        (0, 0),
        (12, 15),
    ]


def test_scene_geometry_rejects_mixed_pixel_scales() -> None:
    """A mosaic cannot represent tiles sampled on different grids."""
    with pytest.raises(ValueError, match="same pixel scale"):
        calculate_scene_geometry(
            [
                _tile(0, 4.5, 4.5),
                _tile(1, 14.5, 4.5, scale_x=0.5),
            ]
        )


def test_four_by_two_scene_geometry_matches_expected_canvas() -> None:
    """The streamed 4x2 tile layout produces the expected scene canvas."""
    tile_width = 1960
    tile_height = 1416
    tiles = [
        TileGeometry(
            scene_index=0,
            tile_index=row * 4 + column,
            position_index=row * 4 + column,
            center_x=979.5 + column * 1764,
            center_y=707.5 + row * 1274,
            position_z=0.0,
            scale_x=1.0,
            scale_y=1.0,
            height=tile_height,
            width=tile_width,
        )
        for row in range(2)
        for column in range(4)
    ]

    geometry = calculate_scene_geometry(tiles)

    assert (geometry.height, geometry.width) == (2690, 7252)


def test_assemble_channel_scene_mosaics_uses_higher_m_index() -> None:
    """M tiles merge per scene and the higher M index wins overlaps."""
    geometries = {
        (0, 0): TileGeometry(0, 0, 0, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        (0, 1): TileGeometry(0, 1, 1, 4.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        (1, 0): TileGeometry(1, 0, 2, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        (1, 1): TileGeometry(1, 1, 3, 1.5, 6.5, 0.0, 1.0, 1.0, 4, 4),
    }
    frames = [
        (0, 0, 0, 0, np.full((4, 4), 2, dtype=np.uint16)),
        (0, 0, 1, 0, np.full((4, 4), 4, dtype=np.uint16)),
        (1, 0, 0, 0, np.full((4, 4), 6, dtype=np.uint16)),
        (1, 0, 1, 0, np.full((4, 4), 8, dtype=np.uint16)),
    ]

    result = assemble_channel_scene_mosaics(frames, geometries)

    assert result.shape == (2, 1, 1, 9, 7)
    assert np.all(result[0, 0, 0, :4, 3] == 4)
    assert np.all(result[1, 0, 0, 4, :] == 0)
    assert np.all(result[1, 0, 0, 5:, :4] == 8)


def _create_raw_tile(
    root: zarr.Group,
    index: int,
    value: int,
    *,
    group_name: str | None = None,
) -> None:
    """Create one raw TCYX tile with ome-writers-style metadata."""
    group = root.create_group(group_name or f"raw_{index}")
    group.create_array(
        "0",
        data=np.full((1, 1, 4, 4), value, dtype=np.uint16),
        chunks=(1, 1, 4, 4),
        dimension_names=("t", "c", "y", "x"),
    )
    group.attrs["ome"] = {
        "multiscales": [
            {
                "axes": [
                    {"name": "t", "type": "time"},
                    {"name": "c", "type": "channel"},
                    {
                        "name": "y",
                        "type": "space",
                        "unit": "micrometer",
                    },
                    {
                        "name": "x",
                        "type": "space",
                        "unit": "micrometer",
                    },
                ],
                "datasets": [
                    {
                        "path": "0",
                        "coordinateTransformations": [
                            {
                                "type": "scale",
                                "scale": [1.0, 1.0, 1.0, 1.0],
                            }
                        ],
                    }
                ],
            }
        ]
    }


def test_scene_mosaic_finalizer_emits_one_scene(
    tmp_path: Path,
) -> None:
    """Finalize overlap and gaps without retaining per-tile image groups."""
    store_path = tmp_path / "test.zarr"
    root = zarr.open_group(store_path, mode="w")
    ome_group = root.create_group("OME")
    ome_group.attrs["ome"] = {
        "version": "0.5",
        "series": ["raw_0", "raw_1", "raw_2"],
    }
    for index, value in enumerate((2, 4, 8)):
        _create_raw_tile(root, index, value)

    tiles = [
        TileGeometry(0, 0, 0, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        TileGeometry(0, 1, 1, 4.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        TileGeometry(0, 2, 2, 1.5, 6.5, 0.0, 1.0, 1.0, 4, 4),
    ]

    _assemble_scene_mosaics(store_path, tiles)

    mosaic = root["scene_0"]["0"][:]
    assert mosaic.shape == (1, 1, 9, 7)
    assert np.all(mosaic[0, 0, :4, 3] == 4)
    assert np.all(mosaic[0, 0, 4, :] == 0)
    assert np.all(mosaic[0, 0, 5:, :4] == 8)
    assert root["OME"].attrs["ome"]["series"] == ["scene_0"]
    assert not any(f"raw_{index}" in root for index in range(3))
    source_tiles = root["scene_0"].attrs["zen_scene"]["source_tiles"]
    assert source_tiles[1]["stage_position_xyz"] == [4.5, 1.5, 0.0]
    assert not root["scene_0"].attrs["zen_scene"]["source_tiles_retained"]
    assert root["scene_0"].attrs["zen_scene"]["overlap_policy"] == ("higher_m_index")
    assert _find_omezarr_image_paths(store_path) == [store_path / "scene_0"]


def test_hcs_scene_mosaic_finalizer_emits_one_scene(
    tmp_path: Path,
) -> None:
    """Assemble raw HCS tiles into one scene and remove tile groups."""
    store_path = tmp_path / "hcs.zarr"
    root = zarr.open_group(store_path, mode="w")
    well = root.create_group("B/02")
    well.attrs["ome"] = {
        "version": "0.5",
        "well": {
            "images": [
                {"path": "0"},
                {"path": "1"},
                {"path": "2"},
            ]
        },
    }
    for index, value in enumerate((2, 4, 8)):
        _create_raw_tile(
            root["B/02"],
            index,
            value,
            group_name=str(index),
        )

    tiles = [
        TileGeometry(0, 0, 0, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        TileGeometry(0, 1, 1, 4.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        TileGeometry(0, 2, 2, 1.5, 6.5, 0.0, 1.0, 1.0, 4, 4),
    ]

    _assemble_scene_mosaics(
        store_path,
        tiles,
        hcs_positions=(
            {
                "scene_index": 0,
                "well_row": 2,
                "well_column": 2,
                "field_index": 1,
            },
        ),
        hcs_tile_count=3,
    )

    mosaic = root["B/02/0/0"][:]
    assert mosaic.shape == (1, 1, 9, 7)
    assert np.all(mosaic[0, 0, :4, 3] == 4)
    assert np.all(mosaic[0, 0, 5:, :4] == 8)
    assert "B/02/0" in root
    assert not any(f"B/02/{index}" in root for index in (1, 2))
    assert root["B/02"].attrs["ome"]["well"]["images"] == [{"path": "0"}]


def test_hcs_single_tile_scene_is_finalized_without_copy(tmp_path: Path) -> None:
    """Reuse one HCS tile as the final scene image without replacing it."""
    store_path = tmp_path / "single-tile-hcs.zarr"
    root = zarr.open_group(store_path, mode="w")
    well = root.create_group("B/02")
    well.attrs["ome"] = {
        "version": "0.5",
        "well": {"images": [{"path": "0"}]},
    }
    _create_raw_tile(root["B/02"], 0, 7, group_name="0")
    root["B/02/0"].attrs["source_marker"] = "original"

    _assemble_scene_mosaics(
        store_path,
        [TileGeometry(0, 0, 0, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4)],
        hcs_positions=(
            {
                "scene_index": 0,
                "well_row": 2,
                "well_column": 2,
                "field_index": 1,
            },
        ),
        hcs_tile_count=1,
    )

    assert root["B/02/0"].attrs["source_marker"] == "original"
    assert np.all(root["B/02/0/0"][:] == 7)
    assert root["B/02"].attrs["ome"]["well"]["images"] == [{"path": "0"}]


def test_generic_single_tile_scene_is_finalized_without_copy(
    tmp_path: Path,
) -> None:
    """Rename one generic tile to its scene path without copying pixels."""
    store_path = tmp_path / "single-tile-generic.zarr"
    root = zarr.open_group(store_path, mode="w")
    ome_group = root.create_group("OME")
    ome_group.attrs["ome"] = {"version": "0.5", "series": ["raw_0"]}
    _create_raw_tile(root, 0, 9)
    root["raw_0"].attrs["source_marker"] = "original"

    _assemble_scene_mosaics(
        store_path,
        [TileGeometry(0, 0, 0, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4)],
    )

    assert "raw_0" not in root
    assert root["scene_0"].attrs["source_marker"] == "original"
    assert np.all(root["scene_0/0"][:] == 9)
    assert root["OME"].attrs["ome"]["series"] == ["scene_0"]


def test_scene_mosaic_finalizer_can_retain_source_tiles(
    tmp_path: Path,
) -> None:
    """Retain source groups when keep_source_tiles is explicitly enabled."""
    store_path = tmp_path / "remove-sources.zarr"
    root = zarr.open_group(store_path, mode="w")
    ome_group = root.create_group("OME")
    ome_group.attrs["ome"] = {
        "version": "0.5",
        "series": ["raw_0", "raw_1"],
    }
    _create_raw_tile(root, 0, 2)
    _create_raw_tile(root, 1, 4)
    tiles = [
        TileGeometry(0, 0, 0, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        TileGeometry(0, 1, 1, 4.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
    ]

    _assemble_scene_mosaics(
        store_path,
        tiles,
        keep_source_tiles=True,
    )

    assert root["OME"].attrs["ome"]["series"] == ["scene_0"]
    assert root["scene_0"]["0"].shape == (1, 1, 4, 7)
    assert all(f"raw_{index}" in root for index in range(2))
    assert root["scene_0"].attrs["zen_scene"]["source_tiles_retained"]


def test_hcs_scene_mosaic_can_retain_source_tiles(tmp_path: Path) -> None:
    """Use a non-conflicting numeric field when retaining HCS tiles."""
    store_path = tmp_path / "retain-hcs.zarr"
    root = zarr.open_group(store_path, mode="w")
    well = root.create_group("B/02")
    well.attrs["ome"] = {
        "version": "0.5",
        "well": {"images": [{"path": "0"}, {"path": "1"}]},
    }
    for index, value in enumerate((2, 4)):
        _create_raw_tile(root["B/02"], index, value, group_name=str(index))

    _assemble_scene_mosaics(
        store_path,
        [
            TileGeometry(0, 0, 0, 1.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
            TileGeometry(0, 1, 1, 4.5, 1.5, 0.0, 1.0, 1.0, 4, 4),
        ],
        keep_source_tiles=True,
        hcs_positions=(
            {
                "scene_index": 0,
                "well_row": 2,
                "well_column": 2,
                "field_index": 1,
            },
        ),
        hcs_tile_count=2,
    )

    assert all(f"B/02/{index}" in root for index in (0, 1, 2))
    assert root["B/02"].attrs["ome"]["well"]["images"] == [{"path": "2"}]
