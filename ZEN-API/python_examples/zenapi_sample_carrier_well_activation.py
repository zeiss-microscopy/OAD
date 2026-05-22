#################################################################
# File        : zenapi_sample__well_activation.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
import sys
from pathlib import Path  # Correct import for file system paths
from grpclib.exceptions import GRPCError
from zen_api_utils.misc import set_logging, initialize_zenapi
from zen_api_utils.experiment import delete_czifile
from zen_api_utils.sample_carrier import WellPlate
import zen_api_utils.zen_tcpip_commands as zen_tcpip_commands
from zen_api_utils.zen_tcpip import ZenCommands

from zen_api.lm.hardware.v1 import (
    SampleCarrierServiceGetConfiguredContainersRequest,
    SampleCarrierServiceGetInfoRequest,
    SampleCarrierServiceStub,
    SampleCarrierServiceActivateContainerRequest,
    SampleCarrierServiceDeactivateContainersRequest,
)

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceCloneRequest,
    ExperimentServiceSaveRequest,
    ExperimentServiceDeleteRequest,
    ExperimentServiceRunExperimentRequest,
)

from zen_api_utils.experiment import get_configured_containernames

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
# config_path = script_dir / "config.ini"
config_path = script_dir / "my_config.ini"
expname = "ZEN_API_Well_Activation"  # has active container B4, B5, C4, C5 with 4 positions each well
exp_cloned_name = "ZEN_API_Well_Activation_Cloned"
czi_name = "zenapi_well_activation"
output_folder = r"f:\Zen_Output\temp"
overwrite = True


async def main(args):

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # get the sample carrier and experiment service
    sample_carrier_service = SampleCarrierServiceStub(channel=channel, metadata=metadata)
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)
    sample_carrier_info = await sample_carrier_service.get_info(SampleCarrierServiceGetInfoRequest())
    plate = WellPlate(sample_carrier_info.rows, sample_carrier_info.columns)

    # show output path for images
    save_path = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    logger.info("Saving Location for CZI Images:" + save_path.image_output_path)

    try:

        # load experiment by its name without the *.czexp extension
        exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=expname))
        logger.info(f"ExperimentName: {expname} Reference Id: {exp.experiment_id}")

        # clone the experiment
        try:
            await exp_service.delete(ExperimentServiceDeleteRequest(experiment_name=exp_cloned_name))
        except Exception as e:
            logger.warning(f"Could not delete cloned experiment: {e}. Maybe it does not exist.")

        logger.info("Cloning Experiment ...")
        exp_cloned = await exp_service.clone(ExperimentServiceCloneRequest(experiment_id=exp.experiment_id))
        logger.info(f"Cloned ExperimentName: {expname} Reference Id: {exp_cloned.experiment_id}")

        # get "configured" containers
        configured_containers = await sample_carrier_service.get_configured_containers(
            SampleCarrierServiceGetConfiguredContainersRequest(experiment_id=exp_cloned.experiment_id)
        )
        for container in configured_containers.configured_containers:
            logger.info(f"Configured Container: {container.container_name}, is_activated {container.is_activated}")

        # get the names of all configured containers as a list of strings
        configured_containers_ids = await get_configured_containernames(
            sample_carrier_service=sample_carrier_service, experiment_id=exp_cloned.experiment_id
        )
        logger.info(f"Configured Containers: {configured_containers_ids}")

        try:
            # deactivate all configured wells
            await sample_carrier_service.deactivate_containers(
                SampleCarrierServiceDeactivateContainersRequest(
                    experiment_id=exp_cloned.experiment_id, container_names=configured_containers_ids
                )
            )
        except Exception as e:
            logger.error(f"Error deactivating all configure containers: {e}")

        # get "configured" containers
        configured_containers = await sample_carrier_service.get_configured_containers(
            SampleCarrierServiceGetConfiguredContainersRequest(experiment_id=exp_cloned.experiment_id)
        )
        for container in configured_containers.configured_containers:
            logger.info(f"Configured Container: {container.container_name}, is_activated {container.is_activated}")

        try:
            # do some modifications of the experiment
            await sample_carrier_service.activate_container(
                SampleCarrierServiceActivateContainerRequest(
                    experiment_id=exp_cloned.experiment_id,
                    container_name=configured_containers.configured_containers[0].container_name,
                )
            )
            logger.info(f"Activated Container: {configured_containers.configured_containers[0].container_name}")
        except Exception as e:
            logger.error(
                f"Error activating container {configured_containers.configured_containers[0].container_name}: {e}"
            )

        # save the cloned experiment using a defined name without the *.czexp extension
        logger.info("Saving Cloned Experiment ...")
        await exp_service.save(
            ExperimentServiceSaveRequest(experiment_id=exp_cloned.experiment_id, experiment_name=exp_cloned_name)
        )

        # execute experiment
        logger.info("Starting Experiment Execution ...")
        exp_result = await exp_service.run_experiment(
            ExperimentServiceRunExperimentRequest(experiment_id=exp_cloned.experiment_id, output_name=czi_name)
        )

        # get the location of the CZI file that was saved to disk
        save_path = Path(save_path.image_output_path) / (exp_result.output_name + ".czi")
        logger.info("Saving Location Experiment Run: " + str(save_path))

        # close the channel
        channel.close()

        # open the image in ZEN (for demo purposes) using TCP-IP
        commandlist = zen_tcpip_commands.add_image(str(save_path))
        my_commands = ZenCommands(commandlist)
        my_commands.execute()

    except GRPCError as e:

        logger.error(f"gRPC error occurred: {e}")
        # close the channel
        channel.close()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    # delete existing czi file
    if overwrite:
        delete_czifile(image_folder=output_folder, cziname=czi_name)

    # run the main function
    asyncio.run(main(sys.argv))
