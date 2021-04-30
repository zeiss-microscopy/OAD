#################################################################
# File        : Intellesis_Segmentation_Tool_adv.py
# Version     : 0.4
# Author      : czsrh, czmri
# Date        : 16.03.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Disclaimer: Use this script at your own risk.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
# ﻿

from System.IO import File, Directory, Path, SearchOption
import sys
import clr
clr.AddReference('System.Xml')
import System.Xml
from System import ApplicationException
import time

version = 0.4

#################################################################


def is_empty(any_structure):
    """Check if a "structure" might be empty

    :param any_structure: input structure
    :type any_structure: 
    :return: Boolean, depending on if the structure was empty or not
    :rtype: bool
    """
    # check is a structure is empty
    if any_structure:
        return False
    else:
        return True


def getshortfiles(filelist):
    """Create a list of files using only the basenames.

    :param filelist: list with files with complete path
    :type filelist: list
    :return: list with filename (basename) only
    :rtype: list
    """
    # get the short filenames from all list entries
    files_short = []
    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short


def getmodelname(xmldoc):
    """Get Intellesis model name from XML file

    :param xmldoc: xml modelfile document
    :type xmldoc: str
    :return: modelname
    :rtype: str
    """
    # get Intellesis modelname from XML file
    modelname = None
    nodes = xmldoc.SelectNodes('Model/ModelName')
    for node in nodes:
        modelname = node.InnerText

    return modelname


def getmodelid(xmldoc):
    """Get Intellesis model id from XML file

    :param xmldoc: xml modelfile document
    :type xmldoc: str
    :return: ID of the model
    :rtype: str
    """
    # get modelid from XML file
    modelid = None
    nodes = xmldoc.SelectNodes('Model/Id')
    for node in nodes:
        modelid = node.InnerText

    return modelid


def getmodelclassnames(modelfile):
    """Get Intellesis model class names

    :param modelfile: xml modelfile document
    :type modelfile: str
    :return: list with class names
    :rtype: list
    """
    # get name of segmentation classes from XML model file
    classnames = []
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(modelfile)
    nodes = xmldoc.SelectNodes('Model/TrainingClasses')
    for node in nodes:
        for c in node.ChildNodes:
            classnames.append(c.GetAttributeNode('Name').Value)

    return classnames


def getmodel_validchannels(modelfile):
    """Get information about the valid channels for a model

    :param modelfile: model file
    :type modelfile: str
    :return: [description]
    :rtype: [type]
    """
    # get modelid from XML model file
    valid_channels = []
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(modelfile)
    nodes = xmldoc.SelectNodes('Model/Channels')
    for node in nodes:
        for c in node.ChildNodes:
            valid_channels.append(c.GetAttributeNode('PixelType').Value)

    return valid_channels, len(valid_channels)


def getmodelclassnumber(modelfile):
    """Get the number of classes from a modelfile

    :param modelfile: modelfile
    :type modelfile: str
    :return: number of classes for that model
    :rtype: int
    """
    # get number of classes del from XML model file
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(modelfile)
    nodes = xmldoc.SelectNodes('Model/TrainingClasses')
    for node in nodes:
        numclasses = node.ChildNodes.Count

    return numclasses


def cleanup_dict(dc, clean_key=None, clean_value=None):
    """Cleanup a dictionary from invalid entries

    :param dc: dictionary to be cleaned
    :type dc: dict
    :return: cleaned dictionary
    :rtype: dict
    """

    # clean dictionary incase there are invalid values
    filtered = {k: v for k, v in dc.items() if k is not clean_key}
    dc.clear()
    dc.update(filtered)

    filtered = {k: v for k, v in dc.items() if v is not clean_value}
    dc.clear()
    dc.update(filtered)

    return dc


