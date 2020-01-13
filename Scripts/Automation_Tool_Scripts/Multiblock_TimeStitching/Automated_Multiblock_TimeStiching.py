#################################################################
# File       : Automated_Multiblock_TimeStitching.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# Generated automatically a timestitching for MultiBlock acquisition (ie: Experiment Designer)

# get the active image document
image = Zen.Application.Documents.ActiveDocument

if image.IsZenMultiBlockImage:
    # get number of blocks
    block_count = image.AcquisitionBlockCount

    # loop over blocks and stitch
    for i in range(0, block_count):
        timestitching = Zen.Processing.Utilities.MultiBlockTimeStitching(image, image.SelectBlockIndices(i))
        Zen.Application.Documents.Add(timestitching)

print('Done.')
