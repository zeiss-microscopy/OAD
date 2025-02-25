#################################################################
# File        : fijipytools.py
# Version     : 1.8.3
# Author      : czsrh
# Date        : 16.09.2022
# Institution : Carl Zeiss Microscopy GmbH
#
# ATTENTION: Use at your own risk.
#
# Copyright(c) 2022 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


import os
import json
import time
import sys
import shutil
from collections import OrderedDict
from java.lang import Double, Integer
from java.awt import GraphicsEnvironment
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, ImageConverter
from ij.process import StackStatistics
from ij.process import AutoThresholder
from ij.plugin import Thresholder, Duplicator
from ij.plugin.filter import GaussianBlur, RankFilters
from ij.plugin.filter import BackgroundSubtracter, Binary
from ij.plugin.filter import ParticleAnalyzer as PA
from ij.plugin.filter import EDM
from ij.plugin import Filters3D
from ij.plugin.frame import RoiManager
from ij.plugin import ChannelSplitter
from ij.io import FileSaver
from ij.gui import Roi
from ij.gui import Overlay
from ij.io import Opener
from ij.measure import ResultsTable
from ij.measure import Calibration
from fiji.threshold import Auto_Threshold
from loci.plugins import BF
from loci.common import Region
from loci.plugins.in import ImporterOptions
from loci.plugins.util import LociPrefs
from loci.plugins.out import Exporter
from loci.plugins import LociExporter
from loci.formats import ImageReader
from loci.formats import MetadataTools
from loci.formats.in import ZeissCZIReader
from loci.formats.in import DynamicMetadataOptions
from ome.units import UNITS

# MorphoLibJ imports
from inra.ijpb.binary import BinaryImages, ChamferWeights3D, ChamferWeights
from inra.ijpb.morphology import MinimaAndMaxima3D, Morphology, Strel3D
from inra.ijpb.watershed import Watershed
from inra.ijpb.label import LabelImages
from inra.ijpb.plugins import ParticleAnalysis3DPlugin
from inra.ijpb.plugins import BoundingBox3DPlugin
from inra.ijpb.plugins import ExtendBordersPlugin
from inra.ijpb.data.border import BorderManager3D, ReplicatedBorder3D
from inra.ijpb.util.ColorMaps import CommonLabelMaps
from inra.ijpb.util import CommonColors
from inra.ijpb.plugins import DistanceTransformWatershed3D, FillHolesPlugin
from inra.ijpb.data.image import Images3D
from inra.ijpb.watershed import ExtendedMinimaWatershed
from inra.ijpb.morphology import Reconstruction
from inra.ijpb.morphology import Reconstruction3D


class MetaData:

    @staticmethod
    def get_metadata(imagefile, imageID=0):

        metainfo = {}
        # checking for thr file Extension
        metainfo['Extension'] = MiscTools.getextension(MiscTools.splitext_recurse(imagefile))

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

        return metainfo

    @staticmethod
    def order_metadict(metainfo_dict):

        # order the metadata dictionary
        metainfo_ordered = OrderedDict(sorted(metainfo_dict.items()))

        return metainfo_ordered 


