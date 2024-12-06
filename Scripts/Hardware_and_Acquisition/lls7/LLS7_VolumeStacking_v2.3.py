#################################################################
# File       : LLS7_VolumeStacking.py
# Version    : 2.3
# Author     : aukelgas
# Date       : 20.06.2022
# Institution : Carl Zeiss Microscopy GmbH
#
# Use at your own Risk !!!
# Compatible with ZEN versions 3.4 and higher (dual cam acquisition and processing only supported with ZEN3.6 HF1)
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
# v1.3 adds time series; user has to set number of time points and delay between stacks; will be saved as individual files, up to 900 time points
#
# v2.1 adds automated processing incl concatenation of recorded volume stacks
#
# v2.2 adds Focus Waist interpolation and time stamps log (time stamp is acquisition start of first volume scan per time point)
#
# v2.3 adds compatibility with Tiles experiments (single position/scene)
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
version = 2.3
# file name tiles image

# delay for specific hardware movements in [seconds]
hwdelay = 1
ttt = 100

def dircheck(basefolder):

    # check if the destination basefolder exists
    base_exists = Directory.Exists(basefolder)

    if base_exists:
        print(('Selected Directory Exists: ', base_exists))
        # specify the desired output format for the folder, e.g. 2017-08-08_17-47-41
        format = '%Y-%m-%d_%H-%M-%S'
        # create the new directory
        newdir = createfolder(basefolder, formatstring=format)
        print(('Created new directory: ', newdir))
    if not base_exists:
        Directory.CreateDirectory(basefolder)
        newdir = basefolder

    return newdir


def createfolder(basedir, formatstring='%Y-%m-%d_%H-%M-%S'):
    # construct new directoty name nased on date and time
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
        print(('Saved Temporay Experiment as : ', exp_newname))
        # close the original experiment object
        exp.Close()
        time.sleep(1)
    # relaod experiment
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
#print(MTBs)
MTBs_short = getshortfiles(MTBs)
print(("MTBs detected: " + str(MTBs_short)))

# Get active MTB
activeMTB =  max(MTBs, key=os.path.getmtime)
activeMTB = os.path.basename(activeMTB)
ind = MTBs_short.index(activeMTB)
#print(ind)

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
format = '%Y-%m-%d_%H-%M-%S'

# get list with all existing experiments and image analysis setup and a short version of that list
expfiles = Directory.GetFiles(Path.Combine(docfolder, 'Experiment Setups'), '*.czexp')
expfiles_short = getshortfiles(expfiles)

# Initialize Dialog
Dialog = ZenWindow()
Dialog.Initialize('LLS Volume Stacking - Version : ' + str(version))
# add components to dialog
#Dialog.AddLabel('1) Select Y Stack Experiment  ------------------------------')
#Dialog.AddDropDown('exp', 'Y Stack Experiment', expfiles_short, 14)
Dialog.AddLabel('1) Select overlap in Percent -------------------------------')
Dialog.AddIntegerRange('overlap', 'Overlap', 0, 0, 100)
Dialog.AddLabel('2) Active MTB-----------------------------------------------')
Dialog.AddDropDown('activeMTB', 'Active MTB', MTBs_short, ind)
Dialog.AddTextBox('TimePoints', 'Number of Time Points', 1)     # Number of time points to be recorded
Dialog.AddTextBox('Delay', 'Delay between Stacks', 0)           # Delay in seconds between loops
Dialog.AddLabel('5) Specify folder to save the images -----------------------')
Dialog.AddFolderBrowser('outfolder', 'Folder for Stack Images', imgfolder)

# show the window
result = Dialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
#ExpName = str(result.GetValue('exp'))
OutputFolder = str(result.GetValue('outfolder'))
Overlap = result.GetValue('overlap')
activeMTB = result.GetValue('activeMTB')
print(("Active MTB: " + str(activeMTB)))
TP = result.GetValue('TimePoints')
Delay = result.GetValue('Delay')

