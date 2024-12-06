#################################################################
# File        : Create_Z_stack.pyNEUBIAS_ApeerOnsite_FijiModule.py
# Version     : 0.1
# Author      : czspr
# Date        : 16.03.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# - create z stack from folder
# - only works with czi files
#
# Copyright(c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# Activate IO library
from System.IO import File, Directory, FileInfo, Path

# create window
window = ZenWindow()
Images = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.Images)
window.Initialize('Create Z stack from czi files')
window.AddFolderBrowser('sourcefolder','Source folder                   ',)
window.AddFolderBrowser('destfolder','Destination folder            ',)

## do setup
result=window.Show()
## check, if Cancel button was clicked
if result.HasCanceled == True:
    sys.exit('Macro aborted with Cancel!')
## get string name of source folder/destination folder
strFolder = str(result.GetValue('sourcefolder'))
newstrFolder = str(result.GetValue('destfolder'))
## Check, if path exists
if (Directory.Exists(strFolder)== False):
    strMessage = 'Path: ' + strFolder + ' does not exist!\nRestart macro and select an existing path!'
    sys.exit(strMessage)
## Check, if newPath exists
if (Directory.Exists(newstrFolder)== False):
    strMessage = 'Path: ' + newstrFolder + ' does not exist!\nRestart macro and select an existing path!'
    sys.exit(strMessage)

imgSeries = ZenImage()

t = 0
c = 0
z = 0

files = Directory.GetFiles(strFolder, "*czi")

for z in range(0, files.Length):
    #--- Get the next image file ---
    file = files[z]
    fileInfo = FileInfo(file)
    strFilenameFullPath = strFolder + "\\" + fileInfo.Name
    img = Zen.Application.LoadImage(strFilenameFullPath, False)
    # separate channels
    for c in range(0, img.Bounds.SizeC):
        channelImage = img.CreateSubImage('C(' + str(c+1) + ')')
        #--- Add image to series ---
        imgSeries.AddSubImage(channelImage, t, c, z)
    #--- Clean up ---
    img.Close()

#--- Show and save the resulting series image ---
Zen.Application.Documents.Add(imgSeries)
imgSeriesNameWE = fileInfo.Name.Substring(0,fileInfo.Name.Length-6)
newimgSeriesName = imgSeriesNameWE + '_ZStack.czi'
imgSeriefullName = Path.Combine(newstrFolder, newimgSeriesName) 
imgSeries.Save(imgSeriefullName)
