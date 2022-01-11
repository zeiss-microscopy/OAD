#################################################################
# File        : ZEN_Connect_SaveAllImagesAsCWS.py
# Version     : 0.2
# Author      : czsrh, czswg, czjuz
# Date        : 26.04.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# - Save all open image documents to a new CWS project
# - Check if image contains preview or label images and add them as well
#
# Use with ZEN Blue 3.4 or newer
# Copyright(c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

version = 0.2

from System.IO import Path, File, Directory, FileInfo, FileStream, FileMode, FileAccess, FileShare, FileOptions
from datetime import datetime
from time import gmtime, strftime
from System import ApplicationException
import os

def GetImageDocument(attachment, name):
    fst = FileStream(name, FileMode.Create, FileAccess.ReadWrite,FileShare.Read, 4096, FileOptions.SequentialScan)
    a.WriteToStream(fst)
    fst.Close()

# clear output
Zen.Application.MacroEditor.ClearMessages()

# close a project, if one is open
OldDocument = ZenConnect.GetActiveZenConnectDocument()
if not OldDocument is None:
    OldDocument.CloseZenConnectDocument(False)


imagefiles = []

initialpath = os.path.join(os.getenv('Userprofile'), "Documents")
CWSDialog = ZenWindow()
CWSDialog.Initialize('Save all open images to new ZEN Connect workspace - Version: ' + str(version))
CWSDialog.AddFolderBrowser('projectfolder', 'ZEN Connect Project Target Folder:', initialpath)
CWSDialog.AddCheckbox('copy', 'Copy Images to new CWS Data Folder', False)
CWSDialog.AddCheckbox('addatt', 'Include Preview or Label Images (if found)', False)
CWSDialog.AddCheckbox('closecws', 'Close CWS project at the end', False)
sf = CWSDialog.Show()

if sf.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

targetprojectfolder = str(sf.GetValue('projectfolder'))
print('Using project target folder: ', targetprojectfolder)
addpreview = sf.GetValue('addatt')
copydata = sf.GetValue('copy')
closecwsproject = sf.GetValue('closecws')

# create CWS project name based on date
projectname = strftime('ZEN_Connect_%Y-%m-%d_%H-%M', gmtime())
fullprojectname = Path.Combine(targetprojectfolder, projectname) + ".a5proj"
print('Created new project name: ', fullprojectname)

# Create the project in the folder below 
NewProject = ZenConnect.CreateZenConnectDocument(fullprojectname)
cwsdata_path = Path.Combine(targetprojectfolder, projectname) + '_data'

# get all open documents
opendocs = Zen.Application.Documents

for doc in opendocs:
  
    if doc.IsZenImage and doc.Name != 'Navigation':
        image = Zen.Application.Documents.GetByName(doc.Name)
                
        if copydata:
            File.Copy(image.FileName, Path.Combine(cwsdata_path, image.Name))
            print('Copied File: ', image.FileName, ' to: ', cwsdata_path)
            NewProject.AddImageToZenConnectDocument(Path.Combine(cwsdata_path, image.Name))
        else:
            NewProject.AddImageToZenConnectDocument(image.FileName)
     
        print('Added image to ZEN Connect: ', image.Name)
        
        # check for labels or preview images
        if addpreview:
            try:
                att = image.Core.Attachments.GetEnumerator()
                index = 0
                
                index_to_remove = -1
                for a in att:
                    
                    if a.Name == 'SlidePreview':
                        print(a.Name)
                        name = Path.Combine(cwsdata_path, image.NameWithoutExtension + '_Preview.czi')
                        GetImageDocument(a, name)
                        preview = Zen.Application.LoadImage(name)
                        print('Save slide image here: ', name)
                        preview.Close()
                        NewProject.AddImageToZenConnectDocument(name)
                        print('Added image to ZEN Connect: ', name)
                        
                    if a.Name == 'Label':
                        print(a.Name)
                        name = Path.Combine(cwsdata_path, image.NameWithoutExtension + '_Label.czi')
                        GetImageDocument(a, name)
                        print('Save label image here: ', name)
                        NewProject.AddImageToZenConnectDocument(name)
                        print('Added image to ZEN Connect: ', name)
                        
                    index = index + 1
                    
            except ApplicationException as e:
                print('Application Exception : ', e.Message)

# save CSW project at the end
NewProject.SaveZenConnectDocument()

# close CWS project at the end
if closecwsproject:
    NewProject.CloseZenConnectDocument(False)
