# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_experiment_methods.py
# Author      : SRh, JSm
# Institution : Carl Zeiss Microscopy GmbH
#
# The script demos the usage of the ZEN-API for Experiments. In order to
# run it the file path and names need to be adapted for usage with ZEN blue or ZEN core
# and the one needs create the experiments and have a working MTB configuration
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
from pylibCZIrw import czi as pyczi
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from typing import Dict, Union
from pathlib import Path
import time
from zen_api_utils.misc import set_logging, initialize_zenapi

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceGetAvailableExperimentsRequest,
    ExperimentServiceCloneRequest,
    ExperimentServiceSaveRequest,
    ExperimentServiceExportRequest,
    ExperimentServiceImportRequest,
    ExperimentServiceDeleteRequest,
    ExperimentServiceRunSnapRequest,
    ExperimentServiceStartLiveRequest,
    ExperimentServiceStopRequest,
    ExperimentServiceStartContinuousRequest,
    ExperimentServiceRunExperimentRequest,
    ExperimentServiceGetStatusRequest,
)


# define some global variables
# exp_folder = Path(r"f:\Documents\Carl Zeiss\ZENCore\Documents\Experiment Setups")
exp_folder = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")
my_experiment = "ZEN_API_Test_w96_1024x1024_CH=2"
exp_cloned_name = "ZEN_API_Test_w96_1024x1024_CH=2_cloned"
# image_folder = Path(r"f:\AppData_TEMP\Temp\Zeiss\ZENCore\SavingPath\temp")
image_folder = Path(r"f:\Zen_Output\temp")
czi_name = "zenapi_myimage"
waittime = 3
open_czi = True

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"

