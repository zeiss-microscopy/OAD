# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_positions.py
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
from zenapi_experiment_tools import save_experiment, delete_czifile

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceCloneRequest,
)

from zen_api.lm.acquisition.v1beta import (
    TilesServiceStub,
    TilesServiceIsTilesExperimentRequest,
    TilesServiceClearRequest,
    TilesServiceAddPositionsRequest,
    Position3D,
)

configfile = r"config.ini"
expname = "ZEN_API_Positions"
expname_cloned = "ZEN_API_Positions_cloned"
image_folder = Path(r"f:\Zen_Output\temp")
exp_folder = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")


poslist = [
    [37980, 11780, 0],
    [38480, 12380, 100],
    [38980, 12880, 200],
]

pos_new = []

for p in poslist:
    pos3d = Position3D(p[0] * 1e-6, p[1] * 1e-6, p[2] * 1e-6)
    pos_new.append(pos3d)


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(configfile)

    # create the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # get TileService
    tile_service = TilesServiceStub(channel=channel, metadata=metadata)

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(
        ExperimentServiceLoadRequest(experiment_name=expname)
    )

    # check if the experiment has tiles or positions
    has_tiles_or_positions = await tile_service.is_tiles_experiment(
        TilesServiceIsTilesExperimentRequest(experiment_id=my_exp.experiment_id)
    )

    logger.info(
        f"ExperimentName: {expname} has Tiles or Positions: {has_tiles_or_positions.is_tiles_experiment}"
    )

    if has_tiles_or_positions.is_tiles_experiment:

        # clone the experiment
        logger.info("Cloning Experiment ...")
        my_exp_cloned = await exp_service.clone(
            ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id)
        )

        # clear existing tile region
        logger.info("Clearing TileRegions or Positions...")
        await tile_service.clear(
            TilesServiceClearRequest(experiment_id=my_exp_cloned.experiment_id)
        )

        # adding a list with positions
        for pos in pos_new:
            logger.info(
                f"Adding Position X: {pos.x*1e6:.3f} Y: {pos.y*1e6:.3f} Z: {pos.z*1e6:.3f}"
            )

        await tile_service.add_positions(
            TilesServiceAddPositionsRequest(
                experiment_id=my_exp_cloned.experiment_id, positions=pos_new
            )
        )

        # save the modified experiment to disk as an *.czexp file
        await save_experiment(
            my_exp_cloned,
            exp_service,
            expname=expname_cloned,
            overwrite=True,
        )

    else:
        logger.info(f"ExperimentName: {expname} - Tiles Dimension is not activated")

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
