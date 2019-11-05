
#######################################################
## A C Q U I S I T I O N - M O D I F Y  T I L E  R E G I O N S 
##
## Macro name: OAD_Training_Modify Tile Regions
##
## Required files: None
## Required demo files: None
##
## Required module/licence:
##
## DESCRIPTION: Run image analysis and modify experiment based on the results of IA
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################


# For testing purposes - Load overview scan image automatically instead of executing the "real" experiment
output_OVScan = Zen.Application.LoadImage(r"C:\Users\M1MALANG\Pictures\Experiment-19.czi", False)

# Load analysis setting created by the wizard or an separate macro
ias = ZenImageAnalysisSetting()

# load image analysis setting (needs to contain Bound center X stage, Bound center Y stage, Bound Height, Bound Width)
ias.Load("GA_Cell_counting")

# Load detailed Scan
DetailScan = Zen.Acquisition.Experiments.GetByName("GA_OAD_Training_Detail")

# Analyse the image
Zen.Analyzing.Analyze(output_OVScan, ias)

# Create Zen table with results for each single object
SingleObj = Zen.Analyzing.CreateRegionTable(output_OVScan)

# check for existence of required column names inside table
soi = SingleObj.GetBoundsColumnInfoFromImageAnalysis(True)

# 1st item is a bool indicating if all required columns could be found
columnsOK = soi.AreRequiredColumnsAvailabe

# show and save data tables to the specified folder
Zen.Application.Documents.Add(SingleObj)

# check the number of detected objects = rows inside image analysis table
num_POI = SingleObj.RowCount

############## Prepare DetailScan #################

# move to 1st detected object to be at a XY-position that makes sense
xpos_1st = SingleObj.GetValue(0, soi.CenterXColumnIndex)
ypos_1st = SingleObj.GetValue(0, soi.CenterYColumnIndex)
Zen.Devices.Stage.MoveTo(xpos_1st , ypos_1st)


# get z-position
zpos = Zen.Devices.Focus.ActualPosition

# active the temporary experiment to trigger its validation
DetailScan.SetActive()

# check if the experiment contains tile regions
DetailIsTileExp = DetailScan.IsTilesExperiment(0)

############# START DETAILED SCAN EXPERIMENT #############

# execute detailed experiment at the position of every detected object
for i in range(0, num_POI, 1):

    # get the object information from the position table
    # get the ID of the object - IDs start with 2 !!!
    POI_ID = SingleObj.GetValue(i, 0)
    #POI_ID = SingleObj.GetValue(i, column_ID)

    # get XY-stage position from table
    xpos = SingleObj.GetValue(i, soi.CenterXColumnIndex)
    ypos = SingleObj.GetValue(i, soi.CenterYColumnIndex)

    # move to the current position
    Zen.Devices.Stage.MoveTo(xpos, ypos)


    # if DetailScan is a Tile Experiment
    if DetailIsTileExp:

        # Modify tile center position - get bounding rectangle width and height in microns
        bcwidth = SingleObj.GetValue(i, soi.WidthColumnIndex)
        bcheight = SingleObj.GetValue(i, soi.HeightColumnIndex)

        # Modify the XYZ position and size of the TileRegion on-the-fly
        DetailScan.ClearTileRegionsAndPositions(0)
        DetailScan.AddRectangleTileRegion(0, xpos, ypos, bcwidth, bcheight, zpos)


    if not DetailIsTileExp:
        print('Detailed Experiment does not contains TileRegions. Nothing to modify.')

    # execute the DetailScan experiment
    output_detailscan = Zen.Acquisition.Execute(DetailScan)
    Zen.Application.Documents.Add(output_detailscan)
