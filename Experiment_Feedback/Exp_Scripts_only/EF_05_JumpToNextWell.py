#################################################################
# File       : EF_05_JumpToNextWell.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

### -------------------- PreScript ---------------------------------------------- ###


cells_per_well = 0  # total number of cells
logfile = ZenService.Xtra.System.AppendLogLine('Well\tTile\tCells/Tile\tCell/Well')
last_tile = 0


### -------------------- LoopScript --------------------------------------------- ###


# this value is different for every acquired picture !!!
index = ZenService.Analysis.Cells.ImageAcquisitionTime

# get cell number for the current tile
cpt = ZenService.Analysis.Cells.RegionsCount

# get current well name
well = ZenService.Analysis.Cells.ImageSceneContainerName

# get current tile number
tile = ZenService.Experiment.CurrentTileIndex

# reset the counter if a new well is started, (i.e. tile < lasttile)
if tile != last_tile:
    if tile < last_tile:
        cells_per_well = 0

    # add cells from current tile to cell_per_well
    cells_per_well = cells_per_well + cpt

# write data into log file
logfile = ZenService.Xtra.System.AppendLogLine(well+'\t'+str(tile)+'\t'+str(cpt)+'\t'+str(cells_per_well))

# update lasttile
last_tile = tile

# jump to next well if the desired cell number was reached
if (cells_per_well > 2000):
    ZenService.Actions.JumpToNextContainer()

    if last_tile < 25:
        logfile = ZenService.Xtra.System.AppendLogLine('Jumped to next well after ' + str(last_tile) + ' tiles')

    if last_tile == 25:
        logfile = ZenService.Xtra.System.AppendLogLine('Well completed')


### -------------------- PostScript --------------------------------------------- ###


ZenService.Xtra.System.ExecuteExternalProgram(r"C:\Program Files\Notepad++\notepad++.exe", logfile)
