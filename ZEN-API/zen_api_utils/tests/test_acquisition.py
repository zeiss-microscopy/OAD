import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

from zen_api_utils.experiment_acquisition import query_experiment_acquisition
from zen_api_utils.extract_czexp_plan import (
    PLAN_SCHEMA,
    Position,
    TileRegion,
    parse_well_id,
)
from zen_api_utils.streaming.acquisition import ExperimentAcquisition


def test_acquisition_from_plan_extracts_dimensions_and_wells() -> None:
    plan = {
        "schema": PLAN_SCHEMA,
        "source": {"path": "example.czexp"},
        "acquisition_blocks": [
            {
                "block_index": 0,
                "dimensions": {"T": 2, "C": 3, "Z": 4, "S": 5, "M": 6, "ZSpacing": 1.5},
                "channels": [{"name": "DAPI", "pixel_type": "GRAY16"}],
                "positions": [
                    {
                        "scene_index": scene,
                        "well_id": well,
                        "well_row": parse_well_id(well)[0],
                        "well_column": parse_well_id(well)[1],
                        "well_index": [0, 1, 0][scene],
                        "field_index": [0, 0, 1][scene],
                        "stage_position": {"x": None, "y": None, "z": None},
                    }
                    for scene, well in enumerate(("A01", "B02", "A01"))
                ],
                "split_scenes_in_separate_files": True,
            }
        ],
    }

    result = ExperimentAcquisition.from_plan(plan)

    assert result.experiment_name == "example"
    assert result.dimensions.channels == 3
    assert result.dimensions.tiles == 6
    assert result.well_ids == ("A01", "B02")
    assert result.well_count == 2
    assert isinstance(result.positions[0], Position)
    assert result.positions[0].well_row == 0
    assert result.positions[2].field_index == 1


def test_file_and_xml_acquisition_share_typed_region_metadata(tmp_path: Path) -> None:
    xml = """
    <Experiment><ExperimentBlocks><AcquisitionBlock IsActivated="true">
      <SubDimensionSetups><RegionsSetup IsActivated="true"><SampleHolder>
        <TileRegions><TileRegion Name="B3">
          <Contour Type="Rectangle"/><ContourSize>100,200</ContourSize>
          <CenterPosition>4500,8500</CenterPosition><Z>-8000</Z>
        </TileRegion></TileRegions>
      </SampleHolder></RegionsSetup></SubDimensionSetups>
    </AcquisitionBlock></ExperimentBlocks></Experiment>
    """
    source = tmp_path / "example.czexp"
    source.write_text(xml, encoding="utf-8")
    file_acquisition = ExperimentAcquisition.from_czexp(str(source))
    xml_acquisition = ExperimentAcquisition.from_xml(xml, "example.czexp")
    assert file_acquisition == xml_acquisition
    service = SimpleNamespace(export=AsyncMock(return_value=SimpleNamespace(xml=xml)))
    live_acquisition = asyncio.run(query_experiment_acquisition(service, "experiment-id", "example"))
    assert live_acquisition == file_acquisition
    service.export.assert_awaited_once()
    position = file_acquisition.positions[0]
    assert position.tile_region == TileRegion("Rectangle", 100.0, 200.0)
    assert (position.well_row, position.well_column, position.field_index) == (1, 2, 0)
    assert (position.x, position.y, position.z) == (4500.0, 8500.0, -8000.0)
