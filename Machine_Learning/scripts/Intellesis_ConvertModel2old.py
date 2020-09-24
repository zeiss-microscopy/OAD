#####################################################################
# File        : Intellesis_ConvertModel2old.py
# Version     : 0.4
# Author      : czsrh, czmri
# Date        : 18.09.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# This script can be used to convert newer CZMODEL files ZEN blue back
# to a version compatible with ZEN blue <= 3.2 or ZEN core <= 3.0
#
# Important: Backup you models for using this script at your own risk!
#
# Copyright (c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#####################################################################

# python imports
import sys
import os
import zipfile

# .NET imports
import clr
clr.AddReference('System.Xml')
clr.AddReference('System.IO.Compression')
clr.AddReference('System.Core')
import System.Xml
import System.Linq
from System.IO import Directory, Path, File, FileInfo, DirectoryInfo, FileMode, FileAccess
from System.IO.Compression import ZipArchive, ZipArchiveMode
clr.ImportExtensions(System.Linq)


def zipfolder(foldername, target_dir):
    """Zip a folder and all of its contents
    :param foldername: Name for the ZIP folder to be created
    :type foldername: str
    :param target_dir: Folder with the content to be zipped
    :type target_dir: str
    """
    filename = foldername + '.zip'
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipobj:
        rootlen = len(target_dir) + 1
        for base, dirs, files in os.walk(target_dir):
            for file in files:
                fn = os.path.join(base, file)
                zipobj.write(fn, fn[rootlen:])
    return filename


def change_dir_sep(zipfile):
    """Changes the directory separator in a zip file to backslash.

    :param zipfile: The path of the ZIP archive.
    :type zipfile: str
    """
    with File.Open(zipfile, FileMode.Open, FileAccess.ReadWrite) as f:
        with ZipArchive(f, ZipArchiveMode.Update) as archive:
            entries = archive.Entries.ToArray()
            for entry in entries:
                if '/' in entry.FullName:
                    newEntry = archive.CreateEntry(entry.FullName.replace('/', '\\'))
                    with entry.Open() as a, newEntry.Open() as b:
                        a.CopyTo(b)
                    entry.Delete()


def get_feature_extractor(modelxml):
    """Get the type of feature extractor from a czmodel
    :param modelxml: Model-XML file with model parameters
    :type modelxml: str
    :return: Name of the feature extractor
    :rtype: str
    """
    # Load XML model file
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(modelxml)
    # get the name of the feature extractor
    items = xmldoc.SelectNodes('Model/FeatureExtractor')
    for item in items:
        feature_extractor = item.InnerText
        print('Feature Extractor : ', feature_extractor)
    return feature_extractor
####################################################################


scriptversion = 0.4
newversion = '1'
remove_tmpfolder = True

# clear the output console
Zen.Application.MacroEditor.ClearMessages()

# create dialog
defaultmodeldir = r'c:\Users\m1srh\OneDrive - Carl Zeiss AG\Testdata_Zeiss\Atomic\Trained_Models'
wd = ZenWindow()
wd.Initialize('Convert CZMODEL to old format - Version: ' + str(scriptversion))
wd.AddFolderBrowser('mf', 'Select folder with CZMODEL files.', defaultmodeldir)
result = wd.Show()

# check, if Cancel button was clicked
if result.HasCanceled:
    sys.exit('Macro aborted with Cancel!')

# get the folder
basedir = result.GetValue('mf')

# get all *.czmodel files inside the folder
czmodelfiles_long = Directory.GetFiles(basedir, '*.czmodel')
czmodelfiles_short = []
for cz in czmodelfiles_long:
    czmodelfiles_short.append(Path.GetFileName(cz))

# create dialog
wd = ZenWindow()
wd.Initialize('Convert CZMODEL to old format - Version: ' + str(scriptversion))
wd.AddDropDown('czmf', 'Select individual CZMODEL to be converted', czmodelfiles_short, 0)
result = wd.Show()

# check, if Cancel button was clicked
if result.HasCanceled:
    sys.exit('Macro aborted with Cancel!')

# get the full path of the selected czmodel file
czmodelfile = Path.Combine(basedir, result.GetValue('czmf'))
print('CZMODEL selected: ', czmodelfile)

# Unzip
tempdir = Path.ChangeExtension(czmodelfile, None) + '_v1'
with zipfile.ZipFile(czmodelfile, 'r') as zip_ref:
    zip_ref.extractall(tempdir)
print('Finished unzipping: ', czmodelfile)

# get the xmlfile inside the newly created directory and load it
modelxml = Directory.GetFiles(tempdir, '*.xml')[0]
print('Load XML File: ', modelxml)
xmldoc = System.Xml.XmlDocument()
xmldoc.Load(modelxml)

# check if conversion is possible for the feature extractor
feature_extractor = get_feature_extractor(modelxml)
if feature_extractor == 'DeepNeuralNetwork':
    # stop the script execution completely
    sys.exit('Conversion to older czmodel not possible for trained DNNs.')

# select the item 'Model'
items = xmldoc.SelectNodes('Model')
for item in items:
    # get the version attribute
    version_number = item.GetAttribute('Version')
    print('Old version : ', version_number)
    try:
        # set the new version number
        item.SetAttribute('Version', newversion)
        print('Set the Modelversion to: ', newversion)
    except:
        # stop the script execution completely
        sys.exit('Could not update the Version number.')

# get the raw XML and write it to disk
rawXML = xmldoc.OuterXml
File.WriteAllText(modelxml, rawXML)

# zip the folder with the updated XML file
print('Started zipping ...')
zipfile = zipfolder(tempdir, tempdir)
change_dir_sep(zipfile)
print('Finished zipping: ', tempdir)

# rename the new zipfile to *.czmodel
print('Rename *.zip back to *.czmodel')
File.Move(zipfile, Path.ChangeExtension(zipfile, '.czmodel'))

# remover the temp folder from unzipping afterwards
if remove_tmpfolder:
    print('Deleting tempory folder : ', tempdir)
    Directory.Delete(tempdir, True)
print('Done.')
