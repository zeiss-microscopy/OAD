#################################################################
# File        : zenapi_pixel_stream_basic.py
# Author      : Srh, JSm, JHa
# Institution : Carl Zeiss Microscopy GmbH
#
# The script demos the usage of the ZEN-API for streaming.
# The script starts an experiment and will display the pixel data using PyQtGraph.
# Frame dimensions are read from each streamed response. The example can also
# apply basic online processing to demonstrate that workflow.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import os

# to avoid a potential error with multiple OpenMP instances when using PyQtGraph and ONNX Runtime in the same environment
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import asyncio
import sys
from enum import Enum, unique
from pathlib import Path
from typing import Any

import numpy as np
import pyqtgraph as pg
import qasync
from pyqtgraph.imageview import ImageView

# import the auto-generated python modules for ZEN API
from zen_api.acquisition.v1beta import (
    ExperimentServiceGetAvailableExperimentsRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceLoadRequest,
    ExperimentServiceStartExperimentRequest,
    ExperimentServiceStub,
    ExperimentStreamingServiceGetNextFrameAllExperimentsRequest,
    ExperimentStreamingServiceStub,
)
from zen_api_utils.misc import initialize_zenapi, set_logging

logger = set_logging()


@unique
class Processing(Enum):
    NO_PROCESSING = 1
    SEG_THRESHOLD_OTSU = 2
    SEG_THRESHOLD_MANUAL = 3
    SEG_SEMANTIC = 4
    DENOISE = 5


def decode_frame(
    raw_data: bytes,
    dtype: np.dtype,
    width: int,
    height: int,
) -> np.ndarray:
    """Decode one row-major ZEN pixel payload with size validation."""
    expected_bytes = height * width * dtype.itemsize
    if len(raw_data) != expected_bytes:
        raise ValueError(
            f"Pixel payload has {len(raw_data)} bytes; expected " f"{expected_bytes} for {width}x{height} {dtype}"
        )
    frame = np.frombuffer(raw_data, dtype=dtype).reshape((height, width))
    return np.ascontiguousarray(frame, dtype=dtype)


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
    # Startup uses its own short-lived channel. The streaming channel remains
    # open on MainWindow because it is needed for the rest of the GUI session.
    try:
        channel, metadata = initialize_zenapi(configfile)
    except Exception as e:
        logger.error(f"Failed to initialize ZEN API with config file '{configfile}': {e}")
        raise
    try:
        exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

        # Querying the folder also verifies that the requested experiment can
        # be resolved by ZEN before the start request is sent.
        available_experiments = await exp_service.get_available_experiments(
            ExperimentServiceGetAvailableExperimentsRequest()
        )

        if verbose:
            logger.info("Available Experiment File(s) inside ZEN folder:")
            for exp in available_experiments.experiments:
                logger.info(exp.name + ".czexp")

        my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=exp_name))
        save_path = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
        logger.info("Saving Location for CZI Images:" + save_path.image_output_path)

        czi_path = Path(save_path.image_output_path) / f"{czi_name}.czi"
        if czi_path.exists():
            if overwrite:
                czi_path.unlink()
                logger.info("Overwrite CZI file: " + czi_name + ".czi")
            else:
                raise FileExistsError(f"CZI file already exists and cannot be overwritten: {czi_path}")

        logger.info("Starting Experiment Execution ...")
        await exp_service.start_experiment(
            ExperimentServiceStartExperimentRequest(
                experiment_id=my_exp.experiment_id,
                output_name=czi_name,
            )
        )
        return my_exp.experiment_id
    finally:
        channel.close()


