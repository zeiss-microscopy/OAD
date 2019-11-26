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
import xml.etree.ElementTree as ET
import napari


def create_metadata_dict():
    """
    A Python dictionary will be created to hold the relevant metadata.
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
                'ImageIDs': []
                }

    return metadata


def get_metadata_ometiff(filename, omemd, series=0):

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
    metadata['InstrumentID'] = omemd.instrument(series).get_ID()
    metadata['DetectorModel'] = omemd.instrument(series).Detector.get_Model()
    metadata['DetectorID'] = omemd.instrument(series).Detector.get_ID()
    metadata['DetectorModel'] = omemd.instrument(series).Detector.get_Type()
    metadata['ObjNA'] = omemd.instrument(series).Objective.get_LensNA()
    metadata['ObjID'] = omemd.instrument(series).Objective.get_ID()
    metadata['ObjMag'] = omemd.instrument(series).Objective.get_NominalMagnification()

    # get channel names
    for c in range(metadata['SizeC']):
        metadata['Channels'].append(omemd.image(series).Pixels.Channel(c).Name)

    return metadata


def get_imgtype(imagefile):

    imgtype = None

    if imagefile.lower().endswith('.ome.tiff') or imagefile.lower().endswith('.ome.tif'):
        # it is on OME-TIFF basd on the file extension ... :-)
        imgtype = 'ometiff'

    if imagefile.lower().endswith('.czi'):
        # it is on CZI basd on the file extension ... :-)
        imgtype = 'czi'

    return imgtype


def get_metadata(imagefile, series=0):

    imgtype = get_imgtype(imagefile)
    print('Image Type: ', imgtype)
    md = None

    if imgtype == 'ometiff':
        
        with tifffile.TiffFile(imagefile) as tif:
            omexml = tif[0].image_description.decode('utf-8')

        print('Getting OME-TIFF Metadata ...')
        omemd = omexmlClass.OMEXML(omexml)
        md = get_metadata_ometiff(imagefile, omemd, series=series)

    if imgtype == 'czi':

        print('Getting CZI Metadata ...')
        md = get_metadata_czi(imagefile, dim2none=False)

    return md


def create_ipyviewer_ome_tiff(array, metadata):

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

        if sliders == 'BSCR':
            if metadata['isRGB']:
                image = array[b -1, s - 1, c - 1, :, :, :]
            else:
                image = array[b -1, s - 1, c - 1, :, :]

        if sliders == 'BTCR':
            if metadata['isRGB']:
                image = array[b - 1, t - 1, c-1, :, :, :]
            else:
                image = array[b - 1, t - 1, c-1, :, :]

        ####### lightsheet Data #############
        if sliders == 'VIHRSCTZR':
            # reduce dimensions
            image = np.squeeze(array, axis=(0, 1, 2, 3, 4))
            image = image[c - 1, t - 1, z - 1, :, :]


    # display the labelled image
    fig, ax = plt.subplots(figsize=(8, 8))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    im = ax.imshow(image, vmin=vmin, vmax=vmax, interpolation='nearest', cmap=cm.gray)
    fig.colorbar(im, cax=cax, orientation='vertical')
    print('Min-Max (Current Plane):', image.min(), '-', image.max())


def get_metadata_czi(filename, dim2none=False):
    """
    # map dimension character to description for CZI files
    DIMENSIONS = {
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
    }
    """

    # get CZI object and read array
    czi = zis.CziFile(filename)
    mdczi = czi.metadata()

    # parse the XML into a dictionary
    metadatadict_czi = xmltodict.parse(mdczi)
    metadata = create_metadata_dict()

    # get directory and filename etc.
    metadata['Directory'] = os.path.dirname(filename)
    metadata['Filename'] = os.path.basename(filename)
    metadata['Extension'] = 'czi'
    metadata['ImageType'] = 'czi'

    # add axes and shape information
    metadata['Axes'] = czi.axes
    metadata['Shape'] = czi.shape

    # check if the CZI image is an RGB image depending on the last dimension entry of axes
    if czi.axes[-1] == 3:
        metadata['isRGB'] = True

    """
    metadata['Experiment'] = metadatadict_czi['ImageDocument']['Metadata']['Experiment']

    try:
        metadata['Experiment'] = metadatadict_czi['ImageDocument']['Metadata']['Experiment']
    except:
        metadata['Experiment'] = None

    try:
        metadata['HardwareSetting'] = metadatadict_czi['ImageDocument']['Metadata']['HardwareSetting']
    except:
        metadata['HardwareSetting'] = None

    try:
        metadata['CustomAttributes'] = metadatadict_czi['ImageDocument']['Metadata']['CustomAttributes']
    except:
        metadata['CustomAttributes'] = None
    """

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

    """
    try:
        metadata['DisplaySetting'] = metadatadict_czi['ImageDocument']['Metadata']['DisplaySetting']
    except KeyError as e:
        print('Key not found:', e)
        metadata['DisplaySetting'] = None

    try:
        metadata['Layers'] = metadatadict_czi['ImageDocument']['Metadata']['Layers']
    except KeyError as e:
        print('Key not found:', e)
        metadata['Layers'] = None
    """

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

    del metadata['Information']
    del metadata['Scaling']

    # close CZI file
    czi.close()

    return metadata


def get_dimorder(dimstring):

    dimindex_list = []
    dims = ['B', 'S', 'T', 'C', 'Z', 'Y', 'X', '0']
    dims_dict = {}

    for d in dims:

        dims_dict[d] = dimstring.find(d)
        dimindex_list.append(dimstring.find(d))

    numvalid_dims = sum(i > 0 for i in dimindex_list)

    return dims_dict, dimindex_list, numvalid_dims


def get_array_czi(filename,
                  replacezero=False,
                  remove_HDim=True):

    metadata = get_metadata_czi(filename)

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

    if replacezero:
        cziarray = replaceZeroNaN(cziarray, value=0)

    czi.close()

    return cziarray, metadata


def replaceZeroNaN(data, value=0):

    data = data.astype('float')
    data[data == value] = np.nan

    return data


def get_scalefactor(metadata):

    scalefactors = {'xy': 1.0,
                    'zx': 1.0
                    }

    try:
        # get the factor between XY scaling
        scalefactors['xy'] = np.round(metadata['XScale']/metadata['YScale'], 3)
        # get the scalefactor between XZ scaling
        scalefactors['zx'] = np.round(metadata['ZScale']/metadata['YScale'], 3)
    except KeyError as e:
        print('Key not found: ', e)

    return scalefactors


def show_napari(array, metadata, verbose=True):

    import napari

    with napari.gui_qt():

        # create scalefcator with all ones
        scalefactors = [1] * len(array.shape)

        # initialize the napari viewer
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
                viewer.add_image(channel, name=chname, scale=scalefactors)
            
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
                print('Scaling Factors: ',  scalefactors)

                viewer.add_image(channel, name=chname, scale=scalefactors)
            

def getWellInfofromCZI(wellstring):

    # labeling schemes for plates up-to 1536 wellplate
    colIDs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
              '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
              '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', ]

    rowIDs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']

    wellOK = wellstring[1:]
    wellOK = wellOK[:-1]
    wellOK = re.sub(r'\s+', '', wellOK)
    welllist = [item for item in wellOK.split(',') if item.strip()]

    cols = []
    rows = []

    for i in range(0, len(welllist)):
        wellid_split = re.findall('\d+|\D+', welllist[i])
        well_ch = wellid_split[0]
        well_id = wellid_split[1]
        cols.append(np.int(well_id) - 1)
        well_id_index = rowIDs.index(well_ch)
        rows.append(well_id_index)

    welldict = Counter(welllist)

    numwells = len(welllist)

    return welllist, cols, rows, welldict, numwells


def getXMLnodes(filename_czi, searchpath, showoutput=False):

    czi = zis.CziFile(filename_czi)
    tree = czi.metadata.getroottree()

    tag = []
    attribute = []
    text = []

    if showoutput:
        print('Path      : ', searchpath)

    for elem in tree.iterfind(searchpath):

        tag.append(elem.tag)
        attribute.append(elem.attrib)
        text.append(elem.text)

        if showoutput:
            print('Tag       : ', elem.tag)
            print('Attribute : ', elem.attrib)
            print('Text      : ', elem.text)

    if showoutput:
        print('-----------------------------------------------------------------------------------------------')

    return tag, attribute, text


def check_for_previewimage(czi):

    att = []

    for attachment in czi.attachments():
        entry = attachment.attachment_entry
        print(entry.name)
        att.append(entry.name)

    has_attimage = False

    if 'SlidePreview' in att:
        has_attimage = True

    return has_attimage
    
    
def get_numscenes(filename):
    """
    Currently the number of scenes cannot be read directly using BioFormats so
    czifile.py is used to determine the number of scenes.
    """

    # Read the dimensions of the image stack and their order
    czi = zis.CziFile(filename)

    # find the index of the "S" inside the dimension string
    try:
        si = czi.axes.index("S")
        numscenes = czi.shape[si]
    except:
        # if no scene was found set to 1
        numscenes = 1

    czi.close()

    return numscenes
    
    
def writexml_czi(filename, xmlsuffix='_CZI_MetaData.xml'):

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