# this is the main test script
async def check_experiment_api(experiment_name: str, configfile: str = "config.ini") -> Dict[str, Union[str, Path]]:
    """
    Tries to run all available experiments methods for ZEN-API.

    Args:
        experiment_name (str): Name of the experiment to be loaded.
        configfile (str): define the ZEN API configuration

    Returns:
        A dictionary with results containing the location of the snap image
        and the experiment result.

    Raises:
        None
    """
    results = {}

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(configfile)

    # get the experiment service
    logger.info("Create gRPC Channel and ExperimentService ...")
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # show output path for images
    save_path = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    logger.info("Saving Location for CZI Images:" + save_path.image_output_path)

    # get available experiments from the ZEN core default folder
    # Example Location: "...\Documents\Carl Zeiss\ZENCore\Documents\Experiment Setups"
    available_experiments = await exp_service.get_available_experiments(
        ExperimentServiceGetAvailableExperimentsRequest()
    )
    logger.info(f"Number of available Experiment File(s) inside ZEN folder: {len(available_experiments.experiments)}")

    # for exp in available_experiments.experiments:
    #    logger.info(exp.name + ".czexp")

    # load the desired experiment and return its reference id
    logger.info("Loading Experiment ...")

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=experiment_name))
    logger.info("ExperimentName:" + my_experiment + " Reference Id: " + my_exp.experiment_id)

    # clone the experiment
    logger.info("Cloning Experiment ...")
    my_exp_cloned = await exp_service.clone(ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id))

    # check if such an experiment already exists and delete it
    if Path(exp_folder / (exp_cloned_name + ".czexp")).exists():
        Path(exp_folder / (exp_cloned_name + ".czexp")).unlink()
        logger.info("Overwrite experiment:" + exp_cloned_name + ".czexp")

    # save the clones experiment using a defined name without the *.czexp extension
    logger.info("Saving Experiment ...")
    await exp_service.save(
        ExperimentServiceSaveRequest(experiment_id=my_exp_cloned.experiment_id, experiment_name=exp_cloned_name)
    )

    # export the experiment as XML string
    logger.info("Exporting Experiment as XML String ...")
    exp_xml = await exp_service.export(
        ExperimentServiceExportRequest(
            experiment_id=my_exp_cloned.experiment_id,
        )
    )

    # print some parts of the XML string
    print(exp_xml.xml[:300])

    # import an experiment from XML string
    logger.info("Importing Experiment from XML String ...")
    imported_exp = await exp_service.import_(ExperimentServiceImportRequest(exp_xml.xml))
    logger.info("Reference Id (imported): " + imported_exp.experiment_id)

    # delete the clones experiment
    logger.info("Delete cloned Experiment ...")
    await exp_service.delete(ExperimentServiceDeleteRequest(experiment_name=exp_cloned_name))

    # check if the experiment is really gone
    if not Path(exp_folder / (exp_cloned_name + ".czexp")).exists():
        logger.info("Deleted experiment:" + exp_cloned_name + ".czexp")

    # acquire a snap image and show its location
    logger.info("Start SNAP Experiment ...")

    # wait until snap is finished
    snap = await exp_service.run_snap(ExperimentServiceRunSnapRequest(experiment_id=my_exp.experiment_id))

    results["snap_path"] = Path(save_path.image_output_path) / (snap.output_name + ".czi")
    logger.info("Saving Location: " + str(results["snap_path"]))

    # start and stop live based on the selected experiment
    logger.info("Starting Live ...")
    await exp_service.start_live(ExperimentServiceStartLiveRequest(experiment_id=my_exp.experiment_id, track_index=0))

    logger.info("Stopping Live ...")
    await exp_service.stop(ExperimentServiceStopRequest(experiment_id=my_exp.experiment_id))
    # time.sleep(waittime)  # this should not be needed soon !!!

    # start and stop Continuous based on selected experiment
    logger.info("Starting Continuous ...")
    await exp_service.start_continuous(ExperimentServiceStartContinuousRequest(experiment_id=my_exp.experiment_id))

    logger.info("Stopping Continuous ...")
    await exp_service.stop(ExperimentServiceStopRequest(experiment_id=my_exp.experiment_id))
    time.sleep(waittime)  # this should not be needed soon !!!

    # check if such an experiment already exists and delete it
    if Path(image_folder / (czi_name + ".czi")).exists():
        Path(image_folder / (czi_name + ".czi")).unlink()
        logger.info("Overwrite CZI file: " + czi_name + ".czi")

    # execute experiment
    logger.info("Starting Experiment Execution ...")

    exp_result = await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(experiment_id=my_exp.experiment_id, output_name=czi_name)
    )

    exp_status = await exp_service.get_status(ExperimentServiceGetStatusRequest(experiment_id=my_exp.experiment_id))

    logger.info(exp_status)

    results["exp_result_path"] = Path(save_path.image_output_path) / (exp_result.output_name + ".czi")
    logger.info("Saving Location Experiment Run: " + str(results["exp_result_path"]))

    # close the channel
    channel.close()

    return results


if __name__ == "__main__":
    # get the logger
    logger = set_logging()

    # run the main function to check zen api methods
    results = asyncio.run(check_experiment_api(experiment_name=my_experiment, configfile=config_path))

    logger.info(results)

    if open_czi:

        with pyczi.open_czi(str(results["exp_result_path"])) as czidoc:

            # read a 2d image plane
            t = 0
            c = 0
            s = 0
            z = 0

            # read the actual pixel data
            img2d = czidoc.read(plane={"C": c, "T": t, "Z": z}, scene=s)
            logger.info(f"Shape of 2D plane: {img2d.shape}")

            # get the total size of all existing dimension for this CZI image
            total_bounding_box = czidoc.total_bounding_box
            logger.info(f"Total BBox: {total_bounding_box}")

        # show the 2D image plane
        logger.info("Displaying CZI image data ...")
        fig1, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.imshow(img2d[..., 0], cmap=cm.inferno, vmin=100, vmax=5000)
        ax.set_title(f"{results['exp_result_path']}: S={s} T={t} C={c} Z={z}")
        plt.show()
