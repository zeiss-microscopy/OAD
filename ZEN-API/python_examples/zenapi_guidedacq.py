# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_guidedacq.py
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
import numpy as np
from pathlib import Path
from zen_api_utils.misc import initialize_zenapi, set_logging
from zen_api_utils.tiles_positions import TileRegionRectangle, TileRegionPolygon, TileRegionEllipse
import zen_api_utils.zen_tcpip_commands as zen_tcpip_commands
from zen_api_utils.zen_tcpip import ZenCommands
from processing_tools import segment_czi
from czitools.utils import planetable
from tqdm import trange
from datetime import datetime
import shutil
from typing import Union
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from pylibCZIrw import czi as pyczi
import pandas as pd

# import the auto-generated python modules for ZEN API
from zen_api.common.v1 import DoublePoint
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceCloneRequest,
    ExperimentServiceRunExperimentRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceSaveRequest,
)

from zen_api.lm.acquisition.v1beta import (
    TilesServiceStub,
    TilesServiceIsTilesExperimentRequest,
    TilesServiceAddRectangleTileRegionRequest,
    TilesServiceAddPolygonTileRegionRequest,
    TilesServiceAddEllipseTileRegionRequest,
    TilesServiceClearRequest,
)


async def gca_run_detailscan(
    experiment: str,
    exp_service: ExperimentServiceStub,
    tile_service: TilesServiceStub,
    tileregion: Union[TileRegionRectangle, TileRegionPolygon, TileRegionEllipse],
    output_name: str = "zenapi_detail",
    verbose: bool = False,  # for testing purposes
):
    """
    Runs a detailed scan for a given experiment and tile region.

    Args:
        experiment (str): The name of the experiment to be loaded.
        exp_service (ExperimentServiceStub): The experiment service stub.
        tile_service (TilesServiceStub): The tile service stub.
        tileregion (Union[TileRegionRectangle, TileRegionPolygon, TileRegionEllipse]): The tile region to be added to the experiment.
        output_name (str, optional): The name of the output CZI file. Defaults to "zenapi_detail".
        verbose (bool, optional): Indicates whether to show addition logging output and do stuff. Defaults to False.

    Returns:
        exp_result: The result of running the experiment.

    """

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=experiment))

    # clone the experiment
    my_exp_cloned = await exp_service.clone(ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id))

    # clear existing TileRegions
    await tile_service.clear(TilesServiceClearRequest(experiment_id=my_exp_cloned.experiment_id))

    if isinstance(tileregion, TileRegionRectangle):

        # add a tile region to the experiment using [m] as unit (experiment needs to have a tileRegion already)
        await tile_service.add_rectangle_tile_region(
            TilesServiceAddRectangleTileRegionRequest(
                experiment_id=my_exp_cloned.experiment_id,
                center_x=tileregion.center_x,
                center_y=tileregion.center_y,
                width=tileregion.width,
                height=tileregion.height,
                z=tileregion.zvalue,
            )
        )

    if isinstance(tileregion, TileRegionPolygon):

        # add a tile region to the experiment using [m] as unit (experiment needs to have a tileRegion already)
        await tile_service.add_polygon_tile_region(
            TilesServiceAddPolygonTileRegionRequest(
                experiment_id=my_exp_cloned.experiment_id,
                polygon_points=tileregion.polygon,
                z=tileregion.zvalue,
            )
        )

    if isinstance(tileregion, TileRegionEllipse):

        # add a tile region to the experiment using [m] as unit (experiment needs to have a tileRegion already)
        await tile_service.add_ellipse_tile_region(
            TilesServiceAddEllipseTileRegionRequest(
                experiment_id=my_exp_cloned.experiment_id,
                center_x=tileregion.center_x,
                center_y=tileregion.center_y,
                width=tileregion.x_diameter,
                height=tileregion.y_diameter,
                z=tileregion.zvalue,
            )
        )

    # create the correct name for the CZI
    cziname = output_name + "_" + str(tileregion.id)

    # for testing purposes - check if the experiment has TileRegions
    if verbose:
        # do something with the TileRegions
        has_tiles = await tile_service.is_tiles_experiment(
            TilesServiceIsTilesExperimentRequest(experiment_id=my_exp.experiment_id)
        )

        logger.info(
            f"Cloned Experiment Id: {my_exp_cloned.experiment_id} has TileRegions: {has_tiles.is_tiles_experiment}"
        )

        # save the clones experimented using a defined name without the *.czexp extension
        logger.info("Saving Experiment ...")

        await exp_service.save(
            ExperimentServiceSaveRequest(
                experiment_id=my_exp_cloned.experiment_id,
                experiment_name=experiment + "_cloned",
                allow_override=True,
            )
        )

    # execute the actual experiment and wait until it is finished
    exp_result = await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(experiment_id=my_exp_cloned.experiment_id, output_name=cziname)
    )

    return exp_result


