#################################################################
# File       : RMI_Nanoparticle_Analysis.py
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


from System.Diagnostics import Process
from System.IO import File, Path, Directory
import time
import re


show_tables = False
close_image = False
analyze_inplace = True

# clear output
Zen.Application.MacroEditor.ClearMessages()

# specify image
image_to_analyze = r'c:\Data\Nanoparticles.tif'

# define the image analysis setting
iasfilename = r'c:\Users\XYZ\Documents\Carl Zeiss\ZEN\Documents\Image Analysis Settings\Nanoparticle Segmentation ZEN25.czias'

# define the external plot script or tool
pythonexe = r'C:\Anaconda3\python.exe'
script = r'c:\Data\External_Python_Scripts_for_OAD\RMI_plot_nanoparticles.py'

# load imnage
image = Zen.Application.LoadImage(image_to_analyze)
Zen.Application.Documents.Add(image)
outputpath = Path.GetDirectoryName(image_to_analyze)
resultname = Path.GetFileNameWithoutExtension(image.Name)

# loead CZIAS image analysis setting
ias = ZenImageAnalysisSetting()
ias.Load(iasfilename)
classnames = ias.GetRegionClassNames()

if analyze_inplace:
    Zen.Analyzing.Analyze(image, ias)

# run the image analyis pipeline and directly create a table
all_tables = Zen.Analyzing.AnalyzeToTable(image, ias)

for class_table in all_tables:

    if show_tables:
        Zen.Application.Documents.Add(class_table)

    print('Saving table for class: ', class_table.Name + '.csv')
    class_table_filename = Path.Combine(outputpath,  class_table.Name + '.csv')
    class_table.Save(class_table_filename)

    if not show_tables:
        class_table.Close()

# close the image and image analysis setting
if close_image:
    image.Close()

# close image analysis setting
ias.Close()

#############################################################################

# define parameters etc.
datatable = 'Nanoparticles.csv'
csvfile = Path.Combine(outputpath, datatable)
parameter2display = 'Area::Area!!R'
title = 'Size Distribution'
xlabel = 'Area [micron**2]'
bins = 10
savename = 'Size Distribution.png'
savename_complete = Path.Combine(Path.GetDirectoryName(csvfile), savename)
print 'Savename: ', savename_complete

# construct the command line string
params = ' -f '+'"'+csvfile+'"'+' -p ' + '"'+parameter2display+'"'+' -sp False -dpi 100' + \
    ' -t '+'"'+title+'"'+' -lx '+'"'+xlabel+'"'+' -bins '+str(bins)+' -s '+'"'+savename+'"'
print 'Parameter: ', params

# start the data display script as an external application
app = Process()
app.StartInfo.FileName = pythonexe
app.StartInfo.Arguments = script + params
app.Start()
app.WaitForExit()

print 'Trying to show figure in ZEN.'

if File.Exists(savename_complete):
    plotfigure = Zen.Application.LoadImage(savename_complete, False)
    Zen.Application.Documents.Add(plotfigure)
else:
    print 'Saved figure not found.'

print 'Done and Exit.'