class ImportTools:

    @staticmethod
    def openfile(imagefile,
                 stitchtiles=True,
                 setflatres=False,
                 readpylevel=0,
                 setconcat=True,
                 openallseries=True,
                 showomexml=False,
                 attach=False,
                 autoscale=True,
                 imageID=0):

        # stitchtiles = option of CZIReader to return the raw tiles as
        # individual series rather than the auto-stitched images

        metainfo = MetaData.get_metadata(imagefile, imageID=imageID)

        # if image file is Carl Zeiss Image - CZI
        if metainfo['Extension'] == '.czi':

            # read the CZI file using the CZIReader
            # pylevel = 0 - read the full resolution image

            imp, metainfo = ImportTools.readCZI(imagefile, metainfo,
                                                           stitchtiles=stitchtiles,
                                                           setflatres=setflatres,
                                                           readpylevel=readpylevel,
                                                           setconcat=setconcat,
                                                           openallseries=openallseries,
                                                           showomexml=showomexml,
                                                           attach=attach,
                                                           autoscale=autoscale)

        # if image file is not Carl Zeiss Image - CZI
        if metainfo['Extension'] != '.czi':

            # read the imagefile using the correct method
            if metainfo['Extension'].lower() == ('.jpg' or '.jpeg'):
                # use dedicated method for jpg
                imp, metainfo = ImageTools.openjpg(imagefile, metainfo, method='IJ', series=0)
            else:
                # if not jpg - use BioFormats
                imp, metainfo = ImportTools.readbf(imagefile, metainfo,
                                                   setflatres=setflatres,
                                                   readpylevel=readpylevel,
                                                   setconcat=setconcat,
                                                   openallseries=openallseries,
                                                   showomexml=showomexml,
                                                   autoscale=autoscale,
                                                   stitchtiles=stitchtiles)

        return imp, metainfo

    @staticmethod
    def readbf(imagefile, metainfo,
               setflatres=False,
               readpylevel=0,
               setconcat=False,
               openallseries=True,
               showomexml=False,
               autoscale=True,
               stitchtiles=True):

        # initialize the importer options
        options = ImporterOptions()
        options.setOpenAllSeries(openallseries)
        options.setShowOMEXML(showomexml)
        options.setConcatenate(setconcat)
        options.setAutoscale(autoscale)
        options.setId(imagefile)
        options.setStitchTiles(stitchtiles)

        # in case of concat=True all series set number of series = 1
        # and set pyramidlevel = 0 (1st level) since there will be only one
        # unless setflatres = True --> read pyramid levels

        series = metainfo['SeriesCount_BF']
        if setconcat and setflatres:
            series = 1
            readpylevel = 0

        metainfo['Pyramid Level Output'] = readpylevel

        # open the ImgPlus
        imps = BF.openImagePlus(options)

        # read image data using the specified pyramid level
        imp, slices, width, height, pylevel = ImageTools.getImageSeries(imps, series=readpylevel)

        metainfo['Output Slices'] = slices
        metainfo['Output SizeX'] = width
        metainfo['Output SizeY'] = height

        return imp, metainfo

    @staticmethod
    def openjpg(imagefile, metainfo, method='IJ',
                                     series=0):

        if method == 'IJ':

            # using IJ static method
            imp = IJ.openImage(imagefile)

        if method == 'Opener':

            # Using Opener class
            imp = Opener().openImage(imagefile)

        if method == 'BF':

            # using BioFormats library
            imps = BF.openImagePlus(imagefile)

            # read image data using the specified pyramid level
            imp, slices, width, height, pylevel = ImageTools.getImageSeries(imps, series=series)
            metainfo['Output Slices'] = slices
            metainfo['Output SizeX'] = width
            metainfo['Output SizeY'] = height

        return imp, metainfo

    @staticmethod
    def readCZI(imagefile,
                metainfo,
                stitchtiles=False,
                setflatres=False,
                readpylevel=0,
                setconcat=False,
                openallseries=True,
                showomexml=False,
                attach=False,
                autoscale=True):
        
        # define the reader options
        reader_options, czireader = ImportTools.setReaderOptions(imagefile, stitchtiles=stitchtiles,
                                                                            setflatres=setflatres,
                                                                            setconcat=setconcat,
                                                                            openallseries=openallseries,
                                                                            showomexml=showomexml,
                                                                            attach=attach,
                                                                            autoscale=autoscale)
        
        # update metainformation
        metainfo['rescount'] = czireader.getResolutionCount()
        metainfo['SeriesCount_CZI'] = czireader.getSeriesCount()
        metainfo['flatres'] = czireader.hasFlattenedResolutions()

        # Dimensions
        metainfo['SizeT'] = czireader.getSizeT()
        metainfo['SizeZ'] = czireader.getSizeZ()
        metainfo['SizeC'] = czireader.getSizeC()
        metainfo['SizeX'] = czireader.getSizeX()
        metainfo['SizeY'] = czireader.getSizeY()

        # check for autostitching and possibility to read attachment
        metainfo['AllowAutoStitching'] = czireader.allowAutostitching()
        metainfo['CanReadAttachments'] = czireader.canReadAttachments()

        # open the ImgPlus using BioFormats
        imps = BF.openImagePlus(reader_options)
        metainfo['Pyramid Level Output'] = readpylevel

        # read image data using the specified pyramid level
        imp, slices, width, height, pylevel = ImageTools.getImageSeries(imps, series=readpylevel)
        metainfo['Pyramid Level Output'] = pylevel

        metainfo['Output Slices'] = slices
        metainfo['Output SizeX'] = width
        metainfo['Output SizeY'] = height

        # calc scaling in case of pyramid
        # scale = float(metainfo['Output SizeX']) / float(metainfo['SizeX'])
        scale = float(metainfo['SizeX']) / float(metainfo['Output SizeX'])

        metainfo['Pyramid Scale Factor'] = scale
        metainfo['ScaleX Output'] = metainfo['ScaleX'] * scale
        metainfo['ScaleY Output'] = metainfo['ScaleY'] * scale

        imp = MiscTools.setscale(imp, scaleX=metainfo['ScaleX Output'],
                                      scaleY=metainfo['ScaleX Output'],
                                      scaleZ=metainfo['ScaleZ'],
                                      unit="micron")

        # close czireader
        czireader.close()

        return imp, metainfo

    @staticmethod
    def setReaderOptions(imagefile, stitchtiles=False,
                                    setflatres=True,
                                    setconcat=False,
                                    openallseries=False,
                                    showomexml=False,
                                    attach=False,
                                    autoscale=True):

        czi_options = DynamicMetadataOptions()
        czi_options.setBoolean("zeissczi.autostitch", stitchtiles)
        czi_options.setBoolean("zeissczi.attachments", attach)

        # set the option for the CZIReader
        czireader = ImportTools.setCZIReaderOptions(imagefile, czi_options, setflatres=setflatres)

        # Set the preferences in the ImageJ plugin
        # Note although these preferences are applied, they are not refreshed in the UI
        Prefs.set("bioformats.zeissczi.allow.autostitch", str(stitchtiles).lower())
        Prefs.set("bioformats.zeissczi.include.attachments", str(attach).lower())

        # set the option for the BioFormats import
        reader_options = ImporterOptions()
        reader_options.setOpenAllSeries(openallseries)
        reader_options.setShowOMEXML(showomexml)
        reader_options.setConcatenate(setconcat)
        reader_options.setAutoscale(autoscale)
        reader_options.setStitchTiles(stitchtiles)
        reader_options.setId(imagefile)

        return reader_options, czireader

    @staticmethod
    def setCZIReaderOptions(imagefile, czi_options, setflatres=True):

        czireader = ZeissCZIReader()
        czireader.setFlattenedResolutions(setflatres)
        czireader.setMetadataOptions(czi_options)
        czireader.setId(imagefile)

        return czireader

    @staticmethod
    def readCZIattachment(imagefile,
                          stitchtiles=False,
                          setflatres=False,
                          readpylevel=0,
                          setconcat=False,
                          openallseries=False,
                          showomexml=False,
                          attach=False,
                          autoscale=True):
        
        # define the reader options
        reader_options, czireader = ImportTools.setReaderOptions(imagefile, stitchtiles=stitchtiles,
                                                                            setflatres=setflatres,
                                                                            setconcat=setconcat,
                                                                            openallseries=openallseries,
                                                                            showomexml=showomexml,
                                                                            attach=attach,
                                                                            autoscale=autoscale)

        # open the ImgPlus
        imps_attach = BF.openImagePlus(reader_options)

        # read image data using the specified pyramid level
        imp_attach, slices, width, height, pylevel = ImageTools.getImageSeries(imps_attach, series=readpylevel)
        czireader.close()

        return imp_attach


