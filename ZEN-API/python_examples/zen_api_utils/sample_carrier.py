#################################################################
# File        : sample_carrier.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from __future__ import annotations
import re
from typing import Final, Tuple
from dataclasses import dataclass

"""
This module defines the `WellPlate` class, which represents an immutable description of a rectangular sample carrier (plate).
It provides functionality to validate plate layouts, convert between well labels and indices, and perform other operations
related to well plates.
Classes:
    - WellPlate: Represents a rectangular sample carrier with a specific number of rows and columns.
Constants:
    - _ASCII_A: ASCII value of the letter 'A', used for converting rows to letters.
    - _WELL_RE: Regular expression for parsing well labels (e.g., 'A1', 'B3').
    - _ALLOWED_LAYOUTS: Set of allowed plate layouts (rows, columns) for validation.
Methods:
    - __post_init__: Validates the plate layout during initialization.
    - index_to_well: Converts 0-based (row, col) indices to well labels (e.g., 'B3').
    - well_to_index: Converts well labels to 0-based (row, col) indices.
    - __repr__: Returns a string representation of the plate (e.g., 'WellPlate(32×48)').
    - __len__: Returns the total number of wells in the plate.
    - __contains__: Checks if a well label is valid for the plate.
    - _check_index: Validates that a given (row, col) index is within the plate's bounds.
    - _row_to_letters: Converts a 0-based row index to Excel-style letters (e.g., 0 → 'A', 25 → 'Z').
    - _letters_to_row: Converts Excel-style letters to a 0-based row index (e.g., 'A' → 0, 'Z' → 25).
Usage:
    The `WellPlate` class can be used to represent and manipulate well plates of various sizes.
    It ensures that only valid plate layouts are allowed and provides methods for converting between
    well labels and indices.
Example:
    print(plate.well_to_index("A1"))  # Output: (0, 0)
    print(plate.index_to_well(7, 11))  # Output: 'H12'
"""


__all__ = ["WellPlate"]

_ASCII_A: Final = ord("A")
_WELL_RE: Final = re.compile(r"^\s*([A-Z]+)(\d+)\s*$", re.I)

# Canonical plate layouts  (rows , cols)  — smaller dimension first
_ALLOWED_LAYOUTS: Final[set[Tuple[int, int]]] = {
    (1, 1),  # microscope slide / single well / petri dish
    (1, 2),  # strip of 2
    (1, 3),  # strip of 3
    (1, 4),  # strip of 4
    (2, 3),  #   6-well plate
    (2, 5),  #  10-well plate
    (2, 6),  #  12-well plate
    (3, 4),  #  12-well plate
    (4, 6),  #  24-well plate
    (6, 8),  #  48-well plate
    (8, 12),  #  96-well plate
    (16, 24),  # 384-well plate
    (32, 48),  # 1536-well plate
}


