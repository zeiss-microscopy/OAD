# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_tileregion.py
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
from pathlib import Path
from zenapi_tools import set_logging, initialize_zenapi

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceCloneRequest,
    ExperimentServiceSaveRequest,
)

from zen_api.lm.acquisition.v1beta import (
    TilesServiceStub,
    TilesServiceIsTilesExperimentRequest,
    TilesServiceAddRectangleTileRegionRequest,
    TilesServiceClearRequest,
)

exp_folder = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")
my_experiments = ["ZEN_API_TileRegion_Test"]  # , "ZEN_API_TileRegion_Test_notiles"]
configfile = r"config.ini"


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(configfile)

    # create the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # get TileService
    tile_service = TilesServiceStub(channel=channel, metadata=metadata)

    for expname in my_experiments:

        # load experiment by its name without the *.czexp extension
        my_exp = await exp_service.load(
            ExperimentServiceLoadRequest(experiment_name=expname)
        )

        # do something with the TileRegions
        has_tiles = await tile_service.is_tiles_experiment(
            TilesServiceIsTilesExperimentRequest(experiment_id=my_exp.experiment_id)
        )

        logger.info(
            f"ExperimentName: {expname} Reference Id: {my_exp.experiment_id} has TileRegions: {has_tiles.is_tiles_experiment}"
        )

        if has_tiles.is_tiles_experiment:

            expname_cloned = expname + "_clone"

            my_exp_cloned = await exp_service.clone(
                ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id)
            )

            # clear existing tile region
            logger.info("Clearing TileRegions ...")
            await tile_service.clear(
                TilesServiceClearRequest(experiment_id=my_exp_cloned.experiment_id)
            )

            # add a tile region to the experiment (experiment needs to have a tileRegion already)
            await tile_service.add_rectangle_tile_region(
                TilesServiceAddRectangleTileRegionRequest(
                    experiment_id=my_exp_cloned.experiment_id,
                    center_x=4500 * 1e-6,
                    center_y=8500 * 1e-6,
                    width=2000 * 1e-6,
                    height=1000 * 1e-6,
                    z=-7000 * 1e-6,
                )
            )

            # save the clones experiment using a defined name without the *.czexp extension
            logger.info(f"Saving cloned Experiment: {expname_cloned}")
            await exp_service.save(
                ExperimentServiceSaveRequest(
                    experiment_id=my_exp_cloned.experiment_id,
                    experiment_name=expname_cloned,
                    allow_override=True,
                )
            )

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