class ExportTools:

    @staticmethod
    def bfexporter(imp, savepath, useLOCI=True):

        if useLOCI:

            paramstring = "outfile=[" + savepath + "] windowless=true compression=Uncompressed saveROI=false"
            plugin = LociExporter()
            plugin.arg = paramstring
            exporter = Exporter(plugin, imp)
            exporter.run()

        # save as OME-TIFF using BioFormats library using the IJ.run method
        if not useLOCI:

            # 2019-04-25: This does not seem to work in headless anymore
            paramstring = "save=[" + savepath + "] compression=Uncompressed"
            IJ.run(imp, "Bio-Formats Exporter", paramstring)

        return paramstring

    @staticmethod
    def savedata(imp, savepath, extension='ome.tiff', replace=False):

        # general function for saving image data in different formats

        # check if file already exists and delete if replace is true
        if os.path.exists(savepath):
            if replace:
                os.remove(savepath)
            if not replace:
                return None

        # general safety check
        # if not extension:
        #    extension = 'ome.tiff'

        # check extension
        if extension in ['tiff', 'tif', 'ome.tiff', 'ome.tif', 'png', 'jpeg']:

            fs = FileSaver(imp)
            nslices = imp.getStack().getSize()  # get the number of slices

            # in case of TIFF
            if extension == ('tiff' or 'tif' or 'TIFF' or 'TIF'):
                if nslices > 1:
                    fs.saveAsTiffStack(savepath)
                if nslices == 1:
                    fs.saveAsTiff(savepath)

            # in case of OME-TIFF
            elif extension == 'ome.tiff' or extension == 'ome.tif':
                print("Saving: ", savepath)
                pstr = ExportTools.bfexporter(imp, savepath, useLOCI=True)
                print('BioFormats Paramstring : ', pstr)

            # in case of PNG
            elif extension == ('png' or 'PNG'):
                fs.saveAsPng(savepath)

            # in case
            elif extension == ('jpeg' or 'jpg' or 'JPEG' or 'JPG'):
                fs.saveAsJpeg(savepath)

        else:
            extension = 'ome.tiff'
            print("Saving: ", savepath)
            pstr = ExportTools.bfexporter(imp, savepath, useLOCI=True)
            print('BioFormats Paramstring : ', pstr)

        return savepath

    @staticmethod
    def save_singleplanes(imp, savepath, metainfo, mode='TZC', format='tiff'):
        """
        This function is still in testing.
        """
        titleext = imp.getTitle()
        title = os.path.splitext(titleext)[0]

        if mode == 'TZC':

            for t in range(metainfo['SizeT']):
                for z in range(metainfo['SizeZ']):
                    for c in range(metainfo['SizeC']):
                        # set position - channel, slice, frame
                        imp.setPosition(c + 1, z + 1, t + 1)
                        numberedtitle = title + "_t" + IJ.pad(t, 2) + "_z" + IJ.pad(z, 4) + "_c" + IJ.pad(c, 4) + "." + format
                        stackindex = imp.getStackIndex(c + 1, z + 1, t + 1)
                        aframe = ImagePlus(numberedtitle, imp.getStack().getProcessor(stackindex))
                        outputpath = os.path.join(savepath, numberedtitle)
                        IJ.saveAs(aframe, "TIFF", outputpath)

        if mode == 'Z':
            c = 0
            t = 0
            for z in range(metainfo['SizeZ']):
                # set position - channel, slice, frame
                imp.setPosition(c + 1, z + 1, t + 1)
                znumber = MiscTools.addzeros(z)
                numberedtitle = title + "_z" + znumber + "." + format
                stackindex = imp.getStackIndex(c + 1, z + 1, t + 1)
                aframe = ImagePlus(numberedtitle, imp.getStack().getProcessor(stackindex))
                outputpath = os.path.join(savepath, numberedtitle)
                IJ.saveAs(aframe, "TIFF", outputpath)


