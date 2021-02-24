# @File(label = "Image File", persist=True, style='file', description='Select an CZI Image file') FILENAME
# @Boolean(label = "Stitch Tiles", value=True, persist=True, description='Stitch Tiles of Mosaic CZI Image') STITCHTILES
# @Integer(label = "Read Pyramid Level (0 - ...)", value=0, persist=True, description='Read a specific level of the CZI image pyramid') READPYLEVEL
# @Boolean(label = "Open All Series", value=True, persist=True, description='Try to open all series. Only works for compatible Image Series') OPENALLSERIES
# @Boolean(label = "Concatenate Series", value=True, persist=True, description='Concatenate series. Only works for compatible Image Series') SETCONCAT
# @Boolean(label = "Show OME-XML data", value=False, persist=True, description='Show the OME-XML metadata in a separate window') SHOWOMEXML
# @Boolean(label = "Show Preview Image attachment", value=False, persist=True, description='Try to open the CZI Image attachment') ATTACH
# @Boolean(label = "Autoscale", value=True, persist=True, description='Autoscale CZI after opening') AUTOSCALE
# @OUTPUT String FILENAME
# @OUTPUT Boolean STITCHTILES
# @OUTPUT Integer READPYLEVEL
# @OUTPUT Boolean OPENALLSERIES
# @OUTPUT Boolean SETCONCAT
# @OUTPUT Boolean SHOWOMEXML
# @OUTPUT Boolean ATTACH
# @OUTPUT Boolean AUTOSCALE

# @UIService uiService
# @LogService log

#################################################################
# File        : czireader_complete.py
# Version     : 0.5
# Author      : czsrh
# Date        : 24.02.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################


import os
import sys
from collections import OrderedDict
from org.scijava.log import LogLevel
from java.lang.System import getProperty
sys.path.append(getProperty('fiji.dir') + '/scripts')
from fijipytools import ImportTools, MetaData

# clear the console automatically when not in headless mode
uiService.getDefaultUI().getConsolePane().clear()

# when set to True the number of pyramid levels can be read
setflatres = False

# get the FILENAME as string
imagefile = FILENAME.toString()

log.log(LogLevel.INFO, 'Filename              : ' + imagefile)
log.log(LogLevel.INFO, '-----------------------------------------')
log.log(LogLevel.INFO, 'Stitch Tiles          : ' + str(STITCHTILES))
log.log(LogLevel.INFO, 'Pyramid Level [0-...] : ' + str(READPYLEVEL))
log.log(LogLevel.INFO, 'Concatenate Series    : ' + str(SETCONCAT))
log.log(LogLevel.INFO, 'Open all Series       : ' + str(OPENALLSERIES))
log.log(LogLevel.INFO, 'Show OME-XML          : ' + str(SHOWOMEXML))
log.log(LogLevel.INFO, 'Open Attachment       : ' + str(ATTACH))
log.log(LogLevel.INFO, 'Autosale Image        : ' + str(AUTOSCALE))


# read the CZI image
imp, metainfo = ImportTools.openfile(imagefile,
                                    stitchtiles=STITCHTILES,
                                    setflatres=setflatres,
                                    readpylevel=READPYLEVEL,
                                    setconcat=SETCONCAT,
                                    openallseries=OPENALLSERIES,
                                    showomexml=SHOWOMEXML,
                                    attach=ATTACH,
                                    autoscale=AUTOSCALE)


# show the CZI image
imp.show()

# show the metadata
log.log(LogLevel.INFO, '------   CZI METADATA INFORMATION   -----')

# order the metadata dictionary
metainfo_ordered = MetaData.order_metadict(metainfo) 

for k, v in metainfo_ordered.items():
    log.log(LogLevel.INFO, str(k) + ' : ' + str(v))


if ATTACH:
    # the the CZI image attachment
    try:
        imp_attach = ImportTools.readCZIattachment(imagefile,
                                                   stitchtiles=True,
                                                   setflatres=False,
                                                   readpylevel=metainfo['SeriesCount_BF'] - 1,
                                                   setconcat=False,
                                                   openallseries=True,
                                                   showomexml=False,
                                                   attach=True,
                                                   autoscale=True)
        imp_attach.show()
    except Exception as e:
        log.log(LogLevel.INFO, e)

log.log(LogLevel.INFO, 'Done.')



