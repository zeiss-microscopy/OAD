import importlib
import io
from pathlib import Path
from typing import Annotated
from unittest.mock import Mock

import pytest
from loguru import logger
from pydantic import AfterValidator, TypeAdapter, ValidationError

from zen_api_utils.extract_czexp_plan import extract_plan_xml
from zen_api_utils.misc import path_validator, set_logging
from zen_api_utils.sample_carrier import WellPlate


def test_tcp_example_import_does_not_connect(monkeypatch: pytest.MonkeyPatch) -> None:
    """Importing the shipped example must never contact the microscope."""
    from zen_api_utils import zen_tcpip

    transport = Mock()
    monkeypatch.setattr(zen_tcpip, "ZenTCPIP", transport)
    module = importlib.import_module("zen_api_utils.zen_tcpip_interface")
    importlib.reload(module)
    transport.assert_not_called()


def test_library_logging_preserves_application_sink() -> None:
    """Library imports and logger access preserve application configuration."""
    output = io.StringIO()
    sink = logger.add(output, format="{message}")
    try:
        assert set_logging() is logger
        module = importlib.import_module("zen_api_utils.cameras")
        importlib.reload(module)
        logger.info("host sink retained")
        assert "host sink retained" in output.getvalue()
    finally:
        logger.remove(sink)


def test_path_validator_rejects_invalid_values() -> None:
    """Invalid values raise ValueError, including inside Pydantic validation."""
    assert path_validator("example.czi") == Path("example.czi")
    with pytest.raises(ValueError, match="not a valid path"):
        path_validator(123)  # type: ignore[arg-type]
    adapter = TypeAdapter(Annotated[object, AfterValidator(path_validator)])
    with pytest.raises(ValidationError, match="not a valid path"):
        adapter.validate_python(123)


def test_well_plate_round_trip() -> None:
    plate = WellPlate(8, 12)

    assert plate.well_to_index("B3") == (1, 2)
    assert plate.index_to_well(7, 11) == "H12"
    assert "A1" in plate
    assert "I1" not in plate


def test_extract_plan_xml_reads_active_tile_regions() -> None:
    xml = """
    <Experiment>
      <ExperimentBlocks>
        <AcquisitionBlock IsActivated="true">
          <SubDimensionSetups>
            <RegionsSetup IsActivated="true">
              <SampleHolder>
                <TileRegions>
                  <TileRegion Name="B2">
                    <CenterPosition>100,200</CenterPosition>
                    <Columns>3</Columns>
                    <Rows>2</Rows>
                    <TemplateShapeId>2-2</TemplateShapeId>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
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
    block = plan["acquisition_blocks"][0]

    assert block["dimensions"]["S"] == 1
    assert block["dimensions"]["M"] == 6
    assert block["positions"][0]["well_id"] == "B2"


def test_extract_plan_xml_reads_direct_single_tile_regions_without_inventing_wells() -> None:
    xml = """
    <Experiment>
      <ExperimentBlocks>
        <AcquisitionBlock IsActivated="true">
          <SubDimensionSetups>
            <RegionsSetup IsActivated="true">
              <SampleHolder>
                <SingleTileRegions>
                  <SingleTileRegion Name="P1" Id="1">
                    <X>30080.21</X><Y>24661.814</Y><Z>-8000</Z>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
                  </SingleTileRegion>
                  <SingleTileRegion Name="P2" Id="2">
                    <X>32389.872</X><Y>27671.373</Y><Z>-8000</Z>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
                  </SingleTileRegion>
                  <SingleTileRegion Name="P3" Id="3">
                    <IsUsedForAcquisition>false</IsUsedForAcquisition>
                  </SingleTileRegion>
                </SingleTileRegions>
                <SingleTileRegionArrays />
              </SampleHolder>
            </RegionsSetup>
          </SubDimensionSetups>
        </AcquisitionBlock>
      </ExperimentBlocks>
    </Experiment>
    """

    block = extract_plan_xml(xml)["acquisition_blocks"][0]

    assert block["dimensions"]["S"] == 2
    assert block["position_count"] == 2
    assert block["well_count"] == 0
    assert block["positions"][0]["stage_position"] == {"x": 30080.21, "y": 24661.814, "z": -8000.0}
    assert [position["well_id"] for position in block["positions"]] == [None, None]
    assert block["planned_outputs"][0]["well_ids"] == []

    split_block = extract_plan_xml(
        xml.replace("<SampleHolder>", "<SampleHolder><SplitScenesInSeparateFiles>true</SplitScenesInSeparateFiles>")
    )["acquisition_blocks"][0]
    assert [output["suggested_filename"] for output in split_block["planned_outputs"]] == [
        "<experiment-export>-Scene-001-P1.czi",
        "<experiment-export>-Scene-002-P2.czi",
    ]
