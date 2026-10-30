r"""Extract a provisional CZI/CZMBI acquisition plan from a ZEN Experiment XML file.

Disclaimer: This script is intended for experimental use and may not cover all edge cases of ZEN Experiment XML files.

Run from the repository root:

    python experimental\extract_czexp_plan.py experimental\ZEN_API_Test_CD7_split.czexp

Write a reduced JSON plan and a CZMBI file in one call:

    python experimental\extract_czexp_plan.py `
        experimental\ZEN_API_Test_CD7_split.czexp `
        --reduced `
        --output experimental\plan.json `
        --czmbi-output experimental\hcs.czmbi

The JSON plan is always written first. When ``--czmbi-output`` is present, the
script reloads that JSON and projects its first acquisition block to CZMBI 1.0.
CZMBI generation requires split-scene acquisition with one planned CZI per scene.
When ZEN does not expose exact output names, the generated CZMBI uses deterministic
``suggested_filename`` values that must be validated against actual ZEN output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


class UnsupportedCzmbiProjectionError(ValueError):
    """Raised when a planned CZI output cannot be represented in CZMBI 1.0."""


def is_active(element: ET.Element | None, default: bool = True) -> bool:
    if element is None:
        return default
    value = element.get("IsActivated")
    return default if value is None else value.lower() == "true"


def child_text(element: ET.Element | None, path: str, default: str | None = None) -> str | None:
    if element is None:
        return default
    child = element.find(path)
    if child is None or child.text is None or not child.text.strip():
        return default
    return child.text.strip()


def number(element: ET.Element | None, path: str) -> float | None:
    value = child_text(element, path)
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None


def integer(element: ET.Element | None, path: str, default: int) -> int:
    value = child_text(element, path)
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


def parse_well_id(well_id: str) -> tuple[int | None, int | None]:
    match = re.fullmatch(r"([A-Za-z]+)(\d+)", well_id)
    if not match:
        return None, None
    row = 0
    for letter in match.group(1).upper():
        row = row * 26 + ord(letter) - ord("A") + 1
    return row, int(match.group(2))


def well_id(row: int, column: int) -> str:
    """Return an Excel-style well identifier for one-based indices."""
    letters = ""
    value = row
    while value > 0:
        value, remainder = divmod(value - 1, 26)
        letters = chr(ord("A") + remainder) + letters
    return f"{letters}{column}"


def coordinate_pair(
    element: ET.Element,
    path: str,
) -> tuple[float, float] | None:
    """Parse a comma-separated XML coordinate pair."""
    value = child_text(element, path)
    if value is None:
        return None
    try:
        first, second = value.split(",", maxsplit=1)
        return float(first), float(second)
    except ValueError:
        return None


def tile_region_well(
    region: ET.Element,
) -> tuple[int | None, int | None]:
    """Read an explicit well coordinate from one ZEN tile region."""
    template_id = child_text(region, "TemplateShapeId", "") or ""
    match = re.fullmatch(r"(\d+)-(\d+)", template_id)
    if match is not None:
        return int(match.group(1)), int(match.group(2))
    return parse_well_id(region.get("Name", ""))


def assign_template_wells(positions: list[dict[str, Any]], sample_holder: ET.Element) -> None:
    """Assign direct positions to wells in a centered, axis-aligned carrier grid."""
    template = sample_holder.find("./Template")
    if template is None or (child_text(template, "HasRegularShapes", "false") or "false").lower() != "true":
        return

    reference = coordinate_pair(template, "ReferencePoint")
    anchor = coordinate_pair(template, "AnchorPoint")
    immersion = coordinate_pair(template, "ImmersionPoint")
    rows = integer(template, "ShapeRows", 0)
    columns = integer(template, "ShapeColumns", 0)
    pitch_x = number(template, "ShapeDistanceX")
    pitch_y = number(template, "ShapeDistanceY")
    width = number(template, "ShapeWidth")
    height = number(template, "ShapeHeight")
    rotation = number(template, "Rotation")
    if (
        reference is None
        or anchor is None
        or immersion is None
        or rows < 1
        or columns < 1
        or pitch_x is None
        or pitch_y is None
        or width is None
        or height is None
        or pitch_x <= 0
        or pitch_y <= 0
        or width <= 0
        or height <= 0
        or rotation is None
        or not math.isclose(rotation, 0.0)
        or reference != (0.0, 0.0)
        or child_text(template, "ReferencePointLocationMode") != "TopLeft"
        or (child_text(template, "AreShapesCenteredX", "false") or "false").lower() != "true"
        or (child_text(template, "AreShapesCenteredY", "false") or "false").lower() != "true"
        or (child_text(template, "AreAxisAnnotationsSwitched", "false") or "false").lower() == "true"
        or (child_text(template, "IsRowAnnotationDirectionInverted", "false") or "false").lower() == "true"
        or (child_text(template, "IsColumnAnnotationDirectionInverted", "false") or "false").lower() == "true"
    ):
        return

    # In this ZEN template layout, AnchorPoint offsets ImmersionPoint to the grid center.
    grid_center_x = immersion[0] + anchor[0]
    grid_center_y = immersion[1] + anchor[1]
    row_center = (rows - 1) / 2
    column_center = (columns - 1) / 2
    field_counts: dict[tuple[int, int], int] = {}

    for position in positions:
        stage_position = position["stage_position"]
        x = stage_position.get("x")
        y = stage_position.get("y")
        if x is None or y is None:
            continue
        if not math.isfinite(x) or not math.isfinite(y):
            LOGGER.warning(
                "Position %s has non-finite X/Y coordinates; well assignment was skipped.",
                position.get("position_name"),
            )
            continue

        # Round to the nearest grid center, then ensure the point lies inside that well.
        column_index = math.floor((x - grid_center_x) / pitch_x + column_center + 0.5)
        row_index = math.floor((y - grid_center_y) / pitch_y + row_center + 0.5)
        if not (0 <= column_index < columns and 0 <= row_index < rows):
            continue

        center_x = grid_center_x + (column_index - column_center) * pitch_x
        center_y = grid_center_y + (row_index - row_center) * pitch_y
        if abs(x - center_x) > width / 2 or abs(y - center_y) > height / 2:
            continue

        well_row = row_index + 1
        well_column = column_index + 1
        well = (well_row, well_column)
        field_counts[well] = field_counts.get(well, 0) + 1
        position.update(
            {
                "well_id": well_id(well_row, well_column),
                "well_row": well_row,
                "well_column": well_column,
                "field_index": field_counts[well],
            }
        )


def parse_detector_frame(block: ET.Element) -> tuple[int | None, int | None]:
    frame = child_text(block, ".//AcquisitionModeSetup/Detectors/Detector/Frame")
    if frame is None:
        return None, None
    try:
        _, _, width, height = (int(value) for value in frame.split(","))
        return width, height
    except (ValueError, TypeError):
        return None, None


def active_channels(block: ET.Element) -> list[dict[str, Any]]:
    channels: list[dict[str, Any]] = []
    for track in block.findall(".//MultiTrackSetup/Track"):
        if not is_active(track):
            continue
        for channel in track.findall("./Channels/Channel"):
            if not is_active(channel):
                continue
            pixel_type = child_text(channel, "PixelType")
            channels.append(
                {
                    "name": channel.get("Name"),
                    "id": channel.get("ChannelSetupId"),
                    "pixel_type": pixel_type,
                }
            )
    return channels


def find_active_dimension_setup(block: ET.Element, setup_name: str) -> ET.Element | None:
    """Find an active dimension setup through active parent dimensions."""

    def find_in(container: ET.Element) -> ET.Element | None:
        for setup in container:
            if not is_active(setup, default=False):
                continue
            if setup.tag == setup_name:
                return setup
            nested = setup.find("./SubDimensionSetups")
            if nested is not None and (match := find_in(nested)) is not None:
                return match
        return None

    setups = block.find("./SubDimensionSetups")
    return find_in(setups) if setups is not None else None


def active_dimension_count(block: ET.Element, setup_name: str, count_path: str) -> int:
    setup = find_active_dimension_setup(block, setup_name)
    return integer(setup, count_path, 1) if setup is not None else 1


def extract_tile_regions(block: ET.Element) -> list[dict[str, Any]]:
    """Extract active rectangular tile grids from the sample holder."""
    regions_setup = find_active_dimension_setup(block, "RegionsSetup")
    sample_holder = regions_setup.find("./SampleHolder") if regions_setup is not None else None
    tile_regions = sample_holder.findall("./TileRegions/TileRegion") if sample_holder is not None else []
    regions: list[dict[str, Any]] = []
    for region in tile_regions:
        if (child_text(region, "IsUsedForAcquisition", "true") or "true").lower() != "true":
            continue
        columns = max(1, integer(region, "Columns", 1))
        rows = max(1, integer(region, "Rows", 1))
        regions.append(
            {
                "name": region.get("Name"),
                "id": region.get("Id"),
                "columns": columns,
                "rows": rows,
                "tile_count": columns * rows,
            }
        )
    return regions


def active_tile_count(block: ET.Element) -> int:
    """Return the largest per-scene M count from active tile grids."""
    return max(
        (region["tile_count"] for region in extract_tile_regions(block)),
        default=1,
    )


def extract_positions(block: ET.Element) -> list[dict[str, Any]]:
    positions: list[dict[str, Any]] = []
    regions_setup = find_active_dimension_setup(block, "RegionsSetup")
    sample_holder = regions_setup.find("./SampleHolder") if regions_setup is not None else None
    arrays = (
        sample_holder.findall("./SingleTileRegionArrays/SingleTileRegionArray") if sample_holder is not None else []
    )
    scene_index = 0
    # Carrier-based exports group positions by well in SingleTileRegionArray elements.
    for well in arrays:
        if not is_active(well) or child_text(well, "IsUsedForAcquisition", "true") != "true":
            continue
        well_name = well.get("Name", "")
        row, column = parse_well_id(well_name)
        field_index = 0
        for position in well.findall("./SingleTileRegions/SingleTileRegion"):
            if child_text(position, "IsUsedForAcquisition", "true") != "true":
                continue
            field_index += 1
            positions.append(
                {
                    "scene_index": scene_index,
                    "well_id": well_name,
                    "well_row": row,
                    "well_column": column,
                    "well_block_id": well.get("Id"),
                    "field_index": field_index,
                    "position_name": position.get("Name"),
                    "position_id": position.get("Id"),
                    "stage_position": {
                        "x": number(position, "X"),
                        "y": number(position, "Y"),
                        "z": number(position, "Z"),
                    },
                }
            )
            scene_index += 1
    if positions or sample_holder is None:
        return positions

    # Carrier-free exports can store all free positions directly under SampleHolder.
    for position in sample_holder.findall("./SingleTileRegions/SingleTileRegion"):
        if (child_text(position, "IsUsedForAcquisition", "true") or "true").lower() != "true":
            continue
        positions.append(
            {
                "scene_index": scene_index,
                "well_id": None,
                "well_row": None,
                "well_column": None,
                "field_index": None,
                "position_name": position.get("Name"),
                "position_id": position.get("Id"),
                "stage_position": {
                    "x": number(position, "X"),
                    "y": number(position, "Y"),
                    "z": number(position, "Z"),
                },
            }
        )
        scene_index += 1
    if positions:
        assign_template_wells(positions, sample_holder)
        return positions

    # Older carrier-mode exports encode one field per TileRegion and identify its well
    # through TemplateShapeId (row-column) or, as a fallback, the region name.
    field_counts: dict[tuple[int, int], int] = {}
    tile_regions = sample_holder.findall("./TileRegions/TileRegion")
    for region in tile_regions:
        if child_text(region, "IsUsedForAcquisition", "true") != "true":
            continue
        row, column = tile_region_well(region)
        if row is None or column is None:
            return []
        center = coordinate_pair(region, "CenterPosition")
        key = (row, column)
        field_counts[key] = field_counts.get(key, 0) + 1
        positions.append(
            {
                "scene_index": scene_index,
                "well_id": well_id(row, column),
                "well_row": row,
                "well_column": column,
                "field_index": field_counts[key],
                "position_name": region.get("Name"),
                "position_id": region.get("Id"),
                "stage_position": {
                    "x": center[0] if center is not None else None,
                    "y": center[1] if center is not None else None,
                    "z": number(region, "Z"),
                },
            }
        )
        scene_index += 1
    return positions


def suggested_filename(base_name: str, position: dict[str, Any]) -> str:
    name = position["position_name"] or "Position"
    well_suffix = f"-{position['well_id']}" if position["well_id"] else ""
    return f"{base_name}-Scene-{position['scene_index'] + 1:03d}-{name}{well_suffix}.czi"


def extract_block(block: ET.Element, block_index: int, autosave_name: str) -> dict[str, Any]:
    positions = extract_positions(block)
    tile_regions = extract_tile_regions(block)
    channels = active_channels(block)
    width, height = parse_detector_frame(block)
    time_points = active_dimension_count(block, "TimeSeriesSetup", "Duration/Cycles")
    z_slices = 1
    z_spacing = 1.0
    z_stack = find_active_dimension_setup(block, "ZStackSetup")
    if z_stack is not None:
        first = number(z_stack, "First/Distance/Value")
        last = number(z_stack, "Last/Distance/Value")
        interval = number(z_stack, "Interval/Distance/Value")
        if first is not None and last is not None and interval:
            z_slices = round(abs(last - first) / abs(interval)) + 1
            z_spacing = abs(interval) * 1e6

    regions_setup = find_active_dimension_setup(block, "RegionsSetup")
    sample_holder = regions_setup.find("./SampleHolder") if regions_setup is not None else None
    split_scenes = child_text(sample_holder, "SplitScenesInSeparateFiles", "false") == "true"
    scene_count = max(1, len(positions)) if positions else max(1, len(tile_regions))
    dimensions = {
        "X": width,
        "Y": height,
        "C": max(1, len(channels)),
        "Z": z_slices,
        "ZSpacing": z_spacing,
        "T": time_points,
        "M": active_tile_count(block),
        "S": scene_count,
    }
    if split_scenes and positions:
        outputs = [
            {
                "output_index": index,
                "zen_filename": None,
                "suggested_filename": suggested_filename(autosave_name, position),
                "dimensions": {**dimensions, "S": 1},
                "well_ids": [position["well_id"]] if position["well_id"] else [],
                "scene_indices": [position["scene_index"]],
            }
            for index, position in enumerate(positions)
        ]
    else:
        outputs = [
            {
                "output_index": 0,
                "zen_filename": None,
                "suggested_filename": f"{autosave_name}.czi",
                "dimensions": dimensions.copy(),
                "well_ids": list(dict.fromkeys(position["well_id"] for position in positions if position["well_id"])),
                "scene_indices": [position["scene_index"] for position in positions] or [0],
            }
        ]

    return {
        "block_index": block_index,
        "block_reference": block.get("BlockReference"),
        "split_scenes_in_separate_files": split_scenes,
        "dimensions": dimensions,
        "individual_scene_dimensions": {**dimensions, "S": 1},
        "channels": channels,
        "tile_regions": tile_regions,
        "tile_count": dimensions["M"],
        "well_count": len({position["well_id"] for position in positions if position["well_id"]}),
        "position_count": len(positions),
        "positions": positions,
        "planned_czi_count": len(outputs),
        "planned_outputs": outputs,
        "unresolved": {
            "stream_channel_mapping": (
                "C counts active channels in the experiment XML. ZEN may expose a different "
                "FramePosition.c count; use live ExperimentStatus for pixel-stream dimensions."
            ),
            "exact_zen_filenames": (
                "The experiment does not expose ZEN's complete split-scene filename expansion. "
                "suggested_filename is deterministic but must not be treated as the ZEN filename."
            ),
            "scene_mapping_assumption": (
                "Each active SingleTileRegion is treated as one scene/field. Validate this mapping "
                "against the supported ZEN API and produced CZI metadata."
            ),
            "tile_mapping_assumption": (
                "Each active rectangular TileRegion describes one scene grid; M is the largest "
                "Columns * Rows count. Validate against live FramePosition.s/m values because XML "
                "geometry and stream indexing can differ."
            ),
        },
    }


def extract_plan_xml(xml: str, source_name: str = "<experiment-export>") -> dict[str, Any]:
    """Extract an acquisition plan from XML returned by the ZEN API."""
    root = ET.fromstring(xml)
    experiment_blocks = root.find("ExperimentBlocks")
    if experiment_blocks is None:
        raise ValueError("The experiment does not contain <ExperimentBlocks>.")

    autosave_name = child_text(root, "AutoSave/Name", Path(source_name).stem) or Path(source_name).stem
    blocks = [
        extract_block(block, index, autosave_name)
        for index, block in enumerate(experiment_blocks.findall("AcquisitionBlock"))
        if is_active(block)
    ]
    return {
        "schema": "experimental.czexp-acquisition-plan/0.1",
        "source": {
            "path": source_name,
            "sha256": hashlib.sha256(xml.encode("utf-8")).hexdigest(),
            "hardware_experiment_version": root.get("Version"),
        },
        "basis": "Persisted ZEN experiment XML under ExperimentBlocks",
        "acquisition_blocks": blocks,
    }


def extract_plan(source: Path) -> dict[str, Any]:
    """Extract an acquisition plan from a persisted ``.czexp`` XML file."""
    return extract_plan_xml(source.read_text(encoding="utf-8"), str(source.resolve()))


def build_czmbi(plan: dict[str, Any], block_index: int = 0) -> ET.Element:
    """Build CZMBI 1.0 for one split-scene block.

    Exact ``zen_filename`` values take precedence. Deterministic
    ``suggested_filename`` values are used only when exact names are unavailable.
    """
    try:
        block = plan["acquisition_blocks"][block_index]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError(f"Acquisition block {block_index} is not available.") from error

    block_id = block.get("block_reference")
    if block_id is None:
        raise ValueError(f"Acquisition block {block_index} has no block reference for CZMBI BlockId.")

    # planned_outputs references position metadata by stable scene index.
    positions_by_scene = {
        position["scene_index"]: position
        for position in block.get("positions", [])
        if position.get("scene_index") is not None
    }
    root = ET.Element("MultiImageDocument", {"version": "1.0"})
    ET.SubElement(root, "Grouping")
    documents = ET.SubElement(root, "Documents")

    planned_outputs = block.get("planned_outputs", [])
    if not planned_outputs:
        raise ValueError(f"Acquisition block {block_index} contains no planned CZI outputs.")

    for output in planned_outputs:
        scene_indices = output.get("scene_indices", [])
        if len(scene_indices) != 1:
            raise UnsupportedCzmbiProjectionError(
                "CZMBI generation requires one planned output per scene; "
                f"output {output.get('output_index')} references {len(scene_indices)} scenes."
            )

        scene_index = scene_indices[0]
        position = positions_by_scene.get(scene_index)
        if position is None:
            raise ValueError(f"No position metadata exists for scene {scene_index}.")

        well = position.get("well_id")
        row = position.get("well_row")
        column = position.get("well_column")
        field = position.get("field_index")
        if well is None or row is None or column is None or field is None:
            raise ValueError(f"Scene {scene_index} has incomplete well/field metadata.")

        # The experiment XML currently provides no exact split-scene expansion, so
        # suggested_filename is an explicit provisional fallback for this projection.
        filename = output.get("zen_filename") or output.get("suggested_filename")
        if not filename:
            raise ValueError(f"Scene {scene_index} has no CZI filename.")

        document = ET.SubElement(
            documents,
            "Document",
            {
                "BlockId": str(block_id),
                "WellId": str(well),
                "Row": str(row),
                "Col": str(column),
                "Field": str(field),
            },
        )
        document.text = str(filename)

    return root


def write_czmbi(plan: dict[str, Any], destination: Path, block_index: int = 0) -> Path:
    """Write a CZMBI 1.0 XML file and return its destination path."""
    root = build_czmbi(plan, block_index)
    ET.indent(root, space="  ")
    xml = ET.tostring(root, encoding="unicode", short_empty_elements=False)
    destination.write_text(
        f'<?xml version="1.0" encoding="utf-8"?>\n{xml}\n',
        encoding="utf-8",
    )
    return destination


def write_czmbi_from_json(plan_source: Path, destination: Path, block_index: int = 0) -> Path:
    """Load an extracted plan JSON file and write its CZMBI 1.0 XML projection."""
    try:
        plan = json.loads(plan_source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid acquisition plan JSON: {plan_source}") from error
    if not isinstance(plan, dict):
        raise TypeError(f"Acquisition plan JSON must contain an object: {plan_source}")
    return write_czmbi(plan, destination, block_index)


def reduce_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Remove non-CZMBI ZEN identifiers from ``plan`` in place and return it."""
    for block in plan["acquisition_blocks"]:
        block.pop("size_estimate", None)
        # Keep BlockReference because CZMBI uses it as Document@BlockId.
        for channel in block["channels"]:
            channel.pop("id", None)
        for tile_region in block.get("tile_regions", []):
            tile_region.pop("id", None)
        for position in block["positions"]:
            position.pop("well_block_id", None)
            position.pop("position_id", None)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("experiment", type=Path, help="Path to a .czexp ZEN experiment XML file")
    parser.add_argument("-o", "--output", type=Path, help="Output JSON path")
    parser.add_argument(
        "--reduced",
        action="store_true",
        help=(
            "Omit channel, tile-region, and position IDs plus size_estimate; "
            "retain block_reference for CZMBI BlockId"
        ),
    )
    parser.add_argument(
        "--czmbi-output",
        type=Path,
        help="Also write a CZMBI 1.0 XML file for the first acquisition block",
    )
    args = parser.parse_args()

    default_suffix = ".reduced.plan.json" if args.reduced else ".plan.json"
    output = args.output or args.experiment.with_suffix(default_suffix)
    plan = extract_plan(args.experiment)
    if args.reduced:
        reduce_plan(plan)
    output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    if args.czmbi_output:
        try:
            print(f"Wrote {write_czmbi_from_json(output, args.czmbi_output)}")
        except UnsupportedCzmbiProjectionError as error:
            LOGGER.warning("%s CZMBI was skipped; the JSON plan is available at %s", error, output)
            return 1
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    raise SystemExit(main())
