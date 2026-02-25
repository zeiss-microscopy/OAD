# -*- coding: utf-8 -*-

#################################################################
# File        : config.py
# Author      : SRh
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

from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# ZEN-API connection
# ---------------------------------------------------------------------------

# Path to the gRPC config file (absolute, or relative to cd7_workflow.py)
CONFIG_FILE: str = r"F:\GitHub\OAD\ZEN-API\python_examples\my_config.ini"

# ---------------------------------------------------------------------------
# Wells to visit (well IDs in Excel-style notation, e.g. "A1", "H12")
# ---------------------------------------------------------------------------

WELLS: list[str] = ["A1", "A2", "A3", "B1", "B2", "C5", "D6", "H12"]

# ---------------------------------------------------------------------------
# Experiment names (without the .czexp extension)
# ---------------------------------------------------------------------------

# Experiment used for Software Autofocus (SWAF) — typically a fast single-channel snap
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
# Z-stack parameters applied per well (in metres)
# ---------------------------------------------------------------------------

# Total z-stack range
MODIFY_ZSTACK: bool = False

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

# Timestamp format appended to each well ID to build the output filename
# e.g. "A1_20260225_143022"
FILENAME_TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"

# Folder where ZEN saves CZI files
# Must match the "Image output path" configured in ZEN.
IMAGE_FOLDER: Path = Path(r"f:\Zen_Output\cd7_workflow")
EXPERIMENT_SUBFOLDER: Path = (
    IMAGE_FOLDER / f"Experiment_{datetime.now().strftime(FILENAME_TIMESTAMP_FORMAT)}"
)  # Subfolder per experiment (can be empty)


# ---------------------------------------------------------------------------
# Image analysis (ZEN Workflow job queue)
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

# Timeout passed to find_auto_focus() (seconds)
SWAF_TIMEOUT_S: int = 15
