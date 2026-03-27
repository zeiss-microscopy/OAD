# -*- coding: utf-8 -*-

#################################################################
# File        : zen_omezarr.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# Utility functions for the ZEN-API OME-ZARR streaming workflow:
#   - ExperimentConfig dataclass & INI parser
#   - start_experiment() helper (ZEN-API experiment control)
#   - build_progress_bar() for console progress display
#   - open_in_ndv_viewer() / open_in_napari_viewer() for viewing
#   - read_omezarr_axis_names() for OME-ZARR 0.5 metadata
#
# Copyright(c) 2026 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import configparser
import json
import logging
from dataclasses import dataclass
from pathlib import Path

from zen_api_utils.misc import initialize_zenapi

# ZEN API auto-generated stubs
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceStartExperimentRequest,
)

logger = logging.getLogger(__name__)


@dataclass
class ExperimentConfig:
    """Parsed experiment configuration."""

    experiment_name: str
    czi_name: str
    start_from_script: bool
    overwrite_czi: bool
    # dimensions
    time_points: int
    channels: int
    z_planes: int
    z_spacing: float
    tiles: int
    scenes: int
    # output
    output_dir: str
    dtype: str
    compression: str | None
    overwrite_zarr: bool
    # stream
    channel_index: int | None
    # zenapi
    zenapi_config: str


def load_experiment_config(config_path: str | Path) -> ExperimentConfig:
    """Load experiment configuration from an INI file.

    Args:
        config_path: Path to the experiment config INI file.

    Returns:
        Populated ExperimentConfig dataclass.
    """
    config_path = Path(config_path).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Experiment config not found: {config_path}")

    cfg = configparser.ConfigParser()
    cfg.read(config_path)

    # zenapi config: if empty, fall back to config.ini next to the script
    zenapi_config = cfg.get("zenapi", "config", fallback="").strip()
    if not zenapi_config:
        zenapi_config = str(Path(__file__).parent / "config.ini")

    # channel index: empty string means None (all channels)
    ch_idx_raw = cfg.get("stream", "channel_index", fallback="").strip()
    channel_index = int(ch_idx_raw) if ch_idx_raw else None

    # compression: 'none' string -> None
    compression_raw = cfg.get("output", "compression", fallback="blosc-zstd").strip()
    compression = compression_raw if compression_raw != "none" else None

    return ExperimentConfig(
        experiment_name=cfg.get("experiment", "name"),
        czi_name=cfg.get("experiment", "czi_name", fallback="zenapi_stream"),
        start_from_script=cfg.getboolean("experiment", "start_from_script", fallback=False),
        overwrite_czi=cfg.getboolean("experiment", "overwrite_czi", fallback=True),
        time_points=cfg.getint("dimensions", "time_points", fallback=1),
        channels=cfg.getint("dimensions", "channels", fallback=1),
        z_planes=cfg.getint("dimensions", "z_planes", fallback=1),
        z_spacing=cfg.getfloat("dimensions", "z_spacing", fallback=1.0),
        tiles=cfg.getint("dimensions", "tiles", fallback=1),
        scenes=cfg.getint("dimensions", "scenes", fallback=1),
        output_dir=cfg.get("output", "directory", fallback="."),
        dtype=cfg.get("output", "dtype", fallback="uint16"),
        compression=compression,
        overwrite_zarr=cfg.getboolean("output", "overwrite", fallback=True),
        channel_index=channel_index,
        zenapi_config=zenapi_config,
    )


async def start_experiment(
    exp_name: str,
    czi_name: str,
    overwrite: bool = False,
    configfile: str | Path = "config.ini",
) -> tuple[str, Path]:
    """Start a ZEN experiment via the ZEN-API.

    Args:
        exp_name: Experiment name (without .czexp extension).
        czi_name: Desired CZI output name (without .czi extension).
        overwrite: Allow overwriting an existing CZI.
        configfile: Path to the ZEN-API config file.

    Returns:
        Tuple of (experiment_id, czi_path).
    """
    channel, metadata = initialize_zenapi(configfile)
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)

    # load experiment
    my_exp = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=exp_name))
    logger.info(f"Loaded experiment: {exp_name} (id={my_exp.experiment_id})")

    # check output path and handle overwrite
    save_path = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    czi_path = Path(save_path.image_output_path) / f"{czi_name}.czi"
    logger.info(f"CZI save location: {czi_path}")

    if czi_path.exists():
        if overwrite:
            czi_path.unlink()
            logger.info(f"Overwrote existing CZI: {czi_path.name}")
        else:
            channel.close()
            raise FileExistsError(f"CZI file already exists: {czi_path}")

    # start the experiment (non-blocking)
    await exp_service.start_experiment(
        ExperimentServiceStartExperimentRequest(experiment_id=my_exp.experiment_id, output_name=czi_name)
    )
    logger.info("Experiment execution started.")

    channel.close()
    return my_exp.experiment_id, czi_path


