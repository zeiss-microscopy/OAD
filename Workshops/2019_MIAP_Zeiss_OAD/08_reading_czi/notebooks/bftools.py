# -*- coding: utf-8 -*-
"""
@author: Sebi

File: bftools.py
Date: 01.03.2019
Version. 2.4.1
"""

import javabridge as jv
import bioformats
import numpy as np
import czitools as czt
import os
import pandas as pd
from lxml import etree as etl
import sys
import re
from collections import Counter
import subprocess
import tifffile
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib.pyplot as plt


VM_STARTED = False
VM_KILLED = False

# define default path to bioformats_package.jar globally
BFPATH = r'bfpackage/5.9.2/bioformats_package.jar'

BF2NP_DTYPE = {
    0: np.int8,
    1: np.uint8,
    2: np.int16,
    3: np.uint16,
    4: np.int32,
    5: np.uint32,
    6: np.float32,
    7: np.double
}


def set_bfpath(bfpackage_path=BFPATH):
    # this function can be used to set the path to the package individually
    global BFPATH
    BFPATH = bfpackage_path

    return BFPATH


def start_jvm(max_heap_size='4G'):
    """
    Start the Java Virtual Machine, enabling BioFormats IO.
    Optional: Specify the path to the bioformats_package.jar to your needs by calling.
    set_bfpath before staring to read the image data

    Parameters
    ----------
    max_heap_size : string, optional
    The maximum memory usage by the virtual machine. Valid strings
    include '256M', '64k', and '2G'. Expect to need a lot.
    """

    # TODO - include check for the OS, so that the file paths are always working

    jars = jv.JARS + [BFPATH]
    jv.start_vm(class_path=jars, max_heap_size=max_heap_size)
    VM_STARTED = True


def kill_jvm():
    """
    Kill the JVM. Once killed, it cannot be restarted.
    See the python-javabridge documentation for more information.
    """
    jv.kill_vm()
    VM_KILLED = True


def jvm_error():

    raise RuntimeError("The Java Virtual Machine has already been "
                       "killed, and cannot be restarted. See the "
                       "python-javabridge documentation for more "
                       "information. You must restart your program "
                       "and try again.")


def get_metadata_store(imagefile):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    # get OME-XML and change the encoding to UTF-8
    omexml = get_OMEXML(imagefile)
    # get the metadata from the OME-XML
    omexmlmetadata = bioformats.OMEXML(omexml)

    return omexmlmetadata


def get_XMLStringfromMetaData(metadata):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    # get the xml string from the metadata
    xmlstring = metadata.to_xml()

    return xmlstring


def get_OMEXML(imagefile):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    # get OME-XML and change the encoding to UTF-8
    omexml = bioformats.get_omexml_metadata(imagefile)
    omexml = omexml.encode('utf-8')
    # omexml = unidecode(omexml)

    return omexml


def get_java_metadata_store(imagefile):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    # get the actual image reader
    rdr = bioformats.get_image_reader(None, path=imagefile)

    # for "whatever" reason the number of total series can only be accessed here ...
    try:
        totalseries = np.int(rdr.rdr.getSeriesCount())
    except:
        totalseries = 1  # in case there is only ONE series

    try:
        for sc in range(0, totalseries):
            rdr.rdr.setSeries(sc)
            resolutioncount = rdr.rdr.getResolutionCount()
            print('Resolution count for series #', sc, ' = ' + resolutioncount)
            for res in range(0, resolutioncount):
                rdr.rdr.setResolution(res)
                print('Resolution #', res, ' dimensions = ', rdr.getSizeX(), ' x ', rdr.getSizeY())
    except:
        print('Multi-Resolution API not enabled yet.')

    series_dimensions = []
    # cycle through all the series and check the dimensions
    for sc in range(0, totalseries):
        rdr.rdr.setSeries(sc)
        dimx = rdr.rdr.getSizeX()
        dimy = rdr.rdr.getSizeY()
        series_dimensions.append((dimx, dimy))

        if len(series_dimensions) == 1:
            multires = False
        elif len(series_dimensions) > 1:
            if len(set(series_dimensions)) > 1:
                multires = True
            elif len(set(series_dimensions)) == 1:
                multires = False

    # rdr.rdr is the actual BioFormats reader. rdr handles its lifetime
    javametadata = jv.JWrapper(rdr.rdr.getMetadataStore())
    imagecount = javametadata.getImageCount()

    imageIDs = []
    for id in range(0, imagecount):
        imageIDs.append(id)

    rdr.close()

    # kill_jvm()

    return javametadata, totalseries, imageIDs, series_dimensions, multires


def get_metainfo_dimension(jmd, MetaInfo, imageID=0):
    """
    Read the actual size for every dimension from the metadata from the 1st image series
    and convert them into numbers.
    dimension order is returned as a string.
    """

    MetaInfo['SizeC'] = np.int(jmd.getPixelsSizeC(imageID).getValue().floatValue())
    MetaInfo['SizeT'] = np.int(jmd.getPixelsSizeT(imageID).getValue().floatValue())
    MetaInfo['SizeZ'] = np.int(jmd.getPixelsSizeZ(imageID).getValue().floatValue())
    MetaInfo['SizeX'] = np.int(jmd.getPixelsSizeX(imageID).getValue().floatValue())
    MetaInfo['SizeY'] = np.int(jmd.getPixelsSizeY(imageID).getValue().floatValue())
    # get dimension order string from BioFormats library
    MetaInfo['DimOrder BF'] = jmd.getPixelsDimensionOrder(imageID).getValue()

    print('Retrieving Image Dimensions ...')
    print('T: ', MetaInfo['SizeT'], 'Z: ', MetaInfo['SizeZ'], 'C: ', MetaInfo['SizeC'], 'X: ',
          MetaInfo['SizeX'], 'Y: ', MetaInfo['SizeY'])

    return MetaInfo


def get_metainfo_scaling(jmd, imageID=0):

    # get scaling for XYZ in micron
    xscale = np.round(jmd.getPixelsPhysicalSizeX(imageID).value().floatValue(), 3)
    yscale = np.round(jmd.getPixelsPhysicalSizeY(imageID).value().floatValue(), 3)

    # check if there is only one z-plane
    SizeZ = jmd.getPixelsSizeZ(imageID).getValue().floatValue()
    if SizeZ > 1:
        zscale = np.round(jmd.getPixelsPhysicalSizeZ(imageID).value().floatValue(), 3)
    else:
        # set z spacing equal to xy, if there is only one z-plane existing
        zscale = xscale

    return xscale, yscale, zscale


def get_metainfo_detector(jmd, instrumentindex=0, detectorindex=0):

    try:
        # get the correct detector ID
        detectorID = jmd.getDetectorID(instrumentindex, detectorindex)
    except:
        print('No suitable detector ID found. Using default = 0.')
        detectorID = 0

    return detectorID


