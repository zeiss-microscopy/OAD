#################################################################
# File        : zenapi_sample_carrier_CD7.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Remark: This works right now only for CellDiscoverer 7 !!!
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
from grpclib.exceptions import GRPCError
from zen_api_utils.misc import set_logging, initialize_zenapi
from zen_api_utils.sample_carrier import WellPlate

from zen_api.lm.hardware.v1 import (
    SampleCarrierServiceStub,
    SampleCarrierServiceMoveToContainerRequest,
    SampleCarrierServiceGetInfoRequest,
    SampleCarrierServiceGetCurrentContainerRequest,
)

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
# config_path = script_dir / "config.ini"
config_path = script_dir / "my_config.ini"
expname = "ZEN_API_Test_w96_1024x1024_CH=2"


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get the sample carrier service
    sample_carrier_service = SampleCarrierServiceStub(channel=channel, metadata=metadata)

    try:
        sample_carrier_info = await sample_carrier_service.get_info(SampleCarrierServiceGetInfoRequest())

        logger.info(f"Sample Carrier Name: {sample_carrier_info.name}")
        logger.info(f"Sample Carrier Rows: {sample_carrier_info.rows}")
        logger.info(f"Sample Carrier Columns: {sample_carrier_info.columns}")
        logger.info(f"Sample Carrier Material: {sample_carrier_info.material}")
        logger.info(f"Sample Carrier Thickness: {sample_carrier_info.thickness}")
        logger.info(f"Sample Carrier Skirt: {sample_carrier_info.skirt}")
        logger.info(f"Sample Carrier Refractive Index: {sample_carrier_info.refractive_index}")

        # define use sample carrier
        plate = WellPlate(sample_carrier_info.rows, sample_carrier_info.columns)

        # get current position and convert to wellID
        current_position = await sample_carrier_service.get_current_container(
            SampleCarrierServiceGetCurrentContainerRequest()
        )
        current_well = plate.index_to_well(current_position.row_index, current_position.column_index)
        logger.info(
            f"Current position: {current_well} - Row: {current_position.row_index} Column: {current_position.column_index}"
        )

        # move to wells
        wells = [
            (0, 0),  # A1
            (0, 11),  # A12
            (7, 11),  # H12
            (7, 0),  # H1
            (3, 5),  # D6
        ]

        for well in wells:
            logger.info(f"Moving to well row, col: {well}")
            await sample_carrier_service.move_to_container(SampleCarrierServiceMoveToContainerRequest(well[0], well[1]))
            time.sleep(1)  # wait a bit between moves

        # use ID to move

        for well in ("A2", "A7", "H11", "H9", "D6"):
            logger.info(f"Moving to {well} --> row, col: {plate.well_to_index(well)}")
            await sample_carrier_service.move_to_container(
                SampleCarrierServiceMoveToContainerRequest(*plate.well_to_index(well))
            )
            time.sleep(1)  # wait a bit between moves

        # close the channel
        channel.close()

    except GRPCError as e:
        logger.error(f"gRPC error occurred: {e}")
        # close the channel
        channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
