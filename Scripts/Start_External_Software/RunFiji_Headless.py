#################################################################
# File       : RunFiji_Headless.py
# Version    : 0.2
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


import FijiTools as ft
import jsontools as jt
from System.Web.Script.Serialization import JavaScriptSerializer
import sys
import clr
import time
from System.Diagnostics import Process
from System.IO import Directory, Path, File, FileInfo
clr.AddReference('System.Web.Extensions')
sys.path.append(r'c:\External_Python_Scripts_for_OAD')


# clear output console
Zen.Application.MacroEditor.ClearMessages()

# define image
czifile = r'c:\Output\Guided_Acquisition\OverViewScan_Test_raw_stitched.czi'

# load image in Zen
img = Zen.Application.LoadImage(czifile, False)
Zen.Application.Documents.Add(img)


IMAGEJ = 'c:\\Fiji\\ImageJ-win64.exe'
IMAGEJDIR = Path.GetDirectoryName(IMAGEJ)
SCRIPT = 'c:\\Fiji\\scripts\\GuidedAcq_fromZEN.py'

# define script parameters
params = {}
params['IMAGEJ'] = IMAGEJ
params['IMAGEJDIR'] = IMAGEJDIR
params['IMAGEJSCRIPT'] = SCRIPT
params['IMAGE'] = czifile
params['IMAGEDIR'] = Path.GetDirectoryName(czifile)
params['FILEWOEXT'] = Path.GetFileNameWithoutExtension(czifile)
params['JSONPARAMSFILE'] = Path.Combine(params['IMAGEDIR'], params['FILEWOEXT'] + '.json')
params['BIN'] = 4
params['RANKFILTER'] = 'Median'
params['RADIUS'] = 3.0
params['MINSIZE'] = 10000
params['MINCIRC'] = 0.01
params['MAXCIRC'] = 0.99
params['THRESHOLD'] = 'Triangle'
params['THRESHOLD_BGRD'] = 'black'
params['CORRFACTOR'] = 1.0
params['PASAVE'] = True
params['SAVEFORMAT'] = 'ome.tiff'
params['RESULTTABLE'] = ''
params['RESULTIMAGE'] = ''
# additional parameters
params['CenterX'] = img.Metadata.StagePositionMicron.X
params['CenterY'] = img.Metadata.StagePositionMicron.Y
params['Width_Pixel'] = int(img.Metadata.Width)
params['Height_Pixel'] = int(img.Metadata.Height)
params['ScaleX'] = round(img.Metadata.ScalingMicron.X, 3)
params['ScaleY'] = round(img.Metadata.ScalingMicron.Y, 3)
params['ScaleZ'] = round(img.Metadata.ScalingMicron.Z, 3)
params['Width_micron'] = round(params['Width_Pixel'] * img.Metadata.ScalingMicron.X, 3)
params['Height_micron'] = round(params['Height_Pixel'] * img.Metadata.ScalingMicron.Y, 3)

print params

# write JSON file for Fiji
jsonfilepath = jt.write_json(params, jsonfile=params['FILEWOEXT'] + '.json', savepath=params['IMAGEDIR'])
print('Save Data to JSON: ', jsonfilepath)

# configre the options
option1 = "--ij2 --headless --console --run " + SCRIPT + " "
#option1 = "--ij2 --headless --run " + SCRIPT + " "
option2 = '"' + "JSONPARAMFILE=" + "'" + params['JSONPARAMSFILE'] + "'" + '"'
print(option1)
print(option2)
option = option1 + option2
print(option)

fijistr = ft.createFijistring(IMAGEJDIR, SCRIPT, jsonfilepath)
fijistr = fijistr.replace('\\', '\\\\')
print fijistr


# start Fiji script in headless mode
app = Process()
#app.StartInfo.FileName = IMAGEJ
app.StartInfo.FileName = "java"
app.StartInfo.Arguments = fijistr
app.Start()
# wait until the script is finished
app.WaitForExit()
excode = app.ExitCode

"""
# start Fiji and execute the macro
app = Process();
app.StartInfo.FileName = IMAGEJ
app.StartInfo.Arguments = option
app.Start()
# wait until the script is finished
app.WaitForExit()
excode = app.ExitCode
print('Exit Code: ', excode)
"""

# read parameters again after external image analysis
params = jt.readjson(jsonfilepath)

# initialize ZenTable object
SingleObj = ZenTable()

# read the result table and convert into a Zentable
SingleObj = ft.ReadResultTable(params['RESULTTABLE'], 1, '\t', 'FijiTable', SingleObj)

# change the name of the table
SingleObj.Name = Path.GetFileNameWithoutExtension(Path.GetFileName(params['RESULTTABLE']))

# show and save data tables to the specified folder
Zen.Application.Documents.Add(SingleObj)

print('Done.')
