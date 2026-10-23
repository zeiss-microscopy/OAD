#################################################################
# File        : zenapi_streaming.py
# Institution : Carl Zeiss Microscopy GmbH
#
# The script demos the usage of the ZEN-API for streaming.
# The script starts an experiment and will display the pixel data using PyQtGraph.
# Frame dimensions are read from each streamed response. The example can also
# apply online processing to demonstrate that workflow.
#
# Copyright(c) 2026 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import importlib
import os
import time

# PyQtGraph and ONNX Runtime can both load OpenMP. On Windows, loading more
# than one OpenMP runtime can cause startup errors, so allow the runtimes to
# coexist before importing either library.
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# qasync probes PyQt6 before PySide6, but this environment has an incomplete
# PyQt6 installation. Keep both Qt consumers on the working PySide6 backend.
os.environ.setdefault("PYQTGRAPH_QT_LIB", "PySide6")
os.environ.setdefault("QT_API", "pyside6")

try:
    # Import PyTorch first so it loads its native DLL dependencies before the
    # GUI and ONNX libraries are initialized.
    importlib.import_module("torch")
except ImportError:
    print(
        "PyTorch is not installed. Please make sure to install the required dependencies for semantic segmentation and denoising."
    )

import asyncio
import random
import sys
from enum import Enum, unique
from pathlib import Path

import numpy as np
import pyqtgraph as pg
import qasync

# import the auto-generated python modules for ZEN API
from czmodel import ModelMetadata
from czmodel.core.util._extract_model import extract_czann_model
from onnx_inference import OnnxInferencer
from processing_tools import ArrayProcessor
from pyqtgraph.imageview import ImageView
from zen_api.acquisition.v1beta import (
    ExperimentServiceGetAvailableExperimentsRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceLoadRequest,
    ExperimentServiceStartExperimentRequest,
    ExperimentServiceStub,
    ExperimentStreamingServiceMonitorAllExperimentsRequest,
    ExperimentStreamingServiceMonitorExperimentRequest,
    ExperimentStreamingServiceStub,
)
from zen_api_utils.misc import initialize_zenapi, set_logging

# ZEN frames arrive as row-major (height, width) arrays. Selecting the matching
# PyQtGraph axis order avoids rotating or transposing every incoming frame.
# This preserves the intended display orientation without an extra copy.
pg.setConfigOption("imageAxisOrder", "row-major")

logger = set_logging()


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
    """Start an experiment through the ZEN API and return its experiment ID.

    This helper owns a short-lived gRPC channel used only for experiment
    startup. The pixel stream uses a separate channel owned by ``MainWindow``.

    Args:
        exp_name: Name of the experiment without the ``.czexp`` extension.
        czi_name: Desired name of the CZI image to be written.
        overwrite: Whether an existing CZI file may be replaced.
        verbose: Whether to log available experiments.
        configfile: Path to the ZEN API configuration file.

    Returns:
        The reference ID of the loaded experiment.
    """
    channel = None
    try:
        # Create the authenticated gRPC channel and metadata required by the
        # generated ZEN API client stubs.
        channel, metadata = initialize_zenapi(configfile)
        exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

        # Query the ZEN Core default experiment folder. A typical location is
        # ``...\Documents\Carl Zeiss\ZENCore\Documents\Experiment Setups``.
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

        output_path = Path(save_path.image_output_path) / (czi_name + ".czi")
        if output_path.exists():
            if overwrite:
                output_path.unlink()
                logger.info("Overwrite CZI file: " + czi_name + ".czi")
            else:
                raise FileExistsError("CZI file: " + czi_name + ".czi cannot be overwritten")

        logger.info("Starting Experiment Execution ...")
        await exp_service.start_experiment(
            ExperimentServiceStartExperimentRequest(experiment_id=my_exp.experiment_id, output_name=czi_name)
        )
        return my_exp.experiment_id
    except (FileExistsError, FileNotFoundError, KeyError, OSError, ValueError) as e:
        logger.error(f"Failed to initialize ZEN API with config file '{configfile}': {e}")
        raise
    finally:
        if channel is not None:
            channel.close()


