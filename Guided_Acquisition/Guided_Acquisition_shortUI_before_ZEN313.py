#################################################################
# File        : Guided_Acquisition_shortUI.py
# Version     : 8.3
# Author      : czsrh, czmla, czkel
# Date        : 21.07.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Optimized for the use with Celldiscoverer 7 and DF2, but
# applicable for all motorized stands running in ZEN Blue.
# Please adapt focussing commands, especially FindSurface
# when using with other stands.
#
# 1) - Select Overview Scan Experiment
# 2) - Select appropriate Image Analysis Pipeline or APEER module setting
#      to detect objects of interest
# 3) - Select Detailed Scan Experiment
# 4) - Specify the output folder for the image and data tables
#
# Tested with ZEN blue 3.4.
# Should work also with later version with some limitations
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk. Especially be aware of the fact
# that automated stage movements might damage hardware if
# one starts an experiment and the the system is not setup
# and calibrated properly. Check everything in simulation mode first!
#
# Copyright(c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import time
from datetime import datetime
import errno
from System import Array
from System import ApplicationException
from System import TimeoutException
from System.IO import File, Directory, Path
from System.Collections.Generic import List
import sys

# version number for dialog window
version = 8.3
# file name for overview scan
ovscan_name = 'OverviewScan.czi'

"""
Additional XY offest for possible 2nd port relative to the 1st port
Example: 1st port Camera and 2nd port LSM
Can be set to Zero, when system is correctly calibrated
!!! Only use when overview and detailed scan are using different detector !!!
"""
dx_detector = 0.0
dy_detector = 0.0

# experiment blockindex
blockindex = 0
# delay for specific hardware movements in [seconds]
hwdelay = 1
# posprocessing switch
do_postprocess = False

##############################################################


def find_module(name):
    """Finds an APEER module given its Name.

    :param name: The name of the module to look for
    :type name: str
    :return: The first module with the specified name or None, if no such module exists.
    :rtype: ApeerModule
    """

    modules = ZenApeer.Onsite.ListLocalModules()

    return next((m for m in modules if m.ModuleName == name), None)


def get_module_inputs(params):
    """Get the module inputs.

    :param params: Apeer module parameters
    :type params: ApeerModuleDescription
    :return: List with input parameters
    :rtype: list
    """
    module_inputs = []
    for ip in params.Inputs:
        module_inputs.append(ip.Key)

    return module_inputs


def get_columns(table):
    """Get columns names and their IDs as a dictionary.

    :param table: Input table
    :type table: ZenTable
    :return: Dictionary with columns names and their respective IDs
    :rtype: dict
    """
    col_dict = {}
    colid = -1
    # loop over all columns
    for col in range(0, table.ColumnCount):
        colid += 1
        # get the caption and store in dictionary with ID as value
        colcaption = table.Columns[col].Caption
        col_dict[colcaption] = colid

    return col_dict


def get_module(module_name, module_version=0):
    """Get an APEER module and check if the desired version is available.

    :param module_name: APEER module name
    :type module_name: str
    :param module_version: Version number of the APEER module, defaults to 0
    :type module_version: int, optional
    :return: mymodule, version_found
    :rtype: ApeerModule, bool
    """
    version_found = False

    # try to find the desired module
    mymodule = find_module(module_name)

    if mymodule is not None:
        print('Module : ' + module_name + ' found.')
    elif mymodule is None:
        print('Module : ' + module_name + ' not found.')

    if str(module_version) in mymodule.AvailableVersions:
        print('Module : ' + module_name + ' Version ' + str(module_version) + ' found.')
        version_found = True
    elif not str(module_version) in mymodule.AvailableVersions:
        print('Module : ' + module_name + ' Version ' + str(module_version) + ' not found.')

    return mymodule, version_found


def getshortfiles(filelist):
    """Create list with shortended filenames

    :param filelist: List with files with complete path names
    :type filelist: list
    :return: List with filenames only
    :rtype: list
    """
    files_short = []
    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short


def checktableentry(datatable, entry2check='ImageSceneContainerName'):
    """Check ZEN table for an existing column by name.

    :param datatable: ZEE Table with data.
    :type datatable: ZenTable
    :param entry2check: Column to look for, defaults to 'ImageSceneContainerName'
    :type entry2check: str, optional
    :return: entry_exits, column
    :rtype: bool, integer
    """

    num_col = datatable.ColumnCount
    entry_exists = False
    column = None

    for c in range(0, num_col):
        # get the current column name
        colname = datatable.Columns[c].ColumnName
        if colname == entry2check:
            column = c
            entry_exists = True
            break

    return entry_exists, column


