#################################################################
# File       : Metadata_Report_Tool.py
# Version    : 1.4
# Author     : czsrh
# Date       : 22.08.2019
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

"""

The scripts creates a table with useful metainformation.
- it creates a ZenTable
- allows saving as CSV file
- allows saving a TXT file
- allows saving as Excel sheet

"""

version = 1.4

from System import ApplicationException
import clr

try:
    clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
    from Microsoft.Office.Interop import Excel
    excelimport = True
except:
    print('Could not import Excel functionality.')
    excelimport = False

import os
from System.IO import Directory, Path, File, FileInfo, DirectoryInfo
try:
    from collections import Counter
    usecounter = False
except:
    print('Warning: Could not import module Collection.Counter.')
    usecounter = True

#########################################################################

# options
verbose = True
createexcelformdict = False

# clear output console
Zen.Application.MacroEditor.ClearMessages()

#########################################################################


# get wellname from image metadata
def GetWellNames(image, usecounter):
    wells = []
    positions = []
    numscenes = image.Bounds.SizeS

    for i in range(0, numscenes, 1):
        IDString_pos = r'Metadata/Information/Image/Dimensions/S/Scenes[' + str(i) + ']/Index'
        IDString_well = r'Metadata/Information/Image/Dimensions/S/Scenes[' + str(i) + ']/Shape/Name'
        pos = image.Metadata.GetMetadataWithPath(IDString_pos)
        # convert position index to string
        positions.append('P' + str(pos))
        well = image.Metadata.GetMetadataWithPath(IDString_well)
        wells.append(well)
        
    # determine the actual number of wells
    if usecounter:
        if len(wells) >= 1:
            numwells = len(Counter(wells).most_common())
        else:
            numwells = 1
    if not usecounter:
        numwells = count_different_wells(wells)
    
    return positions, wells, numwells


def count_different_wells(wells):
    # initialize counter
    numwells = 0
    last_well = 'none'

    for well in wells:
        # check for new wellID
        if well != last_well:
            # increase number of detected wells and update last_well
            numwells = numwells + 1
            last_well = well
            
    return numwells


def list2string(list, separator=','):

    output = ''
    for elem in list:
        output = output + str(elem) + separator
    
    # remove last separator
    output = output[:-1]
        
    return output


def getscale(image):
    
    # get scaling for XYZ in micron
    sx = image.Metadata.ScalingMicron.X
    sy = image.Metadata.ScalingMicron.Y
    sz = image.Metadata.ScalingMicron.Z

    return sx, sy, sz


def getLSMData(image):

    # get values for transmission and attenuation
    try:
        laserpower = image.Metadata.GetMetadataWithPath('Metadata/Information/Image/Dimensions/Channels[]/ChannelLaserScanInfo/LaserAttenuatorMeas')
    except ApplicationException as e:
        laserpower = 'na'
        print('Problem reading Laser Power: ', e.Message)
    
    try:
        attstate = image.Metadata.GetMetadataWithPath('Metadata/Information/Image/Dimensions/Channels[current]/ChannelLaserScanInfo/AttenuatorState')
    except ApplicationException as e:
        attstate = 'na'
        print('Problem Reading Attenuator State : ', e.Message)
        
    try:
        attbleach = image.Metadata.GetMetadataWithPath('Metadata/Information/Image/Dimensions/Channels[current]/ChannelLaserScanInfo/LaserAttenuatorBleach')
    except ApplicationException as e:
        attbleach = 'na'
        print('Problem Reading Laser Attenuator Bleach: ', e.Message)
        
    try:
        lli = image.Metadata.GetMetadataWithPath('Metadata/Information/Image/Dimensions/Channels[current]/LightSourceIntensity')
    except ApplicationException as e:
        lli = 'na'
        print('Problem reading Light Source Intensity : ', e.Message)

    return laserpower, attstate, attbleach, lli


def getNA(image):

    # use the correct path to get the numerical aperture of the used objective
    na = image.Metadata.GetMetadataWithPath('Metadata/Information/Instrument/Objectives[]/LensNA')
    
    return na


def SortZenTable(table, columnname, option='asc'):

    # get the default view for the internal table object
    dv = table.Core.DefaultView
    # sort the table
    dv.Sort  = columnname + ' ' + option
    # convert the table to ZenTable object
    dt = dv.ToTable('Test')
    # clear the original ZenTable
    table.Rows.Clear()
    # fill in the new values
    for dr in dt.Rows:
        table.Rows.Add(dr.ItemArray)
    
    return table


