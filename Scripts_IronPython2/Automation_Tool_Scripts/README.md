## Automation Tool Scripts

### Apotome Export

* The script will export the active Apotome image after it was converted

***
### Apotome Processing

* This script will automatically process the acquired ApoTome raw image, show the result and at the same time save the result in C:\ZEN_Output.
* To change the saving folder, open the script and adjust line 5.
* To adjust some settings (though these are most general), adjust line 14.

***
### Deconvolution

This script will automatically deconvolve a z-stack with the Fast Iterative Lucy-Richardson algorithm (100 iterations). The result will be saved in C:\ZEN_Output.

* To make adjustments chnage the desired output folder (always use double "\" to indicate subfolder and DCV settings to be used inside the script
* To change these, open an image, go to Deconvolution parameters, make changes and save in a new czips-file (save in Parameters window). E.g. this script uses "Lucy_Richardson_DCV.czips".

This file is stored in (change USERNAME to Windows login name):

**C:\\Users\USERNAME\\Documents\\Carl Zeiss\\ZEN\\Documents\\Processing Settings\\DeconvolutionApplication**

***
### Focussing

The script will do the following steps:

1. Run a FindSurface using the Definite Focus
2. Run a SWAF using the current active experiment using the parameters defined inside the scrit
3. Store the resulting Z-Psoition inside the Definite Focus to be able to use RecallFocus

***
### Image Analysis

1. Copy "Analysis_Count_Cells_Active_Image.czmac" into "C:\Users\Public\Documents\Carl Zeiss\ZEN\Documents\Macros"
2. Copy "Count_Cells.czias" into "C:\Users\Public\Documents\Carl Zeiss\ZEN\Documents\Image Analysis Settings"
* Data is saved in a folder on "C:\ZEN_Output". Before running the script, create the folder and/or rename its location in the macro (line 7).
* The script works on any single or multi-channel image as long as the first channel is the DAPI channel. Feel free to create your own script and rename the file & location in the macro accordingly (line 9).
* In ZEN Blue Pro/System, enable Automation, open this script in "After Acquisition". Once image acquisition is finished, it will run automatically and analyze the recently acquired image.

***
### Stitching

This script will automatically  tiled image based on the first channel as reference.
To make adjustments:

* To change these, open an image, go to Stitching parameters, make changes and save in a new czips-file (save in Parameters window). E.g. this script uses "Stitching_Channel_1'.czips".

This file is stored in (change USERNAME to Windows login name):

**C:\Users\USERNAME\Documents\Carl Zeiss\ZEN\Documents\Processing Settings\Stitching**

***
### Multiblock TimeStitching

This script automatically performs Time-stitching of Multi-block images acquired withbthe experiment designer. 
