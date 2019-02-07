#################################################################
# File       : EF_11_Scratch_Assay_dynamic.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

### -------------------- PreScript ---------------------------------------------- ###


from System.Diagnostics import Process

filename = ZenService.Experiment.ImageFileName[:-4] + '_Log.txt'
exeloc = 'python'
script = r'C:\Python_Scripts\EF_ScratchAssay.py'
cmd = script + ' -f ' + filename
ZenService.Xtra.System.WriteDebugOutput(str(filename))

# start Python Option 1
#ZenService.Xtra.System.ExecuteExternalProgram(script, ' -f ' + filename)

# start Python Option 2
app = Process()
app.StartInfo.FileName = exeloc
app.StartInfo.Arguments = cmd
app.Start()


### -------------------- LoopScript --------------------------------------------- ###


# get the current well name, column idex, row index and position index
frame = ZenService.Experiment.CurrentTimePointIndex

# get area parameters for the scratchnumber of cells from current image
area_t = ZenService.Analysis.Scratch.RegionsArea
area_p = ZenService.Analysis.Scratch.RegionsAreaPercentage

# create logfile
logfile = ZenService.Xtra.System.AppendLogLine(str(frame)+'\t'+str(area_t) + '\t' + str(area_p))


### -------------------- PostScript --------------------------------------------- ###


# open logfile
ZenService.Xtra.System.ExecuteExternalProgram(logfile, r'C:\Program Files (x86)\Notepad++\notepad++.exe')
