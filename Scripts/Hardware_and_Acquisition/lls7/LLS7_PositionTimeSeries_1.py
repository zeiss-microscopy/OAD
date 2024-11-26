# Experiment will start at the current stage position.
# With every iteration the actual position will be increased by StageStepSize
# At every position the defined experiement will be performed.
# Experiment needs to be a plain time series without zStack or Tiles
# After StageNumberOfSteps iterations the experiment will be finished and Stage
# stage will be moved to the start position
# keep ROI as small as posible, because copying data is super slow in OAD


StageStepSize = 1           # Stepsize in um
StageNumberOfSteps = 3     # Number of Positions

Experiment = Zen.Acquisition.Experiments.ActiveExperiment
StageStartPosition = Zen.Devices.Stage.ActualPositionY

# Execute first experiment to get image size
# this will open a new tab
Img = Zen.Acquisition.Execute(Experiment)

# Create Final Image. All subsets will be copied in this image
# Get image dimensions
ImgSizeX = Img.Bounds.SizeX
ImgSizeY = Img.Bounds.SizeY
ImgTimePoints = Img.Bounds.SizeT
ImgPixelType = Img.Metadata.PixelType
ImgChannels = Img.Bounds.SizeC
ImgZSlices = StageNumberOfSteps
# Create FinalImage
FinalImage = ZenImage(ImgSizeX, ImgSizeY, ImgPixelType, ImgZSlices, ImgTimePoints, ImgChannels)

# Copy images of first experiment to final image
FinalImage.AddSubset(Img, Img.Bounds)

#Setup boundbox string (this will be used later to copy images to FinalImage)
startX=Img.Bounds.StartX+1
endX=startX + Img.Bounds.SizeX-1
startY=Img.Bounds.StartY+1
endY=startY + Img.Bounds.SizeY-1
startT=Img.Bounds.StartT+1
endT=startY + Img.Bounds.SizeT-1
strBoundBox = 'X(' + str(int(startX)) + '-' + str(int(endX)) + ')|Y(' + str(int(startY)) + '-' + str(int(endY)) + ')'

# Close Img (this will also close tab)
Img.Close()

for zz in range(1,StageNumberOfSteps,1):

    # Calculate next stage position
    StagePosition = StageStartPosition + zz * StageStepSize
    print(StagePosition)
    
    # Move stage
    Zen.Devices.Stage.TargetPositionY = StagePosition
    Zen.Devices.Stage.Apply()
    Zen.Application.Wait(500)

    # Execute experiment (this will open a new tab)
    Img = Zen.Acquisition.Execute(Experiment)

    # Copy all acquired images to FinalImage
    for c in range(Img.Bounds.SizeC):
        for t in range(Img.Bounds.SizeT):
            timepointString= strBoundBox+"|C("+ str(c+1) + ")"+"|T("+ str(t+1) + ")"
            sub = Img.CreateSubImage(timepointString)
            FinalImage.AddSubImage(sub,t,c,zz)
    
    # Close Tab
    Img.Close()
    

# Move stage back to starting position
Zen.Devices.Stage.TargetPositionY = StageStartPosition

# Open tab and display FinalImage
Zen.Application.Documents.Add(FinalImage)
