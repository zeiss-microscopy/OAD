# -*- coding: utf-8 -*-

#################################################################
# File        : czi_tools.py
# Version     : 0.0.2
# Author      : czsrh
# Date        : 24.09.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################

import os
from aicsimageio import AICSImage, imread, imread_dask
import aicspylibczi
import imgfileutils as imf
import itertools as it
from tqdm import tqdm, trange
from tqdm.contrib.itertools import product
import nested_dict as nd
import pandas as pd
import numpy as np
from datetime import datetime
import dateutil.parser as dt
from lxml import etree
import progressbar


def define_czi_planetable():

    df = pd.DataFrame(columns=['Subblock',
                               'Scene',
                               'Tile',
                               'T',
                               'Z',
                               'C',
                               'X [micron]',
                               'Y [micron]',
                               'Z [micron]',
                               'Time [s]',
                               'xstart',
                               'ystart',
                               'xwidth',
                               'ywidth'])

    return df


def get_czi_planetable(czifile):

    # get the czi object using pylibczi
    czi = aicspylibczi.CziFile(czifile)

    # get the czi metadata
    md, add = imf.get_metadata(czifile)

    # initialize the plane table
    df_czi = define_czi_planetable()

    # define subblock counter
    sbcount = -1

    # create progressbar
    #total = md['SizeS'] * md['SizeM'] * md['SizeT'] * md['SizeZ'] * md['SizeC']
    #pbar = tqdm(total=total)

    #pbar = progressbar.ProgressBar(max_value=total)
    # in case the CZI has the M-Dimension
    if md['czi_isMosaic']:

        for s, m, t, z, c in product(range(md['SizeS']),
                                     range(md['SizeM']),
                                     range(md['SizeT']),
                                     range(md['SizeZ']),
                                     range(md['SizeC'])):

            sbcount += 1
            # print(s, m, t, z, c)
            info = czi.read_subblock_rect(S=s, M=m, T=t, Z=z, C=c)

            # read information from subblock
            sb = czi.read_subblock_metadata(unified_xml=True,
                                            B=0,
                                            S=s,
                                            M=m,
                                            T=t,
                                            Z=z,
                                            C=c)

            try:
                time = sb.xpath('//AcquisitionTime')[0].text
                timestamp = dt.parse(time).timestamp()
            except IndexError as e:
                timestamp = 0.0

            try:
                xpos = np.double(sb.xpath('//StageXPosition')[0].text)
            except IndexError as e:
                xpos = 0.0

            try:
                ypos = np.double(sb.xpath('//StageYPosition')[0].text)
            except IndexError as e:
                ypos = 0.0

            try:
                zpos = np.double(sb.xpath('//FocusPosition')[0].text)
            except IndexError as e:
                zpos = 0.0

            df_czi = df_czi.append({'Subblock': sbcount,
                                    'Scene': s,
                                    'Tile': m,
                                    'T': t,
                                    'Z': z,
                                    'C': c,
                                    'X [micron]': xpos,
                                    'Y [micron]': ypos,
                                    'Z [micron]': zpos,
                                    'Time [s]': timestamp,
                                    'xstart': info[0],
                                    'ystart': info[1],
                                    'xwidth': info[2],
                                    'ywidth': info[3]},
                                   ignore_index=True)

    if not md['czi_isMosaic']:

        """
        for s, t, z, c in it.product(range(md['SizeS']),
                                     range(md['SizeT']),
                                     range(md['SizeZ']),
                                     range(md['SizeC'])):
        """

        for s, t, z, c in product(range(md['SizeS']),
                                  range(md['SizeT']),
                                  range(md['SizeZ']),
                                  range(md['SizeC'])):

            sbcount += 1
            info = czi.read_subblock_rect(S=s, T=t, Z=z, C=c)

            # read information from subblocks
            sb = czi.read_subblock_metadata(unified_xml=True, B=0, S=s, T=t, Z=z, C=c)

            try:
                time = sb.xpath('//AcquisitionTime')[0].text
                timestamp = dt.parse(time).timestamp()
            except IndexError as e:
                timestamp = 0.0

            try:
                xpos = np.double(sb.xpath('//StageXPosition')[0].text)
            except IndexError as e:
                xpos = 0.0

            try:
                ypos = np.double(sb.xpath('//StageYPosition')[0].text)
            except IndexError as e:
                ypos = 0.0

            try:
                zpos = np.double(sb.xpath('//FocusPosition')[0].text)
            except IndexError as e:
                zpos = 0.0

            df_czi = df_czi.append({'Subblock': sbcount,
                                    'Scene': s,
                                    'Tile': 0,
                                    'T': t,
                                    'Z': z,
                                    'C': c,
                                    'X [micron]': xpos,
                                    'Y [micron]': ypos,
                                    'Z [micron]': zpos,
                                    'Time [s]': timestamp,
                                    'xstart': info[0],
                                    'ystart': info[1],
                                    'xwidth': info[2],
                                    'ywidth': info[3]},
                                   ignore_index=True)

    # normalize timestamps
    df_czi = imf.norm_columns(df_czi, colname='Time [s]', mode='min')

    # cast data  types
    df_czi = df_czi.astype({'Subblock': 'int32',
                            'Scene': 'int32',
                            'Tile': 'int32',
                            'T': 'int32',
                            'Z': 'int32',
                            'C': 'int16',
                            'xstart': 'int32',
                            'xstart': 'int32',
                            'ystart': 'int32',
                            'xwidth': 'int32',
                            'ywidth': 'int32'},
                           copy=False,
                           errors='ignore')

    return df_czi


def save_planetable(df, filename, separator=',', index=True):
    """Save dataframe as CSV table

    :param df: Dataframe to be saved as CSV.
    :type df: pd.DataFrame
    :param filename: filename of the CSV to be written
    :type filename: str
    :param separator: seperator for the CSV file, defaults to ','
    :type separator: str, optional
    :param index: option write the index into the CSV file, defaults to True
    :type index: bool, optional
    :return: filename of the csvfile that was written
    :rtype: str
    """
    csvfile = os.path.splitext(filename)[0] + '_planetable.csv'

    # write the CSV data table
    df.to_csv(csvfile, sep=separator, index=index)

    return csvfile


def filterplanetable(planetable, S=0, T=0, Z=0, C=0):

    # filter planetable for specific scene
    if S > planetable['Scene'].max():
        print('Scene Index was invalid. Using Scene = 0.')
        S = 0
    pt = planetable[planetable['Scene'] == S]

    # filter planetable for specific timepoint
    if T > planetable['T'].max():
        print('Time Index was invalid. Using T = 0.')
        T = 0
    pt = planetable[planetable['T'] == T]

    # filter resulting planetable pt for a specific z-plane
    if Z > planetable['Z [micron]'].max():
        print('Z-Plane Index was invalid. Using Z = 0.')
        zplane = 0
    pt = pt[pt['Z [micron]'] == Z]

    # filter planetable for specific channel
    if C > planetable['C'].max():
        print('Channel Index was invalid. Using C = 0.')
        C = 0
    pt = planetable[planetable['C'] == C]

    # return filtered planetable
    return pt
