# -*- coding: utf-8 -*-

#################################################################
# File        : processing_tools.py
# Version     : 0.0.1
# Author      : czsrh
# Date        : 10.05.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk.
#
# Copyright (c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################

import numpy as np


def calc_normvar(img2d):
    """Determine normalized focus value for a 2D image
    - based on algorithm F - 11 "Normalized Variance"
    - Taken from: Sun et al., 2004. MICROSCOPY RESEARCH AND TECHNIQUE 65, 139–149.
    - Maximum value is best-focused, decreasing as defocus increases

    :param img2d: 2D image
    :type img2d: NumPy.Array
    :return: normalized focus value for the 2D image
    :rtype: float
    """

    mean = np.mean(img2d)
    height = img2d.shape[0]
    width = img2d.shape[1]

    # subtract the mean and sum up the whole array
    fi = (img2d - mean)**2
    b = np.sum(fi)

    # calculate the normalized variance value
    normvar = b / (height * width * mean)

    return normvar
