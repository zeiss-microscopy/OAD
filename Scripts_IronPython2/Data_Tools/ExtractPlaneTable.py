#####################################################################
# File       : Extract_PlaneTable.py
# Version    : 1.3
# Author     : czsrh
# Date       : 07.03.2022
# Insitution : Carl Zeiss Microscopy GmbH
#
# This script required ZEN blue version 3.5. Please contact us if older
# versions are required
#
# Will only give meaningful results for CZIs acquifred with ZEN blue!
#
# Copyright (c) 2022 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Disclaimer:The script contains undocuments function and methods,
#            which are subject to change. Use at your own risk.
#####################################################################

from System import Convert
from System.IO import Directory, Path, File, FileInfo, DirectoryInfo
import csv
import clr
# this DLL has to be present in the ZEN 3.5 program folder
clr.AddReference('ZenToolsBlue35.dll')
import ZenTools

version = 1.3


def normalize_columns(table, colname):

    # create emty list
    timestamps = []

    for r in range(table.RowCount):
        # create list with all timestamps
        timestamps.append(table.GetValue(r, table.Columns.IndexOf(colname)))
    
    # determine the minimum time value
    tmin = min(timestamps)
    
    for r in range(table.RowCount):
        # replace the timestamps with the normalized value
        table.SetValue(r, table.Columns.IndexOf(colname), timestamps[r] - tmin)
        
    return table


def write_planetable(table, filename, delimiter=','):

    # define the headers carefully - they must match with the table column names
    headers = ['Scene','Tile', 'T', 'Z', 'C', 'X[micron]', 'Y[micron]', 'Z[micron]', 'Time[s]']

    # open the file for writing
    writer = csv.writer(open(filename, 'wb'), delimiter=delimiter)
    
    # write the headers inside the first row
    writer.writerow(headers)
    
    # write values row-by-row
    for r in range(table.RowCount):
        
        row = []
        for h in headers:
            # special formating
            if h in ['X[micron]','Y[micron]', 'Z[micron]']:
                row.append('{0:0.1f}'.format(table.GetValue(r, table.Columns.IndexOf(h))))
            if h in ['Time[s]']:
                row.append('{0:0.3f}'.format(table.GetValue(r, table.Columns.IndexOf(h))))
            if h in ['Scene', 'Tile', 'T', 'Z', 'C']:
                row.append(table.GetValue(r, table.Columns.IndexOf(h)))
        
        # write the formated row
        writer.writerow(row)
        
    print('CSV file written.')

##################################### MAIN SCRIPT #######################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

CZIfiles_short = []
CZIdict = {}

# get all open documents
opendocs = Zen.Application.Documents
for doc in opendocs:
    image = Zen.Application.Documents.GetByName(doc.Name)
    
    if image.FileName.EndsWith('.czi'):
        # get the filename of the current document only when it ends with '.czi'
        CZIfiles_short.append(Path.GetFileName(image.FileName))
        CZIdict[Path.GetFileName(image.FileName)] = image.FileName


# create dialog
wd = ZenWindow()
wd.Initialize('Extract PlaneTable Tool - Version : ' + str(version))
wd.AddDropDown('czi', 'Select CZI Image Document', CZIfiles_short, 0)
wd.AddCheckbox('savedata', 'Save Metadata as CSV file', True)
wd.AddLabel('-----------------------------------------------')
wd.AddCheckbox('closezentable', 'Close ZEN table at the end', False)

# show the window
result=wd.Show()

# check, if Cancel button was clicked
if result.HasCanceled:
    sys.exit('Macro aborted with Cancel!')

# get the input values and store them
cziname = result.GetValue('czi')
czidocument = CZIdict[cziname]
savetable = result.GetValue('savedata')
closetablezen = result.GetValue('closezentable')

# get the active image document
img = Zen.Application.Documents.GetByName(cziname)
Zen.Application.Documents.ActiveDocument = img

# define time unit
tunit = '[s]'

