#################################################################
# File        : Smart_Dynamics.py
# Version     : 0.1.0
# Author      : czsrh
# Date        : 23.02.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Workflow Description
# -----------------------
#
# - define an dynamics experiment (no positions are allowed)
#   Example: 2-Channel TimeSeries with Fura 340 + 380
# - define an image analysis setting to detect the cells
# - create ExperimentRegions based on their shape dervied from Image Analysis
# - Use the regions during Acquistion for MeanROI and Dynamics
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk. Especially be aware of the fact
# that automated stage movements might damage hardware if
# one starts an experiment and the the system is not setup properly.
# Please check everything in simulation mode first!
#
# Copyright (c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
#################################################################

from System.IO import File, Directory, Path
import time
from datetime import datetime
import errno
from System import Array
from System import ApplicationException
from System import TimeoutException
import sys
from collections import *


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


def getshortfiles(filelist):
    files_short = []
    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short


def runSWAF_special(SWAF_exp,
                    delay=1,
                    searchStrategy='Full',
                    sampling=ZenSoftwareAutofocusSampling.Coarse,
                    relativeRangeIsAutomatic=False,
                    relativeRangeSize=500,
                    timeout=0):

    # get current z-Position
    zSWAF = Zen.Devices.Focus.ActualPosition

    # set DetailScan active and wait for moving hardware due to settings
    SWAF_exp.SetActive()
    time.sleep(delay)

    # set SWAF parameters
    SWAF_exp.SetAutofocusParameters(searchStrategy=searchStrategy,
                                    sampling=sampling,
                                    relativeRangeIsAutomatic=relativeRangeIsAutomatic,
                                    relativeRangeSize=relativeRangeSize)
    try:
        print('Running special SWAF ...')
        zSWAF = Zen.Acquisition.FindAutofocus(SWAF_exp, timeoutSeconds=timeout)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
    except TimeoutException as e:
        print(e.Message)

    return zSWAF


def getclassnames(ias):

    # create empty dictionary
    iaclasses = {}
    # define root class, which is always there
    iaclasses['0'] = 'Root'
    classnames = ias.GetRegionClassNames()
    numclasses = len(classnames)

    for id in range(1, numclasses):
        try:
            cl = ias.GetRegionClass(id)
        except:
            cl = ias.GetRegionsClass(id)

        iaclasses[str(cl.ID)] = cl.Name
        print('ID - ClassName: ', cl.ID, cl.Name)

    return iaclasses


def CreateRegionsFromIA(exp, snap, iasname,
                        expblock=0,
                        accuracy='high',
                        color=Colors.GreenYellow,
                        minpoints=10,
                        acquistion=True,
                        bleaching=False,
                        analysis=True,
                        folder=r'c:\Temp'):

    # get the scaling from the image and calculate stageTopLeft
    scaling = snap.Metadata.ScalingMicron
    stageTopLeft = exp.GetStageTopLeftOfImage(scaling, snap)

    # clear all existing experiment regions
    exp.ClearExperimentRegionsAndPositions(expblock)

    # set position regions relative to image
    exp.SetPositionRegionsRelativeToImage(expblock, False)

    # load analysis setting and analyze the image
    ias = ZenImageAnalysisSetting()
    ias.Load(iasname, ZenImageAnalysisSettingDirectory.User)
    Zen.Analyzing.Analyze(snap, ias)
    
    # create the table and save them as CSZ files
    # Create Zen table with results for all detected objects (parent class)
    all_obj = Zen.Analyzing.CreateRegionsTable(snap)
    
    # Create Zen table with results for each single object
    single_obj = Zen.Analyzing.CreateRegionTable(snap)
    
    # show and save data tables to the specified folder
    Zen.Application.Documents.Add(all_obj)
    Zen.Application.Documents.Add(single_obj)
    all_obj.Save(Path.Combine(folder, 'objects_all.csv'))
    single_obj.Save(Path.Combine(folder, 'objects_single.csv'))
    
    # check the number of detected objects = rows inside image analysis table
    num_obj = single_obj.RowCount

    # get classes and derive regions names from that
    iasclasses = getclassnames(ias)
    regionsclassname = iasclasses['2']
    regions = Zen.Analyzing.GetRegions(snap, regionsclassname)

    print('RegionClassNames: ', iasclasses)
    print('Analysis found ' + str(regions.Count) + 'regions!')

    # loop over all regions and get the points of polygon outlins of the region
    for i in range(0, regions.Count):
        # use the desired level of detail
        if accuracy == 'high':
            points = regions[i].GetPolygonHighDetails()
        if accuracy == 'low':
            points = regions[i].GetPolygon()

        if points.Length > minpoints:
            exp.AddPolygonExperimentRegion(scaling, stageTopLeft, expblock,  points, color, acquistion, bleaching, analysis)
            print('Experiment region generated with region id ' + str(i + 2) + ' with ' + str(points.Length) + ' points')
        else:
            print('For region id ' + str(i + 2) + ' no experiment region created. No enough Polygon Points.')

    # save the experiment with the new regions
    exp.Save()

    return exp


def cloneexp(expname, prefix='GA_', save=True, reloadexp=True):

    exp = Zen.Acquisition.Experiments.GetByName(expname)
    exp_newname = prefix + expname

    # save experiment
    if save:
        exp.SaveAs(exp_newname, False)
        print('Saved Temporay Experiment as : ', exp_newname)
        # close the original experiment object
        exp.Close()
        time.sleep(1)
    # relaod experiment
    if reloadexp:
        exp_reload = Zen.Acquisition.Experiments.GetByName(exp_newname)
    elif not reloadexp:
        exp_reload = None

    return exp_reload


