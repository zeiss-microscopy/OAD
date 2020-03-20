#################################################################
# File       : Intellesis_CampareTwoFeatureExtractors_UI.py
# Version    : 0.2
# Author     : czmri, czsrh
# Date       : 19.08.2019
# Insitution : Carl Zeiss Microscopy GmbH
#
# !!! Requires with ZEN >=3.1 - Use at your own Risk !!!
#
# Description: Trains an existing model with various feature sets and compares
#              the segmentation results.
# Hint:        Use the 'Weight' slider in the channel color popup to control
#              segmentation opacity.
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

version = 0.1

import System
from System.IO import Path, File, Directory, FileInfo
from System import Array, String
from System import ApplicationException


def compute_segmentation(input, model, fe, pp):
    """ Trains a new model and computes a segmentation of the specified image
    and feature set. The training data and other settings are copied from the
    specified model.
    The model itself is not modified.
    The segmentation result is returned.

    Arguments:
        input: ZenImage
            The image to segment.
        model: IZenIntellesisModel
            The model from with training data and other settings are taken.
        fe: list of string
            The feature set for which to compute a segmentation.
        pp: list of string
            The feature set for which to compute a segmentation.

     Returns: ZenImage
        The segmentation image in Labels format.
    """
    output = input.Clone()
    try:
        output.Name = fe
        new_model = model.TrainCopy("(temp) " + fe,
                                    featureSet=fe,
                                    postProcessing=pp)
        try:
            # only labels make "sense" here because this allows adding as single channel 
            result = new_model.Segment(output, ZenSegmentationFormat.Labels)
            try:
                output.AddChannel(result[0], fe)
            finally:
                result[0].Close()
                result[1].Close()
        finally:
            new_model.Delete()

        return output
    except:
        output.Close()
        raise


def compare_many(multi_name, item_names):
    """ Compares two or more opened images in a new ZenMultiImageDocument.
    If an old document with the same name exists it is closed.

    Arguments:
        multi_name: string
            The name of the ZenMultiImageDocument.
        item_names: iterable of string
            The names of the images to compare.
    """
    name = multi_name
    multi = Zen.Application.Documents.GetByName(name)
    if multi is not None:
        Zen.Application.Documents.Remove(multi, False)
        multi.Close()
    multi = ZenMultiImageDocument()
    multi.Core.Name = multi_name
    for fe in item_names:
        doc_m = Zen.Application.Documents.GetByName(fe)
        if doc_m is not None:
            multi.AddDocument(doc_m)

    Zen.Application.Documents.Add(multi)


def find_model(name):
    """ Finds a model given its Name.

    Arguments:
        name: string
            The name of the model to look for.

    Returns: IZenIntellesisModel
        The first model with the specified name
        or None, if no such model exists.
    """
    models = ZenIntellesis.ListAvailableSegmentationModels()
    return next((m for m in models if m.Name == name), None)


def create_subset(image, subsetstring):

    try:
        subset = Zen.Processing.Utilities.CreateSubset(image, subsetstring)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
        raise SystemExit
        
    return subset


##############################################################

CZIfiles_short = []
CZIdict = {}
# get all open documents
opendocs = Zen.Application.Documents
for doc in opendocs:
    image = Zen.Application.Documents.GetByName(doc.Name)
    for ext in ['.czi', '.png', '.tiff', '.tif', 'ome.tiff', '.ome.tif']:
        if image.FileName.EndsWith(ext):
            # get the filename of the current document only when it ends with '.czi'
            CZIfiles_short.append(Path.GetFileName(image.FileName))
            CZIdict[Path.GetFileName(image.FileName)] = image.FileName

# get available models
segmodels_list = []
segdict = {}
all_segmodels = ZenIntellesis.ListAvailableSegmentationModels()
for sm in all_segmodels:
    #print 'Model : ', sm
    segmodels_list.append(sm.Name)
    segdict[sm.Name] = sm
    
# sort list for nicer dropdown menu later in dialog window
segmodels_list.sort(key=str.lower)