async def gca_run_overviewscan(
    experiment: str,
    exp_service: ExperimentServiceStub,
    output_name: str = "zenapi_overview",
):
    """
    Runs an experiment with the specified parameters.

    Args:
        experiment (str): The name of the experiment to run.
        exp_service (ExperimentServiceStub): The experiment service stub.
        output_name (str, optional): The output name for the experiment. Defaults to "zenapi_overview".

    Returns:
        The result of running the experiment.
    """

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=experiment))

    # clone the experiment
    my_exp_cloned = await exp_service.clone(ExperimentServiceCloneRequest(experiment_id=my_exp.experiment_id))

    # create the correct name for the CZI
    cziname = output_name + "_OV"

    # execute the actual experiment and wait until it is finished
    exp_result = await exp_service.run_experiment(
        ExperimentServiceRunExperimentRequest(experiment_id=my_exp_cloned.experiment_id, output_name=cziname)
    )

    return exp_result


def show_segmentation(
    savename_seg: Union[Path, str],
    results: pd.DataFrame,
    channel: int = 0,
    export: bool = False,
) -> Union[str, None]:
    """
    Displays a 2D image plane from a CZI file and overlays segmentation results.

    Args:
        savename_seg (Union[Path, str]): Path to the CZI file to be opened.
        results (pd.DataFrame): DataFrame containing segmentation results with polygon coordinates.
        channel (int, optional): The channel to read from the CZI file. Default is 0.
        export (bool, optional): If True, saves the displayed image as a PNG file. Default is False.

    Returns:
        Union[str, None]: The path to the saved PNG file if export is True, otherwise None.
    """
    with pyczi.open_czi(str(savename_seg)) as czidoc:
        # read a 2d image plane
        img2d = czidoc.read(plane={"C": channel})

    # show the 2D image plane
    plt.ion()
    fig1, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.imshow(img2d[..., 0], cmap=cm.inferno, vmin=img2d.min(), vmax=img2d.max())

    for tr_id in range(results.shape[0]):

        # get list with X and Y positions for polygon
        xpos = results["polygon"][tr_id][1]
        ypos = results["polygon"][tr_id][0]

        ax.plot(xpos, ypos, "w--", lw=2, alpha=1.0)

    ax.set_title(savename_seg)
    plt.show(block=False)
    plt.pause(0.5)  # Pause for a short period to allow the plot to update

    if export:
        plt.savefig(savename_seg.with_suffix(".png"), dpi=300)
        plt.close(fig1)

        return savename_seg.with_suffix(".png")

    return None


