"""Regression tests for headless acquisition lifecycle and data integrity."""

import asyncio
import contextlib
import json
import socket
from collections.abc import AsyncIterator
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import numpy as np
import pytest
import zarr
from grpclib.client import Channel
from grpclib.server import Server
from zen_api.acquisition.v1beta import (
    ExperimentStreamingServiceBase,
    ExperimentStreamingServiceMonitorAllExperimentsRequest,
    ExperimentStreamingServiceMonitorAllExperimentsResponse,
    FrameData,
    PixelType,
)

from zen_api_utils.experiment_acquisition import (
    AcquisitionDimensions,
    ExperimentAcquisition,
)
from zen_api_utils.streaming import omezarr, pipeline
from zen_api_utils.streaming.omezarr import ExperimentConfig, start_loaded_experiment


def test_monitor_requests_are_sent_before_open_returns() -> None:
    """Opening monitors sends every request and registers cancellation."""
    channel = Mock()
    streams = [AsyncMock(), AsyncMock()]
    for stream in streams:
        stream.__aenter__.return_value = stream
    channel.request.side_effect = streams

    async def check() -> None:
        async with contextlib.AsyncExitStack() as resources:
            opened = await pipeline._open_channel_streams(channel, [], [0, 1], resources)
            assert [index for index, _ in opened] == [0, 1]
            for index, stream in enumerate(streams):
                stream.send_message.assert_awaited_once()
                assert stream.send_message.call_args.args[0].channel_index == index
                assert stream.send_message.call_args.kwargs == {"end": True}
                stream.cancel.assert_not_awaited()
        for stream in streams:
            stream.cancel.assert_awaited_once()
            stream.__aexit__.assert_awaited_once()

    asyncio.run(check())


def test_start_loaded_experiment_preserves_identity(tmp_path: Path) -> None:
    """Starting an armed experiment must not reload it and change its ID."""
    service = Mock()
    service.get_image_output_path = AsyncMock(return_value=SimpleNamespace(image_output_path=str(tmp_path)))
    service.start_experiment = AsyncMock()

    output = asyncio.run(start_loaded_experiment(service, "armed-id", "output"))

    assert output == tmp_path / "output.czi"
    service.load.assert_not_called()
    assert service.start_experiment.call_args.args[0].experiment_id == "armed-id"


def _frame(
    experiment_id: str = "target",
    channel: int = 0,
    z_index: int = 0,
    value: int = 7,
    tile_index: int = 0,
) -> SimpleNamespace:
    """Create one tiny grayscale payload with complete geometry metadata."""
    return SimpleNamespace(
        frame_data=SimpleNamespace(
            experiment_id=experiment_id,
            frame_position=SimpleNamespace(t=0, c=channel, z=z_index, m=tile_index, s=0),
            frame_size=SimpleNamespace(width=2, height=2),
            pixel_data=SimpleNamespace(
                pixel_type=PixelType.GRAY16,
                raw_data=np.full((2, 2), value, dtype=np.uint16).tobytes(),
            ),
            scaling=SimpleNamespace(x=1e-6, y=1e-6),
            frame_stage_position=SimpleNamespace(x=0.0, y=0.0, z=z_index * 1e-6),
        )
    )


class _Monitor:
    """Transport double that records sending, cancellation, and EOF."""

    def __init__(self, harness: SimpleNamespace) -> None:
        self.harness = harness
        self.responses: list[SimpleNamespace] = []

    async def __aenter__(self) -> "_Monitor":
        return self

    async def __aexit__(self, *args: object) -> None:
        self.harness.events.append("monitor_closed")

    async def send_message(
        self,
        request: ExperimentStreamingServiceMonitorAllExperimentsRequest,
        *,
        end: bool,
    ) -> None:
        assert end
        channel = request.channel_index
        self.harness.events.append(f"subscribe:{channel}")
        self.responses = list(self.harness.frames.get(channel, []))

    async def cancel(self) -> None:
        self.harness.events.append("cancel")

    def __aiter__(self) -> "_Monitor":
        return self

    async def __anext__(self) -> SimpleNamespace:
        if self.responses:
            return self.responses.pop(0)
        if self.harness.hold_open:
            self.harness.waiting.set()
            await asyncio.Event().wait()
        raise StopAsyncIteration