def get_metainfo_instrument(jmd, instrumentindex=0):

    try:
        # get the correctinstrument ID
        instrumentIDstr = jmd.getInstrumentID(instrumentindex)
        instrumentID = np.int(jmd.getInstrumentID(instrumentindex)[-1])
    except:
        print('No suitable instrumentID found. Using default = 0.')
        instrumentIDstr = 'na'
        instrumentID = 0

    return instrumentIDstr, instrumentID


def get_metainfo_objective(jmd, filename, imageID=0):

    try:
        # get the correct objective ID (the objective that was used to acquire the image)
        instrumentIDstr = jmd.getInstrumentID(imageID)
        instrumentID = np.int(jmd.getInstrumentID(imageID)[-1])
        objID = np.int(jmd.getObjectiveSettingsID(instrumentID)[-1])
        # error handling --> sometime only one objective is there with ID > 0
        numobj = jmd.getObjectiveCount(instrumentID)
        if numobj == 1:
            objID = 0
    except:
        print('No suitable instrument and objective ID found.')

    # try to get immersion type -  # get the first objective record in the first Instrument record
    try:
        objimm = jmd.getObjectiveImmersion(instrumentID, objID).getValue()
    except:
        objimm = 'na'

    # try to get objective Lens NA
    try:
        objna = np.round(jmd.getObjectiveLensNA(instrumentID, objID).floatValue(), 3)
    except:
        objna = 'na'

    # try to get objective magnification
    try:
        objmag = np.round(jmd.getObjectiveNominalMagnification(instrumentID, objID).floatValue(), 0)
    except:
        objmag = 'na'

    # try to get objective model
    try:
        objmodel = jmd.getObjectiveModel(instrumentID, objID)
        if objmodel is None:
            # if len(objmodel) == 0:
            objmodel = 'na'
            print('No objective model name found in metadata.')
    except:
        print('Try to read objective name via czifile.py')
        # this is a fallback option --> use cziread.py to get the information
        if filename[-4:] == '.czi':
            objmodel = czt.get_objective_name_cziread(filename)
            if objmodel is None:
                objmodel = 'na'
        else:
            objmodel = 'na'

    return objimm, objna, objmag, objmodel


def get_metainfo_pixeltype(jmd):

    pixtype = jmd.getPixelsType(0).getValue()

    return pixtype


def get_metainfo_numscenes(czishape, cziorder):
    """
    Currently the number of scenes cannot be read directly using BioFormats so
    czifile.py is used to determine the number of scenes.
    """

    # find the index of the "S" inside the dimension string
    try:
        si = cziorder.index("S")
        numscenes = czishape[si]
    except:
        # if no scene was found set to 1
        numscenes = 1

    return numscenes


def get_metainfo_wavelengths(jmd, imageID=0):

    SizeC = np.int(jmd.getPixelsSizeC(imageID).getValue().floatValue())

    # initialize arrays for excitation and emission wavelength
    wl_excitation = np.zeros(SizeC)
    wl_emission = np.zeros(SizeC)
    dyes = []
    channels = []

    for i in range(0, SizeC):

        try:
            # new from bioformats_package.jar >= 5.1.1
            wl_excitation[i] = np.round(jmd.getChannelExcitationWavelength(imageID, i).value().floatValue(), 0)
            wl_emission[i] = np.round(jmd.getChannelEmissionWavelength(imageID, i).value().floatValue(), 0)
            dyes.append(str(jmd.getChannelFluor(imageID, i)))
            channels.append(str(jmd.getChannelName(imageID, i)))
        except:
            wl_excitation[i] = 0
            wl_emission[i] = 0
            dyes.append('n.a.')
            channels.append('n.a.')

    return wl_excitation, wl_emission, dyes, channels


def get_dimension_only(imagefile, imageID=0):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.get_image_reader(None, path=imagefile)
    # read total number of image series
    totalseries = rdr.rdr.getSeriesCount()

    # get dimensions for CTZXY
    metadata = get_metadata_store(imagefile)
    pixels = metadata.image(imageID).Pixels
    SizeC = pixels.SizeC
    SizeT = pixels.SizeT
    SizeZ = pixels.SizeZ
    SizeX = pixels.SizeX
    SizeY = pixels.SizeY

    print('Series: ', totalseries)
    print('Size T: ', SizeT)
    print('Size Z: ', SizeZ)
    print('Size C: ', SizeC)
    print('Size X: ', SizeX)
    print('Size Y: ', SizeY)

    # usually the x-axis of an image is from left --> right and y from top --> bottom
    # in order to be compatible with numpy arrays XY are switched
    # for numpy arrays the 2st axis are columns (top --> down) = Y-Axis for an image

    sizes = [totalseries, SizeT, SizeZ, SizeC, SizeY, SizeX]

    rdr.close()

    return sizes


