#################################################################
# File        : changers.py
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from collections.abc import Callable
from typing import Literal, TypedDict

from grpclib.client import Channel

from zen_api_utils.compatibility import api_capabilities

with api_capabilities("Optical changer control"):
    from zen_api.lm.hardware.v2 import (
        FilterWheelServiceGetFiltersRequest,
        FilterWheelServiceGetFiltersResponse,
        FilterWheelServiceMoveToRequest,
        FilterWheelServiceStub,
        ObjectiveChangerServiceGetObjectivesRequest,
        ObjectiveChangerServiceGetObjectivesResponse,
        ObjectiveChangerServiceMoveToRequest,
        ObjectiveChangerServiceStub,
        OptovarServiceGetOptovarsRequest,
        OptovarServiceGetOptovarsResponse,
        OptovarServiceMoveToRequest,
        OptovarServiceStub,
        ReflectorChangerServiceGetReflectorsRequest,
        ReflectorChangerServiceGetReflectorsResponse,
        ReflectorChangerServiceMoveToRequest,
        ReflectorChangerServiceStub,
    )

from zen_api_utils.filters import (
    get_filter_by_position,
    get_reflector_by_position,
    get_used_filterwheel_positions,
    get_used_reflector_positions,
)
from zen_api_utils.misc import set_logging
from zen_api_utils.objective import (
    get_objective_by_position,
    get_optovar_by_position,
    get_used_objective_positions,
    get_used_optovar_positions,
)

logger = set_logging()

__all__ = [
    "ChangerMove",
    "ChangerResults",
    "get_filter_by_position",
    "get_objective_by_position",
    "get_optovar_by_position",
    "get_reflector_by_position",
    "get_used_filterwheel_positions",
    "get_used_objective_positions",
    "get_used_optovar_positions",
    "get_used_reflector_positions",
    "move_changers",
    "move_changers_adv",
]


class ChangerMove(TypedDict):
    """A completed movement, using the existing dictionary representation."""

    position: int
    name: str
    status: Literal["success"]


class ChangerResults(TypedDict):
    """Best-effort results; None means no successful movement was recorded.

    Unrequested, skipped and failed movements remain None for compatibility.
    The skipped, warnings and errors lists distinguish reported failures.
    """

    objective: ChangerMove | None
    optovar: ChangerMove | None
    reflector: ChangerMove | None
    filterwheel: ChangerMove | None
    skipped: list[str]
    warnings: list[str]
    errors: list[str]


def _empty_results() -> ChangerResults:
    return {
        "objective": None,
        "optovar": None,
        "reflector": None,
        "filterwheel": None,
        "skipped": [],
        "warnings": [],
        "errors": [],
    }


def _initialize_service[Service](
    name: str,
    position: int | None,
    create_service: Callable[[], Service],
    results: ChangerResults,
) -> Service | None:
    """Initialize a requested changer without disabling the other changers."""
    if position is None:
        return None
    try:
        return create_service()
    except Exception as error:
        warning = f"Failed to initialize {name} service: {error} - skipping movement"
        results["warnings"].append(warning)
        results["skipped"].append(name)
        logger.warning(warning)
        return None


async def move_changers(
    channel: Channel,
    metadata: list[tuple[str, str]],
    objectives: ObjectiveChangerServiceGetObjectivesResponse | None = None,
    optovars: OptovarServiceGetOptovarsResponse | None = None,
    reflectors: ReflectorChangerServiceGetReflectorsResponse | None = None,
    filters: FilterWheelServiceGetFiltersResponse | None = None,
    objective_position: int | None = None,
    optovar_position: int | None = None,
    reflector_position: int | None = None,
    filterwheel_position: int | None = None,
) -> ChangerResults:
    """Create requested services and delegate movement to move_changers_adv.

    Missing component data is queried before movement. A None target leaves
    that changer untouched. Initialization failures are logged and reported in
    warnings/skipped while the remaining requested changers continue.
    """
    initialization = _empty_results()
    objective_service = _initialize_service(
        "objective",
        objective_position,
        lambda: ObjectiveChangerServiceStub(channel=channel, metadata=metadata),
        initialization,
    )
    optovar_service = _initialize_service(
        "optovar",
        optovar_position,
        lambda: OptovarServiceStub(channel=channel, metadata=metadata),
        initialization,
    )
    reflector_service = _initialize_service(
        "reflector",
        reflector_position,
        lambda: ReflectorChangerServiceStub(channel=channel, metadata=metadata),
        initialization,
    )
    filterwheel_service = _initialize_service(
        "filterwheel",
        filterwheel_position,
        lambda: FilterWheelServiceStub(channel=channel, metadata=metadata),
        initialization,
    )

    results = await move_changers_adv(
        objchanger_service=objective_service,
        optovar_service=optovar_service,
        reflector_service=reflector_service,
        filterwheel_service=filterwheel_service,
        objectives=objectives,
        optovars=optovars,
        reflectors=reflectors,
        filters=filters,
        objective_position=objective_position
        if objective_service is not None
        else None,
        optovar_position=optovar_position if optovar_service is not None else None,
        reflector_position=reflector_position
        if reflector_service is not None
        else None,
        filterwheel_position=filterwheel_position
        if filterwheel_service is not None
        else None,
    )
    results["warnings"] = initialization["warnings"] + results["warnings"]
    results["skipped"] = initialization["skipped"] + results["skipped"]
    return results