class MainWindow(pg.Qt.QtWidgets.QMainWindow):
    def __init__(
        self,
        loop=None,
        configfile: Path | str = "config.ini",
        start_experiment_from_UI: bool = True,
        my_experiment: str = "my_exp.czexp",
        czi_name: str = "my_image.czi",
        auto_histogram_range: bool = False,
        logging_interval_seconds: float = 1.0,
        display_interval_seconds: float = 0.1,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        del loop, my_experiment, czi_name

        if logging_interval_seconds < 0:
            raise ValueError("logging_interval_seconds must be non-negative")
        if display_interval_seconds <= 0:
            raise ValueError("display_interval_seconds must be positive")

        # Keep display and logging settings on the window so the stream loop
        # can receive frames independently from the GUI refresh rate.
        self.auto_histogram_range = auto_histogram_range
        self.logging_interval_seconds = logging_interval_seconds
        self.display_interval_seconds = display_interval_seconds
        self._last_log_time = 0.0
        self._image_initialized = False
        self._pending_display: tuple[np.ndarray, object | None, bool] | None = None
        self._rois: list[pg.ROI] = []
        self.imageView = ImageView()
        self.setWindowTitle("ZEN-API Pixel Stream")
        self.setCentralWidget(self.imageView)
        self.pen = pg.Qt.QtGui.QPen()
        self.pen.setWidthF(0.05)  # set bounding box width

        # Render at a stable wall-clock rate. The receive loop replaces the
        # pending frame, so a fast stream cannot build an unbounded GUI queue.
        self.display_timer = pg.Qt.QtCore.QTimer(self)
        self.display_timer.setInterval(max(1, round(display_interval_seconds * 1000)))
        self.display_timer.timeout.connect(self._display_pending_frame)
        self.display_timer.start()

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

        self.start_experiment_from_UI = start_experiment_from_UI
        self.expID: str | None = None
        self.stream_task: asyncio.Task | None = None

    def queue_display(self, image: np.ndarray, props=None, update_boxes: bool = True) -> None:
        """Keep only the newest frame for the next scheduled GUI refresh."""
        self._pending_display = (image, props, update_boxes)

    def _display_pending_frame(self) -> None:
        """Render the newest queued frame without blocking frame reception."""
        if self._pending_display is None:
            return

        image, props, update_boxes = self._pending_display
        self._pending_display = None
        self.update_image(image)
        if update_boxes:
            self.update_bounding_boxes(props)

    async def start_experiment_if_needed(self, my_experiment: str, czi_name: str, configfile: Path | str) -> None:
        """Start the experiment when API-controlled startup is enabled.

        When ZEN starts the experiment from its UI, this method deliberately
        does nothing. Otherwise it is awaited on the qasync loop so startup
        does not block Qt event processing.
        """
        if self.start_experiment_from_UI:
            return

        logger.info(f"Starting Experiment via ZEN API: {my_experiment}")
        self.expID = await start_experiment(
            exp_name=my_experiment,
            czi_name=czi_name,
            overwrite=True,
            verbose=False,
            configfile=str(configfile),
        )
        logger.info(f"Experiment ID: {self.expID}")

    def update_image(self, image: np.ndarray) -> None:
        """Display one frame using the configured histogram strategy.

        The first frame chooses useful display levels. By default, later
        frames update only the pixels, avoiding per-frame histogram work. Set
        ``auto_histogram_range`` to true when intensity ranges change often.
        """
        if not self._image_initialized or self.auto_histogram_range:
            self.imageView.setImage(image, autoHistogramRange=self.auto_histogram_range)
            self._image_initialized = True
        else:
            self.imageView.imageItem.setImage(image, autoLevels=False)

    def update_bounding_boxes(self, props) -> None:
        """Update rectangle overlays from ``regionprops`` measurements.

        Regionprops uses ``(min_row, min_col, max_row, max_col)`` while
        PyQtGraph uses ``(x, y)`` and ``(width, height)``. Therefore columns
        become x/width and rows become y/height. Existing ROIs are reused so
        graphics items are not created and destroyed for every frame.
        """
        view = self.imageView.getView()
        rows = list(props.iterrows()) if props is not None else []

        # Remove stale overlays when the current frame has fewer objects.
        while len(self._rois) > len(rows):
            view.removeItem(self._rois.pop())

        for index, (_, row) in enumerate(rows):
            # Create a new overlay only when a newly detected object needs one.
            if index == len(self._rois):
                roi = pg.ROI(
                    [0, 0],
                    pg.Point(1, 1),
                    removable=True,
                    resizable=False,
                    movable=False,
                )
                self._rois.append(roi)
                view.addItem(roi)

            roi = self._rois[index]

            # Convert row/column measurements to the x/y coordinate system of
            # the PyQtGraph view.
            roi.setPos([row["bbox-1"], row["bbox-0"]])
            roi.setSize(
                [
                    row["bbox-3"] - row["bbox-1"],
                    row["bbox-2"] - row["bbox-0"],
                ]
            )

            self.pen.setColor(
                pg.Qt.QtGui.QColor(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
            )
            roi.setPen(self.pen)

    def closeEvent(self, a0) -> None:
        """Cancel asynchronous work and close the streaming gRPC channel.

        Qt calls this method when the user closes the window. Cancelling the
        task prevents the stream from continuing after the view is disposed.
        """
        if self.stream_task is not None and not self.stream_task.done():
            self.stream_task.cancel()
        self.display_timer.stop()
        self.channel.close()
        super().closeEvent(a0)

    async def read(
        self,
        processing: Processing = Processing.NO_PROCESSING,
        dtype: np.dtype | None = None,
        threshold: int | None = 0,
        inferencer: OnnxInferencer | None = None,
        model_metadata: ModelMetadata | None = None,
        channel_index: int | None = None,
        enable_raw_data: bool = False,
        draw_bbox: bool = True,
        measure_properties: tuple | None = None,
        verbose=False,
    ):
        """
        Reads and processes frames from the streaming service.

        Args:
            processing (Processing): The type of processing to apply to the frames.
            dtype (np.dtype | None): The data type of the frames; defaults to uint8.
            threshold (Optional[int]): The threshold value for segmentation.
            inferencer (Optional[OnnxInferencer]): The inferencer for semantic segmentation.
            model_metadata (Optional[ModelMetadata]): The metadata of the model.
            channel_index (Optional[Union[None, int]]): The index of the channel.
            enable_raw_data: Read partial frames or scan lines when true;
                read assembled full frames when false.
            draw_bbox (Optional[bool]): Whether to draw bounding boxes around detected objects.
            verbose (bool): show additional outputs for testing purposes

        Returns:
            None
        """

        # NumPy needs a concrete dtype to calculate the expected byte count and
        # interpret the raw payload. uint8 is the fallback for callers that do
        # not provide the experiment's actual pixel type.
        if dtype is None:
            dtype = np.dtype(np.uint8)

        # Choose the server-streaming RPC. UI-controlled startup monitors all
        # running experiments; API-controlled startup monitors self.expID.
        # channel_index optionally filters the stream to one acquisition
        # channel, while None means that no channel filter is applied.
        if self.start_experiment_from_UI:
            async_iterable = self.streaming_service.monitor_all_experiments(
                ExperimentStreamingServiceMonitorAllExperimentsRequest(
                    channel_index=channel_index, enable_raw_data=enable_raw_data
                )
            )
            logger.info("Getting PixelStream from Experiment started from UI")

        if not self.start_experiment_from_UI:
            if self.expID is None:
                raise RuntimeError("The experiment must be started before monitoring its pixel stream")
            async_iterable = self.streaming_service.monitor_experiment(
                ExperimentStreamingServiceMonitorExperimentRequest(
                    experiment_id=self.expID,
                    channel_index=channel_index,
                    enable_raw_data=enable_raw_data,
                )
            )
            logger.info("Getting PixelStream from Experiment started by ZEN API")

        async for response in async_iterable:
            # A monotonic clock is used for throttling because it is not
            # affected when the computer's wall clock changes.
            now = time.monotonic()
            should_log = self.logging_interval_seconds == 0 or (
                now - self._last_log_time >= self.logging_interval_seconds
            )
            if should_log:
                self._last_log_time = now
                logger.info(
                    f"Received frame {response.frame_data.frame_number}: "
                    f"pixel_type={response.frame_data.pixel_data.pixel_type.name}, "
                    f"bytes={len(response.frame_data.pixel_data.raw_data)}"
                )

            # Read the acquisition metadata before processing so log messages
            # describe the same frame that is displayed below.
            time_index = response.frame_data.frame_position.t  # time index
            zplane = response.frame_data.frame_position.z  # zplane index
            tile = response.frame_data.frame_position.m  # tile index
            ch = response.frame_data.frame_position.c  # channel index
            scene = response.frame_data.frame_position.s  # scene index
            x = response.frame_data.frame_position.x  # xpos top-left [pixel]
            y = response.frame_data.frame_position.y  # ypos top-left [pixel]
            full_size = response.frame_data.frame_size  # full frame sizeXY [pixel]
            scale_x = response.frame_data.scaling.x * 1e6
            scale_y = response.frame_data.scaling.y * 1e6

            # pixel_data.size describes the payload rectangle. For a normal
            # full-frame acquisition it equals full_size; for raw or partial
            # streaming it may describe only one part of the full image.

            partial_size = response.frame_data.pixel_data.size  # partial frame sizeXY [pixel]

            if verbose and should_log:
                logger.info(
                    f"Full Size: {full_size} PartialSize: {partial_size} Scaling: {scale_x:.3f} - {scale_y:.3f}"
                )

            stage_position = response.frame_data.frame_stage_position
            stage_x_value = stage_position.x
            stage_y_value = stage_position.y
            stage_z_value = stage_position.z
            stage_x = 0.0 if stage_x_value is None else stage_x_value * 1e6  # StageX [m]
            stage_y = 0.0 if stage_y_value is None else stage_y_value * 1e6  # StageY [m]
            stage_z = 0.0 if stage_z_value is None else stage_z_value * 1e6  # StageZ [m]

            # Convert the byte stream into a 2D NumPy view without copying it.
            # Validate the byte count first so a truncated or mismatched ZEN
            # payload produces a useful error instead of a reshape exception.
            image_size = partial_size if enable_raw_data else full_size
            expected_bytes = image_size.height * image_size.width * dtype.itemsize
            raw_data = response.frame_data.pixel_data.raw_data
            if len(raw_data) != expected_bytes:
                raise ValueError(
                    f"Pixel payload has {len(raw_data)} bytes; expected {expected_bytes} "
                    f"for {image_size.width}x{image_size.height} {dtype}"
                )
            stream2d = np.frombuffer(raw_data, dtype=dtype).reshape((image_size.height, image_size.width))

            num_objects = 0

            # Processing is optional. NO_PROCESSING displays the decoded frame;
            # the other modes use ArrayProcessor and may update ROIs.
            if processing is not Processing.NO_PROCESSING:

                # ArrayProcessor operates on one decoded 2D frame at a time.
                ap = ArrayProcessor(stream2d)

                # Otsu chooses a threshold automatically from the image
                # histogram, which is useful when illumination varies.
                if processing is Processing.SEG_THRESHOLD_OTSU:

                    pro2d = ap.apply_otsu_threshold()

                # Manual thresholding uses the value supplied to read().
                if processing is Processing.SEG_THRESHOLD_MANUAL:

                    pro2d = ap.apply_threshold(value=threshold if threshold is not None else 0, invert_result=False)

                # Semantic segmentation uses a model supplied by the caller.
                # Metadata describes the model input shape; the inferencer
                # performs the actual prediction.
                if processing is Processing.SEG_SEMANTIC:

                    # Tile-based inference is not implemented yet, so the
                    # model currently receives the complete streamed frame.
                    if model_metadata is None:
                        raise ValueError("model_metadata is required for semantic segmentation")
                    if inferencer is None:
                        raise ValueError("inferencer is required for semantic segmentation")
                    pro2d = ap.apply_semantic_seg(
                        inferencer=inferencer,
                        input_shape=model_metadata.input_shape,
                        class_index=2,
                        use_gpu=True,
                    )

                # Segmentation creates a mask. Label connected objects in the
                # mask, calculate measurements, and draw their bounding boxes.
                if (
                    processing is Processing.SEG_THRESHOLD_OTSU
                    or processing is Processing.SEG_THRESHOLD_MANUAL
                    or processing is Processing.SEG_SEMANTIC
                ):
                    ap = ArrayProcessor(pro2d)
                    pro2d, num_objects, props = ap.label_objects(
                        max_size_remove=100,
                        label_rgb=False,
                        orig_image=None,
                        bg_label=0,
                        measure_params=True,
                        measure_properties=measure_properties,
                    )

                    self.queue_display(stream2d, props if draw_bbox else None)

                # Regression models such as Noise2Void produce a denoised
                # image rather than an object-label mask.
                if processing is Processing.DENOISE:

                    if model_metadata is None:
                        raise ValueError("model_metadata is required for denoising")
                    if inferencer is None:
                        raise ValueError("inferencer is required for denoising")
                    pro2d = ap.apply_regression(
                        inferencer=inferencer,
                        input_shape=model_metadata.input_shape,
                        use_gpu=True,
                    )

                    # Display the model output instead of the original frame.
                    self.queue_display(pro2d, update_boxes=False)

            if processing is Processing.NO_PROCESSING:

                # Display the original decoded frame and clear any overlays
                # left by a previous processed frame.
                self.queue_display(stream2d)

            # Log acquisition metadata at the same throttled interval as the
            # frame-received message so a high-rate stream remains readable.
            if should_log:
                logger.info(
                    f"S={scene} T={time_index} M={tile} Z={zplane} C={ch} - TL_XY [pixel]: {x} x {y} - XYZ [micron]: {stage_x:.3f} x {stage_y:.3f} x {stage_z:.3f} - Objects: {num_objects}"
                )


def main(
    configfile: Path | str,
    pixeltype: np.dtype,
    czi_name: str,
    start_experiment_from_UI: bool,
    my_experiment: str,
    channel_index: int | None,
    processing: Processing,
    threshold: int,
    czann_filepath: str,
    enable_raw_data: bool = False,
    auto_histogram_range: bool = False,
    logging_interval_seconds: float = 1.0,
    display_interval_seconds: float = 1 / 30,
):

    # These values are populated only for model-based processing modes. The
    # simpler threshold and display modes do not need model setup.
    inferencer = None
    clean_models = False
    measure_properties = ("label", "area", "centroid", "bbox")

    # Qt owns the GUI event loop. qasync adapts that loop so Qt events and
    # asynchronous gRPC operations can run together in one thread.
    app = pg.Qt.QtWidgets.QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Create the window before starting the stream so it is ready for the first
    # frame as soon as the asynchronous task begins.
    window = MainWindow(
        loop,
        configfile=configfile,
        my_experiment=my_experiment,
        start_experiment_from_UI=start_experiment_from_UI,
        czi_name=czi_name,
        auto_histogram_range=auto_histogram_range,
        logging_interval_seconds=logging_interval_seconds,
        display_interval_seconds=display_interval_seconds,
    )
    window.show()
    app.aboutToQuit.connect(loop.stop)

    if processing is Processing.SEG_SEMANTIC or processing is Processing.DENOISE:
        # Model-based modes require optional packages. Fail early with an
        # actionable message when those packages are not installed.
        if extract_czann_model is None or OnnxInferencer is None:
            raise ImportError(
                "czmodel and onnx_inference packages are required for SEG_SEMANTIC and DENOISE processing. "
                "Please install the required dependencies."
            )

        # Unpack the CZANN once. Its metadata describes the model and the
        # extracted path is used to initialize one reusable ONNX session.
        model_metadata, model_path = extract_czann_model(
            path=czann_filepath,
            target_dir=Path.cwd() / os.path.dirname(czann_filepath),
        )
        model_path = Path(model_path)

        logger.info(f"Model Path: {model_path}")
        logger.info(f"Model Name: {model_metadata.model_name}")
        logger.info(f"Model Type: {model_metadata.model_type}")
        logger.info(f"Model Input Shape: {model_metadata.input_shape}")
        logger.info(f"Model Output Shape: {model_metadata.output_shape}")
        logger.info(f"Overlap Tile Size: {model_metadata.min_overlap}")

        # Reuse one inferencer for every frame. Creating a new ONNX session per
        # frame would be much slower and would repeatedly allocate resources.
        inferencer = OnnxInferencer(str(model_path))
        logger.info("Started ONNXInferencer Session.")

        # Delete temporary extracted files during final cleanup. Set this to
        # False while debugging if the extracted files need to be inspected.
        clean_models = True
    else:
        model_metadata = None

    with loop:

        async def start_and_read() -> None:
            # Start the experiment first when requested, then begin monitoring
            # its pixel stream. Both operations run on the same event loop.
            await window.start_experiment_if_needed(my_experiment, czi_name, configfile)
            await window.read(
                processing=processing,
                dtype=pixeltype,
                threshold=threshold,
                inferencer=inferencer,
                model_metadata=model_metadata,
                channel_index=channel_index,
                enable_raw_data=enable_raw_data,
                measure_properties=measure_properties,
                verbose=False,
            )

        # Schedule the coroutine instead of calling asyncio.run(): the qasync
        # loop is already responsible for both the Qt window and this task.
        window.stream_task = asyncio.ensure_future(start_and_read(), loop=loop)

        def report_stream_failure(task: asyncio.Future) -> None:
            # Cancellation is expected during normal window shutdown and is
            # not an application failure worth logging.
            if task.cancelled():
                return
            exception = task.exception()
            if exception is not None:
                logger.error(f"Pixel stream stopped: {exception!r}")

        window.stream_task.add_done_callback(report_stream_failure)

        try:
            loop.run_forever()
        finally:
            # Remove files extracted from the CZANN. Keeping this in finally
            # ensures cleanup happens after an exception or normal window
            # closing.
            if clean_models:
                if model_path.exists():
                    model_path.unlink()
                    logger.info(f"Deleted extracted model file: {model_path}")
                model_json = model_path.parent / "model.json"
                if model_json.exists():
                    model_json.unlink()
                    logger.info(f"Deleted extracted model metadata: {model_json}")


if __name__ == "__main__":

    # Select the online processing mode for this example run. Change this to
    # NO_PROCESSING or SEG_THRESHOLD_OTSU to try the other built-in paths.
    # processing = Processing.NO_PROCESSING
    processing = Processing.SEG_THRESHOLD_MANUAL
    # processing = Processing.SEG_THRESHOLD_OTSU

    # The model-based modes require the matching CZANN file and an environment
    # containing PyTorch, ONNX Runtime, czmodel, and onnx_inference.
    # processing = Processing.SEG_SEMANTIC  # --> cyto2022_nuc2.czann
    # processing = Processing.DENOISE  # --> LiveDenoise_DAPI.czann

    # Resolve paths relative to this script so the example can be launched from
    # a different working directory.
    script_dir = Path(__file__).parent

    # Select the ZEN API configuration file. Replace this with config.ini when
    # using the standard filename in the examples folder.
    # config_path = script_dir / "config.ini"
    config_path = script_dir / "my_config.ini"

    # The CZANN path is used only for SEG_SEMANTIC and DENOISE. It is still
    # supplied here because main() keeps one consistent configuration shape.
    # czann_filepath = r"F:\GitHub\OAD\ZEN-API\python_examples\ai_models\cyto2022_nuc2.czann" # --> frame 1014 x 1024 AcqRoi
    czann_filepath = os.path.join(
        "python_examples", "ai_models", "LiveDenoise_DAPI.czann"
    )  # --> 512 x 512 pixel AcqROI

    main(
        configfile=config_path,
        pixeltype=np.dtype(np.uint16),  # must match experiment output
        czi_name="zenapi_test",
        start_experiment_from_UI=True,
        my_experiment="00_ZEN_API_Streaming_Test",  # only relevant if start_experiment_from_UI=False
        channel_index=0,
        processing=processing,
        threshold=850,
        czann_filepath=czann_filepath,
        display_interval_seconds=0.3,
        logging_interval_seconds=0.3,
    )
