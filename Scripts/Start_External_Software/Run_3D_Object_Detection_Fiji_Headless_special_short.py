#################################################################
# File       : Run_3D_Object_Detection_Fiji_Headless_special.py
# Version    : 0.5
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


from System.Web.Script.Serialization import JavaScriptSerializer
from System.IO import Directory, Path, File, FileInfo
from System.Diagnostics import Process
import time
import clr
import FijiTools as ft
import jsontools as jt
import ConvertTools as ct
import sys
# adapt this path depending on your system
sys.path.append(r'c:\External_Python_Scripts_for_OAD')
clr.AddReference('System.Web.Extensions')

# clear output console
Zen.Application.MacroEditor.ClearMessages()

# define image
czifile = r'c:\Output\3d_workflow\XRM_P2.czi'

# load image in Zen
img = Zen.Application.LoadImage(czifile, False)
Zen.Application.Documents.Add(img)
metadata = jt.fill_metadata(img)


IMAGEJ = 'c:\\Fiji\\ImageJ-win64.exe'
IMAGEJDIR = Path.GetDirectoryName(IMAGEJ)
SCRIPT = 'c:\\Fiji\\scripts\\3d_analytics_fromZEN.py'

# define script parameters
params = {}
params['IMAGEJ'] = IMAGEJ
params['IMAGEJSCRIPT'] = SCRIPT
params['IMAGE'] = czifile
params['IMAGEDIR'] = Path.GetDirectoryName(czifile)
params['FILEWOEXT'] = Path.GetFileNameWithoutExtension(czifile)
params['HEADLESS'] = True

# define processing parameters
params['JSONPARAMSFILE'] = Path.Combine(params['IMAGEDIR'], params['FILEWOEXT'] + '.json')
params['LABEL_CONNECT'] = 6
params['LABEL_COLORIZE'] = False
params['MINVOXSIZE'] = 1000

# define outputs
params['SAVEFORMAT'] = 'ome.tiff'
params['RESULTTABLE'] = ''
params['RESULTIMAGE'] = ''

# update dictionary
params.update(metadata)

print(params)

# write JSON file for Fiji
jsonfilepath = jt.write_json(params, jsonfile=params['FILEWOEXT'] + '.json', savepath=params['IMAGEDIR'])
print(('Save Data to JSON: ', jsonfilepath))

# configre the options
option1 = "--ij2 --headless --console --run " + SCRIPT + " "
option2 = '"' + "JSONPARAMFILE=" + "'" + params['JSONPARAMSFILE'] + "'" + '"'
print(option1)
print(option2)
option = option1 + option2
print(option)

fijistr = ft.createFijistring(IMAGEJDIR, SCRIPT, jsonfilepath)
fijistr = fijistr.replace('\\', '\\\\')
print(fijistr)

# start Fiji script in headless mode
app = Process()
#app.StartInfo.FileName = IMAGEJ
app.StartInfo.FileName = "java"
app.StartInfo.Arguments = fijistr
app.Start()
# wait until the script is finished
app.WaitForExit()
excode = app.ExitCode

print(('Exit Code: ', excode))
print('Fiji Analysis Run Finished.')

# read metadata JSON - the name of the file must be specified correctly
md_out = jt.readjson(jsonfilepath)
print(('ResultTable: ', md_out['RESULTTABLE']))

# initialize ZenTable object
SingleObj = ZenTable()
# read the result table and convert into a ZenTable
SingleObj = ct.ReadResultTable(md_out['RESULTTABLE'], 1, '\t', 'FijiTable', SingleObj)
# change the name of the table
SingleObj.Name = Path.GetFileNameWithoutExtension(Path.GetFileName(md_out['RESULTTABLE']))
# show and save data tables to the specified folder
Zen.Application.Documents.Add(SingleObj)

print('Done.')
