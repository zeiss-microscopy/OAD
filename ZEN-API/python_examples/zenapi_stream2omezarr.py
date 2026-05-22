# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_stream2omezarr.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# Stream pixel data from ZEN via the ZEN-API gateway directly
# into an OME-ZARR file using the ome-writers library.
#
# Two modes of operation:
#   1) CLI mode (--experiment): Dimensions are discovered from the
#      pixel stream. All frames are buffered in memory, then written.
#   2) Config mode (--experiment-config): Dimensions are read from
#      an INI file. Frames are written on-the-fly (no buffering).
#
# In both modes the experiment can be started from the script
# (--start-experiment) or from the ZEN UI (--no-start-experiment).
# In config mode, --start-experiment / --no-start-experiment
# overrides the INI 'start_from_script' setting.
#
# Use --viewer ndv or --viewer napari to launch a viewer after acquisition.
#
# Usage:
#   python zenapi_stream2omezarr.py --help
#
# Examples:
#
#   --- Config mode (recommended for production) ---
#   Dimensions are read from an INI file so frames are written on-the-fly.
#
#   # Use INI defaults (start_from_script is read from the INI):
#   python zenapi_stream2omezarr.py --experiment-config experiment_streaming_config.ini
#
#   # Override INI: wait for user to start experiment from ZEN UI:
#   python zenapi_stream2omezarr.py --experiment-config experiment_streaming_config.ini --no-start-experiment
#
#   # Override INI: force experiment start from script:
#   python zenapi_stream2omezarr.py --experiment-config experiment_streaming_config.ini --start-experiment
#
#   # Config mode + open result in ndv viewer:
#   python zenapi_stream2omezarr.py --experiment-config experiment_streaming_config.ini --viewer ndv
#
#   --- CLI mode (quick experiments, no INI needed) ---
#   Dimensions are discovered from the stream; all frames buffered, then written.
#
#   # Start experiment from ZEN UI, save OME-ZARR to ./output:
#   python zenapi_stream2omezarr.py --experiment MyExp --output-dir ./output
#
#   # Start experiment from script, custom CZI name, 8-bit data:
#   python zenapi_stream2omezarr.py --experiment MyExp --output-dir ./output \
#       --start-experiment --czi-name my_acquisition --dtype uint8
#
#   # Stream only channel 0, use lz4 compression, view in napari:
#   python zenapi_stream2omezarr.py --experiment MyExp --output-dir ./output \
#       --channel-index 0 --compression blosc-lz4 --viewer napari
#
#   # Use a custom ZEN-API gateway config:
#   python zenapi_stream2omezarr.py --experiment MyExp --output-dir ./output \
#       --zenapi-config /path/to/my_config.ini
#
# Copyright(c) 2026 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import argparse
import asyncio
import contextlib
import itertools
import numpy as np
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from zen_api_utils.misc import initialize_zenapi, set_logging
from zen_api_utils.zen_omezarr import (
    ExperimentConfig,
    build_progress_bar,
    load_experiment_config,
    open_in_napari_viewer,
    open_in_ndv_viewer,
    start_experiment,
)

# ZEN API auto-generated stubs
from zen_api.acquisition.v1beta import (
    ExperimentServiceRegisterOnStatusChangedRequest,
    ExperimentServiceStub,
    ExperimentStreamingServiceStub,
    ExperimentStreamingServiceMonitorAllExperimentsRequest,
)

# ome-writers
from ome_writers import AcquisitionSettings, Dimension, Position, create_stream

logger = set_logging()

# Default data type for pixel streaming
DEFAULT_DTYPE = np.dtype(np.uint16)

# Inactivity timeout (seconds) – for the status-poll loop.
_STATUS_POLL_TIMEOUT: float = 30.0


