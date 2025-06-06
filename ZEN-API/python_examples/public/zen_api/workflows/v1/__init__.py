# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: zen_api/workflows/v1/start_job_options.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass

import betterproto


@dataclass(eq=False, repr=False)
class StartJobOptions(betterproto.Message):
    """Start Job options."""

    result_path: str = betterproto.string_field(1)
    """
    A value indicating a path for saving a Job results in the file system.
     -- If value is given than Job output will be copied to given path in filesystem and not uploaded to ZEN Archive.
     Have to be in the Windows-supported directory path format (local drive or network share).
     -- If value is null (or empty/whitespace) than Job output will be uploaded to ZEN Archive and not copied to anywhere.
    """
