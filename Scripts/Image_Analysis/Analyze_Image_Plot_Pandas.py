#################################################################
# File       : Analyze_Image_Plot_Pandas.py
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

# clear output
Zen.Application.MacroEditor.ClearMessages()

# define the external plot script or tool
pythonexe = r'C:\Anaconda3\python.exe'
script = r'c:\External_Python_Scripts_for_OAD\test_wellplate_from_ZEN.py'

if not File.Exists(pythonexe):
    message = 'Python Executable not found.'
    print(message)
    raise SystemExit

if File.Exists(pythonexe):
    message = 'Python Executable found.'
    print(message)

if not File.Exists(script):
    message = 'Plot Script not found.'
    print(message)
    raise SystemExit

if File.Exists(script):
    message = 'Plot Script found.'
    print(message)


# load image and add it to ZEN and get the image path
image_to_analyze = r'c:\Testdata\Translocation_comb_96_5ms.czi'
image = Zen.Application.LoadImage(image_to_analyze)
Zen.Application.Documents.Add(image)
outputpath = Path.GetDirectoryName(image_to_analyze)
resultname = Path.GetFileNameWithoutExtension(image.Name)

# define the image analysis setting and run the image analysis on the active image
iasfilename = r'c:\Image Analysis Settings\Translocation_ZEN2.6.czias'
ias = ZenImageAnalysisSetting()
ias.Load(iasfilename)
Zen.Analyzing.Analyze(image, ias)

"""
# Create data list with results for all regions (e.g. all nuclei)
table_all = Zen.Analyzing.CreateRegionsTable(image)
Zen.Application.Documents.Add(table_all)
# Create data list with results for each region (e.g. every single nucleus)
table_single = Zen.Analyzing.CreateRegionTable(image)
Zen.Application.Documents.Add(table_single)
"""

# For ZOI-Image Analysis Settings need to get the results for the Primary Objects

# Create data list with reults for all primary objects
table_all = Zen.Analyzing.CreateRegionsTable(image, "Primary Objects")
# Zen.Application.Documents.Add(table_all)

# Create data list with results for each primary object
table_single = Zen.Analyzing.CreateRegionTable(image, "Primary Object")
# Zen.Application.Documents.Add(table_single)


# Save both data lists as CSV files
table_all_filename = Path.Combine(outputpath, resultname + '_All.csv')
table_all.Save(table_all_filename)
table_single_filename = Path.Combine(outputpath,  resultname + '_Single.csv')
table_single.Save(table_single_filename)

# close the image and image analysis setting
# image.Close()
ias.Close()

# define the actual CSV file and the parameters
#csvfile = r'c:\Users\m1srh\Documents\Testdata_Zeiss\Translocation_ZOI\Translocation_comb_96_5ms_Single.csv'
#csvfile = r'c:\Users\m1srh\Documents\Testdata_Zeiss\Translocation_ZOI\_Primary Object.csv'

csvfile = Path.Combine(outputpath, table_single_filename)
print(csvfile)
# this depends on the actual CZIAS and the import of the CSV table in python
parameter2display = 'Ratio'
params = ' -f ' + '"' + csvfile + '"' + ' -w 96' + ' -p ' + parameter2display + ' -sp False -dpi 100'
print(params)

# start the data display script as an external application
app = Process()
app.StartInfo.FileName = pythonexe
app.StartInfo.Arguments = script + params
app.Start()
app.WaitForExit()

savename_all = Path.Combine(Path.GetDirectoryName(image_to_analyze),
                            Path.GetFileNameWithoutExtension(image_to_analyze) + '_Single_HM_all.png')
savename_single = Path.Combine(Path.GetDirectoryName(image_to_analyze), Path.GetFileNameWithoutExtension(
    image_to_analyze) + '_Single_HM_' + parameter2display + '.png')
print(savename_all)
print(savename_single)
print('Showing saved figure in ZEN.')

if File.Exists(savename_all):
    plotfigure1 = Zen.Application.LoadImage(savename_all, False)
    plotfigure2 = Zen.Application.LoadImage(savename_single, False)
    Zen.Application.Documents.Add(plotfigure1)
    Zen.Application.Documents.Add(plotfigure2)
else:
    print('Saved figure not found.')

print('Done.')
