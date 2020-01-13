# this can be used to switch on/off warnings
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import czifile as zis
from apeer_ometiff_library import io, processing, omexmlClass
import os
from skimage.external import tifffile
import ipywidgets as widgets
from matplotlib import pyplot as plt, cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import xmltodict
import numpy as np
from collections import Counter
#import xml.etree.ElementTree as ET
from lxml import etree as ET
import napari
import time
import re


def get_imgtype(imagefile):
    """
    Returns the type of the image based on the file extension - no magic

    :param imagefile: filename of the image
    :return: imgtype - string specifying the image type
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
    """
    A Python dictionary will be created to hold the relevant metadata.

    :return: metadata - dictionary with keys for the relevant metadata
    """

    metadata = {'Directory': None,
                'Filename': None,
                'Extension': None,
                'ImageType': None,
                'Name': None,
                'AcqDate': None,
                'TotalSeries': None,
                'SizeX': None,
                'SizeY': None,
                'SizeZ': None,
                'SizeC': None,
                'SizeT': None,
                'Sizes BF': None,
                'DimOrder BF': None,
                'DimOrder BF Array': None,
                'DimOrder CZI': None,
                'Axes': None,
                'Shape': None,
                'isRGB': None,
                'ObjNA': None,
                'ObjMag': None,
                'ObjID': None,
                'ObjName': None,
                'ObjImmersion': None,
                'XScale': None,
                'YScale': None,
                'ZScale': None,
                'XScaleUnit': None,
                'YScaleUnit': None,
                'ZScaleUnit': None,
                'DetectorModel': [],
                'DetectorName': [],
                'DetectorID': None,
                'InstrumentID': None,
                'Channels': [],
                'ImageIDs': [],
                'NumPy.dtype': None
                }

    return metadata


def get_metadata(imagefile, series=0):
    """
    Returns a dictionary with metadata depending on the image type
    Only CZI and OME-TIFF are currently supported.

    :param imagefile: filename of the image
    :param series: series of OME-TIFF file
    :return: metadata - dictionary with the metainformation
    :return: additional_mdczi - dictionary with additional CZI metadata
    """

    # get the image type
    imgtype = get_imgtype(imagefile)
    print('Image Type: ', imgtype)

    md = None
    additional_mdczi = None

    if imgtype == 'ometiff':

        with tifffile.TiffFile(imagefile) as tif:
            # get OME-XML metadata as string
            omexml = tif[0].image_description.decode('utf-8')

        # get the OME-XML using the apeer-ometiff-library
        omemd = omexmlClass.OMEXML(omexml)

        # parse the OME-XML and return the metadata dictionary and additional information
        md = get_metadata_ometiff(imagefile, omemd, series=series)

    if imgtype == 'czi':

        # parse the CZI metadata return the metadata dictionary and additional information
        md = get_metadata_czi(imagefile, dim2none=False)
        additional_mdczi = get_additional_metadata_czi(imagefile)

    return md, additional_mdczi


def get_metadata_ometiff(filename, omemd, series=0):
    """
    Returns a dictionary with OME-TIFF metadata.

    :param filename: filename of the OME-TIFF image
    :param omemd: OME-XML information
    :param series
    :return: metadata - dictionary with the relevant OME-TIFF metainformation
    """

    # create dictionary for metadata and get OME-XML data
    metadata = create_metadata_dict()

    # get directory and filename etc.
    metadata['Directory'] = os.path.dirname(filename)
    metadata['Filename'] = os.path.basename(filename)
    metadata['Extension'] = 'ome.tiff'
    metadata['ImageType'] = 'ometiff'
    metadata['AcqDate'] = omemd.image(series).AcquisitionDate
    metadata['Name'] = omemd.image(series).Name

    # get image dimensions
    metadata['SizeT'] = omemd.image(series).Pixels.SizeT
    metadata['SizeZ'] = omemd.image(series).Pixels.SizeZ
    metadata['SizeC'] = omemd.image(series).Pixels.SizeC
    metadata['SizeX'] = omemd.image(series).Pixels.SizeX
    metadata['SizeY'] = omemd.image(series).Pixels.SizeY

    # get number of series
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
    metadata['XScaleUnit'] = omemd.image(series).Pixels.PhysicalSizeXUnit
    metadata['YScale'] = omemd.image(series).Pixels.PhysicalSizeY
    metadata['YScaleUnit'] = omemd.image(series).Pixels.PhysicalSizeYUnit
    metadata['ZScale'] = omemd.image(series).Pixels.PhysicalSizeZ
    metadata['ZScaleUnit'] = omemd.image(series).Pixels.PhysicalSizeZUnit

    # get all image IDs
    for i in range(omemd.get_image_count()):
        metadata['ImageIDs'].append(i)

    # get information about the instrument and objective
    try:
        metadata['InstrumentID'] = omemd.instrument(series).get_ID()
    except:
        metadata['InstrumentID'] = None

    try:
        metadata['DetectorModel'] = omemd.instrument(series).Detector.get_Model()
        metadata['DetectorID'] = omemd.instrument(series).Detector.get_ID()
        metadata['DetectorModel'] = omemd.instrument(series).Detector.get_Type()
    except:
        metadata['DetectorModel'] = None
        metadata['DetectorID'] = None
        metadata['DetectorModel'] = None

    try:
        metadata['ObjNA'] = omemd.instrument(series).Objective.get_LensNA()
        metadata['ObjID'] = omemd.instrument(series).Objective.get_ID()
        metadata['ObjMag'] = omemd.instrument(series).Objective.get_NominalMagnification()
    except:
        metadata['ObjNA'] = None
        metadata['ObjID'] = None
        metadata['ObjMag'] = None

    # get channel names
    for c in range(metadata['SizeC']):
        metadata['Channels'].append(omemd.image(series).Pixels.Channel(c).Name)

    return metadata


def get_metadata_czi(filename, dim2none=False):
    """
    Returns a dictionary with CZI metadata.

    Information CZI Dimension Characters:
    '0': 'Sample',  # e.g. RGBA
    'X': 'Width',
    'Y': 'Height',
    'C': 'Channel',
    'Z': 'Slice',  # depth
    'T': 'Time',
    'R': 'Rotation',
    'S': 'Scene',  # contiguous regions of interest in a mosaic image
    'I': 'Illumination',  # direction
    'B': 'Block',  # acquisition
    'M': 'Mosaic',  # index of tile for compositing a scene
    'H': 'Phase',  # e.g. Airy detector fibers
    'V': 'View',  # e.g. for SPIM

    :param filename: filename of the CZI image
    :param dim2none: option to set non-existing dimension to None
    :return: metadata - dictionary with the relevant CZI metainformation
    """

    # get CZI object and read array
    czi = zis.CziFile(filename)
    #mdczi = czi.metadata()

    # parse the XML into a dictionary
    metadatadict_czi = xmltodict.parse(czi.metadata())
    metadata = create_metadata_dict()

    # get directory and filename etc.
    metadata['Directory'] = os.path.dirname(filename)
    metadata['Filename'] = os.path.basename(filename)
    metadata['Extension'] = 'czi'
    metadata['ImageType'] = 'czi'

    # add axes and shape information
    metadata['Axes'] = czi.axes
    metadata['Shape'] = czi.shape

    # determine pixel type for CZI array
    metadata['NumPy.dtype'] = czi.dtype

    # check if the CZI image is an RGB image depending on the last dimension entry of axes
    if czi.axes[-1] == 3:
        metadata['isRGB'] = True

    metadata['Information'] = metadatadict_czi['ImageDocument']['Metadata']['Information']
    try:
        metadata['PixelType'] = metadata['Information']['Image']['PixelType']
    except KeyError as e:
        print('Key not found:', e)
        metadata['PixelType'] = None

    metadata['SizeX'] = np.int(metadata['Information']['Image']['SizeX'])
    metadata['SizeY'] = np.int(metadata['Information']['Image']['SizeY'])

    try:
        metadata['SizeZ'] = np.int(metadata['Information']['Image']['SizeZ'])
    except:
        if dim2none:
            metadata['SizeZ'] = None
        if not dim2none:
            metadata['SizeZ'] = 1

    try:
        metadata['SizeC'] = np.int(metadata['Information']['Image']['SizeC'])
    except:
        if dim2none:
            metadata['SizeC'] = None
        if not dim2none:
            metadata['SizeC'] = 1

    channels = []
    for ch in range(metadata['SizeC']):
        try:
            channels.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                            ['Channels']['Channel'][ch]['ShortName'])
        except:
            try:
                channels.append(metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
                                                ['Channels']['Channel']['ShortName'])
            except:
                channels.append(str(ch))

    metadata['Channels'] = channels

    try:
        metadata['SizeT'] = np.int(metadata['Information']['Image']['SizeT'])
    except:
        if dim2none:
            metadata['SizeT'] = None
        if not dim2none:
            metadata['SizeT'] = 1

    try:
        metadata['SizeM'] = np.int(metadata['Information']['Image']['SizeM'])
    except:
        if dim2none:
            metadatada['SizeM'] = None
        if not dim2none:
            metadata['SizeM'] = 1

    try:
        metadata['SizeB'] = np.int(metadata['Information']['Image']['SizeB'])
    except:

        if dim2none:
            metadatada['SizeB'] = None
        if not dim2none:
            metadata['SizeB'] = 1

    try:
        metadata['SizeS'] = np.int(metadata['Information']['Image']['SizeS'])
    except:
        if dim2none:
            metadatada['SizeS'] = None
        if not dim2none:
            metadata['SizeS'] = 1

    try:
        metadata['Scaling'] = metadatadict_czi['ImageDocument']['Metadata']['Scaling']
        metadata['XScale'] = float(metadata['Scaling']['Items']['Distance'][0]['Value']) * 1000000
        metadata['YScale'] = float(metadata['Scaling']['Items']['Distance'][1]['Value']) * 1000000
        metadata['XScale'] = np.round(metadata['XScale'], 3)
        metadata['YScale'] = np.round(metadata['YScale'], 3)
        try:
            metadata['XScaleUnit'] = metadata['Scaling']['Items']['Distance'][0]['DefaultUnitFormat']
            metadata['YScaleUnit'] = metadata['Scaling']['Items']['Distance'][1]['DefaultUnitFormat']
        except:
            metadata['XScaleUnit'] = None
            metadata['YScaleUnit'] = None
        try:
            metadata['ZScale'] = float(metadata['Scaling']['Items']['Distance'][2]['Value']) * 1000000
            metadata['ZScale'] = np.round(metadata['ZScale'], 3)
            try:
                metadata['ZScaleUnit'] = metadata['Scaling']['Items']['Distance'][2]['DefaultUnitFormat']
            except:
                metadata['ZScaleUnit'] = metadata['XScaleUnit']
        except:
            if dim2none:
                metadata['ZScale'] = metadata['XScaleUnit']
            if not dim2none:
                # set to isotropic scaling if it was single plane only
                metadata['ZScale'] = metadata['XScale']
    except:
        metadata['Scaling'] = None

    # try to get software version
    try:
        metadata['SW-Name'] = metadata['Information']['Application']['Name']
        metadata['SW-Version'] = metadata['Information']['Application']['Version']
    except KeyError as e:
        print('Key not found:', e)
        metadata['SW-Name'] = None
        metadata['SW-Version'] = None

    try:
        metadata['AcqDate'] = metadata['Information']['Image']['AcquisitionDateAndTime']
    except KeyError as e:
        print('Key not found:', e)
        metadata['AcqDate'] = None

    try:
        metadata['Instrument'] = metadata['Information']['Instrument']
    except KeyError as e:
        print('Key not found:', e)
        metadata['Instrument'] = None

    if metadata['Instrument'] is not None:

        # get objective data
        try:
            metadata['ObjName'] = metadata['Instrument']['Objectives']['Objective']['@Name']
        except:
            metadata['ObjName'] = None

        try:
            metadata['ObjImmersion'] = metadata['Instrument']['Objectives']['Objective']['Immersion']
        except:
            metadata['ObjImmersion'] = None

        try:
            metadata['ObjNA'] = np.float(metadata['Instrument']['Objectives']['Objective']['LensNA'])
        except:
            metadata['ObjNA'] = None

        try:
            metadata['ObjID'] = metadata['Instrument']['Objectives']['Objective']['@Id']
        except:
            metadata['ObjID'] = None

        try:
            metadata['TubelensMag'] = np.float(metadata['Instrument']['TubeLenses']['TubeLens']['Magnification'])
        except:
            metadata['TubelensMag'] = None

        try:
            metadata['ObjNominalMag'] = np.float(metadata['Instrument']['Objectives']['Objective']['NominalMagnification'])
        except KeyError as e:
            metadata['ObjNominalMag'] = None

        try:
            metadata['ObjMag'] = metadata['ObjNominalMag'] * metadata['TubelensMag']
        except:
            metadata['ObjMag'] = None

        # get detector information
        try:
            metadata['DetectorID'] = metadata['Instrument']['Detectors']['Detector']['@Id']
        except:
            metadata['DetectorID'] = None

        try:
            metadata['DetectorModel'] = metadata['Instrument']['Detectors']['Detector']['@Name']
        except:
            metadata['DetectorModel'] = None

        try:
            metadata['DetectorName'] = metadata['Instrument']['Detectors']['Detector']['Manufacturer']['Model']
        except:
            metadata['DetectorName'] = None

        # delete some key from dict
        del metadata['Instrument']

    # check for well information
    metadata['Well_ArrayNames'] = []
    metadata['Well_Indices'] = []
    metadata['Well_PositionNames'] = []
    metadata['Well_ColId'] = []
    metadata['Well_RowId'] = []
    metadata['WellCounter'] = None

    try:
        # extract well information from the dictionary
        allscenes = metadata['Information']['Image']['Dimensions']['S']['Scenes']['Scene']

        # loop over all detected scenes
        for s in range(metadata['SizeS']):

            # more than one scene detected
            if metadata['SizeS'] > 1:
                # get the current well and add the array name to the metadata
                well = allscenes[s]
                metadata['Well_ArrayNames'].append(well['ArrayName'])

            # exactly one scene detected (e.g. after split scenes etc.)
            elif metadata['SizeS'] == 1:
                # only get the current well - nor arraynames exist !
                well = allscenes

            # get the well information
            metadata['Well_Indices'].append(well['@Index'])
            metadata['Well_PositionNames'].append(well['@Name'])
            metadata['Well_ColId'].append(well['Shape']['ColumnIndex'])
            metadata['Well_RowId'].append(well['Shape']['RowIndex'])

            # more than one scene detected
            if metadata['SizeS'] > 1:
                # count the content of the list, e.g. how many time a certain well was detected
                metadata['WellCounter'] = Counter(metadata['Well_ArrayNames'])

            # exactly one scene detected (e.g. after split scenes etc.)
            elif metadata['SizeS'] == 1:

                # set ArrayNames equal to PositionNames for convenience
                metadata['Well_ArrayNames'] = metadata['Well_PositionNames']

                # count the content of the list, e.g. how many time a certain well was detected
                metadata['WellCounter'] = Counter(metadata['Well_PositionNames'])

            # count the number of different wells
            metadata['NumWells'] = len(metadata['WellCounter'].keys())

    except KeyError as e:
        print('Key not found in Metadata Dictionary:', e)
        print('No Scence or Well Information detected.')

    del metadata['Information']
    del metadata['Scaling']

    # close CZI file
    czi.close()

    return metadata


def get_additional_metadata_czi(filename):
    """
    Returns a dictionary with additional CZI metadata.

    :param filename: filename of the CZI image
    :return: additional_czimd - dictionary with the relevant OME-TIFF metainformation
    """

    # get CZI object and read array
    czi = zis.CziFile(filename)

    # parse the XML into a dictionary
    metadatadict_czi = xmltodict.parse(czi.metadata())
    additional_czimd = {}

    try:
        additional_czimd['Experiment'] = metadatadict_czi['ImageDocument']['Metadata']['Experiment']
    except:
        additional_czimd['Experiment'] = None

    try:
        additional_czimd['HardwareSetting'] = metadatadict_czi['ImageDocument']['Metadata']['HardwareSetting']
    except:
        additional_czimd['HardwareSetting'] = None

    try:
        additional_czimd['CustomAttributes'] = metadatadict_czi['ImageDocument']['Metadata']['CustomAttributes']
    except:
        additional_czimd['CustomAttributes'] = None

    try:
        additional_czimd['DisplaySetting'] = metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
    except KeyError as e:
        print('Key not found:', e)
        additional_czimd['DisplaySetting'] = None

    try:
        additional_czimd['Layers'] = metadatadict_czi['ImageDocument']['Metadata']['Layers']
    except KeyError as e:
        print('Key not found:', e)
        additional_czimd['Layers'] = None

    # close CZI file
    czi.close()

    return additional_czimd


def create_ipyviewer_ome_tiff(array, metadata):
    """
    Creates a simple interactive viewer inside a Jupyter Notebook.
    Works with OME-TIFF files and the respective metadata

    :param array: multidimensional array containing the pixel data
    :param metadata: dictionary with the metainformation
    :return: out - interactive widgets
    :return: ui - ui for interactive widgets
    """

    # time slider
    t = widgets.IntSlider(description='Time:',
                          min=1,
                          max=metadata['SizeT'],
                          step=1,
                          value=1,
                          continuous_update=False)

    # zplane lsider
    z = widgets.IntSlider(description='Z-Plane:',
                          min=1,
                          max=metadata['SizeZ'],
                          step=1,
                          value=1,
                          continuous_update=False)

    # channel slider
    c = widgets.IntSlider(description='Channel:',
                          min=1,
                          max=metadata['SizeC'],
                          step=1,
                          value=1)

    # slider for contrast
    r = widgets.IntRangeSlider(description='Display Range:',
                               min=array.min(),
                               max=array.max(),
                               step=1,
                               value=[array.min(), array.max()],
                               continuous_update=False)

    # disable slider that are not needed
    if metadata['SizeT'] == 1:
        t.disabled = True
    if metadata['SizeZ'] == 1:
        z.disabled = True
    if metadata['SizeC'] == 1:
        c.disabled = True

    sliders = metadata['DimOrder BF Array'][:-2] + 'R'

    # TODO: this section is not complete, because it does not contain all possible cases
    # TODO: it is still under constrcution and can be done probably in a much smarter way

    if sliders == 'CTZR':
        ui = widgets.VBox([c, t, z, r])

        def get_TZC_czi(c_ind, t_ind, z_ind, r):
            display_image(array, metadata, sliders, c=c_ind, t=t_ind, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'c_ind': c, 't_ind': t, 'z_ind': z, 'r': r})

    if sliders == 'TZCR':
        ui = widgets.VBox([t, z, c, r])

        def get_TZC_czi(t_ind, z_ind, c_ind, r):
            display_image(array, metadata, sliders, t=t_ind, z=z_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'t_ind': t, 'z_ind': z, 'c_ind': c, 'r': r})

    if sliders == 'TCZR':
        ui = widgets.VBox([t, c, z, r])

        def get_TZC_czi(t_ind, c_ind, z_ind, r):
            display_image(array, metadata, sliders, t=t_ind, c=t_ind, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'t_ind': t, 'c_ind': c, 'z_ind': z, 'r': r})

    if sliders == 'CZTR':
        ui = widgets.VBox([c, z, t, r])

        def get_TZC_czi(c_ind, z_ind, t_ind, r):
            display_image(array, metadata, sliders, c=c_ind, z=z_ind, t=t_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'c_ind': c, 'z_ind': z, 't_ind': t, 'r': r})

    if sliders == 'ZTCR':
        ui = widgets.VBox([z, t, c, r])

        def get_TZC_czi(z_ind, t_ind, c_ind, r):
            display_image(array, metadata, sliders, z=z_ind, t=t_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'z_ind': z, 't_ind': t, 'c_ind': c, 'r': r})

    if sliders == 'ZCTR':
        ui = widgets.VBox([z, c, t, r])

        def get_TZC_czi(z_ind, c_ind, t_ind, r):
            display_image(array, metadata, sliders, z=z_ind, c=c_ind, t=t_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'z_ind': z, 'c_ind': c, 't_ind': t, 'r': r})

    """
    ui = widgets.VBox([t, z, c, r])

    def get_TZC_ometiff(t, z, c, r):
        display_image(array, metadata, 'TZCR', t=t, z=z, c=c, vmin=r[0], vmax=r[1])

    out = widgets.interactive_output(get_TZC_ometiff, {'t': t, 'z': z, 'c': c, 'r': r})
    """

    return out, ui  # , t, z, c, r


def create_ipyviewer_czi(cziarray, metadata):
    """
    Creates a simple interactive viewer inside a Jupyter Notebook.
    Works with CZI files and the respective metadata

    :param cziarray: multidimensional array containing the pixel data
    :param metadata: dictionary with the metainformation
    :return: out - interactive widgets
    :return: ui - ui for interactive widgets
    """

    dim_dict = metadata['DimOrder CZI']

    useB = False
    useS = False

    if 'B' in dim_dict and dim_dict['B'] >= 0:
        useB = True
        b = widgets.IntSlider(description='Blocks:',
                              min=1,
                              max=metadata['SizeB'],
                              step=1,
                              value=1,
                              continuous_update=False)

    if 'S' in dim_dict and dim_dict['S'] >= 0:
        useS = True
        s = widgets.IntSlider(description='Scenes:',
                              min=1,
                              max=metadata['SizeS'],
                              step=1,
                              value=1,
                              continuous_update=False)

    t = widgets.IntSlider(description='Time:',
                          min=1,
                          max=metadata['SizeT'],
                          step=1,
                          value=1,
                          continuous_update=False)

    z = widgets.IntSlider(description='Z-Plane:',
                          min=1,
                          max=metadata['SizeZ'],
                          step=1,
                          value=1,
                          continuous_update=False)

    c = widgets.IntSlider(description='Channel:',
                          min=1,
                          max=metadata['SizeC'],
                          step=1,
                          value=1)

    print(cziarray.min(), cziarray.max())

    r = widgets.IntRangeSlider(description='Display Range:',
                               min=cziarray.min(),
                               max=cziarray.max(),
                               step=1,
                               value=[cziarray.min(), cziarray.max()],
                               continuous_update=False)

    # disable slider that are not needed
    if metadata['SizeB'] == 1 and useB:
        b.disabled = True
    if metadata['SizeS'] == 1 and useS:
        s.disabled = True
    if metadata['SizeT'] == 1:
        t.disabled = True
    if metadata['SizeZ'] == 1:
        z.disabled = True
    if metadata['SizeC'] == 1:
        c.disabled = True

    sliders = metadata['Axes'][:-3] + 'R'

    # TODO: this section is not complete, because it does not contain all possible cases
    # TODO: it is still under constrcution and can be done probably in a much smarter way

    if sliders == 'BTZCR':
        ui = widgets.VBox([b, t, z, c, r])

        def get_TZC_czi(b_ind, t_ind, z_ind, c_ind, r):
            display_image(cziarray, metadata, sliders, b=b_ind, t=t_ind, z=z_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'b_ind': b, 't_ind': t, 'z_ind': z, 'c_ind': c, 'r': r})

    if sliders == 'BTCZR':
        ui = widgets.VBox([b, t, c, z, r])

        def get_TZC_czi(b_ind, t_ind, c_ind, z_ind, r):
            display_image(cziarray, metadata, sliders, b=b_ind, t=t_ind, c=c_ind, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'b_ind': b, 't_ind': t, 'c_ind': c, 'z_ind': z, 'r': r})

    if sliders == 'BSTZCR':
        ui = widgets.VBox([b, s, t, z, c, r])

        def get_TZC_czi(b_ind, s_ind, t_ind, z_ind, c_ind, r):
            display_image(cziarray, metadata, sliders, b=b_ind, s=s_ind, t=t_ind, z=z_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'b_ind': b, 's_ind': s, 't_ind': t, 'z_ind': z, 'c_ind': c, 'r': r})

    if sliders == 'BSCR':
        ui = widgets.VBox([b, s, c, r])

        def get_TZC_czi(b_ind, s_ind, c_ind, r):
            display_image(cziarray, metadata, sliders, b=b_ind, s=s_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'b_ind': b, 's_ind': s, 'c_ind': c, 'r': r})

    if sliders == 'BSTCZR':
        ui = widgets.VBox([b, s, t, c, z, r])

        def get_TZC_czi(b_ind, s_ind, t_ind, c_ind, z_ind, r):
            display_image(cziarray, metadata, sliders, b=b_ind, s=s_ind, t=t_ind, c=c_ind, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'b_ind': b, 's_ind': s, 't_ind': t, 'c_ind': c, 'z_ind': z, 'r': r})

    if sliders == 'STZCR':
        ui = widgets.VBox([s, t, z, c, r])

        def get_TZC_czi(s_ind, t_ind, z_ind, c_ind, r):
            display_image(cziarray, metadata, sliders, s=s_ind, t=t_ind, z=z_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'s_ind': s, 't_ind': t, 'z_ind': z, 'c_ind': c, 'r': r})

    if sliders == 'STCZR':
        ui = widgets.VBox([s, t, c, z, r])

        def get_TZC_czi(s_ind, t_ind, c_ind, z_ind, r):
            display_image(cziarray, metadata, sliders, s=s_ind, t=t_ind, c=c_ind, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'s_ind': s, 't_ind': t, 'c_ind': c, 'z_ind': z, 'r': r})

    if sliders == 'TZCR':
        ui = widgets.VBox([t, z, c, r])

        def get_TZC_czi(t_ind, z_ind, c_ind, r):
            display_image(cziarray, metadata, sliders, t=t_ind, z=z_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'t_ind': t, 'z_ind': z, 'c_ind': c, 'r': r})

    if sliders == 'TCZR':
        ui = widgets.VBox([t, c, z, r])

        def get_TZC_czi(t_ind, c_ind, z_ind, r):
            display_image(cziarray, metadata, sliders, t=t_ind, c=c_ind, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'t_ind': t, 'c_ind': c, 'z_ind': z, 'r': r})

    if sliders == 'SCR':
        ui = widgets.VBox([s, c, r])

        def get_TZC_czi(s_ind, c_ind, r):
            display_image(cziarray, metadata, sliders, s=s_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'s_ind': s, 'c_ind': c, 'r': r})

    if sliders == 'ZR':
        ui = widgets.VBox([z, r])

        def get_TZC_czi(z_ind, r):
            display_image(cziarray, metadata, sliders, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'z_ind': z, 'r': r})

    if sliders == 'TR':
        ui = widgets.VBox([t, r])

        def get_TZC_czi(t_ind, r):
            display_image(cziarray, metadata, sliders, t=t_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'t_ind': t, 'r': r})

    if sliders == 'CR':
        ui = widgets.VBox([c, r])

        def get_TZC_czi(c_ind, r):
            display_image(cziarray, metadata, sliders, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'c_ind': c, 'r': r})

    if sliders == 'BTCR':
        ui = widgets.VBox([b, t, c, r])

        def get_TZC_czi(b_ind, t_ind, c_ind, r):
            display_image(cziarray, metadata, sliders, b=b_ind, t=t_ind, c=c_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'b_ind': b, 't_ind': t, 'c_ind': c, 'r': r})

    ############### Lightsheet data #################

    if sliders == 'VIHRSCTZR':
        ui = widgets.VBox([c, t, z, r])

        def get_TZC_czi(c_ind, t_ind, z_ind, r):
            display_image(cziarray, metadata, sliders, c=c_ind, t=t_ind, z=z_ind, vmin=r[0], vmax=r[1])

        out = widgets.interactive_output(get_TZC_czi, {'c_ind': c, 't_ind': t, 'z_ind': z, 'r': r})

    return out, ui


def display_image(array, metadata, sliders,
                  b=0,
                  s=0,
                  m=0,
                  t=0,
                  c=0,
                  z=0,
                  vmin=0,
                  vmax=1000):
    """
    Displays the CZI or OME-TIFF image using a simple interactive viewer
    inside a Jupyter Notebook with dimension sliders.

    :param array: multidimensional array containing the pixel data
    :param metadata: dictionary with the metainformation
    :param sliders: string specifying the required sliders
    """

    dim_dict = metadata['DimOrder CZI']

    if metadata['ImageType'] == 'ometiff':

        if sliders == 'TZCR':
            image = array[t - 1, z - 1, c - 1, :, :]

        if sliders == 'CTZR':
            image = array[c - 1, t - 1, z - 1, :, :]

        if sliders == 'TCZR':
            image = array[t - 1, c - 1, z - 1, :, :]

        if sliders == 'CZTR':
            image = array[c - 1, z - 1, t - 1, :, :]

        if sliders == 'ZTCR':
            image = array[z - 1, t - 1, c - 1, :, :]

        if sliders == 'ZCTR':
            image = array[z - 1, c - 1, z - 1, :, :]

    if metadata['ImageType'] == 'czi':

        # add more dimension orders when needed
        if sliders == 'BTZCR':
            if metadata['isRGB']:
                image = array[b - 1, t - 1, z - 1, c - 1, :, :, :]
            else:
                image = array[b - 1, t - 1, z - 1, c - 1, :, :]

        if sliders == 'BTCZR':
            if metadata['isRGB']:
                image = array[b - 1, t - 1, c - 1, z - 1, :, :, :]
            else:
                image = array[b - 1, t - 1, c - 1, z - 1, :, :]

        if sliders == 'BSTZCR':
            if metadata['isRGB']:
                image = array[b - 1, s - 1, t - 1, z - 1, c - 1, :, :, :]
            else:
                image = array[b - 1, s - 1, t - 1, z - 1, c - 1, :, :]

        if sliders == 'BSTCZR':
            if metadata['isRGB']:
                image = array[b - 1, s - 1, t - 1, c - 1, z - 1, :, :, :]
            else:
                image = array[b - 1, s - 1, t - 1, c - 1, z - 1, :, :]

        if sliders == 'STZCR':
            if metadata['isRGB']:
                image = array[s - 1, t - 1, z - 1, c - 1, :, :, :]
            else:
                image = array[s - 1, t - 1, z - 1, c - 1, :, :]

        if sliders == 'STCZR':
            if metadata['isRGB']:
                image = array[s - 1, t - 1, c - 1, z - 1, :, :, :]
            else:
                image = array[s - 1, t - 1, c - 1, z - 1, :, :]

        if sliders == 'TZCR':
            if metadata['isRGB']:
                image = array[t - 1, z - 1, c - 1, :, :, :]
            else:
                image = array[t - 1, z - 1, c - 1, :, :]

        if sliders == 'TCZR':
            if metadata['isRGB']:
                image = array[t - 1, c - 1, z - 1, :, :, :]
            else:
                image = array[t - 1, c - 1, z - 1, :, :]

        if sliders == 'SCR':
            if metadata['isRGB']:
                image = array[s - 1, c - 1, :, :, :]
            else:
                image = array[s - 1, c - 1, :, :]

        if sliders == 'ZR':
            if metadata['isRGB']:
                image = array[z - 1, :, :, :]
            else:
                image = array[z - 1, :, :]

        if sliders == 'TR':
            if metadata['isRGB']:
                image = array[t - 1, :, :, :]
            else:
                image = array[t - 1, :, :]

        if sliders == 'CR':
            if metadata['isRGB']:
                image = array[c - 1, :, :, :]
            else:
                image = array[c - 1, :, :]

        if sliders == 'BSCR':
            if metadata['isRGB']:
                image = array[b - 1, s - 1, c - 1, :, :, :]
            else:
                image = array[b - 1, s - 1, c - 1, :, :]

        if sliders == 'BTCR':
            if metadata['isRGB']:
                image = array[b - 1, t - 1, c - 1, :, :, :]
            else:
                image = array[b - 1, t - 1, c - 1, :, :]

        ####### lightsheet Data #############
        if sliders == 'VIHRSCTZR':
            # reduce dimensions
            image = np.squeeze(array, axis=(0, 1, 2, 3, 4))
            image = image[c - 1, t - 1, z - 1, :, :]

    # display the labeled image
    fig, ax = plt.subplots(figsize=(8, 8))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    im = ax.imshow(image, vmin=vmin, vmax=vmax, interpolation='nearest', cmap=cm.gray)
    fig.colorbar(im, cax=cax, orientation='vertical')
    print('Min-Max (Current Plane):', image.min(), '-', image.max())


def get_dimorder(dimstring):
    """
    Get the order of dimensions from dimension string

    :param dimstring: string containing the dimensions
    :return: dims_dict - dictionary with the dimensions and its positions
    :return: dimindex_list - list with indices of dimensions
    :return: numvalid_dims - number of valid dimensions
    """

    dimindex_list = []
    dims = ['B', 'S', 'T', 'C', 'Z', 'Y', 'X', '0']
    dims_dict = {}

    for d in dims:

        dims_dict[d] = dimstring.find(d)
        dimindex_list.append(dimstring.find(d))

    numvalid_dims = sum(i > 0 for i in dimindex_list)

    return dims_dict, dimindex_list, numvalid_dims


def get_array_czi(filename,
                  replacevalue=False,
                  remove_HDim=True,
                  return_addmd=False):
    """
    Get the pixel data of the CZI file as multidimensional NumPy.Array

    :param filename: filename of the CZI file
    :param replacevalue: replace arrays entries with a specific value with Nan
    :param remove_HDim: remove the H-Dimension (Airy Scan Detectors)
    :param return_addmd: read the additional metadata
    :return: cziarray - dictionary with the dimensions and its positions
    :return: metadata - dictionary with CZI metadata
    :return: additional_metadata_czi - dictionary with additional CZI metadata
    """

    metadata = get_metadata_czi(filename)
    additional_metadata_czi = get_additional_metadata_czi(filename)

    # get CZI object and read array
    czi = zis.CziFile(filename)
    cziarray = czi.asarray()

    # check for H dimension and remove
    if remove_HDim and metadata['Axes'][0] == 'H':
        metadata['Axes'] = metadata['Axes'][1:]
        cziarray = np.squeeze(cziarray, axis=0)

    # get additional information about dimension order etc.
    dim_dict, dim_list, numvalid_dims = get_dimorder(metadata['Axes'])
    metadata['DimOrder CZI'] = dim_dict

    if cziarray.shape[-1] == 3:
        pass
    else:
        cziarray = np.squeeze(cziarray, axis=len(metadata['Axes']) - 1)

    if replacevalue:
        cziarray = replace_value(cziarray, value=0)

    # close czi file
    czi.close()

    return cziarray, metadata, additional_metadata_czi


def replace_value(data, value=0):
    """
    Replace specifc values in array with NaN

    :param data: NumPy.Array
    :param value: value inside array to be replaced with Nan
    :return: data - array with new values
    """

    data = data.astype('float')
    data[data == value] = np.nan

    return data


def get_scalefactor(metadata):
    """
    Add scaling factors to the metadata dictionary

    :param metadata: dictionary with CZI or OME-TIFF metadata
    :return: metadata - dictionary with additional keys for scling factors
    """

    # set default scale factore to 1
    scalefactors = {'xy': 1.0,
                    'zx': 1.0
                    }

    try:
        # get the factor between XY scaling
        scalefactors['xy'] = np.round(metadata['XScale'] / metadata['YScale'], 3)
        # get the scalefactor between XZ scaling
        scalefactors['zx'] = np.round(metadata['ZScale'] / metadata['YScale'], 3)
    except KeyError as e:
        print('Key not found: ', e)

    return scalefactors


def show_napari(array, metadata,
                blending='additive',
                gamma=0.85,
                verbose=True):
    """
    Show the multidimensional array using the Napari viewer

    :param array: multidimensional NumPy.Array containing the pixeldata
    :param metadata: dictionary with CZI or OME-TIFF metadata
    :param blending: NapariViewer option for blending
    :param gamma: NapariViewer value for Gamma
    :param verbose: show additional output
    """

    with napari.gui_qt():

        # create scalefcator with all ones
        scalefactors = [1.0] * len(array.shape)

        # initialize the napari viewer
        print('Initializing Napari Viewer ...')
        viewer = napari.Viewer()

        if metadata['ImageType'] == 'ometiff':

            # find position of dimensions
            posZ = metadata['DimOrder BF Array'].find('Z')
            posC = metadata['DimOrder BF Array'].find('C')
            posT = metadata['DimOrder BF Array'].find('T')

            # get the scalefactors from the metadata
            scalef = get_scalefactor(metadata)
            # modify the tuple for the scales for napari
            scalefactors[posZ] = scalef['zx']

            if verbose:
                print('Dim PosT : ', posT)
                print('Dim PosC : ', posC)
                print('Dim PosZ : ', posZ)
                print('Scale Factors : ', scalefactors)

            # add all channels as layers
            for ch in range(metadata['SizeC']):

                try:
                    # get the channel name
                    chname = metadata['Channels'][ch]
                except:
                    # or use CH1 etc. as string for the name
                    chname = 'CH' + str(ch + 1)

                # cutout channel
                channel = array.take(ch, axis=posC)
                print('Shape Channel : ', ch, channel.shape)

                # actually show the image array
                print('Scaling Factors: ', scalefactors)

                # get min-max values for initial scaling
                clim = [channel.min(), np.round(channel.max() * 0.85)]
                if verbose:
                    print('Scaling: ', clim)
                viewer.add_image(channel,
                                 name=chname,
                                 scale=scalefactors,
                                 contrast_limits=clim,
                                 blending=blending,
                                 gamma=gamma)

        if metadata['ImageType'] == 'czi':

            # find position of dimensions
            posZ = metadata['Axes'].find('Z')
            posC = metadata['Axes'].find('C')
            posT = metadata['Axes'].find('T')

            # get the scalefactors from the metadata
            scalef = get_scalefactor(metadata)
            # modify the tuple for the scales for napari
            scalefactors[posZ] = scalef['zx']

            if verbose:
                print('Dim PosT : ', posT)
                print('Dim PosZ : ', posZ)
                print('Dim PosC : ', posC)
                print('Scale Factors : ', scalefactors)

            if metadata['SizeC'] > 1:
                # add all channels as layers
                for ch in range(metadata['SizeC']):

                    try:
                        # get the channel name
                        chname = metadata['Channels'][ch]
                    except:
                        # or use CH1 etc. as string for the name
                        chname = 'CH' + str(ch + 1)

                    # cut out channel
                    channel = array.take(ch, axis=posC)
                    print('Shape Channel : ', ch, channel.shape)

                    # actually show the image array
                    print('Adding Channel: ', chname)
                    print('Scaling Factors: ', scalefactors)

                    # get min-max values for initial scaling
                    clim = [channel.min(), np.round(channel.max() * 0.85)]
                    if verbose:
                        print('Scaling: ', clim)
                    viewer.add_image(channel,
                                     name=chname,
                                     scale=scalefactors,
                                     contrast_limits=clim,
                                     blending=blending,
                                     gamma=gamma)

            if metadata['SizeC'] == 1:

                ch = 0
                # just add one channel as a layer
                try:
                        # get the channel name
                    chname = metadata['Channels'][ch]
                except:
                    # or use CH1 etc. as string for the name
                    chname = 'CH' + str(ch + 1)

                # actually show the image array
                print('Adding Channel: ', chname)
                print('Scaling Factors: ', scalefactors)

                # get min-max values for initial scaling
                clim = [array.min(), np.round(array.max() * 0.85)]
                if verbose:
                    print('Scaling: ', clim)
                viewer.add_image(array,
                                 name=chname,
                                 scale=scalefactors,
                                 contrast_limits=clim,
                                 blending=blending,
                                 gamma=gamma)


def check_for_previewimage(czi):
    """
    Check if the CZI contains an image from a prescan camera

    :param czi: CZI image object
    :return: has_attimage - Boolean if CZI image contains prescan image
    """

    att = []

    for attachment in czi.attachments():
        entry = attachment.attachment_entry
        print(entry.name)
        att.append(entry.name)

    has_attimage = False

    if 'SlidePreview' in att:
        has_attimage = True

    return has_attimage


def writexml_czi(filename, xmlsuffix='_CZI_MetaData.xml'):
    """
    Write XML imformation of CZI to disk

    :param filename: CZI image filename
    :param xmlsuffix: suffix for the XML file that will be created
    :return: xmlfile - filename of the XML file
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


