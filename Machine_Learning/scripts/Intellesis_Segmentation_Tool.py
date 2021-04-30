#################################################################
# File       : Intellesis_Segmentation_Tool.py
# Version    : 0.9
# Author     : czsrh
# Date       : 25.03.2019
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from System.IO import File, Directory, Path, SearchOption
import sys
import clr
clr.AddReference('System.Xml')
import System.Xml
from System import ApplicationException

version = 0.9


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


def getshortfiles(filelist):
    # get the short filesnames from all list entries
    files_short = []
    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short


def getmodelname(xmldoc):
    # get modelname from XML file
    modelname = None
    nodes = xmldoc.SelectNodes('Model/ModelName')
    for node in nodes:
        modelname = node.InnerText

    return modelname


def getmodelid(xmldoc):
    # get modelid from XML file
    modelid = None
    nodes = xmldoc.SelectNodes('Model/Id')
    for node in nodes:
        modelid = node.InnerText

    return modelid


def getmodelclassnumber(modelfile):
    # get number of classes of model from XML model file
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(modelfile)
    nodes = xmldoc.SelectNodes('Model/TrainingClasses')
    for node in nodes:
        numclasses = node.ChildNodes.Count

    return numclasses


def cleanup_dict(dc):

    # clean dictionary incase there are invalid values
    clean_keys = None
    clean_value = None

    filtered = {k: v for k, v in dc.items() if k is not clean_keys}
    dc.clear()
    dc.update(filtered)

    filtered = {k: v for k, v in dc.items() if v is not clean_value}
    dc.clear()
    dc.update(filtered)

    return dc


def classify(image, model,
             use_confidence=True,
             confidence_threshold=0,
             format='MultiChannel',
             extractclass=False,
             addseg=False,
             classid=1,
             adapt_pixeltype=True):

    if format == 'MultiChannel':
        segf = ZenSegmentationFormat.MultiChannel
    if format == 'Labels':
        segf = ZenSegmentationFormat.Labels

    # classify pixels using a trained model
    if use_confidence:
        try:
            # run the segmentation and apply confidence threshold to segmented image
            outputs = Zen.Processing.Segmentation.TrainableSegmentationWithProbabilityMap(image, model, segf)
            seg_image = outputs[0]
            conf_map = outputs[1]
            print('Apply Confidence Threshold to segmented image.')
            seg_image = Zen.Processing.Segmentation.MinimumConfidence(seg_image, conf_map, confidence_threshold)
            conf_map.Close()
            del outputs
        except ApplicationException as e:
            seg_image = None
            print('Application Exception : ', e.Message)

    if not use_confidence:
        try:
            # run the segmentation
            seg_image = Zen.Processing.Segmentation.TrainableSegmentation(image, model, segf)
        except ApplicationException as e:
            seg_image = None
            print('Application Exception : ', e.Message)

    if adapt_pixeltype:
        # adapt the pixeltype to match the type of the original image
        pxtype = image.Metadata.PixelType
        seg_image = Zen.Processing.Utilities.ChangePixelType(seg_image, pxtype)
        print('New PixelTyper for Segmented Image : ', seg_image.Metadata.PixelType)

    if extractclass:

        # create subset string
        substr = 'C(' + str(classid) + ')'
        seg_image = Zen.Processing.Utilities.CreateSubset(seg_image, substr, False)

    if addseg:
        # add original and segmentation
        seg_image = Zen.Processing.Utilities.AddChannels(image, seg_image)

    return seg_image


def createidstr(maxclass):

    classstr = []
    for i in range(1, maxclass + 1):
        classstr.append(str(i))

    return classstr


##############################################################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

# check the location of folder where experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
# or you your own default folder
imgfolder = r'c:\Output\Intellesis_Batch_Test'

# maximum number of classes
maxclass = 16
classlist = createidstr(maxclass)

# get list with all existing models and a short version of that list
modelfolder = Path.Combine(docfolder, 'Model-Repository')
modelfiles = Directory.GetFiles(modelfolder, '*.xml')

if is_empty(modelfiles):
    # catch exception in case the folder contains no models at all
    message = 'No modelfiles found in specified folder: '
    print(message, Path.Combine(docfolder, 'Model-Repository'))
    raise SystemExit

# get the list of filename use only the basefilename
modelfiles_short = getshortfiles(modelfiles)
modeldict = {}

# create list for the short modelnames to be used iside UI of dialog
modelnames_short = []

for modelfile in modelfiles:

    # Load XML model file
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(modelfile)
    # get modelnames and modelid and update dictionary
    modelname = getmodelname(xmldoc)
    modelid = getmodelid(xmldoc)
    modeldict[modelname] = modelfile

# create list from dict
modeldict = cleanup_dict(modeldict)
for mdname in modeldict.keys():
    modelnames_short.append(mdname)

# sort list for nicer dropdown menu later in dialog window
modelnames_short.sort(key=str.lower)

#############################################################################

