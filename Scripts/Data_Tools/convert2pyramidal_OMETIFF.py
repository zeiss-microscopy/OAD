#####################################################################
# File        : convert2pyramidal_OMETIFF.py
# Version     : 0.3
# Author      : czsrh
# Date        : 07.03.2022
# Institution : Carl Zeiss Microscopy GmbH
#
# This script can be used to convert a CZI image into a pyramidal OME-TIFF.
# For more information on those tools please see:
#
# https://github.com/glencoesoftware/bioformats2raw
# https://github.com/glencoesoftware/raw2ometiff
#
#
# Important: CZI Image may contain preview images as an internal attachment.
# If not removed they will be also converted into a pyramidal OME-TIFF.
# Currently on LZW compression is supported.
#
# Copyright (c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Disclaimer: The script contains function and methods,
#             which are subject to change. Use at your own risk.
#####################################################################


from System.IO import File, Directory, Path
import sys
from System.Diagnostics import Process

version = 0.3


def run_tool(toolname, params):

    # run the external tool
    app = Process()
    app.StartInfo.FileName = toolname
    app.StartInfo.Arguments = params
    app.Start()
    done = app.WaitForExit()

    return done

###################################################


# clean output console
Zen.Application.MacroEditor.ClearMessages()

# defaults - adapt to your needs
bf2raw_dir = 'c:\\Temp\\bioformats2raw-0.4.0'
raw2ome_dir = 'c:\\Temp\\raw2ometiff-0.3.0'
ome_comps = ['LZW', 'Uncompressed']
py_default = 4
py_min = 1
py_max = 20

# get all open documents
CZIfiles_short = []
CZIdict = {}
opendocs = Zen.Application.Documents

for doc in opendocs:
    image = Zen.Application.Documents.GetByName(doc.Name)

    # only use CZIs
    if image.FileName.EndsWith('.czi'):
        # get the filename of the current document only when it ends with '.czi'
        CZIfiles_short.append(Path.GetFileName(image.FileName))
        CZIdict[Path.GetFileName(image.FileName)] = image.FileName

# create dialog window
wd = ZenWindow()
wd.Initialize('Convert CZI to pyramidal OME-TIFF - Version : ' + str(version))
wd.AddFolderBrowser('bf2raw_loc', 'Location of bioformats2raw', bf2raw_dir)
wd.AddFolderBrowser('raw2ome_loc', 'Location of raw2ometiff', raw2ome_dir)
wd.AddDropDown('czi', 'Select CZI Image Document', CZIfiles_short, 0)
wd.AddDropDown('comp', 'Select compression for OME-TIFF', ome_comps, 0)
wd.AddIntegerRange('reslevels', 'Number of pyramid levels OME-TIFF', py_default, py_min, py_max)
wd.AddLabel('-----------------------------------------------')
wd.AddCheckbox('clean', 'Clean Up TMP Files and Folder afterwards', True)
result = wd.Show()

if result.HasCanceled:
    sys.exit('Macro aborted with Cancel!')

# get the input values and store them
cziname = result.GetValue('czi')
czifile = CZIdict[cziname]
czidir = Path.GetDirectoryName(czifile)
bf2raw_dir = result.GetValue('bf2raw_loc')
raw2ome_dir = result.GetValue('raw2ome_loc')
resolutions = result.GetValue('reslevels')
compression = result.GetValue('comp')
cleanup = result.GetValue('clean')

# define absolute paths for tools
bf2raw = Path.Combine(bf2raw_dir, Path.Combine('bin', 'bioformats2raw'))
raw2ome = Path.Combine(raw2ome_dir, Path.Combine('bin', 'raw2ometiff'))
print(("Path bioformats2raw : ", bf2raw))
print(("Path raw2ometiff : ", raw2ome))
print(("CZI File : ", czifile))
print(("Compression for OME-TIFF : ", compression))
print(("Cleaning up afterwards : ", cleanup))

# check if the tools exists on the speified location
if not File.Exists(bf2raw):
    sys.exit('bioformats2raw tool not found inside folder : ' + bf2raw_dir)
if not File.Exists(raw2ome):
    sys.exit('raw2ometiff tool not found inside folder : ' + raw2ome_dir)

# create the name for the required TMP folder and the output OME-TIFF
tmpfolder = Path.Combine(Path.GetDirectoryName(czifile), Path.GetFileNameWithoutExtension(czifile))
omefile = tmpfolder + '_PY.ome.tiff'
print(('TMP Folder : ', tmpfolder))
print(('OME-TIFF to be created : ', omefile))

# define parameters and run bioformats2raw
bf2raw_params = '"' + czifile + '" ' + '"' + tmpfolder + '"' + ' --resolutions ' + str(resolutions) + ' --compression=raw'
print(('Command String : ', bf2raw_params))
done1 = run_tool(bf2raw, bf2raw_params)
print(('Done with conversion to RAW.', done1))

# # define parameters and run raw2ometiff
raw2ome_params = '"' + tmpfolder + '" ' + '"' + omefile + '"' + ' --compression=' + compression
print(('Command String : ', raw2ome_params))
done2 = run_tool(raw2ome, raw2ome_params)
print(('Done with conversion to pyramidal OME-TIFF', done2))

# delete bfmemo file and TMP folder
if cleanup:
    print('Cleaning up ...')
    delname = Path.Combine(czidir, '.' + cziname + '.bfmemo')
    print(('Deleting : ', delname))
    File.Delete(delname)
    print(('Deleting Folder : ', tmpfolder))
    Directory.Delete(tmpfolder, True)

print('Done.')
