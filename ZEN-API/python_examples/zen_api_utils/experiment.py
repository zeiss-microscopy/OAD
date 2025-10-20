# -*- coding: utf-8 -*-

#################################################################
# File        : experiment.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


from zen_api.lm.acquisition.v1beta import (
    ZStackServiceGetZStackInfoResponse,
    TrackServiceGetTrackInfoResponse,
    ExperimentSwAutofocusServiceGetAutofocusParametersResponse,
    TrackInfo
)

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceLoadRequest,
    ExperimentServiceRunExperimentRequest,
    ExperimentServiceStub,
    ExperimentServiceLoadResponse,
    ExperimentServiceSaveRequest,
)

from dataclasses import dataclass
from typing import List
from zen_api_utils.misc import set_logging
from pathlib import Path

logger = set_logging()


@dataclass
class Tracks:
    info: List[TrackInfo]
    number: int


def show_zstack_info_LM(zstack_info: ZStackServiceGetZStackInfoResponse) -> None:
    """
    Display the Z-Stack information.
    Args:
        zstack_info (ZStackServiceGetZStackInfoResponse): The Z-Stack information to display.
    Returns:
        None
    """

    logger.info("------------  Z-Stack Information Start  ------------")
    logger.info(f"First Slice: {zstack_info.first_slice*1e6:.3f}")
    logger.info(f"Last Slice: {zstack_info.last_slice*1e6:.3f}")
    logger.info(f"Range: {zstack_info.range*1e6:.3f}")
    logger.info(f"Slices: {zstack_info.num_slices}")
    logger.info(f"Interval: {zstack_info.interval*1e6:.3f}")
    logger.info(f"Center Mode: {zstack_info.is_center_mode}")
    logger.info(f"Offset: {zstack_info.offset}")
    logger.info("------------  Z-Stack Information End  ------------")



def show_swaf_info_LM(
    info: ExperimentSwAutofocusServiceGetAutofocusParametersResponse,
) -> None:
    """
    Display the SWAF information.
    Args:
        info (ExperimentSwAutofocusServiceGetAutofocusParametersResponse): The SWAF information.
    Returns:
        None
    """

    logger.info("------------  SWAF Information Start  ------------")
    logger.info(f"Mode: {info.auto_focus_mode}")
    logger.info(f"Sampling: {info.autofocus_sampling}")
    logger.info(f"Contrast Measure: {info.contrast_measure}")
    logger.info(f"Search Strategy: {info.search_strategy}")
    logger.info(f"Lower Limit: {info.lower_limit*1e6:.3f}")
    logger.info(f"Upper Limit: {info.upper_limit*1e6:.3f}")
    logger.info(f"Offset: {info.offset*1e6:.3f}")
    logger.info(f"Reference Channel: {info.reference_channel_name}")
    logger.info(f"Relative Range Auto: {info.relative_range_is_automatic}")
    logger.info(f"Relative Search Range: {info.relative_search_range*1e6:.3f}")
    logger.info(f"Acquisition ROI: {info.use_acquisition_roi}")
    logger.info("------------  SWAF Information End  ------------")


def show_track_info_LM(info: TrackServiceGetTrackInfoResponse) -> TrackInfo:
    """
    Logs detailed information about tracks and their channels, and returns a TrackInfo object.
    Args:
        info (TrackServiceGetTrackInfoResponse): The response object containing track information.
    Returns:
        TrackInfo: An object containing the track information and the number of tracks.
    Logs:
        Logs the start and end of track information.
        Logs each track's index and activation status.
        Logs each channel's index, name, and activation status within each track.
    """

    tracks = TrackInfo()
    tracks.info = info.track_info
    tracks.number = len(info.track_info)

    logger.info("------------  Track Information Start  ------------")

    for index, ti in enumerate(info.track_info):

        for ch in range(len(ti.channels)):
            logger.info(
                f"TR: {index} - {ti.is_activated} CH: {ch} - {ti.channels[ch].name} - {ti.channels[ch].is_activated}"
            )

    logger.info("------------  Track Information End  ------------")

    return tracks


