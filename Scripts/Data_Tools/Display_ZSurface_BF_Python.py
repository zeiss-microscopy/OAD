#################################################################
# File       : Display_ZSurface_BF_Python.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

"""  

The script call a batch file that internally calls a python script.
This python script used python-bioformats to read the CZI and extract
the planetable data.

For whatever reason calling a python script that start a JVM cannot be
started directly from within an OAD script (at least I could not figure
it out yet ...) while normal python scripts work fine withou any problems.

The advantage of that additional layer using the batch script
is the possibility to use it directly even without ZEN is
running on other microscope image files as well.

"""

from System.IO import Path, File, Directory, FileInfo
from System.Diagnostics import Process
import os

# clear console output
Zen.Application.MacroEditor.ClearMessages()

CZIfiles_short = []
CZIdict = {}
# get all open documents
opendocs = Zen.Application.Documents
for doc in opendocs:
    image = Zen.Application.Documents.GetByName(doc.Name)
    if image.FileName.EndsWith('.czi'):
        # get the filename of the current document only when it ends with '.czi'
        CZIfiles_short.append(Path.GetFileName(image.FileName))
        CZIdict[Path.GetFileName(image.FileName)] = image.FileName

# define possible separators
separator_list = ['tab', 'comma', 'semicolon']
# define image formats for saving figure
saveformat_list = ['jpg', 'png', 'tiff']

# this location might have to be adapted
SCRIPT = r'showZsurface.bat'

# activate GUI
wd = ZenWindow()
wd.Initialize('PlaneTable Tool')
# add components to dialog
wd.AddLabel('Extract PlaneData from CZI using Python-BioFormats.')
wd.AddDropDown('czi', 'Select CZI Image Data', CZIfiles_short, 0)
wd.AddCheckbox('csv_opt', 'Save PlaneTable as CSV', True)
wd.AddDropDown('sep_opt', 'Select separator for CSV file', separator_list, 0)
wd.AddCheckbox('save_opt', 'Save figure as PNG', True)
wd.AddDropDown('format_opt', 'Select image format for saving', saveformat_list, 0)
wd.AddCheckbox('show_opt', 'Show additional surfcae plot', False)
wd.AddCheckbox('show_fig', 'Open saved figure in ZEN', True)
# show the window
result = wd.Show()
# check, if Cancel button was clicked
if result.HasCanceled:
    sys.exit('Macro aborted with Cancel!')

# get the input values and store them
cziname = result.GetValue('czi')
wcsv_result = result.GetValue('csv_opt')
separator = result.GetValue('sep_opt')
save_result = result.GetValue('save_opt')
surface_result = result.GetValue('show_opt')
show_fig_result = result.GetValue('show_fig')
saveformat_result = result.GetValue('format_opt')

if cziname.isspace():
    sys.exit('Macro aborted with Cancel!')


# convert boolean values to strings that can be passed as cmd parameters
if wcsv_result:
    writecsv = 'True'
elif not wcsv_result:
    writecsv = 'False'

if save_result:
    save = 'True'
elif not save_result:
    save = 'False'

if surface_result:
    surface = 'True'
elif not surface_result:
    surface = 'False'


# define the actual CZI file to be analyzed
czifile = CZIdict[cziname]
czifile_cmd = '"' + CZIdict[cziname] + '"'
params = czifile_cmd + ' ' + writecsv + ' ' + separator + ' ' + save + ' ' + saveformat_result + ' ' + surface
print('CZI file to be used: ', czifile)
print('Parameter : ', params)

# when option to save the figure was set
if save_result:

    savename = Path.GetFileNameWithoutExtension(czifile) + '_planetable_XYZ-Pos.' + saveformat_result
    savename_full = Path.Combine(Path.GetDirectoryName(czifile), savename)
    print('Savename: ', savename_full)
    # delete older version of the figure if existing
    if File.Exists(savename_full):
        File.Delete(savename_full)
        print('Deleted older figure: ', savename_full)

# start the data display script as an external application
app = Process()
app.StartInfo.FileName = SCRIPT
app.StartInfo.Arguments = params
app.Start()
# waits until the python figure was closed
app.WaitForExit()

if show_fig_result:
    print('Showing saved figure in ZEN.')
    if File.Exists(savename_full):
        plotfigure = Zen.Application.LoadImage(savename_full, False)
        Zen.Application.Documents.Add(plotfigure)
    else:
        print('Saved figure not found.')

print('Done.')
