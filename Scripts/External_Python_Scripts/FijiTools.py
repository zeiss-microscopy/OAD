"""  
Author: Sebastian Rhode
File: FijiTools.py
Version: 1.1
"""

import csv
from System import Array


def Conv2Array(filename, rowoffset, delim):

    legnames = []
    data = []
    for row in csv.reader(open(filename), delimiter=delim):
        data.append(row)

    headers = data[0]  # contains the column names

    # determine the number of measured parameters and rows
    numvar = len(headers)
    numrows = len(data)
    entries = numrows - 1
    print('Number of Vars    :', numvar)
    print('Number of Entries :', entries)

    # initialize 2D array to store all parameter values
    values = Array.CreateInstance(float, numrows - rowoffset, numvar)
    # define empty list with ... entries
    typelist = [None] * numvar

    # write values from table into array
    for i in range(0, numrows - rowoffset, 1):

        # write the data into array
        tmp = data[i + rowoffset]
        for k in range(0, len(tmp), 1):
            # convert "," to "."
            tmp[k] = str.replace(tmp[k], ',', '.')
            try:
                values[i, k] = float(tmp[k])
                if (i == 0):
                    typelist[k] = 'float'  # type of data for current column = float
            except:
                values[i, k] = float('nan')
                if (i == 0):
                    typelist[k] = 'str'  # type of data for current column = str

    print(typelist)

    # create legend names
    for i in range(0, numvar, 1):
        legname_tmp = headers[i]
        legnames.append(legname_tmp)

    return values, legnames, numvar, entries, typelist


def Conv2List(filename, rowoffset, delim, column):

    legnames = []

    data = []
    for row in csv.reader(open(filename), delimiter=delim):
        data.append(row)

    headers = data[0]  # contains the column names
    # determine the number of measured parameters and row number
    numvar = len(headers)
    numrows = len(data)

    # initialize 2D array to store all parameter values
    labels = ([])

    # write values from table into array
    for i in range(0, numrows - rowoffset, 1):

        tmp = data[i + rowoffset]
        labels.append(tmp[column])
    # create legend names
    for i in range(0, numvar, 1):
        legname_tmp = headers[i]
        legnames.append(legname_tmp)

    return labels


def CreateTable(data, col, rows, legends, startcol, tablename, typelist, table):

    # Create new table
    #table = ZenTable(tablename)

    for i in range(startcol, col, 1):

        print('Column Type : ', typelist[i])
        if (typelist[i] == 'float'):
            table.Columns.Add(legends[i], float)
        if (typelist[i] == 'str'):
            table.Columns.Add(legends[i], str)

    # Write meta data values in table
    for r in range(0, rows, 1):
        table.Rows.Add()
        for c in range(0, col - startcol, 1):
            # set values for cells
            table.SetValue(r, c, data[r, c + startcol])

    print('Table created.')

    return table


def AddLabels(table, labels, numrows, col2insert):
    # add the correct labels to the ZenTable
    for r in range(0, numrows, 1):
        table.SetValue(r, col2insert, labels[r])

    return table


def ReadResultTable(filename, rowoffset, delim, tablename, table):

    # Get the Results Table from Fiji
    ValuesArray, Legends, numvar, entries, coltypelist = Conv2Array(filename, rowoffset, delim)
    table = CreateTable(ValuesArray, numvar, entries, Legends, 1, tablename, coltypelist, table)
    # Read the slice or frame labels separately since those are strings
    labels = Conv2List(filename, rowoffset, delim, 1)
    # Add them to the Zen table to replace the NaNs
    table = AddLabels(table, labels, entries, 0)

    return table


def Fiji2ZenStageXY(PosX_Fiji, PosY_Fiji, ImageCenterStageX, ImageCenterStageY, ImageWidth, ImageHeight, output=False):

    # calculate the origin of the image in stage coordinates
    OriginImage_as_StageX = ImageCenterStageX - (ImageWidth / 2)
    OriginImage_as_StageY = ImageCenterStageY - (ImageHeight / 2)
    End_ImageX_as_StageX = OriginImage_as_StageX + ImageWidth
    End_ImageY_as_StageY = OriginImage_as_StageY + ImageHeight

    # calculate the coordinates of the bounding box as stageXY coordinates inside ZEN
    PosX_Fiji_ZenStageX = OriginImage_as_StageX + PosX_Fiji
    PosY_Fiji_ZenStageY = OriginImage_as_StageY + PosY_Fiji

    if output:
        print('OriginImage_as_StageX = ', OriginImage_as_StageX)
        print('OriginImage_as_StageY = ', OriginImage_as_StageY)
        print('End_ImageX_as_StageX  = ', End_ImageX_as_StageX)
        print('End_ImageY_as_StageY  = ', End_ImageY_as_StageY)
        print('PosX_Fiji_ZenStageX   = ', PosX_Fiji_ZenStageX)
        print('PosY_Fiji_ZenStageY   = ', PosY_Fiji_ZenStageY)

    return PosX_Fiji_ZenStageX, PosY_Fiji_ZenStageY


def CheckTableColumns(table2check, requiredcols=['BX', 'BY', 'Width', 'Height']):

    columnIDs = {}
    hasBX = False
    hasBY = False
    hasWidth = False
    hasHeight = False

    # the table must contain the colums BX, BY Width, Height
    for column in range(0, table2check.ColumnCount):

        columnName = table2check.Columns[column].ColumnName

        if columnName == requiredcols[0]:
            hasBX = True
            columnIDs[requiredcols[0]] = column

        if columnName == requiredcols[1]:
            hasBY = True
            columnIDs[requiredcols[1]] = column

        if columnName == requiredcols[2]:
            hasWidth = True
            columnIDs[requiredcols[2]] = column

        if columnName == requiredcols[3]:
            hasHeight = True
            columnIDs[requiredcols[3]] = column

    columnsOK = hasBX and hasBY and hasWidth and hasHeight

    return columnIDs, columnsOK


def createFijistring(imagejdir, scriptfile, jsonfile):

    # this string can be created by using the following from the commadline
    # c:\Users\Public\Fiji> ImageJ-win64.exe --dry-run --ij2 --headless --console
    #
    # Please adjust the memory to your needs based on your current system !!! When the local Fiji is updated, make sure that the string still works
    # by testing it out using the commands shown above.

    # replace
    fijistr = r"-Dpython.cachedir.skip=true -Dplugins.dir=FJD -Xmx8000m -Djava.awt.headless=true -Dapple.awt.UIElement=true -Xincgc -XX:PermSize=128m -Djava.class.path=FJD/jars/imagej-launcher-4.0.5.jar -Dimagej.dir=FJD -Dij.dir=FJD -Dfiji.dir=FJD -Dfiji.defaultLibPath=bin/server/jvm.dll -Dfiji.executable=FJD\\ImageJ-win64.exe -Dij.executable=FJD\\ImageJ-win64.exe -Djava.library.path=FJD/lib/win64;FJD/mm/win64;FJD/lib/fftw;FJD/lib/jcuda-6.5 -Dscijava.context.strict=false net.imagej.launcher.ClassLauncher -ijjarpath jars -ijjarpath plugins net.imagej.Main --run SCRIPTLOC JSONPARAMFILE"
    fijistr = fijistr.Replace("FJD", imagejdir)
    fijistr = fijistr.Replace("SCRIPTLOC", scriptfile)
    fijistr = fijistr.Replace("JSONPARAMFILE", "JSONPARAMFILE='" + jsonfile + "'")

    return fijistr
