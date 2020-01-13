#################################################################
# File       : Automated_FindSurface_SWAF.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from System import ApplicationException
from System import TimeoutException


def runSWAF(SWAF_exp,
            delay=1,
            searchStrategy='Full',
            sampling=ZenSoftwareAutofocusSampling.Coarse,
            relativeRangeIsAutomatic=False,
            relativeRangeSize=500,
            timeout=0):

    # get current z-Position
    zSWAF = Zen.Devices.Focus.ActualPosition
    print('Z-Position before special SWAF :', zSWAF)

    # set SWAF parameters
    SWAF_exp.SetAutofocusParameters(searchStrategy=searchStrategy,
                                    sampling=sampling,
                                    relativeRangeIsAutomatic=relativeRangeIsAutomatic,
                                    relativeRangeSize=relativeRangeSize)
    try:
        print('Running special SWAF ...')
        zSWAF = Zen.Acquisition.FindAutofocus(SWAF_exp, timeoutSeconds=timeout)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
    except TimeoutException as e:
        print(e.Message)

    print('Z-Position after initial SWAF : ', zSWAF)

    return zSWAF

################## Define Parameters ##################


run_findsurface = True
store_for_recall = True
hwdelay = 1

# get the active experiment
SWAF_exp = Zen.Acquisition.Experiments.ActiveExperiment

# run FindSurface
if run_findsurface:
    try:
        # initial focussing via FindSurface to assure a good starting position
        Zen.Acquisition.FindSurface()
        print('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition)
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
        print('FindSurface (Definite Focus) failed.')

# run SWAF
zSWAF = runSWAF(DetailScan_reloaded,
                delay=hwdelay,
                searchStrategy='Full',
                sampling=ZenSoftwareAutofocusSampling.Coarse,
                relativeRangeIsAutomatic=False,
                relativeRangeSize=500,
                timeout=0)

# store resulting Z-Value inside the Definite Focus
if store_for_recall:
    try:
        # store current focus position inside DF to use it with RecallFocus
        Zen.Acquisition.StoreFocus()
        print('Stored Offset inside Definte Focus.')
    except ApplicationException as e:
        print('Application Exception : ', e.Message)
        print('StoreFocus (Definite Focus) failed.')
