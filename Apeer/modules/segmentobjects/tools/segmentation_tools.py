# -*- coding: utf-8 -*-

#################################################################
# File        : segmentation_tools.py
# Version     : 0.4
# Author      : czsrh
# Date        : 10.12.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################


import sys
from time import process_time, perf_counter
import os
from glob import glob
import logging
import numpy as np
import pandas as pd

from skimage import io, measure, segmentation
from skimage import exposure
from skimage.exposure import rescale_intensity
from skimage.morphology import watershed, dilation
from skimage.morphology import white_tophat, black_tophat, disk, square, ball, closing, square
from skimage.morphology import remove_small_objects, remove_small_holes
from skimage.feature import peak_local_max
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu, threshold_triangle, rank, median, gaussian
from skimage.segmentation import clear_border
from skimage.segmentation import random_walker
from skimage.color import label2rgb
from skimage.util import invert

from scipy.ndimage import distance_transform_edt
from scipy import ndimage


def apply_watershed(binary, min_distance=10):
    """Apply normal watershed to a binary image

    :param binary: binary images from segmentation
    :type binary: NumPy.Array
    :param min_distance: minimum peak distance [pixel], defaults to 10
    :type min_distance: int, optional
    :return: mask - mask with separeted objects
    :rtype: NumPy.Array
    """

    # create distance map
    distance = ndimage.distance_transform_edt(binary)

    # determine local maxima
    local_maxi = peak_local_max(distance,
                                min_distance=min_distance,
                                indices=False,
                                labels=binary)

    # label maxima
    markers, num_features = ndimage.label(local_maxi)

    # apply watershed
    mask = watershed(-distance, markers,
                     mask=binary,
                     watershed_line=True).astype(np.int)

    return mask


def apply_watershed_adv(image2d,
                        segmented,
                        filtermethod_ws='median',
                        filtersize_ws=3,
                        min_distance=2,
                        radius=1):
    """Apply advanced watershed to a binary image

    :param image2d: 2D image with pixel intensities
    :type image2d: NumPy.Array
    :param segmented: binary images from initial segmentation
    :type segmented: NumPy.Array
    :param filtermethod_ws: choice of filter method, defaults to 'median'
    :type filtermethod_ws: str, optional
    :param filtersize_ws: size paramater for the selected filter, defaults to 3
    :type filtersize_ws: int, optional
    :param min_distance: minimum peak distance [pixel], defaults to 2
    :type min_distance: int, optional
    :param radius: radius for dilation disk, defaults to 1
    :type radius: int, optional
    :return: mask - binary mask with separated objects
    :rtype: NumPy.Array
    """

    # convert to float
    image2d = image2d.astype(np.float)

    # rescale 0-1
    image2d = rescale_intensity(image2d, in_range='image', out_range=(0, 1))

    # filter image
    if filtermethod_ws == 'median':
        image2d = median(image2d, selem=disk(filtersize_ws))
    if filtermethod_ws == 'gauss':
        image2d = gaussian(image2d, sigma=filtersize_ws, mode='reflect')

    # create the seeds
    peaks = peak_local_max(image2d,
                           labels=label(segmented),
                           min_distance=min_distance,
                           indices=False)

    # create the seeds
    seed = dilation(peaks, selem=disk(radius))

    # create watershed map
    watershed_map = -1 * distance_transform_edt(segmented)

    # create mask
    mask = watershed(watershed_map,
                     markers=label(seed),
                     mask=segmented,
                     watershed_line=True).astype(np.int)

    return mask


