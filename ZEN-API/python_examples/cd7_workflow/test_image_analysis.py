# -*- coding: utf-8 -*-

#################################################################
# File        : test_image_analysis.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# Minimal test script for run_analysis().
# Runs the analysis on a local CZI file and prints the per-plane
# object counts and a brief summary to the console.
#
# Usage:
#   python test_image_analysis.py
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Make zen_api_utils / processing_tools importable when running from this
# subfolder (cd7_workflow).
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from image_analysis import run_analysis

# ---------------------------------------------------------------------------
# Test file
# ---------------------------------------------------------------------------
CZI_FILE = Path(r"F:\GitHub\OAD\ZEN-API\python_examples\cd7_workflow\Z=7.czi")


async def main() -> None:
    print(f"CZI file : {CZI_FILE}")
    print(f"Exists   : {CZI_FILE.exists()}")

    if not CZI_FILE.exists():
        print("ERROR: CZI file not found — aborting.")
        return

    print("\nRunning analysis ...")
    counts = await run_analysis(CZI_FILE)

    print("\n--- Results ---")
    for z, n in enumerate(counts):
        print(f"  Z-plane {z:>3d} : {n:>6d} objects")

    print("\n--- Summary ---")
    print(f"  Z-planes analysed : {len(counts)}")
    print(f"  Min objects/plane : {min(counts)}")
    print(f"  Max objects/plane : {max(counts)}")
    print(f"  Avg objects/plane : {sum(counts) / len(counts):.1f}")


if __name__ == "__main__":
    asyncio.run(main())
