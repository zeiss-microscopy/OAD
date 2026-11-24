"""Export acquisition positions and their containing wells from a ZEN CZEXP.

Uses zen_api_utils' typed offline parser; no running ZEN is required.
Records follow the utility's zero-based index and micrometer unit convention.
The terminal table converts indices to one-based display values.
extract_positions_dataframe() requires the utility's optional dataframe extra.
"""

import argparse
import csv
import sys
from pathlib import Path

from rich import box
from rich.console import Console
from rich.table import Table
from zen_api_utils.extract_czexp_plan import (
    POSITION_FIELDS as CSV_FIELDS,
)
from zen_api_utils.extract_czexp_plan import (
    Position,
    TileRegion,
)
from zen_api_utils.extract_czexp_plan import (
    load_experiment_positions as extract_positions,
)
from zen_api_utils.extract_czexp_plan import (
    load_experiment_positions_dataframe as extract_positions_dataframe,
)

__all__ = [
    "CSV_FIELDS",
    "Position",
    "TileRegion",
    "extract_positions",
    "extract_positions_dataframe",
    "print_positions",
]

ROOT_FOLDER = Path(__file__).resolve().parent
DEFAULT_EXPERIMENT = ROOT_FOLDER / "data" / "ZEN_API_Test_CD7_Random_Positions.czexp"
# DEFAULT_EXPERIMENT = ROOT_FOLDER / "data" / "ZEN_API_Test_CD7_Random_Positions_empty_W96.czexp"
# DEFAULT_EXPERIMENT = ROOT_FOLDER / "data" / "ZEN_API_Test_CD7_Position_Arrays.czexp"


def print_positions(positions: list[Position], *, title: str) -> None:
    """Display already-extracted positions with the same formatting as the CLI."""
    table = Table(title=title, box=box.ASCII, header_style="bold")
    columns = (
        ("block_index", "Block"),
        ("scene_index", "Scene"),
        ("well_id", "Well"),
        ("well_index", "Well number"),
        ("well_row", "Row"),
        ("well_column", "Column"),
        ("field_index", "Field"),
        ("position_name", "Position"),
        ("stage_x_um", "X (um)"),
        ("stage_y_um", "Y (um)"),
        ("stage_z_um", "Z (um)"),
        ("tile_width_um", "Tile width (um)"),
        ("tile_height_um", "Tile height (um)"),
    )
    for key, label in columns:
        alignment = "left" if key in {"well_id", "position_name"} else "right"
        table.add_column(label, justify=alignment)
    for position in positions:
        row = position.to_record()
        values = []
        for key, _ in columns:
            value = row[key]
            if isinstance(value, int) and key in {
                "block_index",
                "scene_index",
                "well_index",
                "well_row",
                "well_column",
                "field_index",
            }:
                value += 1
            if isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append("-" if value is None else str(value))
        table.add_row(*values)
    Console().print(table)


def main() -> None:
    """Display a terminal table and optionally save the complete CSV."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "experiment",
        nargs="?",
        type=Path,
        default=DEFAULT_EXPERIMENT,
        help="Input CZEXP (default: the workshop well-plate experiment)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Also save CSV here; existing files are replaced",
    )
    args = parser.parse_args()
    positions = extract_positions(args.experiment)
    if not positions:
        parser.error(f"No acquisition positions found in {args.experiment}")
    if args.output is not None:
        if args.output.resolve() == args.experiment.resolve():
            parser.error("--output must not overwrite the input experiment")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(position.to_record() for position in positions)
    print_positions(positions, title=args.experiment.name)
    wells = {position.well_id for position in positions if position.well_id}
    print(
        f"Extracted {len(positions)} positions in {len(wells)} wells"
        + (f" -> {args.output}" if args.output is not None else ""),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