def get_planetable(imagefile, writecsv=False, separator='\t', imageID=0, showinfo=True):

    MetaInfo = create_metainfo_dict()

    # get JavaMetaDataStore and SeriesCount
    try:
        jmd, MetaInfo['TotalSeries'], MetaInfo['ImageIDs'], MetaInfo['SeriesDimensions'], MetaInfo['MultiResolution'] = get_java_metadata_store(
            imagefile)
        MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale'] = get_metainfo_scaling(jmd)
        MetaInfo['SizeC'] = np.int(jmd.getPixelsSizeC(imageID).getValue().floatValue())
        MetaInfo['SizeT'] = np.int(jmd.getPixelsSizeT(imageID).getValue().floatValue())
        MetaInfo['SizeZ'] = np.int(jmd.getPixelsSizeZ(imageID).getValue().floatValue())
        MetaInfo['SizeX'] = np.int(jmd.getPixelsSizeX(imageID).getValue().floatValue())
        MetaInfo['SizeY'] = np.int(jmd.getPixelsSizeY(imageID).getValue().floatValue())
    except:
        print('Problem retrieving Java Metadata Store or Series size:', sys.exc_info()[0])
        raise

    # get dimension information and MetaInfo
    MetaInfo = get_metainfo_dimension(jmd, MetaInfo)

    if showinfo:
        # show relevant image Meta-Information
        print('\n')
        print('-------------------------------------------------------------')
        print('MutiResolution       : ', MetaInfo['MultiResolution'])
        print('Series Dimensions    : ', MetaInfo['SeriesDimensions'])
        print('Images Dim Sizes [0] : ', MetaInfo['Sizes'])
        print('Image Dimensions     : ', MetaInfo['TotalSeries'], MetaInfo['SizeT'],
              MetaInfo['SizeZ'], MetaInfo['SizeC'], MetaInfo['SizeY'], MetaInfo['SizeX'])
        print('Scaling XYZ [micron] : ', MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale'])
        print('ImageIDs             : ', MetaInfo['ImageIDs'])
        print('\n')

    id = []
    plane = []
    xpos = []
    ypos = []
    zpos = []
    dt = []
    theC = []
    theZ = []
    theT = []

    print('Start reading the plane data ...')

    import progressbar
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=max(MetaInfo['ImageIDs']) + 1).start()
    #bar = progressbar.ProgressBar().start()

    for imageIndex in range(0, max(MetaInfo['ImageIDs']) + 1):
        for planeIndex in range(0, MetaInfo['SizeZ'] * MetaInfo['SizeC'] * MetaInfo['SizeT']):

            try:
                theC.append(jmd.getPlaneTheC(imageIndex, planeIndex).getValue().intValue())
                theZ.append(jmd.getPlaneTheZ(imageIndex, planeIndex).getValue().intValue())
                theT.append(jmd.getPlaneTheT(imageIndex, planeIndex).getValue().intValue())
                xpos.append(jmd.getPlanePositionX(imageIndex, planeIndex).value().doubleValue())
                ypos.append(jmd.getPlanePositionY(imageIndex, planeIndex).value().doubleValue())
                zpos.append(jmd.getPlanePositionZ(imageIndex, planeIndex).value().doubleValue())
                dt.append(jmd.getPlaneDeltaT(imageIndex, planeIndex).value().doubleValue())
                id.append(imageIndex)
                plane.append(planeIndex)
            except:
                print('Could not retrieve plane data for imageIndex, PlaneIndex:', imageIndex, planeIndex)

        # create some kind of progress bar
        bar.update(imageIndex)

    # round the data
    xpos = np.round(xpos, 1)
    ypos = np.round(ypos, 1)
    zpos = np.round(zpos, 1)
    dt = np.round(dt, 3)
    # normalize plane timings to 0 for the 1st acquired plane
    dt = dt - dt.min()

    # create Pandas dataframe to hold the plane data
    df = pd.DataFrame([np.asarray(id), np.asarray(plane), np.asarray(theT), np.asarray(theZ), np.asarray(theC), xpos, ypos, zpos, dt])
    df = df.transpose()
    # give the planetable columns the correct names
    df.columns = ['ImageID', 'Plane', 'TheT', 'TheZ', 'TheC', 'XPos', 'YPos', 'ZPos', 'DeltaT']

    if writecsv:
        csvfile = imagefile[:-4] + '_planetable.csv'
        # use tab as separator and do not write the index to the CSV data table
        df.to_csv(csvfile, sep=separator, index=False)
        print('\nWriting CSV file: ', csvfile)
    if not writecsv:
        csvfile = None

    return df, csvfile, MetaInfo