def runmodel(image, model,
             use_confidence=False,
             confidence_threshold=0,
             format='MultiChannel',
             extractclass=False,
             class2extract_id=0,
             addseg=False,
             adapt_pixeltype=True):
    """This function classifies the pixels inside an ZenImage using an Intellesis segmentation model

    :param image: Image to be segmented
    :type image: ZenImage
    :param model: Name of the Intellesis Segmentation model without file extention
    :type model: str
    :param use_confidence: Use confidence threshold to filter segmented pixels, defaults to False
    :type use_confidence: bool, optional
    :param confidence_threshold: threshold value for the confidence, defaults to 0
    :type confidence_threshold: inFormat of segmentation output, defaults to 'MultiChannel'
    :type format: str, optional
    :param extractclass: Option to extract a class from segmentation result, defaults to False
    :type extractclass: bool, optional
    :param class2extract_id: Id of the class to be extracted, defaults to 0
    :type class2extract_id: int, optional
    :param addseg: Option to add the segmentation result as additional channels
    to the original image, defaults to False
    :type addseg: bool, optional
    :param adapt_pixeltype: Adpapt the pixel type of the added segmentation results
    to match the one of the original input image, defaults to True
    :type adapt_pixeltype: bool, optional
    :return: segmented image or original image with added segmentation results
    :rtype: ZenImage
    """

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
        # create subset string and extract the respective channel
        substr = 'C(' + str(class2extract_id + 1) + ')'
        print('Use SubsetString : ', substr)
        seg_image = Zen.Processing.Utilities.CreateSubset(seg_image, substr, False)

    if addseg:
        # add segmentation output to the original image as an additional channel
        print('Add Segmentation output as new channel to image.')
        seg_image = Zen.Processing.Utilities.AddChannels(image, seg_image)

    return seg_image


def get_channelnames(image):
    """Get names of the channels from an image

    :param image: input image
    :type image: ZenImage
    :return: list with channel names
    :rtype: list
    """
    # get the channelnames as a list
    channelnames = []

    # get the number of channels
    numch = image.Bounds.SizeC

    for ch in range(numch):
        channelnames.append(image.Metadata.GetChannelName(ch))

    return channelnames, numch


def createidstr(maxclass):
    """Create a list contains the ids for the classes

    :param maxclass: maximum number of classes
    :type maxclass: int
    :return: list with id strings
    :rtype: list
    """

    classstr = []
    for i in range(1, maxclass + 1):
        classstr.append(str(i))

    return classstr


##############################################################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

CZIfiles_short = []
CZIdict = {}

# get all open documents from ZEN
opendocs = Zen.Application.Documents

for doc in opendocs:
    # check if document is an image
    if isinstance(doc, ZenImage):

        # get the filename of the current document
        CZIfiles_short.append(Path.GetFileName(doc.FileName))
        CZIdict[Path.GetFileName(doc.FileName)] = doc.FileName

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
IntellesisSegTool = ZenWindow()
IntellesisSegTool.Initialize('Intellesis Segmentation Tool - Version: ' + str(version))
# add components to dialog
IntellesisSegTool.AddDropDown('czi', 'Select CZI Image Document', CZIfiles_short, 0)
IntellesisSegTool.AddDropDown('modelnames', 'Intellesis Model', modelnames_short, 0)
IntellesisSegTool.AddDropDown('segformat', 'SegmentationFormat Output', ['MultiChannel', 'Labels'], 0)
IntellesisSegTool.AddCheckbox('use_confidence', 'Use Confidence Threshold', False)
IntellesisSegTool.AddIntegerRange('prob_threshold', 'Specify Confidence Threshold for Classification', 51, 0, 99)
IntellesisSegTool.AddCheckbox('extract_class', 'Extract (requires MultiChannel as Output Format)', True)
IntellesisSegTool.AddCheckbox('addsegm', 'Add Segmentation Mask to Original Image', False)

# show the window
result = IntellesisSegTool.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
cziname = result.GetValue('czi')
czidocument = CZIdict[cziname]
modelname = str(result.GetValue('modelnames'))
segmentationformat = str(result.GetValue('segformat'))
use_conf = result.GetValue('use_confidence')
conf_th = result.GetValue('prob_threshold')
fileext = str(result.GetValue('extension'))
extract = result.GetValue('extract_class')
addseg2orig = result.GetValue('addsegm')

