import copy
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from zen_api_utils import extract_czexp_plan as parser


def experiment_xml(sample_holder: str, *, split: bool = True) -> str:
    return f"""
    <Experiment><ExperimentBlocks>
      <AcquisitionBlock IsActivated="true" BlockReference="7">
        <SubDimensionSetups><RegionsSetup IsActivated="true"><SampleHolder>
          <SplitScenesInSeparateFiles>{str(split).lower()}</SplitScenesInSeparateFiles>
          {sample_holder}
        </SampleHolder></RegionsSetup></SubDimensionSetups>
      </AcquisitionBlock>
    </ExperimentBlocks></Experiment>
    """


def region_xml(*, name: str = "B3", size: str = "548.8,396.48", contour: str = "Rectangle") -> str:
    return f"""
    <TileRegion Name="{name}" Id="region-1">
      <CenterPosition>4500,8500</CenterPosition><Z>-8000</Z>
      <Columns>4</Columns><Rows>2</Rows>
      <Contour Type="{contour}"/><ContourSize>{size}</ContourSize>
    </TileRegion>
    """


@pytest.mark.parametrize(("label", "indices"), [("A1", (0, 0)), ("B3", (1, 2)), ("AA12", (26, 11))])
def test_well_label_round_trip(label: str, indices: tuple[int, int]) -> None:
    assert parser.parse_well_id(label) == indices
    assert parser.well_id(*indices) == label


def test_plan_to_czmbi_converts_indices_only_at_boundary() -> None:
    xml = experiment_xml(f"<TileRegions>{region_xml()}</TileRegions>")
    plan = parser.extract_plan_xml(xml)
    position = plan["acquisition_blocks"][0]["positions"][0]
    assert (position["well_row"], position["well_column"], position["field_index"]) == (1, 2, 0)
    assert plan["schema"] == "experimental.czexp-acquisition-plan/0.2"
    before = copy.deepcopy(plan)
    document = parser.build_czmbi(plan).find("./Documents/Document")
    assert document is not None
    assert document.attrib == {"BlockId": "7", "WellId": "B3", "Row": "2", "Col": "3", "Field": "1"}
    assert plan == before


def test_template_shape_id_converts_one_based_well_coordinates() -> None:
    region = region_xml(name="Unnamed").replace("</TileRegion>", "<TemplateShapeId>2-3</TemplateShapeId></TileRegion>")
    plan = parser.extract_plan_xml(experiment_xml(f"<TileRegions>{region}</TileRegions>"))
    position = plan["acquisition_blocks"][0]["positions"][0]
    assert (position["well_id"], position["well_row"], position["well_column"]) == ("B3", 1, 2)


def test_free_regions_and_missing_coordinates_are_retained() -> None:
    regions = region_xml(name="Region").replace("<Z>-8000</Z>", "")
    regions += region_xml(name="B3").replace('Id="region-1"', 'Id="region-2"')
    block = parser.extract_plan_xml(experiment_xml(f"<TileRegions>{regions}</TileRegions>"))["acquisition_blocks"][0]
    assert block["position_count"] == 2
    assert block["positions"][0]["well_id"] is None
    assert block["positions"][0]["stage_position"] == {"x": 4500.0, "y": 8500.0, "z": None}
    assert block["positions"][1]["well_id"] == "B3"


def test_fields_are_zero_based_per_well_and_unassigned_group() -> None:
    arrays = """
    <SingleTileRegionArrays>
      <SingleTileRegionArray Name="B3"><SingleTileRegions>
        <SingleTileRegion Name="first"/><SingleTileRegion Name="disabled">
          <IsUsedForAcquisition>false</IsUsedForAcquisition>
        </SingleTileRegion><SingleTileRegion Name="second"/>
      </SingleTileRegions></SingleTileRegionArray>
      <SingleTileRegionArray Name="C4"><SingleTileRegions>
        <SingleTileRegion Name="third"/>
      </SingleTileRegions></SingleTileRegionArray>
    </SingleTileRegionArrays>
    """
    positions = parser.extract_plan_xml(experiment_xml(arrays))["acquisition_blocks"][0]["positions"]
    assert [position["field_index"] for position in positions] == [0, 1, 0]
    direct = "<SingleTileRegions><SingleTileRegion/><SingleTileRegion/></SingleTileRegions>"
    positions = parser.extract_plan_xml(experiment_xml(direct))["acquisition_blocks"][0]["positions"]
    assert [position["field_index"] for position in positions] == [0, 1]