def dircheck(basefolder):
    """Check if a directory or folder already exits.
    Create the folder if it does not exist

    :param basefolder: folder to check
    :type basefolder: str
    :return: new_directory
    :rtype: str
    """

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
    """Creates a new folder inside an existing folder using a specific format

    :param basedir: Folder inside which the new directory should be created
    :type basedir: str
    :param formatstring: String format for the new folder, defaults to '%Y-%m-%d_%H-%M-%S'
    :type formatstring: str, optional
    :return: Newly created directory
    :rtype: str
    """    

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


def cloneexp(expname, prefix='GA_', save=True, reloadexp=True):
    """Clone an existing ZenExperiment.

    :param expname: Name of the ZenExperiment
    :type expname: ZenExperiment
    :param prefix: Prefix for the experiment name, defaults to 'GA_'
    :type prefix: str, optional
    :param save: Option to save the cloned experiment, defaults to True
    :type save: bool, optional
    :param reloadexp: option to reload the cloned experiment afterwards, defaults to True
    :type reloadexp: bool, optional
    :return: exp_reload
    :rtype: ZenExperiment or None
    """

    exp = Zen.Acquisition.Experiments.GetByName(expname)
    exp_newname = prefix + expname

    # save experiment
    if save:
        exp.SaveAs(exp_newname, False)
        print(('Saved Temporay Experiment as : ', exp_newname))
        # close the original experiment object
        exp.Close()
        time.sleep(1)
    
    # reload experiment
    if reloadexp:
        exp_reload = Zen.Acquisition.Experiments.GetByName(exp_newname)
    elif not reloadexp:
        exp_reload = None

    return exp_reload


def runSWAF_special(SWAF_exp,
                    delay=5,
                    searchStrategy='Full',
                    sampling=ZenSoftwareAutofocusSampling.Coarse,
                    relativeRangeIsAutomatic=False,
                    relativeRangeSize=500,
                    timeout=0):
    """Execute SWAF for a ZenExperiment with custom settings.

    :param SWAF_exp: ZenExperiment containing the SWAF settings
    :type SWAF_exp: ZenExperiment
    :param delay: Hardware delay to wait until "everything" has moved into place, defaults to 5
    :type delay: int, optional
    :param searchStrategy: Search Strategy for the SWAF, defaults to 'Full'
    :type searchStrategy: str, optional
    :param sampling: Sampling for the SWAF, defaults to ZenSoftwareAutofocusSampling.Coarse
    :type sampling: ZenSoftwareAutofocusSampling, optional
    :param relativeRangeIsAutomatic: Set SWAF range automatically, defaults to False
    :type relativeRangeIsAutomatic: bool, optional
    :param relativeRangeSize: Relative range of SWAF [micron], defaults to 500
    :type relativeRangeSize: int, optional
    :param timeout: Timeout for SWAF [s], defaults to 0
    :type timeout: int, optional
    :return: zSWAF
    :rtype: float
    """

    # get current z-Position
    zSWAF = Zen.Devices.Focus.ActualPosition
    print(('Z-Position before special SWAF :', zSWAF))

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
        print(('Application Exception : ', e.Message))
    except TimeoutException as e:
        print((e.Message))

    print(('Z-Position after initial SWAF [micron]: ', zSWAF))

    return zSWAF


def run_postprocessing(image, parameters={}, func='topography'):
    """Example template to add post-processing functions.

    :param image: Image to be processed
    :type image: ZenImage
    :param parameters: Dictionary with processing parameters for function, defaults to {}
    :type parameters: dict, optional
    :param func: Function name, defaults to 'topography'
    :type func: str, optional
    :return: image or processed image
    :rtype: ZenImage
    """

    if func == 'topography':

        noise_low = parameters['noise_low']
        noise_high = parameters['noise_high']
        outputfolder = parameters['outputfolder']
        ext = parameters['extension']

        # converting to topo, with defined FZ noisecut
        # in filter settings: 0-255 means no filter, 1-254 means cut one gray scale from top and from bottom
        imgtop = Zen.Processing.Transformation.Topography.CreateTopography(image, noise_low, noise_high)
        
        # saving file to the directory
        topo_filepath = Path.Combine(outputfolder, Path.GetFileNameWithoutExtension(image.FileName) + ext)
        Zen.Processing.Utilities.ExportHeightmapFromTopography(imgtop, topo_filepath)
        print(('Exported to : ', topo_filepath))
        imgtop.Close()

    return image


def apply_recall_focus():
    """Recall the stored Z-Value for Definite Focus 2 (DF2).

    :return: [description]
    :rtype: [type]
    """

    # get the z-position
    zpos = Zen.Devices.Focus.ActualPosition

    try:
        # apply RecallFocus for the current position
        Zen.Acquisition.RecallFocus()
        zpos = Zen.Devices.Focus.ActualPosition
        print('Recall Focus (Definite Focus) applied.')
        print(('Updated Z-Position: ', zpos))
    except ApplicationException as e:
        print(('Application Exception : ', e.Message))
        print('Recalling Focus (Definite Focus 2) failed.')

    print(('New Z-Position before Detail Experiment will start:', zpos))

    return zpos


