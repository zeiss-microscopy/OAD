#################################################################
# File        : LLS7_ZStacksOfYStacks.py
# Version     : 1.2
# Author      : aukelgas
# Date        : 29.11.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Use at your own Risk !!!
# Compatible with ZEN versions 3.4 and 3.5
#
# Copyright(c) 2022 Carl Zeiss Microscopy GmbH, Jena, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#
# v1.1 adds capabilities to do more than 9 volume stacks without loosing the correct order of stacks (max 20 stacks)
#
# v1.1 adds capabilities to change 'Focus Sheet' with imaging depths, the user can set 'Focus Sheet'
# close to the cover slip and at the deepest position in the sample, that they want to image and the macro
# will do a linear interpolation and modify 'Focus Sheet' automatically wih imaging depth
#
# v1.2 asks the user to move to and focus @ coverslip and @ depth and automatically reads z positions and Focus Sheet values from those positions
#
# v1.2 reads Scanner Offset y value from calibration files, user just has to select the active MTB, which should be selected correctly automatically based on it being the last modified MTB
#
# v1.2 automatically calculates the number of stacks required from camera ROI, overlap and distance between coverslip and depth positions specified by the user
#
# v1.2 takes the active experiment setup (and potential unsaved changes) rather than letting the user choose from existing experiment setups in a dropdown menu
#
################################################################

import time
from datetime import datetime
import errno
from System import Array
from System import ApplicationException
from System import TimeoutException
from System.IO import File, Directory, Path
from xml.dom import minidom
import sys
import os

# version number for dialog window
version = 1.2

# delay for specific hardware movements in [seconds]
hwdelay = 1


def dircheck(basefolder):

    # check if the destination basefolder exists
    base_exists = Directory.Exists(basefolder)

    if base_exists:
        print('Selected Directory Exists: ', base_exists)

        # specify the desired output format for the folder, e.g. 2017-08-08_17-47-41
        format = '%Y-%m-%d_%H-%M-%S'

        # create the new directory
        newdir = createfolder(basefolder, formatstring=format)
        print('Created new directory: ', newdir)

    if not base_exists:
        Directory.CreateDirectory(basefolder)
        newdir = basefolder

    return newdir


def createfolder(basedir, formatstring='%Y-%m-%d_%H-%M-%S'):

    # construct new directory name based on date and time
    newdir = Path.Combine(basedir, datetime.now().strftime(formatstring))

    # check if the new directory (for whatever reasons) already exists
    try:
        newdir_exists = Directory.Exists(newdir)

        if not newdir_exists:
            # create new directory if is does not exist
            Directory.CreateDirectory(newdir)

        if newdir_exists:
            # raise error if it really already exists
            raise SystemExit

    except OSError as e:
        if e.errno != errno.EEXIST:
            newdir = None
            raise  # This was not a "directory exist" error..

    return newdir


def getshortfiles(filelist):
    files_short = []

    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short


def cloneexp(expname, prefix='ZSYS_', save=True, reloadexp=True):

    exp = Zen.Acquisition.Experiments.GetByName(expname)
    exp_newname = prefix + expname

    # save experiment
    if save:
        exp.SaveAs(exp_newname, False)
        print('Saved Temporay Experiment as : ', exp_newname)

        # close the original experiment object
        exp.Close()
        time.sleep(1)

    # reload experiment
    if reloadexp:
        exp_reload = Zen.Acquisition.Experiments.GetByName(exp_newname)
    elif not reloadexp:
        exp_reload = None

    return exp_reload

###########################################################################


# clear console output
Zen.Application.MacroEditor.ClearMessages()

# Get list of MTBs on the system
dir = 'C:/ProgramData/Carl Zeiss/MTB2011'
MTBs = Directory.GetDirectories(dir)
MTBs_short = getshortfiles(MTBs)
print("MTBs detected: " + str(MTBs_short))

# Get active MTB
activeMTB = max(MTBs, key=os.path.getmtime)
activeMTB = os.path.basename(activeMTB)
ind = MTBs_short.index(activeMTB)

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
format = '%Y-%m-%d_%H-%M-%S'

# get list with all existing experiments and image analysis setup and a short version of that list
expfiles = Directory.GetFiles(Path.Combine(docfolder, 'Experiment Setups'), '*.czexp')
expfiles_short = getshortfiles(expfiles)

# Initialize Dialog
Dialog = ZenWindow()
Dialog.Initialize('YStackTiling - Version : ' + str(version))

