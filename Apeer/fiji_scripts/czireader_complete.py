# @File(label = "Image File", persist=True) FILENAME
# @Boolean(label = "Stitch Tiles", value=True, persist=True) STITCHTILES
# @Integer(label = "Read Pyramid Level (1 - ...)", value=1, persist=True) READPYLEVEL
# @Boolean(label = "Concatenate Series", value=True, persist=True) SETCONCAT
# @Boolean(label = "Open All Series", value=True, persist=True) OPENALLSERIES
# @Boolean(label = "Show OME-XML data", value=False, persist=True) SHOWOMEXML
# @Boolean(label = "Show Preview Image attachment", value=False, persist=True) ATTACH
# @Boolean(label = "Autoscale", value=True, persist=True) AUTOSCALE
# @OUTPUT String FILENAME
# @OUTPUT Boolean STITCHTILES
# @OUTPUT Integer READPYLEVEL
# @OUTPUT Boolean SETCONCAT
# @OUTPUT Boolean OPENALLSERIES
# @OUTPUT Boolean SHOWOMEXML
# @OUTPUT Boolean ATTACH
# @OUTPUT Boolean AUTOSCALE

# @UIService uiService
# @LogService log

import os
from loci.formats import MetadataTools
from loci.formats import ImageReader
from loci.plugins.in import ImporterOptions
from loci.plugins.util import LociPrefs
from loci.plugins import BF
from loci.formats.in import ZeissCZIReader
from loci.formats.in import DynamicMetadataOptions
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.measure import Calibration

# clear the console automatically when not in headless mode
uiService.getDefaultUI().getConsolePane().clear()


class MiscTools:

    @staticmethod
    def getextension(splitresult):

        if len(splitresult) == 2:
            # only one extension part, eg *.czi detetected
            extension = str(splitresult[-1])
        if len(splitresult) >= 3:
            # two extension part, eg *.ome.tiff detetected
            # extension = str(splitresult[1] + splitresult[2])

            ext2 = splitresult[-2]
            if ext2 != ('.ome' or '.OME'):
                # set ext2 empty in case it is not .ome or .OME
                ext2 = ''

            extension = str(ext2 + splitresult[-1])

        return extension

    @staticmethod
    def splitext_recurse(filepath):
        base, ext = os.path.splitext(filepath)
        if ext == '':
            return (base,)
        else:
            return MiscTools.splitext_recurse(base) + (ext,)

    @staticmethod
    def setproperties(imp,
                      scaleX=1.0,
                      scaleY=1.0,
                      scaleZ=1.0,
                      unit="micron",
                      sizeC=1,
                      sizeZ=1,
                      sizeT=1):

        # check if scaleZ has a valid value to call modify the properties
        if scaleZ is None:
            scaleZ = 1

        # run the image properties tool
        IJ.run(imp, "Properties...", "channels=" + str(sizeC) +
               " slices=" + str(sizeZ)
               + " frames=" + str(sizeT)
               + " unit=" + unit
               + " pixel_width=" + str(scaleX)
               + " pixel_height=" + str(scaleY)
               + " voxel_depth=" + str(scaleZ))

        return imp

    @staticmethod
    def setscale(imp,
                 scaleX=1.0,
                 scaleY=1.0,
                 scaleZ=1.0,
                 unit="micron"):

        # check if scaleZ has a valid value to call modify the scaling
        if scaleZ is None:
            scaleZ = 1.0

        # create new Calibration object
        newCal = Calibration()

        # set the new paramters
        newCal.pixelWidth = scaleX
        newCal.pixelHeight = scaleY
        newCal.pixelDepth = scaleZ

        # set the correct unit fro the scaling
        newCal.setXUnit(unit)
        newCal.setYUnit(unit)
        newCal.setZUnit(unit)

        # apply the new calibratiion
        imp.setCalibration(newCal)

        return imp


