# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_swaf.py
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
from zenapi_experiment_tools import show_swaf_info_LM, save_experiment
from grpclib import GRPCError

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceCloneRequest,
)

from zen_api.lm.acquisition.v1beta import (
    ExperimentSwAutofocusServiceStub,
    ExperimentSwAutofocusServiceGetAutofocusParametersRequest,
    ExperimentSwAutofocusServiceSetAutofocusParametersRequest,
    ExperimentSwAutofocusServiceFindAutoFocusRequest,
    AutofocusMode,
    AutofocusContrastMeasure,
    AutofocusSampling,
)

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    # StageServiceStub,
    StageServiceGetPositionRequest,
    # StageServiceMoveToRequest,
    FocusServiceStub,
    # FocusServiceGetPositionRequest,
)

configfile = r"config.ini"
expname = "ZEN_API_SWAF"
expname_cloned = "ZEN_API_SWAF_cloned"
image_folder = Path(r"f:\Zen_Output\temp")
exp_folder = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(configfile)

    # create the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # get SWAF_service
    swaf_service = ExperimentSwAutofocusServiceStub(channel=channel, metadata=metadata)

    # get stage service
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(
        ExperimentServiceLoadRequest(experiment_name=expname)
    )

    # get the information about the SWAF parameters
    swaf_info = await swaf_service.get_autofocus_parameters(
        ExperimentSwAutofocusServiceGetAutofocusParametersRequest(
            experiment_id=my_exp.experiment_id
        )
    )

    # show the SWAF parameters
    show_swaf_info_LM(swaf_info)

    # clone the experiment
    logger.info("Cloning Experiment ...")
    my_exp_cloned = await exp_service.clone(
        ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id)
    )

    # modify the SWAF
    await swaf_service.set_autofocus_parameters(
        ExperimentSwAutofocusServiceSetAutofocusParametersRequest(
            experiment_id=my_exp_cloned.experiment_id,
            autofocus_mode=AutofocusMode.CONTRAST,
            contrast_measure=AutofocusContrastMeasure.LOW_SIGNAL,
            search_strategy="Full",
            autofocus_sampling=AutofocusSampling.MEDIUM,
            # offset=0.5 * 1e-6,  # in [m]
            use_acquisition_roi=True,  # Full frame will be used and not the Focus Region
            reference_channel_name="EGFP",
            # relative_range_is_automatic=False, # if false it is still "relative" but one needs tp provide a search range
            relative_search_range=123 * 1e-6,  # --> cannot be used when range is auto
            # lower_limit=-50 * 1e-6,  # --> cannot be used when range is auto
            # upper_limit=50 * 1e-6,  # --> cannot be used when range is auto
        )
    )

    # save the modified experiment to disk as an *.czexp file
    await save_experiment(
        my_exp_cloned, exp_service, expname=expname_cloned, overwrite=True
    )

    # get the information about the SWAF parameters
    swaf_info = await swaf_service.get_autofocus_parameters(
        ExperimentSwAutofocusServiceGetAutofocusParametersRequest(
            experiment_id=my_exp_cloned.experiment_id
        )
    )

    # show the SWAF parameters
    show_swaf_info_LM(swaf_info)

    # get Z-Position
    posZ_before = await focus_service.get_position(StageServiceGetPositionRequest())
    logger.info(f"Z-Drive Position before SWAF [micron]: {posZ_before.value*1e6:.3f}")

    # run modified SWAF
    try:
        swaf_response = await swaf_service.find_auto_focus(
            ExperimentSwAutofocusServiceFindAutoFocusRequest(
                experiment_id=my_exp_cloned.experiment_id, timeout=12  # in [s]
            )
        )
        logger.info(f"Z-Drive Position after SWAF: {swaf_response.focus_position:.3f}")

    except GRPCError as e:
        logger.error(e.message)
        logger.info(f"Z-Drive Position after SWAF error: {posZ_before.value*1e6:.3f}")

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