def modify_tileexperiment_rect(tileexp, blockindex=0,
                               bcwidth=1.0,
                               bcheight=1.0,
                               xpos=1.0,
                               ypos=1.0,
                               zpos=1.0):
    """Modify an existing ZenExperiment with an existing Tileregion by adding
    an new rectangular Tileregion.

    :param tileexp: ZenExperiment to be modified with a rectangular TileRegion.
    :type tileexp: ZenExperiment
    :param blockindex: Experiment Block index, defaults to 0
    :type blockindex: int, optional
    :param bcwidth: Width of the new TileRegion [micron], defaults to 1.0
    :type bcwidth: float, optional
    :param bcheight: Height of the new Tileregion [micron], defaults to 1.0
    :type bcheight: float, optional
    :param xpos: StageX of the new Tileregion center [micron], defaults to 1.0
    :type xpos: float, optional
    :param ypos: StageY of the new TileRegion center [micron], defaults to 1.0
    :type ypos: float, optional
    :param zpos: StageZ of the new TileRegion [micron], defaults to 1.0
    :type zpos: float, optional
    :return: tileexp
    :rtype: ZenExperiment
    """

    print(('Width and Height : ', '%.2f' % bcwidth, '%.2f' % bcheight))
    print('Modifying Tile Properties XYZ Position and width and height.')

    # Modify the XYZ position and size of the TileRegion on-the-fly
    print(('Starting Z-Position for current Object: ', '%.2f' % zpos))
    print(('New Tile Properties: ', '%.2f' % xpos, '%.2f' % ypos, '%.2f' % zpos, '%.2f' % bcwidth, '%.2f' % bcheight))
    tileexp.ClearTileRegionsAndPositions(blockindex)
    try:
        tileexp.AddRectangleTileRegion(blockindex, xpos, ypos, bcwidth, bcheight, zpos)
    except ApplicationException as e:
        print(('Application Exception : ', e.Message))

    return tileexp


def modify_tileexperiment_polygon(tileexp, polyregion,
                                  blockindex=0,
                                  zpos=0.0):
    """Modify an existing ZenExperiment with an existing Tileregion by adding
    an new Polygon Tileregion.

    :param tileexp: ZenExperiment to be modified with a Polygon TileRegion.
    :type tileexp: ZenExperiment
    :param polyregion: List with ZenPoints decribing the polygon in absolute stageXY coordinates [micron]
    :type bcwidth: IList[ZenPoints]
    :param blockindex: Experiment Block index, defaults to 0
    :type blockindex: int, optional
    :param zpos: StageZ of the new TileRegion [micron], defaults to 1.0
    :type zpos: float, optional
    :return: tileexp
    :rtype: ZenExperiment
    """
                                  
    print('Modifying Tile Properties using Polygon for ZEN Image Analysis.')
    print(('Starting Z-Position for current Object: ', '%.2f' % zpos))
    tileexp.ClearTileRegionsAndPositions(blockindex)
    try:
        tileexp.AddPolygonTileRegion(blockindex, polyregion, zpos)
    except ApplicationException as e:
        print(('Application Exception : ', e.Message))

    return tileexp


def create_exppolygon(points, stageTL, scaling):
    """Convert List of pixel-based points from Image Analysis region into
    List[ZenPoints] in absolute stageXY coordinates [micron].

    :param points: List of Points [pixel]
    :type points: List
    :param stageTL: Image Stage Top-Left [micron]
    :type stageTL: 
    :param scaling: [description]
    :type scaling: Point
    :return: zplist
    :rtype: List[ZenPoints]
    """

    # create new list of ZenPoints
    pl = []
    zplist= List[ZenPoint]()
    
    # iterate over all points inside list
    for p in range(len(points)):
        # use StageTopLeft and scaling to convert points to stageXY
        newx = stageTL.X + round(points[p].X * scaling.X, 1)
        newy = stageTL.Y + round(points[p].Y * scaling.Y, 1)
        pl.append(ZenPoint(newx, newy))

    # create IList[ZenPoint]
    zplist.AddRange(pl)
    
    return zplist


def getclassnames(ias):
    """Get ID and name of classes from Image Analysis Setting

    :param ias: Setting to extract the ID and names from
    :type ias: ZenImageAnalysisSetting
    :return: iaclasses
    :rtype: dict
    """

    # create empty dictionary to conatin the ID and Name
    iaclasses = {}
    classnames = ias.GetRegionClassNames()

    for id in range(0, len(classnames)):
        try:
            # class for single objects
            cl = ias.GetRegionClass(id)
        except:
            # class for all objects
            cl = ias.GetRegionsClass(id)

        iaclasses[cl.ID] = cl.Name
        print(('ID - RegionClassName: ', cl.ID, cl.Name))

    return iaclasses


