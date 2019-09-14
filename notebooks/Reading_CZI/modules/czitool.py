#################################################################
# File       : czitool.py
# Version    : 0.3
# Author     : czsrh
# Date       : 21.01.2019
# Insitution : Carl Zeiss Microscopy GmbH
#
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


import sys
import numpy as np
import czifile as zis
import xmltodict
import xml.etree.ElementTree as ET


def replaceZeroNaN(data, value=0):

    data = data.astype('float')
    data[data == value] = np.nan

    return data


def readczi(filename, replacezero=True):

    # get CZI object and read array
    czi = zis.CziFile(filename)
    array = czi.asarray()
    md = czi.metadata()

    # parse the XML into a dictionary
    metadata = xmltodict.parse(md)

    # create dictionary for the interesting CZI metadata
    czimd = {}

    # add axes and shape information
    czimd['Axes'] = czi.axes
    czimd['Shape'] = czi.shape

    try:
        czimd['Experiment'] = metadata['ImageDocument']['Metadata']['Experiment']
    except:
        czimd['Experiment'] = None

    try:
        czimd['HardwareSetting'] = metadata['ImageDocument']['Metadata']['HardwareSetting']
    except:
        czimd['HardwareSetting'] = None

    try:
        czimd['CustomAttributes'] = metadata['ImageDocument']['Metadata']['CustomAttributes']
    except:
        czimd['CustomAttributes'] = None

    czimd['Information'] = metadata['ImageDocument']['Metadata']['Information']
    czimd['PixelType'] = czimd['Information']['Image']['PixelType']
    czimd['SizeX'] = czimd['Information']['Image']['SizeX']
    czimd['SizeY'] = czimd['Information']['Image']['SizeY'] 
        
    try:
        czimd['SizeZ'] = czimd['Information']['Image']['SizeZ']
    except:
        czimd['SizeZ'] = None
        
    try:
        czimd['SizeC'] = czimd['Information']['Image']['SizeC']
    except:
        czimd['SizeC'] = None
        
    try:    
        czimd['SizeT'] = czimd['Information']['Image']['SizeT']
    except:
        czimd['SizeT'] = None
    
    try:
        czimd['SizeM'] = czimd['Information']['Image']['SizeM']
    except:
        czimd['SizeM'] = None

    try:
        czimd['Scaling'] = metadata['ImageDocument']['Metadata']['Scaling']
        czimd['ScaleX'] = float(czimd['Scaling']['Items']['Distance'][0]['Value']) * 1000000
        czimd['ScaleY'] = float(czimd['Scaling']['Items']['Distance'][1]['Value']) * 1000000
        try:
            czimd['ScaleZ'] = float(czimd['Scaling']['Items']['Distance'][2]['Value']) * 1000000
        except:
            czimd['ScaleZ'] = None
    except:
        czimd['Scaling'] = None

    try:
        czimd['DisplaySetting'] = metadata['ImageDocument']['Metadata']['DisplaySetting']
    except:
        czimd['DisplaySetting'] = None

    try:
        czimd['Layers'] = metadata['ImageDocument']['Metadata']['Layers']
    except:
        czimd['Layers'] = None
    
    if replacezero:
        array = replaceZeroNaN(array, value=0)
    
    return array, czimd