def segment_threshold(image2d,
                      filtermethod='median',
                      filtersize=3,
                      threshold='triangle',
                      split_ws=True,
                      min_distance=30,
                      ws_method='ws_adv',
                      radius=1,
                      dtypemask=np.int16):
    """Segment an image using the following steps:
    - filter image
    - threshold image
    - apply watershed

    :param image2d: 2D image with pixel intensities
    :type image2d: NumPy.Array
    :param filtermethod: choice of filter method, defaults to 'median'
    :type filtermethod: str, optional
    :param filtersize: size paramater for the selected filter, defaults to 3
    :type filtersize: int, optional
    :param threshold: choice of thresholding method, defaults to 'triangle'
    :type threshold: str, optional
    :param split_ws: enable splitting using watershed, defaults to True
    :type split_ws: bool, optional
    :param min_distance: minimum peak distance [pixel], defaults to 30
    :type min_distance: int, optional
    :param ws_method: choice of watershed method, defaults to 'ws_adv'
    :type ws_method: str, optional
    :param radius: radius for dilation disk, defaults to 1
    :type radius: int, optional
    :param dtypemask: datatype of output mask, defaults to np.int16
    :type dtypemask: np.dtype, optional
    :return: mask - binary mask
    :rtype: NumPy.Array
    """

    # filter image
    if filtermethod == 'none' or filtermethod == 'None':
        image2d_filtered = image2d
    if filtermethod == 'median':
        image2d_filtered = median(image2d, selem=disk(filtersize))
    if filtermethod == 'gauss':
        image2d_filtered = gaussian(image2d, sigma=filtersize, mode='reflect')

    # threshold image and run marker-based watershed
    binary = autoThresholding(image2d_filtered, method=threshold)

    # apply watershed
    if split_ws:

        if ws_method == 'ws':
            mask = apply_watershed(binary,
                                   min_distance=min_distance)

        if ws_method == 'ws_adv':
            mask = apply_watershed_adv(image2d, binary,
                                       min_distance=min_distance,
                                       radius=radius)

    if not split_ws:
        # label the objects
        mask, num_features = ndimage.label(binary)
        mask = mask.astype(np.int)

    return mask.astype(dtypemask)


def autoThresholding(image2d,
                     method='triangle',
                     radius=10,
                     value=50):
    """Autothreshold an 2D intensity image which is calculated using:
    binary = image2d >= thresh

    :param image2d: input image for thresholding
    :type image2d: NumPy.Array
    :param method: choice of thresholding method, defaults to 'triangle'
    :type method: str, optional
    :param radius: radius of disk when using local Otsu threshold, defaults to 10
    :type radius: int, optional
    :param value: manual threshold value, defaults to 50
    :type value: int, optional
    :return: binary - binary mask from thresholding
    :rtype: NumPy.Array
    """

    # calculate global Otsu threshold
    if method == 'global_otsu':
        thresh = threshold_otsu(image2d)

    # calculate local Otsu threshold
    if method == 'local_otsu':
        thresh = rank.otsu(image2d, disk(radius))

    if method == 'value_based':
        thresh = value

    if method == 'triangle':
        thresh = threshold_triangle(image2d)

    binary = image2d >= thresh

    return binary


def cutout_subimage(image2d,
                    startx=0,
                    starty=0,
                    width=100,
                    height=200):
    """Cutout a subimage ot of a bigger image

    :param image2d: the original image
    :type image2d: NumPy.Array
    :param startx: startx, defaults to 0
    :type startx: int, optional
    :param starty: starty, defaults to 0
    :type starty: int, optional
    :param width: width, defaults to 100
    :type width: int, optional
    :param height: height, defaults to 200
    :type height: int, optional
    :return: image2d - subimage cutted out from original image2d
    :rtype: NumPy.Array
    """

    image2d = image2d[starty:starty + height, startx:startx + width]

    return image2d


def subtract_background(image,
                        elem='disk',
                        radius=50,
                        light_bg=False):
    """Background substraction using structure element.
    Slightly adapted from: https://forum.image.sc/t/background-subtraction-in-scikit-image/39118/4

    :param image: input image
    :type image: NumPy.Array
    :param elem: type of the structure element, defaults to 'disk'
    :type elem: str, optional
    :param radius: size of structure element [pixel], defaults to 50
    :type radius: int, optional
    :param light_bg: light background, defaults to False
    :type light_bg: bool, optional
    :return: image with background subtracted
    :rtype: NumPy.Array
    """
    # use 'ball' here to get a slightly smoother result at the cost of increased computing time
    if elem == 'disk':
        str_el = disk(radius)
    if elem == 'ball':
        str_el = ball(radius)

    if light_bg:
        img_subtracted = black_tophat(image, str_el)
    if not light_bg:
        img_subtracted = white_tophat(image, str_el)

    return img_subtracted
