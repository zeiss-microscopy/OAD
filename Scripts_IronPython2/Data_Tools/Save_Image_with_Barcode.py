#################################################################
# File       : SaveImage_with_Barcode.py
# Version    : 0.1
# Author     : czsrh
# Date       : 21.08.2019
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# clear output console
Zen.Application.MacroEditor.ClearMessages()

version = 0.1

# set to true when reloading the image (after renaming) is desired
reload = True

from System.IO import Directory, Path, File, FileInfo, DirectoryInfo


def ReadBarCodefromImage(image):

    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    # use the correct path to read the barcode from the image
    barcode_complete = image.Metadata.GetMetadataWithPath('Metadata/AttachmentInfos[]/Label/Barcodes[]/Content')
    if len(barcode_complete) == 0:
        print 'No barcode was found.'
        barcode = None
        barcodeinfo = None
        barcode_found = False

    if len(barcode_complete) > 0:
        indexlist = find(barcode_complete, ':')
        barcode = barcode_complete[max(indexlist)+1:]
        barcodeinfo = barcode_complete[:max(indexlist)]
        barcode_found = True
        # remove leading whitespace from barcode
        barcode = barcode[1:]

    return barcode, barcodeinfo, barcode_found

# get the active image document
activeimage = Zen.Application.Documents.ActiveDocument

# read the barcode from the image
barcode, barcodeinfo, found = ReadBarCodefromImage(activeimage)
print 'Found Barcode : ', found
print 'Barcode       : ', barcode
print 'Barcode Info  : ', barcodeinfo

if found:
    # save with new name
    filename = activeimage.FileName
    newname = Path.Combine(Path.GetDirectoryName(filename), Path.GetFileNameWithoutExtension(filename) + '_' + barcode + '.czi')
    print 'Save with new name : ', newname
    activeimage.Save(newname)
    activeimage.Close()
    
    if reload:
        reload_image = Zen.Application.LoadImage(newname, False)
        Zen.Application.Documents.Add(reload_image)
    
print 'Done.'
