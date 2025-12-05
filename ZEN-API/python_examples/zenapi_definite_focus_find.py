# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_definite_focus_find.py
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

from zen_api_utils.misc import set_logging, initialize_zenapi

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    FocusServiceGetPositionRequest,
    FocusServiceMoveToRequest,
    FocusServiceStub,
)

from zen_api.lm.acquisition.v1 import (
    DefiniteFocusServiceStub,
    DefiniteFocusServiceFindSurfaceRequest,
    DefiniteFocusServiceStoreFocusRequest,
    DefiniteFocusServiceRecallFocusRequest,
)

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get the stage and definite focus service
    definite_focus_service = DefiniteFocusServiceStub(channel=channel, metadata=metadata)
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)

    # move z-drive
    await focus_service.move_to(FocusServiceMoveToRequest(value=-300 * 1e-6))
    zpos = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"Initial Z-Position (ZDrive): {zpos.value * 1e6:.3f} [micron]")

    # find the surface --> z-position is returned in [microns]
    zpos_find_surface = await definite_focus_service.find_surface(DefiniteFocusServiceFindSurfaceRequest())
    logger.info(f"Z-Position (FindSurface): {zpos_find_surface.zposition * 1e6:.3f} [micron]")

    zpos = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"Z-Position (ZDrive) after FS: {zpos.value * 1e6:.3f} [micron]")

    # store the z-value
    await definite_focus_service.store_focus(DefiniteFocusServiceStoreFocusRequest())
    logger.info(f"Focus Position {zpos.value * 1e6:.3f} [micron] stored.")

    # move z-drive by ... [microns]
    await focus_service.move_to(FocusServiceMoveToRequest(value=zpos.value + 500 * 1e-6))
    new_posZ = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"New Z-Drive: {new_posZ.value * 1e6:.3f} [micron]")

    # use recall focus to return
    zpos_recall = await definite_focus_service.recall_focus(DefiniteFocusServiceRecallFocusRequest())
    logger.info(f"Z-Position (RecallFocus): {zpos_recall.zposition * 1e6:.3f} [micron]")

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
