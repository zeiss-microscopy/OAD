# Experiment will start at the current stage position.
# With every iteration the actual position will be increased by StageStepSize
# At every position the defined experiement will be performed.
# Experiment needs to be a plain time series without zStack or Tiles
# After StageNumberOfSteps iterations the experiment will be finished and Stage
# stage will be moved to the start position
# keep ROI as small as posible, because copying data is super slow in OAD

StageStepSize = 1           # Stepsize in um
StageNumberOfSteps = 10     # Number of Positions

Experiment = Zen.Acquisition.Experiments.ActiveExperiment
StageStartPosition = Zen.Devices.Stage.ActualPositionY

# Execute first experiment
FinalImage = Zen.Acquisition.Execute(Experiment)

for zz in range(1,StageNumberOfSteps,1):

    # Calculate next stage position
    StagePosition = StageStartPosition + zz * StageStepSize
    print StagePosition
    
    # Move stage
    Zen.Devices.Stage.TargetPositionY = StagePosition
    Zen.Devices.Stage.Apply()
    Zen.Application.Wait(500)

    # Execute experiment (this will open a new tab)
    Img = Zen.Acquisition.Execute(Experiment)

    # Copy all acquired images to FinalImage
    FinalImage = Zen.Processing.TimeSeries.TimeConcat(FinalImage, Img)
    
    # Close Tab
    Img.Close()
    

# Move stage back to starting position
Zen.Devices.Stage.TargetPositionY = StageStartPosition

# Open tab and display FinalImage
Zen.Application.Documents.Add(FinalImage)