##############################################################################################################

# experiment blockindex
blockindex = 0

# delay for specific hardware movements in [seconds]
hwdelay = 1

# default folder for output
imgfolder = r'c:\Temp\output'

# minimum number of polygon points for an ROI
minpoints_polygon = 10

# clear output console
Zen.Application.MacroEditor.ClearMessages()

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
format = '%Y-%m-%d_%H-%M-%S'

# get list with all existing experiments and image analysis setup and a short version of that list
expfiles = Directory.GetFiles(Path.Combine(docfolder, 'Experiment Setups'), '*.czexp')
ipfiles = Directory.GetFiles(Path.Combine(docfolder, 'Image Analysis Settings'), '*.czias')
expfiles_short = getshortfiles(expfiles)
ipfiles_short = getshortfiles(ipfiles)

# Initialize Dialog
smartD = ZenWindow()
smartD.Initialize('Smart Dynamcis - Version : 0.1.0')
# add components to dialog
smartD.AddLabel('1) Select Dynamics Experiment  ------------------------------')
smartD.AddDropDown('dynamics_exp', 'Dynamics Experiment', expfiles_short, 0)
smartD.AddCheckbox('fs_before_exp', 'OPTION - FindSurface (DF only) before Overview', False)
smartD.AddCheckbox('SWAF_before_exp', 'OPTION - SWAF before Overview', False)
smartD.AddIntegerRange('SWAF_initial_range', 'Initial SWAF Range before Overview [micron]', 200, 50, 3000)
smartD.AddLabel('2) Select Image Analysis to detect objects  ----------------------')
smartD.AddDropDown('ip_pipe', 'Image Analysis Pieline', ipfiles_short, 0)
smartD.AddLabel('3) Accuracy   ---------------------------')
smartD.AddDropDown('accuracy', 'Detail Level for Polygon ROI', ['high', 'low'], 0)
smartD.AddLabel('4) Specify basefolder to save the images ----------------------')
smartD.AddFolderBrowser('outfolder', 'Savefolder for Images', imgfolder)

# show the window
result = smartD.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
dynexpname = str(result.GetValue('dynamics_exp'))
fs_before = result.GetValue('fs_before_exp')
swaf_before = result.GetValue('SWAF_before_exp')
swaf_before_range = result.GetValue('SWAF_initial_range')
iasname = str(result.GetValue('ip_pipe'))
accuracy_polygon = str(result.GetValue('accuracy'))
savefolder = str(result.GetValue('outfolder'))

# check directory and create if not existing
savefolder = dircheck(savefolder)

# create a duplicate of the OVScan experiment to work with
dynexp = cloneexp(dynexpname)

# active the temporary experiment to trigger its validation
dynexp.SetActive()
time.sleep(hwdelay)
# check if the experiment contains tile regions
dynexp_isTileExp = dynexp.IsTilesExperiment(blockindex)

if fs_before:
    # initial focussing via FindSurface to assure a good starting position
    try:
        Zen.Acquisition.FindSurface()
        print('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
        print('Z-Position : ', Zen.Devices.Focus.ActualPosition)
    

if swaf_before:
    # do an initial SWAF before the start of the workflow
    print('Z-Position before special SWAF :', Zen.Devices.Focus.ActualPosition)
    zSWAF = runSWAF_special(dynexp,
                            delay=hwdelay,
                            searchStrategy='Smart',
                            sampling=ZenSoftwareAutofocusSampling.Coarse,
                            relativeRangeIsAutomatic=False,
                            relativeRangeSize=swaf_before_range,
                            timeout=1)

# get the resulting z-position
znew = Zen.Devices.Focus.ActualPosition
print('Z-Position before special SWAF :', znew)


# acquire SNAP using the experiment to detect objects
snap = Zen.Acquisition.AcquireImage(dynexp)
Zen.Application.Documents.Add(snap)

# save the snap image inside the selected folder
savename_snap = Path.Combine(savefolder, snap.Name)
print('Save Snap as : ', savename_snap)
snap.Save(savename_snap)

# get all required objects to be ready to start the region creation
dynexp = CreateRegionsFromIA(dynexp, snap, iasname,
                             expblock=blockindex,
                             accuracy=accuracy_polygon,
                             color=Colors.Yellow,
                             minpoints=minpoints_polygon,
                             acquistion=False,
                             bleaching=False,
                             analysis=True,
                             folder=savefolder)

# run experiment with the added regions
output = Zen.Acquisition.Execute(dynexp)
#output_doc = Zen.Application.Documents.GetByName(output.Name)

# save the overview scan image inside the selected folder
savename_result = Path.Combine(savefolder, output.Name)
print('Save Image as : ', savename_result)
output.Save(savename_result)

# close the snap image and the experiment
snap.Close()

# restore the original OVScan experiment
exp_orig = Zen.Acquisition.Experiments.GetByName(dynexpname)
exp_orig.SetActive()

# delete the temporay experiment
Zen.Acquisition.Experiments.Delete(dynexp)

# show the result
Zen.Application.Documents.Add(output)
print('Smart Dynamics Workflow finished.')
