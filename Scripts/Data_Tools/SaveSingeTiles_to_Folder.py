#################################################################
# File       : SaveSingleTiles_to_Folder.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

"""  
Save the selected image as single tiles into the specified folder
using the selected format.

"""

from System.IO import Path, File, Directory, FileInfo

version = 1.0

CZIfiles_short = []

# get all open documents
opendocs = Zen.Application.Documents

for doc in opendocs:

    image = Zen.Application.Documents.GetByName(doc.Name)
    if image.FileName.EndsWith('.czi'):
        # get the filename of the current document only when it ends with '.czi'
        CZIfiles_short.append(Path.GetFileName(image.FileName))

formats = ['*.czi', '*.jpg', '*.tiff', '*.ome.tiff']
imgfolder = Path.Combine(Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.Images), 'OAD-Test')

# Initialize the dialog window for the required user inputs
wd = ZenWindow()
wd.Initialize('Save Tiles as Single Images - Version: ' + str(version))
wd.AddDropDown('czi', 'Select CZI Image Data', CZIfiles_short, 0, '0', '0')
wd.AddFolderBrowser('savefolder', 'Specify Save Folder', imgfolder, '1', '0')
wd.AddDropDown('saveformat', 'Select Image Format', formats, 0, '2', '0')

# show the window
result = wd.Show()

# check, if Cancel button was clicked
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get results from dialog
ft = result.GetValue('saveformat')
cziname = result.GetValue('czi')
SavePath = result.GetValue('savefolder')
print('Saving CZI : ', cziname, ' as ', ft)

# get the selected image
img = Zen.Application.Documents.GetByName(cziname)
nameParent = img.Name

# get number of tiles
nTiles = img.Bounds.SizeM
print('Number of Tiles detected: ', nTiles)

# address each tile image in Zen without opening it
for m in range(1, nTiles + 1):
    imgTile = img.CreateSubImage('M(' + str(m) + ')')
    imgTile.Name = nameParent[:-4] + '-T' + str(m) + ft[1:]
    print(imgTile.Name)
    # save current tile with the specified format
    Zen.Application.Save(imgTile, Path.Combine(SavePath, imgTile.Name), False)
    imgTile.Close()

print('All Tiles saved.')
