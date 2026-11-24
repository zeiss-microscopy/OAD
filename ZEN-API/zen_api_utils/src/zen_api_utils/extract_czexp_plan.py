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

Index convention (plan schema 0.2 and typed positions): all block, scene,
well-row, well-column, well and field indices are zero-based. Block indices
refer to the original XML order, including skipped inactive blocks. Well indices
follow first appearance within each block; field indices restart per well, with
unassigned fields forming a separate group per block. Counts are not indices.
Well labels remain unchanged (B3 maps to row 1, column 2). XML and CZMBI
one-based coordinates are converted at their input/output boundaries.
Stage coordinates and full rectangular region dimensions are in micrometers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import re
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

LOGGER = logging.getLogger(__name__)
PLAN_SCHEMA = "experimental.czexp-acquisition-plan/0.2"
POSITION_FIELDS: tuple[str, ...] = (
    "block_index", "scene_index", "well_id", "well_row", "well_column",
    "well_index", "field_index", "position_name", "position_id",
    "stage_x_um", "stage_y_um", "stage_z_um", "tile_width_um", "tile_height_um",
)


@dataclass(frozen=True, slots=True)
class TileRegion:
    """Offline contour metadata; dimensions describe a full rectangle in micrometers.

    Nonrectangular contours retain their type but not shape-specific geometry.
    """

    contour_type: str | None
    width_um: float | None = None
    height_um: float | None = None


@dataclass(frozen=True, slots=True)
class Position:
    """An acquisition field following this module's index and unit convention."""

    block_index: int
    scene_index: int
    well_id: str | None
    well_row: int | None
    well_column: int | None
    well_index: int | None
    field_index: int
    position_name: str | None
    position_id: str | None
    x: float | None
    y: float | None
    z: float | None
    tile_region: TileRegion | None = None

    def to_record(self) -> dict[str, object]:
        """Flatten the position to the CSV/DataFrame column schema."""
        return {
            "block_index": self.block_index,
            "scene_index": self.scene_index,
            "well_id": self.well_id,
            "well_row": self.well_row,
            "well_column": self.well_column,
            "well_index": self.well_index,
            "field_index": self.field_index,
            "position_name": self.position_name,
            "position_id": self.position_id,
            "stage_x_um": self.x,
            "stage_y_um": self.y,
            "stage_z_um": self.z,
            "tile_width_um": self.tile_region.width_um if self.tile_region is not None else None,
            "tile_height_um": self.tile_region.height_um if self.tile_region is not None else None,
        }


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
    """Convert an Excel-style label to internal well indices."""
    match = re.fullmatch(r"([A-Za-z]+)(\d+)", well_id)
    if not match or int(match.group(2)) < 1:
        return None, None
    row = 0
    for letter in match.group(1).upper():
        row = row * 26 + ord(letter) - ord("A") + 1
    return row - 1, int(match.group(2)) - 1


def well_id(row: int, column: int) -> str:
    """Convert internal well indices to an Excel-style label."""
    if row < 0 or column < 0:
        raise ValueError("Well indices must be nonnegative.")
    letters = ""
    value = row + 1
    while value > 0:
        value, remainder = divmod(value - 1, 26)
        letters = chr(ord("A") + remainder) + letters
    return f"{letters}{column + 1}"


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
        row, column = int(match.group(1)), int(match.group(2))
        if row < 1 or column < 1:
            return None, None
        return row - 1, column - 1
    return parse_well_id(region.get("Name", ""))


class UnsupportedCarrierGeometryError(ValueError):
    """The experiment's carrier cannot be mapped by the supported geometry model."""


@dataclass(frozen=True, slots=True)
class WellAssignment:
    """A physical well label and zero-based row/column, independent of acquisition selection."""

    well_id: str
    well_row: int
    well_column: int


