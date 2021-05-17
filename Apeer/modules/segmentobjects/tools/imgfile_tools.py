# -*- coding: utf-8 -*-

#################################################################
# File        : imgfile_tools.py
# Version     : 1.7.0
# Author      : czsrh
# Date        : 16.05.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk.
#
# Copyright (c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################


import czifile as zis
from apeer_ometiff_library import omexmlClass
import os
from pathlib import Path
import xmltodict
import numpy as np
import tools.fileutils as czt
from collections import Counter
from lxml import etree as ET
import sys
from aicsimageio import AICSImage, imread, imread_dask
from aicsimageio.writers import ome_tiff_writer
from aicspylibczi import CziFile
import dask.array as da
import pandas as pd
import tifffile
import pydash
import zarr


def get_imgtype(imagefile):
    """Returns the type of the image based on the file extension - no magic

    :param imagefile: filename of the image
    :type imagefile: str
    :return: string specifying the image type
    :rtype: str
    """

    imgtype = None

    if imagefile.lower().endswith('.ome.tiff') or imagefile.lower().endswith('.ome.tif'):
        # it is on OME-TIFF based on the file extension ... :-)
        imgtype = 'ometiff'

    elif imagefile.lower().endswith('.tiff') or imagefile.lower().endswith('.tif'):
        # it is on OME-TIFF based on the file extension ... :-)
        imgtype = 'tiff'

    elif imagefile.lower().endswith('.czi'):
        # it is on CZI based on the file extension ... :-)
        imgtype = 'czi'

    elif imagefile.lower().endswith('.png'):
        # it is on CZI based on the file extension ... :-)
        imgtype = 'png'

    elif imagefile.lower().endswith('.jpg') or imagefile.lower().endswith('.jpeg'):
        # it is on OME-TIFF based on the file extension ... :-)
        imgtype = 'jpg'

    return imgtype


def create_metadata_dict():
    """A Python dictionary will be created to hold the relevant metadata.

    :return: dictionary with keys for the relevant metadata
    :rtype: dict
    """

    metadata = {'Directory': None,
                'Filename': None,
                'Extension': None,
                'ImageType': None,
                'AcqDate': None,
                'TotalSeries': None,
                'SizeX': None,
                'SizeY': None,
                'SizeZ': 1,
                'SizeC': 1,
                'SizeT': 1,
                'SizeS': 1,
                'SizeB': 1,
                'SizeM': 1,
                'Sizes BF': None,
                'DimOrder BF': None,
                'DimOrder BF Array': None,
                'axes_czifile': None,
                'shape_czifile': None,
                'czi_isRGB': False,
                'czi_isMosaic': False,
                'ObjNA': [],
                'ObjMag': [],
                'ObjID': [],
                'ObjName': [],
                'ObjImmersion': [],
                'TubelensMag': [],
                'ObjNominalMag': [],
                'XScale': None,
                'YScale': None,
                'ZScale': None,
                'XScaleUnit': None,
                'YScaleUnit': None,
                'ZScaleUnit': None,
                'DetectorModel': [],
                'DetectorName': [],
                'DetectorID': [],
                'DetectorType': [],
                'InstrumentID': [],
                'Channels': [],
                'ChannelNames': [],
                'ChannelColors': [],
                'ImageIDs': [],
                'NumPy.dtype': None
                }

    return metadata


def get_metadata(imagefile,
                 omeseries=0,
                 round_values=False):
    """Returns a dictionary with metadata depending on the image type.
    Only CZI and OME-TIFF are currently supported.

    :param imagefile: filename of the image
    :type imagefile: str
    :param omeseries: series of OME-TIFF file, , defaults to 0
    :type omeseries: int, optional
    :param round_values: option to round some values, defaults to TrueFalse
    :type round_values: bool, optional
    :return: metadata - dict with the metainformation
    :rtype: dict
    :return: additional_mdczi - dict with additional the metainformation for CZI only
    :rtype: dict
    """

    # get the image type
    imgtype = get_imgtype(imagefile)
    print('Detected Image Type (based on extension):', imgtype)

    md = {}
    additional_md = {}

    if imgtype == 'ometiff':

        # parse the OME-XML and return the metadata dictionary and additional info
        md = get_metadata_ometiff(imagefile, series=omeseries)

    elif imgtype == 'czi':

        # parse the CZI metadata return the metadata dictionary and additional info
        md = get_metadata_czi(imagefile, dim2none=False)
        additional_md = get_additional_metadata_czi(imagefile)

    # TODO - Remove this when issue is fixed
    if round_values:
        # temporary workaround for slider / floating point issue in Napari viewer
        # https://forum.image.sc/t/problem-with-dimension-slider-when-adding-array-as-new-layer-for-ome-tiff/39092/2?u=sebi06

        md['XScale'] = np.round(md['XScale'], 3)
        md['YScale'] = np.round(md['YScale'], 3)
        md['ZScale'] = np.round(md['ZScale'], 3)
    else:
        # no metadate will be returned
        print('Scales will not be rounded.')

    return md, additional_md