def get_image6d(imagefile, metainfo,
                num_levels=1,
                num_scenes=1,
                pylevel2read=0):
    
    """
    This function will read the image data and store them into a 6D numpy array.
    The 6D array has the following dimension order: [Series, T, Z, C, X, Y].
    Pyramid levels start with 0.
    """

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)
    # img6d = np.zeros(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    # img6d = np.moveaxis(np.zeros(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()]), 4, 5)

    readstate = 'OK'
    readproblems = []

    xysizes_pylevel = metainfo['SeriesDimensions'][pylevel2read]

    series_ids = calc_series_pylevel(metainfo['Sizes'][0],
                                        num_levels=num_levels,
                                        num_scenes=num_scenes,
                                        pylevel=pylevel2read)

    # adapt the sizes to reflect that only one pyramid level will be read
    new_sizes = metainfo['Sizes']
    new_sizes[0] = num_scenes
    new_sizes[4] = xysizes_pylevel[1]
    new_sizes[5] = xysizes_pylevel[0]

    img6d = np.zeros(new_sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    # main loop to read the images from the data file
    for seriesID in range(0, num_scenes):

        sid = series_ids[seriesID]

        # for seriesID in range(seriesIDsinglepylevel, seriesIDsinglepylevel + 1):
        print("Series = ", seriesID)
        for timepoint in range(0, new_sizes[1]):
            for zplane in range(0, new_sizes[2]):
                for channel in range(0, new_sizes[3]):
                    try:
                        # img6d[seriesID, timepoint, zplane, channel, :, :] = \
                        #    rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)
                        
                        img6d[seriesID, timepoint, zplane, channel, :, :] = rdr.read(series=sid,
                                                                                        c=channel,
                                                                                        z=zplane,
                                                                                        t=timepoint,
                                                                                        rescale=False)
                    except:
                        print('Problem reading data into Numpy Array for Series', seriesID, sys.exc_info()[1])
                        readstate = 'NOK'
                        readproblems = sys.exc_info()[1]

    rdr.close()

    kill_jvm()

    return img6d, readstate


def get_zstack(imagefile, sizes, seriesID, timepoints='full', tindex=0):
    """
    This will read a single Z-Stack from an image data set for a specified image series.
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    if timepoints == 'full':

        # initialize array for specific series that only contains a mutichannel z-Stack
        imgZStack = np.zeros([sizes[1], sizes[2], sizes[3], sizes[4], sizes[5]], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

        for timepoint in range(0, sizes[1]):
            for zplane in range(0, sizes[2]):
                for channel in range(0, sizes[3]):
                    imgZStack[timepoint, zplane, channel, :, :] = rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)

        dimorder_out = 'TZCXY'

    elif timepoints == 'single':

        # initialize array for specific series and time point that only contains a mutichannel z-Stack
        imgZStack = np.zeros([sizes[2], sizes[3], sizes[4], sizes[5]], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

        for zplane in range(0, sizes[2]):
            for channel in range(0, sizes[3]):
                imgZStack[zplane, channel, :, :] = rdr.read(series=seriesID, c=channel, z=zplane, t=tindex, rescale=False)

        dimorder_out = 'ZCXY'

    rdr.close()

    return imgZStack, dimorder_out


def write_ometiff(filepath, img6d,
                  scalex=0.1,
                  scaley=0.1,
                  scalez=1.0,
                  dimorder='STZCYX',
                  pixeltype='uint16',
                  swapxyaxes=True):
    """
    This function will write an OME-TIFF file to disk.
    The out 6D array has the following dimension order:

    [Series, T, Z, C, Y, X] if swapxyaxes = True

    [Series, T, Z, C, Y, X] if swapxyaxes = False
    """

    # Dimension STZCXY
    if swapxyaxes:
        # sway xy to write the OME-Stack with the correct shape
        Series = img6d.shape[0]
        SizeT = img6d.shape[1]
        SizeZ = img6d.shape[2]
        SizeC = img6d.shape[3]
        SizeX = img6d.shape[5]
        SizeY = img6d.shape[4]

    if not swapxyaxes:
        Series = img6d.shape[0]
        SizeT = img6d.shape[1]
        SizeZ = img6d.shape[2]
        SizeC = img6d.shape[3]
        SizeX = img6d.shape[4]
        SizeY = img6d.shape[5]

    # Getting metadata info
    omexml = bioformats.omexml.OMEXML()
    omexml.image(Series - 1).Name = filepath

    for series in range(Series):
        p = omexml.image(series).Pixels
        p.ID = str(series)
        p.SizeX = SizeX
        p.SizeY = SizeY
        p.SizeC = SizeC
        p.SizeT = SizeT
        p.SizeZ = SizeZ
        p.PhysicalSizeX = np.float(scalex)
        p.PhysicalSizeY = np.float(scaley)
        p.PhysicalSizeZ = np.float(scalez)
        p.PixelType = pixeltype
        p.channel_count = SizeC
        p.plane_count = SizeZ * SizeT * SizeC
        p = writeOMETIFFplanes(p, SizeT=SizeT, SizeZ=SizeZ, SizeC=SizeC, order=dimorder)

        for c in range(SizeC):
            if pixeltype == 'unit8':
                p.Channel(c).SamplesPerPixel = 1
            if pixeltype == 'unit16':
                p.Channel(c).SamplesPerPixel = 2

        omexml.structured_annotations.add_original_metadata(bioformats.omexml.OM_SAMPLES_PER_PIXEL, str(SizeC))

    # Converting to omexml
    xml = omexml.to_xml()

    # write file and save OME-XML as description
    tifffile.imwrite(filepath, img6d, metadata={'axes': dimorder}, description=xml)

    return filepath


def care_getimages(imagefile, sizes):
    """
    Still experimental. Use at your own risk !!!
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)
    img_care = np.zeros(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    readstate = 'OK'
    readproblems = []

    # main loop to read the images from the data file
    for seriesID in range(0, sizes[0]):
        for channel in range(0, sizes[3]):
            try:
                img_care[seriesID, :, :, channel] = rdr.read(series=seriesID, c=channel, z=0, t=0, rescale=False)
            except:
                print('Problem reading data into Numpy Array for Series', seriesID, sys.exc_info()[1])
                readstate = 'NOK'
                readproblems = sys.exc_info()[1]

    rdr.close()

    return img_care, readstate


def get_image6d_subset(imagefile, sizes,
                       seriesstart=0, seriesend=0,
                       tstart=0, tend=0,
                       zstart=0, zend=0,
                       chstart=0, chend=0):
    """

    Attention: Still Experimental !!!

    This function will read a subset of the image file store them into a 6D numpy array.
    The 6D array has the following dimension order: [Series, T, Z, C, X, Y].
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    subsetSizeS = seriesend - seriesstart
    subsetSizeT = tend - tstart
    subsetSizeZ = zend - zstart
    subsetSizeC = chend - chstart

    subsetsizes = [subsetSizeS, subsetSizeT, subsetSizeZ, subsetSizeC, sizes[4], sizes[5]]

    img6dsubset = np.zeros(subsetsizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    readstate = 'OK'
    readproblems = []

    # main loop to read the images from the data file
    for seriesID in range(seriesstart, seriesend):
        for timepoint in range(tstart, tend):
            for zplane in range(zstart, zend):
                for channel in range(chstart, chend):
                    try:
                        img6dsubset[seriesID, timepoint, zplane, channel, :, :] =\
                            rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)
                    except:
                        print('Problem reading data into Numpy Array for Series', seriesID, sys.exc_info()[1])
                        readstate = 'NOK'
                        readproblems = sys.exc_info()[1]

    rdr.close()

    return img6dsubset, readstate


def get_image6d_multires(imagefile, MetaInfo):
    """
    This function will read the image data series by series.
    Every series will be stored inside a tuple as a 5D numpy array.
    The 5D array has the following dimension order: [T, Z, C, X, Y].
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    readstate = 'OK'
    readproblems = []

    # initialize the empty list that will hold all the 5D image arrays
    series_list = []

    numseries = MetaInfo['Sizes'][0]
    sizeT = MetaInfo['Sizes'][1]
    sizeZ = MetaInfo['Sizes'][2]
    sizeC = MetaInfo['Sizes'][3]

    for seriesID in range(0, numseries):
        # read the XY dimension of the first series
        current_sizeX = MetaInfo['SeriesDimensions'][seriesID][0]
        current_sizeY = MetaInfo['SeriesDimensions'][seriesID][1]

        newsize = [sizeT, sizeZ, sizeC, current_sizeX, current_sizeY]

        # create the 5D numpy array
        img5d = np.zeros(newsize, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

        # main loop to read the images from the data file
        for timepoint in range(0, sizeT):
            for zplane in range(0, sizeZ):
                for channel in range(0, sizeC):
                    try:
                        img5d[timepoint, zplane, channel, :, :] =\
                            rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)
                    except:
                        print('Problem reading data into Numpy Array for Series', seriesID, sys.exc_info()[1])
                        readstate = 'NOK'
                        readproblems = sys.exc_info()[1]

        # store the 5D array inside a tuple
        series_list.append(img5d)
        # clear the array from memory
        img5d = None

    rdr.close()

    kill_jvm()

    return series_list, readstate


def get_image6d_pylevel(imagefile, MetaInfo, pylevel=0):
    """
    This function will read the image data only at a specific pyramid level.
    Every series will be stored inside a tuple as a 5D numpy array.
    The 6D array has the following dimension order: [T, Z, C, X, Y].
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    print('Reading MultiRes File.')
    readstate = 'OK'
    readproblems = []

    seriesID = pylevel
    sizeT = MetaInfo['Sizes'][1]
    sizeZ = MetaInfo['Sizes'][2]
    sizeC = MetaInfo['Sizes'][3]

    # read the XY dimension of the first series
    #current_sizeX = MetaInfo['SeriesDimensions'][seriesID][0]
    #current_sizeY = MetaInfo['SeriesDimensions'][seriesID][1]

    current_sizeX = MetaInfo['SeriesDimensions'][seriesID][1]
    current_sizeY = MetaInfo['SeriesDimensions'][seriesID][0]

    newsize = [1, sizeT, sizeZ, sizeC, current_sizeX, current_sizeY]

    # create the 6D numpy array
    img6d = np.zeros(newsize, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    # main loop to read the images from the data file
    for timepoint in range(0, sizeT):
        for zplane in range(0, sizeZ):
            for channel in range(0, sizeC):
                try:
                    img6d[seriesID, timepoint, zplane, channel, :, :] =\
                        rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)
                except:
                    print('Problem reading data into Numpy Array for Series', seriesID, sys.exc_info()[1])
                    readstate = 'NOK'
                    readproblems = sys.exc_info()[1]

    rdr.close()

    kill_jvm()

    return img6d, readstate


def get_image2d(imagefile, seriesID, channel, zplane, timepoint):
    """
    This will just read a single plane from an image data set.
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)
    img2d = rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return img2d


