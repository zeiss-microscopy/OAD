# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_changers.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# This script demonstrates how to interact with microscope hardware changers like
# objective changer, optovar, reflector changer, and filter wheel using the ZEN API.
# If the system does not have any of those components, the respective part of the code
# should be commented out.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
from pathlib import Path
import sys

# from typing import List
from zen_api_utils.misc import set_logging, initialize_zenapi

from zen_api_utils.changers import (
    get_objective_by_position,
    get_optovar_by_position,
    get_filter_by_position,
    get_reflector_by_position,
    move_changers_adv,
)

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    ObjectiveChangerServiceStub,
    ObjectiveChangerServiceGetPositionRequest,
    ObjectiveChangerServiceGetObjectivesRequest,
    ReflectorChangerServiceStub,
    ReflectorChangerServiceGetReflectorsRequest,
    ReflectorChangerServiceGetPositionRequest,
    FilterWheelServiceStub,
    FilterWheelServiceGetPositionRequest,
    FilterWheelServiceGetFiltersRequest,
    OptovarServiceStub,
    OptovarServiceGetPositionRequest,
    OptovarServiceGetOptovarsRequest,
)

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
# config_path = script_dir / "config.ini"
config_path = script_dir / "my_config.ini"


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get services
    objchanger_service = ObjectiveChangerServiceStub(channel=channel, metadata=metadata)
    optovar_service = OptovarServiceStub(channel=channel, metadata=metadata)
    reflector_service = ReflectorChangerServiceStub(channel=channel, metadata=metadata)
    filterwheel_service = FilterWheelServiceStub(channel=channel, metadata=metadata)

    # get available objectives, optovars, reflectors, and filters
    objectives = await objchanger_service.get_objectives(ObjectiveChangerServiceGetObjectivesRequest())
    optovars = await optovar_service.get_optovars(OptovarServiceGetOptovarsRequest())
    reflectors = await reflector_service.get_reflectors(ReflectorChangerServiceGetReflectorsRequest())
    filters = await filterwheel_service.get_filters(FilterWheelServiceGetFiltersRequest())

    logger.info("--------------------- Available changers -----------------------------")

    # Log individual changer details
    changers_data = [
        ("Objective", objectives.objectives),
        ("Optovar", optovars.optovars),
        ("Reflector", reflectors.reflectors),
        ("Filter", filters.filters),
    ]

    for changer_name, changer_list in changers_data:
        for item in changer_list:
            logger.info(f"{changer_name}: {item.name} - Position: {item.position}")

    logger.info("------------------ Current Changer Positions -----------------------")

    # get the current changers positions
    obj_initial_position = await objchanger_service.get_position(ObjectiveChangerServiceGetPositionRequest())
    optovar_initial_position = await optovar_service.get_position(OptovarServiceGetPositionRequest())
    reflector_initial_position = await reflector_service.get_position(ReflectorChangerServiceGetPositionRequest())
    filter_initial_position = await filterwheel_service.get_position(FilterWheelServiceGetPositionRequest())

    # get current positions
    current_objective = get_objective_by_position(objectives, obj_initial_position.value)
    current_optovar = get_optovar_by_position(optovars, optovar_initial_position.value)
    current_reflector = get_reflector_by_position(reflectors, reflector_initial_position.value)
    current_filter = get_filter_by_position(filters, filter_initial_position.value)

    if current_objective is not None:
        logger.info(f"Current Objective: {current_objective.name} Position: {current_objective.position}")
    else:
        logger.info(f"Current Objective Position: {obj_initial_position.value} - No matching objective found")

    if current_optovar is not None:
        logger.info(f"Current Optovar: {current_optovar.name} Position: {current_optovar.position}")
    else:
        logger.info(f"Current Optovar Position: {optovar_initial_position.value} - No matching optovar found")

    if current_reflector is not None:
        logger.info(f"Current Reflector: {current_reflector.name} Position: {current_reflector.position}")
    else:
        logger.info(f"Current Reflector Position: {reflector_initial_position.value} - No matching reflector found")

    if current_filter is not None:
        logger.info(f"Current Filter: {current_filter.name} Position: {current_filter.position}")
    else:
        logger.info(f"Current Filter Position: {filter_initial_position.value} - No matching filter found")

    logger.info("------------------ Move all changers -----------------------")

    results = await move_changers_adv(
        objchanger_service=objchanger_service,
        optovar_service=optovar_service,
        reflector_service=reflector_service,
        filterwheel_service=filterwheel_service,
        objective_position=3,
        optovar_position=1,
        reflector_position=2,
        filterwheel_position=3,
    )

    logger.info(f"Moved: {[k for k, v in results.items() if v and v.get('status') == 'success']}")
    logger.info(f"Skipped: {results['skipped']}")
    logger.info(f"Warnings: {len(results['warnings'])}")

    logger.info("--------------- Move all changers back to initial positions --------------------")

    # move back to initial positions
    results = await move_changers_adv(
        objchanger_service=objchanger_service,
        optovar_service=optovar_service,
        reflector_service=reflector_service,
        filterwheel_service=filterwheel_service,
        objective_position=obj_initial_position.value,
        optovar_position=optovar_initial_position.value,
        reflector_position=reflector_initial_position.value,
        filterwheel_position=filter_initial_position.value,
    )

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