# initialize Dialog
IntellesisBatchDialog = ZenWindow()
IntellesisBatchDialog.Initialize('Intellesis Segmentation Tool - Version: ' + str(version))
# add components to dialog
IntellesisBatchDialog.AddLabel('1) Select Intellesis Model for Segmentation')
IntellesisBatchDialog.AddDropDown('modelnames', 'Intellesis Model', modelnames_short, 0)
IntellesisBatchDialog.AddLabel('2) Select SegmentationFormat type')
IntellesisBatchDialog.AddDropDown('segformat', 'SegmentationFormat Output', ['MultiChannel', 'Labels'], 0)
IntellesisBatchDialog.AddCheckbox('use_confidence', 'Use Confidence Threshold', False)
IntellesisBatchDialog.AddIntegerRange('prob_threshold', 'Specify Confidence Threshold for Classification', 90, 0, 99)
IntellesisBatchDialog.AddLabel('3) Class Extraction Option')
IntellesisBatchDialog.AddCheckbox('extract_class', 'Extract (requires MultiChannel as Output Format)', False)
IntellesisBatchDialog.AddDropDown('extract_class_list', 'Select Class ID', classlist, 0)
IntellesisBatchDialog.AddLabel('4) Additional Tools')
IntellesisBatchDialog.AddCheckbox('addsegm', 'Add Segmentation Mask to Original Image', False)
IntellesisBatchDialog.AddCheckbox('adapt', 'Adapt PixelType of Segmented Mask to match Original Image', False)
IntellesisBatchDialog.AddCheckbox('segactive', 'Segment Active Image only (Do not use Folder !)', True)
IntellesisBatchDialog.AddLabel('5) Select Folder containing Images')
IntellesisBatchDialog.AddFolderBrowser('sourcedir', 'Source Folder with Images: ', imgfolder)
IntellesisBatchDialog.AddDropDown('extension', 'Image File Extension Filter', [
                                  '*.czi', '*.jpg', '*.tif', '*.tiff', '*.png', '*.ome.tiff', '*.ome.tif'], 0)

# show the window
result = IntellesisBatchDialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
modelname = str(result.GetValue('modelnames'))
sourcefolder = str(result.GetValue('sourcedir'))
segmentationformat = str(result.GetValue('segformat'))
use_conf = result.GetValue('use_confidence')
conf_th = result.GetValue('prob_threshold')
fileext = str(result.GetValue('extension'))
extract = result.GetValue('extract_class')
extract_id = int(result.GetValue('extract_class_list'))
addseg2orig = result.GetValue('addsegm')
segactiveimg = result.GetValue('segactive')
adaptpx = result.GetValue('adapt')

# get class number of select model
number_of_classes = getmodelclassnumber(modeldict[modelname])

print('Intellesis Modelname : ', modelname)
print('Model File : ', modeldict[modelname])
print('Number of Classes : ', number_of_classes)
print('Segmentation Format : ', segmentationformat)
print('Source Folder : ', sourcefolder)
print('File Extension Filter : ', fileext)
print('Use Confidence threshold : ', use_conf)
print('Confidence Threshold Value : ', conf_th)
print('Extract Class Option : ', extract)
print('Add Segmented Image to Original : ', addseg2orig)
print('Segment Active Image only : ', segactiveimg)
print('Adapt PixelType of Segmented Image : ', adaptpx)

if extract:
    if segmentationformat == 'Labels':
        message = 'Wrong Segmentation Format for Extraction selected. Must be MultiChannel.\nExit.'
        print(message)
        raise SystemExit
    print('Use Class ID : ', extract_id)

print('Add Segmentation Mask : ', addseg2orig)
print('Segment only Active Image : ', segactiveimg)

# create empty list
imagefiles = []

if not segactiveimg:
    # get list with all existing images and a short version of that list
    imagefiles = Directory.GetFiles(sourcefolder, fileext)

    if is_empty(imagefiles):
        # in case the folder contains no images with specified extension
        message = 'No images found in specified folder: '
        print(message, sourcefolder)
        raise SystemExit

    # check for existing subfolder inside source folder
    seg_subfolder = Path.Combine(sourcefolder, 'Seg')

    if Directory.Exists(seg_subfolder):
        if len(Directory.GetFiles(seg_subfolder)) != 0:
            # subfolder exist and is not empty - stop here
            message = 'Subfolder already exits and is not empty. Stopping Execution.'
            print(message, sourcefolder)
            raise SystemExit
        if len(Directory.GetFiles(seg_subfolder)) == 0:
            print('Subfolder already exists but is empty. Proceed with Segmentation.')

    if not Directory.Exists(seg_subfolder):
        # subfolder does not exist - create one
        Directory.CreateDirectory(seg_subfolder)
        print('Created subfolder for segmentation results : ', seg_subfolder)

if segactiveimg:

    if not Zen.Application.Documents.ActiveDocument.IsZenImage:
        message = 'Active Document is not a ZenImage.'
        print(message, sourcefolder)
        raise SystemExit

    if Zen.Application.Documents.ActiveDocument.IsZenImage:
        image = Zen.Application.ActiveDocument
        imagefiles.append(image.FileName)

print('-----------------------------------------------------------------------------')

# process all images inside the specified folder
for imagefile in imagefiles:

    print('Loading Image : ', imagefile)
    if not segactiveimg:
        image = Zen.Application.LoadImage(imagefile, False)
    seg_name = Path.GetFileNameWithoutExtension(image.FileName) + '_seg' + Path.GetExtension(image.FileName)
    seg_path = Path.GetDirectoryName(image.FileName)
    print('Segmenting ...')

    # check channel number
    if number_of_classes < extract_id:
        message = 'Not enough classes inside model to extract class : ', extract_id
        print(message)
        print('Number of classes in model : ', modelname, ' = ', number_of_classes)
        print('Exit.')
        raise SystemExit

    # do the pixel classification for the current image
    seg = classify(image, modelname,
                   use_confidence=use_conf,
                   confidence_threshold=conf_th,
                   format=segmentationformat,
                   extractclass=extract,
                   addseg=addseg2orig,
                   classid=extract_id)

    if not segactiveimg:
        # close the original image
        image.Close()

    if seg is not None:
        if not segactiveimg:
            # save the resulting image
            savepath = Path.Combine(seg_subfolder, seg_name)
            print('Saving segmented image : ', savepath)
            seg.Save(savepath)
            seg.Close()
        if segactiveimg:
            Zen.Application.Documents.Add(seg)

    elif seg is None:
        print('Could not segment image : ', imagefile)

print('Done.')