class FilterTools:

    @staticmethod
    def apply_rollingball(imp,
                          radius=30,
                          createBackground=False,
                          lightBackground=False,
                          useParaboloid=False,
                          doPresmooth=True,
                          correctCorners=False):

        # Create BackgroundSubtracter instance
        bs = BackgroundSubtracter()
        stack = imp.getStack()  # get the stack within the ImagePlus
        nslices = stack.getSize()  # get the number of slices

        for index in range(1, nslices + 1):
            ip = stack.getProcessor(index)
            # Run public method rollingBallBackground
            bs.rollingBallBackground(ip,
                                     radius,
                                     createBackground,
                                     lightBackground,
                                     useParaboloid,
                                     doPresmooth,
                                     correctCorners)

        return imp

    @staticmethod
    def apply_filter(imp, radius=5, filtertype='MEDIAN'):

        # initialize filter
        filter = RankFilters()

        # create filter dictionary for 2D rank filters
        filterdict = {}
        filterdict['MEAN'] = RankFilters.MEAN
        filterdict['MIN'] = RankFilters.MIN
        filterdict['MAX'] = RankFilters.MAX
        filterdict['MEDIAN'] = RankFilters.MEDIAN
        filterdict['VARIANCE'] = RankFilters.VARIANCE
        filterdict['OPEN'] = RankFilters.OPEN
        filterdict['DESPECKLE'] = RankFilters.DESPECKLE
        filterdict['Mean'] = RankFilters.MEAN
        filterdict['Min'] = RankFilters.MIN
        filterdict['Max'] = RankFilters.MAX
        filterdict['Median'] = RankFilters.MEDIAN
        filterdict['Variance'] = RankFilters.VARIANCE
        filterdict['Open'] = RankFilters.OPEN
        filterdict['Despeckle'] = RankFilters.DESPECKLE

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

    @staticmethod
    def apply_filter3d(imp,
                       radiusx=5,
                       radiusy=5,
                       radiusz=5,
                       filtertype='MEDIAN'):

        # initialize filter
        f3d = Filters3D()

        # create filter dictionary for 3d filters
        filterdict = {}
        filterdict['MEAN'] = f3d.MEAN
        filterdict['MIN'] = f3d.MIN
        filterdict['MAX'] = f3d.MAX
        # filterdict['MAXLOCAL'] = f3d.MAXLOCAL # did not work
        filterdict['MEDIAN'] = f3d.MEDIAN
        filterdict['VAR'] = f3d.VAR

        stack = imp.getStack()  # get the stack within the ImagePlus
        newstack = f3d.filter(stack,
                              filterdict[filtertype],
                              radiusx,
                              radiusy,
                              radiusz)

        imp = ImagePlus('Filtered 3D', newstack)

        return imp