class MainWindow(pg.Qt.QtWidgets.QMainWindow):
    def __init__(
        self,
        loop=None,
        configfile: Path | str = "config.ini",
        start_experiment_from_UI: bool = True,
        my_experiment: str = "my_exp.czexp",
        czi_name: str = "my_image.czi",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # The event loop is supplied by main(), but qasync owns it after this
        # constructor returns. The constructor only needs the API parameters.
        del loop
        self.imageView = ImageView()
        self.setWindowTitle("ZEN-API Pixel Stream")
        self.setCentralWidget(self.imageView)
        self.pen = pg.Qt.QtGui.QPen()
        self.pen.setWidthF(0.05)  # set bounding box width

        try:
            # Open the gRPC channel used by the streaming service. It stays
            # open for the lifetime of the window because frames arrive
            # asynchronously.
            self.channel, self.metadata = initialize_zenapi(configfile)
        except (FileNotFoundError, KeyError, OSError, ValueError) as e:
            logger.error(f"Failed to initialize ZEN API with config file '{configfile}': {e}")
            pg.Qt.QtWidgets.QMessageBox.critical(self, "Error", f"Failed to initialize ZEN API: {e}")
            sys.exit(1)

        self.streaming_service = ExperimentStreamingServiceStub(channel=self.channel, metadata=self.metadata)
        # Keep a control stub available for future experiment operations. The
        # current startup helper uses its own short-lived stub instead.
        self.experiment_service = ExperimentServiceStub(channel=self.channel, metadata=self.metadata)
        self.start_experiment_from_UI = start_experiment_from_UI
        self.stream_task: asyncio.Task | None = None

        # Start synchronously here because the qasync loop has not started yet.
        # Once this returns, the streaming coroutine can safely receive frames
        # from the experiment that was just started.
        if not self.start_experiment_from_UI:
            logger.info(f"Starting Experiment via ZEN API: {my_experiment}")
            self.expID = asyncio.run(
                start_experiment(
                    exp_name=my_experiment,
                    czi_name=czi_name,
                    overwrite=True,
                    verbose=False,
                    configfile=str(configfile),
                )
            )
            logger.info(f"Experiment ID: {self.expID}")

    async def do(
        self,
        dtype: np.dtype | None = None,
        channel_index: int | None = None,
        enable_raw_data: bool | None = False,
        verbose=False,
    ):
        if dtype is None:
            dtype = np.dtype(np.uint8)

        # Use the all-experiments endpoint in this lightweight example, so the
        # reader does not need to coordinate an experiment ID with the stream.
        while True:
            response = await self.streaming_service.get_next_frame_all_experiments(
                ExperimentStreamingServiceGetNextFrameAllExperimentsRequest(channel_index)
            )
            # Metadata describes where this frame belongs in the acquisition.
            # It is logged below so image display and acquisition coordinates
            # can be correlated when diagnosing a stream.
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

            # The payload size describes the rectangle actually present in the
            # byte stream. For partial acquisition it may be smaller than the
            # full image dimensions.
            partial_size = response.frame_data.pixel_data.size  # partial frame sizeXY [pixel]

            if verbose:
                logger.info(
                    f"Full Size: {full_size} PartialSize: {partial_size} Scaling: {scale_x:.3f} - {scale_y:.3f}"
                )

            stage_position = response.frame_data.frame_stage_position
            if stage_position.x is None or stage_position.y is None or stage_position.z is None:
                raise ValueError("Streaming frame has no stage position")
            stage_x = stage_position.x * 1e6  # StageX [m]
            stage_y = stage_position.y * 1e6  # StageY [m]
            stage_z = stage_position.z * 1e6  # StageZ [m]

            # Decode the byte stream using the caller's pixel type. Full-frame
            # mode uses frame_size; raw mode uses the payload rectangle size.
            image_size = partial_size if enable_raw_data else full_size
            stream2d = decode_frame(
                response.frame_data.pixel_data.raw_data,
                dtype,
                image_size.width,
                image_size.height,
            )

            num_objects = 0

            # Each received frame replaces the previous display immediately;
            # this simple example intentionally does not buffer frames.
            self.imageView.setImage(stream2d, autoHistogramRange=True)

            # show pixel stream metadata
            logger.info(
                f"S={scene} T={time} M={tile} Z={zplane} C={ch} - TL_XY [pixel]: {x} x {y} - XYZ [micron]: {stage_x:.3f} x {stage_y:.3f} x {stage_z:.3f} - Objects: {num_objects}"
            )

    async def read(
        self,
        dtype: np.dtype | None = None,
        channel_index: None | int = None,
        enable_raw_data: bool | None = False,
        verbose=False,
    ):

        # NumPy needs a concrete dtype to interpret the raw payload. uint8 is a
        # fallback only; callers should provide the experiment's actual type.
        if dtype is None:
            dtype = np.dtype(np.uint8)

        await self.do(dtype, channel_index, enable_raw_data, verbose)

    def closeEvent(self, event) -> None:
        """Cancel frame reception and close the streaming channel."""
        if self.stream_task is not None and not self.stream_task.done():
            self.stream_task.cancel()
        self.channel.close()
        super().closeEvent(event)


def main(
    configfile: Path | str,
    pixeltype: np.dtype[Any],
    czi_name: str,
    start_experiment_from_UI: bool,
    my_experiment: str,
    channel_index: int,
    enable_raw_data: bool = False,
):
    # Qt owns the GUI loop, while qasync lets the gRPC coroutines run on that
    # same loop without blocking window events.
    app = pg.Qt.QtWidgets.QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # The window opens the long-lived streaming channel and optionally starts
    # the experiment before the read coroutine is scheduled below.
    window = MainWindow(
        loop,
        configfile=configfile,
        my_experiment=my_experiment,
        start_experiment_from_UI=start_experiment_from_UI,
        czi_name=czi_name,
    )
    window.show()

    with loop:

        # Schedule frame reception instead of calling asyncio.run(), because
        # qasync is already the event-loop owner for this application.
        window.stream_task = asyncio.ensure_future(
            window.read(
                dtype=pixeltype,
                channel_index=channel_index,
                enable_raw_data=enable_raw_data,
                verbose=False,
            ),
            loop=loop,
        )

        # Keep the GUI and stream alive until the application is closed.
        loop.run_forever()


if __name__ == "__main__":

    # Resolve paths relative to this script so launching from another working
    # directory does not change which configuration file is loaded.
    script_dir = Path(__file__).parent

    # Select the ZEN API configuration file. Replace this with config.ini when
    # using the standard filename in the examples folder.
    # config_path = script_dir / "config.ini"
    config_path = script_dir / "my_config.ini"

    main(
        configfile=config_path,
        pixeltype=np.dtype(np.uint16),  # must match experiment output
        czi_name="Experiment48",
        start_experiment_from_UI=True,
        my_experiment="ZEN_API_Test_w96_1024x1024_CH=2",
        channel_index=0,
    )
