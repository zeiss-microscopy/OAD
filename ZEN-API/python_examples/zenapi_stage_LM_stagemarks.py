#################################################################
# File        : zenapi_stage_LM_stagemarks.py
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

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    FocusServiceGetPositionRequest,
    FocusServiceMoveToRequest,
    FocusServiceStub,
)
from zen_api_utils.misc import initialize_zenapi, set_logging
from zen_api_utils.stage import PosXYZ, move_xyz, parse_stage_marks

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"
stagemarks_path = script_dir / "StageMarks_Brainslide_CD7.czstm"
use_simple = False


async def main(args):
    del args
    # Initialize the gRPC channel and metadata using the configuration file
    channel, metadata = initialize_zenapi(config_path)

    # Create instances of stage and focus services
    stage_service = SimpleStageServiceStub(channel=channel, metadata=metadata)
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)

    # Parse the stage marks file to retrieve a list of StageMark objects
    logger.info(f"Parsing StageMarks from file: {str(stagemarks_path)}")
    stage_marks = parse_stage_marks(stagemarks_path)

    # Iterate through each StageMark object and move to the specified positions
    for mark in stage_marks:
        logger.info(
            f"Moving to StageMark: {mark.index}, X: {round(mark.x * 1e6, 1)}, Y: {round(mark.y * 1e6, 1)}, Z: {round(mark.z * 1e6, 1)} [micron]"
        )
        # Move the stage to the specified X and Y coordinates
        await stage_service.move_to(SimpleStageServiceMoveToRequest(x=mark.x, y=mark.y))
        # Move the focus to the specified Z position
        await focus_service.move_to(FocusServiceMoveToRequest(value=mark.z))

        # just for demonstration purposes - wait a bit
        time.sleep(1.0)

        # Retrieve the current stage positions and convert to microns
        posXY = await stage_service.get_position(SimpleStageServiceGetPositionRequest())
        posZ = await focus_service.get_position(FocusServiceGetPositionRequest())
        if posZ.value is None:
            raise RuntimeError("Focus service returned no position")
        logger.info(
            f"New XYZ Position {mark.index}: X: {np.round(posXY.x * 1e6, 1)} - Y: {np.round(posXY.y * 1e6, 1)} - Z: {np.round(posZ.value * 1e6, 1)} [micron]"
        )

    # or try the simplified version
    if use_simple:
        logger.info("Now using the simplified move_xyz method")
        for mark in stage_marks:
            pos_xyz = PosXYZ(x_meter=mark.x, y_meter=mark.y, z_meter=mark.z)
            assert pos_xyz.z_micron is not None
            logger.info(
                f"Moving to StageMark: {mark.index}, X: {round(pos_xyz.x_micron, 1)}, Y: {round(pos_xyz.y_micron, 1)}, Z: {round(pos_xyz.z_micron, 1)} [micron]"
            )
            # use a single method
            pos_xyz = await move_xyz(channel, metadata, pos_xyz)
            assert pos_xyz.z_micron is not None
            logger.info(
                f"New XYZ Position {mark.index}: X: {np.round(pos_xyz.x_micron, 1)} - Y: {np.round(pos_xyz.y_micron, 1)} - Z: {np.round(pos_xyz.z_micron, 1)} [micron]"
            )

            # just for demonstration purposes - wait a bit
            time.sleep(1.0)

    # Close the gRPC channel to release resources
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
