# Macro asks the user to move to each of the positions, saves all positions and revisits each position to perform the active experiment.

NumberOfPositions = 2       # Number of Positions
Delay = 3600                # Delay in seconds between loops
NumberOfLoops = 3

# DO NOT EDIT BELOW THIS LINE!

import time

tt = 0

X = [0] * NumberOfPositions
Y = [0] * NumberOfPositions
Z = [0] * NumberOfPositions

X[0] =  Zen.Devices.Stage.ActualPositionX
Y[0] =  Zen.Devices.Stage.ActualPositionY
Z[0] =  Zen.Devices.Focus.ActualPosition
    
for zz in range(1, NumberOfPositions, 1):

    Zen.Application.Pause("Move to next position!")
    X[zz] =  Zen.Devices.Stage.ActualPositionX
    Y[zz] =  Zen.Devices.Stage.ActualPositionY
    Z[zz] =  Zen.Devices.Focus.ActualPosition

Experiment = Zen.Acquisition.Experiments.ActiveExperiment

# Execute experiment

while tt < NumberOfLoops:

    for zz in range(0, NumberOfPositions, 1):

        # Move stage
        Zen.Devices.Stage.TargetPositionX = X[zz]
        Zen.Devices.Stage.TargetPositionY = Y[zz]
        Zen.Devices.Focus.TargetPosition = Z[zz]
        Zen.Devices.Stage.Apply()
        Zen.Devices.Focus.Apply()
        Zen.Application.Wait(500)

        # Execute experiment (this will open a new tab)
        Img = Zen.Acquisition.Execute(Experiment)
    
        # Close Tab
        #Img.Close()

    tt = tt + 1
    time.sleep(Delay)
        
# Move stage back to starting position
Zen.Devices.Stage.TargetPositionX = X[0]
Zen.Devices.Stage.TargetPositionY = Y[0]
Zen.Devices.Focus.TargetPosition = Z[0]
Zen.Devices.Stage.Apply()
Zen.Devices.Focus.Apply()