@dataclass(slots=True, frozen=True)
class WellPlate:
    """Immutable description of a rectangular sample carrier (plate)."""

    rows: int
    cols: int

    # ------------------------------------------------------------- init/validate
    def __post_init__(self) -> None:
        shape = (min(self.rows, self.cols), max(self.rows, self.cols))
        if shape not in _ALLOWED_LAYOUTS:
            allowed = ", ".join(f"{r}×{c}" for r, c in sorted(_ALLOWED_LAYOUTS))
            raise ValueError(f"unsupported plate layout: {self.rows}×{self.cols}. " f"Allowed layouts: {allowed}")

    # ------------------------------------------------------------------  public
    def index_to_well(self, row: int, col: int) -> str:
        """
        Convert a 0-based (row, col) index into a well label.

        Args:
            row (int): The 0-based row index.
            col (int): The 0-based column index.

        Returns:
            str: The well label in the format of a letter (row) followed by a number (column),
                 e.g., 'B3' for row 1 and column 2.

        Raises:
            ValueError: If the provided row or column index is out of bounds.
        """

        self._check_index(row, col)
        return self._row_to_letters(row) + str(col + 1)

    def well_to_index(self, well: str) -> Tuple[int, int]:
        """
        Converts a well identifier (e.g., "A1", "B12") into a tuple of zero-based row and column indices.
        Args:
            well (str): The well identifier to convert. It should be in the format of letters followed by digits
                        (e.g., "A1", "B12"). The letters represent the row, and the digits represent the column.
        Returns:
            Tuple[int, int]: A tuple containing the zero-based row index and column index.
        Raises:
            ValueError: If the provided well identifier is invalid or does not match the expected format.
        """
        match = _WELL_RE.fullmatch(well)
        if not match:
            raise ValueError(f"invalid well id: {well!r}")

        letters, digits = match.groups()
        row = self._letters_to_row(letters)
        col = int(digits) - 1
        self._check_index(row, col)

        return row, col

    def __repr__(self) -> str:
        """
        Provide a string representation of the object.

        Returns:
            str: A string in the format "<ClassName>(<rows>×<cols>)",
                 where <ClassName> is the name of the class, and <rows>
                 and <cols> are the respective attributes of the object.
        """
        return f"{self.__class__.__name__}({self.rows}×{self.cols})"

    def __len__(self) -> int:  # total number of wells
        """
        Returns the total number of wells.

        This method calculates the total number of wells by multiplying
        the number of rows (`self.rows`) by the number of columns (`self.cols`).

        Returns:
            int: The total number of wells.
        """
        return self.rows * self.cols

    def __contains__(self, item: str) -> bool:  # quick membership test
        """
        Check if the given item is a member of the collection.

        This method allows the use of the `in` keyword to test for membership.

        Args:
            item (str): The item to check for membership.

        Returns:
            bool: True if the item is a member of the collection, False otherwise.

        Raises:
            ValueError: If the item is not found during the membership test.
        """
        try:
            self.well_to_index(item)
            return True
        except ValueError:
            return False

    # -----------------------------------------------------------  internals

    def _check_index(self, row: int, col: int) -> None:
        """
        Validates whether the given row and column indices are within the valid range.

        Args:
            row (int): The row index to check.
            col (int): The column index to check.

        Raises:
            ValueError: If the row or column index is out of the valid range.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError(
                f"index out of range: row={row}, col={col} " f"(valid rows 0-{self.rows-1}, cols 0-{self.cols-1})"
            )

    @staticmethod
    def _row_to_letters(row: int) -> str:
        """
        Converts a zero-based row index into its corresponding Excel-style column letters.

        Args:
            row (int): The zero-based row index to convert.

        Returns:
            str: The Excel-style column letters corresponding to the given row index.

        Example:
            _row_to_letters(0) -> 'A'
            _row_to_letters(25) -> 'Z'
            _row_to_letters(26) -> 'AA'
            _row_to_letters(701) -> 'ZZ'
        """
        letters: list[str] = []
        n = row + 1
        while n:
            n, rem = divmod(n - 1, 26)
            letters.append(chr(_ASCII_A + rem))
        return "".join(reversed(letters))

    @staticmethod
    def _letters_to_row(letters: str) -> int:
        """
        Converts a string of letters (e.g., Excel-style column letters) to a zero-based row index.

        Args:
            letters (str): The string of letters to convert. Typically represents column letters
                        in a spreadsheet (e.g., "A", "B", ..., "Z", "AA", "AB", etc.).

        Returns:
            int: The zero-based row index corresponding to the input letters.

        Example:
            _letters_to_row("A") -> 0
            _letters_to_row("Z") -> 25
            _letters_to_row("AA") -> 26
            _letters_to_row("AB") -> 27
        """
        value = 0
        for ch in letters.upper():
            value = value * 26 + (ord(ch) - _ASCII_A + 1)
        return value - 1


# demo code
if __name__ == "__main__":
    plate = WellPlate(32, 48)  # 1536-well plate
    for test in ("A1", "AF48", "B3"):
        print(f"{test} -> {plate.well_to_index(test)}")

    r, c = 7, 11
    print(f"({r}, {c}) -> {plate.index_to_well(r, c)}")