###########################################################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
imgfolder = r'd:\Output\Guided_Acquisition'
format = '%Y-%m-%d_%H-%M-%S'

# get list with all existing experiments and image analysis setup and a short version of that list
expfiles = Directory.GetFiles(Path.Combine(docfolder, 'Experiment Setups'), '*.czexp')
ipfiles = Directory.GetFiles(Path.Combine(docfolder, 'Image Analysis Settings'), '*.czias')
apfiles = Directory.GetFiles(Path.Combine(docfolder, 'APEER Module Settings'), '*.czams')
expfiles_short = getshortfiles(expfiles)
ipfiles_short = getshortfiles(ipfiles)
apfiles_short = getshortfiles(apfiles)

# Initialize Dialog
GuidedAcqDialog = ZenWindow()
GuidedAcqDialog.Initialize('Guided Acquisition - Version : ' + str(version))
# add components to dialog
GuidedAcqDialog.AddLabel('------   Select Overview Experiment   ------')
GuidedAcqDialog.AddDropDown('overview_exp', 'Overview Scan Experiment', expfiles_short, 0)
GuidedAcqDialog.AddCheckbox('fs_before_overview', 'OPTION - FindSurface (DF only) before Overview', False)
GuidedAcqDialog.AddCheckbox('SWAF_before_overview', 'OPTION - SWAF before Overview', False)
GuidedAcqDialog.AddIntegerRange('SWAF_ov_initial_range', 'Initial SWAF Range before Overview [micron]', 200, 50, 3000)
GuidedAcqDialog.AddLabel('------   Select Image Analysis to detect objects   ------')
GuidedAcqDialog.AddDropDown('ip_pipe', 'Image Analysis Pipeline', ipfiles_short, 0)
GuidedAcqDialog.AddCheckbox('use_poly', 'Use Polygons from ZEN IA instead of BBox', True)
GuidedAcqDialog.AddCheckbox('use_apeer_for_IA', 'Use APEER module run run IA instead', False)
GuidedAcqDialog.AddDropDown('ap_pipe', 'APEER Module Settings', apfiles_short, 0)
GuidedAcqDialog.AddLabel('------   Select DetailScan Experiment   ------')
GuidedAcqDialog.AddDropDown('detailed_exp', 'Detailed Scan Experiment', expfiles_short, 1)
GuidedAcqDialog.AddCheckbox('fs_before_detail', 'OPTION - FindSurface (DF only) before Detail', False)
GuidedAcqDialog.AddCheckbox('SWAF_before_detail', 'OPTION - SWAF before Detail', False)
GuidedAcqDialog.AddIntegerRange('SWAF_detail_initial_range', 'Initial SWAF Range before Detail [micron]', 100, 10, 1000)
GuidedAcqDialog.AddCheckbox('recallfocus_beforeDT', 'OPTION - Use RecallFocus (DF only) before Detail', False)
GuidedAcqDialog.AddLabel('------   Specify basefolder to save the images   ------')
GuidedAcqDialog.AddFolderBrowser('outfolder', 'Basefolder for Images and Data Tables', imgfolder)

# show the window
result = GuidedAcqDialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
OverViewExpName = str(result.GetValue('overview_exp'))
ImageAS = str(result.GetValue('ip_pipe'))
ApeerMS = str(result.GetValue('ap_pipe'))
DetailExpName = str(result.GetValue('detailed_exp'))
OutputFolder = str(result.GetValue('outfolder'))
fs_beforeOV = result.GetValue('fs_before_overview')
SWAF_beforeOV = result.GetValue('SWAF_before_overview')
SWAF_beforeOV_range = result.GetValue('SWAF_ov_initial_range')
fs_beforeDT = result.GetValue('fs_before_detail')
SWAF_beforeDT = result.GetValue('SWAF_before_detail')
SWAF_beforeDT_range = result.GetValue('SWAF_detail_initial_range')
RecallFocus = result.GetValue('recallfocus_beforeDT')
use_apeer = result.GetValue('use_apeer_for_IA')
use_polygon = result.GetValue('use_poly')


# print values
print(('Overview Scan Experiment : ', OverViewExpName))
if not use_apeer:
    print(('Image Analysis Pipeline : ', ImageAS))
    print(('Use IA Polygon instead of BBox : ', use_polygon))
if use_apeer:
    print(('Use Apeer Module Setting : ', ApeerMS))
print(('Detailed Scan Experiment : ', DetailExpName))
print(('Output Folder for Data : ', OutputFolder))
print('\n')

# check directory
OutputFolder = dircheck(OutputFolder)

# create a duplicate of the OVScan experiment to work with
OVScan_reloaded = cloneexp(OverViewExpName)

# active the temporary experiment to trigger its validation
OVScan_reloaded.SetActive()
time.sleep(hwdelay)