@dataclass(frozen=True, slots=True)
class CarrierGeometry:
    """An unrotated rectangular well grid in absolute stage micrometers.

    Only centered regular grids with unswitched, noninverted axes and a zero
    TopLeft reference are supported. Width/height must be smaller than pitch:
    touching/overlapping wells are rejected to avoid ambiguous edge assignment.
    All physical wells are considered, regardless of selected well containers.

    Coordinates must share the experiment's stage origin, calibration and plate
    placement. This model cannot verify that condition or correct stage drift.
    It classifies points, not whole images or tile footprints; Z is irrelevant.
    """

    rows: int
    columns: int
    center_x_um: float
    center_y_um: float
    pitch_x_um: float
    pitch_y_um: float
    well_width_um: float
    well_height_um: float

    def __post_init__(self) -> None:
        if (
            not isinstance(self.rows, int) or isinstance(self.rows, bool) or self.rows < 1
            or not isinstance(self.columns, int) or isinstance(self.columns, bool) or self.columns < 1
        ):
            raise ValueError("Carrier rows and columns must be positive integers.")
        values = (
            self.center_x_um, self.center_y_um, self.pitch_x_um, self.pitch_y_um,
            self.well_width_um, self.well_height_um,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("Carrier geometry must contain finite values.")
        if not (0 < self.well_width_um < self.pitch_x_um and 0 < self.well_height_um < self.pitch_y_um):
            raise UnsupportedCarrierGeometryError("Well dimensions must be positive and smaller than their pitch.")

    def locate(self, x_um: float, y_um: float) -> WellAssignment | None:
        """Return the containing well, or None for gaps/outside the plate.

        Rectangle edges are included, without an added tolerance or snapping.
        Non-finite input raises ValueError rather than appearing unassigned.
        """
        if not math.isfinite(x_um) or not math.isfinite(y_um):
            raise ValueError("Stage XY coordinates must be finite micrometer values.")
        column_center = (self.columns - 1) / 2
        row_center = (self.rows - 1) / 2
        column = math.floor((x_um - self.center_x_um) / self.pitch_x_um + column_center + 0.5)
        row = math.floor((y_um - self.center_y_um) / self.pitch_y_um + row_center + 0.5)
        if not (0 <= column < self.columns and 0 <= row < self.rows):
            return None
        center_x = self.center_x_um + (column - column_center) * self.pitch_x_um
        center_y = self.center_y_um + (row - row_center) * self.pitch_y_um
        if abs(x_um - center_x) > self.well_width_um / 2 or abs(y_um - center_y) > self.well_height_um / 2:
            return None
        return WellAssignment(well_id(row, column), row, column)

    def assign_positions(self, xy_um: Sequence[tuple[float, float]]) -> list[WellAssignment | None]:
        """Return one assignment per input XY pair, preserving order and duplicates.

        None means a valid point lies outside every configured well rectangle,
        not that the template is unsupported. Unsupported geometry fails when
        loaded; invalid coordinates raise rather than produce a partial result.
        """
        return [self.locate(x, y) for x, y in xy_um]


def _carrier_geometry(sample_holder: ET.Element) -> CarrierGeometry:
    template = sample_holder.find("./Template")
    if template is None or (child_text(template, "HasRegularShapes", "false") or "false").lower() != "true":
        raise UnsupportedCarrierGeometryError("A regular sample-carrier Template is required.")

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
        or rotation != 0.0
        or not all(math.isfinite(value) for value in (*reference, *anchor, *immersion, pitch_x, pitch_y, width, height))
        or child_text(template, "ShapeType") != "Rectangle"
        or reference != (0.0, 0.0)
        or child_text(template, "ReferencePointLocationMode") != "TopLeft"
        or (child_text(template, "AreShapesCenteredX", "false") or "false").lower() != "true"
        or (child_text(template, "AreShapesCenteredY", "false") or "false").lower() != "true"
        or (child_text(template, "AreAxisAnnotationsSwitched", "false") or "false").lower() == "true"
        or (child_text(template, "IsRowAnnotationDirectionInverted", "false") or "false").lower() == "true"
        or (child_text(template, "IsColumnAnnotationDirectionInverted", "false") or "false").lower() == "true"
    ):
        raise UnsupportedCarrierGeometryError(
            "Carrier requires finite rectangular geometry, zero rotation/reference, "
            "TopLeft reference mode, centered shapes and unswitched, noninverted axes."
        )

    # In this ZEN template layout, AnchorPoint offsets ImmersionPoint to the grid center.
    return CarrierGeometry(rows, columns, immersion[0] + anchor[0], immersion[1] + anchor[1],
                           pitch_x, pitch_y, width, height)


def carrier_geometry_from_xml(xml: str, *, block_index: int = 0) -> CarrierGeometry:
    """Load carrier geometry even when the experiment has no acquisition positions.

    block_index selects the nth active acquisition block. Multiple blocks are
    never merged or searched for a silently substituted carrier. Only the active
    RegionsSetup is used. Missing/unsupported geometry raises ValueError.
    Malformed XML propagates ElementTree.ParseError. No ZEN connection is made.
    """
    root = ET.fromstring(xml)
    blocks = [block for block in root.findall("./ExperimentBlocks/AcquisitionBlock") if is_active(block)]
    if not 0 <= block_index < len(blocks):
        raise ValueError(f"Active acquisition block {block_index} is not available.")
    setup = find_active_dimension_setup(blocks[block_index], "RegionsSetup")
    holder = setup.find("SampleHolder") if setup is not None else None
    if holder is None:
        raise UnsupportedCarrierGeometryError("Active RegionsSetup with SampleHolder is required.")
    return _carrier_geometry(holder)


