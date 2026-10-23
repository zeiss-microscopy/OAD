"""Example: use the ZEN experiment extractor from another Python script."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from extract_czexp_plan import (
    UnsupportedCzmbiProjectionError,
    extract_plan,
    reduce_plan,
    write_czmbi_from_json,
)

LOGGER = logging.getLogger(__name__)

# CZMBI requires one planned CZI output per scene.
experiment_path = Path(
    r"V:\Source\RMS-DEV\LIF_Athena_Doc\experimental\ZEN_API_Well_Activation2_no_carrier_mode_split_scenes.czexp"
)

# Extract the complete plan as ordinary Python dictionaries and lists.
plan = extract_plan(experiment_path)
block = plan["acquisition_blocks"][0]

print("Complete acquisition dimensions:", block["dimensions"])
print("Individual scene dimensions:", block["individual_scene_dimensions"])
print("Wells:", block["well_count"])
print("Positions:", block["position_count"])
print("Planned CZI files:", block["planned_czi_count"])

# Access a planned split-scene CZI directly.
first_output = block["planned_outputs"][0]
print("First suggested filename:", first_output["suggested_filename"])
print("First output dimensions:", first_output["dimensions"])
first_well = first_output["well_ids"][0] if first_output["well_ids"] else None
print("First output well:", first_well)

# Remove internal ZEN IDs before passing the plan to another component.
reduced_plan = reduce_plan(plan)

# Persist the plan as the inspectable handoff for CZMBI generation.
output_path = experiment_path.with_suffix(".programmatic.reduced.plan.json")
output_path.write_text(json.dumps(reduced_plan, indent=2) + "\n", encoding="utf-8")
print("Wrote:", output_path)

# Attempt CZMBI generation; aggregate multi-scene outputs are skipped with a warning.
czmbi_path = experiment_path.with_suffix(".czmbi")
try:
    write_czmbi_from_json(output_path, czmbi_path)
except UnsupportedCzmbiProjectionError as error:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    LOGGER.warning("%s CZMBI was skipped; the JSON plan is available at %s", error, output_path)
    raise SystemExit(1) from None
else:
    print("Wrote:", czmbi_path)
