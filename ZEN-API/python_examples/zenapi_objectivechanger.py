# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_objectivechanger.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
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

from zen_api_utils.objective import (
    get_used_objective_positions,
    get_objective_by_position,
    get_used_optovar_positions,
    get_optovar_by_position,
)

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    ObjectiveChangerServiceStub,
    ObjectiveChangerServiceGetPositionRequest,
    ObjectiveChangerServiceMoveToRequest,
    ObjectiveChangerServiceGetObjectivesRequest,
    OptovarServiceStub,
    OptovarServiceGetPositionRequest,
    OptovarServiceMoveToRequest,
    OptovarServiceGetOptovarsRequest,
)

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get services
    objchanger_service = ObjectiveChangerServiceStub(channel=channel, metadata=metadata)
    optovar_service = OptovarServiceStub(channel=channel, metadata=metadata)

    objectives = await objchanger_service.get_objectives(ObjectiveChangerServiceGetObjectivesRequest())
    optovars = await optovar_service.get_optovars(OptovarServiceGetOptovarsRequest())

    logger.info("-------- Available objectives and Optovars  ----------------------------")

    # check used positions
    used_obj_positions = get_used_objective_positions(objectives)
    used_opt_positions = get_used_optovar_positions(optovars)
    logger.info(f"Used objective positions: {used_obj_positions}")
    logger.info(f"Used optovar positions: {used_opt_positions}")

    for obj in objectives.objectives:
        logger.info(f"Objective: {obj.name} - Position: {obj.position}")

    for opt in optovars.optovars:
        logger.info(f"Optovar: {opt.name} - Position: {opt.position}")

    logger.info("------------------ Move Objectives -----------------------")

    # get the current objective position and name
    pos_obj = await objchanger_service.get_position(ObjectiveChangerServiceGetPositionRequest())
    current_objective = get_objective_by_position(objectives, pos_obj.value)
    logger.info(f"Current Objective: {current_objective.name} Position: {current_objective.position}")
    obj_initial_position = current_objective.position

    # move to a new objective position
    obj_new_position = 3
    out = await objchanger_service.move_to(ObjectiveChangerServiceMoveToRequest(position_index=obj_new_position))
    current_objective = get_objective_by_position(objectives, obj_new_position)
    logger.info(f"Current Objective: {current_objective.name} Position: {current_objective.position}")

    # move back to initial objective position
    out = await objchanger_service.move_to(ObjectiveChangerServiceMoveToRequest(position_index=obj_initial_position))
    current_objective = get_objective_by_position(objectives, obj_initial_position)
    logger.info(f"Current Objective: {current_objective.name} Position: {current_objective.position}")

    logger.info("------------------ Move Optovars -----------------------")

    # get the current optovar position and name
    pos_optovar = await optovar_service.get_position(OptovarServiceGetPositionRequest())
    current_optovar = get_optovar_by_position(optovars, pos_optovar.value)
    logger.info(f"Current Optovar: {current_optovar.name} Position: {current_optovar.position}")
    optovar_initial_position = current_optovar.position

    # move to a new optovar position
    opt_new_position = 1
    out = await optovar_service.move_to(OptovarServiceMoveToRequest(position_index=opt_new_position))
    current_optovar = get_optovar_by_position(optovars, opt_new_position)
    logger.info(f"Current Optovar: {current_optovar.name} Position: {current_optovar.position}")

    # move back to initial optovar position
    out = await optovar_service.move_to(OptovarServiceMoveToRequest(position_index=optovar_initial_position))
    current_optovar = get_optovar_by_position(optovars, optovar_initial_position)
    logger.info(f"Current Optovar: {current_optovar.name} Position: {current_optovar.position}")

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
