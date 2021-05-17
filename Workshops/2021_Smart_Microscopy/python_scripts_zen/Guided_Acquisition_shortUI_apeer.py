#################################################################
# File       : Guided_Acquisition_shortUI_apeer.py
# Version    : 0.1
# Author     : czsrh, czmla, czkel
# Date       : 14.05.2021
# Insitution : Carl Zeiss Microscopy GmbH
#
# Optimized for the use with Celldiscoverer 7 and DF2, but
# applicable for all motorized stands ruuning in ZEN Blue.
# Please adapt focussing commands, especially FindSurface
# when using with other stands.
#
# 1) - Select Overview Scan Experiment
# 2) - Select appropriate Image Analysis Pipeline
# 3) - Select Detailed Scan Experiment
# 4) - Specify the output folder for the image and data tables
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
import sys

# version number for dialog window
version = 0.1
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

#################   Define APEER module here   ###############

# define a module name and version
module_name = 'SegmentObjects-GA'
module_version = 0

# define the processing parameters (or use the defaults: params.Parameters
my_parameters = {'filter_method': 'none',
                 'filter_size': 5,
                 'threshold_method': 'triangle',
                 'min_objectsize': 50000,
                 'min_holesize': 1000}

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
        print 'Module : ' + module_name + ' found.'
    elif mymodule is None:
        print 'Module : ' + module_name + ' not found.'

    if str(module_version) in mymodule.AvailableVersions:
        print 'Module : ' + module_name + ' Version ' + str(module_version) + ' found.'
        version_found = True
    elif not str(module_version) in mymodule.AvailableVersions:
        print 'Module : ' + module_name + ' Version ' + str(module_version) + ' not found.'

    return mymodule, version_found

##############################################################


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


def checktableentry(datatable, entry2check='ImageSceneContainerName'):

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


def runSWAF_special(SWAF_exp,
                    delay=5,
                    searchStrategy='Full',
                    sampling=ZenSoftwareAutofocusSampling.Coarse,
                    relativeRangeIsAutomatic=False,
                    relativeRangeSize=500,
                    timeout=0):

    # get current z-Position
    zSWAF = Zen.Devices.Focus.ActualPosition
    print('Z-Position before specilal SWAF :', zSWAF)

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

    print('Z-Position after initial SWAF : ', zSWAF)

    return zSWAF


def run_postprocessing(image, parameters={}, func='topography'):

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
        print('Exported to : ', topo_filepath)
        imgtop.Close()

    return image


def apply_recall_focus(zpos):
    try:
        # apply RecallFocus for the current position
        Zen.Acquisition.RecallFocus()
        zpos = Zen.Devices.Focus.ActualPosition
        print('Recall Focus (Definite Focus) applied.')
        print('Updated Z-Position: ', zpos)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
        print('RecallFocus (Definite Focus) failed.')

    print('New Z-Position before Detail Experiment will start:', zpos)

    return zpos


def modify_tileexperiment(tileexp, blockindex=1,
                          bcwidth=1.0,
                          bcheight=1.0,
                          xpos=1.0,
                          ypos=1.0,
                          zpos=1.0):

    print('Width and Height : ', '%.2f' % bcwidth, '%.2f' % bcheight)
    print('Modifying Tile Properties XYZ Position and width and height.')

    # Modify the XYZ position and size of the TileRegion on-the-fly
    print('Starting Z-Position for current Object: ', '%.2f' % zpos)
    print('New Tile Properties: ', '%.2f' % xpos, '%.2f' % ypos, '%.2f' % zpos, '%.2f' % bcwidth, '%.2f' % bcheight)
    tileexp.ClearTileRegionsAndPositions(blockindex)
    try:
        tileexp.AddRectangleTileRegion(blockindex, xpos, ypos, bcwidth, bcheight, zpos)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)

    return tileexp


###########################################################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
#imgfolder = Path.Combine(imgfolder, 'Guided_Acquisition')
imgfolder = r'c:\Output\Guided_Acquisition'
format = '%Y-%m-%d_%H-%M-%S'

