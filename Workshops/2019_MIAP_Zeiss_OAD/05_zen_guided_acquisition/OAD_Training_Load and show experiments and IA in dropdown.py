#######################################################
## G E N E R A L - L O A D  F I L E S
##
## Macro name: OAD_Training_Load and show experiments and IA in dropdown.py
##
## Required files: Folder with Experiments and Image Analysis Settings
## Required demo files: None
##
## Required module/licence: 
##
## DESCRIPTION: Load all experiments and image analysis settings from user folder
## and show them in a drop-down menu.
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################

from System.IO import Directory, Path

def getshortfiles(filelist):
    files_short = []
    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)


# get list with all existing experiments and image analysis setup and a short version of that list
expfiles = Directory.GetFiles(Path.Combine(docfolder, 'Experiment Setups'), '*.czexp')
ipfiles = Directory.GetFiles(Path.Combine(docfolder, 'Image Analysis Settings'), '*.czias')
expfiles_short = getshortfiles(expfiles)
ipfiles_short = getshortfiles(ipfiles)

# Initialize Dialog
window = ZenWindow()

# add components to dialog
window.AddLabel('1) Select Overview Experiment  ------------------------------')
window.AddDropDown('overview_exp', 'Overview Scan Experiment', expfiles_short, 0)
window.AddLabel('2) Select Image Analysis to detect objects  ----------------------')
window.AddDropDown('ip_pipe', 'Image Analysis Pieline', ipfiles_short, 0)

# show the window
result = window.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
experimentname = str(result.GetValue('overview_exp'))
ias_name = str(result.GetValue('ip_pipe'))

print(experimentname + "\t" + ias_name)
