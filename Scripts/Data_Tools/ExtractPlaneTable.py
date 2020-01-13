#################################################################
# File       : ExtractPlaneTable.py
# Version    : 1.0
# Author     : czsrh
# Date       : 21.06.2016
# Institution : Carl Zeiss Microscopy GmbH
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

###########   !!!   ATENTION   !!!   ##############
#
# Date: 03.11.2019
# Currently not working due to an open issue in ZEN!
#
###########   !!!   ATENTION   !!!   ##############


def SortZenTable(table, columnname, option='asc'):

    # get the default view for the internal table object
    dv = table.Core.DefaultView

    # sort the table
    dv.Sort = columnname + ' ' + option

    # convert the table to ZenTable object
    dt = dv.ToTable('Test')

    # clear the original ZenTable
    table.Rows.Clear()

    # fill in the new values
    for dr in dt.Rows:
        table.Rows.Add(dr.ItemArray)

    return table


# clear console output
Zen.Application.MacroEditor.ClearMessages()

# get current active image
img = Zen.Application.Documents.ActiveDocument
nameParent = img.Name

# define time unit ms, s, min, h, d
tunit = '[s]'

# create initial plane table
table = ZenTable(nameParent[:-4] + '_PlaneTable')
table.Columns.Add('Scene', int)
table.Columns.Add('Tile', int)
table.Columns.Add('TheT', int)
table.Columns.Add('TheZ', int)
table.Columns.Add('TheC', int)
table.Columns.Add('XPos [micron]', float)
table.Columns.Add('YPos [micron]', float)
table.Columns.Add('ZPos [micron]', float)
table.Columns.Add('Time ' + tunit, float)

# get dimensionality
scenes = img.Bounds.SizeS
tiles = img.Bounds.SizeM
SizeT = img.Bounds.SizeT
SizeZ = img.Bounds.SizeZ
SizeC = img.Bounds.SizeC

print 'Scenes     : ', scenes
print 'Tiles      : ', tiles
print 'TimePoints : ', SizeT
print 'Z-Planes   : ', SizeZ
print 'Channels   : ', SizeC
print 'Overall Image Count: ', scenes * tiles * SizeT * SizeZ * SizeC

count = 0
# open each subimage from the current active image
for scene in range(1, scenes + 1):
    for tile in range(1, tiles + 1):
        # very simple progress bar
        print '\b.',
        for time in range(1, SizeT + 1):
            print '\b.',
            for z in range(1, SizeZ + 1):
                print '\b.',
                for ch in range(1, SizeC + 1):
                    count = count + 1
                    # retrieve the actual subimage using the correct path
                    if tiles > 1:
                        # only try to extract tiles if there are more than one
                        subimg = img.CreateSubImage('S(' + str(scene) + ')|M(' + str(tile) + ')|T(' +
                                                    str(time) + ')|Z(' + str(z) + ')|C(' + str(ch) + ')')
                    if tiles == 1:
                        subimg = img.CreateSubImage('S(' + str(scene) + ')|T(' + str(time) + ')|Z(' + str(z) + ')|C(' + str(ch) + ')')

                    # extract relevant imformation from the metadata
                    if tunit == '[ms]':
                        tr = float(subimg.Metadata.GetMetadataWithPath('ImageRelativeTime')[1].TotalMilliseconds)
                    elif tunit == '[s]':
                        tr = float(subimg.Metadata.GetMetadataWithPath('ImageRelativeTime')[1].TotalSeconds)
                    elif tunit == '[min]':
                        tr = float(subimg.Metadata.GetMetadataWithPath('ImageRelativeTime')[1].TotalMinutes)
                    elif tunit == '[h]':
                        tr = float(subimg.Metadata.GetMetadataWithPath('ImageRelativeTime')[1].TotalHours)
                    elif tunit == '[d]':
                        tr = float(subimg.Metadata.GetMetadataWithPath('ImageRelativeTime')[1].TotalDays)

                    # fill the ZEN table with the extracted values
                    table.Rows.Add()
                    # add scene index
                    table.SetValue(count - 1, 0, scene)
                    # add tile index
                    table.SetValue(count - 1, 1, tile)
                    # add time index
                    table.SetValue(count - 1, 2, time)
                    # add z index
                    table.SetValue(count - 1, 3, z)
                    # add channel index
                    table.SetValue(count - 1, 4, ch)
                    # add xyz position
                    table.SetValue(count - 1, 5, subimg.Metadata.StagePositionMicron.X)
                    table.SetValue(count - 1, 6, subimg.Metadata.StagePositionMicron.Y)
                    table.SetValue(count - 1, 7, subimg.Metadata.FocusPositionMicron)
                    # add timestamps
                    table.SetValue(count - 1, 8, tr)

                    # close the subimage
                    subimg.Close()

print '\nFinished - PlaneTable created.'

# sort the table
newtable = SortZenTable(table, 'Time ' + tunit)

# show the table
Zen.Application.Documents.Add(newtable)
