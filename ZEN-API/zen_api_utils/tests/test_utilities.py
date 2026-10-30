import importlib
import io
from pathlib import Path
from typing import Annotated
from unittest.mock import Mock

import pytest
from loguru import logger
from pydantic import AfterValidator, TypeAdapter, ValidationError

from zen_api_utils.extract_czexp_plan import extract_plan_xml
from zen_api_utils.misc import path_validator, set_logging
from zen_api_utils.sample_carrier import WellPlate


def test_capability_import_errors_include_versions_and_installation_action(monkeypatch: pytest.MonkeyPatch) -> None:
  """Missing generated symbols get actionable diagnostics and preserve their cause."""
  from zen_api_utils import compatibility

  monkeypatch.setattr(compatibility, "version", lambda name: {"zen_api": "2026.7.1", "zen_api_utils": "0.1.0"}[name])
  original = ImportError("cannot import name 'RequiredRequest'", name="zen_api.acquisition.v1beta")
  with pytest.raises(compatibility.ZenApiCompatibilityError) as caught:
    with compatibility.api_capabilities("Pixel streaming"):
      raise original
  assert caught.value.__cause__ is original
  assert caught.value.feature == "Pixel streaming"
  for text in ("RequiredRequest", "zen_api=2026.7.1", "zen_api_utils=0.1.0", "python -m pip check"):
    assert text in str(caught.value)


def test_capability_checks_validate_methods_and_dataclass_fields() -> None:
  """Check callable methods and declared fields without accessing field values."""
  from dataclasses import dataclass, field
  from types import SimpleNamespace

  from zen_api_utils.compatibility import ZenApiCompatibilityError, api_capabilities

  @dataclass
  class Frame:
    pixels: list = field(default_factory=list)

  with api_capabilities("Frame decoding", Frame, members=("pixels",)):
    pass
  with api_capabilities("Experiment loading", SimpleNamespace(load=lambda: None), methods=("load",)):
    pass
  with pytest.raises(ZenApiCompatibilityError, match="missing required capability.*raw_data"):
    with api_capabilities("Frame decoding", Frame, members=("raw_data",)):
      pytest.fail("A missing field must fail before entering the feature.")
  with pytest.raises(ZenApiCompatibilityError, match="missing required capability.*start"):
    with api_capabilities("Experiment start", SimpleNamespace(start=None), methods=("start",)):
      pytest.fail("A non-callable RPC must fail before entering the feature.")


def test_capability_checks_translate_only_unimplemented_rpcs() -> None:
  """Server capability errors are distinct from transport and application failures."""
  from grpclib.const import Status
  from grpclib.exceptions import GRPCError

  from zen_api_utils.compatibility import ZenApiCompatibilityError, api_capabilities

  original = GRPCError(Status.UNIMPLEMENTED, "monitor_all_experiments is unavailable")
  with pytest.raises(ZenApiCompatibilityError, match="ZEN server returned UNIMPLEMENTED") as caught:
    with api_capabilities("Pixel streaming"):
      raise original
  assert caught.value.__cause__ is original
  for original in (
    ImportError("No module named 'zarr'", name="zarr"),
    AttributeError("an internal programming error"),
    GRPCError(Status.UNAVAILABLE, "connection refused"),
    GRPCError(Status.PERMISSION_DENIED, "permission denied"),
  ):
    with pytest.raises(type(original)) as caught:
      with api_capabilities("Pixel streaming"):
        raise original
    assert caught.value is original


def test_capability_errors_work_without_distribution_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
  """Source checkouts without installed metadata still produce a useful error."""
  from zen_api_utils import compatibility

  def no_metadata(name: str) -> str:
    raise compatibility.PackageNotFoundError(name)

  monkeypatch.setattr(compatibility, "version", no_metadata)
  with pytest.raises(compatibility.ZenApiCompatibilityError, match="distribution metadata unavailable"):
    with compatibility.api_capabilities("Acquisition"):
      raise ModuleNotFoundError("No module named 'zen_api'", name="zen_api")


