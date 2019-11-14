#################################################################
# File       : Intellesis_Segmentation_Tool_singleCH.py
# Version    : 0.2
# Author     : czsrh
# Date       : 25.03.2019
# Insitution : Carl Zeiss Microscopy GmbH
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

version = 0.2


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


def getclassnames(modelfile):

    classnames = []
    classnamedict = {}

    # get name of classes of model from XML model file
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(modelfile)
    nodes = xmldoc.SelectNodes('Model/TrainingClasses')
    for node in nodes:
        count = 0
        for n in node.GetEnumerator():
            classnames.append(n.GetAttribute('Name'))
            classnamedict[n.GetAttribute('Name')] = count
            count = count + 1

    return classnames, classnamedict


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
            prop_map = outputs[1]
            print 'Apply Confidence Threshold to segmented image.'
            seg_image = Zen.Processing.Segmentation.MinimumConfidence(seg_image, prop_map, confidence_threshold)
            prop_map.Close()
            del outputs
        except ApplicationException as e:
            seg_image = None
            print 'Application Exception : ', e.Message

    if not use_confidence:
        try:
            # run the segmentation
            seg_image = Zen.Processing.Segmentation.TrainableSegmentation(image, model, segf)
        except ApplicationException as e:
            seg_image = None
            print 'Application Exception : ', e.Message

    if adapt_pixeltype:
        # adapt the pixeltype to match the type of the original image
        pxtype = image.Metadata.PixelType
        seg_image = Zen.Processing.Utilities.ChangePixelType(seg_image, pxtype)
        print 'New PixelTyper for Segmented Image : ', seg_image.Metadata.PixelType

    if extractclass:
        # create subset string
        print 'Extracting segmented class form Segmentation Output ...'
        substr = 'C(' + str(classid) + ')'
        seg_image = Zen.Processing.Utilities.CreateSubset(seg_image, substr, False)

    if addseg:
        # add original and segmentation
        print 'Adding segmented mask to the input image ...'
        seg_image = Zen.Processing.Utilities.AddChannels(image, seg_image)

    return seg_image


##############################################################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

# check the location of folder where experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
# or you your own default folder
imgfolder = r'c:\Output\Intellesis_Batch_Test'

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

if not Zen.Application.Documents.ActiveDocument.IsZenImage:
    message = 'Active Document is not a ZenImage.'
    print message, sourcefolder
    raise SystemExit

if Zen.Application.Documents.ActiveDocument.IsZenImage:
    activeimage = Zen.Application.ActiveDocument
    activeimagefilename = activeimage.FileName
    activeimagename = activeimage.Name

numCH = int(activeimage.Metadata.ChannelCount)

# create dictionary with channel names
chnames = []
chdict = {}

for ch in range(numCH):
    chnames.append(activeimage.Metadata.GetChannelName(ch))
    chdict[activeimage.Metadata.GetChannelName(ch)] = ch + 1

# initialize Dialog
SelectDialog = ZenWindow()
SelectDialog.Initialize('Intellesis Segment Single Channel - Version: ' + str(version))
# add components to dialog
SelectDialog.AddLabel('1) Select Channel to be segmented')
SelectDialog.AddDropDown('channels', 'Channel Names', chnames, 1)
SelectDialog.AddLabel('2) Select Intellesis Single Channel Model for Segmentation')
SelectDialog.AddDropDown('modelnames', 'Model Names', modelnames_short, 0)

# show the window
resultch = SelectDialog.Show()
if resultch.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
modelname = str(resultch.GetValue('modelnames'))
channelname = str(resultch.GetValue('channels'))

print 'Selected Channel Name :', channelname
print 'Intellesis Modelname : ', modelname
print 'Model File : ', modeldict[modelname]

# create list of classes from selected model
classnames, classdict = getclassnames(modeldict[modelname])

# initialize Dialog
IntellesisDialog = ZenWindow()
IntellesisDialog.Initialize('Intellesis Segment Single Channel - Version: ' + str(version))
# add components to dialog
IntellesisDialog.AddLabel('1) Confidence Treshold Option')
IntellesisDialog.AddCheckbox('use_confidence', 'Use Confidence Threshold', False)
IntellesisDialog.AddIntegerRange('conf_threshold', 'Specify Confidence Threshold for Classification', 51, 51, 99)
IntellesisDialog.AddLabel('2) Select Class from Model')
IntellesisDialog.AddDropDown('extract_classname', 'Select Classname', classnames, 0)
IntellesisDialog.AddLabel('3) Additional Tools')
IntellesisDialog.AddCheckbox('addsegm', 'Add Segmentation Mask to Original Image', False)
IntellesisDialog.AddCheckbox('adapt', 'Adapt PixelType of Segmented Mask to match Original Image', True)

# show the window
result = IntellesisDialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
segmentationformat = 'MultiChannel'
use_conf = result.GetValue('use_confidence')
conf_th = result.GetValue('conf_threshold')
classname = result.GetValue('extract_classname')
extract_id = classdict[classname]
extract = True
addseg2orig = result.GetValue('addsegm')
adaptpx = result.GetValue('adapt')

print 'Selected Classname : ', classname
print 'ClassID : ', extract_id
print 'Use Confidence threshold : ', use_conf
print 'Confidence Threshold Value : ', conf_th
print 'Add Segmented Image to Original : ', addseg2orig
print 'Adapt PixelType of Segmented Image : ', adaptpx
print '-----------------------------------------------------------------------------'
print 'Segmenting ...'

# extract select channel from active image
substr = 'C(' + str(chdict[channelname]) + ')'
image = Zen.Processing.Utilities.CreateSubset(activeimage, substr, False)

# do the pixel classification for the current image
seg = classify(image, modelname,
               use_confidence=use_conf,
               confidence_threshold=conf_th,
               format=segmentationformat,
               extractclass=extract,
               addseg=False,
               classid=extract_id + 1,
               adapt_pixeltype=adaptpx)

if addseg2orig:
    # add segmentation result to the original image
    orig_seg = Zen.Processing.Utilities.AddChannels(activeimage, seg)
    Zen.Application.Documents.Add(orig_seg)
    seg_name = Path.GetFileNameWithoutExtension(activeimagefilename) + '_seg' + Path.GetExtension(activeimagefilename)
    orig_seg.Name = seg_name

print 'Done.'
