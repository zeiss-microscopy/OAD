#################################################################
# File        : NEUBIAS_ApeerOnsite_FijiModule.py
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
module_name = 'Simple Fiji Module - Filter Image'
module_version = 4

# get the module parameters for the specified module
params = ZenApeer.Onsite.GetSampleModuleParameters(module_name, module_version)

# show the required module inputs
print '------ Module Inputs ------'
for ip in params.Inputs:
    print ip.Key, ' : ', ip.Value

# show the required parameters and their defaults
print '------ Module Parameters ------'
for p in params.Parameters:
    print p.Key, ' : ', p.Value

# define the input file
input_image = {'IMAGEPATH': r'C:\Users\m1srh\Documents\Testdata_Zeiss\Neubias_Testimages\fiji_filter_image\01_3CH.ome.tiff'}
savepath = Path.Combine(Path.GetDirectoryName(input_image['IMAGEPATH']), 'saved_results')

# create the output directory if not existing
if not Directory.Exists(savepath):
    Directory.CreateDirectory(savepath)

# define the processing parameters (or use the defaults: params.Parameters
my_parameters = {'FILTERTYPE': 'MEDIAN',
                 'FILTER_RADIUS': 7}

# or use default parameters from the module
my_parameters = params.Parameters

# run the local APEER module with using keywords
runoutputs, status, log = ZenApeer.Onsite.RunModule(moduleName=module_name,
                                                    moduleVersion=module_version,
                                                    inputs=input_image,
                                                    parameters=my_parameters,
                                                    storagePath=savepath)

# show output results storage locations
print '--- Results Locations ---'
for o in runoutputs.GetEnumerator():
    print o.Key, ' : ', o.Value

# open the filtered image in Zen
filtered_image = Zen.Application.LoadImage(runoutputs['FILTERED_IMAGE'])
Zen.Application.Documents.Add(filtered_image)
