#################################################################
# File        : image_analysis.py
# Institution : Carl Zeiss Microscopy GmbH
#
# Reads a CZI file and runs a simple Otsu-threshold based object
# detection on every Z-plane of the first channel.
# Called by the analysis worker in analysis_queue.py.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import asyncio
from collections.abc import Sequence
from pathlib import Path

import numpy as np
from czitools.read_tools import read_tools
from processing_tools import ArrayProcessor


async def run_analysis(
    czi_path: Path | str,
    measure_properties: Sequence[str] = ("label", "area", "centroid", "bbox"),
) -> list[int]:
    """Run CZI analysis in a worker thread so microscope tasks can continue.

    Args:
        czi_path: Path to a grayscale CZI file.
        measure_properties: Region properties measured internally per object.

    Returns:
        Object counts for each Z-plane of the first scene, time, and channel.

    Raises:
        ValueError: If the reader returns no image data or no Z dimension.
    """
    return await asyncio.to_thread(
        _run_analysis_sync,
        czi_path,
        measure_properties,
    )


def _run_analysis_sync(
    czi_path: Path | str,
    measure_properties: Sequence[str],
) -> list[int]:
    """
    Read a CZI file and count segmented objects on every Z-plane.

    Only the first scene, time, and channel are processed. Otsu thresholding
    is applied to each 2-D plane; objects of at most 100 pixels are discarded
    before counting. RGB images are not supported by this example.

    The returned array axis order from ``read_6darray`` is:
        (S, T, C, Z, Y, X)
    With ``planes={"C": (0, 0)}`` the C dimension is restricted to a single
    slice (size 1), so we index with ``[0, 0, 0, zplane, :, :]`` to obtain a
    pure 2-D (Y, X) array as required by :class:`ArrayProcessor`.

    Args:
        czi_path: Absolute path to the CZI file to analyse.
        measure_properties: Sequence of ``skimage.measure.regionprops_table``
            property names to include in the per-object measurement table.

    Returns:
        List of per-plane object counts, one entry per Z-plane
        (index 0 = first Z-plane).

    Raises:
        ValueError: If the reader does not return image data or a Z dimension.
    """
    # Restricting C during reading avoids loading channels that this tutorial
    # does not analyze. Disabling Dask and xarray returns a plain NumPy array.
    array6d, mdata = read_tools.read_6darray(
        czi_path,
        zoom=1.0,
        planes={"C": (0, 0)},
        adapt_metadata=True,
        use_dask=False,
        use_xarray=False,
    )

    if array6d is None or mdata is None or mdata.image is None or mdata.image.SizeZ is None:
        raise ValueError("The CZI file does not contain readable image data with a Z dimension")

    # The guard above narrows these optional reader values for both readers and
    # static type checkers.
    size_z = mdata.image.SizeZ

    objects_per_plane: list[int] = []

    for zplane in range(size_z):
        # Extract a single 2-D (Y, X) plane from the 6-D array (S, T, C, Z, Y, X).
        # Scene, timepoint, and channel are all fixed to index 0.
        img2d = np.asarray(array6d[0, 0, 0, zplane, :, :])

        # Otsu automatically estimates a foreground threshold for this plane.
        ap = ArrayProcessor(img2d)
        pro2d = ap.apply_otsu_threshold()

        # Re-wrap the binary mask because ArrayProcessor stores the array it
        # operates on. Objects below 100 pixels are treated as debris.
        ap = ArrayProcessor(pro2d)
        _, num_objects, _ = ap.label_objects(
            max_size_remove=100,
            label_rgb=False,
            orig_image=None,
            bg_label=0,
            measure_params=True,
            measure_properties=tuple(measure_properties),
        )

        # Only counts are exported; the label image and property table are
        # deliberately discarded.
        objects_per_plane.append(num_objects)

    return objects_per_plane