def writexml_ometiff(filename, xmlsuffix='_OMETIFF_MetaData.xml'):
    """
    Write XML imformation of OME-TIFF to disk

    :param filename: OME-TIFF image filename
    :param xmlsuffix: suffix for the XML file that will be created
    :return: xmlfile - filename of the XML file
    """

    if filename.lower().endswith('.ome.tiff'):
        ext = '.ome.tiff'
    if filename.lower().endswith('.ome.tif'):
        ext = '.ome.tif'

    with tifffile.TiffFile(filename) as tif:
            #omexml_string = tif[0].image_description.decode('utf-8')
        omexml_string = tif[0].image_description

    # get tree from string
    #tree = ET.ElementTree(ET.fromstring(omexml_string.encode('utf-8')))
    tree = ET.ElementTree(ET.fromstring(omexml_string))

    # change file name
    xmlfile = filename.replace(ext, xmlsuffix)

    tree.write(xmlfile, encoding='utf-8', method='xml', pretty_print=True)
    print('Created OME-XML file for testdata: ', filename)

    return xmlfile


def getImageSeriesIDforWell(welllist, wellID):
    """
    Returns all ImageSeries (for OME-TIFF) indicies for a specific wellID

    :param welllist: list containing all wellIDs as stringe, e.g. '[B4, B4, B4, B4, B5, B5, B5, B5]'
    :param wellID: string specifying the well, eg.g. 'B4'
    :return: imageseriesindices - list containing all ImageSeries indices, which correspond the the well
    """

    imageseries_indices = [i for i, x in enumerate(welllist) if x == wellID]

    return imageseries_indices
