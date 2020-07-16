#################################################################
# File       : SaveSingleTiles_to_Folder.py
# Version    : 1.1
# Author     : czsrh
# Date       : 16.07.2020
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

version = 1.1


def addzeros(number):
    """Convert a number into a string and add leading zeros.
    Typically used to construct filenames with equal lengths.

    :param number: the number
    :type number: int
    :return: zerostring - string with leading zeros
    :rtype: str
    """

    if number < 10:
        zerostring = '0000' + str(number)
    if number >= 10 and number < 100:
        zerostring = '000' + str(number)
    if number >= 100 and number < 1000:
        zerostring = '00' + str(number)
    if number >= 1000 and number < 10000:
        zerostring = '0' + str(number)

    return zerostring


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
img = Zen.Application.Documents.GetByName(Path.GetFileNameWithoutExtension(cziname))
nameParent = img.Name

# get number of tiles and scenes
try:
    nScenes = img.Bounds.SizeS
except:
    nScenes = 1

try:
    nTiles = img.Bounds.SizeM
except:
    nTiles = 1

print('Number of Scenes detected: ', nScenes)
print('Number of Tiles detected: ', nTiles)

# address each tile image in Zen without opening it
for s in range(1, nScenes + 1):
    for m in range(1, nTiles + 1):

        # get the strings with leading zeros
        s_str = addzeros(s)
        m_str = addzeros(m)

        # create the subimage
        imgTile = img.CreateSubImage('S(' + s_str + ')|M(' + m_str + ')')

        # create a useful name
        imgTile.Name = nameParent[:-4] + '_S' + s_str + '_T' + m_str + ft[1:]
        print(imgTile.Name)

        # save current tile with the specified format
        Zen.Application.Save(imgTile, Path.Combine(SavePath, imgTile.Name), False)
        imgTile.Close()

print('All Tiles saved.')
