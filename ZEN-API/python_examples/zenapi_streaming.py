# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_streaming.py
# Author      : Srh, JSm, JHa
# Institution : Carl Zeiss Microscopy GmbH
#
# The script demos the usage of the ZEN-API for streaming.
# The script starts an experiment and will display the pixel data using PyQtGraph.
# The expected frame size has to be adapted by the user beforehand right now.
# it is also possible to apply so basic online processing to showcase this option
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
import qasync
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QColor
import pyqtgraph as pg
import sys
from pathlib import Path
from zen_api_utils.misc import initialize_zenapi, set_logging
from processing_tools import ArrayProcessor
from czmodel.pytorch.convert import DefaultConverter
from czmodel import ModelMetadata
from onnx_inference import OnnxInferencer
from enum import Enum, unique
import os
import random
from typing import Optional, Union

# import the auto-generated python modules for ZEN API
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentStreamingServiceStub,
    ExperimentStreamingServiceMonitorExperimentRequest,
    ExperimentStreamingServiceMonitorAllExperimentsRequest,
    ExperimentServiceLoadRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceGetAvailableExperimentsRequest,
    ExperimentServiceStartExperimentRequest,
)


@unique
class Processing(Enum):
    NO_PROCESSING = 1
    SEG_THRESHOLD_OTSU = 2
    SEG_THRESHOLD_MANUAL = 3
    SEG_SEMANTIC = 4
    DENOISE = 5


async def start_experiment(
    exp_name: str = "my_exp.czexp",
    czi_name: str = "my_image.czi",
    overwrite: bool = False,
    verbose: bool = False,
    configfile: str = "config.ini",
) -> str:
    """
        Start an experiment from ZEN-API
    Args:
        exp_name (str): name of the experiment without the *.czexp extension
        czi_name (str): desired name of the CZI image to be written
        overwrite (bool): allow overwriting an existing CZI
        verbose (bool): show additional outputs for testing purposes
        configfile (str): define the ZEN API configuration

    Returns:
        my_exp.experiment_id (str): the reference id of the experiment

    Raises:
        None

    """
    # get the gRPC channel and the metadata
    try:
        channel, metadata = initialize_zenapi(configfile)
    except Exception as e:
        logger.error(f"Failed to initialize ZEN API with config file '{configfile}': {e}")
        raise
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # get available experiments from the ZEN core default folder
    # Example Location: "...\Documents\Carl Zeiss\ZENCore\Documents\Experiment Setups"
    available_experiments = await exp_service.get_available_experiments(
        ExperimentServiceGetAvailableExperimentsRequest()
    )

    if verbose:
        logger.info("Available Experiment File(s) inside ZEN folder:")
        for exp in available_experiments.experiments:
            logger.info(exp.name + ".czexp")

    # load experiment by its name without the *.czexp extension
    my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=exp_name))

    # show output path for images
    save_path = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    logger.info("Saving Location for CZI Images:" + save_path.image_output_path)

    # check if such an image already exists and delete it
    if Path(Path(save_path.image_output_path) / (czi_name + ".czi")).exists():
        if overwrite:
            Path(Path(save_path.image_output_path) / (czi_name + ".czi")).unlink()
            logger.info("Overwrite CZI file: " + czi_name + ".czi")
        elif not overwrite:
            logger.error("CZI file: " + czi_name + ".czi cannot be overwritten")
            channel.close()
            raise FileExistsError("CZI file: " + czi_name + ".czi cannot be overwritten")

    # execute experiment
    logger.info("Starting Experiment Execution ...")

    # start the experiment (and do not wait until it is finished)
    await exp_service.start_experiment(
        ExperimentServiceStartExperimentRequest(experiment_id=my_exp.experiment_id, output_name=czi_name)
    )

    # close the channel
    channel.close()

    return my_exp.experiment_id


