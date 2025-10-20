# -*- coding: utf-8 -*-

#################################################################
# File        : stage_xyz.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    FocusServiceGetPositionRequest,
    FocusServiceMoveToRequest,
    FocusServiceStub,
    StageServiceGetPositionRequest,
    StageServiceMoveToRequest,
    StageServiceStub
)

from zen_api_utils.misc import set_logging

logger = set_logging()


@dataclass
class PosXYZ:
    """
    PosXYZ is a data class that represents a position in 3D space with coordinates
    specified in meters and automatically calculates their equivalent values in microns.

    Attributes:
        x_meter (float): The x-coordinate in meters.
        y_meter (float): The y-coordinate in meters.
        z_meter (float, optional): The z-coordinate in meters. Defaults to None if not provided.
        x_micron (float): The x-coordinate in microns, calculated from x_meter.
        y_micron (float): The y-coordinate in microns, calculated from y_meter.
        z_micron (float): The z-coordinate in microns, calculated from z_meter.
    Methods:
        __post_init__():
            Automatically converts the meter values (x_meter, y_meter, z_meter)
            to micron values (x_micron, y_micron, z_micron) after initialization.
    """

    x_meter: float  # x position in [meter]
    y_meter: float  # y position in [meter]
    z_meter: float = field(default=None)  # z position in [meter], optional with default value None

    def __post_init__(self):
        """
        Initializes the micron values for x, y, and z based on their meter values.
        If z_meter is None, z_micron will also be None.
        """
        self.x_micron = self.x_meter * 1e6
        self.y_micron = self.y_meter * 1e6
        self.z_micron = self.z_meter * 1e6 if self.z_meter is not None else None


# Define a class to represent a StageMark
class StageMark:
    """
    Represents a stage mark with coordinates and an optional conversion to zero-based indexing and meters.
    Attributes:
        index (int): The index of the item, adjusted to zero-based indexing if specified.
        x (float): The x-coordinate of the stage mark, optionally converted to meters.
        y (float): The y-coordinate of the stage mark, optionally converted to meters.
        z (float): The z-coordinate of the stage mark, optionally converted to meters.
    Args:
        item_index (int): The original index of the item.
        x (float): The x-coordinate of the stage mark.
        y (float): The y-coordinate of the stage mark.
        z (float): The z-coordinate of the stage mark.
        convert_to_zero_based (bool, optional): Whether to convert the index to zero-based. Defaults to True.
        convert_to_meter (bool, optional): Whether to convert the coordinates to meters. Defaults to True.
    """

    def __init__(self, item_index, x, y, z, convert_to_zero_based=True, convert_to_meter=True):

        self.index = int(item_index) - 1 if convert_to_zero_based else int(item_index)
        if convert_to_meter:
            self.x = float(x) * 1e-6
            self.y = float(y) * 1e-6
            self.z = float(z) * 1e-6
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def __repr__(self):
        return f"StageMark(ItemIndex={self.index}, X={self.x}, Y={self.y}, Z={self.z})"


# Function to parse the XML file and create a list of StageMark objects
def parse_stage_marks(file_path: str | Path):
    """
    Parses an XML file to extract StageMark elements and their attributes.
    
    Args:
        file_path (str | Path): The path to the XML file to be parsed. 
                                Can be a string or Path object.
    
    Returns:
        list: A list of StageMark objects, each representing a StageMark element
              from the XML file. Each object contains the attributes:
              - index (int): The ItemIndex attribute (converted to zero-based).
              - x (float): The X coordinate in meters.
              - y (float): The Y coordinate in meters.
              - z (float): The Z coordinate in meters.
    
    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.

    Example File Content:
        <?xml version="1.0" encoding="utf-8"?>
        <StageMarks>
        <StageMark ItemIndex="1" X="30942.246" Y="10873.572" Z="-8000" />
        <StageMark ItemIndex="2" X="40870.512" Y="10207.245" Z="-8000" />
        <StageMark ItemIndex="3" X="47667.044" Y="10107.296" Z="-8000" />
        <StageMark ItemIndex="4" X="56662.453" Y="10540.409" Z="-8000" />
        <StageMark ItemIndex="5" X="31308.725" Y="19635.767" Z="-8000" />
        <StageMark ItemIndex="6" X="39704.441" Y="19402.553" Z="-8000" />
        <StageMark ItemIndex="7" X="48266.737" Y="18802.859" Z="-8000" />
        <StageMark ItemIndex="8" X="56196.024" Y="18869.491" Z="-8000" />
        </StageMarks>
    """
    # Convert to Path object and check if file exists
    xml_path = Path(file_path)
    if not xml_path.exists():
        raise FileNotFoundError(f"XML file not found: {xml_path}")
    
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # List to store StageMark objects
    stage_marks = []

    # Iterate over all StageMark elements in the XML
    for stage_mark in root.findall("StageMark"):
        index = stage_mark.get("ItemIndex")
        x = stage_mark.get("X")
        y = stage_mark.get("Y")
        z = stage_mark.get("Z")

        # Create a StageMark object and add it to the list
        stage_marks.append(StageMark(index, x, y, z, convert_to_zero_based=True, convert_to_meter=True))

    return stage_marks