class BinaryTools:

    @staticmethod
    def fill_holes(imp, is3d=False):

        if not is3d:
            
            # 2D fill holes
            im_stack = imp.getStack()  # get the stack within the ImagePlus
            nslices = im_stack.getSize()  # get the number of slices
            for index in range(1, nslices + 1):
                
                ip = im_stack.getProcessor(index)
                ip.invert()
                # Reconstruction.fillHoles(imp.getProcessor())
                Reconstruction.fillHoles(ip)
                ip.invert()

        if is3d:
            
            # 3D fill holes
            im_stack = Reconstruction3D.fillHoles(imp.getImageStack())

        # convert back to ImgPlus
        out = ImagePlus("Fill Holes", im_stack)

        return out


class WaterShedTools:

    @staticmethod
    def run_watershed(imp,
                      mj_normalize=True,
                      mj_dynamic=1,
                      mj_connectivity=6,
                      is3d=False):

        if not is3d:
            print('Detected 2D image.')
            # run watershed on 2D image
            print('Watershed : 2D image')
            imp_ws = WaterShedTools.edm_watershed(imp)

        if is3d:

            # for 3D Stacks only connectivity 6 or 26 is allowed
            if mj_connectivity not in [6, 26]:
                mj_connectivity = 6
                print('Only 6 or 26 connectivity for 3D stacks is allowed. Using 6.')

            print('Watershed MJ: 3D image')
            imp_ws = WaterShedTools.mj_watershed3d(imp,
                                                   normalize=mj_normalize,
                                                   dynamic=mj_dynamic,
                                                   connectivity=mj_connectivity)

        
        
        return imp_ws

    @staticmethod
    def edm_watershed(imp):

        stack = imp.getStack()  # get the stack within the ImagePlus
        nslices = stack.getSize()  # get the number of slices
        for index in range(1, nslices + 1):
            # get the image processor
            ip = stack.getProcessor(index)

            if not ip.isBinary():
                ip = BinaryImages.binarize(ip)
            
            #print('Apply Watershed to Binary image ...')
            #print(type(ip))
            #print('isBinary : ', ip.isBinary())
            
            edm = EDM()
            edm.setup("watershed", None)
            edm.run(ip)

        return imp

    @staticmethod
    def mj_watershed3d(imp,
                       normalize=True,
                       dynamic=1,
                       connectivity=6):

        # run watershed on stack
        weights = ChamferWeights3D.BORGEFORS.getFloatWeights()
        
        # calc distance map and invert
        dist = BinaryImages.distanceMap(imp.getStack(), weights, normalize)
        Images3D.invert(dist)
        
        basins = ExtendedMinimaWatershed.extendedMinimaWatershed(dist, imp.getStack(), dynamic, connectivity, False)
        #basins = ExtendedMinimaWatershed.extendedMinimaWatershed(dist, imp, dynamic, connectivity, False)
        
        imp_basins = ImagePlus("basins", basins)
        ip = imp_basins.getProcessor()
        ip.setThreshold(1, 255, ImageProcessor.NO_LUT_UPDATE)

        return imp_basins


class ImageTools:

    @staticmethod
    def getImageSeries(imps, series=0):

        try:
            imp = imps[series]
            pylevelout = series
        except:
            # fallback option
            print('PyLevel = ' + str(series) + ' does not exist.')
            print('Using Pyramid Level = 0 as fallback.')
            imp = imps[0]
            pylevelout = 0

        # get the stack and some info
        imgstack = imp.getImageStack()
        slices = imgstack.getSize()
        width = imgstack.getWidth()
        height = imgstack.getHeight()

        return imp, slices, width, height, pylevelout


