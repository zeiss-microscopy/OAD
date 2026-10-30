#################################################################
# File        : test_well_order.py
# Institution : Carl Zeiss Microscopy GmbH
#
# Focused unit tests for the stage-travel ordering helper. These
# tests require no ZEN connection or microscope hardware.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKFLOW_DIR))
sys.path.insert(0, str(WORKFLOW_DIR.parent))

from well_tasks import optimize_well_order  # noqa: E402
from zen_api_utils.sample_carrier import WellPlate  # noqa: E402


class OptimizeWellOrderTests(unittest.TestCase):
    """Check deterministic routing without microscope hardware."""

    def setUp(self) -> None:
        """Use an eight-row, twelve-column plate for each routing test."""
        self.plate = WellPlate(rows=8, cols=12)

    def test_orders_scattered_wells_by_nearest_neighbor(self) -> None:
        """Visit the nearest remaining well while keeping the starting well."""
        wells = ["A1", "A2", "A3", "B1", "B2", "C5", "D6", "H12"]

        result = optimize_well_order(self.plate, wells)

        self.assertEqual(result, ["A1", "A2", "A3", "B2", "B1", "C5", "D6", "H12"])

    def test_equal_distances_preserve_original_order(self) -> None:
        """Break equal-distance ties using the original worklist order."""
        result = optimize_well_order(self.plate, ["B2", "A2", "B1"])

        self.assertEqual(result, ["B2", "A2", "B1"])

    def test_does_not_modify_input_and_retains_duplicates(self) -> None:
        """Preserve the input and keep duplicate labels as separate visits."""
        wells = ["A1", "C3", "A1"]

        result = optimize_well_order(self.plate, wells)

        self.assertEqual(wells, ["A1", "C3", "A1"])
        self.assertEqual(result, ["A1", "A1", "C3"])

    def test_returns_new_list_for_short_inputs(self) -> None:
        """Return independent lists for single-well and empty worklists."""
        wells = ["A1"]

        result = optimize_well_order(self.plate, wells)

        self.assertEqual(result, wells)
        self.assertIsNot(result, wells)
        self.assertEqual(optimize_well_order(self.plate, []), [])

    def test_rejects_invalid_well(self) -> None:
        """Reject invalid labels in a multi-well worklist."""
        with self.assertRaises(ValueError):
            optimize_well_order(self.plate, ["A1", "Z99"])


if __name__ == "__main__":
    unittest.main()
