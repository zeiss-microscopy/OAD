#################################################################
# File       : Extract_Polygons.py
# Version    : 1.0
# Author     : czchs, czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from System.IO import File, Directory, FileInfo, Path
"""  
- Load image, extract scene and draw contours of ROIs
- save ROIs as separate images
"""

# clear output
Zen.Application.MacroEditor.ClearMessages()

# activate IO library

# get image folder
images = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.Images)

# create setup dialog
window = ZenWindow()
window.AddFolderBrowser('sourcefolder', 'Source Folder with Images', images)
window.AddDropDown('isval', 'Input Image Type', ['*.czi', '*.zvi', '.lsm', '*.jpeg', '.jpg', '*.png', '*.tiff', '*.tif'], 0)
window.AddFolderBrowser('destfolder', 'Destination Folder', images)
window.AddDropDown('osval', 'Output Image type', ['.czi', '.jpeg', '.ome.tiff', '.png', '.tiff'], 0)

# get and check results result=window.Show()

# check, if Cancel button was clicked
if result.HasCanceled:
    sys.exit('Macro aborted with Cancel!')

# get string name of source folder/destination folder
path = str(result.GetValue('sourcefolder'))
newPath = str(result.GetValue('destfolder'))

# Check, if path exists
if not Directory.Exists(path):
    strMessage = 'Path: ' + path + ' does not exist!\nRestart macro and select an existing path!'
    sys.exit(strMessage)

# Check, if newPath exists
if not Directory.Exists(newPath):
    strMessage = 'Path: ' + newPath + ' does not exist!\nRestart macro and select an existing path!'
    sys.exit(strMessage)

# get file type
itype = str(result.GetValue('isval'))
otype = str(result.GetValue('osval'))
files = Directory.GetFiles(path, itype)

# Check, if image type exists
if files.Length == 0:
    strMessage = 'Images of type : ' + itype + ' do not exist!\nRestart macro and select an existing image type!'
    sys.exit(strMessage)

# start loop over all images
saved = True

for slide in range(0, files.Length):

    try:
        file = files[slide]
        fileInfo = FileInfo(file)
        PathAndFile = Path.Combine(path, fileInfo.Name)

        # Load an image automatically
        image = Zen.Application.LoadImage(PathAndFile, False)
        Zen.Application.Documents.Add(image)

        # Extract file name without extension
        OrgFileNameWE = Path.GetFileNameWithoutExtension(image.Name)

        # Extract dimensions
        z = image.Bounds.SizeZ
        t = image.Bounds.SizeT
        c = image.Bounds.SizeC
        s = image.Bounds.SizeS

        # start loop over all scenes
        for scene in range(0, s):
            # Separate and show scene
            if s > 1:
                sc = "S(" + str(scene + 1) + ")"
                sceneImage = Zen.Processing.Utilities.CreateSubset(image, sc)
                Zen.Application.Documents.Add(sceneImage)
            else:
                sceneImage = image
            # Extract scene name
            SceneName = OrgFileNameWE + '-Scene-' + str(scene + 1)
            sceneImage.Name = SceneName

            # Draw ROI contours
            Zen.Application.Pause(
                'Switch to Graphics view!\nSelect Keep tool (only for several ROIs)!\nSelect contour tool and draw ROI contours!\nThen press Continue!')

            # Extract and save ROIs
            for i in range(0, sceneImage.Graphics.Count):

                # Switch of measurement values
                graphic = sceneImage.Graphics[i]
                graphic.IsMeasurementVisible = False

                # Get coordinates of bounding box
                XS = graphic.Bounds.Left - 10
                YS = graphic.Bounds.Top - 10
                XE = graphic.Bounds.Right + 10
                YE = graphic.Bounds.Bottom + 10

                # Create bounding box image of ROI
                strBoundBox = 'X(' + str(int(XS)) + '-' + str(int(XE)) + ')|Y(' + str(int(YS)) + '-' + str(int(YE)) + ')'
                boundbox = Zen.Processing.Utilities.CreateSubset(sceneImage, strBoundBox)
                # Zen.Application.Documents.Add(boundbox)

                # Create mask image
                height = boundbox.Metadata.Height
                width = boundbox.Metadata.Width
                binmask = ZenImage(int(width), int(height), ZenPixelType.Gray8, z, t, c)
                binmask.Graphics.Merge(boundbox.Graphics.Clone())
                copycontour = binmask.Graphics[0]
                copycontour.IsMeasurementVisible = False

                # Zen.Application.Documents.Add(binmask)
                AnnoImage = binmask.BurnInGraphics()
                # Zen.Application.Documents.Add(AnnoImage)
                fill = Zen.Processing.Binary.FillHoles(AnnoImage)
                # Zen.Application.Documents.Add(fill)

                # Mask ROI image
                roi = Zen.Processing.Binary.And(boundbox, fill)
                contour = roi.Graphics[i]
                roi.Graphics.Clear()

                # Create ROI image name
                newFileName = SceneName + '_roi' + str(i + 1)
                newPathAndFile = Path.Combine(newPath, newFileName + otype)
                roi.Name = newFileName
                # Zen.Application.Documents.Add(roi)

                # Save ROI image
                Zen.Application.Save(roi, newPathAndFile)

                # Close ROI image (otherwise it cannot be deleted in explorer)
                roi.Close()

            # Close scene image (otherwise it cannot be deleted in explorer)
            sceneImage.Close()

        # Close image (otherwise it cannot be deleted in explorer)
        image.Close()

    # Give message, if files are corrupted
    except:
        print('Fatal error in: ' + PathAndFile)
        saved = False

# Show message
if saved:
    strMessage = 'ROI images are saved in: ' + newPath
    Zen.Application.Pause(strMessage)
