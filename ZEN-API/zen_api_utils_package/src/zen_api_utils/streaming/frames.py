"""Decode and validate ZEN pixel-stream payloads."""

from __future__ import annotations

import numpy as np
from zen_api.acquisition.v1beta import PixelType

PIXEL_FORMATS: dict[PixelType, tuple[np.dtype, int]] = {
    PixelType.GRAY8: (np.dtype(np.uint8), 1),
    PixelType.GRAY16: (np.dtype(np.uint16), 1),
    PixelType.BGR24: (np.dtype(np.uint8), 3),
    PixelType.BGR48: (np.dtype(np.uint16), 3),
}

GRAYSCALE_PIXEL_DTYPES: dict[PixelType, np.dtype] = {
    PixelType.GRAY8: np.dtype(np.uint8),
    PixelType.GRAY16: np.dtype(np.uint16),
}


def decode_frame(
    raw_data: bytes,
    dtype: np.dtype,
    width: int,
    height: int,
) -> np.ndarray:
    """Decode a row-major grayscale payload with a caller-supplied dtype."""
    expected_bytes = height * width * dtype.itemsize
    if len(raw_data) != expected_bytes:
        raise ValueError(
            f"Pixel payload has {len(raw_data)} bytes; expected " f"{expected_bytes} for {width}x{height} {dtype}"
        )
    frame = np.frombuffer(raw_data, dtype=dtype).reshape((height, width))
    return np.ascontiguousarray(frame, dtype=dtype)


def decode_pixel_payload(
    raw_data: bytes,
    width: int,
    height: int,
    pixel_type: PixelType,
) -> np.ndarray:
    """Decode a ZEN payload using its protocol pixel type metadata."""
    try:
        dtype, components = PIXEL_FORMATS[pixel_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported pixel type: {getattr(pixel_type, 'name', pixel_type)}") from exc

    shape = (height, width) if components == 1 else (height, width, components)
    expected_bytes = height * width * components * dtype.itemsize
    if len(raw_data) != expected_bytes:
        raise ValueError(
            f"Payload has {len(raw_data)} bytes, expected {expected_bytes} for "
            f"{width}x{height} {getattr(pixel_type, 'name', pixel_type)}"
        )
    return np.ascontiguousarray(np.frombuffer(raw_data, dtype=dtype).reshape(shape), dtype=dtype)


def runtime_grayscale_dtype(
    pixel_type: PixelType,
    payload_size: int,
    width: int,
    height: int,
) -> np.dtype:
    """Return and validate the dtype reported by a streamed grayscale frame."""
    try:
        dtype = GRAYSCALE_PIXEL_DTYPES[pixel_type]
    except KeyError as exc:
        name = getattr(pixel_type, "name", str(pixel_type))
        raise ValueError(f"Unsupported streamed pixel type: {name}") from exc

    expected_size = width * height * dtype.itemsize
    if payload_size != expected_size:
        raise ValueError(
            f"Payload has {payload_size} bytes, expected {expected_size} for " f"{width}x{height} {pixel_type.name}"
        )
    return dtype