@pytest.fixture
def harness(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    """Replace only ZEN services while exercising the real OME-Zarr writer."""
    environment = SimpleNamespace(
        events=[],
        frames={0: [_frame()]},
        hold_open=False,
        waiting=asyncio.Event(),
        acquisition=ExperimentAcquisition(
            "test",
            AcquisitionDimensions(1, 1, 1, 1),
            (),
            (),
            False,
        ),
        status=SimpleNamespace(
            time_points_count=1,
            channels_count=1,
            zstack_slices_count=1,
            tiles_count=1,
            scenes_count=1,
            images_count=1,
        ),
    )
    channel = Mock()
    channel.request.side_effect = lambda *args, **kwargs: _Monitor(environment)
    channel.close.side_effect = lambda: environment.events.append("channel_closed")
    service = Mock()
    service.load = AsyncMock(return_value=SimpleNamespace(experiment_id="target"))
    service.get_status = AsyncMock(side_effect=lambda request: SimpleNamespace(status=environment.status))
    service.get_image_output_path = AsyncMock(return_value=SimpleNamespace(image_output_path=str(tmp_path)))
    service.start_experiment = AsyncMock(side_effect=lambda request: environment.events.append("start"))
    environment.channel = channel
    environment.service = service
    environment.config = ExperimentConfig(
        experiment_name="test",
        czi_name="test",
        start_from_script=True,
        overwrite_czi=False,
        time_points=1,
        channels=1,
        z_planes=1,
        z_spacing=1.0,
        tiles=1,
        scenes=1,
        output_dir=str(tmp_path),
        dtype="uint16",
        compression=None,
        overwrite_zarr=False,
        channel_index=None,
        zenapi_config="unused",
        use_hcs_layout=False,
        spatial_shard_size_chunks=None,
    )
    monkeypatch.setattr(pipeline, "initialize_zenapi", lambda *args: (channel, []))
    monkeypatch.setattr(pipeline, "ExperimentServiceStub", lambda **kwargs: service)
    monkeypatch.setattr(
        pipeline,
        "query_experiment_acquisition",
        AsyncMock(side_effect=lambda *args: environment.acquisition),
    )
    return environment


def _pixels(path: Path) -> np.ndarray:
    """Read the first image array from an actual output store."""
    image = pipeline._find_omezarr_image_paths(path)[0]
    return zarr.open_group(image, mode="r")["0"][:]


async def _run_acquisition(harness: SimpleNamespace, mode: str, inactivity_timeout: float = 30.0) -> Path:
    """Run either public writer with the same acquisition double."""
    config = harness.config
    if mode == "configured":
        return await pipeline.stream_to_omezarr_with_config(config, inactivity_timeout=inactivity_timeout)
    return await pipeline.stream_to_omezarr(
        config.zenapi_config,
        config.experiment_name,
        config.output_dir,
        start_experiment_from_script=config.start_from_script,
        czi_name=config.czi_name,
        overwrite_czi=config.overwrite_czi,
        channel_index=config.channel_index,
        overwrite_zarr=config.overwrite_zarr,
        compression=config.compression,
        spatial_shard_size_chunks=config.spatial_shard_size_chunks,
        inactivity_timeout=inactivity_timeout,
    )


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_filters_foreign_frames_and_arms_before_start(harness: SimpleNamespace, mode: str) -> None:
    """A foreign payload cannot enter the target output or affect completion."""
    foreign = _frame("other", value=99)
    foreign.frame_data.pixel_data.raw_data = b"invalid"
    harness.frames[0] = [foreign, _frame(value=7)]

    output = asyncio.run(_run_acquisition(harness, mode))

    assert np.all(_pixels(output) == 7)
    assert harness.events.index("subscribe:0") < harness.events.index("start")
    assert harness.service.get_status.call_args.args[0].experiment_id == "target"
    assert harness.events[-1] == "channel_closed"
    assert "cancel" in harness.events


@pytest.mark.parametrize("hold_open", [False, True])
@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_partial_stream_fails_and_preserves_received_pixels(
    harness: SimpleNamespace, hold_open: bool, mode: str
) -> None:
    """EOF and inactivity preserve partial data but never return success."""
    harness.acquisition = replace(harness.acquisition, dimensions=AcquisitionDimensions(1, 1, 2, 1))
    harness.status.zstack_slices_count = 2
    harness.hold_open = hold_open

    with pytest.raises(pipeline.IncompleteAcquisitionError) as failure:
        asyncio.run(_run_acquisition(harness, mode, inactivity_timeout=0.02))

    error = failure.value
    assert (error.received_frames, error.expected_frames) == (1, 2)
    status = json.loads(error.report_path.read_text(encoding="utf-8"))
    assert status["complete"] is False
    assert status["missing_coordinates"] == [[0, 0, 0, 0, 1]]
    pixels = _pixels(error.zarr_path)
    assert np.all(pixels[0] == 7)
    assert np.all(pixels[1] == 0)
    assert harness.events[-1] == "channel_closed"


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_empty_stream_fails_with_report(harness: SimpleNamespace, mode: str) -> None:
    """No data produces a diagnostic sidecar, not a successful store path."""
    harness.frames.clear()
    with pytest.raises(pipeline.IncompleteAcquisitionError) as failure:
        asyncio.run(_run_acquisition(harness, mode))
    assert not failure.value.zarr_path.exists()
    assert failure.value.report_path.exists()
    assert failure.value.received_frames == 0


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_exports_channels_before_subscribing(harness: SimpleNamespace, mode: str) -> None:
    """Stale INI C=1 cannot hide the experiment's second channel."""
    harness.acquisition = replace(harness.acquisition, dimensions=AcquisitionDimensions(1, 2, 1, 1))
    harness.status.channels_count = 2
    harness.frames[1] = [_frame(channel=1, value=11)]
    output = asyncio.run(_run_acquisition(harness, mode))
    assert set(np.unique(_pixels(output))) == {7, 11}
    assert harness.events.index("subscribe:1") < harness.events.index("start")
    assert harness.config.channels == 1


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_rejects_live_channel_disagreement(harness: SimpleNamespace, mode: str) -> None:
    """A live/XML mismatch must fail instead of claiming a complete subset."""
    harness.status.channels_count = 2
    with pytest.raises(ValueError, match="Live channel count differs"):
        asyncio.run(_run_acquisition(harness, mode))


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_manual_run_pins_first_experiment(harness: SimpleNamespace, mode: str) -> None:
    """After manual arming, frames from subsequent experiments are ignored."""
    harness.config.start_from_script = False
    harness.acquisition = replace(harness.acquisition, dimensions=AcquisitionDimensions(1, 1, 2, 1))
    harness.status.zstack_slices_count = 2
    harness.frames[0] = [
        _frame("manual", value=3),
        _frame("other", z_index=1, value=99),
        _frame("manual", z_index=1, value=5),
    ]
    output = asyncio.run(_run_acquisition(harness, mode))
    assert set(np.unique(_pixels(output))) == {3, 5}
    assert "start" not in harness.events
    assert harness.service.get_status.call_args.args[0].experiment_id == "manual"


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_selected_channel_is_remapped_to_singleton_output(harness: SimpleNamespace, mode: str) -> None:
    """Selecting source C=1 must not create an empty output C=0 plane."""
    harness.acquisition = replace(harness.acquisition, dimensions=AcquisitionDimensions(1, 2, 1, 1))
    harness.status.channels_count = 2
    harness.config.channel_index = 1
    harness.frames[1] = [_frame(channel=1, value=11)]
    output = asyncio.run(_run_acquisition(harness, mode))
    assert _pixels(output).shape == (2, 2)
    assert np.all(_pixels(output) == 11)
    assert "subscribe:0" not in harness.events


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_failed_start_cleans_up_open_subscriptions(harness: SimpleNamespace, mode: str) -> None:
    """A start RPC failure must close every already armed subscription."""
    harness.service.start_experiment.side_effect = RuntimeError("start failed")
    with pytest.raises(RuntimeError, match="start failed"):
        asyncio.run(_run_acquisition(harness, mode))
    assert harness.events == [
        "subscribe:0",
        "cancel",
        "monitor_closed",
        "channel_closed",
    ]


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_cancellation_cleans_up_open_subscriptions(harness: SimpleNamespace, mode: str) -> None:
    """Cancellation cannot leave monitoring tasks or channels alive."""
    harness.frames.clear()
    harness.hold_open = True

    async def check() -> None:
        task = asyncio.create_task(_run_acquisition(harness, mode))
        try:
            await asyncio.wait_for(harness.waiting.wait(), timeout=2.0)
        finally:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

    asyncio.run(check())
    assert harness.events[-3:] == ["cancel", "monitor_closed", "channel_closed"]


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_partial_tiles_are_not_finalized_or_removed(
    harness: SimpleNamespace, mode: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Keep original tile groups intact when a scene acquisition is partial."""
    harness.acquisition = replace(harness.acquisition, dimensions=AcquisitionDimensions(1, 1, 2, 1, tiles=2))
    harness.status.zstack_slices_count = 2
    harness.status.tiles_count = 2
    harness.frames[0] = [_frame(), _frame(z_index=1), _frame(tile_index=1)]
    finalize = Mock()
    monkeypatch.setattr(pipeline, "_assemble_scene_mosaics", finalize)
    with pytest.raises(pipeline.IncompleteAcquisitionError) as failure:
        asyncio.run(_run_acquisition(harness, mode))
    finalize.assert_not_called()
    assert len(pipeline._find_omezarr_image_paths(failure.value.zarr_path)) == 2
    assert failure.value.received_frames == 3


def test_monitor_is_sent_before_first_frame_over_real_grpc() -> None:
    """The real transport can subscribe before the server produces data."""

    async def check() -> None:
        subscribed = asyncio.Event()
        acquire = asyncio.Event()

        class Service(ExperimentStreamingServiceBase):
            async def monitor_all_experiments(
                self,
                request: ExperimentStreamingServiceMonitorAllExperimentsRequest,
            ) -> AsyncIterator[ExperimentStreamingServiceMonitorAllExperimentsResponse]:
                assert request.channel_index == 0
                subscribed.set()
                await acquire.wait()
                yield ExperimentStreamingServiceMonitorAllExperimentsResponse(
                    frame_data=FrameData(experiment_id="local-test")
                )
                await asyncio.Event().wait()

        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
        server = Server([Service()])
        await server.start(sock=listener)
        channel = Channel("127.0.0.1", port)
        try:
            async with contextlib.AsyncExitStack() as resources:
                streams = await asyncio.wait_for(
                    pipeline._open_channel_streams(channel, [], [0], resources),
                    timeout=5.0,
                )
                await asyncio.wait_for(subscribed.wait(), timeout=5.0)
                acquire.set()
                response = await asyncio.wait_for(anext(streams[0][1].__aiter__()), timeout=5.0)
                assert response.frame_data.experiment_id == "local-test"
        finally:
            channel.close()
            server.close()
            await server.wait_closed()
            listener.close()

    asyncio.run(check())


@pytest.mark.parametrize("mode", ["configured", "buffered"])
def test_out_of_order_and_duplicate_frames_preserve_unique_count(harness: SimpleNamespace, mode: str) -> None:
    """Reordering and retransmission must not fake acquisition completion."""
    harness.acquisition = replace(harness.acquisition, dimensions=AcquisitionDimensions(1, 1, 2, 1))
    harness.status.zstack_slices_count = 2
    harness.frames[0] = [
        _frame(z_index=1, value=11),
        _frame(z_index=1, value=11),
        _frame(value=7),
    ]
    output = asyncio.run(_run_acquisition(harness, mode))
    pixels = _pixels(output)
    assert np.all(pixels[0] == 7)
    assert np.all(pixels[1] == 11)
    status = json.loads((output / "acquisition_status.json").read_text(encoding="utf-8"))
    assert status["complete"] is True
    assert status["received_frames"] == status["expected_frames"] == 2


@pytest.mark.parametrize("fail_start", [False, True])
def test_existing_start_helper_still_loads_and_closes(
    harness: SimpleNamespace, monkeypatch: pytest.MonkeyPatch, fail_start: bool
) -> None:
    """The existing public start helper keeps its load/start/close contract."""
    monkeypatch.setattr(omezarr, "initialize_zenapi", lambda *args: (harness.channel, []))
    monkeypatch.setattr(omezarr, "ExperimentServiceStub", lambda **kwargs: harness.service)
    if fail_start:
        harness.service.start_experiment.side_effect = RuntimeError("start failed")
        with pytest.raises(RuntimeError, match="start failed"):
            asyncio.run(omezarr.start_experiment("test", "test"))
    else:
        experiment_id, output = asyncio.run(omezarr.start_experiment("test", "test"))
        assert experiment_id == "target"
        assert output.name == "test.czi"
    harness.service.load.assert_awaited_once()
    harness.channel.close.assert_called_once()
