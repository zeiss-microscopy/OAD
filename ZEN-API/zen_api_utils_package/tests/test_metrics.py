from zen_api_utils.streaming.metrics import calculate_interval


def test_calculate_interval_returns_rates() -> None:
    result = calculate_interval(
        measurement_start_ns=0,
        interval_start_ns=0,
        now_ns=2_000_000_000,
        total_frames=4,
        interval_frames=4,
        total_bytes=8 * 1024 * 1024,
        interval_bytes=8 * 1024 * 1024,
        interval_pixels=2_000_000,
        interval_reshape_ns=8_000_000,
    )

    assert result.frames_per_second == 2
    assert result.mebibytes_per_second == 4
    assert result.megapixels_per_second == 1
    assert result.mean_reshape_microseconds == 2_000
