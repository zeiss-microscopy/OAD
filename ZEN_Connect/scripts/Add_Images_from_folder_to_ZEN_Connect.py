#################################################################
# File        : ZEN_Connect_Add_Images_from_folder.py
# Version     : 0.1
# Author      : czjuz
# Date        : 04.01.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# - Add all images found in a folder to a ZEN Connect project
# - Do this recursively as option
#
# Use with ZEN Blue 3.4 or newer
# Copyright(c) 2022 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

version = 0.1

from System.IO import Path
from datetime import datetime
from time import gmtime, strftime
from System import ApplicationException
import os
FILEWARNING = 50

# count the number of czi files
def CountCZIFiles(basedirectory):
    czicounter = 0
    dirnum = 0
    filenum = 0
    for root, dirs, files in os.walk(basedirectory):
        for elements in files:
            if elements.endswith(".czi"):
                czicounter+=1
        dirnum += len(dirs)
        filenum += len(files)
    
    return dirnum, filenum, czicounter
    
# clear output
Zen.Application.MacroEditor.ClearMessages()

# close a project, if one is open
OldDocument = ZenConnect.GetActiveZenConnectDocument()
if not OldDocument is None:
    OldDocument.CloseZenConnectDocument(False)



# generate dialog
initialpath = os.path.join(os.getenv('Userprofile'), "Documents")
CWSDialog = ZenWindow()
CWSDialog.Initialize('Add all images from the selected folder to a new ZEN Connect workspace - Version: ' + str(version))
CWSDialog.AddFolderBrowser('projectfolder', 'ZEN Connect Project Target Folder:','',"0","0")
CWSDialog.AddFolderBrowser('imagefolder', 'Folder with images:', initialpath, "0", "1")
CWSDialog.AddCheckbox('recursive', 'Include images of all subdirectories', False, "1", "0")
CWSDialog.AddCheckbox('closecws', 'Close CWS project at the end', False, "2", "0")
sf = CWSDialog.Show()

if sf.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# Get resulsts from window
targetprojectfolder = str(sf.GetValue('projectfolder'))
print('Using project target folder: ', targetprojectfolder)
imagefolder = str(sf.GetValue('imagefolder'))
print ('Using images from folder: ', imagefolder)
recursive = sf.GetValue('recursive')
closecwsproject = sf.GetValue('closecws')

# Generates a warning if a high number of CZI images is found
if recursive:
    fileresults = (CountCZIFiles(imagefolder))
    if fileresults[2] > FILEWARNING:
        warndialog = ZenWindow()
        warndialog.HasCancelButton = True
        warndialog.HasOkButton = True
        warndialog.AddLabel("Found more than " + str(fileresults[2]) + " files in " + str(fileresults[0]) + " folders" + "\r\n" + "in folder " +  imagefolder  + "\r\n" + "Would you like to continue ")
        a = warndialog.Show()
        if a.HasCanceled:
            message = 'Macro was canceled by user.'
            print(message)
            raise SystemExit

# create CWS project name based on date
projectname = strftime('ZEN_Connect_%Y-%m-%d_%H-%M', gmtime())
fullprojectname = Path.Combine(targetprojectfolder, projectname) + ".a5proj"
print('Created new project name: ', fullprojectname)

# Create the project in the folder below 
NewProject = ZenConnect.CreateZenConnectDocument(fullprojectname)
cwsdata_path = Path.Combine(targetprojectfolder, projectname) + '_data'

results = []
if recursive:
    results = NewProject.AddImagesInFolderToZenConnectDocument(imagefolder, True)  
else:
    results = NewProject.AddImagesInFolderToZenConnectDocument(imagefolder, False)  

# print files that could not be added
for i in results:
    print ("could not be added: ", i)

# save CSW project at the end
NewProject.SaveZenConnectDocument()

# close CWS project at the end
if closecwsproject:
    NewProject.CloseZenConnectDocument(False)
