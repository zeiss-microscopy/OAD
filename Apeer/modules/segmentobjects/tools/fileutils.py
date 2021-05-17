# -*- coding: utf-8 -*-

#################################################################
# File        : fileutils.py
# Version     : 0.1.2
# Author      : czsrh
# Date        : 16.04.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################

import os
from aicsimageio import AICSImage, imread, imread_dask
import aicspylibczi
from numpy.core.fromnumeric import _size_dispatcher
import tools.imgfile_tools as imf
import itertools as it
from tqdm import tqdm, trange
from tqdm.contrib.itertools import product
import pandas as pd
import numpy as np
from datetime import datetime
import dateutil.parser as dt
from lxml import etree
import progressbar
import zarr


def define_czi_planetable():
    """Define the columns for the dataframe containing the planetable for a CZI image

    :return: empty dataframe with predefined columns
    :rtype: pandas.DataFrame
    """
    df = pd.DataFrame(columns=['Subblock',
                               'Scene',
                               'Tile',
                               'T',
                               'Z',
                               'C',
                               'X[micron]',
                               'Y[micron]',
                               'Z[micron]',
                               'Time[s]',
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
    # total = md['SizeS'] * md['SizeM'] * md['SizeT'] * md['SizeZ'] * md['SizeC']
    # pbar = tqdm(total=total)

    # pbar = progressbar.ProgressBar(max_value=total)
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
                                    'X[micron]': xpos,
                                    'Y[micron]': ypos,
                                    'Z[micron]': zpos,
                                    'Time[s]': timestamp,
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
                                    'X[micron]': xpos,
                                    'Y[micron]': ypos,
                                    'Z[micron]': zpos,
                                    'Time[s]': timestamp,
                                    'xstart': info[0],
                                    'ystart': info[1],
                                    'xwidth': info[2],
                                    'ywidth': info[3]},
                                   ignore_index=True)

    # normalize timestamps
    df_czi = imf.norm_columns(df_czi, colname='Time[s]', mode='min')

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


def norm_columns(df, colname='Time [s]', mode='min'):
    """Normalize a specific column inside a Pandas dataframe

    :param df: DataFrame
    :type df: pf.DataFrame
    :param colname: Name of the coumn to be normalized, defaults to 'Time [s]'
    :type colname: str, optional
    :param mode: Mode of Normalization, defaults to 'min'
    :type mode: str, optional
    :return: Dataframe with normalized column
    :rtype: pd.DataFrame
    """
    # normalize columns according to min or max value
    if mode == 'min':
        min_value = df[colname].min()
        df[colname] = df[colname] - min_value

    if mode == 'max':
        max_value = df[colname].max()
        df[colname] = df[colname] - max_value

    return df


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
    try:
        if Z > planetable['Z[micron]'].max():
            print('Z-Plane Index was invalid. Using Z = 0.')
            zplane = 0
            pt = pt[pt['Z[micron]'] == Z]
    except KeyError as e:
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


def get_bbox_scene(cziobject, sceneindex=0):
    """Get the min / max extend of a given scene from a CZI mosaic image
    at pyramid level = 0 (full resolution)

    :param czi: CZI object for from aicspylibczi
    :type czi: Zeiss CZI file object
    :param sceneindex: index of the scene, defaults to 0
    :type sceneindex: int, optional
    :return: tuple with (XSTART, YSTART, WIDTH, HEIGHT) extend in pixels
    :rtype: tuple
    """

    # get all bounding boxes
    bboxes = cziobject.mosaic_scene_bounding_boxes(index=sceneindex)

    # initialize lists for required values
    xstart = []
    ystart = []
    tilewidth = []
    tileheight = []

    # loop over all tiles for the specified scene
    for box in bboxes:

        # get xstart, ystart amd tile widths and heights
        xstart.append(box[0])
        ystart.append(box[1])
        tilewidth.append(box[2])
        tileheight.append(box[3])

    # get bounding box for the current scene
    XSTART = min(xstart)
    YSTART = min(ystart)

    # do not forget to add the width and height of the last tile :-)
    WIDTH = max(xstart) - XSTART + tilewidth[-1]
    HEIGHT = max(ystart) - YSTART + tileheight[-1]

    return XSTART, YSTART, WIDTH, HEIGHT


