# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_stage_unified.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# Description : Demonstrates stage movement using advanced stage APIs
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
import numpy as np
from pathlib import Path
import sys
from zen_api_utils.misc import set_logging, initialize_zenapi

# Import custom stage helper functions
from zen_api_utils.stage import (
    AxisPositions,
)

# Import auto-generated ZEN API modules for stage control
from zen_api.hardware.v1 import (
    StageServiceMoveToRequest,
    StageAxis,
    StageServiceGetStagePositionRequest,
    StageServiceStub,
    AxisIdentifier,
)

# Configuration file path for ZEN API connection
# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"


async def main(args):
    """
    Main function demonstrating stage movement operations.
    Shows usage of unified stage APIs for position control.
    """

    # Establish gRPC connection to ZEN API
    channel, metadata = initialize_zenapi(config_path)

    # Create stage service stub for basic operations
    stage_service = StageServiceStub(channel=channel, metadata=metadata)

    position_response = await stage_service.get_stage_position(StageServiceGetStagePositionRequest())
    pos = AxisPositions(position_response)
    xpos_orig = pos.X
    ypos_orig = pos.Y

    logger.info(f"Stage XY Position: {np.round(pos.X * 1e6, 2)} - {np.round(pos.Y * 1e6, 2)} [micron]")

    # Define new target position in meters (converted from microns)
    new_posx = 13000 * 1e-6  # 13000 microns = 0.013 meters
    new_posy = 8700 * 1e-6  # 8700 microns = 0.0087 meters

    logger.info("Moving to new XY positions ...")
    await stage_service.move_to(
        StageServiceMoveToRequest(
            [
                StageAxis(AxisIdentifier.X, new_posx),
                StageAxis(AxisIdentifier.Y, new_posy),
            ]
        )
    )

    # check if position are the same as before
    position_response = await stage_service.get_stage_position(StageServiceGetStagePositionRequest())
    pos = AxisPositions(position_response)

    logger.info(f"New Stage XY Position: {np.round(pos.X * 1e6, 2)} - {np.round(pos.Y * 1e6, 2)} [micron]")

    # Move back to origin
    logger.info("Moving to original XY positions ...")
    await stage_service.move_to(
        StageServiceMoveToRequest(
            [
                StageAxis(AxisIdentifier.X, xpos_orig),
                StageAxis(AxisIdentifier.Y, ypos_orig),
            ]
        )
    )

    # check if position are the same as before
    position_response = await stage_service.get_stage_position(StageServiceGetStagePositionRequest())
    pos = AxisPositions(position_response)

    logger.info(f"Final Stage XY Position: {np.round(pos.X * 1e6, 2)} - {np.round(pos.Y * 1e6, 2)} [micron]")

    # Clean up gRPC connection
    channel.close()


if __name__ == "__main__":
    # Initialize logging for the application
    logger = set_logging()

    # Run the main asynchronous function with command line arguments
    asyncio.run(main(sys.argv))
