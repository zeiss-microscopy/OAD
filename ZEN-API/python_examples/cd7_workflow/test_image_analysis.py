#################################################################
# File        : test_image_analysis.py
# Institution : Carl Zeiss Microscopy GmbH
#
# Minimal hardware-independent smoke test for run_analysis().
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
# Make processing_tools importable when running from this subfolder.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from image_analysis import run_analysis

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
# Change this path to analyze another CZI without running the microscope
# acquisition workflow.
CZI_FILE = Path(__file__).resolve().with_name("Z=7.czi")


async def main() -> None:
    """Analyze the bundled CZI and print per-plane counts and a summary."""
    print(f"CZI file : {CZI_FILE}")
    print(f"Exists   : {CZI_FILE.exists()}")

    if not CZI_FILE.exists():
        print("ERROR: CZI file not found — aborting.")
        return

    # run_analysis is async so this test uses the same call pattern as the
    # background worker, while avoiding any ZEN API connection or movement.
    print("\nRunning analysis ...")
    counts = await run_analysis(CZI_FILE)

    print("\n--- Results ---")
    for z_plane, count in enumerate(counts):
        print(f"  Z-plane {z_plane:>3d} : {count:>6d} objects")

    print("\n--- Summary ---")
    print(f"  Z-planes analysed : {len(counts)}")
    print(f"  Min objects/plane : {min(counts)}")
    print(f"  Max objects/plane : {max(counts)}")
    print(f"  Avg objects/plane : {sum(counts) / len(counts):.1f}")


if __name__ == "__main__":
    asyncio.run(main())
