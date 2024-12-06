#################################################################
# File       : Segment_and_and_Cutout_Masks.py
# Version    : 0.1
# Author     : czsrh
# Date       : 26.11.2019
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


import time
from datetime import datetime
import errno
from System import ApplicationException
from System.IO import File, Directory, Path
import sys

version = 0.2

# clear output
Zen.Application.MacroEditor.ClearMessages()

thdict = {'Otsu' : ZenThresholdingMethod.Otsu,
          'Triangle' : ZenThresholdingMethod.TriangleThreshold,
          'IsoData' : ZenThresholdingMethod.IsoData,
          'MaximumPeak' : ZenThresholdingMethod.MaximumPeak,
          'ThreeSigma' : ZenThresholdingMethod.ThreeSigmaThreshold
          }
          
thlist = ['Otsu', 'Triangle', 'IsoData', 'MaximumPeak', 'ThreeSigma']

##########################################################################################

CZIfiles_short = []
CZIdict = {}

# get all open documents
opendocs = Zen.Application.Documents
for doc in opendocs:
    image = Zen.Application.Documents.GetByName(doc.Name)
    
    if image.FileName.EndsWith('.czi'):
        # get the filename of the current document only when it ends with '.czi'
        CZIfiles_short.append(Path.GetFileName(image.FileName))
        CZIdict[Path.GetFileName(image.FileName)] = image.FileName

# create simple dialog
wd = ZenWindow()
wd.Initialize('Segment and Cutout Masks - Version : ' + str(version))
wd.AddLabel('---   Select Image to process from open documents  ---')
wd.AddDropDown('czi', 'Select CZI Image Document', CZIfiles_short, 0)
wd.AddCheckbox('useCORR', 'Correct illumination', True)
wd.AddCheckbox('useRBsub', 'Use RollingBall Background Substraction', True)
wd.AddCheckbox('useFilter', 'Apply Filtering', True)
wd.AddLabel('---   Select Thresholding Method   ---')
wd.AddDropDown('thmethod', 'Algorithm', thlist, 0)
wd.AddCheckbox('lightbgrd', 'Light Background', False)
wd.AddLabel('--------------------------------------')
wd.AddCheckbox('useRemove', 'Remove small Objects', True)
wd.AddCheckbox('useFill', 'Fill Holes', True)
wd.AddCheckbox('useSeparate', 'Separate Binary Objects', True)

# show the window
result=wd.Show()

# check, if Cancel button was clicked
if result.HasCanceled == True:
    sys.exit('Macro aborted with Cancel!')
    
# get the input values and store them
cziname = result.GetValue('czi')
czidocument = CZIdict[cziname]
useRB = result.GetValue('useRBsub')
useFT = result.GetValue('useFilter')
removeOB = result.GetValue('useRemove')
fillHoles = result.GetValue('useFill')
separateOB = result.GetValue('useSeparate')
thm = result.GetValue('thmethod')
useCR = result.GetValue('useCORR')
lbg = result.GetValue('lightbgrd')

# get the correct thrsehold method
th_method = thdict[thm]
print(th_method)

# get the active image document
img_orig = Zen.Application.Documents.GetByName(cziname)
img = Zen.Application.Documents.GetByName(cziname)
Zen.Application.Documents.ActiveDocument = img

"""
Usage Instructions

!!! Check the script parameters carefully and adapt it to your image !!!

- Select on active image from the Zen
- Comment out processing steps that are not needed
- Feel free to re-arrange the order of processing steps
- Add new proceesing steps as needed

"""

if useCR:
    # correct uneven illumination
    print('Correct for uneven illumination ...')
    lowpasscount = 3
    lp_kernelsize = 300
    norm = ZenNormalizeMode.Auto
    # create the background using a lowpass with a large kernel size
    lowpass = Zen.Processing.Filter.Smooth.Lowpass(img, lowpasscount, lp_kernelsize, False)
    # substract the background from the original image
    img = Zen.Processing.Arithmetics.Subtraction(img, lowpass, norm, False)

if useRB:
    # apply background subtraction
    print('Applying RollingBall Background Substraction ...')
    rb_radius = 50
    isLightBackground=False
    img = Zen.Processing.Adjust.BackgroundSubtraction(img, rb_radius, doPreSmooth=False, createBackground=False, isLightBackground=False)

if useFT:
    # apply filter
    print('Applying Filtering ...')
    median_radius = 3
    img = Zen.Processing.Filter.Smooth.Median(img, median_radius, False)

# apply threshold
print('Applying Automated Thresholding ...')
#th_method = ZenThresholdingMethod.Otsu
createBinary = True
invertResult = lbg
print('Invert result : ', invertResult)
img = Zen.Processing.Segmentation.ThresholdAutomatic(img, th_method, createBinary, invertResult, False)

if removeOB:
    # remove small objects
    print('Removing small objects ...')
    minarea = 1 
    maxarea = 100000000
    inrange = True
    img = Zen.Processing.Binary.Scrap(img, minarea, maxarea, inrange, False)

if fillHoles:
    # fill holes
    print('Fill Holes ...')
    img = Zen.Processing.Binary.FillHoles(img)

if separateOB:
    # separate objects
    print('Trying to separate objects ...')
    sep_kernel = 5
    sep_method = ZenSeparationModes.Watersheds
    img = Zen.Processing.Binary.Separation(img, sep_method, sep_kernel, False)

# cutout image by using the binary mask as a template on the original image
print('Using binary mask to cutout regions from original image ...')
img = Zen.Processing.Binary.ApplyMask(img_orig, img, False)

# change name
img.Name = Path.GetFileNameWithoutExtension(img_orig.FileName) + '_masked.czi'

# show result in ZEN
Zen.Application.Documents.Add(img)

print('Done.')