async def main():

    # OVERVIEW SCAN
    overview_exp = "00000_Overview_15x8_DAPI_5X"

    # simulate overview scan by loading a CZI image
    show_overview = True

    # please adapt to your needs
    filepath_overview = Path(
        # r"F:\AzureDevOps\RMS_Users\Playground\ZEN_API\data\OverViewScan.czi"
        r"F:\Github\OAD\ZEN-API\python_examples\data\OverViewScan.czi"
    )

    # DETAIL SCAN
    # detail_exp = "00001_Detail"
    detail_exp = "ZEN_API_GuidedAcq"

    # general parameters
 
    # Get the directory where the current script is located
    script_dir = Path(__file__).parent

    # Build the path to config.ini relative to the script
    config_path = script_dir / "config.ini"
    open_detail = False
    region_type = "polygon"
    show_segresults = True
    verbose = False  # save the cloned experiments to disk to check later and create additional logging

    # run the overview scan
    logger.info(f"Run or simulate OverView Scan: {overview_exp}")

    if show_overview:
        # open the image in ZEN (for demo purposes) using TCP-IP
        commandlist = zen_tcpip_commands.add_image(str(filepath_overview))
        my_commands = ZenCommands(commandlist)
        my_commands.execute()

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string  
    timestamp_folder = now.strftime("%Y-%m-%d_%H-%M-%S")

    # read the planetable to derive a Z-value for the TileRegion modification
    pt, savepath = planetable.get_planetable(filepath_overview, save_table=False, planes={"time": 0, "channel": 0, "zplane": 0})

    # get the median Z-value
    zvalue_image = np.round(pt.loc[:, "Z[micron]"].median(), 2)

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(config_path)

    # create the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # show output path for images
    zen_savefolder = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())

    # exp_result = await gca_run_overviewscan(overview_exp, exp_service)
    # cziname_ov = f"{exp_result.output_name}.czi"
    cziname_ov = filepath_overview.stem + "_OV.czi"

    # run the overview scan
    logger.info(f"Start Segmentation of OverView: {overview_exp}")

    # create general save path
    save_path = Path(zen_savefolder.image_output_path) / timestamp_folder

    savepath_seg, results, savepath_csv, objects = segment_czi(
        str(filepath_overview),
        str(save_path),
        chindex=0,
        filter_method="gaussian",
        filter_size=7,
        min_objectsize=100000,
        max_holesize=1000,
        add_polygons=True,
    )

    logger.info(f"Number of detected objects: {objects['Number'].values[0]}")

    # move the CZI to ist final destination
    src_path_ov = filepath_overview
    dst_path_ov = save_path / cziname_ov
    # shutil.move(str(src_path_ov), str(dst_path_ov))
    shutil.copy(str(src_path_ov), str(dst_path_ov))

    if show_segresults:

        show_segmentation(dst_path_ov, results, channel=0, export=True)

    # get TileService
    tile_service = TilesServiceStub(channel=channel, metadata=metadata)

    # create an empty list to hold the output filepaths of the individual detailed scans
    detail_scan_czifile = []

    for tr_id in trange(results.shape[0]):

        # in case TileRegion should be a polygon
        if region_type == "polygon":

            polygon = []

            # get list with X and Y positions for polygon
            xpos = results["polygon_scaled"][tr_id][0]
            ypos = results["polygon_scaled"][tr_id][1]

            # loop over all points and add to the list of DoublePoints
            for id in range(len(xpos)):
                pointXY = DoublePoint(x=xpos[id] * 1e-6, y=ypos[id] * 1e-6)
                polygon.append(pointXY)

            tr = TileRegionPolygon()
            tr.id = tr_id
            # update values in [m]
            tr.polygon = polygon
            tr.zvalue = zvalue_image * 1e-6
            if verbose:
                logger.info(f"TileRegion PolyGon ID: {tr.id}")

        # in case TileRegion should be a rectangle
        if region_type == "rectangle":

            tr = TileRegionRectangle()
            tr.id = tr_id

            # update values in [m]
            tr.center_x = results.loc[tr_id, "bbox_center_stageX"] * 1e-6
            tr.center_y = results.loc[tr_id, "bbox_center_stageY"] * 1e-6
            tr.width = results.loc[tr_id, "bbox_width_scaled"] * 1e-6
            tr.height = results.loc[tr_id, "bbox_height_scaled"] * 1e-6
            tr.zvalue = zvalue_image * 1e-6
            if verbose:
                logger.info(f"XY Center TileRegion Rectangle: {tr.center_x}, {tr.center_y}")

        # in case TileRegion should be an ellipse
        if region_type == "ellipse":

            tr = TileRegionEllipse()
            tr.id = tr_id
            # update values in [m]
            tr.center_x = results.loc[tr_id, "bbox_center_stageX"] * 1e-6
            tr.center_y = results.loc[tr_id, "bbox_center_stageY"] * 1e-6
            tr.x_diameter = results.loc[tr_id, "bbox_width_scaled"] * 1e-6
            tr.y_diameter = results.loc[tr_id, "bbox_height_scaled"] * 1e-6
            tr.zvalue = zvalue_image * 1e-6
            if verbose:
                logger.info(f"XY Center TileRegion Ellipse: {tr.center_x}, {tr.center_y}")

        # run the actual detail scan for every object
        exp_result = await gca_run_detailscan(
            detail_exp,
            exp_service,
            tile_service,
            tr,
            output_name="zenapi_detail",
            verbose=verbose,
        )

        # move the CZI to ist final destination
        src_path = Path(zen_savefolder.image_output_path) / f"{exp_result.output_name}.czi"
        detail_scan_czifile.append(src_path)

    # close the channel
    channel.close()

    # move the CZI from a detailed scan to the correct folder
    for czifile in detail_scan_czifile:
        dst_path = save_path / czifile.name
        shutil.move(str(czifile), str(dst_path))

        if open_detail:

            # open the image in ZEN (for demo purposes) using TCP-IP
            cmdlist = zen_tcpip_commands.add_image(str(dst_path))
            my_cmds = ZenCommands(cmdlist)
            my_cmds.execute()


if __name__ == "__main__":

    # create logger
    logger = set_logging()

    # run the main function
    asyncio.run(main())
