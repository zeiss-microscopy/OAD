#################################################################
# File       : LLS7_BatchProcess.py
# Version    : 1.0
# Author     : aukelgas
# Date       : 29.03.2023
# Institution : Carl Zeiss Microscopy GmbH
#
# Use at your own Risk !!!
# Compatible with ZEN versions 3.7 and higher
# 
# Copyright(c) 2023 Carl Zeiss Microscopy GmbH, Jena, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#
################################################################

from System.IO import File, Directory, Path
import datetime
import os

imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)

Display=ZenWindow()
Display.AddLabel('Select Folder with .czi Files to process')
Display.AddFolderBrowser('CZIFolder', 'CZI Folder', imgfolder)
Results=Display.Show()
if Results.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# read info from GUI
imgfolder = str(Results.GetValue('CZIFolder'))

# clear console output
Zen.Application.MacroEditor.ClearMessages()

OutputFolder = str(imgfolder + "\processed")
Directory.CreateDirectory(OutputFolder)
print('---------------')
print('Created new directory: ', OutputFolder)
print('---------------')

# get list of files to fuse
filelist = os.listdir(imgfolder)
filelist = [i for i in filelist if i.endswith('.czi')]

for i in range (0, len(filelist)):
    imgname = Path.Combine(imgfolder, filelist[i])
    print(imgname)
    Img1 = Zen.Application.LoadImage(imgname, False)
    SubImg = Zen.Processing.Utilities.CreateSubset(Img1)
    Img2 = Zen.Processing.Deconvolution.LatticeLightsheet(SubImg, "D:\zeiss\Documents\Carl Zeiss\ZEN\Documents\Processing Settings\LatticeLightsheet\AnalysisSettings.czips")
    Zen.Application.Documents.Add(Img2)
    Img2.Save(Path.Combine(OutputFolder, filelist[i][:-4] + '_batch-processed.czi'))
    Zen.Application.Documents.GetByName(filelist[i][:-4] + '_batch-processed.czi').Close()
    Img2.Close
