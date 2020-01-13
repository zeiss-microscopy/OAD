#################################################################
# File       : EF_07_Cell_Count_Blocks.py
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


# define blocks to be analyzed
blocks2do = [1, 3]

# blocks where nothing happens
blocksnot2do = [2]

# header for logfile
logfile = ZenService.Xtra.System.AppendLogLine('Block\tFrame\tCells')


### -------------------- LoopScript --------------------------------------------- ###


block = ZenService.Experiment.CurrentBlockIndex
frame = ZenService.Experiment.CurrentTimePointIndex

if block in blocks2do:
    # get current frame number, number of cells
    cn = ZenService.Analysis.Cells.RegionsCount
    # write into logfile
    logfile = ZenService.Xtra.System.AppendLogLine(str(block) + '\t' + str(frame) + '\t' + str(cn))


elif block in blocksnot2do:
    # write into logfile
    logfile = ZenService.Xtra.System.AppendLogLine(str(block) + '\t' + str(frame) + '\t' + 'skipped analysis')
    # play sound
    ZenService.Xtra.System.PlaySound()


### -------------------- PostScript --------------------------------------------- ###


# Open logfile in Notepad++
ZenService.Xtra.System.ExecuteExternalProgram(r"C:\Program Files\Notepad++\notepad++.exe", logfile)