# check if the experiment contains tile regions
OVScanIsTileExp = OVScan_reloaded.IsTilesExperiment(blockindex)

############# START OVERVIEW SCAN EXPERIMENT #################

if fs_beforeOV:
    # initial focussing via FindSurface to assure a good starting position
    Zen.Acquisition.FindSurface()
    print(('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition))

if SWAF_beforeOV:
    zSWAF = runSWAF_special(OVScan_reloaded,
                            delay=hwdelay,
                            searchStrategy='Full',
                            sampling=ZenSoftwareAutofocusSampling.Coarse,
                            relativeRangeIsAutomatic=False,
                            relativeRangeSize=SWAF_beforeOV_range,
                            timeout=1)

# get the resulting z-position
znew = Zen.Devices.Focus.ActualPosition

# adapt the Overview Scan Tile Experiment with new Z-Position
if OVScanIsTileExp:
    OVScan_reloaded.ModifyTileRegionsZ(blockindex, znew)
    print(('Adapted Z-Position of Tile OverView. New Z = ', '%.2f' % znew))

# execute the experiment
print('\nRunning OverviewScan Experiment.\n')
output_OVScan = Zen.Acquisition.Execute(OVScan_reloaded)
# For testing purposes - Load overview scan image automatically instead of executing the "real" experiment
#ovtestimage = r"D:\GA_test_SRH\ov_ia.czi"
#output_OVScan = Zen.Application.LoadImage(ovtestimage, False)

# the the stage top-left and the scaling of the overview image
stageTL = output_OVScan.GetPositionLeftTop()
ovscaling = output_OVScan.Scaling

# show the overview scan inside the document area
Zen.Application.Documents.Add(output_OVScan)
ovdoc = Zen.Application.Documents.GetByName(output_OVScan.Name)

# save the overview scan image inside the select folder
savepath_ovscan = Path.Combine(OutputFolder, ovscan_name)
output_OVScan.Save(savepath_ovscan)

# get the actual focus value for the overscan independent from the z-value
# before the start of the overview scan using the image metadata
zvalue_ovscan = output_OVScan.Metadata.FocusPositionMicron

############# END OVERVIEW SCAN EXPERIMENT ###################

# run normal ZEN image analysis
if not use_apeer:

    # Load analysis setting created by the wizard or an separate macro
    ias = ZenImageAnalysisSetting()

    # for simulation use: 000 - RareEventExample.czias
    ias.Load(ImageAS)

    # Analyse the image
    Zen.Analyzing.Analyze(output_OVScan, ias)

    if use_polygon:

        # get classes and derive regions names from that
        iasclasses = getclassnames(ias)
        
        # get the individual image analysis regions from 1st IA class (!!!)
        # ATTENTION: the first single objects class will be used. It has ID = 2
        regions = Zen.Analyzing.GetRegions(output_OVScan, iasclasses[2])
        print(('RegionClassNames: ', iasclasses))
        print(('Analysis found ' + str(regions.Count) + 'regions!'))
    
        # create dictionary for polygon regions
        polyregions = {}
        
        # loop over all regions and get the points of polygon (outline of the object)
        for i in range(0, regions.Count):
            points = regions[i].GetPolygon()
            
            # convert points to stage coordinates
            polyregions[i] = create_exppolygon(points, stageTL, ovscaling)

    # Create Zen table with results for all detected objects (parent class)
    AllObj = Zen.Analyzing.CreateRegionsTable(output_OVScan)

    # Create Zen table with results for each single object
    SingleObj = Zen.Analyzing.CreateRegionTable(output_OVScan)

    # check for existence of required column names inside table
    soi = SingleObj.GetBoundsColumnInfoFromImageAnalysis(True)

    # 1st item is a bool indicating if all required columns could be found
    columnsOK = soi.AreRequiredColumnsAvailabe

    if not columnsOK:
        print('Execution stopped. Required Columns are missing.')
        raise Exception('Execution stopped. Required Columns are missing.')

    # show and save data tables to the specified folder
    Zen.Application.Documents.Add(AllObj)
    Zen.Application.Documents.Add(SingleObj)
    AllObj.Save(Path.Combine(OutputFolder, 'OverviewTable.csv'))
    SingleObj.Save(Path.Combine(OutputFolder, 'SingleObjectsTable.csv'))

# use APEER module to detect the objects
if use_apeer:

    # read it from settings file
    ams = ZenApeer.Onsite.ModuleSetting()
    
    # loaf the APEER module seeting b - remove *.czams file extension first
    ams.Load(Path.GetFileNameWithoutExtension(ApeerMS))
    
    print('-----   Apeer Module Setting   -----')
    print(('Module Name    : ', ams.ModuleName))
    print(('Module Version : ', ams.ModuleVersion))
    print(('Module Parameters    : ', ams.Parameters))

    # get module and check
    mymodule, version_found = get_module(ams.ModuleName, module_version=ams.ModuleVersion)

    # exit if the check failed
    if mymodule is None or not version_found:
        print('Module check failed. Exiting.')
        raise SystemExit

    # get the module parameters for the specified module
    module_params = ZenApeer.Onsite.GetSampleModuleParameters(ams.ModuleName, ams.ModuleVersion)

    # get the module input programmatically
    module_inputs = get_module_inputs(module_params)

    # create the required dictionary with the correct key and value
    input_image = {module_inputs[0]: savepath_ovscan}

    # create the path to save the results
    #savepath_apeer = Path.Combine(OutputFolder, 'apeer_results')
    savepath_apeer = OutputFolder

    # create the output directory if not existing already
    if not Directory.Exists(savepath_apeer):
        Directory.CreateDirectory(savepath_apeer)

    # run the local APEER module with using keywords
    try:
        runoutputs, status, log = ZenApeer.Onsite.RunModule(moduleName=ams.ModuleName,
                                                            moduleVersion=ams.ModuleVersion,
                                                            inputs=input_image,
                                                            parameters=ams.Parameters,
                                                            storagePath=savepath_apeer)
                                                            
        for op in runoutputs.GetEnumerator():
            print('-----    Outputs   -----')
            print((op.Key, ' : ', op.Value))
        
    except ApplicationException as e:
        print(('Module Run failded.', e.Message))
        raise SystemExit

    # get results storage locations
    # IMPORTANT: To be used inside Guided Acquisition
    # the APEER Module is expected to have
    # at least those to outputs with exactly those names

    if not runoutputs.ContainsKey('segmented_image'):
        print('No output : segmented_image')
        raise SystemExit
    
    if not runoutputs.ContainsKey('objects_table'):
        print('No output : objects_table')
        raise SystemExit

    # load the segmented image and make sure the pyramid is calculated
    segmented_image = Zen.Application.LoadImage(runoutputs['segmented_image'], False)
    Zen.Processing.Utilities.GenerateImagePyramid(segmented_image, ZenBackgroundMode.Black)
    Zen.Application.Documents.Add(segmented_image)

    # auto-display min-max
    ids = segmented_image.DisplaySetting.GetAllChannelIds()
    for id in ids:
        segmented_image.DisplaySetting.SetParameter(id, 'IsAutoApplyEnabled', True)

    # initialize ZenTable object and load CSV file
    SingleObj = ZenTable()
    SingleObj.Load(runoutputs['objects_table'])
    Zen.Application.Documents.Add(SingleObj)

    # get all columns as dict with columnIDs
    colID = get_columns(SingleObj)

    # define the required column names here
    col2check = ('bbox_center_stageX', 'bbox_center_stageY', 'bbox_width_scaled', 'bbox_height_scaled')

    # check if all columns exist
    if all(key in colID for key in col2check):
        print('All required columns found.')
    else:
        print('Not All required columns found. Exiting.')
        raise SystemExit

# check the number of detected objects = rows inside image analysis table
num_POI = SingleObj.RowCount

############## Prepare DetailScan #################

print('Starting DetailScan ...')

if not use_apeer:
    xpos_1st = SingleObj.GetValue(0, soi.CenterXColumnIndex)
    ypos_1st = SingleObj.GetValue(0, soi.CenterYColumnIndex)

if use_apeer:
    xpos_1st = SingleObj.GetValue(0, colID['bbox_center_stageX'])
    ypos_1st = SingleObj.GetValue(0, colID['bbox_center_stageY'])

# move to 1st detected object to be at a XY-position that makes sense
Zen.Devices.Stage.MoveTo(xpos_1st + dx_detector, ypos_1st + dy_detector)

# and move the the z-values from the overview scan image
Zen.Devices.Focus.MoveTo(zvalue_ovscan)

# create an duplicate of the DetailScan experiment to work with
DetailScan_reloaded = cloneexp(DetailExpName)

# active the temporary experiment to trigger its validation
DetailScan_reloaded.SetActive()
time.sleep(hwdelay)
# check if the experiment contains tile regions
DetailIsTileExp = DetailScan_reloaded.IsTilesExperiment(blockindex)

# test snap to change to the valid settings, e.g. the objective from the DetailScan
testsnap = Zen.Acquisition.AcquireImage(DetailScan_reloaded)
print('Acquire Test Snap using setting from DetailScan')
testsnap.Close()
# wait for moving hardware due to settings
time.sleep(hwdelay)

if fs_beforeDT:
    try:
        # initial focussing via FindSurface to assure a good starting position
        Zen.Acquisition.FindSurface()
        print(('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition))
    except ApplicationException as e:
        print(('Application Exception : ', e.Message))
        print('FindSurface (Definite Focus) failed.')

if SWAF_beforeDT:
    zSWAF = runSWAF_special(DetailScan_reloaded,
                            delay=hwdelay,
                            searchStrategy='Full',
                            sampling=ZenSoftwareAutofocusSampling.Coarse,
                            relativeRangeIsAutomatic=False,
                            relativeRangeSize=SWAF_beforeDT_range,
                            timeout=0)

userecallfocus = False

if RecallFocus:
    try:
        # store current focus position inside DF to use it with RecallFocus
        Zen.Acquisition.StoreFocus()
        userecallfocus = True
    except ApplicationException as e:
        print(('Application Exception : ', e.Message))
        print('StoreFocus (Definite Focus) failed.')
        userecallfocus = False


############# START DETAILED SCAN EXPERIMENT #############

# again get the resulting focus position
zpos = Zen.Devices.Focus.ActualPosition

if not use_apeer:

    # check for the column 'ID' which is required
    ID_exists, column_ID = checktableentry(SingleObj, entry2check='ID')

    # execute detailed experiment at the position of every detected object
    for obj in range(SingleObj.RowCount):

        # get the object information from the position table
        POI_ID = SingleObj.GetValue(obj, column_ID)

        # get XY-stage position from table
        xpos = SingleObj.GetValue(obj, soi.CenterXColumnIndex)
        ypos = SingleObj.GetValue(obj, soi.CenterYColumnIndex)

        # move to the current position
        Zen.Devices.Stage.MoveTo(xpos + dx_detector, ypos + dy_detector)
        print(('Moving Stage to Object ID:', POI_ID, ' at :', '%.2f' % xpos, '%.2f' % ypos))

        # try to apply RecallFocus (DF only) when this option is used
        if userecallfocus:
            zpos = apply_recall_focus()

        # if DetailScan is a Tile Experiment
        if DetailIsTileExp:

            print('Detailed Experiment contains TileRegions.')
            # Modify tile center position - get bounding rectangle width and height in microns
            bcwidth = SingleObj.GetValue(obj, soi.WidthColumnIndex)
            bcheight = SingleObj.GetValue(obj, soi.HeightColumnIndex)

            if use_polygon:
                # modify the experiment with th respective polygon region
                DetailScan_reloaded = modify_tileexperiment_polygon(DetailScan_reloaded, polyregions[obj],
                                                                    blockindex=0,
                                                                    zpos=zpos)
            else:
                # modify the experiment
                DetailScan_reloaded = modify_tileexperiment_rect(DetailScan_reloaded,
                                                                 blockindex=blockindex,
                                                                 bcwidth=bcwidth,
                                                                 bcheight=bcheight,
                                                                 xpos=xpos,
                                                                 ypos=ypos,
                                                                 zpos=zpos)

        if not DetailIsTileExp:
            print('Detailed Experiment does not contains TileRegions. Nothing to modify.')

        # execute the DetailScan experiment
        print('Running Detail Scan Experiment at new XYZ position.')
        try:
            output_detailscan = Zen.Acquisition.Execute(DetailScan_reloaded)
        except ApplicationException as e:
            print(('Application Exception : ', e.Message))

        # get the image data name
        dtscan_name = output_detailscan.Name

        """
        Modification for multiscene images: container name needs to be part
        of the filename of the detailed Scan.
        First check if Column "Image Scene Container Name" or "WellId" is available
        and then add Container Name to filename.
        """

        wellid_exist, column_wellid = checktableentry(SingleObj, entry2check='ImageSceneContainerName')

        # in case Image Scene Container Name is not defined
        if not wellid_exist:
            message = 'Missing column ImageSceneContainerName in Image Analysis Results.\nPlease Select Features inside the Image Analysis when needed.'
            print(message)
            container_name = 'empty'

        # save the image data to the selected folder and close the image
        output_detailscan.Save(Path.Combine(OutputFolder, output_detailscan.Name))
        output_detailscan.Close()

        # rename the CZI regarding to the object ID - Attention - IDs start with 2 !!!
        if not wellid_exist:
            # no wellID found inside table
            newname_dtscan = 'DTScan_ID_' + str(POI_ID) + '.czi'
        if wellid_exist:
            # wellID was found inside table
            well_id = SingleObj.GetValue(obj, column_wellid)
            newname_dtscan = 'DTScan_Well_' + str(well_id) + '_ID_' + str(POI_ID) + '.czi'

        print(('Renaming File: ' + dtscan_name + ' to: ' + newname_dtscan + '\n'))
        File.Move(Path.Combine(OutputFolder, dtscan_name), Path.Combine(OutputFolder, newname_dtscan))

        ############ OPTIONAL POSTPROCESSING ###############

        if do_postprocess:

            # do the postprocessing
            image2process = Zen.Application.LoadImage(newname_dtscan, False)

            # define the parameters for processing: Topography Export
            parameters = {}
            parameters['noise_low'] = 1
            parameters['noise_high'] = 254
            parameters['outputfolder'] = OutputFolder
            parameters['extension'] = '.sur'

            # run the processing and export and close the image
            image2process = run_postprocessing(image2process, parameters=parameters, func='topography')
            image2process.Close()

if use_apeer:

    # execute detailed experiment at the position of every detected object
    for obj in range(SingleObj.RowCount):

        # get the object information from the position table
        POI_ID = obj

        # get XY-stage position from table
        xpos = SingleObj.GetValue(obj, colID['bbox_center_stageX'])
        ypos = SingleObj.GetValue(obj, colID['bbox_center_stageY'])

        # move to the current position
        Zen.Devices.Stage.MoveTo(xpos + dx_detector, ypos + dy_detector)
        print(('Moving Stage to Object:', POI_ID + 1, ' at :', '%.2f' % xpos, '%.2f' % ypos))

        # try to apply RecallFocus (DF only) when this option is used
        if userecallfocus:
            zpos = apply_recall_focus()

        # if DetailScan is a Tile Experiment
        if DetailIsTileExp:


            # Modify tile center position - get bounding rectangle width and height [microns]
            print('Detailed Experiment contains TileRegions.')
            bcwidth = SingleObj.GetValue(obj, colID['bbox_width_scaled'])
            bcheight = SingleObj.GetValue(obj, colID['bbox_height_scaled'])

            # modify the ZenExperiment for the DetailScan
            DetailScan_reloaded = modify_tileexperiment_rect(DetailScan_reloaded,
                                                             blockindex=blockindex,
                                                             bcwidth=bcwidth,
                                                             bcheight=bcheight,
                                                             xpos=xpos,
                                                             ypos=ypos,
                                                             zpos=zpos)

        if not DetailIsTileExp:
            print('Detailed Experiment does not contains TileRegions. Nothing to modify.')

        # execute the DetailScan experiment
        print('Running Detail Scan Experiment at new XYZ position.')
        try:
            output_detailscan = Zen.Acquisition.Execute(DetailScan_reloaded)
        except ApplicationException as e:
            print(('Application Exception : ', e.Message))

        # get the image data name
        dtscan_name = output_detailscan.Name

        """
        Modification for multiscene images: container name needs to be part
        of the filename of the detailed Scan.
        First check if Column "Image Scene Container Name" or "WellId" is available
        and then add Container Name to filename.
        """

        if 'WellId' in colID:
            print('WellId column found.')
            wellid_exist = True
            column_wellid = colID['WellId']
        else:
            print('WellId column not found.')
            wellid_exist = False
            column_wellid = None

        # in case Image Scene Container Name is not defined
        if not wellid_exist:
            message = 'Missing column WellId in DataTable.\nPlease modify your image analysis inside the APEER module or manually add column.'
            print(message)
            container_name = 'empty'

        # save the image data to the selected folder and close the image
        output_detailscan.Save(Path.Combine(OutputFolder, output_detailscan.Name))
        output_detailscan.Close()

        # rename the CZI regarding to the object ID - Attention - IDs start with 2 !!!
        if not wellid_exist:
            # no wellID found inside table
            newname_dtscan = 'DTScan_ID_' + str(POI_ID) + '.czi'
        if wellid_exist:
            # wellID was found inside table
            well_id = SingleObj.GetValue(obj, column_wellid)
            newname_dtscan = 'DTScan_Well_' + str(well_id) + '_ID_' + str(POI_ID) + '.czi'

        print(('Renaming File: ' + dtscan_name + ' to: ' + newname_dtscan + '\n'))
        File.Move(Path.Combine(OutputFolder, dtscan_name), Path.Combine(OutputFolder, newname_dtscan))

        ############ OPTIONAL POSTPROCESSING ###############

        if do_postprocess:

            # do the postprocessing
            image2process = Zen.Application.LoadImage(newname_dtscan, False)

            # define the parameters for processing: Topography Export
            parameters = {}
            parameters['noise_low'] = 1
            parameters['noise_high'] = 254
            parameters['outputfolder'] = OutputFolder
            parameters['extension'] = '.sur'

            # run the processing and export and close the image
            image2process = run_postprocessing(image2process, parameters=parameters, func='topography')
            image2process.Close()


############# END DETAILED SCAN EXPERIMENT #############

# restore the original OVScan experiment
OVScan_orig = Zen.Acquisition.Experiments.GetByName(OverViewExpName)
OVScan_orig.SetActive()

# delete the temporay experiments when all loops are finished
Zen.Acquisition.Experiments.Delete(OVScan_reloaded)
Zen.Acquisition.Experiments.Delete(DetailScan_reloaded)

# show the overview scan document again at the end
Zen.Application.Documents.ActiveDocument = ovdoc
print('All Positions done. Guided Acquisition Workflow finished.')
