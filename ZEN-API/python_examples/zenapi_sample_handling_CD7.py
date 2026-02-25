#################################################################
# File        : zenapi_handling_CD7.py
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
from zen_api_utils.misc import set_logging, initialize_zenapi

from zen_api.lm.live_scan.v1 import (
    LiveScanServiceEjectTrayRequest,
    LiveScanServiceGetConfigurationRequest,
    LiveScanServiceLoadTrayAndPrescanRequest,
    LiveScanServiceSetConfigurationRequest,
    LiveScanServiceStub,
)

import time

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script - please adapt the path to your config.ini if necessary
# config_path = script_dir / "config.ini"
config_path = script_dir / "my_config.ini"
eject = True

carrier_template = "Multichamber 96.czsht"  # Sample holder template for the carrier
# carrier_template = "Insert - 2x Slide - Long.czsht"  # Sample holder template for the carrier


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get the sample carrier service
    lsc_service = LiveScanServiceStub(channel=channel, metadata=metadata)

    lsc = await lsc_service.get_configuration(LiveScanServiceGetConfigurationRequest())

    logger.info(f"LiveScanConfig - Sample Holder Template: {lsc.config.sample_holder_template}")
    logger.info(f"LiveScanConfig - Bottom Material: {lsc.config.material}")
    logger.info(f"LiveScanConfig - Refractive Index: {lsc.config.refractive_index}")
    logger.info(f"LiveScanConfig - Measure Bottom Thickness: {lsc.config.measure_bottom_thickness}")
    logger.info(f"LiveScanConfig - Determine Bottom Material: {lsc.config.determine_bottom_material}")
    logger.info(f"LiveScanConfig - Automatic Carrier Detection: {lsc.config.live_scan_detection}")
    logger.info(f"LiveScanConfig - Create Carrier Overview: {lsc.config.create_carrier_overview}")
    logger.info(f"LiveScanConfig - Read Barcodes: {lsc.config.read_barcodes}")
    logger.info(f"LiveScanConfig - Use Left Barcode: {lsc.config.use_left_barcode}")
    logger.info(f"LiveScanConfig - Use Right Barcode: {lsc.config.use_right_barcode}")
    logger.info(f"LiveScanConfig - Automatic Carrier Calibration: {lsc.config.automatic_live_scan_calibration}")

    # modify parameters for the sample loading process
    lsc.config.sample_holder_template = carrier_template
    lsc.config.refractive_index = 1.234
    lsc.config.create_carrier_overview = False
    await lsc_service.set_configuration(LiveScanServiceSetConfigurationRequest(config=lsc.config))
    logger.info(f"LiveScanConfig - Refractive Index: {lsc.config.refractive_index}")

    # load the sample carrier
    logger.info("Loading sample carrier...")
    # returns object with error messages, warnings and result messages
    result_messages = await lsc_service.load_tray_and_prescan(LiveScanServiceLoadTrayAndPrescanRequest())

    # check if list of notifications is empty
    if result_messages.notifications:
        for notification in result_messages.notifications:
            logger.warning(f"Notification: {notification}")
    else:
        logger.info("No Loading & PreScan notifications.")

    logger.info("Sample carrier loaded and prescan completed.")

    time.sleep(3)  # wait a bit before ejecting the tray

    if eject:
        await lsc_service.eject_tray(LiveScanServiceEjectTrayRequest())
        logger.info("Sample carrier ejected.")
        channel.close()
        return

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