def build_progress_bar(current: int, total: int | None, width: int = 40) -> str:
    """Render a text progress bar string.

    Args:
        current: Current frame number (1-based).
        total: Total expected frames, or None if unknown.
        width: Character width of the bar.

    Returns:
        Formatted progress bar string.
    """
    if total is not None and total > 0:
        frac = min(current / total, 1.0)
        filled = int(width * frac)
        bar = "█" * filled + "░" * (width - filled)
        return f"\r  [{bar}] {current}/{total} frames ({frac*100:.1f}%)"
    else:
        # unknown total – show a spinner-style counter
        return f"\r  Frames written: {current}"


def open_in_ndv_viewer(zarr_path: Path) -> None:
    """Open an OME-ZARR dataset in the ndv viewer.

    Reads axis names (T, C, Z, Y, X) and per-axis scales from the OME-ZARR
    0.5 metadata stored in ``zarr.json`` and wraps the highest-resolution
    array as a dask-backed ``xr.DataArray`` with physically-spaced
    coordinates so that ndv shows correct proportions (including Z depth)
    and labelled sliders.

    Requires optional dependencies: ``ndv``, ``zarr``, ``dask``, ``xarray``.
    If any are missing the function logs a warning and returns silently.

    Args:
        zarr_path: Path to the ``.ome.zarr`` directory.
    """
    try:
        import dask.array as da
        import zarr
        import ndv
        import numpy as np
        import xarray as xr
    except ImportError as e:
        logger.warning(
            f"Cannot open viewer (missing dependency: {e}). " "Install with: pip install ndv zarr dask xarray"
        )
        return

    try:
        logger.info(f"Opening OME-ZARR in ndv viewer: {zarr_path}")
        zarr_group = zarr.open(str(zarr_path), mode="r")

        # OME-ZARR stores the image array under the "0" key (highest resolution).
        # zarr.open() returns Array | Group; subscripting a Group with a string
        # key returns a broad union. We narrow to Array here.
        zarr_arr: zarr.Array = zarr_group["0"]  # type: ignore[index,assignment]
        if not hasattr(zarr_arr, "shape"):
            logger.error("Expected a zarr Array at key '0', got: %s", type(zarr_arr).__name__)
            return
        logger.info(f"Array shape: {zarr_arr.shape}, dtype: {zarr_arr.dtype}")

        # Read axis names from OME-ZARR 0.5 metadata (zarr v3: zarr.json).
        # ome-writers 0.3+ stores multiscales under attributes.ome.multiscales
        axis_names = read_omezarr_axis_names(zarr_path)
        axis_scales = read_omezarr_axis_scales(zarr_path)

        if axis_names and len(axis_names) == len(zarr_arr.shape):
            # Wrap zarr v3 array with dask for lazy chunk-aware loading,
            # then label dimensions via xarray for the ndv viewer.
            # Use physical coordinates (index * scale) so that the viewer
            # renders the correct aspect ratio, especially for Z stacks
            # where the z-spacing typically differs from the XY pixel size.
            dask_arr = da.from_array(zarr_arr, chunks=zarr_arr.chunks)  # type: ignore[arg-type]
            coords = {}
            for name, size in zip(axis_names, zarr_arr.shape):
                scale = axis_scales.get(name, 1.0) if axis_scales else 1.0
                coords[name] = np.arange(size, dtype=np.float64) * scale
            data = xr.DataArray(dask_arr, dims=axis_names, coords=coords)
            logger.info(f"Viewer data: shape={data.shape}, dims={data.dims}")
            if axis_scales:
                logger.info(f"Applied axis scales: {axis_scales}")
            ndv.imshow(data)
        else:
            logger.warning("Could not read axis names from OME-ZARR metadata, showing without labels.")
            ndv.imshow(zarr_arr)
    except Exception as e:
        logger.error(f"Failed to open OME-ZARR in ndv viewer: {e}")