def test_async_capability_operations_preserve_signatures_and_optional_fallbacks() -> None:
  """Async guards execute around await, preserve cancellation, and keep local fallbacks."""
  import asyncio
  import inspect
  from types import SimpleNamespace

  from grpclib.const import Status
  from grpclib.exceptions import GRPCError

  from zen_api_utils.compatibility import ZenApiCompatibilityError, api_operation

  async def operation(value: int) -> int:
    return value + 1

  guarded = api_operation("Acquisition")(operation)
  assert inspect.signature(guarded) == inspect.signature(operation)
  assert asyncio.run(guarded(2)) == 3

  @api_operation("Optional status")
  async def fallback() -> int:
    try:
      raise GRPCError(Status.UNIMPLEMENTED, "status unavailable")
    except GRPCError:
      return 7

  assert asyncio.run(fallback()) == 7

  @api_operation("Required RPC")
  async def unsupported() -> None:
    raise GRPCError(Status.UNIMPLEMENTED, "export unavailable")

  with pytest.raises(ZenApiCompatibilityError, match="Required RPC"):
    asyncio.run(unsupported())

  @api_operation("Cancelled acquisition")
  async def cancelled() -> None:
    raise asyncio.CancelledError()

  with pytest.raises(asyncio.CancelledError):
    asyncio.run(cancelled())

  @api_operation("Missing RPC", SimpleNamespace(), methods=("load",))
  async def missing() -> None:
    pytest.fail("Capability validation must run before the operation.")

  with pytest.raises(ZenApiCompatibilityError, match="load"):
    asyncio.run(missing())


@pytest.mark.parametrize(
  "utility, api_module, symbol",
  [
    ("cameras", "zen_api.lm.hardware.v2", "CameraServiceGetCameraRequest"),
    ("changers", "zen_api.lm.hardware.v2", "FilterData"),
    ("experiment", "zen_api.acquisition.v1beta", "ExperimentServiceLoadRequest"),
    ("filters", "zen_api.lm.hardware.v2", "FilterData"),
    ("objective", "zen_api.lm.hardware.v2", "ObjectiveData"),
    ("stage", "zen_api.hardware.v1", "SimpleStageServiceStub"),
    ("tiles_positions", "zen_api.common.v1", "DoublePoint"),
    ("workflow", "zen_api.workflows.v3beta", "JobTemplateInfo"),
    ("workflow", "zen_api.workflows.v1beta", "JobResourcesServiceStub"),
    ("streaming.frames", "zen_api.acquisition.v1beta", "PixelType"),
    ("streaming.omezarr", "zen_api.acquisition.v1beta", "ExperimentServiceGetImageOutputPathRequest"),
    ("streaming.pipeline", "zen_api.acquisition.v1beta", "ExperimentStreamingServiceMonitorAllExperimentsResponse"),
  ],
)
def test_capability_guards_wrap_real_utility_imports(
  monkeypatch: pytest.MonkeyPatch, utility: str, api_module: str, symbol: str
) -> None:
  """Every generated-import boundary reports an actually missing API symbol."""
  from zen_api_utils.compatibility import ZenApiCompatibilityError

  if utility in {"streaming.omezarr", "streaming.pipeline"}:
    pytest.importorskip("ome_writers")
  module_name = f"zen_api_utils.{utility}"
  spec = importlib.util.find_spec(module_name)
  assert spec is not None and spec.origin is not None
  code = compile(Path(spec.origin).read_text(encoding="utf-8-sig"), spec.origin, "exec")
  generated = importlib.import_module(api_module)
  monkeypatch.delattr(generated, symbol)
  with pytest.raises(ZenApiCompatibilityError) as caught:
    exec(code, {"__name__": module_name, "__package__": module_name.rsplit(".", 1)[0]})
  assert symbol in str(caught.value)
  assert "python -m pip check" in str(caught.value)
  assert isinstance(caught.value.__cause__, ImportError)