class MainWindow(QtWidgets.QMainWindow):
    def __init__(
        self,
        loop=None,
        configfile: str = "config.ini",
        start_experiment_from_UI: bool = True,
        my_experiment: str = "my_exp.czexp",
        czi_name: str = "my_image.czi",
        *args,
        **kwargs,
    ):
        super(MainWindow, self).__init__(*args, **kwargs)

        # self.expID will be assigned when needed
        self.loop = loop
        self.imageView = pg.ImageView()
        self.setWindowTitle("ZEN-API Pixel Stream")
        self.setCentralWidget(self.imageView)
        self.pen = QPen()
        self.pen.setWidthF(0.05)  # set bounding box width

        try:
            # get the gRPC channel and the metadata
            self.channel, self.metadata = initialize_zenapi(configfile)
        except Exception as e:
            logger.error(f"Failed to initialize ZEN API with config file '{configfile}': {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to initialize ZEN API: {e}")
            sys.exit(1)

        self.streaming_service = ExperimentStreamingServiceStub(channel=self.channel, metadata=self.metadata)

        self.start_experiment_from_UI = start_experiment_from_UI

        # if the experiment is not started from UI than start one via ZEN API
        if not self.start_experiment_from_UI:
            logger.info(f"Starting Experiment via ZEN API: {my_experiment}")
            self.expID = asyncio.run(
                start_experiment(
                    exp_name=my_experiment,
                    czi_name=czi_name,
                    overwrite=True,
                    verbose=False,
                    configfile=configfile,
                )
            )
            logger.info(f"Experiment ID: {self.expID}")

    async def read(
        self,
        processing: Processing = Processing.NO_PROCESSING,
        dtype: np.dtype = np.uint8,
        threshold: Optional[int] = 0,
        inferencer: Optional[OnnxInferencer] = None,
        model_metadata: Optional[ModelMetadata] = None,
        channel_index: Optional[Union[None, int]] = None,
        enable_raw_data: Optional[bool] = False,
        draw_bbox: Optional[bool] = True,
        measure_properties: Optional[tuple] = None,
        verbose=False,
    ):
        """
        Reads and processes frames from the streaming service.

        Args:
            processing (Processing): The type of processing to apply to the frames.
            dtype (np.dtype): The data type of the frames.
            threshold (Optional[int]): The threshold value for segmentation.
            inferencer (Optional[OnnxInferencer]): The inferencer for semantic segmentation.
            model_metadata (Optional[ModelMetadata]): The metadata of the model.
            channel_index (Optional[Union[None, int]]): The index of the channel.
            enable_raw_data: Optional[bool]: Read partial frames or scan lines (True) or full frames (True)
            draw_bbox (Optional[bool]): Whether to draw bounding boxes around detected objects.
            verbose (bool): show additional outputs for testing purposes

        Returns:
            None
        """

        # this will only return a stream if there is an experiment running
        # the channel index can be used to "filter" for specific channels.
        # If None, all channels are returned.

        if self.start_experiment_from_UI:
            async_iterable = self.streaming_service.monitor_all_experiments(
                ExperimentStreamingServiceMonitorAllExperimentsRequest(
                    channel_index=channel_index, enable_raw_data=enable_raw_data
                )
            )
            logger.info("Getting PixelStream from Experiment started from UI")

        if not self.start_experiment_from_UI:
            async_iterable = self.streaming_service.monitor_experiment(
                ExperimentStreamingServiceMonitorExperimentRequest(
                    experiment_id=self.expID,
                    channel_index=channel_index,
                    enable_raw_data=enable_raw_data,
                )
            )
            logger.info("Getting PixelStream from Experiment started by ZEN API")

        async for response in async_iterable:

            time = response.frame_data.frame_position.t  # time index
            zplane = response.frame_data.frame_position.z  # zplane index
            tile = response.frame_data.frame_position.m  # tile index
            ch = response.frame_data.frame_position.c  # channel index
            scene = response.frame_data.frame_position.s  # scene index
            x = response.frame_data.frame_position.x  # xpos top-left [pixel]
            y = response.frame_data.frame_position.y  # ypos top-left [pixel]
            full_size = response.frame_data.frame_size  # full frame sizeXY [pixel]
            scale_x = response.frame_data.scaling.x * 1e6
            scale_y = response.frame_data.scaling.y * 1e6

            # Size (in pixels) of the pixel data.
            # Together with the start position property, this represents the rectangle where the pixels are located inside the full frame.
            # For ordinary acquisition this will be the full frame size, but for partial acquisition this can be just one part of the full frame.

            partial_size = response.frame_data.pixel_data.size  # partial frame sizeXY [pixel]

            if verbose:
                logger.info(
                    f"Full Size: {full_size} PartialSize: {partial_size} Scaling: {scale_x:.3f} - {scale_y:.3f}"
                )

            stage_x = response.frame_data.frame_stage_position.x * 1e6  # StageX [m]
            stage_y = response.frame_data.frame_stage_position.y * 1e6  # StageY [m]
            stage_z = response.frame_data.frame_stage_position.z * 1e6  # StageZ [m]

            # convert the byte stream into 2d image
            if not enable_raw_data:
                stream2d = np.frombuffer(response.frame_data.pixel_data.raw_data, dtype=dtype).reshape(
                    (full_size.height, full_size.width)
                )

            if enable_raw_data:
                stream2d = np.frombuffer(response.frame_data.pixel_data.raw_data, dtype=dtype).reshape(
                    (partial_size.height, partial_size.width)
                )

            # rotate and flip the image to have the same orientation as in ZEN
            stream2d = np.flipud(np.rot90(stream2d))

            # testing - not sure if that really imporves performance yet
            stream2d = np.ascontiguousarray(stream2d, dtype=dtype)

            num_objects = 0

            # processing
            if processing is not Processing.NO_PROCESSING:

                # create an ArrayProcessor using the current frame from stream
                ap = ArrayProcessor(stream2d)

                # apply threshold segmentation OTSU
                if processing is Processing.SEG_THRESHOLD_OTSU:

                    pro2d = ap.apply_otsu_threshold()

                # apply threshold segmentation MANUAL
                if processing is Processing.SEG_THRESHOLD_MANUAL:

                    pro2d = ap.apply_threshold(value=threshold, invert_result=False)

                # apply a semantic segmentation
                if processing is Processing.SEG_SEMANTIC:

                    # there is no tile inference implemented yet
                    pro2d = ap.apply_semantic_seg(
                        inferencer=inferencer,
                        input_shape=model_metadata.input_shape,
                        class_index=2,
                        use_gpu=True,
                    )

                # count objects and measure parameters
                if (
                    processing is Processing.SEG_THRESHOLD_OTSU
                    or processing is Processing.SEG_THRESHOLD_MANUAL
                    or processing is Processing.SEG_SEMANTIC
                ):
                    ap = ArrayProcessor(pro2d)
                    pro2d, num_objects, props = ap.label_objects(
                        min_size=100,
                        label_rgb=False,
                        orig_image=None,
                        bg_label=0,
                        measure_params=True,
                        measure_properties=measure_properties,
                    )

                    # update the image view with original image
                    self.imageView.setImage(stream2d, autoHistogramRange=True)

                    # draw bounding boxes around the objects
                    if draw_bbox and props is not None:

                        # remove all ROIs from previous frame
                        for item in self.imageView.getView().allChildren():
                            if isinstance(item, pg.ROI):
                                self.imageView.getView().removeItem(item)

                        for index, row in props.iterrows():

                            roi = pg.ROI(
                                [row["bbox-0"], row["bbox-1"]],  # [x, y]
                                [
                                    row["bbox-2"] - row["bbox-0"],  # width
                                    row["bbox-3"] - row["bbox-1"],  # height
                                ],
                                removable=True,
                                resizable=False,
                                movable=False,
                            )

                            # set random color
                            self.pen.setColor(
                                QColor(
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                )
                            )
                            roi.setPen(self.pen)

                            self.imageView.addItem(roi)

                # apply a regression model (aka Noise2Void etc.)
                if processing is Processing.DENOISE:

                    pro2d = ap.apply_regression(
                        inferencer=inferencer,
                        input_shape=model_metadata.input_shape,
                        use_gpu=True,
                    )

                    # update the image view with processed image
                    self.imageView.setImage(pro2d, autoHistogramRange=True)

            if processing is Processing.NO_PROCESSING:

                # update the image view with original image
                self.imageView.setImage(stream2d, autoHistogramRange=True)

            # show pixel stream metadata
            logger.info(
                f"S={scene} T={time} M={tile} Z={zplane} C={ch} - TL_XY [pixel]: {x} x {y} - XYZ [micron]: {stage_x:.3f} x {stage_y:.3f} x {stage_z:.3f} - Objects: {num_objects}"
            )


