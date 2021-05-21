#################################################################
# File        : ApeerOnsite_RunModule.py
# Version     : 0.3
# Author      : czsrh
# Date        : 21.05.2021
# Institution : Carl Zeiss Microscopy GmbH
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

from System.IO import File, Directory, Path
from System import ApplicationException

# clear the output console
Zen.Application.MacroEditor.ClearMessages()


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


###########################################################################################

# define the input image
czifile = r'c:\Users\m1srh\OneDrive - Carl Zeiss AG\Smart_Microscopy_Workshop\datasets\brain_slide\OverViewScan.czi'

# run from seeting or define parameters manually
run_from_setting = True

# create empyt dictionary for the parameters
parameters = {}

if run_from_setting:

    # name of the APEER module seeting
    apeer_modulesetting = 'SegmentObjects_Brainslide'

    # read it from settings file
    ams = ZenApeer.Onsite.ModuleSetting()
    ams.Load(apeer_modulesetting)

    print '-----   Show APEER Module Setting   -----'
    print 'Module Name    : ', ams.ModuleName
    print 'Module Version : ', ams.ModuleVersion
    print 'Module Parameters    : ', ams.Parameters

    module_name = ams.ModuleName
    module_version = ams.ModuleVersion
    parameters = ams.Parameters

if not run_from_setting:

    # define a module name and version
    module_name = 'SegmentObjects-GA'  # use without file extension *.czams
    module_version = 3  # 0 = draft

    # define the processing parameters (or use the defaults: params.Parameters
    parameters = {'filter_method': 'none',
                  'filter_size': 5,
                  'threshold_method': 'triangle',
                  'min_objectsize': 50000,
                  'max_holesize': 1000}

# get module and check
mymodule, version_found = get_module(module_name, module_version=module_version)

# exit if the check failed
if mymodule is None or not version_found:
    print 'Module check failed. Exiting.'
    raise SystemExit

# get the module parameters for the specified module
module_params = ZenApeer.Onsite.GetSampleModuleParameters(module_name, module_version)

# show the required module inputs
print '------ Module Inputs ------'
for ip in module_params.Inputs:
    print ip.Key

# sho the required parameters and their defaults
print '------ Module Parameters ------'
for p in module_params.Parameters:
    print p.Key

print '------ Outputs ------'
for op in module_params.Outputs.GetEnumerator():
    print op.Key


# get the module input programmatically
module_inputs = get_module_inputs(module_params)

# create the required dictionary with the correct key and value for the input
input_image = {module_inputs[0]: czifile}

# create the path to save the results
savepath = Path.Combine(Path.GetDirectoryName(czifile), 'saved_results')

# create the output directory if not existing already
if not Directory.Exists(savepath):
    Directory.CreateDirectory(savepath)


if not run_from_setting:

    # define the processing parameters (or use the defaults: params.Parameters
    parameters = {'filter_method': 'none',
                  'filter_size': 5,
                  'threshold_method': 'triangle',
                  'min_objectsize': 50000,
                  'max_holesize': 1000}

    # or use default parameters from the module
    #my_parameters = params.Parameters


# run the local APEER module with using keywords
runoutputs, status, log = ZenApeer.Onsite.RunModule(module_name,
                                                    moduleVersion=module_version,
                                                    inputs=input_image,
                                                    parameters=parameters,
                                                    storagePath=savepath)

print '--------------   Module Results   ---------------'
for op in runoutputs.GetEnumerator():
    print op.Key, ' : ', op.Value

if not runoutputs.ContainsKey('segmented_image'):
    print 'No output : segmented_image'
    raise SystemExit

if not runoutputs.ContainsKey('objects_table'):
    print 'No output : objects_table'
    raise SystemExit

# load the segmented image and make sure the pyramid is calculated
segmented_image = Zen.Application.LoadImage(runoutputs['segmented_image'], False)
Zen.Processing.Utilities.GenerateImagePyramid(segmented_image, ZenBackgroundMode.Black)
Zen.Application.Save(segmented_image, segmented_image.FileName[:-8] + 'czi', False)
Zen.Application.Documents.Add(segmented_image)

# auto-display min-max
ids = segmented_image.DisplaySetting.GetAllChannelIds()
for id in ids:
    segmented_image.DisplaySetting.SetParameter(id, 'IsAutoApplyEnabled', True)

# initialize ZenTable object and load CSV file
object_table = ZenTable()
object_table.Load(runoutputs['objects_table'])
Zen.Application.Documents.Add(object_table)

# get all columns as dict with columnIDs
colID = get_columns(object_table)
col2check = ('bbox_center_stageX', 'bbox_center_stageY', 'bbox_width_scaled', 'bbox_height_scaled')
if all(key in colID for key in col2check):
    print('All required columns found.')
else:
    print('Not All required columns found. Exiting.')
    raise SystemExit


# execute detailed experiment at the position of every detected object
for obj in range(object_table.RowCount):

    # get the object information from the position table - make sure to use the correct names !
    xpos = object_table.GetValue(obj, colID['bbox_center_stageX'])  # get X-position from table
    ypos = object_table.GetValue(obj, colID['bbox_center_stageY'])  # get Y-position from table
    bwidth = object_table.GetValue(obj, colID['bbox_width_scaled'])  # get the width of the bounding box
    bheight = object_table.GetValue(obj, colID['bbox_height_scaled'])  # get the height of the bounding box

    print 'Moving Stage to Object:', obj + 1, ' at :', '{:.2f}'.format(xpos), '{:.2f}'.format(ypos)


if 'WellId' in colID:
    print('WellId column found.')
    well_exist = True
    column_wellid = colID['WellId']
else:
    print('WellId column not found.')
    well_exist = False
    column_wellid = None

print well_exist, column_wellid