def test_capability_guard_checks_real_export_request_and_response(monkeypatch: pytest.MonkeyPatch) -> None:
  """Export validates its client, request, and response before reading missing fields."""
  import asyncio
  from types import SimpleNamespace
  from unittest.mock import AsyncMock

  from zen_api_utils.compatibility import ZenApiCompatibilityError
  from zen_api_utils.experiment_acquisition import query_experiment_acquisition

  with pytest.raises(ZenApiCompatibilityError, match="missing required capability.*export"):
    asyncio.run(query_experiment_acquisition(SimpleNamespace(), "experiment-id"))
  service = SimpleNamespace(export=AsyncMock(return_value=SimpleNamespace()))
  with pytest.raises(ZenApiCompatibilityError, match="missing required capability.*xml"):
    asyncio.run(query_experiment_acquisition(service, "experiment-id"))
  service.export.reset_mock()
  generated = importlib.import_module("zen_api.acquisition.v1beta")
  monkeypatch.setattr(generated, "ExperimentServiceExportRequest", type("RequestWithoutExperimentId", (), {}))
  with pytest.raises(ZenApiCompatibilityError, match="missing required capability.*experiment_id"):
    asyncio.run(query_experiment_acquisition(service, "experiment-id"))
  service.export.assert_not_called()


@pytest.mark.parametrize(
  "utility, operation, rpc, arguments",
  [
    ("cameras", "get_cameras_info_LM", "get_cameras", ()),
    ("experiment", "load_experiment", "load", ("example",)),
    ("experiment_acquisition", "query_experiment_acquisition", "export", ("experiment-id",)),
    ("stage", "get_stageXY_position_simple", "get_position", ()),
    ("workflow", "get_status", "get_status", ()),
  ],
)
def test_capability_guards_translate_server_failures_in_real_operations(
  utility: str, operation: str, rpc: str, arguments: tuple
) -> None:
  """Mock unsupported server methods without connecting to microscope hardware."""
  import asyncio
  from types import SimpleNamespace
  from unittest.mock import AsyncMock

  from grpclib.const import Status
  from grpclib.exceptions import GRPCError

  from zen_api_utils.compatibility import ZenApiCompatibilityError

  original = GRPCError(Status.UNIMPLEMENTED, f"{rpc} is unavailable")
  service = SimpleNamespace(**{rpc: AsyncMock(side_effect=original)})
  function = getattr(importlib.import_module(f"zen_api_utils.{utility}"), operation)
  with pytest.raises(ZenApiCompatibilityError) as caught:
    asyncio.run(function(service, *arguments))
  assert caught.value.__cause__ is original
  assert rpc in str(caught.value)
  assert "ZEN installation" in str(caught.value)


def test_capability_guard_detects_missing_generated_method_before_rpc(monkeypatch: pytest.MonkeyPatch) -> None:
  """A present stub with a missing method fails before issuing an RPC."""
  import asyncio
  from types import SimpleNamespace
  from unittest.mock import AsyncMock

  from zen_api_utils import cameras
  from zen_api_utils.compatibility import ZenApiCompatibilityError

  service = SimpleNamespace(get_camera=AsyncMock())
  monkeypatch.setattr(cameras.CameraServiceStub, "get_camera", None)
  with pytest.raises(ZenApiCompatibilityError, match="missing required capability.*get_camera"):
    asyncio.run(cameras.get_camera_info_LM(service, "camera-id"))
  service.get_camera.assert_not_called()


def test_capability_guard_keeps_save_failure_status_and_logs_action() -> None:
  """Legacy save returns False, but its log contains the compatibility remedy."""
  import asyncio
  from types import SimpleNamespace
  from unittest.mock import AsyncMock

  from grpclib.const import Status
  from grpclib.exceptions import GRPCError

  from zen_api_utils.experiment import save_experiment

  output = io.StringIO()
  sink = logger.add(output, format="{message}")
  try:
    service = SimpleNamespace(save=AsyncMock(side_effect=GRPCError(Status.UNIMPLEMENTED, "save unavailable")))
    assert asyncio.run(save_experiment(SimpleNamespace(experiment_id="id"), service)) is False
    assert "Experiment saving" in output.getvalue()
    assert "python -m pip check" in output.getvalue()
  finally:
    logger.remove(sink)


