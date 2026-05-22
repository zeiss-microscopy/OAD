# -*- coding: utf-8 -*-

#################################################################
# File        : image_analysis.py
# Author      : SRh
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

from pathlib import Path
from typing import Sequence, Tuple, List

from czitools.read_tools import read_tools
from processing_tools import ArrayProcessor


async def run_analysis(
    czi_path: Path | str,
    measure_properties: Sequence[str] = ("label", "area", "centroid", "bbox"),
) -> List[int]:
    """
    Read a CZI file and count segmented objects on every Z-plane.

    Only the first channel (C=0) is processed.  Otsu thresholding is applied
    to each 2-D plane; small objects below *max_size_remove* pixels are
    discarded before counting.

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
    """
    array6d, mdata = read_tools.read_6darray(
        czi_path,
        zoom=1.0,
        planes={"C": (0, 0)},
        adapt_metadata=True,
        use_dask=False,
        use_xarray=False,
    )

    objects_per_plane: List[int] = []

    for zplane in range(mdata.image.SizeZ):
        # Extract a single 2-D (Y, X) plane from the 6-D array (S, T, C, Z, Y, X).
        # Scene, timepoint, and channel are all fixed to index 0.
        img2d = array6d[0, 0, 0, zplane, :, :]

        # Otsu threshold → binary mask
        ap = ArrayProcessor(img2d)
        pro2d = ap.apply_otsu_threshold()

        # Label connected objects, remove small debris, measure properties
        ap = ArrayProcessor(pro2d)
        _labeled, num_objects, _props = ap.label_objects(
            max_size_remove=100,
            label_rgb=False,
            orig_image=None,
            bg_label=0,
            measure_params=True,
            measure_properties=tuple(measure_properties),
        )

        objects_per_plane.append(num_objects)

    return objects_per_plane
