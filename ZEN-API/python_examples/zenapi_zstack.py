# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_zstack.py
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
import numpy as np
from pathlib import Path
from zenapi_tools import set_logging, initialize_zenapi
from zenapi_experiment_tools import show_zstack_info_LM, save_experiment, delete_czifile

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceCloneRequest,
    ExperimentServiceRunExperimentRequest,
)

from zen_api.lm.acquisition.v1beta import (
    ZStackServiceStub,
    ZStackServiceGetZStackInfoRequest,
    ZStackServiceModifyZStackCenterRangeRequest,
    ZStackServiceModifyZStackFirstLastRequest,
)

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    FocusServiceGetPositionRequest,
    FocusServiceMoveToRequest,
    FocusServiceStub,
)


configfile = r"config.ini"
expname = "ZEN_API_ZStack"
expname_mod1 = "ZEN_API_ZStack_mod1"
expname_mod2 = "ZEN_API_ZStack_mod2"
czi_name_orig = "zstack_orig"
czi_name_mod1 = "zstack_mod1"
czi_name_mod2 = "zstack_mod2"
image_folder = Path(r"f:\Zen_Output\temp")
exp_folder = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(configfile)

    # create the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # get stage service
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)

    # get zstack_service
    zstack_service = ZStackServiceStub(channel=channel, metadata=metadata)

    # move z-drive to zero
    await focus_service.move_to(FocusServiceMoveToRequest(value=0.0))
    new_posZ = await focus_service.get_position(FocusServiceGetPositionRequest())
    logger.info(f"Initial Z-Drive: {np.round(new_posZ.value, 2)} [micron]")

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(
        ExperimentServiceLoadRequest(experiment_name=expname)
    )

    # get the information about the stack
    zstack_info1 = await zstack_service.get_z_stack_info(
        ZStackServiceGetZStackInfoRequest(experiment_id=my_exp.experiment_id)
    )

    show_zstack_info_LM(zstack_info1)

    # execute experiment
    logger.info(f"Experiment Execution: {expname}")

    delete_czifile(image_folder, czi_name_orig)

    await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(
            experiment_id=my_exp.experiment_id, output_name=czi_name_orig
        )
    )

    # clone the original experiment
    logger.info("Cloning Experiment ...")
    my_exp_mod1 = await exp_service.clone(
        ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id)
    )

    # modify the z-stack center and range
    await zstack_service.modify_z_stack_center_range(
        ZStackServiceModifyZStackCenterRangeRequest(
            experiment_id=my_exp_mod1.experiment_id,
            center=123 * 1e-6,
            interval=5 * 1e-6,
            range=100 * 1e-6,
        )
    )

    # get the information about the mdoified stack
    zstack_info2 = await zstack_service.get_z_stack_info(
        ZStackServiceGetZStackInfoRequest(experiment_id=my_exp_mod1.experiment_id)
    )

    # show z-stack info
    show_zstack_info_LM(zstack_info2)

    # delete already existing CZI files with same name
    delete_czifile(image_folder, czi_name_mod1)

    # run the modified experiment
    logger.info(f"Experiment Execution: {expname_mod1}")
    await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(
            experiment_id=my_exp_mod1.experiment_id, output_name=czi_name_mod1
        )
    )

    # save the modified experiment to disk as an *.czexp file
    await save_experiment(
        my_exp_mod1, exp_service, expname=expname_mod1, overwrite=True
    )

    # modify the experiment again
    await zstack_service.modify_z_stack_first_last(
        ZStackServiceModifyZStackFirstLastRequest(
            experiment_id=my_exp_mod1.experiment_id,
            first=10 * 1e-6,
            last=50 * 1e-6,
            interval=2 * 1e-6,
        )
    )

    zstack_info3 = await zstack_service.get_z_stack_info(
        ZStackServiceGetZStackInfoRequest(experiment_id=my_exp_mod1.experiment_id)
    )

    show_zstack_info_LM(zstack_info3)
    delete_czifile(image_folder, czi_name_mod2)

    # execute experiment
    logger.info(f"Experiment Execution: {expname_mod2}")
    await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(
            experiment_id=my_exp_mod1.experiment_id, output_name=czi_name_mod2
        )
    )

    await save_experiment(
        my_exp_mod1, exp_service, expname=expname_mod2, overwrite=True
    )

    # close the channel
    channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main(sys.argv))
