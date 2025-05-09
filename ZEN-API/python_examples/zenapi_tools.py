# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_tools.py
# Author      : SRh, JSm
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


import configparser
import ssl
from grpclib.client import Channel
from typing import List, Tuple
from pathlib import Path

# from pydantic.error_wrappers import ValidationError
from pydantic import ValidationError
from dataclasses import dataclass, field
from public.zen_api.common.v1 import DoublePoint
from loguru import logger
import sys
import os


def set_logging():
    """
    Configures the logging settings for the application.
    This function removes any existing loggers and sets up a new logger
    that outputs to the standard output stream (sys.stdout). The log
    messages are colorized and formatted to include the timestamp, log
    level, and message.
    Returns:
        logger (Logger): The configured logger instance.
    """

    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time}s</green> - <level>{level}</level> - <level>{message}</level>",
    )

    return logger


def initialize_zenapi(
    config_file: str = "config.ini",
) -> Tuple[Channel, List[Tuple[str, str]]]:
    """
    Create an gRPC channel for ZEN-API using the specified configuration file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        Tuple consisting of gRPC Channel and metadata as a list of tuples.
    """

    # check if config file exists
    if not Path(config_file).exists():
        logger.error(f"Configuration file {config_file} does not exist.")
        logger.info("Searching for configuration file...")
        config_file = find_file(config_file)
        if config_file:
            logger.info(f"Configuration file found at {config_file}.")
        else:
            logger.error(f"Configuration file {config_file} not found.")
            raise FileNotFoundError(f"Configuration file {config_file} does not exist.")

    # get the configuration
    config = configparser.ConfigParser()
    config.read(config_file)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Load a “certification authority” (CA) certificate
    context.load_verify_locations(cafile=config["api"]["cert_file"])
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True

    # Set protocol which should be used during the SSL/TLS handshake
    context.set_alpn_protocols(["h2"])
    channel = Channel(
        host=config["api"]["host"], port=int(config["api"]["port"]), ssl=context
    )
    metadata = [("control-token", config["api"]["control-token"])]

    return channel, metadata


def path_validator(v):
    """Returns a Path object.

    Args:
        v: A string or Path object.

    Returns:
        A Path object.

    Raises:
        ValidationError: If the value is not a valid path.
    """
    if isinstance(v, (str, Path)):
        return Path(v)
    raise ValidationError("value is not a valid path")


def find_file(filename: str, root_dir: str | os.PathLike | None = None) -> str | None:
    """
    Recursively search for a file and return its absolute path.

    Parameters
    ----------
    filename : str
        Name of the file to locate.
    root_dir : str | os.PathLike | None, optional
        Directory to start searching from.
        • None (default) → directory that contains the running script
        • Any valid path → search starts there

    Returns
    -------
    str | None
        Absolute path to the first match, or None if not found.
    """
    # Resolve default start dir
    if root_dir is None:
        root_dir = (
            Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
        )

    root_dir = Path(root_dir)

    for path in root_dir.rglob("*"):
        if path.name == filename:
            return str(path.resolve())

    return None


@dataclass
class TileRegionRectangle:
    """
    Represents a rectangular tile region.
    All units are in [m].
    """

    id: int = field(init=False, default=None)
    center_x: float = field(init=False, default=None)
    center_y: float = field(init=False, default=None)
    width: float = field(init=False, default=None)
    height: float = field(init=False, default=None)
    zvalue: float = field(init=False, default=None)


@dataclass
class TileRegionPolygon:
    """
    Represents a polygon tile region.
    All units are in [m].
    """

    id: int = field(init=False, default=None)
    polygon: List[DoublePoint] = field(init=False, default=None)
    zvalue: float = field(init=False, default=None)


@dataclass
class TileRegionEllipse:
    """
    Represents an ellipse tile region.
    All units are in [m].
    """

    id: int = field(init=False, default=None)
    center_x: float = field(init=False, default=None)
    center_y: float = field(init=False, default=None)
    x_diameter: float = field(init=False, default=None)  # diameter in x-direction
    y_diameter: float = field(init=False, default=None)  # diameter in y-direction
    zvalue: float = field(init=False, default=None)