def test_template_grid_assignment_preserves_zero_based_wells_and_fields() -> None:
    template = """
    <Template>
      <HasRegularShapes>true</HasRegularShapes><ShapeType>Rectangle</ShapeType>
      <ReferencePoint>0,0</ReferencePoint><AnchorPoint>0,0</AnchorPoint>
      <ImmersionPoint>0,0</ImmersionPoint><ShapeRows>1</ShapeRows><ShapeColumns>2</ShapeColumns>
      <ShapeDistanceX>10</ShapeDistanceX><ShapeDistanceY>10</ShapeDistanceY>
      <ShapeWidth>8</ShapeWidth><ShapeHeight>8</ShapeHeight><Rotation>0</Rotation>
      <ReferencePointLocationMode>TopLeft</ReferencePointLocationMode>
      <AreShapesCenteredX>true</AreShapesCenteredX><AreShapesCenteredY>true</AreShapesCenteredY>
    </Template>
    """
    direct = "<SingleTileRegions>" + "".join(
        f"<SingleTileRegion><X>{x}</X><Y>0</Y></SingleTileRegion>" for x in (-5, 5, -5, 100)
    ) + "</SingleTileRegions>"
    positions = parser.positions_from_plan(parser.extract_plan_xml(experiment_xml(template + direct)))
    assert [(p.well_id, p.well_row, p.well_column, p.field_index) for p in positions] == [
        ("A1", 0, 0, 0), ("A2", 0, 1, 0), ("A1", 0, 0, 1), (None, None, None, 0)
    ]


def test_typed_positions_reuse_plan_geometry_and_parse_file_once(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "test.czexp"
    source.write_text(experiment_xml(f"<TileRegions>{region_xml()}</TileRegions>"), encoding="utf-8")
    read_text = Path.read_text
    reads = []

    def read_once(path: Path, *args, **kwargs) -> str:
        reads.append(path)
        return read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_once)
    positions = parser.load_experiment_positions(source)
    assert reads == [source]
    position = positions[0]
    assert isinstance(position, parser.Position)
    assert (position.x, position.y, position.z) == (4500.0, 8500.0, -8000.0)
    assert position.tile_region == parser.TileRegion("Rectangle", 548.8, 396.48)
    assert position.to_record()["field_index"] == 0
    xml = read_text(source, encoding="utf-8")
    assert parser.positions_from_plan(parser.extract_plan_xml(xml)) == positions


@pytest.mark.parametrize("size", ["", "548.8", "1,2,3", "bad,1", "nan,1", "1,inf", "-1,2", "1,0"])
def test_invalid_rectangles_raise_with_region_context(size: str) -> None:
    with pytest.raises(ValueError, match="Invalid rectangular tile-region ContourSize.*region-1"):
        parser.extract_plan_xml(experiment_xml(f"<TileRegions>{region_xml(size=size)}</TileRegions>"))


def test_nonrectangular_regions_preserve_contour_without_rectangle_dimensions() -> None:
    plan = parser.extract_plan_xml(
        experiment_xml(f"<TileRegions>{region_xml(contour='Ellipse', size='')}</TileRegions>")
    )
    position = parser.positions_from_plan(plan)[0]
    assert position.tile_region == parser.TileRegion("Ellipse")


def test_dataframe_preserves_nullable_values_and_empty_schema(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    pd = pytest.importorskip("pandas")
    source = tmp_path / "test.czexp"
    source.write_text(
        experiment_xml("<SingleTileRegions><SingleTileRegion Name='P1'><X>1.25</X></SingleTileRegion></SingleTileRegions>"),
        encoding="utf-8",
    )
    table = parser.load_experiment_positions_dataframe(source)
    assert list(table.columns) == list(parser.POSITION_FIELDS)
    assert str(table["field_index"].dtype) == "Int64"
    assert str(table["stage_x_um"].dtype) == "Float64"
    assert str(table["position_name"].dtype) == "string"
    assert table.loc[0, "stage_x_um"] == 1.25
    assert pd.isna(table.loc[0, "stage_z_um"])
    source.write_text(experiment_xml(""), encoding="utf-8")
    assert list(parser.load_experiment_positions_dataframe(source).columns) == list(parser.POSITION_FIELDS)
    assert parser.load_experiment_positions(source) == []
    assert capsys.readouterr() == ("", "")


def test_dataframe_reports_missing_optional_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "pandas", None)
    with pytest.raises(ImportError, match=r"zen_api_utils\[dataframe\]"):
        parser.positions_to_dataframe([])


