#################################################################
# File        : zenapi_streaming_benchmark.py
# Institution : Carl Zeiss Microscopy GmbH
#
# Benchmark ZEN API experiment pixel-stream throughput without display or
# image processing. The experiment is started manually from the ZEN UI.
#
# Copyright(c) 2026 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import argparse
import asyncio
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import perf_counter_ns

import numpy as np
from grpclib.config import Configuration
from zen_api.acquisition.v1beta import (
    ExperimentStreamingServiceMonitorAllExperimentsRequest,
    ExperimentStreamingServiceStub,
    PixelType,
)
from zen_api_utils.misc import initialize_zenapi, set_logging

logger = set_logging()

NANOSECONDS_PER_SECOND = 1_000_000_000
BYTES_PER_MEBIBYTE = 1024 * 1024


@dataclass(slots=True)
class IntervalResult:
    elapsed_seconds: float
    interval_seconds: float
    total_frames: int
    interval_frames: int
    total_bytes: int
    interval_bytes: int
    frames_per_second: float
    mebibytes_per_second: float
    megapixels_per_second: float
    mean_reshape_microseconds: float


PIXEL_FORMATS: dict[PixelType, tuple[np.dtype, int]] = {
    PixelType.GRAY8: (np.dtype(np.uint8), 1),
    PixelType.GRAY16: (np.dtype(np.uint16), 1),
    PixelType.BGR24: (np.dtype(np.uint8), 3),
    PixelType.BGR48: (np.dtype(np.uint16), 3),
}


def reshape_frame(raw_data: bytes, width: int, height: int, pixel_type: PixelType) -> np.ndarray:
    """Create a zero-copy NumPy view of one streamed pixel payload."""
    try:
        dtype, components = PIXEL_FORMATS[pixel_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported pixel type: {pixel_type.name}") from exc

    shape = (height, width) if components == 1 else (height, width, components)
    expected_bytes = height * width * components * dtype.itemsize
    if len(raw_data) != expected_bytes:
        raise ValueError(
            f"Payload has {len(raw_data)} bytes, expected {expected_bytes} for " f"{width}x{height} {pixel_type.name}"
        )

    return np.frombuffer(raw_data, dtype=dtype).reshape(shape)


def calculate_interval(
    measurement_start_ns: int,
    interval_start_ns: int,
    now_ns: int,
    total_frames: int,
    interval_frames: int,
    total_bytes: int,
    interval_bytes: int,
    interval_pixels: int,
    interval_reshape_ns: int,
) -> IntervalResult:
    interval_seconds = (now_ns - interval_start_ns) / NANOSECONDS_PER_SECOND
    elapsed_seconds = (now_ns - measurement_start_ns) / NANOSECONDS_PER_SECOND
    return IntervalResult(
        elapsed_seconds=elapsed_seconds,
        interval_seconds=interval_seconds,
        total_frames=total_frames,
        interval_frames=interval_frames,
        total_bytes=total_bytes,
        interval_bytes=interval_bytes,
        frames_per_second=interval_frames / interval_seconds,
        mebibytes_per_second=interval_bytes / BYTES_PER_MEBIBYTE / interval_seconds,
        megapixels_per_second=interval_pixels / 1_000_000 / interval_seconds,
        mean_reshape_microseconds=interval_reshape_ns / interval_frames / 1_000,
    )


def log_interval(result: IntervalResult) -> None:
    logger.info(
        f"elapsed={result.elapsed_seconds:8.2f}s | "
        f"frames={result.total_frames:8d} | "
        f"rate={result.frames_per_second:9.2f} frame/s | "
        f"payload={result.mebibytes_per_second:9.2f} MiB/s | "
        f"pixels={result.megapixels_per_second:9.2f} MP/s | "
        f"reshape={result.mean_reshape_microseconds:8.2f} us/frame"
    )


def write_csv(path: Path, results: list[IntervalResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(IntervalResult.__annotations__))
        writer.writeheader()
        for result in results:
            writer.writerow({field: getattr(result, field) for field in IntervalResult.__annotations__})


def plot_throughput(path: Path, results: list[IntervalResult], show_plot: bool) -> None:
    """Save and optionally display interval throughput after measurement."""
    from matplotlib import pyplot as plt

    elapsed_seconds = [result.elapsed_seconds for result in results]
    payload_rates = [result.mebibytes_per_second for result in results]
    frame_rates = [result.frames_per_second for result in results]

    figure, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, layout="constrained")
    figure.suptitle("ZEN API Pixel-stream Throughput")

    axes[0].plot(elapsed_seconds, payload_rates, marker="o", linewidth=1.5)
    axes[0].set_ylabel("Payload (MiB/s)")
    axes[0].grid(alpha=0.3)

    axes[1].plot(elapsed_seconds, frame_rates, marker="o", linewidth=1.5, color="tab:orange")
    axes[1].set_xlabel("Elapsed measurement time (s)")
    axes[1].set_ylabel("Frame rate (frames/s)")
    axes[1].grid(alpha=0.3)

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=150)
    logger.info(f"Throughput plot written to: {path.resolve()}")

    if show_plot:
        plt.show()
    else:
        plt.close(figure)