@pytest.mark.parametrize("variant", ["move_changers", "move_changers_adv"])
@pytest.mark.parametrize("component", ["objective", "optovar", "reflector", "filterwheel"])
@pytest.mark.parametrize("phase", ["query", "movement"])
@pytest.mark.parametrize("failure", ["missing-method", "unimplemented"])
def test_capability_guards_keep_changer_error_results(
  monkeypatch: pytest.MonkeyPatch, variant: str, component: str, phase: str, failure: str
) -> None:
  """Both changer variants keep best-effort results without hiding compatibility actions."""
  import asyncio
  from types import SimpleNamespace
  from unittest.mock import AsyncMock

  from grpclib.const import Status
  from grpclib.exceptions import GRPCError

  from zen_api_utils import changers

  service_argument, stub_name, query, collection = {
    "objective": ("objchanger_service", "ObjectiveChangerServiceStub", "get_objectives", "objectives"),
    "optovar": ("optovar_service", "OptovarServiceStub", "get_optovars", "optovars"),
    "reflector": ("reflector_service", "ReflectorChangerServiceStub", "get_reflectors", "reflectors"),
    "filterwheel": ("filterwheel_service", "FilterWheelServiceStub", "get_filters", "filters"),
  }[component]
  move = AsyncMock()
  service = SimpleNamespace(move_to=move)
  kwargs = {f"{component}_position": 1}
  if phase == "movement":
    kwargs[collection] = SimpleNamespace(**{collection: [SimpleNamespace(position=1, name="component")]})
  method = query if phase == "query" else "move_to"
  if failure == "missing-method":
    setattr(service, method, None)
  else:
    setattr(service, method, AsyncMock(side_effect=GRPCError(Status.UNIMPLEMENTED, f"{method} unavailable")))
  if variant == "move_changers":
    monkeypatch.setattr(changers, stub_name, lambda *args, **kwargs: service)
    result = asyncio.run(changers.move_changers(None, [], **kwargs))
  else:
    result = asyncio.run(changers.move_changers_adv(**{service_argument: service}, **kwargs))
  assert result["errors"]
  assert "ZEN API compatibility error" in result["errors"][0]
  assert method in result["errors"][0]
  assert "python -m pip check" in result["errors"][0]
  move.assert_not_called()
  if phase == "query":
    assert component in result["skipped"]