async def save_experiment(
    exp: ExperimentServiceLoadResponse,
    expservice: ExperimentServiceStub,
    expname: str = "MyExperiment",
    overwrite: bool = False,
):
    """
    Saves the modified experiment using a defined name.
    Args:
        exp (ExperimentServiceLoadResponse): The experiment to be saved.
        expservice (ExperimentServiceStub): The service stub to handle the save operation.
        expname (str, optional): The name to save the experiment as. Defaults to "MyExperiment".
        overwrite (bool, optional): Whether to allow overwriting an existing experiment with the same name. Defaults to False.
    Returns:
        bool: True if the experiment was saved successfully, False otherwise.
    Raises:
        Exception: If there is an error during the save operation, it will be logged and the function will return False.
    """
    try:
        # save the modified experiment using a defined name without the *.czexp extension
        logger.info("Saving Experiment ...")
        await expservice.save(
            ExperimentServiceSaveRequest(
                experiment_id=exp.experiment_id,
                experiment_name=expname,
                allow_override=overwrite,
            )
        )

        return True

    except Exception as e:
        logger.error(f"Error saving experiment: {e}")

        return False


def delete_czifile(image_folder: str | Path, cziname: str) -> bool:
    """
    Deletes a CZI file from the specified folder.

    Args:
        image_folder (str | Path): The path to the folder containing the CZI file.
        cziname (str): The name of the CZI file (without the .czi extension).

    Returns:
        bool: True if the file was successfully deleted, False otherwise.

    Raises:
        ValueError: If image_folder or cziname is empty or None.
    """

    # Input validation
    if not image_folder:
        logger.error("Image folder path cannot be empty or None")
        return False

    if not cziname or not cziname.strip():
        logger.error("CZI filename cannot be empty or None")
        return False

    try:
        # Convert to Path object and validate
        folder_path = Path(image_folder)

        # For string inputs, check if empty after stripping
        if isinstance(image_folder, str) and not image_folder.strip():
            logger.error("Image folder path cannot be empty")
            return False

        # Clean the filename - remove .czi extension if already present
        clean_filename = cziname.strip()
        if clean_filename.lower().endswith(".czi"):
            clean_filename = clean_filename[:-4]

        filepath2check = folder_path / f"{clean_filename}.czi"

        # Check if the path is valid and file exists
        if not filepath2check.parent.exists():
            logger.error(f"Directory does not exist: {filepath2check.parent}")
            return False

        if filepath2check.exists():
            # Check if it's actually a file (not a directory)
            if not filepath2check.is_file():
                logger.error(f"Path exists but is not a file: {filepath2check}")
                return False

            logger.info(f"Deleting CZI file: {filepath2check}")
            filepath2check.unlink()

            # Verify deletion was successful
            if filepath2check.exists():
                logger.error(f"Failed to delete file: {filepath2check}")
                return False

            logger.info(f"Successfully deleted: {filepath2check}")
            return True
        else:
            logger.warning(f"File does not exist: {filepath2check}")
            return False

    except PermissionError as e:
        logger.error(f"Permission denied when trying to delete {filepath2check}: {e}")
        return False
    except OSError as e:
        logger.error(f"OS error when trying to delete {filepath2check}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error when trying to delete CZI file: {e}")
        return False


async def load_experiment(experiment_service: ExperimentServiceStub, experiment_name: str) -> str:
    """
    Load an experiment by name and return its ID.
    Args:
        experiment_service (ExperimentServiceStub): The experiment service stub for making API calls.
        experiment_name (str): The name of the experiment to load.
    Returns:
        str: The unique identifier of the loaded experiment.
    Raises:
        Exception: If the experiment loading fails or the experiment is not found.
    """
    response = await experiment_service.load(ExperimentServiceLoadRequest(experiment_name))

    return response.experiment_id


async def run_experiment(experiment_service: ExperimentServiceStub, experiment_id: str) -> Path:
    """
    Run an experiment and return the path to the output image file.
    This function initiates an experiment execution by first retrieving the image output path
    from the experiment service, then running the specified experiment, and finally constructing
    the full path to the resulting CZI image file.
    Args:
        experiment_service (ExperimentServiceStub): The gRPC service stub for experiment operations.
        experiment_id (str): The unique identifier of the experiment to run.
    Returns:
        Path: The complete file path to the generated CZI image file, constructed by combining
              the image output path with the experiment's output name and .czi extension.
    Raises:
        Exception: May raise exceptions from the underlying gRPC service calls if the experiment
                   service is unavailable or if the experiment execution fails.
    """
    response = await experiment_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    image_output_path = response.image_output_path

    response = await experiment_service.run_experiment(ExperimentServiceRunExperimentRequest(experiment_id))

    return Path(image_output_path) / f"{response.output_name}.czi"