def getMetaDataExtra(image, usecounter, list2str=True, fullwellinfo=False):
    # get additional metadada
    Metadata = {}
    
    # get the number of scenes, tiles, dimensions and etc.
    Metadata['NumberScenes'] = image.Bounds.SizeS
    Metadata['NumberTiles'] = image.Metadata.TilesCount
    Metadata['SizeT'] = image.Bounds.SizeT
    Metadata['SizeZ'] = image.Bounds.SizeZ
    Metadata['SizeC'] = image.Bounds.SizeC
    Metadata['SizeX'] = int(image.Bounds.SizeX)
    Metadata['SizeY'] = int(image.Bounds.SizeY)
    Metadata['Dimensionality'] = image.Bounds.Dimensionality
    Metadata['NumberBlocks'] = image.Bounds.SizeB
    Metadata['ScalingUnit'] = image.Metadata.ScalingUnitInfo
    Metadata['ScalingMicron'] = image.Metadata.ScalingMicron
    
    # get objective NA
    Metadata['ObjectiveNA'] = float(getNA(image))
    
    # add scale
    Metadata['ScaleX'], Metadata['ScaleY'], Metadata['ScaleZ'] = getscale(image)
    
    # get well and position information
    positionlist, welllist, wellnumber = GetWellNames(image, usecounter)
    if fullwellinfo:
        Metadata['PositionList'] = positionlist
        Metadata['WellList'] = welllist
        Metadata['WellNumber'] = wellnumber
        # covnvert pytjhon list to string
        if list2str:
            Metadata['PositionList'] = list2string(Metadata['PositionList'])
            Metadata['WellList'] = list2string(Metadata['WellList'])
    
    if not fullwellinfo:
        Metadata['PositionList'] = positionlist[0] + ' - ' + positionlist[-1]
        Metadata['WellList'] = welllist[0] + ' - ' + welllist[-1]
        Metadata['WellNumber'] = wellnumber

    # read barcode
    Metadata['Barcode'], Metadata['BarcodeInfo'], barcode_found = ReadBarCodefromImage(image)

    # get laser data
    Metadata['LaserAttenuator'], Metadata['AttenuatorState'], Metadata['AttenuatorBleach'], Metadata['LightSourceIntensity'] = getLSMData(image)

    return Metadata


def ReadBarCodefromImage(image):

    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]
    
    # use the correct path to read the barcode from the image
    barcode_complete = image.Metadata.GetMetadataWithPath('Metadata/AttachmentInfos[]/Label/Barcodes[]/Content')
    if len(barcode_complete) == 0:
        print('No barcode was found.')
        barcode = 'n.a.'
        barcodeinfo = 'n.a.'
        barcode_found = False
    
    if len(barcode_complete) > 0:
        indexlist = find(barcode_complete, ':')
        barcode = barcode_complete[max(indexlist)+1:]
        barcodeinfo = barcode_complete[:max(indexlist)]
        barcode_found = True
        # remove leading whitespace from barcode
        barcode = barcode[1:]

    return barcode, barcodeinfo, barcode_found


##################################### MAIN SCRIPT #######################################

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

# Activate GUI
wd = ZenWindow()
wd.Initialize('MetaData Report Tool - Version : ' + str(version))
wd.AddLabel('---   Read MetaData to ZenTable and Save   ---')
wd.AddDropDown('czi', 'Select CZI Image Document', CZIfiles_short, 0)
wd.AddCheckbox('saveascsv', 'Save Metadata as CSV file', False)
wd.AddCheckbox('saveastxt', 'Save Metadata as TXT file', True)
if excelimport:
    wd.AddCheckbox('showexcel', 'Save Metadata in Excel', False)
wd.AddCheckbox('fullwellinfo', 'Include full wellinfo in metadata', False)
wd.AddLabel('-----------------------------------------------')
wd.AddCheckbox('closezentable', 'Close ZEN table at the end', False)
if excelimport:
    wd.AddCheckbox('closeexcel', 'Close Excel at the end', False)

# show the window
result=wd.Show()

