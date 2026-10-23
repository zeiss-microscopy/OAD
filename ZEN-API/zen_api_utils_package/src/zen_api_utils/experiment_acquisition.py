"""Typed acquisition metadata extracted from a ZEN experiment."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_api.acquisition.v1beta import ExperimentServiceStub


@dataclass(frozen=True)
class AcquisitionDimensions:
    """Acquisition axes known before pixel streaming starts."""

    time_points: int
    channels: int
    z_planes: int
    scenes: int
    z_spacing: float = 1.0
    tiles: int = 1
    pixel_width: int | None = None
    pixel_height: int | None = None


@dataclass(frozen=True)
class AcquisitionChannel:
    """An active acquisition channel."""

    name: str | None
    pixel_type: str | None


@dataclass(frozen=True)
class ExperimentAcquisition:
    """Small typed snapshot of the acquisition settings used by streaming."""

    experiment_name: str | None
    dimensions: AcquisitionDimensions
    channels_info: tuple[AcquisitionChannel, ...]
    positions: tuple[dict[str, object], ...]
    split_scenes_in_separate_files: bool

    @property
    def well_ids(self) -> tuple[str, ...]:
        """Unique sample-carrier well IDs in acquisition order."""
        return tuple(
            dict.fromkeys(
                well_id
                for position in self.positions
                if isinstance((well_id := position.get("well_id")), str) and well_id
            )
        )

    @property
    def well_count(self) -> int:
        """Number of sample-carrier wells used for acquisition."""
        return len(self.well_ids)

    @property
    def position_count(self) -> int:
        """Number of active acquisition positions/scenes."""
        return len(self.positions)

    @classmethod
    def from_plan(cls, plan: dict[str, object], block_index: int = 0) -> ExperimentAcquisition:
        blocks = plan.get("acquisition_blocks")
        if not isinstance(blocks, list) or not blocks:
            raise ValueError("The experiment contains no active acquisition blocks.")
        block = blocks[block_index]
        if not isinstance(block, dict):
            raise TypeError("The acquisition block has an invalid structure.")

        dimensions = block.get("dimensions")
        if not isinstance(dimensions, dict):
            raise TypeError("The acquisition block has no dimensions.")
        channels = block.get("channels", [])
        positions = block.get("positions", [])
        if not isinstance(channels, list) or not isinstance(positions, list):
            raise TypeError("The acquisition block has invalid channel or position data.")

        source = plan.get("source")
        experiment_name = None
        if isinstance(source, dict):
            source_path = source.get("path")
            if isinstance(source_path, str):
                experiment_name = Path(source_path).stem.removesuffix(".czexp")

        return cls(
            experiment_name=experiment_name,
            dimensions=AcquisitionDimensions(
                time_points=int(dimensions.get("T", 1) or 1),
                channels=int(dimensions.get("C", 1) or 1),
                z_planes=int(dimensions.get("Z", 1) or 1),
                scenes=int(dimensions.get("S", 1) or 1),
                z_spacing=float(dimensions.get("ZSpacing", 1.0) or 1.0),
                tiles=int(dimensions.get("M", 1) or 1),
                pixel_width=_optional_int(dimensions.get("X")),
                pixel_height=_optional_int(dimensions.get("Y")),
            ),
            channels_info=tuple(
                AcquisitionChannel(
                    name=channel.get("name") if isinstance(channel.get("name"), str) else None,
                    pixel_type=channel.get("pixel_type") if isinstance(channel.get("pixel_type"), str) else None,
                )
                for channel in channels
                if isinstance(channel, dict)
            ),
            positions=tuple(position for position in positions if isinstance(position, dict)),
            split_scenes_in_separate_files=bool(block.get("split_scenes_in_separate_files", False)),
        )

    @classmethod
    def from_czexp(cls, source: Path) -> ExperimentAcquisition:
        from .extract_czexp_plan import extract_plan

        return cls.from_plan(extract_plan(source))


async def query_experiment_acquisition(
    service: ExperimentServiceStub,
    experiment_id: str,
    experiment_name: str | None = None,
) -> ExperimentAcquisition:
    """Export and parse a loaded experiment through the ZEN API."""
    from .extract_czexp_plan import extract_plan_xml

    from zen_api.acquisition.v1beta import ExperimentServiceExportRequest

    response = await service.export(ExperimentServiceExportRequest(experiment_id=experiment_id))
    xml = getattr(response, "xml", None)
    if not isinstance(xml, str) or not xml.strip():
        raise ValueError("ZEN returned an empty experiment XML export.")
    acquisition = ExperimentAcquisition.from_plan(extract_plan_xml(xml, experiment_name or experiment_id))
    if experiment_name is None:
        return acquisition
    return replace(acquisition, experiment_name=experiment_name)


async def load_experiment_acquisition(
    service: ExperimentServiceStub,
    experiment_name: str,
) -> ExperimentAcquisition:
    """Load an experiment by name, export it, and return its acquisition data."""
    from .experiment import load_experiment

    experiment_id = await load_experiment(service, experiment_name)
    return await query_experiment_acquisition(service, experiment_id, experiment_name)


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) else None
