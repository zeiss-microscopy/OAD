#################################################################
# File       : SaveSingleTiles_to_Folder.py
# Version    : 1.4
# Author     : czsrh
# Date       : 14.02.2023
# Insitution : Carl Zeiss Microscopy GmbH
#
# Save the selected image as single tiles into the specified folder
# using the selected format.
# When using OME-TIFF export make sure one used a valid setting
#
# Copyright(c) 2023 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from System.IO import Path, File, Directory, FileInfo

version = 1.4

# clear output
Zen.Application.MacroEditor.ClearMessages()

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
wd.AddDropDown('czi', 'Select CZI Image Data', CZIfiles_short, 0)
wd.AddCheckbox('split_channels', 'Split Channels', False)
wd.AddFolderBrowser('savefolder', 'Specify Save Folder', imgfolder)
wd.AddDropDown('saveformat', 'Select Image Format', formats, 0)

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
split_ch = result.GetValue('split_channels')
print(('Saving CZI : ', cziname, ' as ', ft))
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
    
try:
    nChannels = img.Bounds.SizeC
except:
    nChannels = 1

print(('Number of Scenes detected: ', nScenes))
print(('Number of Tiles detected: ', nTiles))

# initilaize OME-TIFF setting
settingsfile = 'OME-TIFF_Default.czips'
ometiff_setting = Zen.Processing.Utilities.Settings.OmeTiffExportSetting()
# the seeting must be located in:
# c:\Users\XXX\Documents\Carl Zeiss\ZEN\Documents\Processing Settings\OmeTiffExport\
ometiff_setting.Load(settingsfile, ZenSettingDirectory.User)


if split_ch:

    # address each tile image in Zen without opening it
    for s in range(0, nScenes):
        for m in range(0, nTiles):
            for c in range(0, nChannels):
    
                # get the strings with leading zeros for splitting
                s_str = addzeros(s + 1)
                m_str = addzeros(m + 1)
                c_str = addzeros(c + 1)
        
                # create the subimage
                imgTile = img.CreateSubImage('S(' + s_str + ')|M(' + m_str + ')|C(' + c_str + ')')
        
                # create a useful name
                s_str = addzeros(s)
                m_str = addzeros(m)
                c_str = addzeros(c)
                
                if ft == "*.ome.tiff":
                    imgTile.Name = nameParent[:-4] + '_S' + s_str + '_T' + m_str + '_C' + c_str
                    print((imgTile.Name))
                    # save current tile with the specified format
                    Zen.Processing.Utilities.ExportOmeTiff(imgTile, ometiff_setting, imgTile.Name, SavePath)
                
                else:
                    imgTile.Name = nameParent[:-4] + '_S' + s_str + '_T' + m_str +'_C' + c_str + ft[1:]
                    print((imgTile.Name))
                    # save current tile with the specified format
                    Zen.Application.Save(imgTile, Path.Combine(SavePath, imgTile.Name), False)
                
                imgTile.Close()
                
if not split_ch:

    # address each tile image in Zen without opening it
    for s in range(0, nScenes):
        for m in range(0, nTiles):
    
                # get the strings with leading zeros for splitting
                s_str = addzeros(s + 1)
                m_str = addzeros(m + 1)
        
                # create the subimage
                imgTile = img.CreateSubImage('S(' + s_str + ')|M(' + m_str + ')')
        
                # create a useful name
                s_str = addzeros(s)
                m_str = addzeros(m)
                
                if ft == "*.ome.tiff":
                    imgTile.Name = nameParent[:-4] + '_S' + s_str + '_T' + m_str
                    print((imgTile.Name))
                    # save current tile with the specified format
                    Zen.Processing.Utilities.ExportOmeTiff(imgTile, ometiff_setting, imgTile.Name, SavePath)
                
                else:
                    imgTile.Name = nameParent[:-4] + '_S' + s_str + '_T' + m_str + ft[1:]
                    print((imgTile.Name))
                    # save current tile with the specified format
                    Zen.Application.Save(imgTile, Path.Combine(SavePath, imgTile.Name), False)
                
                imgTile.Close()

print('All Tiles saved.')
