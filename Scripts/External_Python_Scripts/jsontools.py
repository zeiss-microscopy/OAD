"""
File: jsontools.py
Author: Sebastian Rhode
Date: 2018_03_14
"""
version = 0.1

import clr
from System.IO import Directory, Path, File, FileInfo
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer


# Write output json
def write_json(metadata, jsonfile='Metadata.json', savepath=r'C:\Temp'):
    jsonfile = Path.Combine(savepath, jsonfile)
    js = JavaScriptSerializer().Serialize(metadata)
    File.WriteAllText(jsonfile, js)

    return jsonfile


# read JSON file as to string
def readjson(jsonfile):
    datastring = File.ReadAllText(jsonfile)
    json_dict = JavaScriptSerializer().DeserializeObject(datastring)

    return json_dict


# Create metadata from the image
def fill_metadata(image):
    metadata = {}
    # this must be written to the output JSON for CA
    metadata['IMAGEFILENAME'] = image.Name
    metadata['IMAGEFILEPATH'] = image.FileName
    metadata['CENTERX'] = image.Metadata.StagePositionMicron.X
    metadata['CENTERY'] = image.Metadata.StagePositionMicron.Y
    metadata['WIDTH_PIXEL'] = int(image.Metadata.Width)
    metadata['HEIGHT_PIXEL'] = int(image.Metadata.Height)
    metadata['SCALEX'] = round(image.Metadata.ScalingMicron.X, 3)
    metadata['SCALEY'] = round(image.Metadata.ScalingMicron.Y, 3)
    metadata['SCALEZ'] = round(image.Metadata.ScalingMicron.Z, 3)
    metadata['WIDTH_MICRON'] = round(metadata['WIDTH_PIXEL'] * image.Metadata.ScalingMicron.X, 3)
    metadata['HEIGHT_MICRON'] = round(metadata['HEIGHT_PIXEL'] * image.Metadata.ScalingMicron.Y, 3)

    return metadata
