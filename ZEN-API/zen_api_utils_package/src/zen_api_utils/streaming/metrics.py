"""Pure throughput metrics for ZEN pixel-stream measurements."""

from __future__ import annotations

from dataclasses import dataclass

NANOSECONDS_PER_SECOND = 1_000_000_000
BYTES_PER_MEBIBYTE = 1024 * 1024


@dataclass(slots=True)
class IntervalResult:
    """Throughput accumulated over one reporting interval."""

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
    """Calculate rates for an interval using monotonic nanosecond timestamps."""
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
