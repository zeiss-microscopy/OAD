#################################################################
# File       : EF_08_Time_Lapse_zStack.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################

### -------------------- PreScript ---------------------------------------------- ###


# count the loops from experiment designer (=number of Z-layers)
loopcount = 0

# define the z-stack
deltaz = 5.0  # spacing of z-stack (um)
# zpos = 240.7 # set start position for z-stack
zpos = ZenService.HardwareActions.ReadFocusPosition()  # get focus position as start position for z-stack

# number of Timepoints from Time Series Toolwindow
timepoints = 5

# write header for logfile
logfile = ZenService.Xtra.System.AppendLogLine('Position\tz-pos[um]\tTimepoint')


### -------------------- LoopScript --------------------------------------------- ###


# current time point
timepoint = ZenService.Experiment.CurrentTimePointIndex

# create logfile
logfile = ZenService.Xtra.System.AppendLogLine(str(loopcount+1) + '\t' + str(zpos) + '\t' + str(timepoint))

if (timepoint == timepoints):
    # increase loop counter
    loopcount = loopcount + 1
    # calculate new z-position for next timelapse
    zpos = zpos + deltaz
    # set new focus position
    ZenService.HardwareActions.SetFocusPosition(zpos)


### -------------------- PostScript --------------------------------------------- ###


# Open logfile in Notepad++
ZenService.Xtra.System.ExecuteExternalProgram(r"C:\Program Files\Notepad++\notepad++.exe", logfile)
