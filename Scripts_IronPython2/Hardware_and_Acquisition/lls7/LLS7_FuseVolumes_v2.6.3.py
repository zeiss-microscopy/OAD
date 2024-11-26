#################################################################
# File       : LLS7_FuseVolumes.py
# Version    : 2.5
# Author     : aukelgas
# Date       : 13.11.2022
# Institution : Carl Zeiss Microscopy GmbH
#
# Use at your own Risk !!!
# Compatible with ZEN versions 3.4 and higher (dual cam processing only supported with ZEN3.6 HF1)
# 
# Copyright(c) 2022 Carl Zeiss Microscopy GmbH, Jena, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#
# v2.5 allows to fuse volumes recorded with LLS7_VolumeStacking_v2.5.py after manual processing of individual volume stacks (such as deconvolution or spectral unmixing. 
# Note that deskew + cover glass transformation of each volume stack is mandatory before using LLS7_FuseVolumes.py. All volume stacks to be fused need to be in a single folder with no other .czi files in that same folder.
#
# v2.6 allows to fuse files processed with Direct Processing instead of Autosave within the macro
#
################################################################

from System.IO import File, Directory, Path
import datetime
import os

imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)

Display=ZenWindow()
Display.AddLabel('Select Folder with .czi Files to fuse')
Display.AddFolderBrowser('CZIFolder', 'CZI Folder', imgfolder)
Display.AddTextBox('TimePoints', 'Number of Time Points recorded', 1)     # Number of time points recorded
Display.AddTextBox('Positions', 'Number of Positions recorded', 1)     # Number of positions recorded
Display.AddCheckbox('DP', 'Processed with Direct Processing?', True)
Results=Display.Show()
if Results.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# read info from GUI
imgfolder = str(Results.GetValue('CZIFolder'))
TP = Results.GetValue('TimePoints')
P = Results.GetValue('Positions')
DP = Results.GetValue('DP')

ttt = 100
j = 0

OutputFolder = str(imgfolder + "\concatenated")
Directory.CreateDirectory(OutputFolder)
print('---------------')
print('Created new directory: ', OutputFolder)
print('---------------')

# get list of files to fuse
filelist = os.listdir(imgfolder)
filelist = [i for i in filelist if i.endswith('.czi')]

# get number of stacks
NumberOfStacks = len(filelist)/TP/P
print(NumberOfStacks)

# load first image to get parameters
imgname = Path.Combine(imgfolder, filelist[0])
Img = Zen.Application.LoadImage(imgname, False)

SizeZ = Img.Bounds.SizeZ-1;
SizeX = Img.Bounds.SizeX;
SizeY = Img.Bounds.SizeY;
SizeC = Img.Bounds.SizeC;
PixelSizeXY = Img.Scaling.X
PixelSizeZ = Img.Scaling.Z
#print(PixelSizeXY)
print(SizeZ)
Img.Close()

if DP == True:
    while ttt &lt; TP+100:
        for s in range (0, P):
            for i in range (10, NumberOfStacks+10):
                if s &lt; 9:
                    stack_name = str('position0' + str(s+1) + '_TP' + str(ttt) + str(i) + '_processed_' + filelist[j][:-4]) + '.czi'
                    #print(stack_name)
                    #print(Path.Combine(imgfolder, filelist[j]))
                    #print(Path.Combine(imgfolder, stack_name))
                    os.rename(Path.Combine(imgfolder, filelist[j]), Path.Combine(imgfolder, stack_name))
                    j = j+1
                else:
                    stack_name = str('position' + str(s+1) + '_TP' + str(ttt) + str(i) + '_processed_' + filelist[j][:-4]) + '.czi'
                    #print(stack_name)
                    #print(Path.Combine(imgfolder, filelist[j]))
                    #print(Path.Combine(imgfolder, stack_name))
                    os.rename(Path.Combine(imgfolder, filelist[j]), Path.Combine(imgfolder, stack_name))
                    j = j+1
        ttt = ttt + 1

# get list of files to fuse
filelist = os.listdir(imgfolder)
filelist = [i for i in filelist if i.endswith('.czi')]

#Copy image
for l in range (0, P):
    #FinalImage = ZenImage(Img.Bounds.SizeX, Img.Bounds.SizeY,ZenPixelType.Gray16, Img.Bounds.SizeZ, NumberOfTimePoints-1,0)
    FinalImage = None
    FinalImage = Zen.Processing.Utilities.ImageGenerator(Img.Bounds.SizeX, Img.Bounds.SizeY, NumberOfStacks*Img.Bounds.SizeZ, Img.Bounds.SizeC, 1, 0,65535, ZenImageGeneratorPattern.Checker, ZenPixelType.Gray16, ZenThirdProcessingDimension.Z, False)
    FinalImage.Scaling.X = PixelSizeXY
    FinalImage.Scaling.Y = PixelSizeXY
    FinalImage.Scaling.Z = PixelSizeZ
    for ttt in range (0, TP):
        jj=0
        for ii in range ((NumberOfStacks*TP)*l+ttt*NumberOfStacks, (NumberOfStacks*TP)*l+(ttt+1)*NumberOfStacks):
            imgname = Path.Combine(imgfolder, filelist[ii])
            print(imgname)
            Img1 = Zen.Application.LoadImage(imgname, False)
            for cc in range (0, SizeC):
                for zz in range(0, SizeZ):
                    SubsetString= "Z("+ str(zz+2) + ") | C("+ str(cc+1) +") | T("+ str(ttt+1) +")"
                    #print(SubsetString)
                    SubImg = Img1.CreateSubImage(SubsetString)
                    FinalImage.AddSubImage(SubImg,ttt,cc,(jj*SizeZ)+zz)
                    SubImg.Close()
            Img.Close()
            jj=jj+1
    
    Zen.Application.Documents.Add(FinalImage)
    if l &lt; 9:
        FinalImage.Save(Path.Combine(OutputFolder, 'concatenated_stacks_position0' + str(l+1) + '.czi'))
        print('Saved as concatenated_stacks_position0' + str(l+1) + '.czi')
        print('---------------')
        Zen.Application.Documents.GetByName('concatenated_stacks_position0' + str(l+1) + '.czi').Close()
    else:
        FinalImage.Save(Path.Combine(OutputFolder, 'concatenated_stacks_position' + str(l+1) + '.czi'))
        print('Saved as concatenated_stacks_position' + str(l+1) + '.czi')
        print('---------------')
        Zen.Application.Documents.GetByName('concatenated_stacks_position' + str(l+1) + '.czi').Close()
    FinalImage.Close

print('All volume stacks processed. Workflow finished.')
