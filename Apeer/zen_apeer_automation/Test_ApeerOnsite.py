#################################################################
# File        : Test_ApeerOnsite.py
# Version     : 0.2
# Author      : czsrh
# Date        : 22.01.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# clear the output console
Zen.Application.MacroEditor.ClearMessages()

# get a list of all local available APEER modules
local_modules = ZenApeer.Onsite.ListLocalModules()

for local_module in local_modules:

    # show the name of the module as a string
    print 'Model Name : ', local_module.ModuleName

    # return string containing all available module versions as a string
    # Draft = 0
    print 'Model Version : ', local_module.AvailableVersions
    print '------------------------------------------------------------------'

# define a module name and version
module_name = 'Particle-Analyzer-Cleanliness'
module_version = 6
module_name = 'Simple Fiji Module - Filter Image'
module_version = 4

# get the module parameters for the specified module
params = ZenApeer.Onsite.GetSampleModuleParameters(module_name, module_version)

print '\n'
print '------ Inputs ------'
for ip in params.Inputs.GetEnumerator():
    print ip.Key, ' : ', ip.Value

print '\n'
print '------ Parameters ------'
for p in params.Parameters.GetEnumerator():
    print p.Key, ' : ', p.Value

print '\n'
print '------ Outputs ------'
for op in params.Outputs.GetEnumerator():
    print op.Key, ' : ', op.Value

# get the complete module description as a string
module_description = ZenApeer.Onsite.GetModuleDescription(module_name, module_version)

print '\n'
print '------ Module Description ------'
print module_description
print '--------------------------------'

# define the input parameters
input_image = {'particle_image': r'C:\Apeer_onsite_results\particle_TC\Filter_with_Particles_small.czi'}
savepath = r'c:\Apeer_onsite_results\particle_TC\saved_results'

mythreshold = 65

# how to define parameters explicitly
my_parameters = {'relative_threshold': mythreshold,
                 'REMOVE_SMALL': False,
                 'REMOVE_SMALL_MIN': 1,
                 'FERETMAX_MINVALUE': 1,
                 'pa_parameter': 'FeretMax',
                 'figure_dpi': 100}


##########################################################

# run the local APEER module without using keywords
out = ZenApeer.Onsite.RunModule(module_name,
                                module_version,
                                input_image,
                                params.Parameters,
                                savepath)

# show output results storage locations
print '\n'
print '------ Results Locations ------'
for o in out.Outputs.GetEnumerator():
    print o.Key, ' : ', o.Value

# show filename of logfile
print '\n'
print '------ Location of Logfile ------'
print out.LogFile

# show state of module completion
print '\n'
print '------ State of Module Completion ------'
print out.State


# run the local APEER module with using keywords
runoutputs, status, log = ZenApeer.Onsite.RunModule(moduleName=module_name,
                                                    moduleVersion=module_version,
                                                    inputs=input_image,
                                                    parameters=my_parameters,
                                                    storagePath=savepath)

# show output results storage locations
print '\n'
print '--- Results Locations ---'
for o in runoutputs.GetEnumerator():
    print o.Key, ' : ', o.Value

# show filename of logfile
print '\n'
print '--- Location of Logfile ---'
print log

# show state of module completion
print '\n'
print '--- State of Module Completion ---'
print status