def read_scene_bbox(cziobject, metadata,
                    sceneindex=0,
                    channel=0,
                    timepoint=0,
                    zplane=0,
                    scalefactor=1.0):
    """Read a specific scene from a CZI image file.

    : param cziobject: The CziFile reader object from aicspylibczi
    : type cziobject: CziFile
    : param metadata: Image metadata dictionary from imgfileutils
    : type metadata: dict
    : param sceneindex: Index of scene, defaults to 0
    : type sceneindex: int, optional
    : param channel: Index of channel, defaults to 0
    : type channel: int, optional
    : param timepoint: Index of Timepoint, defaults to 0
    : type timepoint: int, optional
    : param zplane: Index of z - plane, defaults to 0
    : type zplane: int, optional
    : param scalefactor: scaling factor to read CZI image pyramid, defaults to 1.0
    : type scalefactor: float, optional
    : return: scene as a numpy array
    : rtype: NumPy.Array
    """
    # set variables
    scene = None
    hasT = False
    hasZ = False

    # check if scalefactor has a reasonable value
    if scalefactor < 0.01 or scalefactor > 1.0:
        print('Scalefactor too small or too large. Will use 1.0 as fallback')
        scalefactor = 1.0

    # check if CZI has T or Z dimension
    if 'T' in metadata['dims_aicspylibczi']:
        hasT = True
    if 'Z' in metadata['dims_aicspylibczi']:
        hasZ = True

    # get the bounding box for the specified scene
    xmin, ymin, width, height = get_bbox_scene(cziobject,
                                               sceneindex=sceneindex)

    # read the scene as numpy array using the correct function calls
    if hasT is True and hasZ is True:
        scene = cziobject.read_mosaic(region=(xmin, ymin, width, height),
                                      scale_factor=scalefactor,
                                      T=timepoint,
                                      Z=zplane,
                                      C=channel)

    if hasT is True and hasZ is False:
        scene = cziobject.read_mosaic(region=(xmin, ymin, width, height),
                                      scale_factor=scalefactor,
                                      T=timepoint,
                                      C=channel)

    if hasT is False and hasZ is True:
        scene = cziobject.read_mosaic(region=(xmin, ymin, width, height),
                                      scale_factor=scalefactor,
                                      Z=zplane,
                                      C=channel)

    if hasT is False and hasZ is False:
        scene = cziobject.read_mosaic(region=(xmin, ymin, width, height),
                                      scale_factor=scalefactor,
                                      C=channel)

    # add new entries to metadata to adjust XY scale due to scaling factor
    metadata['XScale Pyramid'] = metadata['XScale'] * 1 / scalefactor
    metadata['YScale Pyramid'] = metadata['YScale'] * 1 / scalefactor

    return scene, (xmin, ymin, width, height), metadata


def getbboxes_allscenes(czi, md, numscenes=1):

    all_bboxes = []
    for s in range(numscenes):
        sc = CZIScene(czi, md, sceneindex=s)
        all_bboxes.append(sc)

    return all_bboxes


