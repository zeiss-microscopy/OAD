#######################################################
## H A R D W A R E
##
## Macro name: OAD_Training_get HWS.py
##
## Required files: None
## Required demo files: None
##
## Required module/licence:
##
## DESCRIPTION: Read and set Hardwaresettings
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################

HWS = Zen.Devices.ReadHardwareSetting()

#HWS = ZenHardwareSetting()

#HWS.Load('HWS_5x.czhws')


# Get the IDs of every component in the Hardware Setting:
HWSIDs = HWS.GetAllComponentIds()
"""
# go through all the Component IDs
for ID in HWSIDs:
    print(ID)
    

    
    # for each Component ID get the Parameter names
    HWSParams = HWS.GetAllParameterNames(ID)
    
    # go through all Parameters
    for HWSParam in HWSParams:
        print("\t" + HWSParam)

"""

focus_params = HWS.GetAllParameterNames('MTBFocus')

for param in focus_params:
    print param



focus_position = HWS.GetParameter('MTBFocus', 'Position')
print(focus_position)


HWS.SetParameter('MTBFocus', 'Position', -7000)

focus_position = HWS.GetParameter('MTBFocus', 'Position')
print(focus_position)


#HWS.SaveAs("HWS_02")