def test_legacy_plan_indices_are_not_silently_reinterpreted() -> None:
    plan = parser.extract_plan_xml(experiment_xml(""))
    plan["schema"] = "experimental.czexp-acquisition-plan/0.1"
    with pytest.raises(ValueError, match="0.2"):
        parser.positions_from_plan(plan)
    with pytest.raises(ValueError, match="0.2"):
        parser.build_czmbi(plan)


def test_inactive_blocks_and_setups_keep_original_block_indices() -> None:
    root = ET.fromstring(experiment_xml(f"<TileRegions>{region_xml()}</TileRegions>"))
    blocks = root.find("ExperimentBlocks")
    assert blocks is not None
    original = blocks[0]
    inactive = copy.deepcopy(original)
    inactive.set("IsActivated", "false")
    blocks.insert(0, inactive)
    parent = original.find("SubDimensionSetups")
    assert parent is not None
    inactive_setup = copy.deepcopy(parent[0])
    inactive_setup.set("IsActivated", "false")
    inactive_setup.find(".//ContourSize").text = "bad"
    parent.insert(0, inactive_setup)
    positions = parser.positions_from_plan(parser.extract_plan_xml(ET.tostring(root, encoding="unicode")))
    assert len(positions) == 1
    assert positions[0].block_index == 1


@pytest.fixture
def carrier_xml() -> str:
    return experiment_xml("""
    <Template>
      <HasRegularShapes>true</HasRegularShapes><ShapeType>Rectangle</ShapeType>
      <ReferencePoint>0,0</ReferencePoint><ReferencePointLocationMode>TopLeft</ReferencePointLocationMode>
      <AnchorPoint>-9900,-2750</AnchorPoint><ImmersionPoint>63900,42750</ImmersionPoint>
      <ShapeRows>8</ShapeRows><ShapeColumns>12</ShapeColumns>
      <ShapeDistanceX>9000</ShapeDistanceX><ShapeDistanceY>9000</ShapeDistanceY>
      <ShapeWidth>7250</ShapeWidth><ShapeHeight>7250</ShapeHeight><Rotation>0</Rotation>
      <AreShapesCenteredX>true</AreShapesCenteredX><AreShapesCenteredY>true</AreShapesCenteredY>
    </Template>
    """)


def test_empty_carrier_maps_all_wells_in_input_order(carrier_xml: str, tmp_path: Path) -> None:
    source = tmp_path / "empty.czexp"
    source.write_text(carrier_xml, encoding="utf-8")
    geometry = parser.load_carrier_geometry(source)
    assert parser.extract_plan(source)["acquisition_blocks"][0]["position_count"] == 0
    expected = [parser.WellAssignment(parser.well_id(row, col), row, col) for row in range(8) for col in range(12)]
    centers = [(4500 + col * 9000, 8500 + row * 9000) for row in range(8) for col in range(12)]
    assert geometry.assign_positions(centers) == expected
    assert geometry.assign_positions([centers[1], centers[0], centers[1]]) == [expected[1], expected[0], expected[1]]
    assert geometry.assign_positions([]) == []


def test_carrier_includes_edges_but_not_gaps_or_outside(carrier_xml: str) -> None:
    geometry = parser.carrier_geometry_from_xml(carrier_xml)
    assert geometry.locate(875, 4875) == parser.WellAssignment("A1", 0, 0)
    assert geometry.locate(8125, 12125) == parser.WellAssignment("A1", 0, 0)
    assert geometry.locate(8125.001, 8500) is None
    assert geometry.locate(9000, 8500) is None
    assert geometry.locate(-10000, 8500) is None
    assert geometry.locate(200000, 8500) is None


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_carrier_rejects_nonfinite_inputs(carrier_xml: str, value: float) -> None:
    geometry = parser.carrier_geometry_from_xml(carrier_xml)
    with pytest.raises(ValueError, match="finite"):
        geometry.locate(value, 8500)
    with pytest.raises(ValueError, match="finite"):
        geometry.assign_positions([(4500, value)])


