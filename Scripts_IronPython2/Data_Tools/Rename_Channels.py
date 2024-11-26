#################################################################
# File       : Rename_Channels.py
# Version    : 0.1
# Author     : czsrh
# Date       : 21.08.2019
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import sys
from System.IO import Directory, Path, File, FileInfo, DirectoryInfo

# remove all messages
Zen.Application.MacroEditor.ClearMessages()

# load an image
filename = r'C:\Users\m1srh\Documents\Testdata_Zeiss\OAD_Testing\3CH.czi'
image = Zen.Application.LoadImage(filename)

#################################################

# define dictionary with desired channel names
newnames = {0: 'CH1',
            1: 'CH2',
            2: 'CH3'}

#################################################

# get number of channels in dict
len(newnames.keys())

# get the number of channels
numch = image.Bounds.SizeC

if numch != len(newnames.keys()):
    sys.exit('Number of Channel does not match number of new channel names.')
else:
    for ch in range(numch):
        # rename all channels
        image.SetChannelName(ch, newnames[ch])

# define new filename and save image
newname = Path.Combine(Path.GetDirectoryName(filename), Path.GetFileNameWithoutExtension(filename) + '_newCH.czi')
print 'New Filename : ', newname
image.Save(newname)

# close the image
image.Close()

print 'Done Renaming.'
