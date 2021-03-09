# @File(label = "Image File", persist=True) FILENAME
# @String(label = "Select Filter", choices={"NONE", "MEDIAN", "MIN", "MAX", "MEAN", "VARIANCE", "OPEN", "DESPECKLE"}, style="listBox", value="MEDIAN", persist=True) FILTERTYPE
# @Integer(label = "Filter Radius", value=5.0, persist=False) FILTER_RADIUS
# @Boolean(label = "Run in headless mode", value=False, persist=False) HEADLESS
# @OUTPUT String FILENAME
# @OUTPUT String FILTERTYPE
# @OUTPUT Integer FILTER_RADIUS
# @OUTPUT Boolean HEADLESS

#@UIService uiService
#@LogService log

#################################################################
# File        : my_fijipyscript_local.py
# Version     : 0.0.8
# Author      : czsrh
# Date        : 20.02.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# The idea of this module is to provide a template showing some of the required
# code parts in order to create modules based on Fiji. The chosen processing step
# is just an example for your image analysis pipeline
#
# ATTENTION: Use at your own risk.
#
# Copyright(c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# required imports
import os
import json
import time
import sys
from collections import OrderedDict
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
from org.scijava.log import LogLevel
from loci.plugins.util import LociPrefs
from loci.plugins.out import Exporter
from loci.plugins import LociExporter
from loci.formats import ImageReader
from loci.formats import MetadataTools
from loci.formats.in import ZeissCZIReader
from loci.formats.in import DynamicMetadataOptions
from ome.units import UNITS


######### HELPER FUNCTIONS ##############

# helper function to apply the filter
def apply_filter(imp,
                 radius=5,
                 filtertype='MEDIAN'):

    # initialize filter
    filter = RankFilters()

    # create filter dictionary
    filterdict = {}
    filterdict['MEAN'] = RankFilters.MEAN
    filterdict['MIN'] = RankFilters.MIN
    filterdict['MAX'] = RankFilters.MAX
    filterdict['MEDIAN'] = RankFilters.MEDIAN
    filterdict['VARIANCE'] = RankFilters.VARIANCE
    filterdict['OPEN'] = RankFilters.OPEN
    filterdict['DESPECKLE'] = RankFilters.DESPECKLE

    # get the stack and number of slices
    stack = imp.getStack()  # get the stack within the ImagePlus
    nslices = stack.getSize()  # get the number of slices

    # apply filter based on filtertype
    if filtertype in filterdict:
        for index in range(1, nslices + 1):
            ip = stack.getProcessor(index)
            filter.rank(ip, radius, filterdict[filtertype])
    else:
        print("Argument 'filtertype': {filtertype} not found")

    return imp


def get_metadata(imagefile, imageID=0):

    metainfo = {}

    # initialize the reader and get the OME metadata
    reader = ImageReader()
    omeMeta = MetadataTools.createOMEXMLMetadata()
    metainfo['ImageCount_OME'] = omeMeta.getImageCount()
    reader.setMetadataStore(omeMeta)
    reader.setId(imagefile)
    metainfo['SeriesCount_BF'] = reader.getSeriesCount()
    reader.close()

    # read dimensions TZCXY from OME metadata
    metainfo['SizeT'] = omeMeta.getPixelsSizeT(imageID).getValue()
    metainfo['SizeZ'] = omeMeta.getPixelsSizeZ(imageID).getValue()
    metainfo['SizeC'] = omeMeta.getPixelsSizeC(imageID).getValue()
    metainfo['SizeX'] = omeMeta.getPixelsSizeX(imageID).getValue()
    metainfo['SizeY'] = omeMeta.getPixelsSizeY(imageID).getValue()

    # store info about stack
    if metainfo['SizeZ'] == 1:
        metainfo['is3d'] = False
    elif metainfo['SizeZ'] > 1:
        metainfo['is3d'] = True

    # get the scaling for XYZ
    physSizeX = omeMeta.getPixelsPhysicalSizeX(0)
    physSizeY = omeMeta.getPixelsPhysicalSizeY(0)
    physSizeZ = omeMeta.getPixelsPhysicalSizeZ(0)

    if physSizeX is not None:
        metainfo['ScaleX'] = round(physSizeX.value(), 3)
        metainfo['ScaleY'] = round(physSizeY.value(), 3)
    if physSizeX is None:
        metainfo['ScaleX'] = None
        metainfo['ScaleY'] = None

    if physSizeZ is not None:
        metainfo['ScaleZ'] = round(physSizeZ.value(), 3)
    if physSizeZ is None:
        metainfo['ScaleZ'] = None

    # sort the dictionary
    metainfo =  OrderedDict(sorted(metainfo.items()))

    return metainfo