class CZIScene:
    def __init__(self, czi, md, sceneindex):

        x, y, w, h = get_bbox_scene(czi, sceneindex)
        self.xstart = x
        self.ystart = y
        self.width = w
        self.height = h
        self.index = sceneindex
        self.hasT = False
        self.hasZ = False
        self.hasS = False
        #self.sizeT = None
        #self.sizeZ = None
        #self.sizeS = None
        #self.sizeC = czi.dims_shape()[0]['C'][1]
        #self.sizeS = czi.dims_shape()[0]['S'][1]
        #self.sizeT = czi.dims_shape()[0]['T'][1]
        #self.sizeZ = czi.dims_shape()[0]['Z'][1]

        # check if the scene has T or Z slices
        dims_aicspylibczi = czi.dims_shape()[0]

        if 'C' in dims_aicspylibczi:
            self.hasC = True
            self.sizeC = czi.dims_shape()[0]['C'][1]
        else:
            self.hasS = False
            self.sizeS = None

        if 'T' in dims_aicspylibczi:
            self.hasT = True
            self.sizeT = czi.dims_shape()[0]['T'][1]
        else:
            self.hasT = False
            self.sizeT = None

        if 'Z' in dims_aicspylibczi:
            self.hasZ = True
            self.sizeZ = czi.dims_shape()[0]['Z'][1]
        else:
            self.hasZ = False
            self.sizeZ = None

        if 'S' in dims_aicspylibczi:
            self.hasS = True
            self.sizeS = czi.dims_shape()[0]['S'][1]
        else:
            self.hasS = False
            self.sizeS = None

        if 'M' in dims_aicspylibczi:
            self.hasM = True
            self.sizeM = czi.dims_shape()[0]['M'][1]
        else:
            self.hasM = False
            self.sizeM = None

        # determine the shape of the scene
        shape_single_scene = [1]
        single_scene_dimstr = 'S'
        posdict = {'S': 'SizeS', 'T': 'SizeT', 'C': 'SizeC', 'Z': 'SizeZ'}

        # find key based upon value
        for v in range(1, 4):

            # get the corresponding dim_id, e.g. 'S'
            dim_id = imf.get_key(md['dimpos_aics'], v)

            # get the correspong string to access the size of tht dimension
            dimstr = posdict[dim_id]

            # append size for this dimension to list containing the shape
            shape_single_scene.append(md[dimstr])

        # add width and height of scene to the required shape list
        shape_single_scene.append(self.height)
        shape_single_scene.append(self.width)

        self.shape_scene = shape_single_scene

        # determine required dtype
        self.dtype_scene_array = md['NumPy.dtype']

        # position for dimension for scene array
        self.posC = md['dimpos_aics']['C']
        self.posZ = md['dimpos_aics']['Z']
        self.posT = md['dimpos_aics']['T']


def get_shape_allscenes(czi, md):

    shape_single_scenes = []

    # loop over all scenes
    for s in range(md['SizeS']):

        # get info for a single scene
        single_scene = CZIScene(czi, md, s)

        # add shape info to the list for shape of all single scenes
        print('Adding shape for scene: ', s)
        shape_single_scenes.append(single_scene.shape_scene)

    # check if all calculated scene sizes have the same shape
    same_shape = all(elem == shape_single_scenes[0] for elem in shape_single_scenes)

    # create required array shape in case all scenes are equal
    array_size_all_scenes = None
    if same_shape:
        array_size_all_scenes = shape_single_scenes[0].copy()
        array_size_all_scenes[md['dimpos_aics']['S']] = md['SizeS']

    return array_size_all_scenes, shape_single_scenes, same_shape