# add components to dialog
Dialog.AddLabel('1) Select overlap in Percent -------------------------------')
Dialog.AddIntegerRange('overlap', 'Overlap', 0, 0, 100)
Dialog.AddLabel('2) Active MTB-----------------------------------------------')
Dialog.AddDropDown('activeMTB', 'Active MTB', MTBs_short, ind)
Dialog.AddLabel('3) Specify folder to save the images -----------------------')
Dialog.AddFolderBrowser('outfolder', 'Folder for Stack Images', imgfolder)

# show the window
result = Dialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
OutputFolder = str(result.GetValue('outfolder'))
Overlap = result.GetValue('overlap')
activeMTB = result.GetValue('activeMTB')
print("Active MTB: " + str(activeMTB))

# Get Lattice Lightsheet used
hw = Zen.Devices.ReadHardwareSetting()
ls = hw.GetParameter('MTBMuSPIMSLM', 'Position')
lsname = hw.GetParameter('MTBMuSPIMSLM', 'PositionName')
print(lsname)

# Get Scanner Offset y for respective Lightsheet
xmlfile = 'C:/ProgramData/Carl Zeiss/MTB2011/' + activeMTB + '/CalibrationFiles/MuSPIM/SLM/MTBMuSPIMSLM.xml'
print(xmlfile)
xmldoc = minidom.parse(xmlfile)
itemlist = xmldoc.getElementsByTagName('CalibrationUniqueDataValue')
ScannerOffsetYCal = float(itemlist[int(ls) * 3 - 1].attributes['Value'].value)
print("Scanner Offset y: " + str(ScannerOffsetYCal))

# get z position and Focus Sheet close to coverslip
Zen.Application.Pause("Set lowest position and adjust Focus Sheet!")
Exp1 = Zen.Acquisition.Experiments.ActiveExperiment
Det = Exp1.GetDetectorSettings(0)
F1 = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
Z1 = Zen.Devices.Focus.ActualPosition
print(F1)
print(str(round((F1 - ScannerOffsetYCal) * 10, 3)))
print(Z1)

# get z position and Focus Sheet at depth
Zen.Application.Pause("Set highest position and adjust Focus Sheet!")
Exp1 = Zen.Acquisition.Experiments.ActiveExperiment
Det = Exp1.GetDetectorSettings(0)
F2 = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
Z2 = Zen.Devices.Focus.ActualPosition

# calculate Focus Sheet values
if Z2 - Z1 != 0:
    m = (F2 - F1) / (Z2 - Z1)
    b = F1 - Z1 * m
else:
    m = 0
    b = F1
print(m)
print(b)

# print values
print('Overlap : ' + str(Overlap) + '%')
print('Output Folder for Data : ' + OutputFolder)
print('\n')

# check directory
OutputFolder = dircheck(OutputFolder)

############# START LINE SCAN EXPERIMENT #################

# execute the experiment
print('\nRunning Y Stack Tiling Experiment.\n')

Zen.Devices.Focus.MoveTo(Z1)
focus = Zen.Devices.Focus.ActualPosition

stack_name = 'ystack_10_0.000um.czi'
curz = Zen.Devices.Focus.ActualPosition
curf = curz * m + b
Det.SetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY', str(curf))
FocusYActual = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
print('Recording at z position: ' + str(curz))
print('with Focus Sheet position: ' + str(round((FocusYActual - ScannerOffsetYCal) * 10, 3)))
output = Zen.Acquisition.Execute(Exp1)
SizeY = output.Bounds.SizeY
PixelSizeXY = output.Scaling.X
output.Save(Path.Combine(OutputFolder, stack_name))

# calculate interval between stacks
dz = (1 - (Overlap * 0.01)) * 0.5 * SizeY * PixelSizeXY

# get number of stacks required
d = Z2 - Z1
NStacks = int(abs(round(d / dz))) + 1
if NStacks < 1:
    NStacks = 1

# record z stacks
for i in range(11, NStacks + 10):
    stack_name = 'ystack_' + str(i) + '_' + str(round((i - 10) * dz, 3)) + 'um.czi'
    Zen.Devices.Focus.MoveTo(focus - (i - 10) * dz)
    curz = Zen.Devices.Focus.ActualPosition
    curf = curz * m + b
    Det.SetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY', str(curf))
    FocusYActual = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
    print('Recording at z position: ' + str(curz))
    print('with Focus Sheet position: ' + str(round((FocusYActual - ScannerOffsetYCal) * 10, 3)))
    output = Zen.Acquisition.Execute(Exp1)
    output.Save(Path.Combine(OutputFolder, stack_name))

# go back to center position
Zen.Devices.Focus.MoveTo(focus)

############# END LINE SCAN EXPERIMENT ###################

print('\nAll y stacks done. Workflow finished.')
