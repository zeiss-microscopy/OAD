"""  
File: OAD_Automated_Physiology_IA.py
Author: Sebastian Rhode
Date: 2018_10_17
Version: 1.2

Workflow Description
-----------------------

- Acquire SNAP and detect the cells using a predefined CZIAS
- Loop over all detected objects
- Create ExperimentRegions based on their shape
- Use those created regions during Acquistion for MeanROI and Dynamics

Last Test with: c:\ServerBuild\Main\3.0-Autumn2018_18284.1\
"""

#############################################################################

from System.IO import File, Directory, Path
from collections import *


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
                        analysis=True):

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
            print('For region id ' + str(i + 2) + ' no experiment region created!')

    # save the experiment with the new regions
    exp.Save()

    return exp


##############################################################################################################

# clear output console
Zen.Application.MacroEditor.ClearMessages()

# define files
iasname = r'Physiology_340_380_Automatic.czias'
#imagefile = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\CCD_Testimages_Folder\Calcium_340_380_SNAP.czi'

# define and load experiment
expname = r'OAD_Smart_Physiology3.czexp'
exp = ZenExperiment()
exp.Load(expname, ZenSettingDirectory.User)
exp.SetActive()

# acquire SNAP using the experiment to detect objects
snap = Zen.Acquisition.AcquireImage(exp)

# get all required objects to be ready to start the region creation
exp = CreateRegionsFromIA(exp, snap, iasname,
                          expblock=0,
                          accuracy='high',
                          color=Colors.Yellow,
                          minpoints=10,
                          acquistion=False,
                          bleaching=False,
                          analysis=True)

# run experiment with the added regions
output = Zen.Acquisition.Execute(exp)

# close the snap image and the experiment
snap.Close()
#exp.Close()

print('Done. Experiment finished')