@pytest.mark.parametrize(("old", "new"), [
    ("<Rotation>0</Rotation>", "<Rotation>1</Rotation>"),
    ("<ShapeType>Rectangle</ShapeType>", "<ShapeType>Ellipse</ShapeType>"),
    ("<ShapeWidth>7250</ShapeWidth>", "<ShapeWidth>9000</ShapeWidth>"),
    ("<ShapeHeight>7250</ShapeHeight>", "<ShapeHeight>0</ShapeHeight>"),
    ("<ShapeDistanceX>9000</ShapeDistanceX>", "<ShapeDistanceX>nan</ShapeDistanceX>"),
    ("<ReferencePoint>0,0</ReferencePoint>", "<ReferencePoint>1,0</ReferencePoint>"),
    ("<AreShapesCenteredX>true</AreShapesCenteredX>", "<AreShapesCenteredX>false</AreShapesCenteredX>"),
    ("</Template>", "<AreAxisAnnotationsSwitched>true</AreAxisAnnotationsSwitched></Template>"),
    ("</Template>", "<IsRowAnnotationDirectionInverted>true</IsRowAnnotationDirectionInverted></Template>"),
    ("</Template>", "<IsColumnAnnotationDirectionInverted>true</IsColumnAnnotationDirectionInverted></Template>"),
])
def test_carrier_rejects_unsupported_geometry(carrier_xml: str, old: str, new: str) -> None:
    with pytest.raises(parser.UnsupportedCarrierGeometryError):
        parser.carrier_geometry_from_xml(carrier_xml.replace(old, new))


def test_carrier_requires_active_setup_and_explicit_active_block_selection(carrier_xml: str) -> None:
    with pytest.raises(parser.UnsupportedCarrierGeometryError):
        parser.carrier_geometry_from_xml(experiment_xml(""))
    with pytest.raises(parser.UnsupportedCarrierGeometryError):
        parser.carrier_geometry_from_xml(carrier_xml.replace('RegionsSetup IsActivated="true"', 'RegionsSetup IsActivated="false"'))
    with pytest.raises(ValueError, match="not available"):
        parser.carrier_geometry_from_xml(carrier_xml, block_index=1)
    with pytest.raises(ValueError, match="not available"):
        parser.carrier_geometry_from_xml(carrier_xml, block_index=-1)
    root = ET.fromstring(carrier_xml)
    blocks = root.find("ExperimentBlocks")
    inactive = copy.deepcopy(blocks[0])
    inactive.set("IsActivated", "false")
    inactive.find(".//Rotation").text = "90"
    blocks.insert(0, inactive)
    assert parser.carrier_geometry_from_xml(ET.tostring(root, encoding="unicode")).locate(4500, 8500).well_id == "A1"


def test_carrier_ignores_acquisition_subset_and_logs_unsupported_plan_inference(
    carrier_xml: str, caplog: pytest.LogCaptureFixture
) -> None:
    subset = """<SingleTileRegionArrays><SingleTileRegionArray Name="B3">
      <IsUsedForAcquisition>false</IsUsedForAcquisition><SingleTileRegions/>
    </SingleTileRegionArray></SingleTileRegionArrays>"""
    geometry = parser.carrier_geometry_from_xml(carrier_xml.replace("</SampleHolder>", subset + "</SampleHolder>"))
    assert geometry.locate(4500, 8500) == parser.WellAssignment("A1", 0, 0)
    direct = "<SingleTileRegions><SingleTileRegion><X>4500</X><Y>8500</Y></SingleTileRegion></SingleTileRegions>"
    unsupported = carrier_xml.replace("<Rotation>0</Rotation>", "<Rotation>90</Rotation>")
    plan = parser.extract_plan_xml(unsupported.replace("</SampleHolder>", direct + "</SampleHolder>"))
    assert plan["acquisition_blocks"][0]["positions"][0]["well_id"] is None
    assert "Template well assignment skipped" in caplog.text
