#######################################################
## A C Q U I S I T I O N - A U T O F O C U S
##
## Macro name: OAD_Training_SWAF_Simple
##
## Required files: "OAD_Training_Exp.czexp"
## Required demo files: None
##
## Required module/licence:
##
## DESCRIPTION: Run experiment with SW Autofocus
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################
  
# clear macro editor output
Zen.Application.MacroEditor.ClearMessages()

exp = ZenExperiment()
exp = Zen.Acquisition.Experiments.ActiveExperiment
#exp = Zen.Acquisition.Experiments.GetByName("OAD_Training_Exp.czexp")

# get actual position
old_pos = Zen.Devices.Focus.ActualPosition
print(str(old_pos))

# Run Autofocus based on the settings defined in the Experiment
try:
    Zen.Acquisition.FindAutofocus(exp, 30)
except:
    print("SWAF failed, the original position will be used")

# get actual position
new_pos = Zen.Devices.Focus.ActualPosition
print(str(new_pos))