class StageXYPosition:
    """
    Represents a position on a stage with X and Y coordinates.
    This class encapsulates the coordinates of a position on a stage system,
    typically used for microscopy or other precision positioning applications.
    Attributes:
        x (float): The X coordinate position in meters.
        y (float): The Y coordinate position in meters.
    Example:
        >>> position = StagePosition(10.5, 20.3)
        >>> print(position)
        (X: 10.5 m; Y: 20.3 m)
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(X: {self.x} m; Y: {self.y} m)"


async def get_stageXY_position_simple(simple_stage_service: StageServiceStub) -> StageXYPosition:
    """
    Get the current stage position using the simple stage service.
    Args:
        simple_stage_service (SimpleStageServiceStub): The simple stage service stub
            used to communicate with the stage hardware.
    Returns:
        StageXYPosition: An object containing the current X and Y coordinates
            of the stage position.
    Raises:
        Any exceptions that may be raised by the simple_stage_service.get_position() call.
    """
    response = await simple_stage_service.get_position(StageServiceGetPositionRequest())

    return StageXYPosition(response.x, response.y)


async def move_to_stageXY_position_simple(
    simple_stage_service: StageServiceStub, stage_positionXY: StageXYPosition
) -> None:
    """
    Move the stage to a specified XY position using the simple stage service.

    Args:
        simple_stage_service (SimpleStageServiceStub): The gRPC service stub for controlling the simple stage.
        stage_position (StageXYPosition): The target position containing x and y coordinates to move to.

    Returns:
        None

    Raises:
        grpc.RpcError: If the gRPC call fails or the stage movement encounters an error.
    """
    await simple_stage_service.move_to(StageServiceMoveToRequest(stage_positionXY.x, stage_positionXY.y))


async def move_xyz(channel, metadata, pos_xyz: PosXYZ) -> PosXYZ:
    """
    Asynchronously moves the stage and focus to specified X, Y, and Z positions and retrieves the updated positions.
    Args:
        channel: The gRPC channel used for communication with the services.
        metadata: Metadata for the gRPC requests.
        xpos (float): The target X-coordinate in microns.
        ypos (float): The target Y-coordinate in microns.
        zpos (float): The target Z-coordinate in microns.
    Returns:
        PosXYZ: An object containing the updated X, Y, and Z positions in meters.
    Raises:
        Any exceptions raised by the gRPC services during movement or position retrieval.
    """

    # Create instances of stage and focus services
    stage_service = StageServiceStub(channel=channel, metadata=metadata)
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)

    # check if pos_xyz.z_meter is None, if so use the current focus position
    if pos_xyz.z_meter is None:
        # Retrieve the current focus position in meters
        posZ = await focus_service.get_position(FocusServiceGetPositionRequest())
        pos_xyz.z_meter = posZ.value

    # Move the stage to the specified X and Y coordinates
    await stage_service.move_to(StageServiceMoveToRequest(x=pos_xyz.x_meter, y=pos_xyz.y_meter))
    # Move the focus to the specified Z position
    await focus_service.move_to(FocusServiceMoveToRequest(value=pos_xyz.z_meter))

    # Retrieve the current stage positions in microns
    posXY = await stage_service.get_position(StageServiceGetPositionRequest())
    posZ = await focus_service.get_position(FocusServiceGetPositionRequest())

    pos_xyz = PosXYZ(x_meter=posXY.x, y_meter=posXY.y, z_meter=posZ.value)

    return pos_xyz