# get list with all existing experiments and image analysis setup and a short version of that list
expfiles = Directory.GetFiles(Path.Combine(docfolder, 'Experiment Setups'), '*.czexp')
ipfiles = Directory.GetFiles(Path.Combine(docfolder, 'Image Analysis Settings'), '*.czias')
expfiles_short = getshortfiles(expfiles)
ipfiles_short = getshortfiles(ipfiles)

# Initialize Dialog
GuidedAcqDialog = ZenWindow()
GuidedAcqDialog.Initialize('Guided Acquisition - Version : ' + str(version))
# add components to dialog
GuidedAcqDialog.AddLabel('1) Select Overview Experiment  ------------------------------')
GuidedAcqDialog.AddDropDown('overview_exp', 'Overview Scan Experiment', expfiles_short, 0)
GuidedAcqDialog.AddCheckbox('fs_before_overview', 'OPTION - FindSurface (DF only) before Overview', False)
GuidedAcqDialog.AddCheckbox('SWAF_before_overview', 'OPTION - SWAF before Overview', False)
GuidedAcqDialog.AddIntegerRange('SWAF_ov_initial_range', 'Initial SWAF Range before Overview [micron]', 200, 50, 3000)
GuidedAcqDialog.AddLabel('2) Select Image Analysis to detect objects  ----------------------')
GuidedAcqDialog.AddDropDown('ip_pipe', 'Image Analysis Pieline', ipfiles_short, 0)
GuidedAcqDialog.AddCheckbox('use_apeer_for_IA', 'Use APEER module run run IA instead', True)
GuidedAcqDialog.AddLabel('3) Select DetailScan Experiment  ---------------------------')
GuidedAcqDialog.AddDropDown('detailed_exp', 'Detailed Scan Experiment', expfiles_short, 1)
GuidedAcqDialog.AddCheckbox('fs_before_detail', 'OPTION - FindSurface (DF only) before Detail', False)
GuidedAcqDialog.AddCheckbox('SWAF_before_detail', 'OPTION - SWAF before Detail', False)
GuidedAcqDialog.AddIntegerRange('SWAF_detail_initial_range', 'Initial SWAF Range before Detail [micron]', 100, 10, 1000)
GuidedAcqDialog.AddCheckbox('recallfocus_beforeDT', 'OPTION - Use RecallFocus (DF only) before Detail', False)
GuidedAcqDialog.AddLabel('4) Specify basefolder to save the images ----------------------')
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


# print values
print('Overview Scan Experiment : ' + OverViewExpName)
if not use_apeer:
    print('Image Analysis Pipeline : ' + ImageAS)
if use_apeer:
    print('Use Apeer Module for IA : ')
