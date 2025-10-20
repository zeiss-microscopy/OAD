# -*- coding: utf-8 -*-

#################################################################
# File        : cameras.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
# Description : Camera management tools for ZEN API operations.
#               Provides dataclasses and functions for retrieving
#               and managing camera information with integer-based
#               frame and size representations.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from zen_api_utils.misc import set_logging
from dataclasses import dataclass

# Import auto-generated ZEN API modules for camera control
from zen_api.lm.hardware.v2 import (
    CameraServiceGetCameraRequest,
    CameraServiceStub,  # Service interface for camera operations
    CameraServiceGetCamerasRequest,  # Request object for retrieving all cameras
)

# Initialize logger for this module
logger = set_logging()


@dataclass
class IntegerFrame:
    """
    Frame representation with integer coordinates.

    Replaces DoubleFrame from ZEN API to avoid floating-point precision issues
    and provide cleaner integer-based coordinate handling.

    Attributes:
        x (int): X-coordinate of the frame's starting point (left edge)
        y (int): Y-coordinate of the frame's starting point (top edge)
        width (int): Width of the frame in pixels
        height (int): Height of the frame in pixels
    """

    x: int
    y: int
    width: int
    height: int


@dataclass
class IntegerSize:
    """
    Size representation with integer dimensions.

    Replaces DoubleSize from ZEN API to provide cleaner integer-based
    dimension handling without floating-point precision concerns.

    Attributes:
        width (int): Width dimension in pixels
        height (int): Height dimension in pixels
    """

    width: int
    height: int


@dataclass
class CameraInfo:
    """
    Comprehensive camera information container.

    Contains all relevant camera parameters converted to appropriate data types
    for easier handling and processing. Frame and size information is converted
    to integer-based representations for precision and convenience.

    Attributes:
        available_binnings (list[str]): List of available binning modes (e.g., "1x1", "2x2")
        binning (int): Current binning factor
        binning_description (str): Human-readable description of current binning
        exposure_time (float): Current exposure time in seconds
        min_exposure_time (float): Minimum allowed exposure time in seconds
        max_exposure_time (float): Maximum allowed exposure time in seconds
        id (str): Unique camera identifier
        name (str): Human-readable camera name
        is_preset (bool): Whether camera settings are from a preset configuration
        frame (IntegerFrame): Current camera frame/ROI with integer coordinates
        max_frame_size (IntegerSize): Maximum possible frame size with integer dimensions
    """

    available_binnings: list[str]  # Available binning options
    binning: int  # Current binning factor
    binning_description: str  # Description of current binning mode
    exposure_time: float  # Current exposure time [seconds]
    min_exposure_time: float  # Minimum exposure time [seconds]
    max_exposure_time: float  # Maximum exposure time [seconds]
    id: str  # Unique camera identifier
    name: str  # Camera display name
    is_preset: bool  # Whether using preset configuration
    frame: IntegerFrame  # Current frame/ROI (integer coordinates)
    max_frame_size: IntegerSize  # Maximum frame size (integer dimensions)


async def get_cameras_info_LM(cameras_service: CameraServiceStub) -> list[CameraInfo]:
    """
    Retrieve comprehensive information about all available cameras.

    Queries the ZEN API camera service to get detailed information about all
    cameras in the system, including their current settings, capabilities,
    and frame configurations. Converts ZEN API's DoubleFrame and DoubleSize
    objects to integer-based representations for easier handling.

    Args:
        cameras_service (CameraServiceStub): Connected camera service stub for API calls

    Returns:
        list[CameraInfo]: List of camera information objects with converted data types

    Raises:
        Exception: If camera service communication fails or camera data is inaccessible

    Example:
        >>> channel, metadata = initialize_zenapi("config.ini")
        >>> camera_service = CameraServiceStub(channel=channel, metadata=metadata)
        >>> cameras = await get_cameras_list_LM(camera_service)
        >>> for camera in cameras:
        ...     print(f"Camera: {camera.name}, Size: {camera.max_frame_size.width}x{camera.max_frame_size.height}")
    """

    # Request all camera information from the ZEN API service
    camera_response = await cameras_service.get_cameras(CameraServiceGetCamerasRequest())

    camera_list = []

    # Process each camera in the response
    for camera in camera_response.cameras:
        # Use helper function to convert camera data
        camera_info = _convert_camera_to_info(camera)
        camera_list.append(camera_info)

    return camera_list


def _convert_camera_to_info(camera) -> CameraInfo:
    """
    Convert a single ZEN API camera object to CameraInfo dataclass.

    Private helper function to eliminate code duplication between
    get_cameras_info_LM and get_camera_info_LM functions.

    Args:
        camera: ZEN API camera object with frame and max_frame_size attributes

    Returns:
        CameraInfo: Converted camera information with integer-based coordinates
    """
    # Convert ZEN API's DoubleFrame to our IntegerFrame
    # DoubleFrame structure: start_point.x/y + size.width/height
    integer_frame = IntegerFrame(
        x=int(camera.frame.start_point.x),  # Convert start X to integer
        y=int(camera.frame.start_point.y),  # Convert start Y to integer
        width=int(camera.frame.size.width),  # Convert frame width to integer
        height=int(camera.frame.size.height),  # Convert frame height to integer
    )

    # Convert ZEN API's DoubleSize to our IntegerSize
    # DoubleSize structure: width + height
    integer_max_frame_size = IntegerSize(
        width=int(camera.max_frame_size.width),  # Convert max width to integer
        height=int(camera.max_frame_size.height),  # Convert max height to integer
    )

    # Create comprehensive camera information object
    return CameraInfo(
        available_binnings=camera.available_binnings,  # List of binning options
        binning=camera.binning,  # Current binning factor
        binning_description=camera.binning_description,  # Binning description
        exposure_time=camera.exposure_time,  # Current exposure [s]
        min_exposure_time=camera.min_exposure_time,  # Min exposure limit [s]
        max_exposure_time=camera.max_exposure_time,  # Max exposure limit [s]
        id=camera.id,  # Unique camera ID
        name=camera.name,  # Camera display name
        is_preset=camera.is_preset,  # Using preset config?
        frame=integer_frame,  # Current frame/ROI
        max_frame_size=integer_max_frame_size,  # Maximum frame size
    )


async def get_camera_info_LM(cameras_service: CameraServiceStub, camera_id: str) -> CameraInfo:
    """
    Retrieve comprehensive information about a specific camera by its ID.

    Queries the ZEN API camera service to get detailed information about a
    specific camera identified by its unique ID, including its current
    settings, capabilities, and frame configurations. Converts ZEN API's
    DoubleFrame and DoubleSize objects to integer-based representations for
    easier handling.

    Args:
        cameras_service (CameraServiceStub): Connected camera service stub for API calls
        camera_id (str): Unique identifier of the camera to retrieve

    Returns:
        CameraInfo: Camera information object with converted data types

    Raises:
        Exception: If camera service communication fails or camera ID is invalid

    Example:
        >>> channel, metadata = initialize_zenapi("config.ini")
        >>> camera_service = CameraServiceStub(channel=channel, metadata=metadata)
        >>> camera = await get_camera_info_LM(camera_service, "camera_001")
        >>> print(f"Camera: {camera.name}, Binning: {camera.binning}")
    """

    # Request specific camera information from the ZEN API service
    single_camera_response = await cameras_service.get_camera(CameraServiceGetCameraRequest(camera_id))

    # Use helper function to convert camera data (eliminates code duplication)
    return _convert_camera_to_info(single_camera_response.camera)