def main(
    configfile: str,
    pixeltype: np.dtype,
    czi_name: str,
    start_experiment_from_UI: bool,
    my_experiment: str,
    channel_index: int,
    processing: Processing,
    threshold: int,
    czann_filepath: str,
    enable_raw_data: bool = False,
):

    inferencer = None
    measure_properties = ("label", "area", "centroid", "bbox")

    # start application and create async event loop to display the pixels
    app = QtWidgets.QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # create the main window and pass on the event loop
    window = MainWindow(
        loop,
        configfile=configfile,
        my_experiment=my_experiment,
        start_experiment_from_UI=start_experiment_from_UI,
        czi_name=czi_name,
    )
    window.show()

    if processing is Processing.SEG_SEMANTIC or processing is Processing.DENOISE:
        # extract the model information and path and to the prediction

        # this is the new way of unpacking using the czann files
        model_metadata, model_path = DefaultConverter().unpack_model(
            model_file=czann_filepath,
            target_dir=Path.cwd() / os.path.dirname(czann_filepath),
        )

        # this is the new way of unpacking using the czann files
        model_metadata, model_path = DefaultConverter().unpack_model(
            model_file=czann_filepath,
            target_dir=Path.cwd() / os.path.dirname(czann_filepath),
        )

        # create ONNX inferencer once and use it for every tile
        inferencer = OnnxInferencer(str(model_path))
        logger.info("Started ONNXInferencer Session.")
    else:
        model_metadata = None

    with loop:

        # start the pixel display application
        asyncio.ensure_future(
            window.read(
                processing=processing,
                dtype=pixeltype,
                threshold=threshold,
                inferencer=inferencer,
                model_metadata=model_metadata,
                channel_index=channel_index,
                enable_raw_data=enable_raw_data,
                measure_properties=measure_properties,
                verbose=False,
            ),
            loop=loop,
        )

        loop.run_forever()