async def move_changers_adv(
    objchanger_service: ObjectiveChangerServiceStub | None = None,
    optovar_service: OptovarServiceStub | None = None,
    reflector_service: ReflectorChangerServiceStub | None = None,
    filterwheel_service: FilterWheelServiceStub | None = None,
    objectives: ObjectiveChangerServiceGetObjectivesResponse | None = None,
    optovars: OptovarServiceGetOptovarsResponse | None = None,
    reflectors: ReflectorChangerServiceGetReflectorsResponse | None = None,
    filters: FilterWheelServiceGetFiltersResponse | None = None,
    objective_position: int | None = None,
    optovar_position: int | None = None,
    reflector_position: int | None = None,
    filterwheel_position: int | None = None,
) -> ChangerResults:
    """Move requested changers using caller-owned services and optional data.

    Query missing data first, then move in objective/optovar/reflector/filterwheel
    order. Each query or movement failure is logged and included in errors so
    independent changers can continue. Missing services are warnings/skipped;
    failed queries also mark the changer skipped. Cancellation propagates.

    Results remain ordinary dictionaries. A successful entry contains position,
    name and status="success"; all other entries are None.
    """
    results = _empty_results()
    for name, service, position in (
        ("objective", objchanger_service, objective_position),
        ("optovar", optovar_service, optovar_position),
        ("reflector", reflector_service, reflector_position),
        ("filterwheel", filterwheel_service, filterwheel_position),
    ):
        if position is not None and service is None:
            warning = f"{name.capitalize()} position {position} requested but service not available - skipping"
            results["warnings"].append(warning)
            results["skipped"].append(name)
            logger.warning(warning)

    if (
        objective_position is not None
        and objchanger_service is not None
        and objectives is None
    ):
        try:
            with api_capabilities(
                "Objective changer information",
                objchanger_service,
                methods=("get_objectives",),
            ):
                objectives = await objchanger_service.get_objectives(
                    ObjectiveChangerServiceGetObjectivesRequest()
                )
        except Exception as error:
            message = f"Failed to fetch objectives data: {error}"
            results["errors"].append(message)
            results["skipped"].append("objective")
            logger.error(message)
            objective_position = None

    if (
        optovar_position is not None
        and optovar_service is not None
        and optovars is None
    ):
        try:
            with api_capabilities(
                "Optovar information", optovar_service, methods=("get_optovars",)
            ):
                optovars = await optovar_service.get_optovars(
                    OptovarServiceGetOptovarsRequest()
                )
        except Exception as error:
            message = f"Failed to fetch optovars data: {error}"
            results["errors"].append(message)
            results["skipped"].append("optovar")
            logger.error(message)
            optovar_position = None

    if (
        reflector_position is not None
        and reflector_service is not None
        and reflectors is None
    ):
        try:
            with api_capabilities(
                "Reflector information", reflector_service, methods=("get_reflectors",)
            ):
                reflectors = await reflector_service.get_reflectors(
                    ReflectorChangerServiceGetReflectorsRequest()
                )
        except Exception as error:
            message = f"Failed to fetch reflectors data: {error}"
            results["errors"].append(message)
            results["skipped"].append("reflector")
            logger.error(message)
            reflector_position = None

    if (
        filterwheel_position is not None
        and filterwheel_service is not None
        and filters is None
    ):
        try:
            with api_capabilities(
                "Filter wheel information",
                filterwheel_service,
                methods=("get_filters",),
            ):
                filters = await filterwheel_service.get_filters(
                    FilterWheelServiceGetFiltersRequest()
                )
        except Exception as error:
            message = f"Failed to fetch filters data: {error}"
            results["errors"].append(message)
            results["skipped"].append("filterwheel")
            logger.error(message)
            filterwheel_position = None

    if (
        objective_position is not None
        and objchanger_service is not None
        and objectives is not None
    ):
        try:
            target_objective = get_objective_by_position(objectives, objective_position)
            if target_objective is None:
                raise ValueError(f"Invalid objective position: {objective_position}")
            with api_capabilities(
                "Objective changer movement", objchanger_service, methods=("move_to",)
            ):
                await objchanger_service.move_to(
                    ObjectiveChangerServiceMoveToRequest(
                        position_index=objective_position
                    )
                )
            results["objective"] = {
                "position": target_objective.position,
                "name": target_objective.name,
                "status": "success",
            }
            logger.info(
                f"Moved objective to position {objective_position}: {target_objective.name}"
            )
        except Exception as error:
            message = (
                f"Failed to move objective to position {objective_position}: {error}"
            )
            results["errors"].append(message)
            logger.error(message)

    if (
        optovar_position is not None
        and optovar_service is not None
        and optovars is not None
    ):
        try:
            target_optovar = get_optovar_by_position(optovars, optovar_position)
            if target_optovar is None:
                raise ValueError(f"Invalid optovar position: {optovar_position}")
            with api_capabilities(
                "Optovar movement", optovar_service, methods=("move_to",)
            ):
                await optovar_service.move_to(
                    OptovarServiceMoveToRequest(position_index=optovar_position)
                )
            results["optovar"] = {
                "position": target_optovar.position,
                "name": target_optovar.name,
                "status": "success",
            }
            logger.info(
                f"Moved optovar to position {optovar_position}: {target_optovar.name}"
            )
        except Exception as error:
            message = f"Failed to move optovar to position {optovar_position}: {error}"
            results["errors"].append(message)
            logger.error(message)

    if (
        reflector_position is not None
        and reflector_service is not None
        and reflectors is not None
    ):
        try:
            target_reflector = get_reflector_by_position(reflectors, reflector_position)
            if target_reflector is None:
                raise ValueError(f"Invalid reflector position: {reflector_position}")
            with api_capabilities(
                "Reflector movement", reflector_service, methods=("move_to",)
            ):
                await reflector_service.move_to(
                    ReflectorChangerServiceMoveToRequest(
                        position_index=reflector_position
                    )
                )
            results["reflector"] = {
                "position": target_reflector.position,
                "name": target_reflector.name,
                "status": "success",
            }
            logger.info(
                f"Moved reflector to position {reflector_position}: {target_reflector.name}"
            )
        except Exception as error:
            message = (
                f"Failed to move reflector to position {reflector_position}: {error}"
            )
            results["errors"].append(message)
            logger.error(message)

    if (
        filterwheel_position is not None
        and filterwheel_service is not None
        and filters is not None
    ):
        try:
            target_filter = get_filter_by_position(filters, filterwheel_position)
            if target_filter is None:
                raise ValueError(
                    f"Invalid filterwheel position: {filterwheel_position}"
                )
            with api_capabilities(
                "Filter wheel movement", filterwheel_service, methods=("move_to",)
            ):
                await filterwheel_service.move_to(
                    FilterWheelServiceMoveToRequest(position_index=filterwheel_position)
                )
            results["filterwheel"] = {
                "position": target_filter.position,
                "name": target_filter.name,
                "status": "success",
            }
            logger.info(
                f"Moved filterwheel to position {filterwheel_position}: {target_filter.name}"
            )
        except Exception as error:
            message = f"Failed to move filterwheel to position {filterwheel_position}: {error}"
            results["errors"].append(message)
            logger.error(message)

    successful_moves = [
        name
        for name, movement in (
            ("objective", results["objective"]),
            ("optovar", results["optovar"]),
            ("reflector", results["reflector"]),
            ("filterwheel", results["filterwheel"]),
        )
        if movement is not None
    ]
    if successful_moves:
        logger.info(
            f"Successfully moved {len(successful_moves)} changers: {', '.join(successful_moves)}"
        )
    if results["skipped"]:
        logger.info(
            f"Skipped {len(results['skipped'])} changers: {', '.join(results['skipped'])}"
        )
    return results