async def _monitor_status_until_done(
    zenapi_config: str | Path,
    exp_id: str,
    stop_event: asyncio.Event,
    timeout: float = _STATUS_POLL_TIMEOUT,
) -> None:
    """Monitor ZEN experiment status and set stop_event when finished.

    Connects to the ZEN ExperimentService and streams status updates via
    ``register_on_status_changed``.  Sets ``stop_event`` as soon as
    ``is_experiment_running`` becomes False, or when no status update
    arrives within ``timeout`` seconds.

    Args:
        zenapi_config: Path to the ZEN-API gateway config.ini.
        exp_id: Experiment ID returned by ``start_experiment()``.
        stop_event: Shared event; set when the experiment is done.
        timeout: Seconds to wait for each status update before giving up.
    """
    # Use a dedicated gRPC channel so the status monitor does not
    # contend with the pixel-streaming channel for bandwidth.
    channel, metadata = initialize_zenapi(zenapi_config)
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)
    # register_on_status_changed returns an async generator that yields one
    # message each time ZEN updates the experiment state (acquisition
    # started, T/C/Z index advanced, finished, etc.).
    status_stream = exp_service.register_on_status_changed(ExperimentServiceRegisterOnStatusChangedRequest(exp_id))
    try:
        while not stop_event.is_set():
            # wait_for raises TimeoutError if ZEN goes silent for `timeout`
            # seconds, which is treated as "experiment must be done".
            response = await asyncio.wait_for(status_stream.__anext__(), timeout=timeout)
            if not response.status.is_experiment_running:
                logger.info("Experiment finished - status monitor signalling stop.")
                stop_event.set()
                break
            logger.debug(
                "Experiment status: "
                f"acq={response.status.is_acquisition_running} "
                f"T={response.status.time_points_index} "
                f"C={response.status.channels_index} "
                f"Z={response.status.zstack_slices_index}"
            )
    except asyncio.TimeoutError:
        logger.warning(f"Status monitor: no update for {timeout:.0f}s" " - assuming experiment finished.")
        stop_event.set()
    except StopAsyncIteration:
        logger.info("Status stream closed - experiment finished.")
        stop_event.set()
    except asyncio.CancelledError:
        # Task was cancelled by the caller during cleanup; exit silently.
        pass
    finally:
        channel.close()