# check, if Cancel button was clicked
if result.HasCanceled == True:
    sys.exit('Macro aborted with Cancel!')

# get the input values and store them
cziname = result.GetValue('czi')
czidocument = CZIdict[cziname]
savecsv = result.GetValue('saveascsv')
savetxt = result.GetValue('saveastxt')
showxls = result.GetValue('showexcel')
closetablezen = result.GetValue('closezentable')
if excelimport:
    closetableexcel = result.GetValue('closeexcel')
fwinfo = result.GetValue('fullwellinfo')

# get the active image document
activeimage = Zen.Application.Documents.GetByName(cziname)
Zen.Application.Documents.ActiveDocument = activeimage

# get the full metadata using the normal built-in method
info = activeimage.Metadata.GetAllMetadata()

# show optional output
if verbose:
    print('-----------------   GetAllMetadata()  -------------------------------')
    for i in info: 
        print(i.Key, '\t ', i.Value)

# get additional metainformation
metadata = getMetaDataExtra(activeimage, usecounter, fullwellinfo=fwinfo)

if verbose:
    for k, v in metadata.items():
        print(k, '\t', v)

# concatenate the two python dictionaries
metadata.update(info)

# Create new table with 2 col with name Key and Value
table1 = ZenTable('MetaData - ' + Path.GetFileNameWithoutExtension(cziname))
table1.Columns.Add('Name',str)
table1.Columns.Add('Value',str)

# fill the table from the dictionary
r = 0
for k, v in metadata.items():
    table1.Rows.Add()
    table1.SetValue(r, 0, k)
    table1.SetValue(r, 1, v)
    r = r + 1

# sort the table
table1_sorted = SortZenTable(table1, 'Name')
Zen.Application.Documents.Add(table1_sorted)

if savecsv:
    # Save data table
    csvfilename = activeimage.FileName[:-4] + '_MetaData.csv'
    print('CSV file to save: ', csvfilename)
    table1_sorted.Save(csvfilename)


if savetxt:
    # write text file
    txtfilename = activeimage.FileName[:-4] + '_MetaData.txt'
    print('TXT file to save: ', txtfilename)
    wFile = open(txtfilename,'w')
    
    for row in range(table1_sorted.RowCount):
        # Write text file
        wFile.write(table1_sorted.GetValue(row, 0) + ':')
        wFile.write ('\t')
        wFile.write(table1_sorted.GetValue(row, 1))
        wFile.write ('\n')
    
    wFile.close()

if showxls:
    # activate excel
    excel = Excel.ApplicationClass()
    excel.Visible = True
    excel.DisplayAlerts = False
    workbook = excel.Workbooks.Add()
    ws = workbook.Worksheets[1]
    
    # create headers inside the 1st row for the worksheet
    excel.Cells(1,1).Value = 'Name'
    excel.Cells(1,2).Value = 'Value'
    
    # create excel sheet from dictionary, but the it is not sorted
    if createexcelformdict:
        # set counter
        r = 1
        # iterate over all the entries from the metadata dictionary and add to worksheet
        for k, v in metadata.items():
            r = r + 1
            excel.Cells(r, 1).value = k
            excel.Cells(r, 2).value = v
    
    if not createexcelformdict:
        # create excel sheet directly from sorted table 
        numrows = table1_sorted.RowCount
        for r in range(0, numrows):
            # in Excel the counting starts with one, while in ZEN with zero ... :-)
            excel.Cells(r+1, 1).value = table1_sorted.GetValue(r, 0)
            excel.Cells(r+1, 2).value = table1_sorted.GetValue(r, 1)
        
    excel.Rows('1:1').Select()
    excel.Selection.Font.Bold = True
    excel.Cells.Select()
    excel.Cells.EntireColumn.AutoFit()
    excel.Columns(2).HorizontalAlignment = 2
    excel.Columns(2).VerticalAlignment = 2
    
    # save the worksheet with the metadata
    excelfilename = activeimage.FileName[:-4] + '_MetaData.xlsx'
    print('Excel file to save: ', excelfilename)
    workbook.SaveAs(excelfilename)

    # close the workbook and excel
    if closetableexcel:
        print('Closing Excel.')
        workbook.Close()
        excel.Application.Quit()

# close ZEN table
if closetablezen:
    print('Close the table in ZEN.')
    table1_sorted.Close()
