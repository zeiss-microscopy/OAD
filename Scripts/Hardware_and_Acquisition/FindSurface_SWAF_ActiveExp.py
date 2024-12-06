#################################################################
# File       : FindSurface_SWAF_ActiveExp.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# clear output
Zen.Application.MacroEditor.ClearMessages()

# Run initial FindSurface
Zen.Acquisition.FindSurface()
print('FindSurface Result z-value: ', Zen.Devices.Focus.ActualPosition)

# Run Autofocus using the active experiment
SWAF_exp = Zen.Acquisition.Experiments.ActiveExperiment
Zen.Acquisition.FindAutofocus(SWAF_exp)
print('SWAF Result z-value: ', Zen.Devices.Focus.ActualPosition)

# store facus value inside DF.2 for Recall Focus
Zen.Acquisition.StoreFocus()
print('Store Focus Z-Value for RecallFocus. Done.')