# Get Lattice Lightsheet used
hw = Zen.Devices.ReadHardwareSetting()
ls = hw.GetParameter('MTBMuSPIMSLM', 'Position')
lsname = hw.GetParameter('MTBMuSPIMSLM', 'PositionName')
print(lsname)

# Get Scanner Offset y for respective Lightsheet
xmlfile = 'C:/ProgramData/Carl Zeiss/MTB2011/' + activeMTB +'/CalibrationFiles/MuSPIM/SLM/MTBMuSPIMSLM.xml'
print(xmlfile)
xmldoc = minidom.parse(xmlfile)
itemlist = xmldoc.getElementsByTagName('CalibrationUniqueDataValue')
ScannerOffsetYCal = float(itemlist[int(ls)*3-1].attributes['Value'].value)
print(("Scanner Offset y: " + str(ScannerOffsetYCal)))

# Check if Tiles experiment
Exp1 = Zen.Acquisition.Experiments.ActiveExperiment
YN = Exp1.IsTilesExperiment(0)
print(("Is Tiles Experiment: " + str(YN)))

# get z position and Focus Sheet close to coverslip
#Zen.Acquisition.StartLive()
## Show pause dialog 
Zen.Application.Pause("Set lowest position and adjust Focus Sheet and Focus Waist!")
Exp1 = Zen.Acquisition.Experiments.ActiveExperiment
Det = Exp1.GetDetectorSettings(0)
F1 = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
Z1 =  Zen.Devices.Focus.ActualPosition
#print(F1)
#print(str(round((F1 - ScannerOffsetYCal) * 10,3)))
#print(Z1)
hw = Zen.Devices.ReadHardwareSetting()
W1 = float(hw.GetParameter('MTBMuSPIMLightSheetRefocus', 'Position'))
#print(W1)

# get z position and Focus Sheet at depth
#Zen.Acquisition.StartLive()
## Show pause dialog 
Zen.Application.Pause("Set highest position and adjust Focus Sheet and Focus Waist!")
Exp1 = Zen.Acquisition.Experiments.ActiveExperiment
Det = Exp1.GetDetectorSettings(0)
F2 = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
Z2 =  Zen.Devices.Focus.ActualPosition
#print(F2)
#print(str(round((F2 - ScannerOffsetYCal) * 10,3)))
#print(Z2)
hw = Zen.Devices.ReadHardwareSetting()
W2 = float(hw.GetParameter('MTBMuSPIMLightSheetRefocus', 'Position'))
#print(W2)

# calculate Focus Sheet values
if Z2-Z1 != 0:
    m = (F2-F1)/(Z2-Z1)
    b = F1 - Z1 * m
else:
    m = 0
    b = F1
#print(m)
#print(b)

# calculate Focus Waist values
if Z2-Z1 != 0:
    n = (W2-W1)/(Z2-Z1)
    c = W1 - Z1 * n
else:
    n = 0
    c = W1
#print(n)
#print(c)

# print values
#print('Y Stack Experiment : ' + ExpName)
print(('Overlap : ' + str(Overlap) + '%'))
#print('Number of Stacks : ' + str(NStacks))
print(('Output Folder for Data : ' + OutputFolder))
print('\n')

# check directory
OutputFolder = dircheck(OutputFolder)

# Create initial time table
table = ZenTable('ResultsTable')
table.Columns.Add('Time Point', str)
table.Columns.Add('Acquisition Time', str)

# create a duplicate of the LineScan experiment to work with
#Exp_reloaded = cloneexp(ExpName)

# active the temporary experiment to trigger its validation
#Exp_reloaded.SetActive()
#time.sleep(hwdelay)


############# START VOLUME STACK EXPERIMENT #################

# execute the experiment
print('\nRunning Volume Stacking Experiment.\n')

# get lightsheet to define z movement between stacks
#hw = Zen.Devices.ReadHardwareSetting()
#ls = hw.GetParameter('MTBMuSPIMSLM', 'Position')
#Exp1 = Zen.Acquisition.Experiments.ActiveExperiment

