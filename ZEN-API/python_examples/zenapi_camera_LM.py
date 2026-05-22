# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_camera_LM.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
from pathlib import Path
import sys
from dataclasses import asdict
from pprint import pprint
from zen_api_utils.misc import set_logging, initialize_zenapi
from zen_api_utils.cameras import get_camera_info_LM, get_cameras_info_LM

# Import auto-generated ZEN API modules for stage control
from zen_api.lm.hardware.v2 import (
    CameraServiceStub,  # Camera service interface
)

# Configuration file path for ZEN API connection
# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"


async def main(args):

    # Establish gRPC connection to ZEN API
    channel, metadata = initialize_zenapi(config_path)

    # Create simple stage service stub for basic operations
    camera_service = CameraServiceStub(channel=channel, metadata=metadata)

    # get the information for all cameras
    cameras_info = await get_cameras_info_LM(camera_service)

    for camera in cameras_info:
        pprint(camera)

    # get the information for a single camera (the first one in the list)
    single_camera_info = await get_camera_info_LM(camera_service, camera_id=cameras_info[0].id)
    pprint(asdict(single_camera_info))

    # Clean up gRPC connection
    channel.close()


if __name__ == "__main__":
    # Initialize logging for the application
    logger = set_logging()

    # Run the main asynchronous function with command line arguments
    asyncio.run(main(sys.argv))
