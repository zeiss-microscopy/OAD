"""  
Author: Sebastian Rhode
Date: 2016_10_07
File: FindSurface_SWAF_ActiveExp.czmac
Version: 1.0
"""
# clear output
Zen.Application.MacroEditor.ClearMessages()

# Run initial FindSurface
Zen.Acquisition.FindSurface()
print 'FindSurface Result z-value: ', Zen.Devices.Focus.ActualPosition

# Run Autofocus using the active experiment
SWAF_exp = Zen.Acquisition.Experiments.ActiveExperiment
Zen.Acquisition.FindAutofocus(SWAF_exp)
print 'SWAF Result z-value: ', Zen.Devices.Focus.ActualPosition

# store facus value inside DF.2 for Recall Focus
Zen.Acquisition.StoreFocus()
print 'Store Focus Z-Value for RecallFocus. Done.'
