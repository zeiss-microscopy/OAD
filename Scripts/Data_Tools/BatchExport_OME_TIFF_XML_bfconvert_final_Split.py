#################################################################
# File       : BatchExport_OME_TIFF_XML_bfconvert_final_Split.py
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

import sys
import clr
import time
from System.Diagnostics import Process
from System.IO import Directory, Path, File, FileInfo


def removeczi(removedir):

    # check directory for files to export
    czi2remove = Directory.GetFiles(removedir, '*.czi')
    print('Number of files to be removed: ', len(czi2remove))

    for czi in czi2remove:
        # delete the splitted CZI files when option was checked
        try:
            File.Delete(czi)
            print('Removed: ', czi)
        except:
            print('Could not remove: ', czi)

    print('Removal complete.')


# clear output console
Zen.Application.MacroEditor.ClearMessages()
# specify the desired destination folder
#defaultdir = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Wellplate\CZI_Wellplate_Export\Test'
defaultdir = r'c:\data'

#########################################   !!!   ############################################
# default directory for bftools - please check location and modify if required!
exelocfolder_default = r'c:\data\bftools_5.5.0'

# define location of batch script to be used
batfolder_default = r'c:\data\Data_Export'
batchfile = 'czi2ometiff_xml_split.bat'
exeloc = '"' + Path.Combine(batfolder_default, batchfile) + '"'
#########################################   !!!   ############################################

# splittiung options for bfconvert - the space is important!
splitoptions = ['NOSPLIT', 'T']

# create setup dialog and enter source and destination directory with GUI
window = ZenWindow()
window.Title = 'Export CZI as OME-TIFF using bfconvert with options - Version: ' + str(version)
window.AddFolderBrowser('sourcedir', 'Source folder: ', defaultdir)
window.AddCheckbox('splitczi', 'Split CZIs into single files', True)
window.AddLabel('----- Export as OME-TIFF and options ---')
window.AddCheckbox('omeexp', 'Export as OME-TIFF after Split', True)
window.AddCheckbox('bfsplitczi', 'Split Dimensions for single OME-TIFFs', True)
window.AddDropDown('splitoption', 'Spliting Option', splitoptions, 1)
window.AddCheckbox('cziremove', 'Remove single CZIs after Split and OME-Export', False)
window.AddLabel('-------------- Metadata Options --------------')
window.AddCheckbox('omexml', 'Create OME-XML from CZI', False)
window.AddLabel('----------------  Misc -----------------')
window.AddCheckbox('waitkey', 'Wait for key press after every file (for testing)', False)
window.AddLabel('---------- bftools location -----------')
window.AddFolderBrowser('bftoolsdir', 'bftools directory:', exelocfolder_default)

# show the window
result = window.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit(message)

# read results from dialog
exedir = result.GetValue('bftoolsdir')
sourcedir = result.GetValue('sourcedir')
split = result.GetValue('splitczi')
bfsplit = result.GetValue('bfsplitczi')
splitopt = result.GetValue('splitoption')
chadd = result.GetValue('addch')
omeexport = result.GetValue('omeexp')
chadd = result.GetValue('addch')
createomexml = result.GetValue('omexml')
waitforkey = result.GetValue('waitkey')
czidelete = result.GetValue('cziremove')

# check directory for files to export
czidir = Directory.GetFiles(sourcedir, '*.czi')
numczi = czidir.Length

# this list contains the subdirectories created for splitting
splitdirs = []

if split == True:

    print('Split CZI using Split Scenes (Write Files): yes')
    # Batch Loop - Load all CZI images and do Split Scenes (Write Files)
    for i in range(0, numczi):
        # get current CZI file
        czifile = czidir[i]
        file_woExt = Path.GetFileNameWithoutExtension(czifile)
        # create separate directory for the current file
        splitdir = Path.Combine(sourcedir, file_woExt + '_Single')
        Directory.CreateDirectory(splitdir)
        # store directory name inside list
        splitdirs.append(splitdir)
        print('File to split: ', czifile)
        image = Zen.Application.LoadImage(czifile, False)

        # split single CZI file containing all wells into single CZI files
        Zen.Processing.Utilities.SplitScenes(image, splitdir, ZenCompressionMethod.None, True, True, False)
        # close file
        image.Close()
        print('Finished Split Scences (Write Files): ', czifile)

elif split == False:
    # set the splitdir to the original folder when no splitting takes place
    print('Split CZI using Split Scenes (Write Files): no')
    splitdirs.append(sourcedir)

print('----------------------------------------------------')

for dir in splitdirs:

    option = ' "' + dir + '"'

    if omeexport == True:
        print('Export as OME-TIFF: yes')
        option = option + ' -export'
    elif omeexport == False:
        print('Export as OME-TIFF: no')
        option = option + ' -noexport'

    if createomexml == True:
        print('Create OME_XML from CZI: yes')
        option = option + ' -xml'
    elif createomexml == False:
        print('Create OME_XML from CZI: no')
        option = option + ' -noxml'

    if waitforkey == True:
        # wait for key press inside the command line window after every CZI file
        print('Wait at the end for key press: yes')
        option = option + ' -wait'
    if waitforkey == False:
        print('Wait at the end for key press: no')
        option = option + ' -nowait'

    if czidelete == True:
        print('Remove CZIs after Split Scenes (Write Files): yes.')
    elif czidelete == False:
        print('Remove CZIs after Split Scenes (Write Files): no')

    # add directory containing the bftools to the options
    option = option + ' "' + exedir + '"'

    if bfsplit == True:
        print('Split single CZIs using bfconvert: ', splitopt)
        option = option + ' -' + splitopt
    elif bfsplit == False:
        print('No splitting using bfconvert: -NOSPLIT')
        option = option + ' -NOSPLIT'

    # run commad line argument
    print('Batch script to run the OME-TIFF export using bfconvert.')
    print('Argument: ' + exeloc)
    print('Working directory: ', dir)
    print('...')
    time.sleep(2)

    # start batch script (*.bat) to use the bftools
    app = Process()
    print('Batch File to run: ', exeloc)
    print('Batch Options    : ', option)
    app.StartInfo.FileName = exeloc
    app.StartInfo.Arguments = option
    app.Start()
    # wait until the batch script is finished
    app.WaitForExit()

# remove czis from all created subdirs and only when the option was set
if czidelete == True and split == True:
    for dir2clean in splitdirs:
        print('Removing CZIs in created subdirectories ...')
        removeczi(dir2clean)

print('Export finished.')
