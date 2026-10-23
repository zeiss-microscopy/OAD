import numpy as np
import pytest

from zen_api.acquisition.v1beta import PixelType
from zen_api_utils.streaming.frames import decode_frame, decode_pixel_payload, runtime_grayscale_dtype


def test_decode_frame_validates_and_preserves_shape() -> None:
    raw_data = np.array([[1, 2], [3, 4]], dtype=np.uint16).tobytes()

    result = decode_frame(raw_data, np.dtype(np.uint16), width=2, height=2)

    np.testing.assert_array_equal(result, [[1, 2], [3, 4]])
    assert result.flags.c_contiguous


def test_decode_pixel_payload_supports_bgr() -> None:
    raw_data = bytes(range(6))

    result = decode_pixel_payload(raw_data, width=2, height=1, pixel_type=PixelType.BGR24)

    assert result.shape == (1, 2, 3)
    assert result.tolist() == [[[0, 1, 2], [3, 4, 5]]]


def test_runtime_grayscale_dtype_rejects_wrong_payload_size() -> None:
    with pytest.raises(ValueError, match="expected 8"):
        runtime_grayscale_dtype(PixelType.GRAY16, payload_size=2, width=2, height=2)
