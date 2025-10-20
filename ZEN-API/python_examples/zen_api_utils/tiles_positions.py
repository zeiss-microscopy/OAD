# -*- coding: utf-8 -*-

#################################################################
# File        : tiles_positions.py
# Author      : SRh, JSm
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################
from typing import List

from dataclasses import dataclass, field
from zen_api.common.v1 import DoublePoint


@dataclass
class TileRegionRectangle:
    """
    Represents a rectangular tile region.
    All units are in [m].
    """

    id: int = field(init=False, default=None)
    center_x: float = field(init=False, default=None)
    center_y: float = field(init=False, default=None)
    width: float = field(init=False, default=None)
    height: float = field(init=False, default=None)
    zvalue: float = field(init=False, default=None)


@dataclass
class TileRegionPolygon:
    """
    Represents a polygon tile region.
    All units are in [m].
    """

    id: int = field(init=False, default=None)
    polygon: List[DoublePoint] = field(init=False, default=None)
    zvalue: float = field(init=False, default=None)


@dataclass
class TileRegionEllipse:
    """
    Represents an ellipse tile region.
    All units are in [m].
    """

    id: int = field(init=False, default=None)
    center_x: float = field(init=False, default=None)
    center_y: float = field(init=False, default=None)
    x_diameter: float = field(init=False, default=None)  # diameter in x-direction
    y_diameter: float = field(init=False, default=None)  # diameter in y-direction
    zvalue: float = field(init=False, default=None)