def get_metadata_ometiff(filename, series=0):
    """Returns a dictionary with OME-TIFF metadata.

    :param filename: filename of the OME-TIFF image
    :type filename: str
    :param series: Image Series, defaults to 0
    :type series: int, optional
    :return: dictionary with the relevant OME-TIFF metainformation
    :rtype: dict
    """

    with tifffile.TiffFile(filename) as tif:
        try:
            # get OME-XML metadata as string the old way
            omexml_string = tif[0].image_description.decode('utf-8')
        except TypeError as e:
            print('TypeError :', e)
            omexml_string = tif.ome_metadata

    # get the OME-XML using the apeer-ometiff-library
    omemd = omexmlClass.OMEXML(omexml_string)

    # create dictionary for metadata and get OME-XML data
    metadata = create_metadata_dict()

    # get directory and filename etc.
    metadata['Directory'] = os.path.dirname(filename)
    metadata['Filename'] = os.path.basename(filename)
    metadata['Extension'] = 'ome.tiff'
    metadata['ImageType'] = 'ometiff'
    metadata['AcqDate'] = omemd.image(series).AcquisitionDate
    metadata['Name'] = omemd.image(series).Name

    # get image dimensions TZCXY
    metadata['SizeT'] = omemd.image(series).Pixels.SizeT
    metadata['SizeZ'] = omemd.image(series).Pixels.SizeZ
    metadata['SizeC'] = omemd.image(series).Pixels.SizeC
    metadata['SizeX'] = omemd.image(series).Pixels.SizeX
    metadata['SizeY'] = omemd.image(series).Pixels.SizeY

    # get number of image series
    metadata['TotalSeries'] = omemd.get_image_count()
    metadata['Sizes BF'] = [metadata['TotalSeries'],
                            metadata['SizeT'],
                            metadata['SizeZ'],
                            metadata['SizeC'],
                            metadata['SizeY'],
                            metadata['SizeX']]

    # get dimension order
    metadata['DimOrder BF'] = omemd.image(series).Pixels.DimensionOrder

    # reverse the order to reflect later the array shape
    metadata['DimOrder BF Array'] = metadata['DimOrder BF'][::-1]

    # get the scaling
    metadata['XScale'] = omemd.image(series).Pixels.PhysicalSizeX
    metadata['XScale'] = np.round(metadata['XScale'], 3)
    # metadata['XScaleUnit'] = omemd.image(series).Pixels.PhysicalSizeXUnit
    metadata['YScale'] = omemd.image(series).Pixels.PhysicalSizeY
    metadata['YScale'] = np.round(metadata['YScale'], 3)
    # metadata['YScaleUnit'] = omemd.image(series).Pixels.PhysicalSizeYUnit
    metadata['ZScale'] = omemd.image(series).Pixels.PhysicalSizeZ
    metadata['ZScale'] = np.round(metadata['ZScale'], 3)
    # metadata['ZScaleUnit'] = omemd.image(series).Pixels.PhysicalSizeZUnit

    # get all image IDs
    for i in range(omemd.get_image_count()):
        metadata['ImageIDs'].append(i)

    # get information about the instrument and objective
    try:
        metadata['InstrumentID'] = omemd.instrument(series).get_ID()
    except (KeyError, AttributeError) as e:
        print('Key not found:', e)
        metadata['InstrumentID'] = None

    try:
        metadata['DetectorModel'] = omemd.instrument(series).Detector.get_Model()
        metadata['DetectorID'] = omemd.instrument(series).Detector.get_ID()
        metadata['DetectorModel'] = omemd.instrument(series).Detector.get_Type()
    except (KeyError, AttributeError) as e:
        print('Key not found:', e)
        metadata['DetectorModel'] = None
        metadata['DetectorID'] = None
        metadata['DetectorModel'] = None

    try:
        metadata['ObjNA'] = omemd.instrument(series).Objective.get_LensNA()
        metadata['ObjID'] = omemd.instrument(series).Objective.get_ID()
        metadata['ObjMag'] = omemd.instrument(series).Objective.get_NominalMagnification()
    except (KeyError, AttributeError) as e:
        print('Key not found:', e)
        metadata['ObjNA'] = None
        metadata['ObjID'] = None
        metadata['ObjMag'] = None

    # get channel names
    for c in range(metadata['SizeC']):
        metadata['Channels'].append(omemd.image(series).Pixels.Channel(c).Name)

    # add axes and shape information using aicsimageio package
    ometiff_aics = AICSImage(filename)
    metadata['Axes_aics'] = ometiff_aics.dims
    metadata['Shape_aics'] = ometiff_aics.shape
    metadata['SizeX_aics'] = ometiff_aics.size_x
    metadata['SizeY_aics'] = ometiff_aics.size_y
    metadata['SizeC_aics'] = ometiff_aics.size_c
    metadata['SizeZ_aics'] = ometiff_aics.size_t
    metadata['SizeT_aics'] = ometiff_aics.size_t
    metadata['SizeS_aics'] = ometiff_aics.size_s

    # close AICSImage object
    ometiff_aics.close()

    # check for None inside Scaling to avoid issues later one ...
    metadata = checkmdscale_none(metadata,
                                 tocheck=['XScale', 'YScale', 'ZScale'],
                                 replace=[1.0, 1.0, 1.0])

    return metadata


def checkmdscale_none(md, tocheck=['ZScale'], replace=[1.0]):
    """Check scaling entries for None to avoid issues later on

    :param md: original metadata
    :type md: dict
    :param tocheck: list with entries to check for None, defaults to ['ZScale']
    :type tocheck: list, optional
    :param replace: list with values replacing the None, defaults to [1.0]
    :type replace: list, optional
    :return: modified metadata where None entries where replaces by
    :rtype: [type]
    """
    for tc, rv in zip(tocheck, replace):
        if md[tc] is None:
            md[tc] = rv

    return md


