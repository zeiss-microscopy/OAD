# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_tracks.py
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
from zen_api_utils.misc import set_logging, initialize_zenapi
from zen_api_utils.experiment import show_track_info_LM

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceCloneRequest,
    ExperimentServiceSaveRequest,
)

from zen_api.lm.acquisition.v1beta import (
    TrackServiceGetTrackInfoRequest,
    TrackServiceActivateTrackRequest,
    TrackServiceDeactivateTrackRequest,
    TrackServiceActivateChannelRequest,
    TrackServiceDeactivateChannelRequest,
    TrackServiceStub,
)

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"

expname = "ZEN_API_Tracks_LSM"
expname_cloned = "ZEN_API_Tracks_LSM_cloned"
image_folder = Path(r"f:\Zen_Output\temp")
exp_folder = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # create the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # get track service
    track_service = TrackServiceStub(channel=channel, metadata=metadata)

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(
        ExperimentServiceLoadRequest(experiment_name=expname)
    )

    # get the information about the track parameters
    track_info = await track_service.get_track_info(
        TrackServiceGetTrackInfoRequest(experiment_id=my_exp.experiment_id)
    )

    # show the track parameters
    tracks = show_track_info_LM(track_info)

    # clone the experiment
    logger.info("Cloning Experiment ...")
    my_exp_cloned = await exp_service.clone(
        ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id)
    )

    await track_service.deactivate_track(
        TrackServiceDeactivateTrackRequest(
            experiment_id=my_exp_cloned.experiment_id, track_index=1
        )
    )

    await track_service.deactivate_track(
        TrackServiceDeactivateTrackRequest(
            experiment_id=my_exp_cloned.experiment_id, track_index=2
        )
    )

    await track_service.deactivate_channel(
        TrackServiceDeactivateChannelRequest(
            experiment_id=my_exp_cloned.experiment_id, track_index=2, channel_index=0
        )
    )

    # check if such an experiment already exists and delete it
    if Path(exp_folder / (expname_cloned + ".czexp")).exists():
        Path(exp_folder / (expname_cloned + ".czexp")).unlink()
        logger.info("Overwrite experiment:" + expname_cloned + ".czexp")

    # save the cloned experiment using a defined name without the *.czexp extension
    logger.info("Saving Experiment ...")
    await exp_service.save(
        ExperimentServiceSaveRequest(
            experiment_id=my_exp_cloned.experiment_id, experiment_name=expname_cloned
        )
    )

    # get the information about the tracks
    track_info = await track_service.get_track_info(
        TrackServiceGetTrackInfoRequest(experiment_id=my_exp_cloned.experiment_id)
    )

    # show the track parameters
    tracks = show_track_info_LM(track_info)

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
