# -*- coding: utf-8 -*-
"""
@author: Sebi

File: czitools.py
Date: 01.02.2019
Version. 1.2
"""

import misctools as misc
import czifile as zis
import numpy as np
import re
from collections import Counter
import xml.etree.ElementTree as ET


def get_metainfo_channel_description(filename):

    try:
        czi = zis.CziFile(filename)
        namelst = []
        valuelst = []
        # get root tree of CZI metadata (uses ElementTree)

        for elem in czi.metadata.getiterator():

            namelst.append(elem.tag)
            valuelst.append(elem.text)

        # get the channel descriptions
        ids = misc.find_index_byname(namelst, 'Description')
        chdescript = misc.get_entries(valuelst, ids)

        czi.close()

    except:
        chdescript = 'n.a.'

    return chdescript


def writexml_czi(filename):

    # write xml file to disk
    czi = zis.CziFile(filename)

    # Change File name and write XML file to same folder
    xmlfile = filename.replace('.czi', '_CZI_MetaData.xml')
    tree = czi.metadata.getroottree()
    tree.write(xmlfile, encoding='utf-8', method='xml')
    print('Write special CZI XML metainformation for: ', xmlfile)

    czi.close()


def get_objective_name_cziread(filename):

    czi = zis.CziFile(filename)
    namelst = []
    valuelst = []
    # get root tree of CZI metadata (uses ElementTree)

    for elem in czi.metadata.getiterator():

        namelst.append(elem.tag)
        valuelst.append(elem.text)

    # get the channel descriptions
    try:
        ids = misc.find_index_byname(namelst, 'ObjectiveName')
        objname = misc.get_entries(valuelst, ids)
    except:
        objname = 'n.a.'

    czi.close()


def read_dimensions_czi(filename):

    # Read the dimensions of the image stack and their order
    czi = zis.CziFile(filename)
    czishape = czi.shape
    cziorder = czi.axes
    czi.close()

    return czishape, cziorder


def get_numscenes(filename):
    """
    Currently the number of scenes cannot be read directly using BioFormats so
    czifile.py is used to determine the number of scenes.
    """

    # Read the dimensions of the image stack and their order
    czi = zis.CziFile(filename)

    # find the index of the "S" inside the dimension string
    try:
        si = czi.axes.index("S")
        numscenes = czi.shape[si]
    except:
        # if no scene was found set to 1
        numscenes = 1

    czi.close()

    return numscenes


def get_shapeinfo_cziread(filename):
    # get CZI shape and dimension order using czifile.py

    try:
        czi = zis.CziFile(filename)
        czishape = czi.shape
        cziorder = czi.axes

        czi.close()

    except:

        print('czifile.py did not detect an CZI file.')
        czishape = 'unknown'
        cziorder = 'unknown'

    return czishape, cziorder


def get_metainfo_cziread(filename):

    # define default values in case something is missing inside the metadata
    objNA = np.NaN
    objMag = np.NaN
    objName = 'n.a.'
    objImm = 'n.a.'
    CamName = 'n.a.'
    totalMag = np.NaN

    try:
        czi = zis.CziFile(filename)

        # Iterate over the metadata
        for elem in czi.metadata.getiterator():

            if elem.tag == 'LensNA':
                objNA = np.float(elem.text)

            if elem.tag == 'NominalMagnification':
                objMag = elem.text

            if elem.tag == 'ObjectiveName':
                objName = elem.text

            if elem.tag == 'Immersion':
                objImm = elem.text

            if elem.tag == 'CameraName':
                CamName = elem.text

            if elem.tag == 'TotalMagnification':
                totalMag = np.float(elem.text)
                if totalMag == 0:
                    totalMag == 'n.a.'

        czi.close()

    except:

        print('czifile.py did not detect an CZI file.')

    return objNA, objMag, objName, objImm, CamName, totalMag


def get_metainfo_cziread_camera(filename):

    czi = zis.CziFile(filename)

    md = czi.metadata
    tree = ET.ElementTree(ET.fromstring(md))
    root = ET.fromstring(md)

    # Iterate over the metadata
    for elem in tree.iter():
        if elem.tag == 'CameraName':
            cameraname = elem.text

    czi.close()

    return cameraname


def get_metainfo_cziread_detetcor(filename):

    czi = zis.CziFile(filename)

    md = czi.metadata
    tree = ET.ElementTree(ET.fromstring(md))
    root = ET.fromstring(md)

    # Iterate over the metadata
    for elem in tree.iter():
        if elem.tag == 'Detetctor':
            detectorname = elem.text

    czi.close()

    return detectorname


def getWellInfofromCZI(wellstring):

    # labeling schemes for plates up-to 1536 wellplate
    colIDs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
              '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
              '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', ]

    rowIDs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']

    wellOK = wellstring[1:]
    wellOK = wellOK[:-1]
    wellOK = re.sub(r'\s+', '', wellOK)
    welllist = [item for item in wellOK.split(',') if item.strip()]

    cols = []
    rows = []

    for i in range(0, len(welllist)):
        wellid_split = re.findall('\d+|\D+', welllist[i])
        well_ch = wellid_split[0]
        well_id = wellid_split[1]
        cols.append(np.int(well_id) - 1)
        well_id_index = rowIDs.index(well_ch)
        rows.append(well_id_index)

    welldict = Counter(welllist)

    numwells = len(welllist)

    return welllist, cols, rows, welldict, numwells


def getXMLnodes(filename_czi, searchpath, showoutput=False):

    czi = zis.CziFile(filename_czi)
    tree = czi.metadata.getroottree()

    tag = []
    attribute = []
    text = []

    if showoutput:
        print('Path      : ', searchpath)

    for elem in tree.iterfind(searchpath):

        tag.append(elem.tag)
        attribute.append(elem.attrib)
        text.append(elem.text)

        if showoutput:
            print('Tag       : ', elem.tag)
            print('Attribute : ', elem.attrib)
            print('Text      : ', elem.text)

    if showoutput:
        print('-----------------------------------------------------------------------------------------------')

    return tag, attribute, text