# create initial plane table 
table = ZenTable(cziname[:-4] + '_PlaneTable')
table.Columns.Add('Scene', int)
table.Columns.Add('Tile', int)
table.Columns.Add('T', int)
table.Columns.Add('Z', int)
table.Columns.Add('C', int)
table.Columns.Add('X[micron]', float)
table.Columns.Add('Y[micron]', float)
table.Columns.Add('Z[micron]', float)
table.Columns.Add('Time' + tunit, float)

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
print 'Overall Image Count  : ', scenes * tiles * SizeT * SizeZ * SizeC
print 'Total SubBlock Count : ', ZenTools.ImageTools.GetNumberOfSubblocks(image=img)

count = -1

pbar = 1
# get collection of image subblocks
sbs = ZenTools.ImageTools.GetImageSubblocks(image=img)

if sbs.Count <= 100:
    pbar = 10
if sbs.Count <= 1000:
    pbar = 20
if sbs.Count <= 10000:
    pbar = 50
    

print(' Start checking Image Subblocks ...')

# loop over all image subblocks inside the CZI
for sb in sbs:

    # check if the subblock is a pyramid block
    if not sb.IsScaled:
        
        count = count + 1
        if divmod(count, pbar)[1] == 0:
            print '\b.',
        
        # allow data accsess
        sb.BeginImageDataAccess()
        
        # fill the ZEN table with the extracted values
        table.Rows.Add()
        
        # add scene index
        table.SetValue(count, table.Columns.IndexOf('Scene'), sb.Bounds.StartS)
        
        # add tile index
        table.SetValue(count, table.Columns.IndexOf('Tile'), sb.Bounds.StartM)
        
        # add time index
        table.SetValue(count, table.Columns.IndexOf('T'), sb.Bounds.StartT)
        
        # add z index
        table.SetValue(count, table.Columns.IndexOf('Z'), sb.Bounds.StartZ)
        
        # add channel index
        table.SetValue(count, table.Columns.IndexOf('C'), sb.Bounds.StartC)
        
        # add xyz position
        table.SetValue(count, table.Columns.IndexOf('X[micron]'), round(sb.Metadata.StageXPosition, 1))
        table.SetValue(count, table.Columns.IndexOf('Y[micron]'), round(sb.Metadata.StageYPosition, 1))
        table.SetValue(count, table.Columns.IndexOf('Z[micron]'), round(sb.Metadata.FocusPosition, 1))
        
        try:
            # add timestamps
            ft = sb.Metadata.AcquisitionTime.ToFileTime()
            # convert to [sec] because ft is in 100ns intervals
            ft_sec = Convert.ToDouble(ft)/10000000.0
            table.SetValue(count, table.Columns.IndexOf('Time' + tunit), ft_sec)
        except:
            table.SetValue(count, table.Columns.IndexOf('Time' + tunit), 0.0)

# extra blank line for outout for better readability
print('\n')

# normalize the timestamps
table = normalize_columns(table, 'Time' + tunit)

# sort the table
table = ZenTools.TableTools.SortColumn(table=table,
                                       columnname='Time' + tunit,
                                       option='asc')

# show the soted table
Zen.Application.Documents.Add(table)

if savetable:

    # save the data to file
    tablefilename = img.FileName[:-4] + '_PlaneTable.csv'
    print 'Data will be saved to: ', tablefilename
    
    # check for exiting file
    if File.Exists(tablefilename):
        msg = ZenWindow()
        msg.Initialize('!!! Attention !!!')
        msg.AddLabel('File already exits. Allow to Overwrite?')
        result = msg.Show()

    # check, if Cancel button was clicked
    if result.HasCanceled:
      print('Canceled. Data will not be saved.')
    if not result.HasCanceled:
        print('File will be overwritten.')
        write_planetable(table, tablefilename, delimiter=',')
        
    if not File.Exists(tablefilename):
        write_planetable(table, tablefilename, delimiter=',')
    
# close ZEN table
if closetablezen:
    newtable.Close()
    
print('Done.')
