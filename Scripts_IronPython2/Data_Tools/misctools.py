# -*- coding: utf-8 -*-

#################################################################
# File       : misctooly.py
# Version    : 0.1
# Author     : czsrh
# Date       : 21.06.2016
# Institution : Carl Zeiss Microscopy GmbH
#
# Beta Version: Use at your own risk!
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


def calc_series_range(total_series, scenes, sceneID):

    sps = total_series / scenes  # series_per_scence = sps
    series_seq = range(sceneID * sps - sps, sps * sceneID)

    return series_seq


def calc_series_range_well(wellnumber, imgperwell):
    """
    this function can be used when the number of positions or scenes per well is equal for every well.
    The well numbers start with Zero and have nothing to do with the actual wellID, e.g. C2
    """
    seriesseq = range(wellnumber * imgperwell,  wellnumber * imgperwell + imgperwell, 1)

    return seriesseq


def find_index_byname(lst, element):

    # find all indices for a certain keyword with all list
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)

    return result


def get_entries(lst, ids, exclude=None):

    # get all entries from a list given their indices
    entries = []
    for i in range(0, len(ids)):

        entry = lst[ids[i]]
        if entry != exclude:
            entries.append(entry)

    return entries
