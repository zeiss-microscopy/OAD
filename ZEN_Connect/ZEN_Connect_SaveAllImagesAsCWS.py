#################################################################
# File       : ZEN_Connect_SaveAllImagesAsCWS.py
# Version    : 0.1
# Author     : czsrh, czswg
# Date       : 05.07.2019
# Institution : Carl Zeiss Microscopy GmbH
#
# - Save all open image documents to a new CWS project
# - Check if image contains preview or label images and add the as well
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

version = 0.1

from System.IO import Path, File, Directory, FileInfo
from datetime import datetime
from time import gmtime, strftime
from System import ApplicationException

# clear output
Zen.Application.MacroEditor.ClearMessages()

# close a project, if one is open
ZenConnectDocument.CloseZenConnectProject(False)

imagefiles = []

initialpath = r'%Userprofile%'
CWSDialog = ZenWindow()
CWSDialog.Initialize('Save all open images to new ZEN Connect workspace - Version: ' + str(version))
CWSDialog.AddFolderBrowser('projectfolder', 'ZEN Connect Project Target Folder:', initialpath)
CWSDialog.AddCheckbox('copy', 'Move Images to new CWS Data Folder', False)
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
print('Created new project name: ', projectname)

# Create the project in the folder below 
ZenConnectDocument.CreateZenConnectProject(targetprojectfolder, projectname + '.a5proj')
cwspath = ZenConnectDocument.GetZenConnectDocumentPath()
cwsdata_path = Path.Combine(cwspath, projectname + '_data')

# get all open documents
opendocs = Zen.Application.Documents

for doc in opendocs:
  
    if doc.IsZenImage and doc.Name != 'Navigation':
        image = Zen.Application.Documents.GetByName(doc.Name)
        # add current image document to ZEN Connect workspace
        ZenConnectDocument.AddImageToZenConnectProject(image.FileName)
        
        if copydata:
            File.Copy(image.FileName, Path.Combine(cwsdata_path, image.Name))
            print('Copied File: ', image.FileName, ' to: ', cwsdata_path)
     
        print('Added image to ZEN Connect: ', image.Name)
        
        # check for labels or preview images
        try:
            att = image.Core.Attachments.GetEnumerator()
            index = 0
            
            index_to_remove = -1
            for a in att:
                
                if a.Name == 'SlidePreview':
                    preview = a.GetImageDocument()
                    print(a.Name)
                    name = Path.Combine(Path.Combine(targetprojectfolder, cwsdata_path), image.Name + '_Preview.czi')
                    preview.SaveAs(name)
                
                    if preview.Metadata.Information.Image.Session.SessionName is None:
                        print('Image: ', name, ' does not contain valid stage positions.')
                        print('It will be placed at the coordinate system origin.')
                    
                    print('Save slide image here: ', name)
                    preview.Close()
                    ZenConnectDocument.AddImageToZenConnectProject(name)
                    print('Added image to ZEN Connect: ', name)
                    
                if a.Name == 'Label':
                    preview = a.GetImageDocument()
                    print(a.Name)
                    name = Path.Combine(Path.Combine(targetprojectfolder, cwsdata_path), image.Name + '_Label.czi')
                    preview.SaveAs(name)
                    
                    if preview.Metadata.Information.Image.Session.SessionName is None:
                        print('Image: ', name, ' does not contain valid stage positions.')
                        print('It will be placed at the coordinate system origin.')

                    print('Save label image here: ', name)
                    preview.Close()
                    ZenConnectDocument.AddImageToZenConnectProject(name)
                    print('Added image to ZEN Connect: ', name)
                    
                index = index + 1
                
        except ApplicationException as e:
            print('Application Exception : ', e.Message)

# save CSW project at the end
ZenConnectDocument.SaveZenConnectProject()

# close CWS project at the end
if closecwsproject:
    ZenConnectDocument.CloseZenConnectProject(False)

print('Done. Added all open images to ZEN Connect workspace.')
