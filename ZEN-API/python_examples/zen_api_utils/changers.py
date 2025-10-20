# -*- coding: utf-8 -*-

#################################################################
# File        : changers.py
# Author      : SRh, JSm
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from typing import List

from zen_api_utils.misc import set_logging


# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    ObjectiveData,
    ObjectiveChangerServiceStub,
    ObjectiveChangerServiceGetObjectivesResponse,
    ObjectiveChangerServiceGetObjectivesRequest,
    ObjectiveChangerServiceMoveToRequest,
    OptovarData,
    OptovarServiceGetOptovarsResponse,
    OptovarServiceStub,
    OptovarServiceGetOptovarsRequest,
    OptovarServiceMoveToRequest,
    ReflectorChangerServiceGetReflectorsResponse,
    ReflectorData,
    ReflectorChangerServiceStub,
    ReflectorChangerServiceGetReflectorsRequest,
    ReflectorChangerServiceMoveToRequest,
    FilterWheelServiceGetFiltersResponse,
    FilterData,
    FilterWheelServiceStub,
    FilterWheelServiceGetFiltersRequest,
    FilterWheelServiceMoveToRequest,
)

# create logger
logger = set_logging()


def get_filter_by_position(filters: FilterWheelServiceGetFiltersResponse, position: int) -> FilterData | None:
    """
    Return the filter that matches the given position from the filters list.
    Args:
        filters (FilterWheelServiceGetFiltersResponse):
            An object containing a list of filters.
        position (int):
            The position of the filter to retrieve.
    Returns:
        FilterData | None:
            The filter at the specified position if found, otherwise None.
    """
    for filter in filters.filters:
        if filter.position == position:
            return filter
    return None


def get_used_filterwheel_positions(filters: FilterWheelServiceGetFiltersResponse) -> List[int]:
    """
    Generates a list of used filter positions from a collection of filter data.
    Args:
        filters (FilterWheelServiceGetFiltersResponse):
            An object containing a list of filters with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the filters.
    """

    used_positions: List[int] = []

    for filter in filters.filters:
        used_positions.append(filter.position)

    return used_positions


def get_reflector_by_position(
    reflectors: ReflectorChangerServiceGetReflectorsResponse, position: int
) -> ReflectorData | None:
    """
    Return the reflector that matches the given position from the reflectors list.
    Args:
        reflectors (ReflectorChangerServiceGetReflectorsResponse):
            An object containing a list of reflectors.
        position (int):
            The position of the reflector to retrieve.
    Returns:
        ReflectorData | None:
            The reflector at the specified position if found, otherwise None.
    """
    for reflector in reflectors.reflectors:
        if reflector.position == position:
            return reflector
    return None


def get_used_reflector_positions(reflectors: ReflectorChangerServiceGetReflectorsResponse) -> List[int]:
    """
    Generates a list of used reflector positions from a collection of reflector data.
    Args:
        reflectors (ReflectorChangerServiceGetReflectorsResponse):
            An object containing a list of reflectors with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the reflectors.
    """

    used_positions: List[int] = []

    for reflector in reflectors.reflectors:
        used_positions.append(reflector.position)

    return used_positions


def get_objective_by_position(
    objectives: ObjectiveChangerServiceGetObjectivesResponse, position: int
) -> ObjectiveData | None:
    """
    Return the objective that matches the given position from the objectives list.
    Args:
        objectives (ObjectiveChangerServiceGetObjectivesResponse):
            An object containing a list of objectives.
        position (int):
            The position of the objective to retrieve.
    Returns:
        ObjectiveData | None:
            The objective at the specified position if found, otherwise None.
    """
    for obj in objectives.objectives:
        if obj.position == position:
            return obj
    return None


def get_optovar_by_position(optovars: OptovarServiceGetOptovarsResponse, position: int) -> OptovarData | None:
    """
    Return the optovar that matches the given position from the objectives list.
    Args:
        objectives (OptovarServiceGetOptovarsResponse):
            An object containing a list of optovars.
        position (int):
            The position of the optovar to retrieve.
    Returns:
        OptovarData | None:
            The optovar at the specified position if found, otherwise None.
    """
    for opt in optovars.optovars:
        if opt.position == position:
            return opt
    return None


