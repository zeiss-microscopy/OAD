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

# required imports
import os
import json
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
import time

# helper function to apply the filetr
def getImageStack(imp):

    # get the stacks
    try:
        stack = imp.getStack()  # get the stack within the ImagePlus
        nslices = stack.getSize()  # get the number of slices
    except:
        stack = imp.getProcessor()
        nslices = 1

    return stack, nslices


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
    stack, nslices = getImageStack(imp)

    for index in range(1, nslices + 1):
        # get the image processor
        ip = stack.getProcessor(index)
        # apply filter based on filtertype
        filter.rank(ip, radius, filterdict[filtertype])

    return imp

############################################################################

if not HEADLESS:
    # clear the console automatically when not in headless mode
    uiService.getDefaultUI().getConsolePane().clear()


def run(imagefile, useBF=True, series=0):

    log.info('Image Filename : ' + imagefile)

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

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if FILTERTYPE != 'NONE':

        # apply filter
        log.info('Apply Filter  : ' + FILTERTYPE)
        log.info('Filter Radius : ' + str(FILTER_RADIUS))

        # apply the filter based on the choosen type
        imp = apply_filter(imp,
                           radius=FILTER_RADIUS,
                           filtertype=FILTERTYPE)

    if FILTERTYPE == 'NONE':
        log.info('No filter selected. Do nothing.')

    return imp


#########################################################################

# the the filename
IMAGEPATH = FILENAME.toString()

# suffix for the filename of the saved data
SUFFIX_FL = '_FILTERED'
SAVEFORMAT = 'ome.tiff'

log.info('Starting ...')
log.info('Filename               : ' + IMAGEPATH)
log.info('Save Format used       : ' + SAVEFORMAT)
log.info('------------  START IMAGE ANALYSIS ------------')

##############################################################

# define path for the output
outputimagepath = '/output/' + os.path.basename(IMAGEPATH)
basename = os.path.splitext(outputimagepath)[0]

# remove the extra .ome before reassembling the filename
if basename[-4:] == '.ome':
    basename = basename[:-4]
    log.info('New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT

#############   RUN MAIN IMAGE ANALYSIS PIPELINE ##########

# get the starting time of processing pipeline
start = time.clock()

# run image analysis pipeline
filtered_image = run(IMAGEPATH,
                     useBF=True,
                     series=0)

# get time at the end and calc duration of processing
end = time.clock()
log.info('Duration of whole Processing : ' + str(end - start))

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
log.info('Duration of saving as OME-TIFF : ' + str(end - start))

# show the image
filtered_image.show()

# finish
log.info('Done.')
