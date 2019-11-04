#################################################################
# File       : ZEN_Intellesis_Simple_Test.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

"""
Very simple test script to demonstrate the segmentation
functionality of the Intellesis segmentation module

"""

from System.IO import File, Path, Directory
from System import ApplicationException

# clear output console
Zen.Application.MacroEditor.ClearMessages()

modelfolder = r'c:\models'
imagefolder = r'c:\images'

# define model and image to load
modelname = 'XRM_Sandstone_Default_Features_Demo'
modelfile = Path.Combine(modelfolder, modelname + '.czmodel')
imagefile = Path.Combine(imagefolder, 'XRM_Testimage.czi')

print 'Model Name : ', modelname
print 'Modelfile  : ', modelfile
print 'Imagefile  : ', imagefile

# load and show image
image = Zen.Application.LoadImage(imagefile, False)
Zen.Application.Documents.Add(image)

##### ZEN Blue 3.1 code - BEGIN ########

# import new model - this will only work for ZEN Blue 3.1
available_models = ZenIntellesis.ListAvailableSegmentationModels()
model_exists = False

for m in available_models:
    if m.Name == modelname:
        print 'Model : ', modelname, ' already exists.'
        model_exists = True
        break

if not model_exists:
    ZenIntellesis.ImportModel(modelfile, False)

##### ZEN Blue 3.1 code - END ########

# classify pixels - default output is MultiChannel format
seg_opt_default = Zen.Processing.Segmentation.TrainableSegmentation(image, modelname)
seg_opt_default.Name = 'Segmented_Default'
Zen.Application.Documents.Add(seg_opt_default)

# classify pixels - option with optional specified output format: MultiChannel
seg_opt_multich = Zen.Processing.Segmentation.TrainableSegmentation(image, modelname, ZenSegmentationFormat.MultiChannel)
seg_opt_multich.Name = 'Segmented_Option_MultiCH'
Zen.Application.Documents.Add(seg_opt_multich)

# classify pixels - option with specified output format: Labels
seg_opt_label = Zen.Processing.Segmentation.TrainableSegmentation(image, modelname, ZenSegmentationFormat.Labels)
seg_opt_label.Name = 'Segmented_Option_Labels'
Zen.Application.Documents.Add(seg_opt_label)

# classify pixels - option with specified output format: MultiChannel
# run the segmentation and apply probability threshold to segmented image
probability_threshold = 95  # confidence threshold for classifier[0 - 100]
outputs = Zen.Processing.Segmentation.TrainableSegmentationWithProbabilityMap(image, modelname, ZenSegmentationFormat.MultiChannel)
seg_opt_prob = outputs[0]
prob_map = outputs[1]
seg_opt_prob_th = Zen.Processing.Segmentation.MinimumConfidence(seg_opt_prob, prob_map, probability_threshold)
Zen.Application.Documents.Add(seg_opt_prob_th)
seg_opt_prob_th.Name = 'Segmented_Option_Probability_Threshold'
Zen.Application.Documents.Add(prob_map)
prob_map.Name = 'Segmented_Option_ProbabilityMap'

print 'Done.'