@pytest.mark.parametrize(
  "failure",
  ["missing-method", "missing-symbol", "missing-request-field", "missing-response-field", "missing-status-field", "unimplemented"],
)
def test_capability_guards_preserve_optional_live_status_fallback(
  monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
  """An unavailable optional status capability keeps the exported acquisition dimensions."""
  import asyncio
  from types import SimpleNamespace
  from unittest.mock import AsyncMock

  from grpclib.const import Status
  from grpclib.exceptions import GRPCError

  pytest.importorskip("ome_writers")
  from zen_api_utils.streaming import pipeline

  fallback = pipeline.AcquisitionDimensions(time_points=3, channels=2, z_planes=5, scenes=1)
  status = SimpleNamespace(time_points_count=0, channels_count=0, zstack_slices_count=0, scenes_count=0, tiles_count=0)
  response = SimpleNamespace(status=status)
  service = SimpleNamespace(get_status=AsyncMock(return_value=response))
  generated = importlib.import_module("zen_api.acquisition.v1beta")
  if failure == "missing-method":
    del service.get_status
  elif failure == "missing-symbol":
    monkeypatch.delattr(generated, "ExperimentServiceGetStatusRequest")
  elif failure == "missing-request-field":
    monkeypatch.setattr(generated, "ExperimentServiceGetStatusRequest", type("RequestWithoutExperimentId", (), {}))
  elif failure == "missing-response-field":
    del response.status
  elif failure == "missing-status-field":
    del status.tiles_count
  else:
    service.get_status.side_effect = GRPCError(Status.UNIMPLEMENTED, "status unavailable")
  assert asyncio.run(pipeline._live_dimensions(service, "experiment-id", fallback)) is fallback


def test_tcp_example_import_does_not_connect(monkeypatch: pytest.MonkeyPatch) -> None:
    """Importing the shipped example must never contact the microscope."""
    from zen_api_utils import zen_tcpip

    transport = Mock()
    monkeypatch.setattr(zen_tcpip, "ZenTCPIP", transport)
    module = importlib.import_module("zen_api_utils.zen_tcpip_interface")
    importlib.reload(module)
    transport.assert_not_called()


def test_library_logging_preserves_application_sink() -> None:
    """Library imports and logger access preserve application configuration."""
    output = io.StringIO()
    sink = logger.add(output, format="{message}")
    try:
        assert set_logging() is logger
        module = importlib.import_module("zen_api_utils.cameras")
        importlib.reload(module)
        logger.info("host sink retained")
        assert "host sink retained" in output.getvalue()
    finally:
        logger.remove(sink)


def test_path_validator_rejects_invalid_values() -> None:
    """Invalid values raise ValueError, including inside Pydantic validation."""
    assert path_validator("example.czi") == Path("example.czi")
    with pytest.raises(ValueError, match="not a valid path"):
        path_validator(123)  # type: ignore[arg-type]
    adapter = TypeAdapter(Annotated[object, AfterValidator(path_validator)])
    with pytest.raises(ValidationError, match="not a valid path"):
        adapter.validate_python(123)


def test_well_plate_round_trip() -> None:
    plate = WellPlate(8, 12)

    assert plate.well_to_index("B3") == (1, 2)
    assert plate.index_to_well(7, 11) == "H12"
    assert "A1" in plate
    assert "I1" not in plate


def test_extract_plan_xml_reads_active_tile_regions() -> None:
    xml = """
    <Experiment>
      <ExperimentBlocks>
        <AcquisitionBlock IsActivated="true">
          <SubDimensionSetups>
            <RegionsSetup IsActivated="true">
              <SampleHolder>
                <TileRegions>
                  <TileRegion Name="B2">
                    <CenterPosition>100,200</CenterPosition>
                    <Columns>3</Columns>
                    <Rows>2</Rows>
                    <TemplateShapeId>2-2</TemplateShapeId>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
                  </TileRegion>
                </TileRegions>
              </SampleHolder>
            </RegionsSetup>
          </SubDimensionSetups>
        </AcquisitionBlock>
      </ExperimentBlocks>
    </Experiment>
    """

    plan = extract_plan_xml(xml)
    block = plan["acquisition_blocks"][0]

    assert block["dimensions"]["S"] == 1
    assert block["dimensions"]["M"] == 6
    assert block["positions"][0]["well_id"] == "B2"


def test_extract_plan_xml_reads_direct_single_tile_regions_without_inventing_wells() -> None:
    xml = """
    <Experiment>
      <ExperimentBlocks>
        <AcquisitionBlock IsActivated="true">
          <SubDimensionSetups>
            <RegionsSetup IsActivated="true">
              <SampleHolder>
                <SingleTileRegions>
                  <SingleTileRegion Name="P1" Id="1">
                    <X>30080.21</X><Y>24661.814</Y><Z>-8000</Z>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
                  </SingleTileRegion>
                  <SingleTileRegion Name="P2" Id="2">
                    <X>32389.872</X><Y>27671.373</Y><Z>-8000</Z>
                    <IsUsedForAcquisition>true</IsUsedForAcquisition>
                  </SingleTileRegion>
                  <SingleTileRegion Name="P3" Id="3">
                    <IsUsedForAcquisition>false</IsUsedForAcquisition>
                  </SingleTileRegion>
                </SingleTileRegions>
                <SingleTileRegionArrays />
              </SampleHolder>
            </RegionsSetup>
          </SubDimensionSetups>
        </AcquisitionBlock>
      </ExperimentBlocks>
    </Experiment>
    """

    block = extract_plan_xml(xml)["acquisition_blocks"][0]

    assert block["dimensions"]["S"] == 2
    assert block["position_count"] == 2
    assert block["well_count"] == 0
    assert block["positions"][0]["stage_position"] == {"x": 30080.21, "y": 24661.814, "z": -8000.0}
    assert [position["well_id"] for position in block["positions"]] == [None, None]
    assert block["planned_outputs"][0]["well_ids"] == []

    split_block = extract_plan_xml(
        xml.replace("<SampleHolder>", "<SampleHolder><SplitScenesInSeparateFiles>true</SplitScenesInSeparateFiles>")
    )["acquisition_blocks"][0]
    assert [output["suggested_filename"] for output in split_block["planned_outputs"]] == [
        "<experiment-export>-Scene-001-P1.czi",
        "<experiment-export>-Scene-002-P2.czi",
    ]