def readczi(imagefile,
            stitchtiles=True,
            setflatres=False,
            readpylevel=0,
            setconcat=True,
            openallseries=True,
            showomexml=False,
            attach=False,
            autoscale=True):

    log.info('Filename : ' + imagefile)

    metainfo = {}
    # checking for thr file Extension
    metainfo['Extension'] = MiscTools.getextension(MiscTools.splitext_recurse(imagefile))
    log.info('Detected File Extension : ' + metainfo['Extension'])

    # initialite the reader and get the OME metadata
    reader = ImageReader()
    omeMeta = MetadataTools.createOMEXMLMetadata()
    #metainfo['ImageCount_OME'] = omeMeta.getImageCount()
    reader.setMetadataStore(omeMeta)
    reader.setId(imagefile)
    metainfo['SeriesCount_BF'] = reader.getSeriesCount()
    reader.close()

    # get the scaling for XYZ
    physSizeX = omeMeta.getPixelsPhysicalSizeX(0)
    physSizeY = omeMeta.getPixelsPhysicalSizeY(0)
    physSizeZ = omeMeta.getPixelsPhysicalSizeZ(0)

    if physSizeX is not None:
        metainfo['ScaleX'] = round(physSizeX.value(), 3)
        metainfo['ScaleY'] = round(physSizeX.value(), 3)

    if physSizeX is None:
        metainfo['ScaleX'] = None
        metainfo['ScaleY'] = None

    if physSizeZ is not None:
        metainfo['ScaleZ'] = round(physSizeZ.value(), 3)
    if physSizeZ is None:
        metainfo['ScaleZ'] = None

    options = DynamicMetadataOptions()
    options.setBoolean("zeissczi.autostitch", stitchtiles)
    options.setBoolean("zeissczi.attachments", attach)

    czireader = ZeissCZIReader()
    czireader.setFlattenedResolutions(setflatres)
    czireader.setMetadataOptions(options)
    czireader.setId(imagefile)

    # Set the preferences in the ImageJ plugin
    # Note although these preferences are applied, they are not refreshed in the UI
    Prefs.set("bioformats.zeissczi.allow.autostitch", str(stitchtiles).lower())
    Prefs.set("bioformats.zeissczi.include.attachments", str(attach).lower())

    # metainfo = {}
    metainfo['rescount'] = czireader.getResolutionCount()
    metainfo['SeriesCount_CZI'] = czireader.getSeriesCount()
    #metainfo['flatres'] = czireader.hasFlattenedResolutions()
    #metainfo['getreslevel'] = czireader.getResolution()

    # Dimensions
    metainfo['SizeT'] = czireader.getSizeT()
    metainfo['SizeZ'] = czireader.getSizeZ()
    metainfo['SizeC'] = czireader.getSizeC()
    metainfo['SizeX'] = czireader.getSizeX()
    metainfo['SizeY'] = czireader.getSizeY()

    # check for autostitching and possibility to read attchmenst
    metainfo['AllowAutoStitching'] = czireader.allowAutostitching()
    metainfo['CanReadAttachments'] = czireader.canReadAttachments()

    # read in and display ImagePlus(es) with arguments
    options = ImporterOptions()
    options.setOpenAllSeries(openallseries)
    options.setShowOMEXML(showomexml)
    options.setConcatenate(setconcat)
    options.setAutoscale(autoscale)
    options.setId(imagefile)

    # open the ImgPlus
    imps = BF.openImagePlus(options)
    metainfo['Pyramid Level Output'] = readpylevel + 1

    try:
        imp = imps[readpylevel]
        pylevelout = metainfo['SeriesCount_CZI']
    except:
        # fallback option
        log.info('PyLevel=' + str(readpylevel) + ' does not exist.')
        log.info('Using Pyramid Level = 0 as fallback.')
        imp = imps[0]
        pylevelout = 0
        metainfo['Pyramid Level Output'] = pylevelout
        
    # get the stack and some info
    imgstack = imp.getImageStack()
    metainfo['Output Slices'] = imgstack.getSize()
    metainfo['Output SizeX'] = imgstack.getWidth()
    metainfo['Output SizeY'] = imgstack.getHeight()

    # calc scaling in case of pyramid
    scale = float(metainfo['SizeX']) / float(metainfo['Output SizeX'])
    metainfo['Pyramid Scale Factor'] = scale
    metainfo['ScaleX Output'] = metainfo['ScaleX'] * scale
    metainfo['ScaleY Output'] = metainfo['ScaleY'] * scale

    # set the correct scaling
    imp = MiscTools.setscale(imp, scaleX=metainfo['ScaleX Output'],
                             scaleY=metainfo['ScaleX Output'],
                             scaleZ=metainfo['ScaleZ'],
                             unit="micron")

    # close czireader
    czireader.close()

    return imp, metainfo

#################################################################################


"""
# stitch togehter tiles
stitchtiles = True

# when set to True the number of pyramid levels can be read
setflatres = True

# select the desired pyramid level - level=0 for full resolution
readpylevel = 0
setconcat = True
openallseries = True
showomexml = False
attach = False
autoscale = True
"""

# get the FILENAME as string
imagefile = FILENAME.toString()
SETFLATRES=False

# check for meaningful pyramid level
if READPYLEVEL == 0:
	log.info('PyLevel = 0 is not valid. Use 1')
	READPYLEVEL = 1

# read the CZI image
imp, info = readczi(imagefile,
                    stitchtiles=STITCHTILES,
                    setflatres=SETFLATRES,
                    readpylevel=READPYLEVEL-1,
                    setconcat=SETCONCAT,
                    openallseries=OPENALLSERIES,
                    showomexml=SHOWOMEXML,
                    attach=ATTACH,
                    autoscale=AUTOSCALE)

# show the image
imp.show()

# show the metadata
for k, v in info.items():
    log.info(str(k) + ' : ' + str(v))