class ThresholdTools:

    @staticmethod
    def apply_autothreshold(hist, method='Otsu'):    
        """
        if method == 'Otsu':
            lowthresh = Auto_Threshold.Otsu(hist)
        if method == 'Triangle':
            lowthresh = Auto_Threshold.Triangle(hist)
        if method == 'Default':
            lowthresh = Auto_Threshold.IJDefault(hist)
        if method == 'Huang':
            lowthresh = Auto_Threshold.Huang(hist)
        if method == 'MaxEntropy':
            lowthresh = Auto_Threshold.MaxEntropy(hist)
        if method == 'Mean':
            lowthresh = Auto_Threshold.Mean(hist)
        if method == 'Shanbhag':
            lowthresh = Auto_Threshold.Shanbhag(hist)
        if method == 'Yen':
            lowthresh = Auto_Threshold.Yen(hist)
        if method == 'Li':
            lowthresh = Auto_Threshold.Li(hist)

        return lowthresh
        """

        method_dict = {'Otsu': Auto_Threshold.Otsu,
                       'Triangle': Auto_Threshold.Triangle,
                       'Default': Auto_Threshold.IJDefault,
                       'Huang': Auto_Threshold.Huang,
                       'MaxEntropy': Auto_Threshold.MaxEntropy,
                       'Mean': Auto_Threshold.Mean,
                       'Shanbhag': Auto_Threshold.Shanbhag,
                       'Yen': Auto_Threshold.Yen,
                       'Li': Auto_Threshold.Li
                       }

        if method in method_dict:
            method_func = method_dict[method]
            lowthresh = method_func(hist)
            return lowthresh
        else:
            print("Method passed not found: {method}")
            return None

    @staticmethod
    # helper function to apply threshold to whole stack
    # using one corrected value for the stack
    def apply_threshold_stack_corr(imp, lowth_corr):

        # get the stacks
        stack = imp.getStack()
        nslices = stack.getSize()

        for index in range(1, nslices + 1):
            ip = stack.getProcessor(index)
            ip.threshold(lowth_corr)

        # convert to 8bit without rescaling
        ImageConverter.setDoScaling(False)
        ImageConverter(imp).convertToGray8()

        return imp

    @staticmethod
    # apply threshold either to whole stack or slice-by-slice
    def apply_threshold(imp, method='Otsu',
                        background_threshold='dark',
                        stackopt=False,
                        corrf=1.0):

        # one threshold value for the whole stack with correction
        if stackopt:

            # create argument string for the IJ.setAutoThreshold
            thcmd = method + ' ' + background_threshold + ' stack'

            # set threshold and get the lower threshold value
            IJ.setAutoThreshold(imp, thcmd)
            ip = imp.getProcessor()

            # get the threshold value and correct it
            lowth = ip.getMinThreshold()
            lowth_corr = int(round(lowth * corrf, 0))

            # process stack with corrected threshold value
            imp = ThresholdTools.apply_threshold_stack_corr(imp, lowth_corr)

        # threshold slice-by-slice with correction
        if not stackopt:

            # get the stack
            stack = imp.getStack()  # get the stack within the ImagePlus
            nslices = stack.getSize()  # get the number of slices
            print('Slices: ' + str(nslices))
            print('Thresholding slice-by-slice')

            for index in range(1, nslices + 1):

                ip = stack.getProcessor(index)

                # get the histogram
                hist = ip.getHistogram()

                # get the threshold value
                lowth = ThresholdTools.apply_autothreshold(hist, method=method)
                lowth_corr = int(round(lowth * corrf, 0))
                ip.threshold(lowth_corr)

            # convert to 8bit without rescaling
            ImageConverter.setDoScaling(False)
            ImageConverter(imp).convertToGray8()

        return imp