def get_used_objective_positions(objectives: ObjectiveChangerServiceGetObjectivesResponse) -> List[int]:
    """
    Generates a list of used objective positions from a collection of objective data.
    Args:
        objectives (ObjectiveChangerServiceGetObjectivesResponse):
            An object containing a list of objectives with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the objectives.
    """

    used_positions: List[int] = []

    for obj in objectives.objectives:
        used_positions.append(obj.position)

    return used_positions


def get_used_optovar_positions(optovars: OptovarServiceGetOptovarsResponse) -> List[int]:
    """
    Generates a list of used optovar positions from a collection of optovar data.
    Args:
        objectives (OptovarServiceGetOptovarsResponse):
            An object containing a list of optovars with their respective positions.
    Returns:
        List[int]:
            A list of all positions currently in use by the optovars.
    """

    used_positions: List[int] = []

    for opt in optovars.optovars:
        used_positions.append(opt.position)

    return used_positions


async def move_changers(
    channel,
    metadata,
    objectives=None,
    optovars=None,
    reflectors=None,
    filters=None,
    objective_position: int = None,
    optovar_position: int = None,
    reflector_position: int = None,
    filterwheel_position: int = None,
) -> dict:
    """
    Move microscope changers to specified positions based on keyword arguments.
    This function is robust and handles situations where not all services are available.

    Args:
        channel: gRPC channel for communication
        metadata: gRPC metadata for authentication
        objectives: Available objectives data (optional, will be fetched if service available)
        optovars: Available optovars data (optional, will be fetched if service available)
        reflectors: Available reflectors data (optional, will be fetched if service available)
        filters: Available filters data (optional, will be fetched if service available)
        objective_position (int, optional): Target position for objective changer
        optovar_position (int, optional): Target position for optovar changer
        reflector_position (int, optional): Target position for reflector changer
        filterwheel_position (int, optional): Target position for filterwheel changer

    Returns:
        dict: Dictionary containing the results of each movement operation with current positions.
              Includes 'skipped' entries for unavailable services and 'warnings' for service failures.

    Note:
        - If a service cannot be initialized, the operation will be skipped with a warning
        - Only successfully initialized services will be used for movement operations
        - The function continues execution even if some services fail to initialize

    Example:
        >>> # This will attempt to move all requested changers, skipping unavailable services
        >>> results = await move_changers(
        ...     channel=channel,
        ...     metadata=metadata,
        ...     objective_position=2,
        ...     optovar_position=1,
        ...     reflector_position=3,
        ...     filterwheel_position=2
        ... )
        >>> print(f"Successful moves: {[k for k, v in results.items() if v and v.get('status') == 'success']}")
        >>> print(f"Skipped services: {results['skipped']}")
    """
    results = {
        "objective": None,
        "optovar": None,
        "reflector": None,
        "filterwheel": None,
        "skipped": [],
        "warnings": [],
        "errors": [],
    }

    # Initialize services with error handling
    objchanger_service = None
    optovar_service = None
    reflector_service = None
    filterwheel_service = None

    try:
        # Try to initialize services - each with individual error handling
        if objective_position is not None:
            try:
                objchanger_service = ObjectiveChangerServiceStub(channel=channel, metadata=metadata)
            except Exception as e:
                warning_msg = f"Failed to initialize objective changer service: {str(e)} - skipping objective movement"
                results["warnings"].append(warning_msg)
                results["skipped"].append("objective")
                logger.warning(warning_msg)

        if optovar_position is not None:
            try:
                optovar_service = OptovarServiceStub(channel=channel, metadata=metadata)
            except Exception as e:
                warning_msg = f"Failed to initialize optovar service: {str(e)} - skipping optovar movement"
                results["warnings"].append(warning_msg)
                results["skipped"].append("optovar")
                logger.warning(warning_msg)

        if reflector_position is not None:
            try:
                reflector_service = ReflectorChangerServiceStub(channel=channel, metadata=metadata)
            except Exception as e:
                warning_msg = f"Failed to initialize reflector service: {str(e)} - skipping reflector movement"
                results["warnings"].append(warning_msg)
                results["skipped"].append("reflector")
                logger.warning(warning_msg)

        if filterwheel_position is not None:
            try:
                filterwheel_service = FilterWheelServiceStub(channel=channel, metadata=metadata)
            except Exception as e:
                warning_msg = f"Failed to initialize filterwheel service: {str(e)} - skipping filterwheel movement"
                results["warnings"].append(warning_msg)
                results["skipped"].append("filterwheel")
                logger.warning(warning_msg)

        # Fetch available components if not provided (only for successfully initialized services)
        if objective_position is not None and objchanger_service is not None:
            if objectives is None:
                try:
                    objectives = await objchanger_service.get_objectives(ObjectiveChangerServiceGetObjectivesRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch objectives data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("objective")
                    logger.error(error_msg)
                    objective_position = None  # Skip this changer

        if optovar_position is not None and optovar_service is not None:
            if optovars is None:
                try:
                    optovars = await optovar_service.get_optovars(OptovarServiceGetOptovarsRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch optovars data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("optovar")
                    logger.error(error_msg)
                    optovar_position = None  # Skip this changer

        if reflector_position is not None and reflector_service is not None:
            if reflectors is None:
                try:
                    reflectors = await reflector_service.get_reflectors(ReflectorChangerServiceGetReflectorsRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch reflectors data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("reflector")
                    logger.error(error_msg)
                    reflector_position = None  # Skip this changer

        if filterwheel_position is not None and filterwheel_service is not None:
            if filters is None:
                try:
                    filters = await filterwheel_service.get_filters(FilterWheelServiceGetFiltersRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch filters data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("filterwheel")
                    logger.error(error_msg)
                    filterwheel_position = None  # Skip this changer
        # Move objective changer (only if service available and position requested)
        if objective_position is not None and objchanger_service is not None:
            try:
                # Validate position exists
                target_objective = get_objective_by_position(objectives, objective_position)
                if target_objective is None:
                    raise ValueError(f"Invalid objective position: {objective_position}")

                await objchanger_service.move_to(
                    ObjectiveChangerServiceMoveToRequest(position_index=objective_position)
                )

                results["objective"] = {
                    "position": target_objective.position,
                    "name": target_objective.name,
                    "status": "success",
                }
                logger.info(f"Moved objective to position {objective_position}: {target_objective.name}")

            except Exception as e:
                error_msg = f"Failed to move objective to position {objective_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Move optovar changer (only if service available and position requested)
        if optovar_position is not None and optovar_service is not None:
            try:
                # Validate position exists
                target_optovar = get_optovar_by_position(optovars, optovar_position)
                if target_optovar is None:
                    raise ValueError(f"Invalid optovar position: {optovar_position}")

                await optovar_service.move_to(OptovarServiceMoveToRequest(position_index=optovar_position))

                results["optovar"] = {
                    "position": target_optovar.position,
                    "name": target_optovar.name,
                    "status": "success",
                }
                logger.info(f"Moved optovar to position {optovar_position}: {target_optovar.name}")

            except Exception as e:
                error_msg = f"Failed to move optovar to position {optovar_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Move reflector changer (only if service available and position requested)
        if reflector_position is not None and reflector_service is not None:
            try:
                # Validate position exists
                target_reflector = get_reflector_by_position(reflectors, reflector_position)
                if target_reflector is None:
                    raise ValueError(f"Invalid reflector position: {reflector_position}")

                await reflector_service.move_to(ReflectorChangerServiceMoveToRequest(position_index=reflector_position))

                results["reflector"] = {
                    "position": target_reflector.position,
                    "name": target_reflector.name,
                    "status": "success",
                }
                logger.info(f"Moved reflector to position {reflector_position}: {target_reflector.name}")

            except Exception as e:
                error_msg = f"Failed to move reflector to position {reflector_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Move filterwheel changer (only if service available and position requested)
        if filterwheel_position is not None and filterwheel_service is not None:
            try:
                # Validate position exists
                target_filter = get_filter_by_position(filters, filterwheel_position)
                if target_filter is None:
                    raise ValueError(f"Invalid filterwheel position: {filterwheel_position}")

                await filterwheel_service.move_to(FilterWheelServiceMoveToRequest(position_index=filterwheel_position))

                results["filterwheel"] = {
                    "position": target_filter.position,
                    "name": target_filter.name,
                    "status": "success",
                }
                logger.info(f"Moved filterwheel to position {filterwheel_position}: {target_filter.name}")

            except Exception as e:
                error_msg = f"Failed to move filterwheel to position {filterwheel_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Log summary of operations
        successful_moves = [k for k, v in results.items() if v and isinstance(v, dict) and v.get("status") == "success"]
        if successful_moves:
            logger.info(f"Successfully moved {len(successful_moves)} changers: {', '.join(successful_moves)}")

        if results["skipped"]:
            logger.info(
                f"Skipped {len(results['skipped'])} changers due to service issues: {', '.join(results['skipped'])}"
            )

    except Exception as e:
        error_msg = f"General error in move_changers: {str(e)}"
        results["errors"].append(error_msg)
        logger.error(error_msg)

    return results


async def move_changers_adv(
    objchanger_service: ObjectiveChangerServiceStub = None,
    optovar_service: OptovarServiceStub = None,
    reflector_service: ReflectorChangerServiceStub = None,
    filterwheel_service: FilterWheelServiceStub = None,
    objectives=None,
    optovars=None,
    reflectors=None,
    filters=None,
    objective_position: int = None,
    optovar_position: int = None,
    reflector_position: int = None,
    filterwheel_position: int = None,
) -> dict:
    """
    Advanced version of move_changers that accepts service stubs directly instead of channel & metadata.
    This is more efficient when you already have service stubs initialized and want to avoid redundant
    service stub creation. The function is robust and handles situations where not all services are available.

    Args:
        objchanger_service (ObjectiveChangerServiceStub, optional): Pre-initialized objective changer service
        optovar_service (OptovarServiceStub, optional): Pre-initialized optovar service
        reflector_service (ReflectorChangerServiceStub, optional): Pre-initialized reflector service
        filterwheel_service (FilterWheelServiceStub, optional): Pre-initialized filterwheel service
        objectives: Available objectives data (optional, will be fetched if None and service available)
        optovars: Available optovars data (optional, will be fetched if None and service available)
        reflectors: Available reflectors data (optional, will be fetched if None and service available)
        filters: Available filters data (optional, will be fetched if None and service available)
        objective_position (int, optional): Target position for objective changer
        optovar_position (int, optional): Target position for optovar changer
        reflector_position (int, optional): Target position for reflector changer
        filterwheel_position (int, optional): Target position for filterwheel changer

    Returns:
        dict: Dictionary containing the results of each movement operation with current positions.
              Includes 'skipped' entries for unavailable services and 'warnings' for missing services.

    Note:
        - If a position is specified but the corresponding service is not available, the operation will be skipped
        - Only available services will be used for movement operations
        - The function continues execution even if some services are unavailable

    Example:
        >>> # Only objective and optovar services available
        >>> objchanger_service = ObjectiveChangerServiceStub(channel=channel, metadata=metadata)
        >>> optovar_service = OptovarServiceStub(channel=channel, metadata=metadata)
        >>>
        >>> # This will move objective and optovar, skip reflector and filterwheel
        >>> results = await move_changers_adv(
        ...     objchanger_service=objchanger_service,
        ...     optovar_service=optovar_service,
        ...     objective_position=2,
        ...     optovar_position=1,
        ...     reflector_position=3,      # Will be skipped (no service)
        ...     filterwheel_position=2     # Will be skipped (no service)
        ... )
    """
    results = {
        "objective": None,
        "optovar": None,
        "reflector": None,
        "filterwheel": None,
        "skipped": [],
        "warnings": [],
        "errors": [],
    }

    try:
        # Check service availability and warn about missing services when positions are requested
        if objective_position is not None and objchanger_service is None:
            warning_msg = (
                f"Objective position {objective_position} requested but objchanger_service not available - skipping"
            )
            results["warnings"].append(warning_msg)
            results["skipped"].append("objective")
            logger.warning(warning_msg)

        if optovar_position is not None and optovar_service is None:
            warning_msg = f"Optovar position {optovar_position} requested but optovar_service not available - skipping"
            results["warnings"].append(warning_msg)
            results["skipped"].append("optovar")
            logger.warning(warning_msg)

        if reflector_position is not None and reflector_service is None:
            warning_msg = (
                f"Reflector position {reflector_position} requested but reflector_service not available - skipping"
            )
            results["warnings"].append(warning_msg)
            results["skipped"].append("reflector")
            logger.warning(warning_msg)

        if filterwheel_position is not None and filterwheel_service is None:
            warning_msg = f"Filterwheel position {filterwheel_position} requested but filterwheel_service not available - skipping"
            results["warnings"].append(warning_msg)
            results["skipped"].append("filterwheel")
            logger.warning(warning_msg)

        # Fetch available components if not provided (only for available services)
        if objective_position is not None and objchanger_service is not None:
            if objectives is None:
                try:
                    objectives = await objchanger_service.get_objectives(ObjectiveChangerServiceGetObjectivesRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch objectives data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("objective")
                    logger.error(error_msg)
                    objective_position = None  # Skip this changer

        if optovar_position is not None and optovar_service is not None:
            if optovars is None:
                try:
                    optovars = await optovar_service.get_optovars(OptovarServiceGetOptovarsRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch optovars data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("optovar")
                    logger.error(error_msg)
                    optovar_position = None  # Skip this changer

        if reflector_position is not None and reflector_service is not None:
            if reflectors is None:
                try:
                    reflectors = await reflector_service.get_reflectors(ReflectorChangerServiceGetReflectorsRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch reflectors data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("reflector")
                    logger.error(error_msg)
                    reflector_position = None  # Skip this changer

        if filterwheel_position is not None and filterwheel_service is not None:
            if filters is None:
                try:
                    filters = await filterwheel_service.get_filters(FilterWheelServiceGetFiltersRequest())
                except Exception as e:
                    error_msg = f"Failed to fetch filters data: {str(e)}"
                    results["errors"].append(error_msg)
                    results["skipped"].append("filterwheel")
                    logger.error(error_msg)
                    filterwheel_position = None  # Skip this changer

        # Move objective changer (only if service available and position requested)
        if objective_position is not None and objchanger_service is not None:
            try:
                # Validate position exists
                target_objective = get_objective_by_position(objectives, objective_position)
                if target_objective is None:
                    raise ValueError(f"Invalid objective position: {objective_position}")

                await objchanger_service.move_to(
                    ObjectiveChangerServiceMoveToRequest(position_index=objective_position)
                )

                results["objective"] = {
                    "position": target_objective.position,
                    "name": target_objective.name,
                    "status": "success",
                }
                logger.info(f"Moved objective to position {objective_position}: {target_objective.name}")

            except Exception as e:
                error_msg = f"Failed to move objective to position {objective_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Move optovar changer (only if service available and position requested)
        if optovar_position is not None and optovar_service is not None:
            try:
                # Validate position exists
                target_optovar = get_optovar_by_position(optovars, optovar_position)
                if target_optovar is None:
                    raise ValueError(f"Invalid optovar position: {optovar_position}")

                await optovar_service.move_to(OptovarServiceMoveToRequest(position_index=optovar_position))

                results["optovar"] = {
                    "position": target_optovar.position,
                    "name": target_optovar.name,
                    "status": "success",
                }
                logger.info(f"Moved optovar to position {optovar_position}: {target_optovar.name}")

            except Exception as e:
                error_msg = f"Failed to move optovar to position {optovar_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Move reflector changer (only if service available and position requested)
        if reflector_position is not None and reflector_service is not None:
            try:
                # Validate position exists
                target_reflector = get_reflector_by_position(reflectors, reflector_position)
                if target_reflector is None:
                    raise ValueError(f"Invalid reflector position: {reflector_position}")

                await reflector_service.move_to(ReflectorChangerServiceMoveToRequest(position_index=reflector_position))

                results["reflector"] = {
                    "position": target_reflector.position,
                    "name": target_reflector.name,
                    "status": "success",
                }
                logger.info(f"Moved reflector to position {reflector_position}: {target_reflector.name}")

            except Exception as e:
                error_msg = f"Failed to move reflector to position {reflector_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Move filterwheel changer (only if service available and position requested)
        if filterwheel_position is not None and filterwheel_service is not None:
            try:
                # Validate position exists
                target_filter = get_filter_by_position(filters, filterwheel_position)
                if target_filter is None:
                    raise ValueError(f"Invalid filterwheel position: {filterwheel_position}")

                await filterwheel_service.move_to(FilterWheelServiceMoveToRequest(position_index=filterwheel_position))

                results["filterwheel"] = {
                    "position": target_filter.position,
                    "name": target_filter.name,
                    "status": "success",
                }
                logger.info(f"Moved filterwheel to position {filterwheel_position}: {target_filter.name}")

            except Exception as e:
                error_msg = f"Failed to move filterwheel to position {filterwheel_position}: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Log summary of operations
        successful_moves = [k for k, v in results.items() if v and isinstance(v, dict) and v.get("status") == "success"]
        if successful_moves:
            logger.info(f"Successfully moved {len(successful_moves)} changers: {', '.join(successful_moves)}")

        if results["skipped"]:
            logger.info(
                f"Skipped {len(results['skipped'])} changers due to unavailable services: {', '.join(results['skipped'])}"
            )

    except Exception as e:
        error_msg = f"General error in move_changers_adv: {str(e)}"
        results["errors"].append(error_msg)
        logger.error(error_msg)

    return results