def open_in_napari_viewer(zarr_path: Path) -> None:
    """Open an OME-ZARR dataset in the napari viewer.

    Uses the ``napari-ome-zarr`` plugin to read the dataset with full
    OME-ZARR metadata support (channels, scales, axis labels).

    Requires optional dependencies: ``napari`` and ``napari-ome-zarr``.
    If any are missing the function logs a warning and returns silently.

    Args:
        zarr_path: Path to the ``.ome.zarr`` directory.
    """
    try:
        import napari  # noqa: F811
    except ImportError as e:
        logger.warning(f"Cannot open napari viewer (missing dependency: {e}). " "Install with: pip install napari[all]")
        return

    try:
        import napari_ome_zarr  # noqa: F401
    except ImportError as e:
        logger.warning(f"Cannot open napari viewer (missing plugin: {e}). " "Install with: pip install napari-ome-zarr")
        return

    try:
        logger.info(f"Opening OME-ZARR in napari viewer: {zarr_path}")
        viewer = napari.Viewer()
        viewer.open(str(zarr_path), plugin="napari-ome-zarr")
        logger.info("napari viewer opened successfully.")
        napari.run()
    except Exception as e:
        logger.error(f"Failed to open OME-ZARR in napari viewer: {e}")


def read_omezarr_axis_names(zarr_path: Path) -> tuple[str, ...] | None:
    """Read axis names from the OME-ZARR 0.5 root metadata.

    OME-ZARR 0.5 (zarr v3) stores the multiscales metadata inside
    ``zarr.json → attributes.ome.multiscales``, unlike OME-ZARR 0.4
    which used ``.zattrs``.

    Args:
        zarr_path: Path to the ``.ome.zarr`` directory.

    Returns:
        Tuple of uppercase axis names (e.g. ``('T', 'C', 'Z', 'Y', 'X')``),
        or ``None`` if the metadata cannot be read.
    """
    zarr_json_path = zarr_path / "zarr.json"
    if not zarr_json_path.exists():
        return None

    with open(zarr_json_path) as f:
        root_meta = json.load(f)

    multiscales = root_meta.get("attributes", {}).get("ome", {}).get("multiscales", [])
    if not multiscales:
        return None

    axes = multiscales[0].get("axes", [])
    if not axes:
        return None

    axis_names = tuple(ax["name"].upper() for ax in axes)
    logger.info(f"OME-ZARR axis names: {axis_names}")
    return axis_names


def read_omezarr_axis_scales(zarr_path: Path) -> dict[str, float] | None:
    """Read per-axis scale factors from the OME-ZARR 0.5 root metadata.

    The scale transform is stored in
    ``zarr.json → attributes.ome.multiscales[0].datasets[0].coordinateTransformations``
    as a list entry with ``{"type": "scale", "scale": [s0, s1, ...]}``.
    The scale values are ordered to match the axes list.

    Args:
        zarr_path: Path to the ``.ome.zarr`` directory.

    Returns:
        Dict mapping uppercase axis name to its scale factor,
        or ``None`` if the metadata cannot be read.
    """
    zarr_json_path = zarr_path / "zarr.json"
    if not zarr_json_path.exists():
        return None

    with open(zarr_json_path) as f:
        root_meta = json.load(f)

    multiscales = root_meta.get("attributes", {}).get("ome", {}).get("multiscales", [])
    if not multiscales:
        return None

    axes = multiscales[0].get("axes", [])
    datasets = multiscales[0].get("datasets", [])
    if not axes or not datasets:
        return None

    # Find the scale transform for the highest-resolution dataset (index 0)
    transforms = datasets[0].get("coordinateTransformations", [])
    scale_values = None
    for t in transforms:
        if t.get("type") == "scale":
            scale_values = t.get("scale")
            break

    if scale_values is None or len(scale_values) != len(axes):
        return None

    axis_scales = {ax["name"].upper(): float(sv) for ax, sv in zip(axes, scale_values)}
    logger.info(f"OME-ZARR axis scales: {axis_scales}")
    return axis_scales
