#################################################################
# File       : EF_01_Plot_Cell_Count_Simple.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

### -------------------- PreScript ---------------------------------------------- ###


from System.Diagnostics import Process


### -------------------- LoopScript --------------------------------------------- ###


# Retrieve the current image acquisition time. This will be different for every frame!
index = ZenService.Analysis.Cells.ImageIndexTime

# get the number of cells for the current frame
cn = ZenService.Analysis.Cells.RegionsCount

# write data to log file: index and number of cells
logfile = ZenService.Xtra.System.AppendLogLine(str(index) + "\t" + str(cn))


### -------------------- PostScript --------------------------------------------- ###


# Open logfile in Notepad++
ZenService.Xtra.System.ExecuteExternalProgram(r"C:\Program Files\Notepad++\notepad++.exe", logfile)

filename = ZenService.Experiment.ImageFileName[:-4] + '_Log.txt'
exeloc = 'python'
script = r'C:\Python_Scripts\display_results_simple.py'
cmd = script + ' -f ' + filename

# start Python Option 1
#ZenService.Xtra.System.ExecuteExternalProgram(script, ' -f ' + filename)

# start Python Option 2
app = Process()
app.StartInfo.FileName = exeloc
app.StartInfo.Arguments = cmd
app.Start()
