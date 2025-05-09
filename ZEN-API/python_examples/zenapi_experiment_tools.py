# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_experiment_tools.py
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
    TrackInfo,
)

# import the auto-generated python modules
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadResponse,
    ExperimentServiceSaveRequest,
)

from dataclasses import dataclass
from typing import List
from zenapi_tools import set_logging
from pathlib import Path

logger = set_logging()


@dataclass
class Tracks:
    info: List[TrackInfo]
    number: int


def show_zstack_info_LM(info: ZStackServiceGetZStackInfoResponse) -> None:
    """
    Display the Z-Stack information.
    Args:
        info (ZStackServiceGetZStackInfoResponse): The Z-Stack information to display.
    Returns:
        None
    """

    logger.info("------------  Z-Stack Information Start  ------------")
    logger.info(f"First Slice: {info.first_slice*1e6:.3f}")
    logger.info(f"Last Slice: {info.last_slice*1e6:.3f}")
    logger.info(f"Range: {info.range*1e6:.3f}")
    logger.info(f"Slices: {info.num_slices}")
    logger.info(f"Interval: {info.interval*1e6:.3f}")
    logger.info(f"Center Mode: {info.is_center_mode}")
    logger.info(f"Offset: {info.offset}")
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

        # logger.info(f"Track: {index} Active: {ti.is_activated}")

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


def delete_czifile(image_folder: str, cziname: str) -> bool:
    """
    Deletes a CZI file from the specified folder.
    Args:
        image_folder (str): The path to the folder containing the CZI file.
        cziname (str): The name of the CZI file (without the .czi extension).
    Returns:
        bool: True if the file was successfully deleted, False otherwise.
    """

    if Path(image_folder / (cziname + ".czi")).exists():
        logger.info("Deleting CZI file: " + cziname + ".czi")
        Path(image_folder / (cziname + ".czi")).unlink()
        return True

    return False