def get_series_from_well(imagefile, sizes, seriesseq):
    """
    Reads all scenes from a single well and stores them in a array.
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)
    sizes[0] = len(seriesseq)

    img6dwell = np.zeros(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    for seriesID in range(0, len(seriesseq)):
        for timepoint in range(0, sizes[1]):
            for zplane in range(0, sizes[2]):
                for channel in range(0, sizes[3]):
                    img6dwell[seriesID, timepoint, zplane, channel, :, :] =\
                        rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return img6dwell


def create_metainfo_dict():
    """
    A Python dictionary will be created to hold the relevant Metadata.
    """

    MetaInfo = {'Directory': '',
                'Filename': '',
                'TotalSeries': 0,
                'SizeX': 0,
                'SizeY': 0,
                'SizeZ': 0,
                'SizeC': 0,
                'SizeT': 0,
                'DimOrder BF': 'n.a.',
                'Immersion': 'n.a.',
                'NA': 0,
                'ObjMag': 0,
                'ObjModel': 'n.a.',
                'ShapeCZI': 0,
                'CZIhasPreview': None,
                'OrderCZI': 0,
                'XScale': 0,
                'YScale': 0,
                'ZScale': 0,
                'WLEx': 0,
                'WLEm': 0,
                'Detector Model': [],
                'Detector Name': [],
                'DetectorID': 'n.a.',
                'InstrumentID': None,
                'Dyes': [],
                'Channels': [],
                'ChDesc': 'n.a.',
                'Sizes': None,
                'ImageIDs': [],
                'SeriesDimensions': [],
                'MutiResolution': False,
                'PyLevels': None,
                'NumScenes': None}

    return MetaInfo


def get_relevant_metainfo_wrapper(imagefile,
                                  namespace='http://www.openmicroscopy.org/Schemas/OME/2016-01',
                                  bfpath=r'bfpackage/5.9.2/bioformats_package.jar',
                                  showinfo=False,
                                  xyorder='YX'):

    MetaInfo = create_metainfo_dict()
    omexml = get_OMEXML(imagefile)

    MetaInfo['Directory'] = os.path.dirname(imagefile)
    MetaInfo['Filename'] = os.path.basename(imagefile)

    # get JavaMetaDataStore and SeriesCount
    try:
        jmd, MetaInfo['TotalSeries'], MetaInfo['ImageIDs'], MetaInfo['SeriesDimensions'],\
            MetaInfo['MultiResolution'] = get_java_metadata_store(imagefile)
    except:
        print('Problem retrieving Java Metadata Store or Series size:', sys.exc_info()[0])
        raise

    # get dimension information and MetaInfo
    try:
        MetaInfo = get_metainfo_dimension(jmd, MetaInfo, imageID=0)
    except:
        print('Problem retrieving image dimensions:', sys.exc_info()[0])

    if imagefile[-4:] == '.czi':
        # get objective information using cziread
        print('Using czifile.py to get CZI Shape info.')
        MetaInfo['ShapeCZI'], MetaInfo['OrderCZI'], MetaInfo['CZIhasPreview'] = czt.get_shapeinfo_cziread(imagefile)
        MetaInfo['NumScenes'] = get_metainfo_numscenes(MetaInfo['ShapeCZI'], MetaInfo['OrderCZI'])

    print('Using BioFormats to get MetaInformation.')

    # use bioformats to get the objective information
    try:
        MetaInfo['Immersion'], MetaInfo['NA'], MetaInfo['ObjMag'], MetaInfo['ObjModel'] = get_metainfo_objective(jmd, imagefile, imageID=0)
    except:
        print('Problem retrieving object information:', sys.exc_info()[0])

    # get scaling information
    try:
        MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale'] = get_metainfo_scaling(jmd)
    except:
        print('Problem retrieving scaling information:', sys.exc_info()[0])

    # get wavelengths and dyes information
    try:
        MetaInfo['WLEx'], MetaInfo['WLEm'], MetaInfo['Dyes'], MetaInfo['Channels'] = get_metainfo_wavelengths(jmd)
    except:
        print('Problem retrieving wavelength information:', sys.exc_info()[0])

    # get channel description
    try:
        MetaInfo['ChDesc'] = czt.get_metainfo_channel_description(imagefile)
    except:
        print('Problem retrieving channel description:', sys.exc_info()[0])

    # summarize dimensions
    if xyorder == 'XY':
        MetaInfo['Sizes'] = [MetaInfo['TotalSeries'], MetaInfo['SizeT'], MetaInfo['SizeZ'],
                             MetaInfo['SizeC'], MetaInfo['SizeX'], MetaInfo['SizeY']]

    # this is the default
    if xyorder == 'YX':
        MetaInfo['Sizes'] = [MetaInfo['TotalSeries'], MetaInfo['SizeT'], MetaInfo['SizeZ'],
                             MetaInfo['SizeC'], MetaInfo['SizeY'], MetaInfo['SizeX']]

    # try to get detector information - 1
    try:
        MetaInfo['Detector Model'] = getinfofromOMEXML(omexml, ['Instrument', 'Detector'], namespace)[0]['Model']
    except:
        try:
            MetaInfo['Detector Model'] = czt.get_metainfo_cziread_camera(imagefile)
        except:
            print('Problem reading Detector Model.')
            MetaInfo['Detector Model'] = 'n.a.'

    try:
        MetaInfo['Detector Name'] = getinfofromOMEXML(omexml, ['Instrument', 'Detector'], namespace)[0]['ID']
    except:
        try:
            MetaInfo['Detector Name'] = czt.get_metainfo_cziread_detetcor(imagefile)
        except:
            print('Problem reading Detector Name.')
            MetaInfo['Detector Name'] = 'n.a.'

    # try to get detector information - 2
    try:
        MetaInfo['DetectorID'] = get_metainfo_detector(jmd, instrumentindex=0, detectorindex=0)
    except:
        print('Problem reading DetectorID from OME-XML.')

    if not MetaInfo['CZIhasPreview'] or MetaInfo['CZIhasPreview'] is None:
        MetaInfo['PyLevels'] = len(set(MetaInfo['SeriesDimensions']))
    if MetaInfo['CZIhasPreview']:
        # reduce the number because of the additional series due the attchment image
        MetaInfo['PyLevels'] = len(set(MetaInfo['SeriesDimensions'])) - 1
        MetaInfo['Sizes'][0] = MetaInfo['Sizes'][0] - 1
        MetaInfo['TotalSeries'] = MetaInfo['TotalSeries'] - 1 

    if showinfo:
        showtypicalmetadata(MetaInfo)

    return MetaInfo


def calc_series_range(total_series, scenes, sceneID):

    sps = total_series / scenes  # series_per_scence = sps
    series_seq = range(sceneID * sps - sps, sps * sceneID)

    return series_seq


def calc_series_range_well(wellnumber, imgperwell):
    """
    This function can be used when the number of positions or scenes
    per well is equal for every well
    The well numbers start with Zero and have nothing to do with the actual wellID, e.g. C2
    """
    seriesseq = range(wellnumber * imgperwell, wellnumber * imgperwell + imgperwell, 1)

    return seriesseq


def writeomexml(imagefile, method=1, writeczi_metadata=True):

    # creates readable xml files from image data files. Default method should be = 1.
    if method == 1:
        # method 1
        # Change File name and write XML file to same folder
        xmlfile1 = imagefile[:-4] + '_MetaData1.xml'

        try:
            # get the actual OME-XML
            omexml = get_OMEXML(imagefile)
            # create root and tree from XML string and write "pretty" to disk
            root = etl.fromstring(omexml)
            tree = etl.ElementTree(root)
            tree.write(xmlfile1, pretty_print=True, encoding='utf-8', method='xml')
            print('Created OME-XML file for testdata: ', imagefile)
        except:
            print('Creating OME-XML failed for testdata: ', imagefile)

    if method == 2:

        # method 2
        # Change File name and write XML file to same folder
        xmlfile2 = imagefile + '_MetaData2.xml'

        try:
            # get the actual OME-XML
            md = get_metadata_store(imagefile)
            omexmlstring = get_XMLStringfromMetaData(md)
            # create root and tree from XML string and write "pretty" to disk
            root = etl.fromstring(omexmlstring)
            tree = etl.ElementTree(root)
            tree.write(xmlfile2, pretty_print=True, encoding='utf-8', method='xml')
            print('Created OME-XML file for : ', imagefile)
        except:
            print('Creating OME-XML failed for : ', imagefile)

    if writeczi_metadata:

        # this writes the special CZI xml metadata to disk, when a CZI file was found.

        if imagefile[-4:] == '.czi':
            try:
                czt.writexml_czi(imagefile)
            except:
                print('Could not write special CZI metadata for: ', imagefile)


def getinfofromOMEXML(omexml, nodenames, ns='http://www.openmicroscopy.org/Schemas/OME/2015-01'):
    """
    This function can be used to read the most useful OME-MetaInformation from the respective XML.
    Check for the correct namespace. More info can be found at: http://www.openmicroscopy.org/Schemas/

    BF 5.1.10 ueses: 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
    BF >  5.2 ueses: 'http://www.openmicroscopy.org/Schemas/OME/2016-06' --> not fully supported yet

    The output is a list that can contain multiple elements.

    Usage:
    ------

    filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi
    omexml = bf.get_OMEXML(filename)
    parseXML(omexml, 'Image', 'Pixel')

    # case 1
    result = getinfofromOMEXML(omexml, ['Instrument', 'Objective'], ns='http://www.openmicroscopy.org/Schemas/OME/2015-01')
    print result

    # case 2
    result = getinfofromOMEXML(omexml, ['Instrument', 'Detector'])
    print result

    # case 3
    result = getinfofromOMEXML(omexml, ['Image', 'Pixels', 'Channel'])
    print result[0]
    print result[1]

    """

    # get the root tree
    root = etl.fromstring(omexml)

    # define the namespace in order to find the correct path later on
    NSMAP = {'mw': ns}
    # enclose namespace with {...} and check the length
    namespace = u'{%s}' % ns
    nsl = len(namespace)

    # construct the search string
    if len(nodenames) >= 1:
        search = './/mw:' + nodenames[0]
    if len(nodenames) >= 2:
        search = search + '/mw:' + nodenames[1]
    if len(nodenames) >= 3:
        search = search + '/mw:' + nodenames[2]

    # find all elements using the search string
    out = root.findall(search, namespaces=NSMAP)
    # create an empty list to store the dictionaries in
    dictlist = []
    for i in range(0, len(out)):
        # create the dictionary from key - values pairs of the element
        dict = {}
        for k in range(0, len(out[i].attrib)):
            dict[out[i].keys()[k]] = out[i].values()[k]
        # add dictionary to the list
        dictlist.append(dict)

    return dictlist


def parseXML(omexml, topchild, subchild, highdetail=False):
    """
    Parse XML with ElementTree and print the output to the console.
    topchild = specific node to search for
    subchild = specfic subchild of the topchild to search for
    """
    root = etl.fromstring(omexml)
    tree = etl.ElementTree(root)

    for child in root:
        print('*   ', child.tag, '--> ', child.attrib)
        if topchild in child.tag:
            # if child.tag == "{http://www.openmicroscopy.org/Schemas/OME/2015-01}Instrument":
            for step_child in child:
                print('**  ', step_child.tag, '-->', step_child.attrib)

                if subchild in step_child.tag and highdetail:
                    print("*** ", step_child.tag)

                    testdict = {}
                    if highdetail:
                        for step_child2 in step_child:
                            print('****', step_child2.tag, step_child2.attrib)
                            testdict[step_child2.tag] = step_child2.attrib


def getWelllNamesfromCZI(imagefile, namespace='{http://www.openmicroscopy.org/Schemas/SA/2016-06}'):
    """
    This function can be used to extract information about the well or image scence container
    a CZI image was acquired. Those information are "hidden" inside the XML meta-information.

    Attention: It works for CZI image data sets only!

    Example XML structure (shortend)
    -------------------------------------------------------------------------------------------------------------------------
    <OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2015-01" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2015-01 http://www.openmicroscopy.org/Schemas/OME/2015-01/ome.xsd">
      <Experimenter ID="Experimenter:0" UserName="M1SRH"/>
      <Image ID="Image:0" Name="B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi #1">
        <AcquisitionDate>2016-07-20T11:44:16.161</AcquisitionDate>
        <ExperimenterRef ID="Experimenter:0"/>
        <InstrumentRef ID="Instrument:0"/>
        <ObjectiveSettings ID="Objective:1" Medium="Air" RefractiveIndex="1.000293"/>
        <Pixels BigEndian="false" DimensionOrder="XYCZT" ID="Pixels:0" Interleaved="false" PhysicalSizeX="0.39999999999999997" PhysicalSizeXUnit="µm" PhysicalSizeY="0.39999999999999997" PhysicalSizeYUnit="µm" SignificantBits="8" SizeC="1" SizeT="2" SizeX="640" SizeY="640" SizeZ="1" Type="uint8">
          <Channel AcquisitionMode="WideField" EmissionWavelength="465.0" EmissionWavelengthUnit="nm" ExcitationWavelength="353.0" ExcitationWavelengthUnit="nm" ID="Channel:0:0" IlluminationType="Epifluorescence" Name="DAPI" SamplesPerPixel="1">
            <DetectorSettings Binning="1x1" Gain="0.0" ID="Detector:Internal"/>
            <FilterSetRef ID="FilterSet:1"/>
            <LightPath/>
          </Channel>
          <MetadataOnly/>
          <Plane DeltaT="0.46000003814697266" DeltaTUnit="s" ExposureTime="20.0" ExposureTimeUnit="s" PositionX="30533.145" PositionXUnit="reference frame" PositionY="16533.145" PositionYUnit="reference frame" PositionZ="111.842" PositionZUnit="reference frame" TheC="0" TheT="0" TheZ="0"/>
          <Plane DeltaT="5.456000089645386" DeltaTUnit="s" ExposureTime="20.0" ExposureTimeUnit="s" PositionX="30533.145" PositionXUnit="reference frame" PositionY="16533.145" PositionYUnit="reference frame" PositionZ="111.842" PositionZUnit="reference frame" TheC="0" TheT="1" TheZ="0"/>
        </Pixels>
      </Image>
      <StructuredAnnotations xmlns="http://www.openmicroscopy.org/Schemas/SA/2015-01">
        <XMLAnnotation ID="Annotation:2127" Namespace="openmicroscopy.org/OriginalMetadata">
          <Value>
            <OriginalMetadata>
              <Key>Information|Image|S|Scene|Shape|Name</Key>
              <Value>[B4, B4, B4, B4, B5, B5, B5, B5]</Value>
            </OriginalMetadata>
          </Value>
        </XMLAnnotation>
      </StructuredAnnotations>
    </OME>

    :param filename: input CZI image file location
    :return: string wellstring containing the information
    """

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    # Current key for wells inside the meta-information - 2016_07_21
    wellkey = 'Information|Image|S|Scene|Shape|Name'

    # Create OME-XML using BioFormats from CZI file and encode
    omexml = get_OMEXML(imagefile)
    # Get the tree and define namespace
    tree = etl.fromstring(omexml)
    # namespace = '{http://www.openmicroscopy.org/Schemas/SA/2015-01}'

    # find OriginalMetadata
    wellstring = ''
    origin_meta_datas = tree.findall(".//{}OriginalMetadata".format(namespace))
    # Iterate in founded origins
    for origin in origin_meta_datas:
        key = origin.find("{}Key".format(namespace)).text
        if key == wellkey:
            wellstring = origin.find("{}Value".format(namespace)).text
            print("Value: {}".format(wellstring))

    return wellstring


def processWellStringfromCZI(wellstring):
    """
    This function extracts the information from a CZI wellstring and process the information.
    Every scene inside a CZI file carries this information. Usually BioFormats translates scenes
    into ImageSeries.

    Input:
    --------------------------------------------------------------
    wellstring = '[B4, B4, B4, B4, B5, B5, B5, B5]'

    Output:
    ---------------------------------------------------------------
    welllist    = ['B4', 'B4', 'B4', 'B4', 'B5', 'B5', 'B5', 'B5']
    colindex    = [3, 3, 3, 3, 4, 4, 4, 4]
    rowindex    = [1, 1, 1, 1, 1, 1, 1, 1]
    welldict    = Counter({'B4': 4, 'B5': 4})
    numwells    = 8

    :param wellstring:
    :return: welllist - list containing all wellIDs as strings
    :return: colindex - column indices for well found in welllist as integers
    :return: rowindex - row indices for well found in welllist as integers
    :return: welldict - dictionary containing all found wells and there occurence
    :return: numwells, cols, rows, welldict, numwells
    """

    # labeling schemes for up-to 1536 wellplate
    # currently colIDs is not used
    colIDs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
              '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
              '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', ]

    rowIDs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']

    # remove the brackets and the white spaces
    wellOK = wellstring[1:]
    wellOK = wellOK[:-1]
    wellOK = re.sub(r'\s+', '', wellOK)
    # split the rest based on the commas
    welllist = [item for item in wellOK.split(',') if item.strip()]
    # initialize the lists
    cols = []
    rows = []
    # split strings for single well intto the character and the number
    for i in range(0, len(welllist)):
        wellid_split = re.findall('\d+|\D+', welllist[i])
        well_ch = wellid_split[0]
        well_id = wellid_split[1]
        # update the column index based on the number
        cols.append(np.int(well_id) - 1)
        # update the row index based on the character
        rows.append(rowIDs.index(well_ch))
    # count the content of the list, e.g. how many time a certain well was detected
    welldict = Counter(welllist)
    # count the number of different wells
    numdifferentwells = len(welldict.keys())

    # create

    return welllist, cols, rows, welldict, numdifferentwells


def getImageSeriesIDforWell(welllist, wellID):
    """
    Returns all ImageSeries indicies for a specific wellID

    :param welllist: list containing all wellIDs as stringe, e.g. '[B4, B4, B4, B4, B5, B5, B5, B5]'
    :param wellID: string specifying the well, eg.g. 'B4'
    :return: imageseriesindices - list containing all ImageSeries indices, which correspond the the well
    """

    imageseriesindices = [i for i, x in enumerate(welllist) if x == wellID]

    return imageseriesindices


def getPlanesAndPixelsFromCZI(imagefile):
    """
      This function can be used to extract information about the <Plane> and <Pixel> Elements in the
      inside the XML meta-information tree. Returns two lists of dictionaries, each dictionary element corresponds to one <Plane> element
      of the XML tree, with key/values of the XML tree mapped to respective key/values of the dictionary.
      Attention: works for CZI image data sets only!
      Added by Volker.Hilsenstein@embl.de
    """
    # if not VM_STARTED:
    #    start_jvm()
    # if VM_KILLED:
    #    jvm_error()

    # Create OME-XML using BioFormats from CZI file
    omexml = get_OMEXML(imagefile)

    # Get the tree and define namespace
    tree = etl.fromstring(omexml)
    # had wrong schema here SA instead of OME and was searching
    # like crazy for the bug ...
    # Maybe leave out schema completely and only search for *Plane*
    # and *Pixels*
    namespace = "{http://www.openmicroscopy.org/Schemas/OME/2015-01}"
    planes = []
    pixels = []
    # for child in root:
    #    m = re.match('.*Image.*', child.tag)
    #    if m:
    #        first_tag = m.group(0)
    for element in tree.iter():
        # print element.tag
        if "{}Plane".format(namespace) in element.tag:
            tmpdict = dict(zip(element.keys(), element.values()))
            planes.append(tmpdict)
        if "{}Pixels".format(namespace) in element.tag:
            tmpdict = dict(zip(element.keys(), element.values()))
            pixels.append(tmpdict)

    return planes, pixels


def output2file(scriptname, output_name='output.txt', targetdir=os.getcwd()):

    # log output to file
    filepath_output = os.path.join(targetdir, output_name)
    with open(filepath_output, 'w') as f:
        subprocess.check_call(['python', scriptname], stdout=f)

    f.close()
    # reset stdout to normal
    sys.stdout.close()
    sys.__stdout__

    print('Output written to : ', filepath_output)

    return filepath_output


def showtypicalmetadata(MetaInfo):

    # show relevant image Meta-Information
    print('\n')
    print('-------------------------------------------------------------')
    print('Image Directory      : ', MetaInfo['Directory'])
    print('Image Filename       : ', MetaInfo['Filename'])
    print('MutiResolution       : ', MetaInfo['MultiResolution'])
    print('Pyramid Levels       : ', MetaInfo['PyLevels'])
    print('Series Dimensions    : ', MetaInfo['SeriesDimensions'])
    print('Number of Scenes     : ', MetaInfo['NumScenes'])
    print('Dimension Sizes      : ', MetaInfo['Sizes'])
    print('Dimension Order BF   : ', MetaInfo['DimOrder BF'])
    print('Dimension Order CZI  : ', MetaInfo['OrderCZI'])
    print('Shape CZI            : ', MetaInfo['ShapeCZI'])
    print('CZI Preview Image    : ', MetaInfo['CZIhasPreview'])
    print('Total Series Number  : ', MetaInfo['TotalSeries'])
    print('Image Dimensions     : ', MetaInfo['TotalSeries'], MetaInfo['SizeT'],
          MetaInfo['SizeZ'], MetaInfo['SizeC'], MetaInfo['SizeY'], MetaInfo['SizeX'])
    print('Scaling XYZ [micron] : ', MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale'])
    print('Objective M-NA-Imm   : ', MetaInfo['ObjMag'], MetaInfo['NA'], MetaInfo['Immersion'])
    print('Objective Name       : ', MetaInfo['ObjModel'])
    print('Ex. Wavelengths [nm] : ', MetaInfo['WLEx'])
    print('Em. Wavelengths [nm] : ', MetaInfo['WLEm'])
    print('Dyes                 : ', MetaInfo['Dyes'])
    print('Detector Model       : ', MetaInfo['Detector Model'])
    print('Detector Name        : ', MetaInfo['Detector Name'])
    print('Detector ID          : ', MetaInfo['DetectorID'])
    print('Channels             : ', MetaInfo['Channels'])
    print('Channel Description  : ', MetaInfo['ChDesc'])
    print('ImageIDs             : ', MetaInfo['ImageIDs'])

    return None


def writeOMETIFFplanes(pixel, SizeT=1, SizeZ=1, SizeC=1, order='STZCXY', verbose=False):

    if order == 'STZCXY':

        pixel.DimensionOrder = bioformats.omexml.DO_XYCZT
        counter = 0
        for t in range(SizeT):
            for z in range(SizeZ):
                for c in range(SizeC):

                    if verbose:
                        print('Write PlaneTable: ', t, z, c),
                        sys.stdout.flush()

                    pixel.Plane(counter).TheT = t
                    pixel.Plane(counter).TheZ = z
                    pixel.Plane(counter).TheC = c
                    counter = counter + 1

    return pixel


def calcimageid(scene, numpylevels, pylevel=0):

    id = numpylevels * scene + pylevel

    return id


def calc_series_pylevel(num_series,
                        num_levels=1,
                        num_scenes=1,
                        pylevel=0):

    series_per_level = int(num_series / num_levels)
    print('Series per Pyramid Level : ', series_per_level)
    series_ids = []

    if num_levels == 1:
        series_ids = list(range(0, num_series))

    if num_levels > 1:
        # for p in range(0, series_per_level):
        for p in range(0, num_scenes):
            series_ids.append(p * num_levels + pylevel)

    return series_ids


def filterplanetable(planetable, ImageID=0, T=0, Z=0, CH=0):

    # TODO - Implement smart filtering without creating an itermediate table

    # filter planetable for specific imageID
    if ImageID > planetable['ImageID'].max():
        print('ImageID was invalid. Using ImageID = 0.')
        CH = 0
    pt = planetable[planetable['ImageID'] == ImageID]

    # filter planetable for specific timepoint
    if T > planetable['TheT'].max():
        print('Time Index was invalid. Using T = 0.')
        CH = 0
    pt = planetable[planetable['TheT'] == T]

    # filter resulting planetable pt for a specific z-plane
    if Z > planetable['TheZ'].max():
        print('Z-Plane Index was invalid. Using Z = 0.')
        zplane = 0
    pt = pt[pt['TheZ'] == Z]

    # filter planetable for specific channel
    if CH > planetable['TheC'].max():
        print('Channel Index was invalid. Using CH = 0.')
        CH = 0
    pt = planetable[planetable['TheC'] == CH]

    # return filtered planetable
    return pt


def scatterplot(planetable, ImageID=0, T=0, Z=0, CH=0, size=35,
                savefigure=False, figsavename='test.png', showsurface=True):
    """

    This function can be used to visualize al XYZ positions from an image file for
    the selcted channel and zplane as a scatterplot.

    :param planetable: XYZ planetable generated by bftools.get_planetable
    :param ImageID: zero-based ImageID indes (image series inside BioFormats)
    :param T: zero-based timepoint Index
    :param Z: zero-based zplane index
    :param CH: zero-based channel index
    :param size: maker size used to plot all YX positions
    :param savefigure: boolean
    :param filename: filename to save the figure as PNG
    :param showsurface: displays the surface as 3D plot
    :return: Plot and optional save figure as ...
    """

    ptf = filterplanetable(planetable, ImageID=0, T=0, Z=0, CH=0)

    # extract XYZ position for the selected channel
    xpos = ptf['XPos']
    ypos = ptf['YPos']
    zpos = ptf['ZPos']

    # normalize z-data by substracting the minimum value
    zpos_norm = zpos - zpos.min()

    #fig1 = plt.figure(figsize=(10, 6), dpi=100)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.grid(True)
    plt.axis('equal')

    # invert the Y-axis --> O,O = Top-Left
    ax1.invert_yaxis()

    ax1.autoscale(enable=True, axis='x', tight=True)
    ax1.autoscale(enable=True, axis='y', tight=True)

    # define the labels
    ax1.set_title('XYZ-Positions (norm) : ' + 'ImageID=' + str(ImageID) + ' T=' + str(T) + ' Z=' + str(Z) + ' CH=' + str(CH))
    ax1.set_xlabel('Stage X-Axis [micron]')
    ax1.set_ylabel('Stage Y-Axis [micron]')

    # plot data and label the colorbar
    sc1 = plt.scatter(xpos, ypos, marker='s', c=zpos_norm, s=size, cmap=cm.coolwarm)
    cb1 = plt.colorbar(sc1, fraction=0.046, shrink=0.8, pad=0.04)
    cb1.set_label('Z-Offset [micron]', labelpad=20)

    # optional save figure as PNG
    if savefigure:
        fig1.savefig(figsavename, dpi=100)
        print('Saved: ', figsavename)

    # optional 3D plot of surface
    if showsurface:

        fig2 = plt.figure(figsize=(10, 6), dpi=100)
        ax2 = fig2.add_subplot(111, projection='3d')

        # invert the Y-axis --> O,O = Top-Left
        ax2.invert_yaxis()

        ax1.autoscale(enable=True, axis='x', tight=True)
        ax1.autoscale(enable=True, axis='y', tight=True)
        ax1.autoscale(enable=True, axis='z', tight=True)

        # define the labels
        ax2.set_xlabel('Stage X-Axis [micron]')
        ax2.set_ylabel('Stage Y-Axis [micron]')
        ax2.set_zlabel('Z-Offset [micron]')

        # plot data and label the colorbar
        #sc2 = ax2.plot(xpos, ypos, zpos_norm, '.', markersize=10, cmap=plt.cm.coolwarm)
        sc2 = ax2.scatter(xpos, ypos, zpos_norm, marker='.', s=200, c=zpos_norm, cmap=plt.cm.coolwarm, depthshade=False)
        cb2 = plt.colorbar(sc2, shrink=0.8)
        cb2.set_label('Z-Offset [micron]', labelpad=20)

    if not showsurface:
        fig2 = None

    return fig1, fig2