while ttt < TP+100:
    print('---------------')
    print(('Time Point # ' + str(ttt-99) + ', Volume Stack # 1'))
    Zen.Devices.Focus.MoveTo(Z1)
    focus = Zen.Devices.Focus.ActualPosition
    #print(focus)
    #print(ttt)

    stack_name = 'volumestack_TP' + str(ttt) + '10_0.000um.czi'
    curz = Zen.Devices.Focus.ActualPosition
    curf = curz*m+b
    curw = curz*n+c
    #print(curw)
    hardwaresetting1 = ZenHardwareSetting()
    hardwaresetting1.SetParameter('MTBMuSPIMLightSheetRefocus', 'Position', curw)
    Zen.Devices.ApplyHardwareSetting(hardwaresetting1)
    Det.SetParameter('MTBMuSPIMImagingDevice','ScannerOffsetY', str(curf))
    FocusYActual = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
    print(('Recording at z position: ' + str(curz)))
    print(('with Focus Sheet position: ' + str(round((FocusYActual - ScannerOffsetYCal) * 10,3))))
    hw = Zen.Devices.ReadHardwareSetting()
    test = float(hw.GetParameter('MTBMuSPIMLightSheetRefocus', 'Position'))
    #print('with Focus Waist position: ' + str(round(curw)))
    print(('with Focus Waist position: ' + str(round(test))))
    output = Zen.Acquisition.Execute(Exp1)
    SizeY = output.Bounds.SizeY
    PixelSizeXY = output.Scaling.X
    #print(SizeY)
    #print(PixelSizeXY)
    output.Save(Path.Combine(OutputFolder, stack_name))
    output.Close()
    timestring='%H-%M-%S'
    table.SetValue(ttt-100, 0, ttt-99)
    table.SetValue(ttt-100, 1, datetime.now().strftime(timestring))

    # calculate interval between stacks
    dz = (1-(Overlap*0.01))*0.5*SizeY*PixelSizeXY
    #print(dz)

    # get number of stacks required
    d = Z2 - Z1
    NStacks = int(abs(round(d / dz)))+1
    if NStacks < 1:
        NStacks = 1
        #print(NStacks)

    # record z stacks
    for i in range (11, NStacks+10):
        print('---------------')
        print(('Time Point # ' + str(ttt-99) + ', Volume Stack # ' + str(i-9)))
        stack_name = 'volumestack_TP' + str(ttt) + str(i) + '_' + str(round((i-10)*dz,3)) + 'um.czi'
        Zen.Devices.Focus.MoveTo(focus-(i-10)*dz)
        curz = Zen.Devices.Focus.ActualPosition
        curf = curz*m+b
        curw = curz*n+c
        #print(curw)
        hardwaresetting1 = ZenHardwareSetting()
        hardwaresetting1.SetParameter('MTBMuSPIMLightSheetRefocus', 'Position', curw)
        Zen.Devices.ApplyHardwareSetting(hardwaresetting1)
        Det.SetParameter('MTBMuSPIMImagingDevice','ScannerOffsetY',str(curf))
        FocusYActual = float(Det.GetParameter('MTBMuSPIMImagingDevice', 'ScannerOffsetY'))
        print(('Recording at z position: ' + str(curz)))
        print(('with Focus Sheet position: ' + str(round((FocusYActual - ScannerOffsetYCal) * 10,3))))
        hw = Zen.Devices.ReadHardwareSetting()
        test = float(hw.GetParameter('MTBMuSPIMLightSheetRefocus', 'Position'))
        #print('with Focus Waist position: ' + str(round(curw)))
        print(('with Focus Waist position: ' + str(round(test))))
        if YN == True:
            Exp1.ModifyTileRegionsZ(0,curz)
        output = Zen.Acquisition.Execute(Exp1)
        output.Save(Path.Combine(OutputFolder, stack_name))
        output.Close()

    ttt = ttt + 1
    time.sleep(Delay)

# go back to center position
Zen.Devices.Focus.MoveTo(focus)

# add table
Zen.Application.Documents.Add(table)
table.Save(Path.Combine(OutputFolder, 'timepoints.czt'))