if __name__ == "__main__":

    # define the desired online processing here
    # processing = Processing.NO_PROCESSING
    # processing = Processing.SEG_THRESHOLD_MANUAL
    processing = Processing.SEG_THRESHOLD_OTSU
    # processing = Processing.SEG_SEMANTIC  # --> cyto2022_nuc2.czann
    # processing = Processing.DENOISE  # --> LiveDenoise_DAPI.czann

    # Get the directory where the current script is located
    script_dir = Path(__file__).parent

    # Build the path to config.ini relative to the script
    config_path = script_dir / "config.ini"

    #czann_filepath = r"F:\Github\ZEN_Python_CZI_Smart_Microscopy_Workshop\workshop\zen_api\ai_models\simple_pytorch_nuclei_segmodel_pytorch.czann"
    czann_filepath = r"F:\Github\ZEN_Python_CZI_Smart_Microscopy_Workshop\workshop\zen_api\ai_models\cyto2022_nuc2.czann"
    # czann_filepath = r"F:\Github\ZEN_Python_CZI_Smart_Microscopy_Workshop\workshop\zen_api\ai_models\LiveDenoise_DAPI.czann"

    logger = set_logging()

    main(
        configfile=config_path,
        pixeltype=np.dtype(np.uint16),  # must match experiment output
        czi_name="zenapi_test",
        start_experiment_from_UI=True,
        my_experiment="ZEN_API_Test_w96_1024x1024_CH=2",
        channel_index=0,
        processing=processing,
        threshold=850,
        czann_filepath=czann_filepath,
    )