def read_czi_scene(czi, scene, metadata, scalefactor=1.0, array_type='zarr'):

    if array_type == 'numpy':
        # create the required array for this scene as numoy array
        scene_array = np.empty(scene.shape_scene, dtype=metadata['NumPy.dtype'])

    if array_type == "zarr":
        # create the required array for this scene as numoy array
        scene_array = zarr.create(tuple(scene.shape_scene),
                                  dtype=metadata['NumPy.dtype'],
                                  chunks=True)

    # check if scalefactor has a reasonable value
    if scalefactor < 0.01 or scalefactor > 1.0:
        print('Scalefactor too small or too large. Will use 1.0 as fallback')
        scalefactor = 1.0

    # read the scene as numpy array using the correct function calls
    # unfortunately a CZI not always has all dimensions.
    # Current status:
    # 1: hasT = True + hasZ = True          - OK
    # 2: hasT = False + hasT = False        - OK
    # 3: hasT = True + hasT = False         - NOK
    # 4: hasT = False + hasT = False        - NOK

    # in case T and Z dimension are found
    if scene.hasT is True and scene.hasZ is True:

        # create an array for the scene
        for t, z, c in it.product(range(scene.sizeT),
                                  range(scene.sizeZ),
                                  range(scene.sizeC)):

            scene_array_tzc = czi.read_mosaic(region=(scene.xstart,
                                                      scene.ystart,
                                                      scene.width,
                                                      scene.height),
                                              scale_factor=scalefactor,
                                              T=t,
                                              Z=z,
                                              C=c)

            if scene.posT == 1:
                if scene.posZ == 2:
                    # STZCYX
                    #scene_array[:, t, z, c, :, :] = scene_array_tzc
                    #scene_array[:, t, z, c, :, :] = scene_array_tzc[:, 0, 0]
                    scene_array[0, t, z, c, :, :] = scene_array_tzc[0, 0, 0, :, :]
                if scene.posZ == 3:
                    # STCZYX
                    #scene_array[:, t, c, z, :, :] = scene_array_tzc
                    #scene_array[:, t, c, z, :, :] = scene_array_tzc[:, 0, 0]
                    scene_array[0, t, c, z, :, :] = scene_array_tzc[0, 0, 0, :, :]

    # in case no T and Z dimension are found
    if scene.hasT is False and scene.hasZ is False:

        # create an array for the scene
        for c in range(czi.dims_shape()[0]['C'][1]):

            scene_array_c = czi.read_mosaic(region=(scene.xstart,
                                                    scene.ystart,
                                                    scene.width,
                                                    scene.height),
                                            scale_factor=scalefactor,
                                            C=c)
            if scene.posC == 1:
                # SCTZYX
                #scene_array[:, c, 0, 0, :, :] = scene_array_c
                scene_array[0, c, 0, 0, :, :] = scene_array_c[0, :, :]
            if scene.posC == 2:
                # STCZYX
                #scene_array[:, 0, c, 0, :, :] = scene_array_c
                scene_array[0, 0, c, 0, :, :] = scene_array_c[0, :, :]
            if scene.posC == 3:
                # STZCYX
                #scene_array[:, 0, 0, c, :, :] = scene_array_c
                scene_array[0, 0, 0, c, :, :] = scene_array_c[0, :, :]

            # if scene.posC == 1:
            #    # SCTZYX
            #    scene_array[:, c, 0:1, 0:1, ...] = scene_array_c
            # if scene.posC == 2:
            #    # STCZYX
            #    scene_array[:, 0:1, c, 0:1, ...] = scene_array_c
            # if scene.posC == 3:
            #    # STZCYX
            #    scene_array[:, 0:1, 0:1, c, ...] = scene_array_c

    if scene.hasT is False and scene.hasZ is True:

        # create an array for the scene
        for z, c in it.product(range(scene.sizeZ),
                               range(scene.sizeC)):

            scene_array_zc = czi.read_mosaic(region=(scene.xstart,
                                                     scene.ystart,
                                                     scene.width,
                                                     scene.height),
                                             scale_factor=scalefactor,
                                             Z=z,
                                             C=c)

            if scene.posC == 1:
                if scene.posZ == 2:
                    # SCTZYX
                    scene_array[0, c, 0, 0, :, :] = scene_array_zc[0, 0, :, :]

            if scene.posC == 2:
                if scene.posZ == 1:
                    # SZCTYX
                    scene_array[0, z, c, 0, :, :] = scene_array_zc[0, 0, :, :]
                if scene.posZ == 3:
                    # STCZYX
                    scene_array[0, 0, c, z, :, :] = scene_array_zc[0, 0, :, :]

            if scene.posC == 3:
                if scene.posZ == 2:
                    # STZCYX
                    scene_array[0, 0, z, c, :, :] = scene_array_zc[0, 0, :, :]

    return scene_array
