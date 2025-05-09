# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_stage_LM.py
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
import numpy as np
import sys
from zenapi_tools import set_logging, initialize_zenapi

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    StageServiceStub,
    StageServiceGetPositionRequest,
    StageServiceMoveToRequest,
)

configfile = r"config.ini"


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(configfile)

    # get stage service
    stage_service = StageServiceStub(channel=channel, metadata=metadata)

    # get the stage positions in [m]
    posXY = await stage_service.get_position(StageServiceGetPositionRequest())
    logger.info(
        f"Stage XY Position 1: {np.round(posXY.x * 1e6, 2)} - {np.round(posXY.y * 1e6, 2)} [micron]"
    )

    # move to new position in [m]
    new_posx = 13000 * 1e-6
    new_posy = 8700 * 1e-6

    await stage_service.move_to(StageServiceMoveToRequest(x=new_posx, y=new_posy))
    new_posXY = await stage_service.get_position(StageServiceGetPositionRequest())
    logger.info(
        f"Stage XY Position 2: {np.round(new_posXY.x * 1e6, 2)} - {np.round(new_posXY.y * 1e6, 2)} [micron]"
    )

    # move back to initial position
    await stage_service.move_to(StageServiceMoveToRequest(x=posXY.x, y=posXY.y))
    posXY = await stage_service.get_position(StageServiceGetPositionRequest())
    logger.info(
        f"Stage XY Position 1: {np.round(posXY.x * 1e6, 2)} - {np.round(posXY.y * 1e6, 2)} [micron]"
    )

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
