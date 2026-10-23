#################################################################
# File        : zenapi_stage_LM.py
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
import sys
import time
from pathlib import Path

import numpy as np

# import the auto-generated python modules
from zen_api.hardware.v1 import (
    SimpleStageServiceGetPositionRequest,
    SimpleStageServiceMoveToRequest,
    SimpleStageServiceStub,
)
from zen_api_utils.misc import initialize_zenapi, set_logging

# Import custom stage helper functions
from zen_api_utils.stage import StageXYPosition, get_stageXY_position_simple, move_to_stageXY_position_simple

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"


async def main(args):
    del args

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get stage service
    simple_stage_service = SimpleStageServiceStub(channel=channel, metadata=metadata)

    # get the stage positions in [m]
    posXY = await simple_stage_service.get_position(SimpleStageServiceGetPositionRequest())
    logger.info(f"Stage XY Position 1: {np.round(posXY.x * 1e6, 2)} - {np.round(posXY.y * 1e6, 2)} [micron]")

    # move to new position in [m]
    new_posx = 4500 * 1e-6
    new_posy = 8500 * 1e-6

    await simple_stage_service.move_to(SimpleStageServiceMoveToRequest(x=new_posx, y=new_posy))
    new_posXY = await simple_stage_service.get_position(SimpleStageServiceGetPositionRequest())
    logger.info(f"Stage XY Position 2: {np.round(new_posXY.x * 1e6, 2)} - {np.round(new_posXY.y * 1e6, 2)} [micron]")

    # wait for a while
    logger.info("Waiting for 3 seconds...")
    time.sleep(3)

    # move to new position in [m]
    new_posx = 103500 * 1e-6
    new_posy = 71500 * 1e-6
    await move_to_stageXY_position_simple(simple_stage_service, stage_positionXY=StageXYPosition(new_posx, new_posy))
    new_posXY = await get_stageXY_position_simple(simple_stage_service)
    logger.info(f"Stage XY Position 2: {np.round(new_posXY.x * 1e6, 2)} - {np.round(new_posXY.y * 1e6, 2)} [micron]")

    # wait for a while
    logger.info("Waiting for 3 seconds...")
    time.sleep(3)

    # move back to initial position
    await simple_stage_service.move_to(SimpleStageServiceMoveToRequest(x=posXY.x, y=posXY.y))
    posXY = await simple_stage_service.get_position(SimpleStageServiceGetPositionRequest())
    logger.info(f"Stage XY Position 1: {np.round(posXY.x * 1e6, 2)} - {np.round(posXY.y * 1e6, 2)} [micron]")

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