class AnalyzeTools:

    @staticmethod
    def analyzeParticles(imp,
                         minsize,
                         maxsize,
                         mincirc,
                         maxcirc,
                         #filename='Test.czi',
                         addROIManager=False,
                         #headless=False,
                         exclude=True):

        if GraphicsEnvironment.isHeadless():
            print('Headless Mode detected. Do not use ROI Manager.')
            addROIManager = False

        if addROIManager:

            # get the ROI manager instance
            rm = RoiManager.getInstance()
            if rm is None:
                rm = RoiManager()
            rm.runCommand("Associate", "true")

            if not exclude:
                options = PA.SHOW_ROI_MASKS \
                    + PA.SHOW_RESULTS \
                    + PA.DISPLAY_SUMMARY \
                    + PA.ADD_TO_MANAGER \
                    + PA.ADD_TO_OVERLAY \

            if exclude:
                options = PA.SHOW_ROI_MASKS \
                    + PA.SHOW_RESULTS \
                    + PA.DISPLAY_SUMMARY \
                    + PA.ADD_TO_MANAGER \
                    + PA.ADD_TO_OVERLAY \
                    + PA.EXCLUDE_EDGE_PARTICLES

        if not addROIManager:

            if not exclude:
                options = PA.SHOW_ROI_MASKS \
                    + PA.SHOW_RESULTS \
                    + PA.DISPLAY_SUMMARY \
                    + PA.ADD_TO_OVERLAY \

            if exclude:
                options = PA.SHOW_ROI_MASKS \
                    + PA.SHOW_RESULTS \
                    + PA.DISPLAY_SUMMARY \
                    + PA.ADD_TO_OVERLAY \
                    + PA.EXCLUDE_EDGE_PARTICLES

        measurements = PA.STACK_POSITION \
            + PA.LABELS \
            + PA.AREA \
            + PA.RECT \
            + PA.PERIMETER \
            + PA.SLICE \
            + PA.SHAPE_DESCRIPTORS \
            + PA.CENTER_OF_MASS \
            + PA.CENTROID

        results = ResultsTable()
        p = PA(options, measurements, results, minsize, maxsize, mincirc, maxcirc)
        p.setHideOutputImage(True)
        particlestack = ImageStack(imp.getWidth(), imp.getHeight())

        for i in range(imp.getStackSize()):
            imp.setSliceWithoutUpdate(i + 1)
            ip = imp.getProcessor()
            # convert to a mask for the particle analyzer
            ip.invert()
            # do the particle analysis
            p.analyze(imp, ip)
            mmap = p.getOutputImage()
            # add the slide to the full stack
            particlestack.addSlice(mmap.getProcessor())

        return particlestack, results

    @staticmethod
    def create_resultfilename(filename, suffix='_Results', extension='txt'):

        # create the name for the result file
        rtfilename = os.path.splitext(filename)[0] + suffix + '.' + extension

        return rtfilename


class RoiTools:

    @staticmethod
    def roiprocess(imp, filename):

        # get the ROI manager instance
        rm = RoiManager.getInstance()
        if rm is None:
            rm = RoiManager()

        rm.runCommand(imp, "Select All")
        # rm.runCommand("Deselect"); # deselect ROIs to save them all
        rm.runCommand(imp, 'Show All')
        # define the path to save the rois as azip file
        roisavelocation = os.path.splitext(filename)[0] + '_RoiSet.zip'
        # log.info('ROISs saved: ' + roisavelocation)
        # print('ROIs saved: ', roisavelocation)
        rm.runCommand("Save", roisavelocation)

        return roisavelocation

    @staticmethod
    def roiprocess_ov(imp, filename):
        """
        !!! This is for testing purposes only. It is currently not used !!!
        """
        ov = Overlay()
        rt = ov.measure(imp)
        # log.info('Size ResultTable: ' + str(rt.size()))
        # print('Size ResultTable: ', rt.size())

        return None


