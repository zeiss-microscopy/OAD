#################################################################
# File       : Automated_Analysis_Count_Cells_Active_Image.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# Run Image Analysis Script automatically after acquisition

from System.IO import Path

# get current active image
image = Zen.Application.Documents.ActiveDocument

# define output path and setting
outputpath = r'c:\ZEN_Output'

iafilename = r'c:\Users\Public\Documents\Carl Zeiss\ZEN\Documents\Image Analysis Settings\Count_Cells.czias'
ias = ZenImageAnalysisSetting()
ias.Load(iafilename)

method = 1

#### Analyze, Create Table and Export tables explicitly #######
if method == 1:

    Zen.Analyzing.Analyze(image, ias)
    # Create data list with results for all regions
    table_all = Zen.Analyzing.CreateRegionsTable(image)
    Zen.Application.Documents.Add(table_all)
    # Create data list with results for each region
    table_single = Zen.Analyzing.CreateRegionTable(image)
    Zen.Application.Documents.Add(table_single)

    # Save data list for all regions
    table_all_filename = Path.Combine(outputpath, image.Name[:-4] + '_All.csv')
    table_all.Save(table_all_filename)

    # Save data list for all single regions
    table_single_filename = Path.Combine(outputpath, image.Name[:-4] + '_Single.csv')
    table_single.Save(table_single_filename)

#### Analyze directly to CSV file #######
if method == 2:

    Zen.Analyzing.AnalyzeToFile(image, ias, outputpath, image.Name[:-4], False)

# close the image and image analysis setting
# image.Close()
# ias.Close()
