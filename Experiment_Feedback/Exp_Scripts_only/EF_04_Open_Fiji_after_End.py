#################################################################
# File       : EF_04_Open_Fiji_after_End.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################

### -------------------- PreScript ---------------------------------------------- ###


### -------------------- LoopScript --------------------------------------------- ###


### -------------------- PostScript --------------------------------------------- ###


# get the name of the current image data set
filename = ZenService.Experiment.ImageFileName
# use the absolute path --> this works always
exeloc = 'C:\Users\Public\Documents\Fiji.app\Fiji.exe'
# specify the Fiji macro one wants to use
macro = r'-macro C:\ExperimentFeedback\Fiji\Open_CZI_and_MaxInt.ijm'
# 'glue' together the options
option = macro + ' ' + filename
# start Fiji, open the data set and execute the macro
ZenService.Xtra.System.ExecuteExternalProgram(exeloc, option)
