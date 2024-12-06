#################################################################
# File       : LLS7_MultiPosition.py
# Version    : 1.0
# Author     : aukelgas
# Date       : 01.09.2022
# Institution : Carl Zeiss Microscopy GmbH
#
# Use at your own Risk !!!
# Compatible with ZEN versions 3.6 and higher
# 
# Copyright(c) 2022 Carl Zeiss Microscopy GmbH, Jena, Germany. All Rights Reserved.

import time

# version number for dialog window
version = 1.0

# clear console output
Zen.Application.MacroEditor.ClearMessages()

# check the location of experiment setups and image analysis settings are stored
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)

# Initialize Dialog
Dialog = ZenWindow()
Dialog.Initialize('LLS MultiPosition - Version : ' + str(version))
# add components to dialog
Dialog.AddTextBox('Positions', '1) Number of Positions', 2)     # Number of positions to be recorded, default 2
Dialog.AddLabel('2) Specify folder to save the images -----------------------')
Dialog.AddFolderBrowser('outfolder', 'Folder for MultiPosition Images', imgfolder)

# show the window
result = Dialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
OutputFolder = str(result.GetValue('outfolder'))
P = result.GetValue('Positions')

## get positions from user
#Zen.Application.Pause("Go to first position!")
#px = [0 for a in range(P)]
#py = [0 for a in range(P)]
#pz = [0 for a in range(P)]
#
#px[0] = Zen.Devices.Stage.ActualPositionX
#py[0] = Zen.Devices.Stage.ActualPositionY
#pz[0] = Zen.Devices.Focus.ActualPosition
##print(pz[0])
#
#for k in range (1, P):
#    Zen.Application.Pause("Go to next position!")
#    px[k] = Zen.Devices.Stage.ActualPositionX
#    py[k] = Zen.Devices.Stage.ActualPositionY
#    pz[k] = Zen.Devices.Focus.ActualPosition

# get positions from user
Zen.Application.Pause("Go to first position!")
act = Zen.Acquisition.Experiments.ActiveExperiment
act.AddSinglePosition(0,Zen.Devices.Stage.ActualPositionX, Zen.Devices.Stage.ActualPositionY, Zen.Devices.Focus.ActualPosition)

for k in range (1, P):
    Zen.Application.Pause("Go to next position!")
    act = Zen.Acquisition.Experiments.ActiveExperiment
    act.AddSinglePosition(0,Zen.Devices.Stage.ActualPositionX, Zen.Devices.Stage.ActualPositionY, Zen.Devices.Focus.ActualPosition)