############################################################################

if not HEADLESS:
    # clear the console automatically when not in headless mode
    uiService.getDefaultUI().getConsolePane().clear()


def run(imagefile, useBF=True,
                   series=0,
                   filtertype='MEDIAN',
                   filterradius='5'):

    log.log(LogLevel.INFO, 'Image Filename : ' + imagefile)

    # get basic image metainfo
    metainfo = get_metadata(imagefile, imageID=series)
    for k, v in metainfo.items():
        log.log(LogLevel.INFO, str(k) + ' : ' + str(v))

    if not useBF:
        # using IJ static method
        imp = IJ.openImage(imagefile)

    if useBF:

        # initialize the importer options
        options = ImporterOptions()
        options.setOpenAllSeries(True)
        options.setShowOMEXML(False)
        options.setConcatenate(True)
        options.setAutoscale(True)
        options.setId(imagefile)
        options.setStitchTiles(True)

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if filtertype != 'NONE':

        # apply filter
        log.log(LogLevel.INFO, 'Apply Filter  : ' + filtertype)
        log.log(LogLevel.INFO, 'Filter Radius : ' + str(filterradius))

        # apply the filter based on the chosen type
        imp = apply_filter(imp,
                           radius=filterradius,
                           filtertype=filtertype)

    if filtertype == 'NONE':
        log.log(LogLevel.INFO, 'No filter selected. Do nothing.')

    return imp


#########################################################################

# the the filename
IMAGEPATH = FILENAME.toString()

# suffix for the filename of the saved data
SUFFIX_FL = '_FILTERED'
SAVEFORMAT = 'ome.tiff'

# log some outputs
log.log(LogLevel.INFO, 'Starting ...')
log.log(LogLevel.INFO, 'Filename               : ' + IMAGEPATH)
log.log(LogLevel.INFO, 'Save Format used       : ' + SAVEFORMAT)
log.log(LogLevel.INFO, '------------  START IMAGE ANALYSIS ------------')

##############################################################

# define path for the output
outputimagepath = '/output/' + os.path.basename(IMAGEPATH)
basename = os.path.splitext(outputimagepath)[0]

# remove the extra .ome before reassembling the filename
if basename[-4:] == '.ome':
    basename = basename[:-4]
    log.log(LogLevel.INFO, 'New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT

#############   RUN MAIN IMAGE ANALYSIS PIPELINE ##########

# get the starting time of processing pipeline
start = time.clock()

# run image analysis pipeline
filtered_image = run(IMAGEPATH,
                     useBF=True,
                     series=0,
                     filtertype=FILTERTYPE,
                     filterradius=FILTER_RADIUS)

# get time at the end and calc duration of processing
end = time.clock()
log.log(LogLevel.INFO, 'Duration of whole Processing : ' + str(end - start))

###########################################################

start = time.clock()

# create the argument string for the BioFormats Exporter and save as OME.TIFF
paramstring = "outfile=" + outputimagepath + " " + "windowless=true compression=Uncompressed saveROI=false"
plugin = LociExporter()
plugin.arg = paramstring
exporter = Exporter(plugin, filtered_image)
exporter.run()

# get time at the end and calc duration of processing
end = time.clock()
log.log(LogLevel.INFO, 'Duration of saving as OME-TIFF : ' + str(end - start))

# show the image
filtered_image.show()

# finish
log.log(LogLevel.INFO, 'Done.')
