#################################################################
# File       : DramaticZoom.py
# Version    : 1.0
# Author     : Sara McArdle
# Date       : 03.12.2018
# Institution : La Jolla Institute for Immunology, LJI Microscopy Core
#
#
# Macro to create a zoom-in or zoom-out movie
# Draw a region around the area you want to focus on. Any of the solid-line shapes, but not the dotted-line ROI
# A window will pop up asking for some user input, and then it will create a movie from the entire image to the region you selected
# Final output has the aspect ratio of the entire image (or scene, if a multiscene file) and contains the entire drawn ROI.
# The most zoomed-in frame will be at native resolution, all other images are downsampled
#
#################################################################


Zen.Processing.Options.IsImagePyramidEnabled = False  # try not to use pyramids, though this doesn't seem to make a difference
img = Zen.Application.Documents.ActiveDocument
assert (img.Graphics.Count > 0), "Must draw an ROI"

# get user input
window = ZenWindow()
window.Initialize("Zoom Movie Parameters", 500, 200, True, True)
window.AddTextBox('frameNum', 'Enter Number of Frames', '20')  # number of frames in final movie
window.AddDropDown('zoomDir', 'Zoom Direction', ['Zoom Out', 'Zoom In', 'Both'], 0)

if img.Bounds.IsMultiScene:
    window.AddIntegerRange('sceneNum', 'Choose which scene', 1, 1, img.Bounds.SizeS)  # which scene when there are multiple
    window.Height = window.Height+100
if img.Bounds.IsTimeLapse:
    window.AddIntegerRange('timeNum', 'Choose which timepoint', 1, 1, img.Bounds.SizeT)  # which timepoint when there are multple
    window.Height = window.Height+100
if img.Graphics.Count > 1:
    window.AddIntegerRange('roiNum', 'Choose which Region', 1, 1, img.Graphics.Count)  # which roi when there are multiple
    window.Height = window.Height+100
result = window.Show()

steps = int(result.GetValue('frameNum')) - 1
assert (steps > 1), "Must choose more than 1 frame"

zoomDir = result.GetValue('zoomDir')
if img.Bounds.IsMultiScene:
    sceneNum = result.GetValue('sceneNum')
    img = img.CreateSubImage('S({})'.format(sceneNum))
if img.Bounds.IsTimeLapse:
    timeNum = result.GetValue('timeNum')
    img = img.CreateSubImage('T({})'.format(timeNum))
if img.Graphics.Count > 1:
    roiNum = str(result.GetValue('roiNum'))
else:
    roiNum = "1"

# get size and aspect ratio of full image
sizeX = img.Bounds.SizeX
sizeY = img.Bounds.SizeY
imgAspect = float(sizeX)/float(sizeY)

# get boundaries of selected region
roi1 = img.Graphics.GetById(roiNum)
[left, top, width, height] = roi1.GetBounds()
boxAspect = width/height

# decide if ROI width or height is limiting, then calculate new region that has the same aspect ratio as the original image
if (imgAspect > boxAspect):
    zoomHeight = height
    zoomWidth = height*imgAspect
    zoomShift = int((zoomWidth-width)/2)
    box = [round(left-zoomShift), round(top), round(zoomWidth), round(zoomHeight)]
    if (box[0] < 0):
        box[0] = 0
    if (box[0] + box[2]) > sizeX:
        box[0] = sizeX - box[2]
    # calculate how much each step must grow (exponential growth in zoom)
    expansion = img.Bounds.SizeY/height
    expSteps = expansion**(1/float(steps))


else:
    zoomWidth = width
    zoomHeight = width/imgAspect
    zoomShift = int((zoomHeight - height)/2)
    box = [round(left), round(top-zoomShift), round(zoomWidth), round(zoomHeight)]
    if (box[1] < 0):
        box[1] = 0
    if (box[1] + box[3]) > sizeY:
        box[1] = sizeY - box[3]
    expansion = img.Bounds.SizeX/width
    expSteps = expansion**(1/float(steps))

    # calculate image for each frame
for step in range(steps+1):
    if step < 1:  # frame 1
        # use the just-calculated box
        boxstr = "X(%i-%i)|Y(%i-%i)" % (box[0], box[0]+box[2], box[1], box[1]+box[3])
        imageMov = Zen.Processing.Utilities.CreateSubset(img, boxstr, False, False)

    elif step < steps:  # for middle frames
       # expand the previous box by expSteps
        newWidth = round((expSteps) * box[2])
        newLeft = round(box[0] - (newWidth - box[2])/2)
        # do not let it go past the image boundaries
        if (newLeft < 0):
            newLeft = 0
        elif (newLeft + newWidth) > sizeX:
            newLeft = sizeX - newWidth
        newHeight = round((expSteps)*box[3])
        newTop = round(box[1]-(newHeight-box[3])/2)
        if (newTop < 0):
            newTop = 0
        elif (newTop+newHeight) > sizeY:
            newTop = sizeY-newHeight
        box = [round(newLeft), round(newTop), round(newWidth), round(newHeight)]
        boxstr = "X(%i-%i)|Y(%i-%i)" % (box[0], box[0]+box[2], box[1], box[1] + box[3])

        # create an image with the new region
        image2 = Zen.Processing.Utilities.CreateSubset(img, boxstr, False, False)
        # down sample so that is has the same number of pixels as frame 1
        image3 = Zen.Processing.Transformation.Geometric.Resample(image2, True, ZenInterpolation.Linear, ZenThirdProcessingDimension.None, 0, 0, 0, expSteps**(-1*step), expSteps**(-1*step), 1, False)
        imageMov = Zen.Processing.TimeSeries.TimeConcat(imageMov, image3, False)

    else:  # for the last image, do not create a new subset, just downsample
        image3 = Zen.Processing.Transformation.Geometric.Resample(img, True, ZenInterpolation.Linear, ZenThirdProcessingDimension.None, 0, 0, 0, expSteps**(-1*steps), expSteps**(-1*steps), 1, False)
        imageMov = Zen.Processing.TimeSeries.TimeConcat(imageMov, image3, False)

if zoomDir == 'Zoom Out':
    Zen.Application.Documents.Add(imageMov)
    imageMov.Graphics.Clear()
elif zoomDir == 'Zoom In':  # to zoom from large to small, reverse order of movie
    for movFrame in reversed(list(range(steps+1))):
        frameStr = 'T({})'.format(str(movFrame+1))
        tFrame = Zen.Processing.Utilities.CreateSubset(imageMov, frameStr, False, False)
        if movFrame == steps:
            mirrorMov = tFrame
        else:
            mirrorMov = Zen.Processing.TimeSeries.TimeConcat(mirrorMov, tFrame, False)
    Zen.Application.Documents.Add(mirrorMov)
    mirrorMov.Graphics.Clear()
else:
    Zen.Application.Documents.Add(imageMov)
    for movFrame in reversed(list(range(steps + 1))):
        frameStr = 'T({})'.format(str(movFrame + 1))
        tFrame = Zen.Processing.Utilities.CreateSubset(imageMov, frameStr, False, False)
        if movFrame == steps:
            mirrorMov = tFrame
        else:
            mirrorMov = Zen.Processing.TimeSeries.TimeConcat(mirrorMov, tFrame, False)
    Zen.Application.Documents.Add(mirrorMov)
    mirrorMov.Graphics.Clear()
    imageMov.Graphics.Clear()