class MiscTools:

    @staticmethod
    def apply_binning(imp, binning=4, method="Sum"):

        IJ.run(imp, "Bin...", "x=" + str(binning) + " y=" + str(binning) + " bin=" + method)

        return imp

    @staticmethod
    def getextension(splitresult):
        """Get the file extension even it is  *.ome.tiff

        :param splitresult: results from splitting the path
        :type splitresult: list
        :return: file extension
        :rtype: str
        """  

        if len(splitresult) == 2:
            # only one extension part, eg *.czi detected
            extension = str(splitresult[-1])
        if len(splitresult) >= 3:
            # two extension part, eg *.ome.tiff detected
            # extension = str(splitresult[1] + splitresult[2])

            ext2 = splitresult[-2]
            if ext2 != ('.ome' or '.OME'):
                # set ext2 empty in case it is not .ome or .OME
                ext2 = ''

            extension = str(ext2 + splitresult[-1])

        return extension

    @staticmethod
    def splitext_recurse(filepath):
        """Get base filename

        :param filepath: filepath
        :type filepath: str
        :return: base filename
        :rtype: str
        """ 

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
        """Set properties of image in Fiji

        :param imp: Image
        :type imp: ImgPlus
        :param scaleX: scaleX, defaults to 1.0
        :type scaleX: float, optional
        :param scaleY: scaleY, defaults to 1.0
        :type scaleY: float, optional
        :param scaleZ: scaleZ, defaults to 1.0
        :type scaleZ: float, optional
        :param unit: scale unit, defaults to "micron"
        :type unit: str, optional
        :param sizeC: sizeC, defaults to 1
        :type sizeC: int, optional
        :param sizeZ: sizeZ, defaults to 1
        :type sizeZ: int, optional
        :param sizeT: sizeT, defaults to 1
        :type sizeT: int, optional
        :return: Image
        :rtype: ImgPlus
        """        

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

        # apply the new calibration
        imp.setCalibration(newCal)

        return imp

    @staticmethod
    def setscale(imp,
                 scaleX=1.0,
                 scaleY=1.0,
                 scaleZ=1.0,
                 unit="micron"):
        """Set new scaling for image.

        :param imp: image
        :type imp: ImgPlus
        :param scaleX: scaleX, defaults to 1.0
        :type scaleX: float, optional
        :param scaleY: scaleY, defaults to 1.0
        :type scaleY: float, optional
        :param scaleZ: scaleZ, defaults to 1.0
        :type scaleZ: float, optional
        :param unit: scaling unit, defaults to "micron"
        :type unit: str, optional
        :return: image
        :rtype: ImgPlus
        """  


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

    @staticmethod
    def splitchannel(imp, chindex):

        nch = imp.getNChannels()
        print('Number of Channels: ' + str(nch))
        if chindex > nch:
            # if nch > 1:
            print('Fallback : Using Channel 1')
            chindex = 1
            imps = ChannelSplitter.split(imp)
            imp = imps[chindex - 1]

        if chindex <= nch:
            imps = ChannelSplitter.split(imp)
            imp = imps[chindex - 1]

        return imp

    @staticmethod
    def addzeros(number):

        if number < 10:
            zerostring = '000000' + str(number)
        if number >= 10 and number < 100:
            zerostring = '00000' + str(number)
        if number >= 100 and number < 1000:
            zerostring = '0000' + str(number)
        if number >= 1000 and number < 10000:
            zerostring = '000' + str(number)
        if number >= 10000 and number < 100000:
            zerostring = '00' + str(number)
        if number >= 100000 and number < 1000000:
            zerostring = '0' + str(number)

        return zerostring

    @staticmethod
    def createdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
            dir_created = False
        else:
            print("Successfully created the directory %s " % path)
            dir_created = True

        return dir_created

    @staticmethod
    def getfiles(path, filter='ome.tiff'):

        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if filter in file:
                    files.append(os.path.join(r, file))

        return files

    @staticmethod
    def import_sequence(inputdir,
                        number=10,
                        start=1,
                        increment=1,
                        scale=100,
                        filepattern='*.',
                        sort=True,
                        use_virtualstack=False):

        args = "open=" + inputdir
        args += " number=" + str(number)
        args += " starting=" + str(start)
        args += " increment=" + str(increment)
        args += " scale=" + str(scale)
        args += " file=" + filepattern

        if sort:
            args += " sort"
        if use_virtualstack:
            args += " use"

        print "Import Sequence Arguments : ", args

        IJ.run("Image Sequence...", args)
        imp = IJ.getImage()

        return imp

    @staticmethod
    def copyorig(src, dst, force_overwrite=True):

        if force_overwrite:
            if os.path.exists(dst):
                os.remove(dst)
                print('Removed before copy: ', dst)
        start = time.clock()
        try:
            shutil.copy2(src, dst)
            copy_ok = 'Copied original file to output.'
        except IOError:
            copy_ok = str(IOError)
        end = time.clock()

        print('Duration Copying : ', str(end - start))

        return copy_ok


class JSONTools:

    @staticmethod
    def writejsonoutput(outfilelist, inputjson):
        # write files to output
        with open("/output/" + inputjson['WFE_output_params_file'], 'w') as f:
            outputjson = {"FILTERED_IMAGE": outfilelist}
            json.dump(outputjson, f)

    @staticmethod
    def writejsonfile(data, jsonfilename='Metadata.json', savepath='C:\Temp'):

        jsonfile = os.path.join(savepath, jsonfilename)

        # Writing JSON data
        with open(jsonfile, 'w') as f:
            json.dump(data, f, indent=4)

        return jsonfile

    @staticmethod
    def convert2bool(inputstring):

        if inputstring == 'False' or inputstring == 'false':
            outputbool = False
        if inputstring == 'True' or inputstring == 'true':
            outputbool = True

        return outputbool
