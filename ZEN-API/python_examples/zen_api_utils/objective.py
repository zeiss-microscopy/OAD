# -*- coding: utf-8 -*-

#################################################################
# File        : objective.py
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

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    ObjectiveData,
    ObjectiveChangerServiceGetObjectivesResponse,
    OptovarData,
    OptovarServiceGetOptovarsResponse,
)


def get_objective_by_position(
    objectives: ObjectiveChangerServiceGetObjectivesResponse, position: int
) -> ObjectiveData | None:
    """
    Return the objective that matches the given position from the objectives list.
    Args:
        objectives (ObjectiveChangerServiceGetObjectivesResponse):
            An object containing a list of objectives.
        position (int):
            The position of the objective to retrieve.
    Returns:
        ObjectiveData | None:
            The objective at the specified position if found, otherwise None.
    """
    for obj in objectives.objectives:
        if obj.position == position:
            return obj
    return None


def get_optovar_by_position(optovars: OptovarServiceGetOptovarsResponse, position: int) -> OptovarData | None:
    """
    Return the optovar that matches the given position from the objectives list.
    Args:
        objectives (OptovarServiceGetOptovarsResponse):
            An object containing a list of optovars.
        position (int):
            The position of the optovar to retrieve.
    Returns:
        OptovarData | None:
            The optovar at the specified position if found, otherwise None.
    """
    for opt in optovars.optovars:
        if opt.position == position:
            return opt
    return None


def get_used_objective_positions(objectives: ObjectiveChangerServiceGetObjectivesResponse) -> List[int]:
    """
    Generates a list of used objective positions from a collection of objective data.
    Args:
        objectives (ObjectiveChangerServiceGetObjectivesResponse):
            An object containing a list of objectives with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the objectives.
    """

    used_positions: List[int] = []

    for obj in objectives.objectives:
        used_positions.append(obj.position)

    return used_positions


def get_used_optovar_positions(optovars: OptovarServiceGetOptovarsResponse) -> List[int]:
    """
    Generates a list of used optovar positions from a collection of optovar data.
    Args:
        objectives (OptovarServiceGetOptovarsResponse):
            An object containing a list of optovars with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the optovars.
    """

    used_positions: List[int] = []

    for opt in optovars.optovars:
        used_positions.append(opt.position)

    return used_positions
