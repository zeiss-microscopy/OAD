#################################################################
# File        : cameras.py
# Institution : Carl Zeiss Microscopy GmbH
#
# Description : Camera management tools for ZEN API operations.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from dataclasses import dataclass

from zen_api_utils.compatibility import api_capabilities, api_operation

with api_capabilities("Camera information"):
    from zen_api.lm.hardware.v2 import (
        CameraServiceGetCameraRequest,
        CameraServiceGetCamerasRequest,
        CameraServiceStub,
        GetCameraData,
    )


@dataclass
class IntegerFrame:
    """Camera ROI in pixels, measured from its top-left corner."""

    x: int
    y: int
    width: int
    height: int


@dataclass
class IntegerSize:
    """Camera image dimensions in pixels."""

    width: int
    height: int


@dataclass
class CameraInfo:
    """Camera settings with exposure times in seconds and geometry in pixels.

    Frame coordinates and sizes are truncated to integers, matching the
    established conversion of the API's floating-point geometry.
    """

    available_binnings: list[str]
    binning: int
    binning_description: str
    exposure_time: float
    min_exposure_time: float
    max_exposure_time: float
    id: str
    name: str
    is_preset: bool
    frame: IntegerFrame
    max_frame_size: IntegerSize


@api_operation("Camera list", CameraServiceStub, methods=("get_cameras",))
async def get_cameras_info_LM(cameras_service: CameraServiceStub) -> list[CameraInfo]:
    """Return all camera settings in service order; communication errors propagate."""
    response = await cameras_service.get_cameras(CameraServiceGetCamerasRequest())
    return [_convert_camera_to_info(camera) for camera in response.cameras]


def _convert_camera_to_info(camera: GetCameraData) -> CameraInfo:
    """Convert generated camera data without changing exposure or binning values."""
    return CameraInfo(
        available_binnings=camera.available_binnings,
        binning=camera.binning,
        binning_description=camera.binning_description,
        exposure_time=camera.exposure_time,
        min_exposure_time=camera.min_exposure_time,
        max_exposure_time=camera.max_exposure_time,
        id=camera.id,
        name=camera.name,
        is_preset=camera.is_preset,
        frame=IntegerFrame(
            x=int(camera.frame.start_point.x),
            y=int(camera.frame.start_point.y),
            width=int(camera.frame.size.width),
            height=int(camera.frame.size.height),
        ),
        max_frame_size=IntegerSize(
            width=int(camera.max_frame_size.width),
            height=int(camera.max_frame_size.height),
        ),
    )


@api_operation("Camera information", CameraServiceStub, methods=("get_camera",))
async def get_camera_info_LM(
    cameras_service: CameraServiceStub, camera_id: str
) -> CameraInfo:
    """Return settings for one camera; invalid-ID and communication errors propagate."""
    response = await cameras_service.get_camera(
        CameraServiceGetCameraRequest(camera_id)
    )
    return _convert_camera_to_info(response.camera)