def get_metadata_czi(filename, dim2none=False,
                     forceDim=False,
                     forceDimname='SizeC',
                     forceDimvalue=2,
                     convert_scunit=True):
    """
    Returns a dictionary with CZI metadata.

    Information CZI Dimension Characters:
    - '0':'Sample',  # e.g. RGBA
    - 'X':'Width',
    - 'Y':'Height',
    - 'C':'Channel',
    - 'Z':'Slice',  # depth
    - 'T':'Time',
    - 'R':'Rotation',
    - 'S':'Scene',  # contiguous regions of interest in a mosaic image
    - 'I':'Illumination',  # direction
    - 'B':'Block',  # acquisition
    - 'M':'Mosaic',  # index of tile for compositing a scene
    - 'H':'Phase',  # e.g. Airy detector fibers
    - 'V':'View',  # e.g. for SPIM

    :param filename: filename of the CZI image
    :type filename: str
    :param dim2none: option to set non-existing dimension to None, defaults to False
    :type dim2none: bool, optional
    :param forceDim: option to force to not read certain dimensions, defaults to False
    :type forceDim: bool, optional
    :param forceDimname: name of the dimension not to read, defaults to SizeC
    :type forceDimname: str, optional
    :param forceDimvalue: index of the dimension not to read, defaults to 2
    :type forceDimvalue: int, optional
    :param convert_scunit: convert scale unit string from 'µm' to 'micron', defaults to False
    :type convert_scunit: bool, optional
    :return: metadata - dictionary with the relevant CZI metainformation
    :rtype: dict
    """

    # get CZI object
    czi = zis.CziFile(filename)

    # parse the XML into a dictionary
    metadatadict_czi = czi.metadata(raw=False)

    # initialize metadata dictionary
    #metadata = {}
    metadata = create_metadata_dict()

    # get directory and filename etc.
    metadata['Directory'] = os.path.dirname(filename)
    metadata['Filename'] = os.path.basename(filename)
    metadata['Extension'] = 'czi'
    metadata['ImageType'] = 'czi'

    # add axes and shape information using czifile package
    metadata['axes_czifile'] = czi.axes
    metadata['shape_czifile'] = czi.shape

    # add axes and shape information using aicsimageio package
    czi_aics = AICSImage(filename)
    metadata['Axes_aics'] = czi_aics.dims
    try:
        metadata['Shape_aics'] = czi_aics.shape
        metadata['SizeX_aics'] = czi_aics.size_x
        metadata['SizeY_aics'] = czi_aics.size_y
        metadata['SizeC_aics'] = czi_aics.size_c
        metadata['SizeZ_aics'] = czi_aics.size_t
        metadata['SizeT_aics'] = czi_aics.size_t
        metadata['SizeS_aics'] = czi_aics.size_s
    except KeyError as e:
        print('AICSImageIO could not detect dimension :', e)
        metadata['Shape_aics'] = None
        metadata['SizeX_aics'] = None
        metadata['SizeY_aics'] = None
        metadata['SizeC_aics'] = None
        metadata['SizeZ_aics'] = None
        metadata['SizeT_aics'] = None
        metadata['SizeS_aics'] = None

    # get additional data by using pylibczi directly
    # Get the shape of the data, the coordinate pairs are (start index, size)
    aics_czi = CziFile(filename)
    metadata['dims_aicspylibczi'] = aics_czi.dims_shape()[0]
    metadata['axes_aicspylibczi'] = aics_czi.dims
    metadata['size_aicspylibczi'] = aics_czi.size
    metadata['czi_isMosaic'] = aics_czi.is_mosaic()
    print('CZI is Mosaic :', metadata['czi_isMosaic'])

    # get positions of dimensions
    try:
        metadata['dimpos_aics'] = get_dimpositions(metadata['Axes_aics'])
    except KeyError:
        metadata['dimpos_aics'] = None

    # determine pixel type for CZI array
    metadata['NumPy.dtype'] = czi.dtype

    # check if the CZI image is an RGB image depending
    # on the last dimension entry of axes
    if czi.shape[-1] == 3:
        metadata['czi_isRGB'] = True
    if czi.shape[-1] != 3:
        metadata['czi_isRGB'] = False
    print('CZI is RGB :', metadata['czi_isRGB'])

    try:
        metadata['PixelType'] = metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['PixelType']
    except KeyError as e:
        print('No PixelType :', e)
        metadata['PixelType'] = None
    try:
        metadata['SizeX'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeX'])
    except KeyError as e:
        print('No X Dimension :', e)
        metadata['SizeX'] = None
    try:
        metadata['SizeY'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeY'])
    except KeyError as e:
        print('No Y Dimension :', e)
        metadata['SizeY'] = None

    try:
        metadata['SizeZ'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeZ'])
    except KeyError as e:
        print('No Z Dimension :', e)
        if dim2none:
            metadata['SizeZ'] = None
        if not dim2none:
            metadata['SizeZ'] = 1

    # for special cases do not read the SizeC from the metadata
    if forceDim and forceDimname == 'SizeC':
        metadata[forceDimname] = forceDimvalue

    if not forceDim:

        try:
            metadata['SizeC'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeC'])
        except KeyError as e:
            print('No C Dimension :', e)
            if dim2none:
                metadata['SizeC'] = None
            if not dim2none:
                metadata['SizeC'] = 1

    # create empty lists for channel related information
    channels = []
    channels_names = []
    channels_colors = []

    # in case of only one channel
    if metadata['SizeC'] == 1:
        # get name for dye
        try:
            channels.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                            ['Channels']['Channel']['ShortName'])
        except KeyError as e:
            print('Channel shortname not found :', e)
            try:
                channels.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                ['Channels']['Channel']['DyeName'])
            except KeyError as e:
                print('Channel dye not found :', e)
                channels.append('Dye-CH1')

        # get channel name
        try:
            channels_names.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                  ['Channels']['Channel']['Name'])
        except KeyError as e:
            print('Channel name found :', e)
            channels_names.append['CH1']

        # get channel color
        try:
            channels_colors.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                   ['Channels']['Channel']['Color'])
        except KeyError as e:
            print('Channel color not found :', e)
            channels_colors.append('#80808000')

    # in case of two or more channels
    if metadata['SizeC'] > 1:
        # loop over all channels
        for ch in range(metadata['SizeC']):
            # get name for dyes
            try:
                channels.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                                ['Channels']['Channel'][ch]['ShortName'])
            except KeyError as e:
                print('Channel shortname not found :', e)
                try:
                    channels.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                                    ['Channels']['Channel'][ch]['DyeName'])
                except KeyError as e:
                    print('Channel dye not found :', e)
                    channels.append('Dye-CH' + str(ch))

            # get channel names
            try:
                channels_names.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                      ['Channels']['Channel'][ch]['Name'])
            except KeyError as e:
                print('Channel name not found :', e)
                channels_names.append('CH' + str(ch))

            # get channel colors
            try:
                channels_colors.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                       ['Channels']['Channel'][ch]['Color'])
            except KeyError as e:
                print('Channel color not found :', e)
                # use grayscale instead
                channels_colors.append('80808000')

    # write channels information (as lists) into metadata dictionary
    metadata['Channels'] = channels
    metadata['ChannelNames'] = channels_names
    metadata['ChannelColors'] = channels_colors

    try:
        metadata['SizeT'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeT'])
    except KeyError as e:
        print('No T Dimension :', e)
        if dim2none:
            metadata['SizeT'] = None
        if not dim2none:
            metadata['SizeT'] = 1

    try:
        metadata['SizeM'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeM'])
    except KeyError as e:
        print('No M Dimension :', e)
        if dim2none:
            metadata['SizeM'] = None
        if not dim2none:
            metadata['SizeM'] = 1

    try:
        metadata['SizeB'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeB'])
    except KeyError as e:
        print('No B Dimension :', e)
        if dim2none:
            metadata['SizeB'] = None
        if not dim2none:
            metadata['SizeB'] = 1

    try:
        metadata['SizeS'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeS'])
    except KeyError as e:
        print('No S Dimension :', e)
        if dim2none:
            metadata['SizeS'] = None
        if not dim2none:
            metadata['SizeS'] = 1

    try:
        metadata['SizeH'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeH'])
    except KeyError as e:
        print('No H Dimension :', e)
        if dim2none:
            metadata['SizeH'] = None
        if not dim2none:
            metadata['SizeH'] = 1

    try:
        metadata['SizeI'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeI'])
    except KeyError as e:
        print('No I Dimension :', e)
        if dim2none:
            metadata['SizeI'] = None
        if not dim2none:
            metadata['SizeI'] = 1

    try:
        metadata['SizeV'] = np.int(metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['SizeV'])
    except KeyError as e:
        print('No V Dimension :', e)
        if dim2none:
            metadata['SizeV'] = None
        if not dim2none:
            metadata['SizeV'] = 1

    # get the XY scaling information
    try:
        metadata['XScale'] = float(metadatadict_czi['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][0]['Value']) * 1000000
        metadata['YScale'] = float(metadatadict_czi['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][1]['Value']) * 1000000
        metadata['XScale'] = np.round(metadata['XScale'], 3)
        metadata['YScale'] = np.round(metadata['YScale'], 3)
        try:
            metadata['XScaleUnit'] = metadatadict_czi['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][0]['DefaultUnitFormat']
            metadata['YScaleUnit'] = metadatadict_czi['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][1]['DefaultUnitFormat']
        except (KeyError, TypeError) as e:
            print('Error extracting XY ScaleUnit :', e)
            metadata['XScaleUnit'] = None
            metadata['YScaleUnit'] = None
    except (KeyError, TypeError) as e:
        print('Error extracting XY Scale  :', e)

    # get the XY scaling information
    try:
        metadata['ZScale'] = float(metadatadict_czi['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][2]['Value']) * 1000000
        metadata['ZScale'] = np.round(metadata['ZScale'], 3)
        # additional check for faulty z-scaling
        if metadata['ZScale'] == 0.0:
            metadata['ZScale'] = 1.0
        try:
            metadata['ZScaleUnit'] = metadatadict_czi['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][2]['DefaultUnitFormat']
        except (IndexError, KeyError, TypeError) as e:
            print('Error extracting Z ScaleUnit :', e)
            metadata['ZScaleUnit'] = metadata['XScaleUnit']
    except (IndexError, KeyError, TypeError) as e:
        print('Error extracting Z Scale  :', e)
        if dim2none:
            metadata['ZScale'] = None
            metadata['ZScaleUnit'] = None
        if not dim2none:
            # set to isotropic scaling if it was single plane only
            metadata['ZScale'] = metadata['XScale']
            metadata['ZScaleUnit'] = metadata['XScaleUnit']

    # convert scale unit to avoid encoding problems
    if convert_scunit:
        if metadata['XScaleUnit'] == 'µm':
            metadata['XScaleUnit'] = 'micron'
        if metadata['YScaleUnit'] == 'µm':
            metadata['YScaleUnit'] = 'micron'
        if metadata['ZScaleUnit'] == 'µm':
            metadata['ZScaleUnit'] = 'micron'

    # try to get software version
    try:
        metadata['SW-Name'] = metadatadict_czi['ImageDocument']['Metadata']['Information']['Application']['Name']
        metadata['SW-Version'] = metadatadict_czi['ImageDocument']['Metadata']['Information']['Application']['Version']
    except KeyError as e:
        print('Key not found:', e)
        metadata['SW-Name'] = None
        metadata['SW-Version'] = None

    try:
        metadata['AcqDate'] = metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['AcquisitionDateAndTime']
    except KeyError as e:
        print('Key not found:', e)
        metadata['AcqDate'] = None

    # check if Instrument metadat actually exist
    if pydash.objects.has(metadatadict_czi, ['ImageDocument', 'Metadata', 'Information', 'Instrument']):
        if metadatadict_czi['ImageDocument']['Metadata']['Information']['Instrument'] is not None:
            # get objective data
            if isinstance(metadatadict_czi['ImageDocument']['Metadata']['Information']['Instrument']['Objectives']['Objective'], list):
                num_obj = len(metadatadict_czi['ImageDocument']['Metadata']['Information']['Instrument']['Objectives']['Objective'])
            else:
                num_obj = 1

            # if there is only one objective found
            if num_obj == 1:
                try:
                    metadata['ObjName'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                               ['Instrument']['Objectives']['Objective']['Name'])
                except (KeyError, TypeError) as e:
                    print('No Objective Name :', e)
                    metadata['ObjName'].append(None)

                try:
                    metadata['ObjImmersion'] = metadatadict_czi['ImageDocument']['Metadata']['Information']['Instrument']['Objectives']['Objective']['Immersion']
                except (KeyError, TypeError) as e:
                    print('No Objective Immersion :', e)
                    metadata['ObjImmersion'] = None

                try:
                    metadata['ObjNA'] = np.float(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                 ['Instrument']['Objectives']['Objective']['LensNA'])
                except (KeyError, TypeError) as e:
                    print('No Objective NA :', e)
                    metadata['ObjNA'] = None

                try:
                    metadata['ObjID'] = metadatadict_czi['ImageDocument']['Metadata']['Information']['Instrument']['Objectives']['Objective']['Id']
                except (KeyError, TypeError) as e:
                    print('No Objective ID :', e)
                    metadata['ObjID'] = None

                try:
                    metadata['TubelensMag'] = np.float(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                       ['Instrument']['TubeLenses']['TubeLens']['Magnification'])
                except (KeyError, TypeError) as e:
                    print('No Tubelens Mag. :', e, 'Using Default Value = 1.0.')
                    metadata['TubelensMag'] = 1.0

                try:
                    metadata['ObjNominalMag'] = np.float(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                         ['Instrument']['Objectives']['Objective']['NominalMagnification'])
                except (KeyError, TypeError) as e:
                    print('No Nominal Mag.:', e, 'Using Default Value = 1.0.')
                    metadata['ObjNominalMag'] = 1.0

                try:
                    if metadata['TubelensMag'] is not None:
                        metadata['ObjMag'] = metadata['ObjNominalMag'] * metadata['TubelensMag']
                    if metadata['TubelensMag'] is None:
                        print('Using Tublens Mag = 1.0 for calculating Objective Magnification.')
                        metadata['ObjMag'] = metadata['ObjNominalMag'] * 1.0

                except (KeyError, TypeError) as e:
                    print('No Objective Magnification :', e)
                    metadata['ObjMag'] = None

            if num_obj > 1:
                for o in range(num_obj):

                    try:
                        metadata['ObjName'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                   ['Instrument']['Objectives']['Objective'][o]['Name'])
                    except KeyError as e:
                        print('No Objective Name :', e)
                        metadata['ObjName'].append(None)

                    try:
                        metadata['ObjImmersion'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                        ['Instrument']['Objectives']['Objective'][o]['Immersion'])
                    except KeyError as e:
                        print('No Objective Immersion :', e)
                        metadata['ObjImmersion'].append(None)

                    try:
                        metadata['ObjNA'].append(np.float(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                          ['Instrument']['Objectives']['Objective'][o]['LensNA']))
                    except KeyError as e:
                        print('No Objective NA :', e)
                        metadata['ObjNA'].append(None)

                    try:
                        metadata['ObjID'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                 ['Instrument']['Objectives']['Objective'][o]['Id'])
                    except KeyError as e:
                        print('No Objective ID :', e)
                        metadata['ObjID'].append(None)

                    try:
                        metadata['TubelensMag'].append(np.float(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                                ['Instrument']['TubeLenses']['TubeLens'][o]['Magnification']))
                    except KeyError as e:
                        print('No Tubelens Mag. :', e, 'Using Default Value = 1.0.')
                        metadata['TubelensMag'].append(1.0)

                    try:
                        metadata['ObjNominalMag'].append(np.float(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                                  ['Instrument']['Objectives']['Objective'][o]['NominalMagnification']))
                    except KeyError as e:
                        print('No Nominal Mag. :', e, 'Using Default Value = 1.0.')
                        metadata['ObjNominalMag'].append(1.0)

                    try:
                        if metadata['TubelensMag'] is not None:
                            metadata['ObjMag'].append(metadata['ObjNominalMag'][o] * metadata['TubelensMag'][o])
                        if metadata['TubelensMag'] is None:
                            print('Using Tublens Mag = 1.0 for calculating Objective Magnification.')
                            metadata['ObjMag'].append(metadata['ObjNominalMag'][o] * 1.0)

                    except KeyError as e:
                        print('No Objective Magnification :', e)
                        metadata['ObjMag'].append(None)

    # get detector information

    # check if there are any detector entries inside the dictionary
    if pydash.objects.has(metadatadict_czi, ['ImageDocument', 'Metadata', 'Information', 'Instrument', 'Detectors']):

        if isinstance(metadatadict_czi['ImageDocument']['Metadata']['Information']['Instrument']['Detectors']['Detector'], list):
            num_detectors = len(metadatadict_czi['ImageDocument']['Metadata']['Information']['Instrument']['Detectors']['Detector'])
        else:
            num_detectors = 1

        # if there is only one detector found
        if num_detectors == 1:

            # check for detector ID
            try:
                metadata['DetectorID'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                              ['Instrument']['Detectors']['Detector']['Id'])
            except KeyError as e:
                print('DetectorID not found :', e)
                metadata['DetectorID'].append(None)

            # check for detector Name
            try:
                metadata['DetectorName'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                ['Instrument']['Detectors']['Detector']['Name'])
            except KeyError as e:
                print('DetectorName not found :', e)
                metadata['DetectorName'].append(None)

            # check for detector model
            try:
                metadata['DetectorModel'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                 ['Instrument']['Detectors']['Detector']['Manufacturer']['Model'])
            except KeyError as e:
                print('DetectorModel not found :', e)
                metadata['DetectorModel'].append(None)

            # check for detector type
            try:
                metadata['DetectorType'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                ['Instrument']['Detectors']['Detector']['Type'])
            except KeyError as e:
                print('DetectorType not found :', e)
                metadata['DetectorType'].append(None)

        if num_detectors > 1:
            for d in range(num_detectors):

                # check for detector ID
                try:
                    metadata['DetectorID'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                  ['Instrument']['Detectors']['Detector'][d]['Id'])
                except KeyError as e:
                    print('DetectorID not found :', e)
                    metadata['DetectorID'].append(None)

                # check for detector Name
                try:
                    metadata['DetectorName'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                    ['Instrument']['Detectors']['Detector'][d]['Name'])
                except KeyError as e:
                    print('DetectorName not found :', e)
                    metadata['DetectorName'].append(None)

                # check for detector model
                try:
                    metadata['DetectorModel'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                     ['Instrument']['Detectors']['Detector'][d]['Manufacturer']['Model'])
                except KeyError as e:
                    print('DetectorModel not found :', e)
                    metadata['DetectorModel'].append(None)

                # check for detector type
                try:
                    metadata['DetectorType'].append(metadatadict_czi['ImageDocument']['Metadata']['Information']
                                                    ['Instrument']['Detectors']['Detector'][d]['Type'])
                except KeyError as e:
                    print('DetectorType not found :', e)
                    metadata['DetectorType'].append(None)

    # check for well information
    metadata['Well_ArrayNames'] = []
    metadata['Well_Indices'] = []
    metadata['Well_PositionNames'] = []
    metadata['Well_ColId'] = []
    metadata['Well_RowId'] = []
    metadata['WellCounter'] = None
    metadata['SceneStageCenterX'] = []
    metadata['SceneStageCenterY'] = []

    try:
        print('Trying to extract Scene and Well information if existing ...')

        # extract well information from the dictionary
        allscenes = metadatadict_czi['ImageDocument']['Metadata']['Information']['Image']['Dimensions']['S']['Scenes']['Scene']

        # loop over all detected scenes
        for s in range(metadata['SizeS']):

            if metadata['SizeS'] == 1:
                well = allscenes
                try:
                    metadata['Well_ArrayNames'].append(allscenes['ArrayName'])
                except KeyError as e:
                    print('WellArray Names not found :', e)
                    try:
                        metadata['Well_ArrayNames'].append(well['Name'])
                    except KeyError as e:
                        print('Well Name not found :', e, 'Using A1 instead')
                        metadata['Well_ArrayNames'].append('A1')

                try:
                    metadata['Well_Indices'].append(allscenes['Index'])
                except KeyError as e:
                    print('Well Index not found :', e)
                    metadata['Well_Indices'].append(1)

                try:
                    metadata['Well_PositionNames'].append(allscenes['Name'])
                except KeyError as e:
                    print('Well Position Names not found :', e)
                    metadata['Well_PositionNames'].append('P1')

                try:
                    metadata['Well_ColId'].append(np.int(allscenes['Shape']['ColumnIndex']))
                except KeyError as e:
                    print('Well ColumnIDs not found :', e)
                    metadata['Well_ColId'].append(0)

                try:
                    metadata['Well_RowId'].append(np.int(allscenes['Shape']['RowIndex']))
                except KeyError as e:
                    print('Well RowIDs not found :', e)
                    metadata['Well_RowId'].append(0)

                try:
                    # count the content of the list, e.g. how many time a certain well was detected
                    metadata['WellCounter'] = Counter(metadata['Well_ArrayNames'])
                except KeyError:
                    metadata['WellCounter'].append(Counter({'A1': 1}))

                try:
                    # get the SceneCenter Position
                    sx = allscenes['CenterPosition'].split(',')[0]
                    sy = allscenes['CenterPosition'].split(',')[1]
                    metadata['SceneStageCenterX'].append(np.double(sx))
                    metadata['SceneStageCenterY'].append(np.double(sy))
                except (TypeError, KeyError) as e:
                    print('Stage Positions XY not found :', e)
                    metadata['SceneStageCenterX'].append(0.0)
                    metadata['SceneStageCenterY'].append(0.0)

            if metadata['SizeS'] > 1:
                try:
                    well = allscenes[s]
                    metadata['Well_ArrayNames'].append(well['ArrayName'])
                except KeyError as e:
                    print('Well ArrayNames not found :', e)
                    try:
                        metadata['Well_ArrayNames'].append(well['Name'])
                    except KeyError as e:
                        print('Well Name not found :', e, 'Using A1 instead')
                        metadata['Well_ArrayNames'].append('A1')

                # get the well information
                try:
                    metadata['Well_Indices'].append(well['Index'])
                except KeyError as e:
                    print('Well Index not found :', e)
                    metadata['Well_Indices'].append(None)
                try:
                    metadata['Well_PositionNames'].append(well['Name'])
                except KeyError as e:
                    print('Well Position Names not found :', e)
                    metadata['Well_PositionNames'].append(None)

                try:
                    metadata['Well_ColId'].append(np.int(well['Shape']['ColumnIndex']))
                except KeyError as e:
                    print('Well ColumnIDs not found :', e)
                    metadata['Well_ColId'].append(None)

                try:
                    metadata['Well_RowId'].append(np.int(well['Shape']['RowIndex']))
                except KeyError as e:
                    print('Well RowIDs not found :', e)
                    metadata['Well_RowId'].append(None)

                # count the content of the list, e.g. how many time a certain well was detected
                metadata['WellCounter'] = Counter(metadata['Well_ArrayNames'])

                # try:
                if isinstance(allscenes, list):
                    try:
                        # get the SceneCenter Position
                        sx = allscenes[s]['CenterPosition'].split(',')[0]
                        sy = allscenes[s]['CenterPosition'].split(',')[1]
                        metadata['SceneStageCenterX'].append(np.double(sx))
                        metadata['SceneStageCenterY'].append(np.double(sy))
                    except KeyError as e:
                        print('Stage Positions XY not found :', e)
                        metadata['SceneCenterX'].append(0.0)
                        metadata['SceneCenterY'].append(0.0)
                if not isinstance(allscenes, list):
                    metadata['SceneStageCenterX'].append(0.0)
                    metadata['SceneStageCenterY'].append(0.0)

            # count the number of different wells
            metadata['NumWells'] = len(metadata['WellCounter'].keys())

    except (KeyError, TypeError) as e:
        print('No valid Scene or Well information found:', e)

    # get the dimensions of the bounding boxes for the scenes
    # acces CZI image using aicslibczi
    cziobject = CziFile(filename)
    metadata['BBoxes_Scenes'] = czt.getbboxes_allscenes(cziobject, metadata,
                                                        numscenes=metadata['SizeS'])

    # close CZI file
    czi.close()

    # close AICSImage object
    czi_aics.close()

    return metadata


def get_additional_metadata_czi(filename):
    """
    Returns a dictionary with additional CZI metadata.

    :param filename: filename of the CZI image
    :type filename: str
    :return: additional_czimd - dictionary with additional CZI metainformation
    :rtype: dict
    """

    # get CZI object and read array
    czi = zis.CziFile(filename)

    # parse the XML into a dictionary
    metadatadict_czi = xmltodict.parse(czi.metadata())
    additional_czimd = {}

    try:
        additional_czimd['Experiment'] = metadatadict_czi['ImageDocument']['Metadata']['Experiment']
    except KeyError as e:
        print('Key not found :', e)
        additional_czimd['Experiment'] = None

    try:
        additional_czimd['HardwareSetting'] = metadatadict_czi['ImageDocument']['Metadata']['HardwareSetting']
    except KeyError as e:
        print('Key not found :', e)
        additional_czimd['HardwareSetting'] = None

    try:
        additional_czimd['CustomAttributes'] = metadatadict_czi['ImageDocument']['Metadata']['CustomAttributes']
    except KeyError as e:
        print('Key not found :', e)
        additional_czimd['CustomAttributes'] = None

    try:
        additional_czimd['DisplaySetting'] = metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
    except KeyError as e:
        print('Key not found :', e)
        additional_czimd['DisplaySetting'] = None

    try:
        additional_czimd['Layers'] = metadatadict_czi['ImageDocument']['Metadata']['Layers']
    except KeyError as e:
        print('Key not found :', e)
        additional_czimd['Layers'] = None

    # close CZI file
    czi.close()

    return additional_czimd


def md2dataframe(metadata, paramcol='Parameter', keycol='Value'):
    """Convert the metadata dictionary to a Pandas DataFrame.

    :param metadata: MeteData dictionary
    :type metadata: dict
    :param paramcol: Name of Columns for the MetaData Parameters, defaults to 'Parameter'
    :type paramcol: str, optional
    :param keycol: Name of Columns for the MetaData Values, defaults to 'Value'
    :type keycol: str, optional
    :return: Pandas DataFrame containing all the metadata
    :rtype: Pandas.DataFrame
    """
    mdframe = pd.DataFrame(columns=[paramcol, keycol])

    for k in metadata.keys():
        d = {'Parameter': k, 'Value': metadata[k]}
        df = pd.DataFrame([d], index=[0])
        mdframe = pd.concat([mdframe, df], ignore_index=True)

    return mdframe


def get_dimorder(dimstring):
    """Get the order of dimensions from dimension string

    :param dimstring: string containing the dimensions
    :type dimstring: str
    :return: dims_dict - dictionary with the dimensions and its positions
    :rtype: dict
    :return: dimindex_list - list with indices of dimensions
    :rtype: list
    :return: numvalid_dims - number of valid dimensions
    :rtype: integer
    """

    dimindex_list = []
    dims = ['R', 'I', 'M', 'H', 'V', 'B', 'S', 'T', 'C', 'Z', 'Y', 'X', '0']
    dims_dict = {}

    # loop over all dimensions and find the index
    for d in dims:

        dims_dict[d] = dimstring.find(d)
        dimindex_list.append(dimstring.find(d))

    # check if a dimension really exists
    numvalid_dims = sum(i > 0 for i in dimindex_list)

    return dims_dict, dimindex_list, numvalid_dims


def replace_value(data, value=0):
    """Replace specifc values in array with NaN

    :param data: Array where values should be replaced
    :type data: NumPy.Array
    :param value: value inside array to be replaced with NaN, defaults to 0
    :type value: int, optional
    :return: array with new values
    :rtype: NumPy.Array
    """

    data = data.astype('float')
    data[data == value] = np.nan

    return data


def get_scalefactor(metadata):
    """Add scaling factors to the metadata dictionary

    :param metadata: dictionary with CZI or OME-TIFF metadata
    :type metadata: dict
    :return: dictionary with additional keys for scling factors
    :rtype: dict
    """

    # set default scale factor to 1.0
    scalefactors = {'xy': 1.0,
                    'zx': 1.0
                    }

    try:
        # get the factor between XY scaling
        scalefactors['xy'] = np.round(metadata['XScale'] / metadata['YScale'], 3)
        # get the scalefactor between XZ scaling
        scalefactors['zx'] = np.round(metadata['ZScale'] / metadata['YScale'], 3)
    except (KeyError, TypeError) as e:
        print(e, 'Using defaults = 1.0')

    return scalefactors


def check_for_previewimage(czi):
    """Check if the CZI contains an image from a prescan camera

    :param czi: CZI imagefile object (using czifile)
    :type metadata: CziFile object
    :return: has_attimage - Boolean if CZI image contains prescan image
    :rtype: bool
    """

    att = []

    # loop over the attachments
    for attachment in czi.attachments():
        entry = attachment.attachment_entry
        print(entry.name)
        att.append(entry.name)

    has_attimage = False

    # check for the entry "SlidePreview"
    if 'SlidePreview' in att:
        has_attimage = True

    return has_attimage


def writexml_czi(filename, xmlsuffix='_CZI_MetaData.xml'):
    """Write XML imformation of CZI to disk

    :param filename: CZI image filename
    :type filename: str
    :param xmlsuffix: suffix for the XML file that will be created, defaults to '_CZI_MetaData.xml'
    :type xmlsuffix: str, optional
    :return: filename of the XML file
    :rtype: str
    """

    # open czi file and get the metadata
    czi = zis.CziFile(filename)
    mdczi = czi.metadata()
    czi.close()

    # change file name
    xmlfile = filename.replace('.czi', xmlsuffix)

    # get tree from string
    tree = ET.ElementTree(ET.fromstring(mdczi))

    # write XML file to same folder
    tree.write(xmlfile, encoding='utf-8', method='xml')

    return xmlfile


def getImageSeriesIDforWell(welllist, wellID):
    """
    Returns all ImageSeries (for OME-TIFF) indicies for a specific wellID

    :param welllist: list containing all wellIDs as stringe, e.g. '[B4, B4, B4, B4, B5, B5, B5, B5]'
    :type welllist: list
    :param wellID: string specifying the well, eg.g. 'B4'
    :type wellID: str
    :return: imageseriesindices - list containing all ImageSeries indices, which correspond the the well
    :rtype: list
    """

    imageseries_indices = [i for i, x in enumerate(welllist) if x == wellID]

    return imageseries_indices


def addzeros(number):
    """Convert a number into a string and add leading zeros.
    Typically used to construct filenames with equal lengths.

    :param number: the number
    :type number: int
    :return: zerostring - string with leading zeros
    :rtype: str
    """

    if number < 10:
        zerostring = '0000' + str(number)
    if number >= 10 and number < 100:
        zerostring = '000' + str(number)
    if number >= 100 and number < 1000:
        zerostring = '00' + str(number)
    if number >= 1000 and number < 10000:
        zerostring = '0' + str(number)

    return zerostring


def write_ometiff_aicsimageio(savepath, imgarray, metadata,
                              reader='aicsimageio',
                              overwrite=False):
    """Write an OME-TIFF file from an image array based on the metadata.

    :param filepath: savepath of the OME-TIFF stack
    :type filepath: str
    :param imgarray: multi-dimensional image array
    :type imgarray: NumPy.Array
    :param metadata: metadata dictionary with the required information
    to create an correct OME-TIFF file
    :type metadata: dict
    :param reader: string (aicsimagio or czifile) specifying
    the used reader, defaults to aicsimageio
    :type metadata: str
    :param overwrite: option to overwrite an existing OME-TIFF, defaults to False
    :type overwrite: bool, optional
    """

    # define scaling from metadata or use defualt scaling
    try:
        pixels_physical_size = [metadata['XScale'],
                                metadata['YScale'],
                                metadata['ZScale']]
    except KeyError as e:
        print('Key not found:', e)
        print('Use default scaling XYZ=1.0')
        pixels_physical_size = [1.0, 1.0, 1.0]

    # define channel names list from metadata
    try:
        channel_names = []
        for ch in metadata['Channels']:
            channel_names.append(ch)
    except KeyError as e:
        print('Key not found:', e)
        channel_names = None

    # get the dimensions and their position inside the dimension string
    if reader == 'aicsimageio':

        dims_dict, dimindex_list, numvalid_dims = get_dimorder(metadata['Axes_aics'])

        # if the array has more than 5 dimensions then remove the S dimension
        # because it is not supported by OME-TIFF
        if len(imgarray.shape) > 5:
            try:
                imgarray = np.squeeze(imgarray, axis=dims_dict['S'])
            except Exception:
                print('Could not remover S Dimension from string.)')

        # remove the S character from the dimension string
        new_dimorder = metadata['Axes_aics'].replace('S', '')

    if reader == 'czifile':

        new_dimorder = metadata['Axes']
        dims_dict, dimindex_list, numvalid_dims = get_dimorder(metadata['Axes'])
        """
        '0':'Sample',  # e.g. RGBA
        'X':'Width',
        'Y':'Height',
        'C':'Channel',
        'Z':'Slice',  # depth
        'T':'Time',
        'R':'Rotation',
        'S':'Scene',  # contiguous regions of interest in a mosaic image
        'I':'Illumination',  # direction
        'B':'Block',  # acquisition
        'M':'Mosaic',  # index of tile for compositing a scene
        'H':'Phase',  # e.g. Airy detector fibers
        'V':'View',  # e.g. for SPIM
        """

        to_remove = []

        # list of unspupported dims for writing an OME-TIFF
        dims = ['R', 'I', 'M', 'H', 'V', 'B', 'S', '0']

        for dim in dims:
            if dims_dict[dim] >= 0:
                # remove the CZI DIMENSION character from the dimension string
                new_dimorder = new_dimorder.replace(dim, '')
                # add dimension index to the list of axis to be removed
                to_remove.append(dims_dict[dim])
                print('Remove Dimension:', dim)

        # create tuple with dimensions to be removed
        dims2remove = tuple(to_remove)
        # remove dimensions from array
        imgarray = np.squeeze(imgarray, axis=dims2remove)

    # write the array as an OME-TIFF incl. the metadata
    try:
        with ome_tiff_writer.OmeTiffWriter(savepath, overwrite_file=overwrite) as writer:
            writer.save(imgarray,
                        channel_names=channel_names,
                        ome_xml=None,
                        image_name=os.path.basename((savepath)),
                        pixels_physical_size=pixels_physical_size,
                        channel_colors=None,
                        dimension_order=new_dimorder)
            writer.close()
    except Exception as error:
        print(error.__class__.__name__ + ": " + error.msg)
        print('Could not write OME-TIFF')
        savepath = None

    return savepath


def get_fname_woext(filepath):
    """Get the complete path of a file without the extension
    It alos will works for extensions like c:\myfile.abc.xyz
    The output will be: c:\myfile

    :param filepath: complete fiepath
    :type filepath: str
    :return: complete filepath without extension
    :rtype: str
    """
    # create empty string
    real_extension = ''

    # get all part of the file extension
    sufs = Path(filepath).suffixes
    for s in sufs:
        real_extension = real_extension + s

    # remover real extension from filepath
    filepath_woext = filepath.replace(real_extension, '')

    return filepath_woext


def convert_to_ometiff(imagefilepath,
                       bftoolsdir='/Users/bftools',
                       czi_include_attachments=False,
                       czi_autostitch=True,
                       verbose=True):
    """Convert image file using bfconvert tool into a OME-TIFF from with a python script.

    :param imagefilepath: path to imagefile
    :type imagefilepath: str
    :param bftoolsdir: bftools directory containing the bfconvert, defaults to '/Users/bftools'
    :type bftoolsdir: str, optional
    :param czi_include_attachments: option convert a CZI attachment (if CZI), defaults to False
    :type czi_include_attachments: bool, optional
    :param czi_autostitch: option stich a CZI, defaults to True
    :type czi_autostitch: bool, optional
    :param verbose: show additional output, defaults to True
    :type verbose: bool, optional
    :return: fileparh of created OME-TIFF file
    :rtype: str
    """
    # check if path exits
    if not os.path.exists(bftoolsdir):
        print('No bftools dirctory found. Nothing will be converted')
        file_ometiff = None

    if os.path.exists(bftoolsdir):

        # set working dir
        os.chdir(bftoolsdir)

        # get the imagefile path without extension
        imagefilepath_woext = get_fname_woext(imagefilepath)

        # create imagefile path for OME-TIFF
        file_ometiff = imagefilepath_woext + '.ome.tiff'

        # create cmdstring for CZI files- mind the spaces !!!
        if imagefilepath.lower().endswith('.czi'):

            # configure the CZI options
            if czi_include_attachments:
                czi_att = 'true'
            if not czi_include_attachments:
                czi_att = 'false'

            if czi_autostitch:
                czi_stitch = 'true'
            if not czi_autostitch:
                czi_stitch = 'false'

            # create cmdstring - mind the spaces !!!
            cmdstring = 'bfconvert -no-upgrade -option zeissczi.attachments ' + czi_att + ' -option zeissczi.autostitch ' + \
                czi_stitch + ' "' + imagefilepath + '" "' + file_ometiff + '"'

        else:
            # create cmdstring for non-CZIs- mind the spaces !!!
            cmdstring = 'bfconvert -no-upgrade' + ' "' + imagefilepath + '" "' + file_ometiff + '"'

        if verbose:
            print('Original ImageFile :', imagefilepath_woext)
            print('ImageFile OME.TIFF :', file_ometiff)
            print('Use CMD :', cmdstring)

        # run the bfconvert tool with the specified parameters
        os.system(cmdstring)
        print('Done.')

    return file_ometiff


def get_dimpositions(dimstring, tocheck=['B', 'S', 'T', 'Z', 'C']):
    """Simple function to get the indices of the dimension identifiers in a string

    :param dimstring: dimension string
    :type dimstring: str
    :param tocheck: list of entries to check, defaults to ['B', 'S', 'T', 'Z', 'C']
    :type tocheck: list, optional
    :return: dictionary with positions of dimensions inside string
    :rtype: dict
    """
    dimpos = {}
    for p in tocheck:
        dimpos[p] = dimstring.find(p)

    return dimpos


def update5dstack(image5d, image2d,
                  dimstring5d='TCZYX',
                  t=0,
                  z=0,
                  c=0):

    # remove XY
    dimstring5d = dimstring5d.replace('X', '').replace('Y', '')

    if dimstring5d == 'TZC':
        image5d[t, z, c, :, :] = image2d
    if dimstring5d == 'TCZ':
        image5d[t, c, z, :, :] = image2d
    if dimstring5d == 'ZTC':
        image5d[z, t, c, :, :] = image2d
    if dimstring5d == 'ZCT':
        image5d[z, c, t, :, :] = image2d
    if dimstring5d == 'CTZ':
        image5d[c, t, z, :, :] = image2d
    if dimstring5d == 'CZT':
        image5d[c, z, t, :, :] = image2d

    return image5d


def getdims_pylibczi(czi):

    # Get the shape of the data, the coordinate pairs are (start index, size)
    # [{'X': (0, 1900), 'Y': (0, 1300), 'Z': (0, 60), 'C': (0, 4), 'S': (0, 40), 'B': (0, 1)}]
    # dimensions = czi.dims_shape()

    dimsizes = {}
    for d in range(len(czi.dims)):
        # print(d)
        dimsizes['Size' + czi.dims[d]] = czi.size[d]

    return dimsizes


# function to return key for any value
def get_key(my_dict, val):
    """Get the key based on a value

    :param my_dict: dictionary with key - value pair
    :type my_dict: [dict
    :param val: value used to find the key
    :type val: any
    :return: key
    :rtype: any
    """
    for key, value in my_dict.items():
        if val == value:
            return key

    return None


def expand_dims5d(array, metadata):

    # Expand image array to 5D of order (T, Z, C, X, Y)
    if metadata['SizeC'] == 1:
        array = np.expand_dims(array, axis=-3)
    if metadata['SizeZ'] == 1:
        array = np.expand_dims(array, axis=-4)
    if metadata['SizeT'] == 1:
        array = np.expand_dims(array, axis=-5)

    return array
