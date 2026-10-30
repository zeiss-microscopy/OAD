#################################################################
# File        : workflow_config.py
# Institution : Carl Zeiss Microscopy GmbH
#
# All user-tunable parameters for the CD7 per-well acquisition
# and parallel image-analysis workflow.
# Edit this file only — do not touch the other modules.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# ZEN-API connection
# ---------------------------------------------------------------------------

# Absolute paths are used directly. Relative paths start at python_examples.
CONFIG_FILE: str = r"F:\GitHub\ZEN_API\python_examples\my_config.ini"

# ---------------------------------------------------------------------------
# Wells to visit (well IDs in Excel-style notation, e.g. "A1", "H12")
# ---------------------------------------------------------------------------

WELLS: list[str] = ["A1", "A2", "A3", "B1", "B2", "C5", "D6", "H12"]

# Reorder WELLS with a nearest-neighbor heuristic to reduce stage travel.
# The first configured well remains the starting point.
OPTIMIZE_WELL_ORDER: bool = True

# ---------------------------------------------------------------------------
# Experiment names (without the .czexp extension)
# ---------------------------------------------------------------------------

# SWAF (software autofocus) normally uses a fast, single-channel experiment.
RUN_SWAF: bool = False
SWAF_EXPERIMENT: str = "ZEN_API_CD7_Workflow"

# Experiment used for the real acquisition (z-stack, multi-channel, …)
ACQ_EXPERIMENT: str = "ZEN_API_CD7_Workflow"

# ---------------------------------------------------------------------------
# Objective changer positions
# ---------------------------------------------------------------------------

# Changer position of the lower-magnification objective used for SWAF
CHANGE_TO_SWAF_OBJECTIVE: bool = False
OBJECTIVE_POS_SWAF: int = 2

# Changer position of the higher-magnification objective used for acquisition
CHANGE_TO_ACQ_OBJECTIVE: bool = False
OBJECTIVE_POS_ACQ: int = 4

# ---------------------------------------------------------------------------
# Per-well Z-stack updates
# ---------------------------------------------------------------------------

# When enabled, the workflow clones ACQ_EXPERIMENT once and updates that
# reusable clone's Z-stack center for each well. This requires RUN_SWAF = True.
MODIFY_ZSTACK: bool = True
ZSTACK_RANGE_M: float = 20.0 * 1e-6
ZSTACK_INTERVAL_M: float = 3.0 * 1e-6

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

# Timestamp format appended to each well ID to build the output filename
# e.g. "A1_20260225_143022"
FILENAME_TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"

# Keep CZI files in ZEN's configured image output folder and write the result
# CSV there as well. This is fastest because the run API cannot select another
# output directory and no post-acquisition file move is required.
USE_ZEN_OUTPUT_FOLDER_DIRECTLY: bool = False

# Destination root used only when USE_ZEN_OUTPUT_FOLDER_DIRECTLY is False.
IMAGE_FOLDER: Path = Path(r"f:\Zen_Output\cd7_workflow")
EXPERIMENT_SUBFOLDER: Path = (
    IMAGE_FOLDER / f"Experiment_{datetime.now(timezone.utc).strftime(FILENAME_TIMESTAMP_FORMAT)}"
)  # Created on demand when the first CZI or result CSV is written.


# ---------------------------------------------------------------------------
# Local image analysis queue
# ---------------------------------------------------------------------------

RUN_IMAGE_ANALYSIS: bool = True

# ---------------------------------------------------------------------------
# File-ready detection (polling-based, no OS file-watcher dependency)
# ---------------------------------------------------------------------------

# How often to check whether the CZI file exists / has grown (seconds)
POLL_INTERVAL_S: float = 1.0

# How long the file size must be unchanged before it is considered fully written (seconds)
FILE_SETTLE_S: float = 3.0

# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------

# Short pause between stage moves to let the system settle (seconds)
MOVE_SETTLE_S: float = 0.5

# Timeout sent to the ZEN software-autofocus operation (seconds)
SWAF_TIMEOUT_S: int = 15
