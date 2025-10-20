# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_experiment_status.py
# Author      : SRh, JSm
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
from pylibCZIrw import czi as pyczi
from matplotlib import pyplot as plt
import matplotlib.cm as cm

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceRegisterOnStatusChangedRequest,
    ExperimentServiceStartExperimentRequest,
)


czi_name = "test_czi"
# exp_folder = Path(r"f:\Documents\Carl Zeiss\ZENCore\Documents\Experiment Setups")
exp_folder = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")
my_experiment = "ZEN_API_Test_w96_1024x1024_CH=2"
# image_folder = Path(r"f:\AppData_TEMP\Temp\Zeiss\ZENCore\SavingPath\temp")
image_folder = Path(r"f:\Zen_Output\temp")
overwrite = True
open_czi = True

# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"

async def main(args):
    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # create the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=my_experiment))
    logger.info(f"ExperimentName: {my_experiment} Reference Id: {my_exp.experiment_id}")

    # show output path for images
    save_path = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    logger.info(f"Saving Location for CZI Images: {save_path.image_output_path}")

    if overwrite:
        # check if such an image already exists and delete it
        if Path(Path(save_path.image_output_path) / (czi_name + ".czi")).exists():
            if overwrite:
                Path(Path(save_path.image_output_path) / (czi_name + ".czi")).unlink()
                logger.info("Overwrite CZI file: " + czi_name + ".czi")
            elif not overwrite:
                logger.error("CZI file: " + czi_name + ".czi cannot be overwritten")
                channel.close()
                raise FileExistsError("CZI file: " + czi_name + ".czi cannot be overwritten")

    # start the actual experiment
    exp_result = await exp_service.start_experiment(
        ExperimentServiceStartExperimentRequest(experiment_id=my_exp.experiment_id, output_name=czi_name)
    )

    # define api method for the "observable"
    api_method = exp_service.register_on_status_changed(
        ExperimentServiceRegisterOnStatusChangedRequest(my_exp.experiment_id)
    )

    try:
        while True:
            # stream is closed after 30 seconds of inactivity
            response = await asyncio.wait_for(api_method.__anext__(), timeout=30)

            # stop observing if the experiment has stopped
            if not response.status.is_experiment_running:
                break

            logger.info(
                f"Exp. running: {response.status.is_experiment_running} "
                + f"Acq. running: {response.status.is_acquisition_running} "
                + f"Scenes Index: {response.status.scenes_index} "
                + f"Tiles Index: {response.status.tiles_index} "
                + f"Time Index: {response.status.time_points_index} "
                + f"Channel Index: {response.status.channels_index} "
                + f"ZPlane Index: {response.status.zstack_slices_index} "
                + f"Images Acq-Index: {response.status.images_acquired_index}"
            )

    except Exception as exc:
        logger.error("Stopped observing status: " + type(exc).__name__)

    # close the channel
    channel.close()

    if open_czi:
        czi_fullpath = str(Path(save_path.image_output_path) / (exp_result.output_name + ".czi"))

        with pyczi.open_czi(czi_fullpath) as czidoc:

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
        ax.set_title(f"{czi_fullpath}: S={s} T={t} C={c} Z={z}")
        plt.show()


if __name__ == "__main__":
    # create logger
    logger = set_logging()

    if not Path.exists(exp_folder / (my_experiment + ".czexp")):
        logger.warning(f"Selected experiment {my_experiment} does not exist")
    else:
        # run the main function
        asyncio.run(main(sys.argv))
