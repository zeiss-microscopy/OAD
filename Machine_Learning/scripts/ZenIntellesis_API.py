#################################################################
# File       : ZenIntellesis_API.py
# Version    : 0.1
# Author     : czsrh
# Date       : 03.11.2019
# Institution : Carl Zeiss Microscopy GmbH
#
# Very simple test script to demonstrate the segmentation
# functionality of the Intellesis segmentation module
#
# !!! Requires ZEN Blue 3.1 or better
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

Zen.Application.MacroEditor.ClearMessages()

modelname = 'Grains_MET101'

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


model = find_model(modelname)

Zen.Application.MacroEditor.ClearMessages()

print 'Modelname : ', model.Name
print 'Model Status : ', model.Status
print model.Description

training_images = model.TrainingImages
for ti in training_images:
    print ti


# All feature extractors.
all_feature_sets = ZenIntellesis.GetAvailableFeatureSets()
for fs in  all_feature_sets:
    print fs

# all postprocessings
all_postprocessings = ZenIntellesis.GetAvailablePostProcessings()
for ps in all_postprocessings:
    print ps