async def benchmark_stream(
    config_path: Path,
    http2_window_mib: int,
    channel_index: int | None,
    enable_raw_data: bool,
    report_interval: float,
    duration: float | None,
    max_frames: int | None,
    csv_path: Path,
    plot_path: Path,
    show_plot: bool,
) -> None:
    http2_window_bytes = http2_window_mib * BYTES_PER_MEBIBYTE
    grpc_config = Configuration(
        http2_connection_window_size=http2_window_bytes,
        http2_stream_window_size=http2_window_bytes,
    )
    channel, metadata = initialize_zenapi(config_path, grpc_config=grpc_config)
    streaming_service = ExperimentStreamingServiceStub(channel=channel, metadata=metadata)
    request = ExperimentStreamingServiceMonitorAllExperimentsRequest(
        channel_index=channel_index,
        enable_raw_data=enable_raw_data,
    )

    logger.info("Pixel-stream benchmark is ready. Start the experiment from the ZEN UI.")
    logger.info(
        f"channel={'all' if channel_index is None else channel_index}, "
        f"raw_data={enable_raw_data}, report_interval={report_interval:.2f}s, "
        f"http2_window={http2_window_mib} MiB"
    )

    received_frames = 0
    measured_frames = 0
    total_bytes = 0
    total_pixels = 0
    total_reshape_ns = 0
    interval_frames = 0
    interval_bytes = 0
    interval_pixels = 0
    interval_reshape_ns = 0
    measurement_start_ns: int | None = None
    interval_start_ns: int | None = None
    results: list[IntervalResult] = []
    channels: Counter[int] = Counter()
    last_frame: np.ndarray | None = None
    last_frame_ns: int | None = None
    first_frame_description: str | None = None

    async_iter = streaming_service.monitor_all_experiments(request).__aiter__()
    try:
        while True:
            timeout: float | None = None
            if duration is not None and measurement_start_ns is not None:
                measured_seconds = (perf_counter_ns() - measurement_start_ns) / NANOSECONDS_PER_SECOND
                timeout = max(0.0, duration - measured_seconds)
                if timeout == 0:
                    logger.info("Benchmark duration reached while waiting for a frame.")
                    break

            try:
                if timeout is None:
                    response = await async_iter.__anext__()
                else:
                    response = await asyncio.wait_for(
                        async_iter.__anext__(),
                        timeout=timeout,
                    )
            except asyncio.TimeoutError:
                logger.info("Benchmark duration reached while waiting for a frame.")
                break
            except StopAsyncIteration:
                break

            frame_data = response.frame_data
            pixel_data = frame_data.pixel_data
            size = pixel_data.size if enable_raw_data else frame_data.frame_size
            received_frames += 1
            channels[frame_data.frame_position.c] += 1

            reshape_start_ns = perf_counter_ns()
            last_frame = reshape_frame(
                pixel_data.raw_data,
                width=size.width,
                height=size.height,
                pixel_type=pixel_data.pixel_type,
            )
            now_ns = perf_counter_ns()
            reshape_ns = now_ns - reshape_start_ns

            if measurement_start_ns is None:
                measurement_start_ns = now_ns
                interval_start_ns = now_ns
                first_frame_description = (
                    f"{size.width}x{size.height}, {pixel_data.pixel_type.name}, "
                    f"shape={last_frame.shape}, {len(pixel_data.raw_data)} bytes/frame"
                )
                logger.info(f"Warm-up frame received: {first_frame_description}")
                if max_frames is not None and received_frames >= max_frames:
                    break
                continue

            payload_bytes = len(pixel_data.raw_data)
            pixels = size.width * size.height
            last_frame_ns = now_ns
            measured_frames += 1
            total_bytes += payload_bytes
            total_pixels += pixels
            total_reshape_ns += reshape_ns
            interval_frames += 1
            interval_bytes += payload_bytes
            interval_pixels += pixels
            interval_reshape_ns += reshape_ns

            assert interval_start_ns is not None
            if (now_ns - interval_start_ns) / NANOSECONDS_PER_SECOND >= report_interval:
                result = calculate_interval(
                    measurement_start_ns,
                    interval_start_ns,
                    now_ns,
                    measured_frames,
                    interval_frames,
                    total_bytes,
                    interval_bytes,
                    interval_pixels,
                    interval_reshape_ns,
                )
                results.append(result)
                log_interval(result)
                interval_start_ns = now_ns
                interval_frames = 0
                interval_bytes = 0
                interval_pixels = 0
                interval_reshape_ns = 0

            elapsed_seconds = (now_ns - measurement_start_ns) / NANOSECONDS_PER_SECOND
            if duration is not None and elapsed_seconds >= duration:
                break
            if max_frames is not None and received_frames >= max_frames:
                break
    except asyncio.CancelledError:
        logger.info("Benchmark interrupted; finalizing collected measurements.")
    finally:
        close = getattr(async_iter, "aclose", None)
        if close is not None:
            await close()
        channel.close()

    if measurement_start_ns is None or last_frame_ns is None or measured_frames == 0:
        logger.warning("Fewer than two frames were received; no throughput result is available.")
        return

    if interval_frames > 0 and interval_start_ns is not None:
        final_interval = calculate_interval(
            measurement_start_ns,
            interval_start_ns,
            last_frame_ns,
            measured_frames,
            interval_frames,
            total_bytes,
            interval_bytes,
            interval_pixels,
            interval_reshape_ns,
        )
        results.append(final_interval)
        log_interval(final_interval)

    elapsed_seconds = max((last_frame_ns - measurement_start_ns) / NANOSECONDS_PER_SECOND, 1e-9)
    logger.info("Benchmark complete")
    logger.info(f"frame={first_frame_description}")
    logger.info(f"channels={dict(sorted(channels.items()))}")
    logger.info(
        f"received={received_frames} frames, measured={measured_frames} frames after 1 warm-up, "
        f"{total_bytes / BYTES_PER_MEBIBYTE:.2f} measured MiB, {elapsed_seconds:.3f}s | "
        f"average={measured_frames / elapsed_seconds:.2f} frame/s, "
        f"{total_bytes / BYTES_PER_MEBIBYTE / elapsed_seconds:.2f} MiB/s, "
        f"{total_pixels / 1_000_000 / elapsed_seconds:.2f} MP/s, "
        f"reshape={total_reshape_ns / measured_frames / 1_000:.2f} us/frame"
    )

    if results:
        write_csv(csv_path, results)
        logger.info(f"Interval results written to: {csv_path.resolve()}")
        plot_throughput(plot_path, results, show_plot)


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    parser = argparse.ArgumentParser(
        description="Measure ZEN API pixel-stream receive and zero-copy reshape throughput."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=script_dir / "my_config.ini",
        help="ZEN API gateway configuration (default: my_config.ini next to this script).",
    )
    parser.add_argument(
        "--channel-index",
        type=int,
        default=0,
        help="Only receive this zero-based channel index (default: 0).",
    )
    parser.add_argument(
        "--http2-window-mib",
        type=int,
        default=4,
        help="HTTP/2 connection and stream receive window in MiB (default: 4).",
    )
    parser.add_argument(
        "--raw-data",
        action="store_true",
        help="Benchmark partial/raw frames instead of assembled full frames.",
    )
    parser.add_argument(
        "--report-interval",
        type=float,
        default=1.0,
        help="Seconds between throughput summaries (default: 1.0).",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Stop after this many measured seconds (default: run until Ctrl+C).",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Stop after this many received frames, including warm-up (default: run until Ctrl+C).",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=script_dir / "benchmark_results" / f"stream_{timestamp}.csv",
        help="CSV path for interval results.",
    )
    parser.add_argument(
        "--plot",
        type=Path,
        default=script_dir / "benchmark_results" / f"stream_{timestamp}.png",
        help="PNG path for the throughput plot.",
    )
    parser.add_argument(
        "--no-show-plot",
        action="store_true",
        help="Save the throughput plot without opening its window after the benchmark.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.report_interval <= 0:
        raise ValueError("--report-interval must be greater than zero")
    if not 1 <= args.http2_window_mib <= 2047:
        raise ValueError("--http2-window-mib must be between 1 and 2047")
    if args.duration is not None and args.duration <= 0:
        raise ValueError("--duration must be greater than zero")
    if args.max_frames is not None and args.max_frames <= 0:
        raise ValueError("--max-frames must be greater than zero")

    try:
        asyncio.run(
            benchmark_stream(
                config_path=args.config,
                http2_window_mib=args.http2_window_mib,
                channel_index=args.channel_index,
                enable_raw_data=args.raw_data,
                report_interval=args.report_interval,
                duration=args.duration,
                max_frames=args.max_frames,
                csv_path=args.csv,
                plot_path=args.plot,
                show_plot=not args.no_show_plot,
            )
        )
    except KeyboardInterrupt:
        logger.info("Benchmark stopped by user.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
