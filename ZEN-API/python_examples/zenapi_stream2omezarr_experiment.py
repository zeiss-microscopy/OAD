"""Stream a ZEN experiment to OME-ZARR using metadata exported from ZEN.

The command-line interface is useful for manual runs. The same workflow can
be called from another Python script without an INI file::

    import asyncio
    from pathlib import Path

    from zenapi_stream2omezarr_experiment import stream_experiment

    output = asyncio.run(
        stream_experiment(
            "00_ZEN_API_OMEZARR_Stream",
            zenapi_config=Path("config.ini"),
            output_dir=Path(r"F:\\Zen_Output\\streaming"),
            start_experiment=True,
        )
    )
    print(output)

The experiment is loaded and exported through ZEN-API before streaming. Its
time points, channels, Z planes, scenes, active channel information, and
scene-to-well mapping are then used to configure the OME-ZARR writer. When
the experiment uses sample-carrier wells, the output is written directly as
an OME-ZARR HCS plate.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from zen_api.acquisition.v1beta import ExperimentServiceStub
from zen_api_utils.experiment_acquisition import load_experiment_acquisition
from zen_api_utils.misc import initialize_zenapi, set_logging
from zen_api_utils.streaming.omezarr import ExperimentConfig
from zen_api_utils.streaming.pipeline import generate_omezarr_pyramids, stream_to_omezarr_with_config

logger = set_logging()


def validate_omezarr_output(path: str | Path) -> None:
    """Validate a regular image or HCS plate OME-Zarr output."""
    from czitools.export_tools.validation import validate_ome_zarr

    logger.info(f"Validating OME-ZARR metadata: {path}")
    if not validate_ome_zarr(path):
        raise RuntimeError(f"OME-ZARR validation failed: {path}")
    logger.info(f"OME-ZARR validation passed: {path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stream a ZEN experiment to OME-ZARR using exported experiment metadata."
    )
    parser.add_argument(
        "--experiment",
        required=True,
        help="ZEN experiment name without the .czexp extension.",
    )
    parser.add_argument(
        "--zenapi-config",
        type=Path,
        default=Path(__file__).with_name("config.ini"),
        help="Path to the ZEN-API gateway configuration file.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="OME-ZARR output directory.")
    parser.add_argument(
        "--dtype",
        choices=["uint8", "uint16", "float32"],
        default="uint16",
        help="Pixel data type; must match the experiment output.",
    )
    parser.add_argument("--czi-name", default="zenapi_stream", help="CZI output name without .czi.")
    parser.add_argument(
        "--start-experiment",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Start the experiment from the script; use --no-start-experiment for ZEN UI startup.",
    )
    parser.add_argument("--channel-index", type=int, default=None, help="Stream only one channel index.")
    parser.add_argument(
        "--compression",
        choices=["blosc-zstd", "blosc-lz4", "zstd", "none"],
        default="blosc-zstd",
        help="OME-ZARR compression algorithm.",
    )
    parser.add_argument(
        "--spatial-shard-size-chunks",
        type=int,
        default=2,
        help="Chunks per Y/X shard; use 0 to disable Zarr v3 sharding.",
    )
    parser.add_argument("--no-overwrite-czi", action="store_true", help="Preserve an existing CZI file.")
    parser.add_argument("--no-overwrite-zarr", action="store_true", help="Preserve an existing OME-ZARR.")
    parser.add_argument(
        "--validate-ome-zarr",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Validate the completed image or HCS OME-Zarr output with czitools.",
    )
    parser.add_argument(
        "--hcs-layout",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Write explicit ZEN wells using the OME-ZARR HCS plate layout.",
    )
    parser.add_argument(
        "--keep-source-tiles",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Retain the streamed source tile groups after scene assembly.",
    )
    parser.add_argument(
        "--inactivity-timeout",
        type=float,
        default=30.0,
        help="Seconds without a frame before acquisition is considered complete.",
    )
    parser.add_argument(
        "--max-pending-frames",
        type=int,
        default=4096,
        help="Maximum out-of-order frames retained before aborting.",
    )
    parser.add_argument(
        "--pyramid-levels",
        type=int,
        default=0,
        help="Number of 2x Y/X pyramid levels to generate after acquisition; use 0 to disable.",
    )
    return parser.parse_args()


async def build_config(args: argparse.Namespace) -> ExperimentConfig:
    """Query ZEN and build the streaming configuration without an INI file."""
    channel, metadata = initialize_zenapi(args.zenapi_config)
    try:
        experiment_service = ExperimentServiceStub(channel=channel, metadata=metadata)
        acquisition = await load_experiment_acquisition(experiment_service, args.experiment)
    finally:
        channel.close()

    dimensions = acquisition.dimensions
    logger.info(
        f"Experiment metadata: T={dimensions.time_points} C={dimensions.channels} "
        f"Z={dimensions.z_planes} scenes={dimensions.scenes} tiles={dimensions.tiles} "
        f"z-spacing={dimensions.z_spacing:.4f} um "
        f"frame={dimensions.pixel_width or 'unknown'}x{dimensions.pixel_height or 'unknown'}"
    )
    logger.info(f"Active channels: {[channel.name for channel in acquisition.channels_info]}")

    return ExperimentConfig(
        experiment_name=args.experiment,
        czi_name=args.czi_name,
        start_from_script=args.start_experiment,
        overwrite_czi=not args.no_overwrite_czi,
        time_points=dimensions.time_points,
        channels=dimensions.channels,
        z_planes=dimensions.z_planes,
        z_spacing=dimensions.z_spacing,
        tiles=dimensions.tiles,
        scenes=dimensions.scenes,
        output_dir=str(args.output_dir),
        dtype=args.dtype,
        compression=None if args.compression == "none" else args.compression,
        overwrite_zarr=not args.no_overwrite_zarr,
        channel_index=args.channel_index,
        zenapi_config=str(args.zenapi_config),
        positions=acquisition.positions,
        use_hcs_layout=args.hcs_layout,
        keep_source_tiles=args.keep_source_tiles,
        spatial_shard_size_chunks=args.spatial_shard_size_chunks or None,
        max_pending_frames=args.max_pending_frames,
    )


async def run(args: argparse.Namespace) -> Path:
    config = await build_config(args)
    output = await stream_to_omezarr_with_config(
        config,
        inactivity_timeout=args.inactivity_timeout,
    )
    if args.pyramid_levels:
        generate_omezarr_pyramids(
            output,
            pyramid_levels=args.pyramid_levels,
            spatial_shard_size_chunks=config.spatial_shard_size_chunks,
        )
    if args.validate_ome_zarr:
        validate_omezarr_output(output)
    return output


async def stream_experiment(
    experiment_name: str,
    *,
    zenapi_config: str | Path | None = None,
    output_dir: str | Path = ".",
    dtype: str = "uint16",
    czi_name: str = "zenapi_stream",
    start_experiment: bool = False,
    channel_index: int | None = None,
    compression: str = "blosc-zstd",
    overwrite_czi: bool = True,
    overwrite_zarr: bool = True,
    validate_ome_zarr: bool = False,
    use_hcs_layout: bool = True,
    keep_source_tiles: bool = False,
    spatial_shard_size_chunks: int | None = 2,
    inactivity_timeout: float = 30.0,
    max_pending_frames: int = 4096,
    pyramid_levels: int = 0,
) -> Path:
    """Query *experiment_name* and stream it to OME-ZARR.

    This is the programmatic API equivalent of the command-line entry point.
    Acquisition dimensions are queried from ZEN; output and streaming
    behavior are supplied as ordinary function arguments.

    Args:
        experiment_name: ZEN experiment name without ``.czexp``.
        zenapi_config: Path to the ZEN-API gateway configuration file.
        output_dir: Directory where the OME-ZARR directory is created.
        dtype: Pixel dtype matching the experiment output.
        czi_name: CZI output name when starting the experiment from Python.
        start_experiment: Start acquisition through ZEN-API when true.
        channel_index: Optional channel filter; ``None`` streams all channels.
        compression: OME-ZARR compression name, or ``"none"``.
        overwrite_czi: Allow replacing an existing CZI output.
        overwrite_zarr: Allow replacing an existing OME-ZARR output.
        validate_ome_zarr: Validate the completed image or HCS OME-Zarr output.
        use_hcs_layout: Write explicit ZEN wells as an HCS plate when true.
        keep_source_tiles: Retain raw tile groups after scene assembly.
        spatial_shard_size_chunks: Number of chunks per Y/X shard, or None
            to disable Zarr v3 sharding.
        inactivity_timeout: Seconds without a frame before completion.
        max_pending_frames: Maximum buffered out-of-order frames.
        pyramid_levels: Number of post-acquisition 2x Y/X pyramid levels.

    Returns:
        Path to the created OME-ZARR directory.
    """
    if zenapi_config is None:
        zenapi_config = Path(__file__).with_name("config.ini")
    if dtype not in {"uint8", "uint16", "float32"}:
        raise ValueError("dtype must be uint8, uint16, or float32")
    if compression not in {"blosc-zstd", "blosc-lz4", "zstd", "none"}:
        raise ValueError("Unsupported compression")
    if channel_index is not None and channel_index < 0:
        raise ValueError("channel_index must be non-negative or None")
    if spatial_shard_size_chunks is not None and spatial_shard_size_chunks < 1:
        raise ValueError("spatial_shard_size_chunks must be positive or None")
    if inactivity_timeout <= 0:
        raise ValueError("inactivity_timeout must be greater than zero")
    if max_pending_frames < 1:
        raise ValueError("max_pending_frames must be a positive integer")
    if pyramid_levels < 0:
        raise ValueError("pyramid_levels must be non-negative")

    args = argparse.Namespace(
        experiment=experiment_name,
        zenapi_config=Path(zenapi_config),
        output_dir=Path(output_dir),
        dtype=dtype,
        czi_name=czi_name,
        start_experiment=start_experiment,
        channel_index=channel_index,
        compression=compression,
        no_overwrite_czi=not overwrite_czi,
        no_overwrite_zarr=not overwrite_zarr,
        validate_ome_zarr=validate_ome_zarr,
        hcs_layout=use_hcs_layout,
        keep_source_tiles=keep_source_tiles,
        spatial_shard_size_chunks=spatial_shard_size_chunks or 0,
        inactivity_timeout=inactivity_timeout,
        max_pending_frames=max_pending_frames,
        pyramid_levels=pyramid_levels,
    )
    return await run(args)


def main() -> None:
    args = parse_args()
    result = asyncio.run(run(args))
    logger.info(f"Done. OME-ZARR: {result}")


if __name__ == "__main__":
    main()
