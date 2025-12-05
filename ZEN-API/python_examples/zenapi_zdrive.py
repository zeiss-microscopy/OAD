# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_zdrive.py
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
import sys
import time
from pathlib import Path

from zen_api_utils.misc import set_logging, initialize_zenapi

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    FocusServiceGetPositionRequest,
    FocusServiceMoveToRequest,
    FocusServiceStub,
)

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"

delta_z = 500 * 1e-6  # move Z-drive by this value in micron


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get Z-stage service
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)

    # find the surface at the current position
    initial_zpos = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"Initial Z-position:  {initial_zpos.value * 1e6:.3f}  [micron]")

    # wait a few seconds
    time.sleep(1)

    # move z-drive
    await focus_service.move_to(FocusServiceMoveToRequest(value=initial_zpos.value + delta_z))
    new_posZ = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"New Z-Position: {new_posZ.value * 1e6:.3f} [micron]")

    # wait a few seconds
    time.sleep(1)

    # move z-drive
    await focus_service.move_to(FocusServiceMoveToRequest(value=new_posZ.value - delta_z))
    new_posZ = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"Return to initial Z-Position: {new_posZ.value * 1e6:.3f} [micron]")

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
