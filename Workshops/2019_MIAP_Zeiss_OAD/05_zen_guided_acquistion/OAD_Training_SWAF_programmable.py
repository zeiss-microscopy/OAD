#######################################################
## A C Q U I S I T I O N - A U T O F O C U S
##
## Macro name: OAD_Training_SWAF_programmable
##
## Required files: "OAD_Training_Exp.czexp"
## Required demo files: None
##
## Required module/licence:
##
## DESCRIPTION: Run experiment with programmable SW Autofocus
## 
## Copyright © 2019 by Carl Zeiss Microscopy GmbH.
## Permission is granted to use, modify and distribute this code,
## as long as this copyright notice remains part of the code.
#######################################################


def runSWAF_special(SWAF_exp,
                    delay=5,
                    searchStrategy='Full',
                    sampling=ZenSoftwareAutofocusSampling.Coarse,
                    relativeRangeIsAutomatic=False,
                    relativeRangeSize=500,
                    timeout=0):

    # get current z-Position
    zSWAF = Zen.Devices.Focus.ActualPosition
    print 'Z-Position before specilal SWAF :', zSWAF

    # set DetailScan active and wait for moving hardware due to settings
    SWAF_exp.SetActive()
    #time.sleep(delay)

    # set SWAF parameters
    SWAF_exp.SetAutofocusParameters(searchStrategy=searchStrategy,
                                    sampling=sampling,
                                    relativeRangeIsAutomatic=relativeRangeIsAutomatic,
                                    relativeRangeSize=relativeRangeSize)

    try:
        print 'Running special SWAF ...'
        zSWAF = Zen.Acquisition.FindAutofocus(SWAF_exp, timeoutSeconds=timeout)
    except ApplicationException as e:
        print 'Application Exception : ', e.Message
    except TimeoutException as e:
        print(e.Message)

    print 'Z-Position after initial SWAF : ', zSWAF
    SWAF_exp.Close()

    return zSWAF


exp = ZenExperiment()
#exp = Zen.Acquisition.Experiments.ActiveExperiment
exp = Zen.Acquisition.Experiments.GetByName("OAD_Training_Exp.czexp")


zSWAF_new = runSWAF_special(exp)

