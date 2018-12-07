#################################################################
# File       : EF_02_Plot_Cells_Tiles_DAPI.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################

### -------------------- PreScript ---------------------------------------------- ###


from System.Diagnostics import Process
cells_total = 0
logfile = ZenService.Xtra.System.AppendLogLine('Tile \t Cells \t Total \t PosX \t PosY')


### -------------------- LoopScript --------------------------------------------- ###


# get cell number for current tile
cn = ZenService.Analysis.Cells.RegionsCount
# get current tile number
tn = ZenService.Experiment.CurrentTileIndex
# calculate sum of cells measured up to now
cells_total = cells_total + cn

# stop condition if a cell number is reached
if (cells_total > 3000):
    ZenService.Actions.StopExperiment()

# read xy position of current image
posx = ZenService.Analysis.Cells.ImageStageXPosition0
posy = ZenService.Analysis.Cells.ImageStageYPosition0

# write into log file
logfile = ZenService.Xtra.System.AppendLogLine(str(tn) + '\t' + str(cn) + '\t' + str(cells_total) + '\t' + str(posx) + '\t' + str(posy))


### -------------------- PostScript --------------------------------------------- ###


# open editor to display the logfile
ZenService.Xtra.System.ExecuteExternalProgram(r"C:\Program Files\Notepad++\notepad++.exe", logfile)

# define filename, external application and python script
filename = ZenService.Experiment.ImageFileName[:-4] + '_Log.txt'
exeloc = 'python'
script = r'C:\Python_Scripts\display_results_tiles.py'
cmd = script + ' -f ' + filename

# start Python Option 1
#ZenService.Xtra.System.ExecuteExternalProgram(script, ' -f ' + filename)

# start Python Option 2
app = Process()
app.StartInfo.FileName = exeloc
app.StartInfo.Arguments = cmd
app.Start()
