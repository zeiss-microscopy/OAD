#################################################################
# File        : tiles_positions.py
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################
from dataclasses import dataclass, field

from zen_api.common.v1 import DoublePoint


@dataclass
class TileRegionRectangle:
    """
    Represents a rectangular tile region.
    All units are in [m].
    """

    id: int | None = field(init=False, default=None)
    center_x: float | None = field(init=False, default=None)
    center_y: float | None = field(init=False, default=None)
    width: float | None = field(init=False, default=None)
    height: float | None = field(init=False, default=None)
    zvalue: float | None = field(init=False, default=None)


@dataclass
class TileRegionPolygon:
    """
    Represents a polygon tile region.
    All units are in [m].
    """

    id: int | None = field(init=False, default=None)
    polygon: list[DoublePoint] | None = field(init=False, default=None)
    zvalue: float | None = field(init=False, default=None)


@dataclass
class TileRegionEllipse:
    """
    Represents an ellipse tile region.
    All units are in [m].
    """

    id: int | None = field(init=False, default=None)
    center_x: float | None = field(init=False, default=None)
    center_y: float | None = field(init=False, default=None)
    x_diameter: float | None = field(init=False, default=None)  # diameter in x-direction
    y_diameter: float | None = field(init=False, default=None)  # diameter in y-direction
    zvalue: float | None = field(init=False, default=None)
