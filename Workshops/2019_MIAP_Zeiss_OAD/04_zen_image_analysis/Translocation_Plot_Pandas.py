
#######################################################
## A C Q U I S I T I O N - A U T O F O C U S
##
## Macro name: Translocation_Plot_Pandas.py
##
## Required files: test_wellplate_from_ZEN.PY, wellplate_tools_pandas.py
## Required demo files: None
##
## Required module/licence:
##
## DESCRIPTION: Analyze a Translocation Assay, Plot Images, Create Excel-File
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################


from System.Diagnostics import Process
from System.IO import File, Path, Directory
import time

# clear macro editor output
Zen.Application.MacroEditor.ClearMessages()

# define the external plot script or tool
#pythonexe =  r'C:\ProgramData\Anaconda3\python.exe' # Anaconda
pythonexe = r'C:\Program Files\Carl Zeiss\ZeissPython\Py20190211\env\python.exe' # Zeisspython
# requires progressbar2 libary: "C:\Program Files\Carl Zeiss\ZeissPython\Py20190211\env\python.exe" -m pip install progressbar2 #
script = r'C:\testdata\Broadinstitute\test_wellplate_from_ZEN.PY'

if File.Exists(pythonexe) is False:
    message = 'Python Executable not found.'
    print(message)
    raise SystemExit

if File.Exists(pythonexe) is True:
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
image_to_analyze = r'C:\testdata\Broadinstitute\Translocation_comb_96_5ms.czi'
image = Zen.Application.LoadImage(image_to_analyze)
Zen.Application.Documents.Add(image)
outputpath = Path.GetDirectoryName(image_to_analyze)
resultname = Path.GetFileNameWithoutExtension(image.Name)

# define the image analysis setting and run the image analysis on the active image. For Translocation Assay use:
# ID parent | ID | Image Scene container Name | Image Scene Row | Image Scene Column | Index | Area | NucMeanDapi | NucMeanGFP | RingMeanGFP | RingArea

# Load image analysis setting and perform image anlaysis
iasfilename = r'C:\Users\M1MALANG\Documents\Carl Zeiss\ZEN\Documents\Image Analysis Settings\Translocation_26.czias'
ias = ZenImageAnalysisSetting()
ias.Load(iasfilename)
Zen.Analyzing.Analyze(image,ias)

# For ZOI-Image Analysis Settings need to get the results for the Primary Objects

# Create data list with results for each primary object
table_single = Zen.Analyzing.CreateRegionTable(image, "Primary Object")
#Zen.Application.Documents.Add(table_single)

# Save data list as CSV file
#table_all_filename = Path.Combine(outputpath, resultname + '_All.csv')
#table_all.Save(table_all_filename)
table_single_filename = Path.Combine(outputpath,  resultname + '_Single.csv')
table_single.Save(table_single_filename)

# close the image and image analysis setting
#image.Close()
ias.Close()

# define the actual CSV file and the parameters
csvfile = Path.Combine(outputpath, table_single_filename)
print csvfile


# this depends on the actual CZIAS and the import of the CSV table in python
parameter2display = 'Ratio'
#params = ' -f ' + csvfile + ' -w 96' + ' -p ' + parameter2display + ' -sp False -dpi 100 -xlsx True'
params = ' -f ' + csvfile + ' -w 96' + ' -p ' + parameter2display + ' -sp False -dpi 100'
print params

## start the data display script as an external application
app = Process();
app.StartInfo.FileName = pythonexe
app.StartInfo.Arguments = script + params
app.Start()
app.WaitForExit()


savename_all =  Path.Combine(Path.GetDirectoryName(image_to_analyze), Path.GetFileNameWithoutExtension(image_to_analyze) + '_Single_HM_all.png')
savename_single = Path.Combine(Path.GetDirectoryName(image_to_analyze), Path.GetFileNameWithoutExtension(image_to_analyze) + '_Single_HM_' + parameter2display + '.png')
print(savename_all +'\n' + savename_single + '\nShowing saved figure in ZEN.')


if File.Exists(savename_all):
    plotfigure1 = Zen.Application.LoadImage(savename_all, False)
    plotfigure2 = Zen.Application.LoadImage(savename_single, False)
    Zen.Application.Documents.Add(plotfigure1)
    Zen.Application.Documents.Add(plotfigure2)
else:
    print 'Saved figure not found.'

print 'Done.'