###########################################################################
# PROCESSING
###########################################################################

# use output folder as defind by user in acquistion step as input folder
InputFolder = OutputFolder
OutputFolder = str(OutputFolder + "\deskewed")

Directory.CreateDirectory(OutputFolder)
print('---------------')
print(('Created new directory: ', OutputFolder))

# Set parameters (deskew with cover glass transformation)
myShear = ZenZAxisShear.None
myInt = ZenInterpolation.Linear

# get list of files to deskew
filelist = os.listdir(InputFolder)
filelist = [i for i in filelist if i.endswith('.czi') and not i.endswith('MIP.czi')]

# get number of stacks
NumberOfStacks = len(filelist)
print(NumberOfStacks)

# Deskew images
for ii in range(0, NumberOfStacks):
        imgname = Path.Combine(InputFolder, filelist[ii])
        deskew_name = str(filelist[ii][:-4] + '_deskewed.czi')
        Img1 = Zen.Application.LoadImage(imgname, False)
        Img2 = Zen.Processing.Transformation.Geometric.Deskew(Img1,myInt,myShear)
        Img2.Save(Path.Combine(OutputFolder, deskew_name))


###########################################################################
# FUSING
###########################################################################

# use output folder from previous step as input folder
InputFolder = OutputFolder
OutputFolder = str(OutputFolder + "\concatenated")

Directory.CreateDirectory(OutputFolder)
print('---------------')
print(('Created new directory: ', OutputFolder))

# get list of files to fuse
filelist = os.listdir(InputFolder)
filelist = [i for i in filelist if i.endswith('.czi')]

# get number of stacks
NumberOfStacks = len(filelist)/TP
print(NumberOfStacks)

# load first image to get parameters
imgname = Path.Combine(InputFolder, filelist[0])
Img = Zen.Application.LoadImage(imgname, False)

SizeZ = Img.Bounds.SizeZ-1;
SizeX = Img.Bounds.SizeX;
SizeY = Img.Bounds.SizeY;
SizeC = Img.Bounds.SizeC;
PixelSizeXY = Img.Scaling.X
PixelSizeZ = Img.Scaling.Z
#print(PixelSizeXY)
print(SizeZ)
Img.Close()

#FinalImage = ZenImage(Img.Bounds.SizeX, Img.Bounds.SizeY,ZenPixelType.Gray16, Img.Bounds.SizeZ, NumberOfTimePoints-1,0)
FinalImage = Zen.Processing.Utilities.ImageGenerator(Img.Bounds.SizeX, Img.Bounds.SizeY, NumberOfStacks*Img.Bounds.SizeZ, Img.Bounds.SizeC, 1, 0,65535, ZenImageGeneratorPattern.Checker, ZenPixelType.Gray16, ZenThirdProcessingDimension.Z, False)
FinalImage.Scaling.X = PixelSizeXY
FinalImage.Scaling.Y = PixelSizeXY
FinalImage.Scaling.Z = PixelSizeZ

#Copy image
for ttt in range (0, TP):
    jj=0
    for ii in range (ttt*NumberOfStacks, (ttt+1)*NumberOfStacks):
        imgname = Path.Combine(InputFolder, filelist[ii])
        print(imgname)
        Img1 = Zen.Application.LoadImage(imgname, False)
        for cc in range (0, SizeC):
            for zz in range(0, SizeZ):
                SubsetString= "Z("+ str(zz+2) + ") | C("+ str(cc+1) +") | T("+ str(ttt+1) +")"
                #print(SubsetString)
                SubImg = Img1.CreateSubImage(SubsetString)
                FinalImage.AddSubImage(SubImg,ttt,cc,(jj*SizeZ)+zz)
                SubImg.Close()
        Img.Close()
        jj=jj+1

Zen.Application.Documents.Add(FinalImage)
FinalImage.Save(Path.Combine(OutputFolder, 'concatenated_stacks.czi'))

print('---------------')
print('All volume stacks recorded and processed. Workflow finished.')