async def stream_to_omezarr(
    zenapi_config: str | Path,
    experiment_name: str,
    output_dir: str | Path,
    dtype: np.dtype | None = None,
    start_experiment_from_script: bool = False,
    czi_name: str = "zenapi_stream",
    overwrite_czi: bool = True,
    channel_index: int | None = None,
    overwrite_zarr: bool = True,
    compression: str | None = "blosc-zstd",
    inactivity_timeout: float = _STATUS_POLL_TIMEOUT,
) -> Path:
    """Stream ZEN pixel data into an OME-ZARR file.

    Args:
        zenapi_config: Path to the ZEN-API gateway config.ini.
        experiment_name: ZEN experiment name (without .czexp).
        output_dir: Folder where the OME-ZARR will be created.
        dtype: Pixel data type (must match the experiment output).
        start_experiment_from_script: If True, start the experiment via API.
            If False, the user starts the experiment from the ZEN UI.
        czi_name: CZI output name when starting experiment from script.
        overwrite_czi: Allow overwriting an existing CZI.
        channel_index: Optional channel filter index (None = all channels).
        overwrite_zarr: Overwrite an existing OME-ZARR at the output path.
        compression: Compression for ZARR
            ('blosc-zstd', 'blosc-lz4', 'zstd', 'none', or None).
        inactivity_timeout: Seconds without a new frame before the stream
            is considered finished.  Also used as the status-poll window
            when an experiment_id is available.

    Returns:
        Path to the created OME-ZARR directory.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # derive OME-ZARR name from experiment + timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zarr_name = f"{experiment_name}_{timestamp}.ome.zarr"
    zarr_path = output_dir / zarr_name
    logger.info(f"OME-ZARR output path: {zarr_path}")

    # ----- connect to ZEN-API streaming service -----
    channel, metadata = initialize_zenapi(zenapi_config)
    streaming_service = ExperimentStreamingServiceStub(channel=channel, metadata=metadata)

    # ----- open the pixel stream FIRST (before starting the experiment) -----
    # Opening before triggering the experiment ensures no early frames are
    # dropped.  monitor_all_experiments is a perpetual gRPC server-streaming
    # call – the server pushes frames as soon as they are produced.
    async_iterable = streaming_service.monitor_all_experiments(
        ExperimentStreamingServiceMonitorAllExperimentsRequest(
            channel_index=channel_index,
            enable_raw_data=False,
        )
    )
    logger.info("Pixel stream opened (monitoring all experiments).")

    # ----- now optionally start the experiment -----
    # stop_event is shared between this coroutine and the status-monitor
    # task below.  The monitor sets it when ZEN reports the experiment
    # has finished, which breaks the frame-receive loop.
    stop_event = asyncio.Event()
    _status_task: asyncio.Task | None = None

    if start_experiment_from_script:
        logger.info(f"Starting experiment '{experiment_name}' via ZEN-API ...")
        exp_id, czi_path = await start_experiment(
            exp_name=experiment_name,
            czi_name=czi_name,
            overwrite=overwrite_czi,
            zenapi_config=zenapi_config,
        )
        logger.info(f"Experiment ID: {exp_id}")
        logger.info(f"CZI file will be saved to: {czi_path}")
        # Spawn a concurrent task that polls ZEN's status stream and sets
        # stop_event when is_experiment_running becomes False.  This gives
        # a reliable termination signal alongside the inactivity timeout.
        _status_task = asyncio.create_task(
            _monitor_status_until_done(zenapi_config, exp_id, stop_event, inactivity_timeout)
        )
    else:
        logger.info(
            "Waiting for experiment to be started from ZEN UI. "
            f"Stream stops after {inactivity_timeout:.0f}s of inactivity."
        )

    # ----- collect frames & metadata in first pass to build dimensions -----
    # We need to know the full extent of the acquisition before we can
    # create the AcquisitionSettings.  We accumulate all frames in memory,
    # track the coordinate ranges, then write them out.
    #
    # For very large acquisitions a two-pass approach (peek first frame for
    # size, assume bounded dims from experiment metadata) would be better,
    # but ZEN API does not currently expose the full experiment shape upfront.

    frames: list[np.ndarray] = []
    frame_coords: list[dict] = []  # list of {t, z, c, m, s} per frame
    frame_metadata_list: list[dict] = []

    # track dimension extents
    max_t = 0
    max_z = 0
    max_c = 0
    max_m = 0  # tiles
    max_s = 0  # scenes

    frame_height: int | None = None
    frame_width: int | None = None
    scale_x: float | None = None
    scale_y: float | None = None

    frame_count = 0

    logger.info("Receiving pixel stream ...")

    # We iterate the gRPC stream manually (via __aiter__ + __anext__)
    # instead of `async for` so we can wrap each step in wait_for() to
    # detect inactivity (no frame for `inactivity_timeout` seconds) and
    # react to stop_event set by the concurrent status-monitor task.
    async_iter = async_iterable.__aiter__()
    while not stop_event.is_set():
        try:
            response = await asyncio.wait_for(async_iter.__anext__(), timeout=inactivity_timeout)
        except asyncio.TimeoutError:
            logger.info(f"No frames for {inactivity_timeout:.0f}s" " - assuming experiment finished.")
            break
        except StopAsyncIteration:
            break

        fd = response.frame_data
        fp = fd.frame_position

        # Extract 5-D acquisition coordinate of this frame.
        t = fp.t
        z = fp.z
        c = fp.c
        m = fp.m  # tile index
        s = fp.s  # scene index

        full_size = fd.frame_size
        # ZEN API reports scaling in metres; convert to µm for OME metadata.
        sx = fd.scaling.x * 1e6  # m -> µm
        sy = fd.scaling.y * 1e6

        # Stage positions also in metres -> µm.
        # type: ignore[operator]: stubs declare float | None but values are
        # always numeric during an active acquisition.
        stage_x = fd.frame_stage_position.x * 1e6  # type: ignore[operator]
        stage_y = fd.frame_stage_position.y * 1e6  # type: ignore[operator]
        stage_z = fd.frame_stage_position.z * 1e6  # type: ignore[operator]

        # pixel_data.raw_data is a flat bytes buffer; reshape to (H, W).
        frame = np.frombuffer(fd.pixel_data.raw_data, dtype=dtype).reshape((full_size.height, full_size.width))

        # ZEN streams frames in a rotated/flipped orientation relative to
        # the physical stage.  Apply the same fix as the legacy
        # zenapi_streaming.py reference implementation.
        frame = np.flipud(np.rot90(frame))
        # Ensure C-contiguous memory layout for efficient downstream writes.
        frame = np.ascontiguousarray(frame, dtype=dtype)

        # Accumulate frames and coordinates for the second-pass write.
        frames.append(frame)
        frame_coords.append({"t": t, "z": z, "c": c, "m": m, "s": s})
        frame_metadata_list.append(
            {
                "position_x": stage_x,
                "position_y": stage_y,
                "position_z": stage_z,
            }
        )

        # Track the highest seen index in each dimension so we can infer
        # the full shape once the stream ends (max_index + 1 == count).
        max_t = max(max_t, t)
        max_z = max(max_z, z)
        max_c = max(max_c, c)
        max_m = max(max_m, m)
        max_s = max(max_s, s)

        # Capture pixel dimensions and physical scale from the first frame.
        if frame_height is None:
            frame_height = frame.shape[0]
            frame_width = frame.shape[1]
            scale_x = sx
            scale_y = sy

        frame_count += 1

        # progress
        sys.stdout.write(build_progress_bar(frame_count, None))
        sys.stdout.flush()

        if stop_event.is_set():
            logger.info("Stop event from status monitor – closing pixel stream.")
            break

    # newline after progress bar
    sys.stdout.write("\n")
    logger.info(f"Stream finished. Total frames received: {frame_count}")

    if frame_count == 0:
        logger.warning("No frames received. Nothing to write.")
        if _status_task is not None and not _status_task.done():
            _status_task.cancel()
            # Awaiting a cancelled task re-raises CancelledError; suppress it
            # so the caller receives a clean return rather than an exception.
            with contextlib.suppress(asyncio.CancelledError):
                await _status_task
        channel.close()
        return zarr_path

    # ----- build OME-ZARR dimensions from observed extents -----
    num_t = max_t + 1
    num_z = max_z + 1
    num_c = max_c + 1
    num_m = max_m + 1  # tile / position count
    num_s = max_s + 1  # scene count

    # Total positions = scenes * tiles
    num_positions = num_s * num_m

    # Build the dimension list
    dimensions: list[Dimension] = []

    if num_t > 1:
        dimensions.append(Dimension(name="t", count=num_t, chunk_size=1, type="time"))

    # positions (scenes x tiles)
    if num_positions > 1:
        pos_coords = []
        for s_idx in range(num_s):
            for m_idx in range(num_m):
                pos_coords.append(Position(name=f"S{s_idx}_M{m_idx}", grid_row=s_idx, grid_column=m_idx))
        dimensions.append(Dimension(name="p", type="position", coords=pos_coords))  # type: ignore[arg-type]

    if num_c > 1:
        dimensions.append(Dimension(name="c", count=num_c, chunk_size=1, type="channel"))

    if num_z > 1:
        # compute z_spacing from stage positions of the first Z-stack
        z_stage_positions: dict[int, float] = {}
        for fc, fmeta in zip(frame_coords, frame_metadata_list):
            z_idx = fc["z"]
            if z_idx not in z_stage_positions:
                z_stage_positions[z_idx] = fmeta["position_z"]
            if len(z_stage_positions) == num_z:
                break
        if len(z_stage_positions) >= 2:
            sorted_z = sorted(z_stage_positions.items())
            z_spacing = abs(sorted_z[1][1] - sorted_z[0][1])
            if z_spacing == 0:
                z_spacing = 1.0
        else:
            z_spacing = 1.0
        logger.info(f"Z spacing from stage positions: {z_spacing:.4f} µm")

        dimensions.append(
            Dimension(
                name="z",
                count=num_z,
                chunk_size=max(1, num_z),
                type="space",
                scale=z_spacing,
                unit="um",
            )
        )

    # Y and X (always present, must be last two).
    # frame_height/width are guaranteed non-None since frame_count > 0.
    assert frame_height is not None and frame_width is not None
    dimensions.append(
        Dimension(
            name="y",
            count=frame_height,
            chunk_size=min(512, frame_height),
            type="space",
            scale=scale_y,
            unit="um",
        )
    )
    dimensions.append(
        Dimension(
            name="x",
            count=frame_width,
            chunk_size=min(512, frame_width),
            type="space",
            scale=scale_x,
            unit="um",
        )
    )

    settings = AcquisitionSettings(
        root_path=str(zarr_path),
        dimensions=tuple(dimensions),
        dtype=str(dtype),
        format="ome-zarr",  # type: ignore[arg-type]  # ome-writers accepts str
        compression=compression,  # type: ignore[arg-type]  # ome-writers accepts str
        overwrite=overwrite_zarr,
    )

    logger.info(f"AcquisitionSettings created: shape={settings.shape}")
    total_expected = settings.num_frames
    logger.info(f"Total expected frames: {total_expected}")

    # ----- sort frames into acquisition order (t, p, c, z) -----
    # ome-writers expects frames in the order defined by the dimensions list.
    # Build a mapping from (t, s, m, c, z) -> frame index, then iterate in order.

    coord_to_idx: dict[tuple, int] = {}
    for idx, fc in enumerate(frame_coords):
        key = (fc["t"], fc["s"], fc["m"], fc["c"], fc["z"])
        coord_to_idx[key] = idx

    # ----- write to OME-ZARR -----
    # itertools.product generates (t, s, m, c, z) tuples in the same
    # T→S→M→C→Z order as the dimension list, so the stream receives
    # frames in the expected sequence.  For any missing frame we call
    # stream.skip() to keep the ZARR layout fully rectangular.
    logger.info(f"Writing {frame_count} frames to OME-ZARR ...")
    written = 0

    with create_stream(settings) as stream:
        coords = itertools.product(range(num_t), range(num_s), range(num_m), range(num_c), range(num_z))
        for t_idx, s_idx, m_idx, c_idx, z_idx in coords:
            key = (t_idx, s_idx, m_idx, c_idx, z_idx)
            if key in coord_to_idx:
                fidx = coord_to_idx[key]
                stream.append(
                    frames[fidx],
                    frame_metadata=frame_metadata_list[fidx],
                )
            else:
                # Frame was not received (dropped or filtered by
                # channel_index).  Emit a placeholder so the ZARR shape
                # remains rectangular.
                stream.skip(frames=1)
                logger.warning(f"Missing frame at " f"T={t_idx} S={s_idx} M={m_idx} C={c_idx} Z={z_idx}")

            written += 1
            sys.stdout.write(build_progress_bar(written, total_expected))
            sys.stdout.flush()

    sys.stdout.write("\n")
    logger.info(f"OME-ZARR written successfully: {zarr_path}")
    if _status_task is not None and not _status_task.done():
        _status_task.cancel()
        # Awaiting a cancelled task re-raises CancelledError; suppress it
        # so the caller receives a clean return rather than an exception.
        with contextlib.suppress(asyncio.CancelledError):
            await _status_task
    channel.close()
    return zarr_path


async def stream_to_omezarr_with_config(
    ecfg: ExperimentConfig,
    inactivity_timeout: float = _STATUS_POLL_TIMEOUT,
) -> Path:
    """Stream ZEN pixel data into OME-ZARR using known dimensions from config.

    Because the dimensions are known upfront the OME-ZARR stream is opened
    *before* frames arrive and each frame is written directly on-the-fly
    (no in-memory buffering of the full acquisition).

    Args:
        ecfg: Parsed ExperimentConfig.
        inactivity_timeout: Seconds to wait for the next frame before
            treating the acquisition as finished.

    Returns:
        Path to the created OME-ZARR directory.
    """
    dtype = np.dtype(ecfg.dtype)
    output_dir = Path(ecfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zarr_name = f"{ecfg.experiment_name}_{timestamp}.ome.zarr"
    zarr_path = output_dir / zarr_name
    logger.info(f"OME-ZARR output path: {zarr_path}")

    num_t = ecfg.time_points
    num_c = ecfg.channels
    num_z = ecfg.z_planes
    num_m = ecfg.tiles
    num_s = ecfg.scenes
    num_positions = num_s * num_m

    # ----- connect to ZEN-API streaming service -----
    channel, metadata = initialize_zenapi(ecfg.zenapi_config)
    streaming_service = ExperimentStreamingServiceStub(channel=channel, metadata=metadata)

    # ----- open the pixel stream FIRST (before starting the experiment) -----
    # This ensures no early frames are missed.  We always use
    # monitor_all_experiments here so the stream is ready before the
    # experiment_id exists.
    async_iterable = streaming_service.monitor_all_experiments(
        ExperimentStreamingServiceMonitorAllExperimentsRequest(
            channel_index=ecfg.channel_index,
            enable_raw_data=False,
        )
    )
    logger.info("Pixel stream opened (monitoring all experiments).")

    # ----- now optionally start the experiment -----
    if ecfg.start_from_script:
        logger.info(f"Starting experiment '{ecfg.experiment_name}' via ZEN-API ...")
        exp_id, czi_path = await start_experiment(
            exp_name=ecfg.experiment_name,
            czi_name=ecfg.czi_name,
            overwrite=ecfg.overwrite_czi,
            zenapi_config=ecfg.zenapi_config,
        )
        logger.info(f"Experiment ID: {exp_id}")
        logger.info(f"CZI file will be saved to: {czi_path}")
    else:
        logger.info(
            "Waiting for experiment to be started from ZEN UI. "
            f"Stream stops after {inactivity_timeout:.0f}s of inactivity."
        )

    # ----- Pre-compute the linear index for every (t, s, m, c, z) combination -----
    # Expected order: T -> P(S*M) -> C -> Z  (matching the dimensions list)
    coord_to_linear = {
        coord: idx
        for idx, coord in enumerate(
            itertools.product(range(num_t), range(num_s), range(num_m), range(num_c), range(num_z))
        )
    }

    # We receive frames in the order ZEN sends them which may differ from
    # the dimension iteration order above.  Buffer out-of-order frames in
    # a small look-ahead window and flush in-order as soon as possible.
    pending: dict[int, tuple[np.ndarray, dict]] = {}
    next_write = 0
    frame_count = 0

    # The OME-ZARR stream and settings are created lazily after the first
    # frame arrives (we need its size and pixel scaling).
    zarr_stream = None
    settings = None
    total_expected: int | None = None

    logger.info("Waiting for first frame to determine frame size ...")

    # We iterate the gRPC stream manually (via __aiter__ + __anext__)
    # instead of `async for` so we can wrap each step in wait_for() to
    # detect inactivity (no frame for `inactivity_timeout` seconds).
    # In config mode the total frame count is known upfront, so the
    # primary exit condition is frame_count >= total_expected.
    # Intentionally NO status-monitor stop_event here: ZEN delivers the
    # experiment-finished status *before* all pixel data has been pushed
    # through gRPC, so reacting to it would truncate the write.
    async_iter = async_iterable.__aiter__()
    while True:
        try:
            response = await asyncio.wait_for(async_iter.__anext__(), timeout=inactivity_timeout)
        except asyncio.TimeoutError:
            logger.info(f"No frames for {inactivity_timeout:.0f}s - assuming experiment finished.")
            break
        except StopAsyncIteration:
            break
        fd = response.frame_data
        fp = fd.frame_position

        t, z, c, m, s = fp.t, fp.z, fp.c, fp.m, fp.s

        full_size = fd.frame_size
        sx = fd.scaling.x * 1e6
        sy = fd.scaling.y * 1e6
        stage_x = fd.frame_stage_position.x * 1e6  # type: ignore[operator]  # ZEN API stubs type x/y/z as float | None
        stage_y = fd.frame_stage_position.y * 1e6  # type: ignore[operator]
        stage_z = fd.frame_stage_position.z * 1e6  # type: ignore[operator]

        frame = np.frombuffer(fd.pixel_data.raw_data, dtype=dtype).reshape((full_size.height, full_size.width))
        frame = np.flipud(np.rot90(frame))
        frame = np.ascontiguousarray(frame, dtype=dtype)

        frame_meta = {
            "position_x": stage_x,
            "position_y": stage_y,
            "position_z": stage_z,
        }

        # ----- on the very first frame, build the OME-ZARR settings & open the stream -----
        if zarr_stream is None:
            frame_height = full_size.height
            frame_width = full_size.width
            scale_x = sx
            scale_y = sy

            logger.info(
                f"Frame size from stream: {frame_height}x{frame_width}, "
                f"pixel scale: {scale_x:.4f} x {scale_y:.4f} µm"
            )
            logger.info(
                f"Known dimensions: T={num_t}, C={num_c}, Z={num_z}, "
                f"Tiles(M)={num_m}, Scenes(S)={num_s}, "
                f"Frame={frame_height}x{frame_width}"
            )

            dimensions: list[Dimension] = []

            if num_t > 1:
                dimensions.append(Dimension(name="t", count=num_t, chunk_size=1, type="time"))

            if num_positions > 1:
                pos_coords = [
                    Position(name=f"S{s_}_M{m_}", grid_row=s_, grid_column=m_)
                    for s_ in range(num_s)
                    for m_ in range(num_m)
                ]
                dimensions.append(Dimension(name="p", type="position", coords=pos_coords))  # type: ignore[arg-type]

            if num_c > 1:
                dimensions.append(Dimension(name="c", count=num_c, chunk_size=1, type="channel"))

            if num_z > 1:
                dimensions.append(
                    Dimension(
                        name="z",
                        count=num_z,
                        chunk_size=max(1, num_z),
                        type="space",
                        scale=ecfg.z_spacing,
                        unit="um",
                    )
                )

            dimensions.append(
                Dimension(
                    name="y",
                    count=frame_height,
                    chunk_size=min(512, frame_height),
                    type="space",
                    scale=scale_y,
                    unit="um",
                )
            )
            dimensions.append(
                Dimension(
                    name="x",
                    count=frame_width,
                    chunk_size=min(512, frame_width),
                    type="space",
                    scale=scale_x,
                    unit="um",
                )
            )

            settings = AcquisitionSettings(
                root_path=str(zarr_path),
                dimensions=tuple(dimensions),
                dtype=str(dtype),
                format="ome-zarr",  # type: ignore[arg-type]  # ome-writers accepts str
                compression=ecfg.compression,  # type: ignore[arg-type]  # ome-writers accepts str
                overwrite=ecfg.overwrite_zarr,
            )

            total_expected = settings.num_frames
            logger.info(f"AcquisitionSettings: shape={settings.shape}  total_frames={total_expected}")
            logger.info("Receiving & writing pixel stream on-the-fly ...")

            zarr_stream = create_stream(settings).__enter__()

        # ----- process the current frame -----
        key = (t, s, m, c, z)
        lin_idx = coord_to_linear.get(key)
        if lin_idx is None:
            logger.warning(f"Unexpected coordinate {key} – skipping frame.")
            continue

        frame_count += 1

        # Buffer the frame; flush everything we can write in order
        pending[lin_idx] = (frame, frame_meta)

        while next_write in pending:
            frm, fmeta = pending.pop(next_write)
            zarr_stream.append(frm, frame_metadata=fmeta)
            next_write += 1
            sys.stdout.write(build_progress_bar(next_write, total_expected))
            sys.stdout.flush()

        # All expected frames received – break out of the gRPC stream
        # (monitor_all_experiments does not terminate on its own).
        if total_expected is not None and frame_count >= total_expected:
            logger.info(
                f"Closing pixel stream (received {frame_count}/{total_expected} frames, "
                f"last linear index={lin_idx})."
            )
            break

    # After the async stream ends, flush remaining buffered frames
    # (fill gaps with skips for any frames that never arrived)
    if zarr_stream is not None:
        while next_write < len(coord_to_linear):
            if next_write in pending:
                frm, fmeta = pending.pop(next_write)
                zarr_stream.append(frm, frame_metadata=fmeta)
            else:
                zarr_stream.skip(frames=1)
                logger.warning(f"Missing frame at linear index {next_write} – skipped.")
            next_write += 1
            sys.stdout.write(build_progress_bar(next_write, total_expected))
            sys.stdout.flush()

        zarr_stream.__exit__(None, None, None)

    sys.stdout.write("\n")
    logger.info(f"OME-ZARR written successfully: {zarr_path}")
    logger.info(f"Frames received: {frame_count} / {total_expected} expected")
    channel.close()
    return zarr_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Stream ZEN pixel data into OME-ZARR via ZEN-API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--experiment-config",
        type=str,
        default=None,
        help=(
            "Path to an experiment config INI file (see experiment_config.ini). "
            "When provided, dimensions are known upfront and frames are written "
            "on-the-fly. Most other CLI flags are ignored except "
            "--start-experiment / --no-start-experiment which override the INI."
        ),
    )
    parser.add_argument(
        "--zenapi-config",
        type=str,
        default=str(Path(__file__).parent / "config.ini"),
        help="Path to the ZEN-API configuration file.",
    )
    parser.add_argument(
        "--experiment",
        type=str,
        required=False,
        default=None,
        help="ZEN experiment name (without .czexp extension). Required unless --experiment-config is used.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to store the OME-ZARR output.",
    )
    parser.add_argument(
        "--dtype",
        type=str,
        default="uint16",
        choices=["uint8", "uint16", "float32"],
        help="Pixel data type (must match experiment output).",
    )
    parser.add_argument(
        "--start-experiment",
        action=argparse.BooleanOptionalAction,
        default=None,
        help=(
            "Start the ZEN experiment from the script. "
            "Use --no-start-experiment to wait for the user to start from ZEN UI. "
            "In config mode this overrides the INI 'start_from_script' setting."
        ),
    )
    parser.add_argument(
        "--czi-name",
        type=str,
        default="zenapi_stream",
        help="CZI output name when starting experiment from script (without .czi).",
    )
    parser.add_argument(
        "--channel-index",
        type=int,
        default=None,
        help="Filter pixel stream by channel index (None = all channels).",
    )
    parser.add_argument(
        "--compression",
        type=str,
        default="blosc-zstd",
        choices=["blosc-zstd", "blosc-lz4", "zstd", "none"],
        help="Compression algorithm for the OME-ZARR store.",
    )
    parser.add_argument(
        "--no-overwrite-zarr",
        action="store_true",
        default=False,
        help="Do not overwrite an existing OME-ZARR at the output path.",
    )
    parser.add_argument(
        "--viewer",
        type=str,
        default=None,
        choices=["ndv", "napari"],
        help=(
            "Open the OME-ZARR in a viewer after acquisition. "
            "'ndv' uses the ndv viewer (requires ndv, zarr, dask, xarray). "
            "'napari' uses napari (requires napari, napari-ome-zarr). "
            "Omit to skip."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Entry point: parse arguments, run the appropriate streaming mode, and open the viewer."""
    args = parse_args()

    if args.experiment_config:
        # ---------- config-file mode (known dimensions, on-the-fly write) ----------
        ecfg = load_experiment_config(args.experiment_config)
        # CLI --start-experiment / --no-start-experiment overrides the INI value
        if args.start_experiment is not None:
            ecfg.start_from_script = args.start_experiment
        logger.info(f"Loaded experiment config: {args.experiment_config}")
        zarr_path = asyncio.run(stream_to_omezarr_with_config(ecfg))
    else:
        # ---------- CLI mode (unknown dimensions, buffered write) ----------
        if not args.experiment:
            logger.error("Either --experiment-config or --experiment must be provided.")
            sys.exit(1)

        compression = args.compression if args.compression != "none" else None

        zarr_path = asyncio.run(
            stream_to_omezarr(
                zenapi_config=args.zenapi_config,
                experiment_name=args.experiment,
                output_dir=args.output_dir,
                dtype=np.dtype(args.dtype),
                start_experiment_from_script=bool(args.start_experiment),
                czi_name=args.czi_name,
                channel_index=args.channel_index,
                overwrite_zarr=not args.no_overwrite_zarr,
                compression=compression,
            )
        )

    logger.info(f"Done. OME-ZARR: {zarr_path}")

    if args.viewer == "ndv":
        open_in_ndv_viewer(zarr_path)
    elif args.viewer == "napari":
        open_in_napari_viewer(zarr_path)


if __name__ == "__main__":
    main()
