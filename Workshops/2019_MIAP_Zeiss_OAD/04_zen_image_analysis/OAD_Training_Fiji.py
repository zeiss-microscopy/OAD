#######################################################
## M I S C E L L A N E O U S
##
## Macro name: OAD_Training_Fiji
##
## Required files: CZI_DimorderTZC.czi, Open_CZI_and_MaxInt_Save.ijm
## Required demo files: None
##
## Required module/licence:
##
## DESCRIPTION: Start Fiji and load results in ZEN
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################

from System.Diagnostics import Process
from System.IO import File

img = ZenImage()
img.Load("C:\\Training\\CZI_DimorderTZC.czi")
Zen.Application.Documents.Add(img)

filename = img.FileName
# use the absolute path; this works always 
exeloc = 'C:\Fiji_Sebi\ImageJ-win64.exe'

# specify the Fiji macro that will be appplied
macro = r'-macro C:\Training\Open_CZI_and_MaxInt_Save.ijm'

# define parameters for the Fiji macro
params =  macro + ' ' + filename

# start Fiji, open the data set and execute the macro
app = Process();
app.StartInfo.FileName = exeloc
app.StartInfo.Arguments = params
app.Start()
app.WaitForExit()

savename =  "C:\\Training\\fiji.png"

if File.Exists(savename):
    fiji_result = Zen.Application.LoadImage(savename, False)
    Zen.Application.Documents.Add(fiji_result)
else:
    print 'Saved figure not found.'

<