def load_carrier_geometry(experiment: str | Path, *, block_index: int = 0) -> CarrierGeometry:
    """Read a CZEXP once as a geometry-only reference; see CarrierGeometry boundaries."""
    return carrier_geometry_from_xml(Path(experiment).read_text(encoding="utf-8"), block_index=block_index)


def assign_template_wells(positions: list[dict[str, Any]], sample_holder: ET.Element) -> None:
    """Assign parser positions with the same geometry used by the public XY API.

    Missing/unsupported templates leave metadata unchanged with a warning.
    Unlike the strict public loader, acquisition-plan extraction can still
    return positions without inferred wells. Explicit well metadata is preserved.
    """
    try:
        geometry = _carrier_geometry(sample_holder)
    except UnsupportedCarrierGeometryError as error:
        LOGGER.warning("Template well assignment skipped: %s", error)
        return
    for position in positions:
        if position.get("well_id"):
            continue
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

        assignment = geometry.locate(x, y)
        if assignment is not None:
            position.update(
                well_id=assignment.well_id,
                well_row=assignment.well_row,
                well_column=assignment.well_column,
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
    """Extract active tile grids and their contour metadata from the sample holder."""
    regions_setup = find_active_dimension_setup(block, "RegionsSetup")
    sample_holder = regions_setup.find("./SampleHolder") if regions_setup is not None else None
    tile_regions = sample_holder.findall("./TileRegions/TileRegion") if sample_holder is not None else []
    regions: list[dict[str, Any]] = []
    for region in tile_regions:
        if (child_text(region, "IsUsedForAcquisition", "true") or "true").lower() != "true":
            continue
        columns = max(1, integer(region, "Columns", 1))
        rows = max(1, integer(region, "Rows", 1))
        contour = region.find("Contour")
        contour_type = contour.get("Type") if contour is not None else None
        width = height = None
        if contour_type == "Rectangle":
            try:
                width, height = (float(value) for value in (child_text(region, "ContourSize") or "").split(","))
                if not all(math.isfinite(value) and value > 0 for value in (width, height)):
                    raise ValueError("Dimensions must be finite and positive.")
            except ValueError as error:
                raise ValueError(
                    "Invalid rectangular tile-region ContourSize in "
                    f"block {block.get('BlockReference')}, region {region.get('Id') or region.get('Name')}"
                ) from error
        regions.append(
            {
                "name": region.get("Name"),
                "id": region.get("Id"),
                "columns": columns,
                "rows": rows,
                "tile_count": columns * rows,
                "contour_type": contour_type,
                "width_um": width,
                "height_um": height,
            }
        )
    return regions


def active_tile_count(block: ET.Element) -> int:
    """Return the largest per-scene M count from active tile grids."""
    return max(
        (region["tile_count"] for region in extract_tile_regions(block)),
        default=1,
    )


def _index_positions(positions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    well_indices: dict[str, int] = {}
    field_counts: dict[str | None, int] = {}
    for position in positions:
        well = position["well_id"] or None
        position["well_index"] = well_indices.setdefault(well, len(well_indices)) if well else None
        position["field_index"] = field_counts.get(well, 0)
        field_counts[well] = position["field_index"] + 1
    return positions


def extract_positions(
    block: ET.Element, tile_regions: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    """Extract active fields using this module's index and unit convention."""
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
        for position in well.findall("./SingleTileRegions/SingleTileRegion"):
            if child_text(position, "IsUsedForAcquisition", "true") != "true":
                continue
            positions.append(
                {
                    "scene_index": scene_index,
                    "well_id": well_name,
                    "well_row": row,
                    "well_column": column,
                    "well_block_id": well.get("Id"),
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
        return _index_positions(positions)

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
        return _index_positions(positions)

    # Older carrier-mode exports encode one field per TileRegion and identify its well
    # through TemplateShapeId (row-column) or, as a fallback, the region name.
    region_elements = [
        region for region in sample_holder.findall("./TileRegions/TileRegion")
        if (child_text(region, "IsUsedForAcquisition", "true") or "true").lower() == "true"
    ]
    metadata = extract_tile_regions(block) if tile_regions is None else tile_regions
    for region, geometry in zip(region_elements, metadata, strict=True):
        row, column = tile_region_well(region)
        center = coordinate_pair(region, "CenterPosition")
        positions.append(
            {
                "scene_index": scene_index,
                "well_id": well_id(row, column) if row is not None and column is not None else None,
                "well_row": row,
                "well_column": column,
                "position_name": region.get("Name"),
                "position_id": region.get("Id"),
                "stage_position": {
                    "x": center[0] if center is not None else None,
                    "y": center[1] if center is not None else None,
                    "z": number(region, "Z"),
                },
                "tile_region": {
                    "contour_type": geometry["contour_type"],
                    "width_um": geometry["width_um"],
                    "height_um": geometry["height_um"],
                },
            }
        )
        scene_index += 1
    return _index_positions(positions)


def suggested_filename(base_name: str, position: dict[str, Any]) -> str:
    name = position["position_name"] or "Position"
    well_suffix = f"-{position['well_id']}" if position["well_id"] else ""
    return f"{base_name}-Scene-{position['scene_index'] + 1:03d}-{name}{well_suffix}.czi"


def extract_block(block: ET.Element, block_index: int, autosave_name: str) -> dict[str, Any]:
    tile_regions = extract_tile_regions(block)
    positions = extract_positions(block, tile_regions)
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
        "M": max((region["tile_count"] for region in tile_regions), default=1),
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
        "schema": PLAN_SCHEMA,
        "source": {
            "path": source_name,
            "sha256": hashlib.sha256(xml.encode("utf-8")).hexdigest(),
            "hardware_experiment_version": root.get("Version"),
        },
        "basis": "Persisted ZEN experiment XML under ExperimentBlocks",
        "acquisition_blocks": blocks,
    }


def extract_plan(source: str | Path) -> dict[str, Any]:
    """Extract an acquisition plan from a persisted ``.czexp`` XML file."""
    source = Path(source)
    return extract_plan_xml(source.read_text(encoding="utf-8"), str(source.resolve()))


def _require_current_schema(plan: dict[str, Any]) -> None:
    if plan.get("schema") != PLAN_SCHEMA:
        raise ValueError(f"Expected plan schema {PLAN_SCHEMA}; re-extract legacy plans from the original CZEXP.")


def positions_from_plan(plan: dict[str, Any], *, block_index: int | None = None) -> list[Position]:
    """Build typed positions without reparsing XML.

    By default all active blocks are included. ``block_index`` selects an ordinal
    in the active-block list, not the original XML block index. Empty plans
    return an empty list. Missing metadata stays None.
    """
    _require_current_schema(plan)
    blocks = plan["acquisition_blocks"]
    if block_index is not None:
        if not 0 <= block_index < len(blocks):
            raise ValueError(f"Active acquisition block {block_index} is not available.")
        blocks = [blocks[block_index]]
    positions: list[Position] = []
    for block in blocks:
        for position in block["positions"]:
            stage = position["stage_position"]
            region = position.get("tile_region")
            positions.append(
                Position(
                    block_index=block["block_index"],
                    scene_index=position["scene_index"],
                    well_id=position["well_id"],
                    well_row=position["well_row"],
                    well_column=position["well_column"],
                    well_index=position["well_index"],
                    field_index=position["field_index"],
                    position_name=position.get("position_name"),
                    position_id=position.get("position_id"),
                    x=stage["x"],
                    y=stage["y"],
                    z=stage["z"],
                    tile_region=TileRegion(**region) if region is not None else None,
                )
            )
    return positions


def load_experiment_positions(experiment: str | Path) -> list[Position]:
    """Read a CZEXP once and return its typed acquisition positions, without I/O output."""
    return positions_from_plan(extract_plan(experiment))


def positions_to_dataframe(positions: Sequence[Position]) -> pd.DataFrame:
    """Convert typed positions to a nullable pandas table; requires the dataframe extra."""
    try:
        import pandas as pd
    except ModuleNotFoundError as error:
        if error.name != "pandas":
            raise
        raise ImportError("Position tables require pandas; install 'zen_api_utils[dataframe]'.") from error
    return pd.DataFrame.from_records(
        [position.to_record() for position in positions], columns=POSITION_FIELDS
    ).astype(
        {
            "block_index": "Int64",
            "scene_index": "Int64",
            "well_id": "string",
            "well_row": "Int64",
            "well_column": "Int64",
            "well_index": "Int64",
            "field_index": "Int64",
            "position_name": "string",
            "position_id": "string",
            "stage_x_um": "Float64",
            "stage_y_um": "Float64",
            "stage_z_um": "Float64",
            "tile_width_um": "Float64",
            "tile_height_um": "Float64",
        }
    )


def load_experiment_positions_dataframe(experiment: str | Path) -> pd.DataFrame:
    """Read a CZEXP and return a table without printing or writing files."""
    return positions_to_dataframe(load_experiment_positions(experiment))


def build_czmbi(plan: dict[str, Any], block_index: int = 0) -> ET.Element:
    """Build CZMBI 1.0 for one split-scene block.

    Exact ``zen_filename`` values take precedence. Deterministic
    ``suggested_filename`` values are used only when exact names are unavailable.
    """
    _require_current_schema(plan)
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
                "Row": str(row + 1),
                "Col": str(column + 1),
                "Field": str(field + 1),
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
