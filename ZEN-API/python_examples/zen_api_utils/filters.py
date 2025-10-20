# -*- coding: utf-8 -*-

#################################################################
# File        : filters.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from typing import List

from zen_api.lm.hardware.v2 import (
    FilterWheelServiceGetFiltersResponse,
    FilterData,
    ReflectorChangerServiceGetReflectorsResponse,
    ReflectorData,
)


def get_filter_by_position(filters: FilterWheelServiceGetFiltersResponse, position: int) -> FilterData | None:
    """
    Return the filter that matches the given position from the filters list.
    Args:
        filters (FilterWheelServiceGetFiltersResponse):
            An object containing a list of filters.
        position (int):
            The position of the filter to retrieve.
    Returns:
        FilterData | None:
            The filter at the specified position if found, otherwise None.
    """
    for filter in filters.filters:
        if filter.position == position:
            return filter
    return None


def get_used_filterwheel_positions(filters: FilterWheelServiceGetFiltersResponse) -> List[int]:
    """
    Generates a list of used filter positions from a collection of filter data.
    Args:
        filters (FilterWheelServiceGetFiltersResponse):
            An object containing a list of filters with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the filters.
    """

    used_positions: List[int] = []

    for filter in filters.filters:
        used_positions.append(filter.position)

    return used_positions


def get_reflector_by_position(
    reflectors: ReflectorChangerServiceGetReflectorsResponse, position: int
) -> ReflectorData | None:
    """
    Return the reflector that matches the given position from the reflectors list.
    Args:
        reflectors (ReflectorChangerServiceGetReflectorsResponse):
            An object containing a list of reflectors.
        position (int):
            The position of the reflector to retrieve.
    Returns:
        ReflectorData | None:
            The reflector at the specified position if found, otherwise None.
    """
    for reflector in reflectors.reflectors:
        if reflector.position == position:
            return reflector
    return None


def get_used_reflector_positions(reflectors: ReflectorChangerServiceGetReflectorsResponse) -> List[int]:
    """
    Generates a list of used reflector positions from a collection of reflector data.
    Args:
        reflectors (ReflectorChangerServiceGetReflectorsResponse):
            An object containing a list of reflectors with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the reflectors.
    """

    used_positions: List[int] = []

    for reflector in reflectors.reflectors:
        used_positions.append(reflector.position)

    return used_positions
