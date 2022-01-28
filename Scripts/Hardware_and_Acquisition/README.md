# Hardware and Acquisition

## FindSurface_SWAF_ActiveExp.py

This script is intended to be placed as a action button inside the ZEN menu bar especially when using a Celldiscoverer 7 system. The idea here is to combine the hard-based focus with the software focus to store the final z-value (where something should be in focus) inside the hardware focus in order to be able to relocate to that value (relative to the sample carrier surface) easily without bleaching.

The script does the following things:

* run **FindSurface** to move to the surface of the sample carrier, which is not in all cases exactly the focal plane the user wants to see

* execute a **Software Autofocus** (SWAF) based on the resulting z-position from **FindSurface**.

* The result of the **SWAF** will be stored as an offset inside the DF.2 and be recalled anytime via **RecallFocus**

## Smart_Dynamics.py

ZEN Blue offers the possibility to measure the intensity ratio etc. of objects during a running acquisition. Typically the ROIs (where the intensities will be measured) will be created manually.

For some applications or workflows in can be very beneficial to let an Image Analysis setting create those ROIs automatically be segmenting the objects before the start of the experiment.

<p><img src="./images/smart_dynamics1.png" title="Smart Dynamics - User Interface" width="600"></p>

The user has to define the following parameters:

* ZEN Experiment wit Dynamics activated (no positions or tiles)
* Option to run a FindSurface using the DF.2 (if available) to find the sample surface
* Option to run a software autofocus before the actual experiment starts
* the Image Analysis setting (*.czias) to segment the actual cells or objects
  * classical threshold as well as machine-learning based segmentation (PixelClassifier or Deep Neural Networks) can be used
* level of accuracy for the creation of the polygons to outline objects
* folder to save the results including the data tables from the image analysis

<p><img src="./images/smart_dynamics2.png" title="Smart Dynamics - Result in ZEN Blue" width="1200"></p>


## LLS7_ZStacksOfYstacks.py

The [ZStacksOfYStack](./LLS7_ZStacksOfYStacks_v1.2.py) macro is specifically designed for Lattice Lightsheet 7 and enables the user to record multiple volumes stacked on top of each other. This allows for recording larger volumes and imaging deeper into the sample as the focus position of the lightsheet can be adjusted with imaging depth. The macro asks the user to move close to the coverslip and focus the lightsheet, then to move to the deepest position of the sample that they want to image and focus the lightsheet there. The macro will then record the defined volume by stacking multiple volume scans and adjusting the lightsheet with depth using linear interpolation of the values set by the user.

### Versions and Changes

* v1.1 adds capabilities to do more than 9 volume stacks without loosing the correct order of stacks (max 20 stacks)
* v1.1 adds capabilities to change 'Focus Sheet' with imaging depths, the user can set 'Focus Sheet' close to the cover slip and at the deepest position in the sample, that they want to image and the macro will do a linear interpolation and modify 'Focus Sheet' automatically wih imaging depth
* v1.2 asks the user to move to and focus @ coverslip and @ depth and automatically reads z positions and Focus Sheet values from those positions
* v1.2 reads Scanner Offset y value from calibration files, user just has to select the active MTB, which should be selected correctly automatically based on it being the last modified MTB
* v1.2 automatically calculates the number of stacks required from camera ROI, overlap and distance between coverslip and depth positions specified by the user
* v1.2 takes the active experiment setup (and potential unsaved changes) rather than letting the user choose from existing experiment setups in a dropdown menu

<p><img src="./images/lls7_ytile.png" title="LLS7 - YStackTiling" width="600"></p>

## Disclaimer

:warning: **This tutorial and the related scripts are free to use for everybody. Use it on your own risk. Especially be aware of the fact that automated stage movements might damage hardware if the system is not setup properly. Please check everything in simulation mode first!**

Carl Zeiss Microscopy GmbH's ZEN software allows connection to the third party software, Python. Therefore Carl Zeiss Microscopy GmbH undertakes no warranty concerning Python, makes no representation that Python will work on your hardware, and will not be liable for any damages caused by the use of this extension. By running this example you agree to this disclaimer.