# get availbale feature extractors
feature_extractor_list = []
fex_dict = {}
all_feature_sets = ZenIntellesis.GetAvailableFeatureSets()
for fs in  all_feature_sets:
    feature_extractor_list.append(fs)
    fex_dict[fs] = fs

# get available postprocessings
postprocessing_list = []
postp_dict = {}
all_postprocessings = ZenIntellesis.GetAvailablePostProcessings()
for ps in all_postprocessings:
    postprocessing_list.append(ps)
    postp_dict[ps] = ps

# initialize Dialog
SelectDialog = ZenWindow()
SelectDialog.Initialize('Intellesis Model Compare - Version: ' + str(version))
# add components to dialog

SelectDialog.AddDropDown('imagedoc', 'Select Open CZI Image Document', CZIfiles_short, 0)
SelectDialog.AddDropDown('segm', 'Segmentation Model', segmodels_list, 0)
SelectDialog.AddDropDown('fex1', 'Feature Extractor 1', feature_extractor_list, 0)
SelectDialog.AddDropDown('pps1', 'Post-Processing 1', postprocessing_list, 0)
SelectDialog.AddDropDown('fex2', 'Feature Extractor 2', feature_extractor_list, 1)
SelectDialog.AddDropDown('pps2', 'Post-Processing 2', postprocessing_list, 0)
SelectDialog.AddCheckbox('usesub', 'Use Substring', True)
SelectDialog.AddTextBox('subsetstring', 'Define Subset String', 'T(1)')

# show the window
result = SelectDialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

imagename = result.GetValue('imagedoc')
model_name = result.GetValue('segm')
feature_ex1 = result.GetValue('fex1')
feature_ex2 = result.GetValue('fex2')
postprocess1 = result.GetValue('pps1')
postprocess2 = result.GetValue('pps2')
use_subset = result.GetValue('usesub')
subsetstring = result.GetValue('subsetstring')

print 'Active Image        : ', imagename
print 'Model Name          : ', model_name
print 'Feature Extractor 1 : ', feature_ex1
print 'Post processing 1   : ', postprocess1
print 'Feature Extractor 2 : ', feature_ex2
print 'Post Processing 2   : ', postprocess2
if use_subset:
    print 'Subset String       : ', subsetstring

# get the select image as an ZenImage
image2seg = Zen.Application.Documents.GetByName(imagename)

# get all feature extractors as System.String array.
all_feature_sets = ZenIntellesis.GetAvailableFeatureSets()

# create a normal python list
all_feature_sets_list = list(all_feature_sets)

# create lits with feature extractors and postprocessings
feature_sets = []
feature_sets.append(fex_dict[feature_ex1])
feature_sets.append(fex_dict[feature_ex2])

postprocessings = []
postprocessings.append(postprocess1)
postprocessings.append(postprocess2)


def main():
    """ The main routine. """
    model = find_model(model_name)
    if model is None:
        model = ZenIntellesis.ImportModel(model_path)
    
    if use_subset:
        # create the image subset
        if subsetstring != '':
            print 'Creating Subset ...'
            input = create_subset(image2seg, subsetstring)
        else:
            print 'No Subset String specified. Using full image.'
            input = image2seg
            
    if not use_subset:
        input = image2seg
    
    segout = []
    segout_names = []
    
    # run segmentation for every feature extractor + postprocessings
    for r in range(len(feature_sets)):
        
        print 'Running Segmentation: ', feature_sets[r], ' + ',postprocessings[r]
        
        # calculate the segmenation using the correct options
        tmp = compute_segmentation(input, model, feature_sets[r], postprocessings[r])
        
        # create a new name
        tmp.Name = tmp.Name + '_' + str(r+1)
        print 'New Name : ', tmp.Name
        segout.append(tmp)
        segout_names.append(tmp.Name)
        
        # show the segmentation for the current option
        Zen.Application.Documents.Add(tmp)
    
    # show both results inside multiview document
    compare_many('FeatureExtractor - Comparison', segout_names)

    print 'Done.'

main()
