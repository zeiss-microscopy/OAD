# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_definite_focus_stabilize.py
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
import time

from grpclib import GRPCError

from zen_api_utils.misc import set_logging, initialize_zenapi

# import the auto-generated python modules
from zen_api.lm.acquisition.v1 import (
    DefiniteFocusServiceStub,
    DefiniteFocusServiceLockFocusRequest,
    DefiniteFocusServiceUnlockFocusRequest,
)

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


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get the definite focus service
    definite_focus_service = DefiniteFocusServiceStub(channel=channel, metadata=metadata)
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)

    # move z-drive
    await focus_service.move_to(FocusServiceMoveToRequest(value=0.0))
    zpos = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"Initial Z-position (ZDrive): {zpos.value * 1e6:.3f} [micron]")

    try:

        # lock the focus - timeout in [s]
        await definite_focus_service.lock_focus(DefiniteFocusServiceLockFocusRequest(timeout=5))
        logger.info("Focus locked.")

        time.sleep(3)  # just wait a few seconds

        # unlock the focus
        await definite_focus_service.unlock_focus(DefiniteFocusServiceUnlockFocusRequest())
        logger.info("Focus unlocked.")

    except GRPCError as e:
        logger.error(f"Error occurred: {e}")

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
