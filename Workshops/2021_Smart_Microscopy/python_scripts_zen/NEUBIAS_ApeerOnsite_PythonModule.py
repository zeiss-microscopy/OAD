#################################################################
# File        : NEUBIAS_ApeerOnsite_PythonModule.py
# Version     : 0.1
# Author      : czsrh
# Date        : 01.02.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from System.IO import File, Directory, Path

# clear the output console
Zen.Application.MacroEditor.ClearMessages()

# define a module name and version
module_name = 'SegmentObj-GA'
module_version = 0

# get the module parameters for the specified module
params = ZenApeer.Onsite.GetSampleModuleParameters(module_name, module_version)

# show the required module inputs
print '------ Module Inputs ------'
for ip in params.Inputs:
    print ip.Key, ' : ', ip.Value

# sho the required parameters and their defaults
print '------ Module Parameters ------'
for p in params.Parameters:
    print p.Key, ' : ', p.Value
    
print '------ Outputs ------'
for op in params.Outputs.GetEnumerator():
    print op.Key, ' : ', op.Value

# define the list of input images and the allowed file extensions
sourcefolder = r'c:\Users\m1srh\Documents\Testdata_Zeiss\Neubias_Testimages\list_of_images'
itype = '*.ome.tiff'

# create list of images to be processed
imglist = []

for file in Directory.GetFiles(sourcefolder, itype):
    imglist.append(file)

# create the required dict with the correct key and value
# the required value here: list of the input images
input_images = {'list_input_images': imglist}

# define the savepath
savepath = Path.Combine(sourcefolder, 'saved_results')

# create the output directory if not existing
if not Directory.Exists(savepath):
    Directory.CreateDirectory(savepath)

# define the processing parameters (or use the defaults: params.Parameters
my_parameters = {'filtertype': 'Median',
                 'filter_kernel_size': 7}

# or use default parameters from the module
#my_parameters = params.Parameters

# run the local APEER module with using keywords
runoutputs, status, log = ZenApeer.Onsite.RunModule(moduleName=module_name,
                                                    moduleVersion=module_version,
                                                    inputs=input_images,
                                                    parameters=my_parameters,
                                                    storagePath=savepath)

# show output results storage locations
print '--- Results Locations ---'

for result in runoutputs['list_output_files']:
    print 'Result : ', result