print('Detailed Scan Experiment : ' + DetailExpName)
print('Output Folder for Data : ' + OutputFolder)
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
    print('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition)

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
    print('Adapted Z-Position of Tile OverView. New Z = ', '%.2f' % znew)

# execute the experiment
print('\nRunning OverviewScan Experiment.\n')
#output_OVScan = Zen.Acquisition.Execute(OVScan_reloaded)
# For testing purposes - Load overview scan image automatically instead of executing the "real" experiment
ovtestimage = r"C:\Users\m1srh\OneDrive - Carl Zeiss AG\Smart_Microscopy_Workshop\datasets\brain_slide\OverViewScan.czi"
output_OVScan = Zen.Application.LoadImage(ovtestimage, False)

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

    # get module and check
    mymodule, version_found = get_module(module_name, module_version=module_version)

    # exit if the check failed
    if mymodule is None or not version_found:
        print 'Module check failed. Exiting.'
        raise SystemExit

    # get the module parameters for the specified module
    params = ZenApeer.Onsite.GetSampleModuleParameters(mymodule.ModuleName, module_version)

    # get the module input programmatically
    module_inputs = get_module_inputs(params)

    # create the required dictionary with the correct key and value
    input_image = {module_inputs[0]: savepath_ovscan}

    # create the path to save the results
    #savepath_apeer = Path.Combine(OutputFolder, 'apeer_results')
    savepath_apeer = OutputFolder

    # create the output directory if not existing already
    if not Directory.Exists(savepath_apeer):
        Directory.CreateDirectory(savepath_apeer)

    # run the local APEER module with using keywords
    runoutputs, status, log = ZenApeer.Onsite.RunModule(moduleName=mymodule.ModuleName,
                                                        moduleVersion=module_version,
                                                        inputs=input_image,
                                                        parameters=my_parameters,
                                                        storagePath=savepath_apeer)

    # get results storage locations
    path_segmented_image = runoutputs['segmented_image']
    path_object_table = runoutputs['objects_table']

    print '--------------   Module Results   ---------------'
    print 'Segmented Image : ', path_segmented_image
    print 'Objects Table : ', path_object_table

    # load the segmented image and make sure the pyramid is calculated
    segmented_image = Zen.Application.LoadImage(path_segmented_image, False)
    Zen.Processing.Utilities.GenerateImagePyramid(segmented_image, ZenBackgroundMode.Black)
    Zen.Application.Documents.Add(segmented_image)

    # auto-display min-max
    ids = segmented_image.DisplaySetting.GetAllChannelIds()
    for id in ids:
        segmented_image.DisplaySetting.SetParameter(id, 'IsAutoApplyEnabled', True)

    # initialize ZenTable object and load CSV file
    SingleObj = ZenTable()
    SingleObj.Load(path_object_table)
    Zen.Application.Documents.Add(SingleObj)

    # get all columns as dict with columnIDs
    colID = get_columns(SingleObj)

    # define the required column names here
    col2check = ('bbox_center_stageX', 'bbox_center_stageX', 'bbox_width_scaled', 'bbox_height_scaled')

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

# test snap to change to the valid settings, e.g. the objetive from the DetailScan
testsnap = Zen.Acquisition.AcquireImage(DetailScan_reloaded)
print('Acquire Test Snap using setting from DetailScan')
testsnap.Close()
# wait for moving hardware due to settings
time.sleep(hwdelay)

if fs_beforeDT:
    try:
        # initial focussing via FindSurface to assure a good starting position
        Zen.Acquisition.FindSurface()
        print('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
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
        print('Application Exception : ', e.Message)
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
        print('Moving Stage to Object ID:', POI_ID, ' at :', '%.2f' % xpos, '%.2f' % ypos)

        # try to apply RecallFocus (DF only) when this option is used
        if userecallfocus:
            zpos = apply_recall_focus(zpos)

        # if DetailScan is a Tile Experiment
        if DetailIsTileExp:

            print('Detailed Experiment contains TileRegions.')
            # Modify tile center position - get bounding rectangle width and height in microns
            bcwidth = SingleObj.GetValue(obj, soi.WidthColumnIndex)
            bcheight = SingleObj.GetValue(obj, soi.HeightColumnIndex)

            # modify the experiment
            DetailScan_reloaded = modify_tileexperiment(DetailScan_reloaded,
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
            print('Application Exception : ', e.Message)

        # get the image data name
        dtscan_name = output_detailscan.Name

        """
        Modification for multiscene images: container name needs to be part
        of the filename of the detailed Scan.
        First check if Column "Image Scene Container Name" or "WellId" is available
        and then add Container Name to filename.
        """

        wellid_exist, column_wellid = checktableentry(SingleObj,
                                                      entry2check='ImageSceneContainerName')

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

        print('Renaming File: ' + dtscan_name + ' to: ' + newname_dtscan + '\n')
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
        print('Moving Stage to Object:', POI_ID + 1, ' at :', '%.2f' % xpos, '%.2f' % ypos)

        # try to apply RecallFocus (DF only) when this option is used
        if userecallfocus:
            zpos = apply_recall_focus(zpos)

        # if DetailScan is a Tile Experiment
        if DetailIsTileExp:

            print('Detailed Experiment contains TileRegions.')
            # Modify tile center position - get bounding rectangle width and height in microns
            bcwidth = SingleObj.GetValue(obj, colID['bbox_width_scaled'])
            bcheight = SingleObj.GetValue(obj, colID['bbox_height_scaled'])

            # modify the experiment
            DetailScan_reloaded = modify_tileexperiment(DetailScan_reloaded,
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
            print('Application Exception : ', e.Message)

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

        print('Renaming File: ' + dtscan_name + ' to: ' + newname_dtscan + '\n')
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