# get class number of select model
number_of_classes = getmodelclassnumber(modeldict[modelname])
valid_channels, num_valid_channels = getmodel_validchannels(modeldict[modelname])

# get name of classes
classnames = getmodelclassnames(modeldict[modelname])
print('Detected Class Names : ', classnames)

# get the active image document
image = Zen.Application.Documents.GetByName(cziname)
Zen.Application.Documents.ActiveDocument = image

# get channel information from image
chnames, numch = get_channelnames(image)
chnames.append('All Channels')

if extract and segmentationformat == 'MultiChannel':

    # initialize Dialog
    IntellesisClassSelector = ZenWindow()
    IntellesisClassSelector.Initialize('Intellesis Class and Channel Selection - Version: ' + str(version))
    IntellesisClassSelector.AddLabel('1) --- Define Class to extract ---')
    IntellesisClassSelector.AddLabel('Model : ' + modelname)
    IntellesisClassSelector.AddLabel('Required Channel Number : ' + str(num_valid_channels))
    IntellesisClassSelector.AddDropDown('extract_classname', 'Select Class Name', classnames, 0)

    if numch > 1:
        IntellesisClassSelector.AddLabel('2) --- Define Channel to be Segmented ---')
        IntellesisClassSelector.AddCheckbox('apply2single', 'Apply to single channel', True)
        IntellesisClassSelector.AddDropDown('ch2segment', 'Select Channel to be segmented', chnames, 0)

    # show the window
    cs_result = IntellesisClassSelector.Show()
    if cs_result.HasCanceled:
        message = 'Macro was canceled by user.'
        print(message)
        raise SystemExit

    class2extract = cs_result.GetValue('extract_classname')
    # get the Channel ID from Class (to be extracted)
    class2extract_id = classnames.IndexOf(class2extract)
    apply2ch = cs_result.GetValue('apply2single')
    ch2seg = cs_result.GetValue('ch2segment')

if not extract:
    class2extract_id = None

print('CZI Image Document : ', cziname)
print('Intellesis Modelname : ', modelname)
print('Model File : ', modeldict[modelname])
print('Number of Classes : ', number_of_classes)
print('Segmentation Format : ', segmentationformat)
print('Use Confidence threshold : ', use_conf)
print('Confidence Threshold Value : ', conf_th)
print('Add Segmented Image to Original : ', addseg2orig)
print('Extract Class Option : ', extract)

if extract:
    print('Detected Class Names : ', classnames)
    print('Extract Class    : ', class2extract)
    print('Channel ID of Class : ', class2extract_id)

if apply2ch:
    print('Apply to single Channel : ', apply2ch)
    print('Selected Image Channel  : ', ch2seg)

if extract:
    if segmentationformat == 'Labels':
        message = r'Wrong Segmentation Format for Extraction selected. Must be MultiChannel.\nExit.'
        print(message)
        raise SystemExit
    # print 'Use Class Name : ', extract

print('-----------------------------------------------------------------------------')

# process the image
seg_name = Path.GetFileNameWithoutExtension(image.FileName) + '_seg' + Path.GetExtension(image.FileName)
seg_path = Path.GetDirectoryName(image.FileName)

# if a single needs to be extracted
if apply2ch:
    # create substring
    print('Extract Channel before Segmentation: ', ch2seg)
    ch_id = chnames.IndexOf(ch2seg)
    substr = 'C(' + str(ch_id + 1) + ')'
    image = seg_image = Zen.Processing.Utilities.CreateSubset(image, substr, False)

# do the pixel classification for the current image
print('Starting - Loading / Init model might take a while ...')
start = time.clock()

# run the actual model
seg = runmodel(image, modelname,
               use_confidence=use_conf,
               confidence_threshold=conf_th,
               format=segmentationformat,
               extractclass=extract,
               class2extract_id=class2extract_id,
               addseg=addseg2orig,
               adapt_pixeltype=True)

end = time.clock()
print(r'Total Time (Start Service + Load / Init model + Processing ) : ', str(round(end - start, 0)))

if seg is not None:
    Zen.Application.Documents.Add(seg)

elif seg is None:
    print('Could not segment image : ', czidocument)

print('Done.')
