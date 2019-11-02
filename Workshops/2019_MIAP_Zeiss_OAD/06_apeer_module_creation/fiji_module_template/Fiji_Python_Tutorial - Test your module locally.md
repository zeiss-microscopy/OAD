# Tutorial: Using ImageJ/Fiji scripts in APEER modules - Test your module locally

This tutorial describe how to create an APEER module based on an existing ImageJ / Fiji python script or how to easily adapt such a script for APEER.

**To follow this tutorial basic python scripting knowledge is required.**

## Goal of the tutorial

Test your newly created module locally.

## Introduction

This tutorial is based on the

### ImageJ/Fiji - Headless Mode 

Before one can start coding it is important to understand a few basic things about scripting in Fiji. In order to be able to create an APEER module using Fiji one needs:

* a docker container with the latest version of Fiji inside
* a python script that can run in headless mode, since APEER modules do not allow for any dynamically generated UI elements
* typically such a script is using *script parameters* to define its inputs and when used directly from Fiji those will even automatically create an user interface
* when running such a script in headless mode one has to pass those script parameters as commandline arguments or ...
* ... in case of creating an APEER module, those parameters will be provided by the APEER module user interface

More information and additional examples can be found here:

* [image.sc Forum](https://forum.image.sc/)
* [Python + ImageJ and Fiji Cookbook](http://wiki.cmci.info/documents/120206pyip_cooking/python_imagej_cookbook)
* [ImageJ - Jython Scripting](https://imagej.net/Jython_Scripting)
* [Fiji Scripting Tutorial](https://www.ini.uzh.ch/~acardona/fiji-tutorial/)
* [ImageJ - Scripting](https://imagej.net/Scripting)
* [ImageJ - Jython Scripting Examples](https://imagej.net/Jython_Scripting_Examples)
* [ImageJ - Headless](https://imagej.net/Headless)
* [ImageJ - Scripting Headless](https://imagej.net/Scripting_Headless)
* [ImageJ - Script Parameters](https://imagej.net/Script_Parameters)


#### Script Parameters

Below you see a typical definition of those scripting parameters inside a Fiji python script. In this case the required inputs are:

* *FILENAME* - allows to select the input file
* *FILTERTYPE* - defines the filter type via a dropdown list
* *FILTER_RADIUS* - defines the desired kernel size via a numeric control
* *HEADLESS* - option to disable some part of the scripts when using it locally in headless mode

When running this script from your Fiji script editor one will see the following UI:

```python
# @File(label = "Image File", persist=True) FILENAME
# @String(label = "Select Filter", choices={"NONE", "MEDIAN", "MIN", "MAX", "MEAN", "VARIANCE", "OPEN", "DESPECKLE"}, style="listBox", value="MEDIAN", persist=True) FILTERTYPE
# @Integer(label = "Filter Radius", value=5.0, persist=False) FILTER_RADIUS
# @Boolean(label = "Run in headless mode", value=False, persist=False) HEADLESS
# @OUTPUT String FILENAME
# @OUTPUT String FILTERTYPE
# @OUTPUT Integer FILTER_RADIUS
# @OUTPUT Boolean HEADLESS
```

![Fiji Script Parameters - User Interface](/images/Fiji_Scriptparameter_UI.png)

#### Complete Example Script - Local Fiji version

We will now use this python script example as a template for creating an APEER module out of it. The core functions of this script are quite simple:

* Read the image using the BioFormats pluging
* Apply a filter to that image using the specifed radius
* Save the resulting image as OME-TIFF using BioFormats
* Create some logs to provide some information about what is happening 

```python
# @File(label = "Image File", persist=True) FILENAME
# @String(label = "Select Filter", choices={"NONE", "MEDIAN", "MIN", "MAX", "MEAN", "VARIANCE", "OPEN", "DESPECKLE"}, style="listBox", value="MEDIAN", persist=True) FILTERTYPE
# @Integer(label = "Filter Radius", value=5.0, persist=False) FILTER_RADIUS
# @Boolean(label = "Run in headless mode", value=False, persist=False) HEADLESS
# @OUTPUT String FILENAME
# @OUTPUT String FILTERTYPE
# @OUTPUT Integer FILTER_RADIUS
# @OUTPUT Boolean HEADLESS

#@UIService uiService
#@LogService log

"""
File: my_fijipyscript.py
Author: sebi06
Date: 2019_05_21
Version: 0.2

The idea of this module is to provide a template showing some of the required
code parts in order to create modules based on Fiji. The choosen processing step
is just an example for your image analysis pipeline

Disclaimer: Use at your own risk!

"""

# required imports
import os
import json
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
import time

# helper function to apply the filetr
def getImageStack(imp):

    # get the stacks
    try:
        stack = imp.getStack()  # get the stack within the ImagePlus
        nslices = stack.getSize()  # get the number of slices
    except:
        stack = imp.getProcessor()
        nslices = 1

    return stack, nslices


def apply_filter(imp,
                 radius=5,
                 filtertype='MEDIAN'):

    # initialize filter
    filter = RankFilters()

    # create filter dictionary
    filterdict = {}
    filterdict['MEAN'] = RankFilters.MEAN
    filterdict['MIN'] = RankFilters.MIN
    filterdict['MAX'] = RankFilters.MAX
    filterdict['MEDIAN'] = RankFilters.MEDIAN
    filterdict['VARIANCE'] = RankFilters.VARIANCE
    filterdict['OPEN'] = RankFilters.OPEN
    filterdict['DESPECKLE'] = RankFilters.DESPECKLE

    # get the stack and number of slices
    stack, nslices = getImageStack(imp)

    for index in range(1, nslices + 1):
        # get the image processor
        ip = stack.getProcessor(index)
        # apply filter based on filtertype
        filter.rank(ip, radius, filterdict[filtertype])

    return imp

############################################################################

if not HEADLESS:
    # clear the console automatically when not in headless mode
    uiService.getDefaultUI().getConsolePane().clear()


def run(imagefile, useBF=True, series=0):

    log.info('Image Filename : ' + imagefile)

    if not useBF:
        # using IJ static method
        imp = IJ.openImage(imagefile)

    if useBF:

        # initialize the importer options
        options = ImporterOptions()
        options.setOpenAllSeries(True)
        options.setShowOMEXML(False)
        options.setConcatenate(True)
        options.setAutoscale(True)
        options.setId(imagefile)

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if FILTERTYPE != 'NONE':

        # apply filter
        log.info('Apply Filter  : ' + FILTERTYPE)
        log.info('Filter Radius : ' + str(FILTER_RADIUS))

        # apply the filter based on the choosen type
        imp = apply_filter(imp,
                           radius=FILTER_RADIUS,
                           filtertype=FILTERTYPE)

    if FILTERTYPE == 'NONE':
        log.info('No filter selected. Do nothing.')

    return imp


#########################################################################

# convert the filename into a string
IMAGEPATH = FILENAME.toString()

# suffix for the filename of the saved data
SUFFIX_FL = '_FILTERED'
SAVEFORMAT = 'ome.tiff'

log.info('Starting ...')
log.info('Filename               : ' + IMAGEPATH)
log.info('Save Format used       : ' + SAVEFORMAT)
log.info('------------  START IMAGE ANALYSIS ------------')

##############################################################

# define path for the output
outputimagepath = '/output/' + os.path.basename(IMAGEPATH)
basename = os.path.splitext(outputimagepath)[0]

# remove the extra .ome before reassembling the filename
if basename[-4:] == '.ome':
    basename = basename[:-4]
    log.info('New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT

#############   RUN MAIN IMAGE ANALYSIS PIPELINE ##########

# get the starting time of processing pipeline
start = time.clock()

# run image analysis pipeline
filtered_image = run(IMAGEPATH,
                     useBF=True,
                     series=0)

# get time at the end and calc duration of processing
end = time.clock()
log.info('Duration of whole Processing : ' + str(end - start))

###########################################################

start = time.clock()

# create the argument string for the BioFormats Exporter and save as OME.TIFF
paramstring = "outfile=" + outputimagepath + " " + "windowless=true compression=Uncompressed saveROI=false"
plugin = LociExporter()
plugin.arg = paramstring
exporter = Exporter(plugin, filtered_image)
exporter.run()

# get time at the end and calc duration of processing
end = time.clock()
log.info('Duration of saving as OME-TIFF : ' + str(end - start))

# show the image
filtered_image.show()

# finish
log.info('Done.')
```


### Structure and files

Below you see an overview of the files we will generate for this tutorial.
All these files except the Dockerfile and the json will be utilitzed within the Docker Container.

```shell
├── Dockerfile                  (the file neccessary to generate the Docker container)
├── module_specification.json   (module input/output and GUI specification for the WFE)
├── my_fijipyscript.py          (the actual Fiji script)
├── start.sh                    (shell script to run Fiji script from the command line)
└── wfe.env                     (file for defining environment variables for local test runs)
```

### Prerequites - How to create a Docker Container with Fiji inside

In order to create APEER modules based on Fiji it is useful to create an docker container with Fiji first which will be referenced later when creating the actual module. One can find it here:

[Team APEER - Fiji Docker Container](https://hub.docker.com/r/czsip/fiji_linux64_baseimage)

To keep things simple team APEER already created such a container, so one can skip that part, but for those who are interested in how to create such an container the required steps are described below.

* Download latest Fiji for Linux and unpack it.
* There should be a folder called Fiji.app inside the same folder as the dockefile.
* Add extra script(s) one might want to use like *fijipytools* below (optional)
* Make sure docker is running and open a terminal.

```bash
docker login
user:yourusername
pwd:yourpwd
```
The dockerfile for updating and creating Fiji docker container looks like this:

```docker
# Pull ubuntu
FROM ubuntu:latest

COPY ./Fiji.app /Fiji.app

# copy Fiji and other scripts or files
COPY ./fijipytools.py /Fiji.app/scripts

# activate or deactivate Fiji-Update sites as needed (just a few examples)
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BAR http://sites.imagej.net/Tiago/
#RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BASIC http://sites.imagej.net/BaSiC/
#RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BioVoxxel http://sites.imagej.net/BioVoxxel/
#RUN ./Fiji.app/ImageJ-linux64 --update add-update-site CMP-BIAtools http://sites.imagej.net/CMP-BIA/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site IJPB-plugins http://sites.imagej.net/IJPB-plugins/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site ImageScience http://sites.imagej.net/ImageScience/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site IMCFUniBasel http://sites.imagej.net/UniBas-IMCF/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site PTBIOP http://biop.epfl.ch/Fiji-Update
RUN ./Fiji.app/ImageJ-linux64 --ij2 --headless --update update
RUN ./Fiji.app/ImageJ-linux64 --ij2 --headless
```

When the login was sucessfull start the build and push the new container.

```bash
docker build -t xyz/fiji_linux64_baseimage:tag .

docker push xyz/fiji_linux64_baseimage:tag
```

That's it. Now this container can be used later when creating the actual module


### Module Creation: Step-by-Step

There is no specific order in which the files from above have to be created, so feel free to start with the file you prefer.

#### Module Specifications

The module specification are the same as you have seen in previous tutorials (See [Module Specification Tutorial](https://docs.apeer.com/Producer/module_specification/ "Module Specification Tutorial"))

In brief you need to supply a JSON file that specifies your inputs, outputs and if neccessary how the UI for the module looks like in case the user can interact with the module. In our case this specification file looks like this:


```json
{
    "spec": {
        "inputs": {
            "IMAGEPATH": {
                "type:file": {
                    "format": [
                        "czi",
                        "tiff",
                        "png",
                        "jpeg",
                        "ome-tiff"
                    ]
                }
            },
            "FILTERTYPE": {
                "type:choice_single": [
                    "NONE",
                    "MEAN",
                    "MIN",
                    "MAX",
                    "MEDIAN",
                    "VARIANCE",
                    "OPEN",
                    "DESPECKLE"
                ],
                "default": "MEDIAN"
            },
            "FILTER_RADIUS": {
                "type:integer": {
                    "min": 1,
                    "max": 20
                },
                "default": 5
            }
        },
        "outputs": {
            "FILTERED_IMAGE": {
                "type:file": {
                    "format": [
                        "ome-tiff"
                    ]
                }
            }
        }
    },
    "ui": {
        "inputs": {
            "IMAGEPATH": {
                "label": "Input Image",
                "index": 1,
                "widget:none": null,
                "description": "Choose the image to be processed"
            },
            "FILTERTYPE": {
                "label": "Filter Method",
                "index": 2,
                "widget:dropdown": {
                    "items": [
                        {
                            "key": "NONE",
                            "label": "NONE"
                        },
                        {
                            "key": "MEAN",
                            "label": "MEAN"
                        },
                        {
                            "key": "MIN",
                            "label": "MIN"
                        },
                        {
                            "key": "MAX",
                            "label": "MAX"
                        },
                        {
                            "key": "MEDIA",
                            "label": "MEDIAN"
                        },
                        {
                            "key": "VARIANCE",
                            "label": "VARIANCE"
                        },
                        {
                            "key": "OPEN",
                            "label": "OPEN"
                        },
                        {
                            "key": "DESPECKLE",
                            "label": "DESPECKLE"
                        }
                    ]
                },
                "description": "Choose filter method"
            },
            "FILTER_RADIUS": {
                "label": "Kernel Size",
                "index": 3,
                "widget:slider": {
                    "step": 1
                },
                "description": "Choose kernel size for filter"
            }
        },
        "outputs": {
            "FILTERED_IMAGE": {
                "label": "Filtered image",
                "index": 1,
                "description": "Filtered Image as OME-TIFF"
            }
        }
    }
}
```

On the APEER platform the UI rendered based on this JSON file would look like this:


![APEER - Module UI based on JSON file](/images/apeer_module_UI.png)

#### Shell script for the Docker Entrypoint

As discussed above when a container is executed it will run the command supplied by the *ENTRYPOINT* parameters.
On our example we execute a shell script that contains the following command below. In essence we start ImageJ with the argument to run our python script

Make sure that the variable `SCRIPT` inside the bash script is specified correctly.

```shell
#!/bin/sh
SCRIPT=/Fiji.app/scripts/my_fijipyscript.py

/Fiji.app/ImageJ-linux64 --ij2 --headless --console --run $SCRIPT
```

#### Defining the WFE file for local testing (optional)

With a working local Docker installation you can build and run the container we prepared during the tutorial locally on your machine. Below are some suggestions assuming a Windows operating system.

First you should create some testing folder for convenience we basis this directly on C:\ and create:

* C:\Temp\input\
* C:\Temp\output\

Place the test image inside the input folder, e.g. C:\Temp\input\cell.ome.tiff

Now it is time to specify the WFE file.

```json
WFE_INPUT_JSON={"SCRIPT":"/Fiji.app/scripts/my_fijipyscript.py",
                "IMAGEPATH":"/input/3d_nuclei_image_holes.ome.tiff",
                "FILTERTYPE":"MEDIAN",
                "FILTER_RADIUS":5,
                "WFE_output_params_file":"/output.json"}
```

#### Main Python Script - my_fijipyscript.py

The desired core function of the APEER module are the same as for the local version of this script:

* Read the image using BioFormats
* Apply a filter to that image using the specifed radius
* Save the resulting image as OME-TIFF using BioFormats
* Create some logs to provide some information about what is happening 

The main task is to read the JSON parameters for the APEER module UI and use them instead of the script parameters of the original local Fiji version. During the following steps the main function of this script will be explained in more detail. The crucial things are directly commented inside the respective code snippets.

##### Import of modules

One important thing one has to to at the beginning is the define the required inputs. Which one are needed obviously depend from the actul script. Worth mentioning is the first line `# @LogService log`, which is required to enable the logging. This is very useful for debugging purposes later on.

```python
# @LogService log

# required import
import os
import json
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
import time
```

##### Define useful *helper* functions needed

Often it is usefule to define some *helper* functions inside the script, that can be used later inside the main part of the script code in order to structure the script and make it readable easily

For our example we need two of those function. The 1st one is called `getImageStack()` and is used to get the respective image stack from an [*ImagePlus*](https://imagej.nih.gov/ij/developer/api/ij/ImagePlus.html) object.

The 2nd one is the more interesting function for our example. This one is applying the selected filter to an image based on the selected parameters. As an input it needs:

* an *ImagePlus* object, which is the actual image
* the type of filter to be applied
* the kernel size to be used for the filter

Inside the function the correct command to apply the filter *is looked up* inside the dictionary by using the `filtertype` string. Finally the selected filter is apllied to every slice of the image stack using a simple loop.

```python
# helper function to apply the filter

def getImageStack(imp):

    # get the stacks
    try:
        stack = imp.getStack()  # get the stack within the ImagePlus
        nslices = stack.getSize()  # get the number of slices
    except:
        stack = imp.getProcessor()
        nslices = 1

    return stack, nslices


def apply_filter(imp,
                 radius=5,
                 filtertype='MEDIAN'):

    # initialize filter
    filter = RankFilters()

    # create filter dictionary
    filterdict = {}
    filterdict['MEAN'] = RankFilters.MEAN
    filterdict['MIN'] = RankFilters.MIN
    filterdict['MAX'] = RankFilters.MAX
    filterdict['MEDIAN'] = RankFilters.MEDIAN
    filterdict['VARIANCE'] = RankFilters.VARIANCE
    filterdict['OPEN'] = RankFilters.OPEN
    filterdict['DESPECKLE'] = RankFilters.DESPECKLE

    # get the stack and number of slices
    stack, nslices = getImageStack(imp)

    for index in range(1, nslices + 1):
        # get the image processor
        ip = stack.getProcessor(index)
        # apply filter based on filtertype
        filter.rank(ip, radius, filterdict[filtertype])

    return imp
```

##### Define the main image analysis pipeline

This part of the code contains the main function that is used to run the actual image analysis pipeline. The reason for creating such an extra function is that one can easily cut out this part of the script an re-use somewhere else. For our example the crucial steps inside this function are:

* Open the image by using **BioFormats**
  * when using BioFromats it is required to set the respective options
  * since an image can have many image series, it is also needed to extract the desired ImageSeries. In our example we just use the 1st one for simplicity reasons
* Apply the filter to the image by calling the helper function `apply_filter()` from above
  * In case `NONE` was slected, the script will basically just do nothing and retun the unfiltered image
  * additional it creates some logging output

```python
def run(imagefile, useBF=True, series=0):

    log.info('Image Filename : ' + imagefile)

    if not useBF:
        # using IJ static method
        imp = IJ.openImage(imagefile)

    if useBF:

        # initialize the importer options
        options = ImporterOptions()
        options.setOpenAllSeries(True)
        options.setShowOMEXML(False)
        options.setConcatenate(True)
        options.setAutoscale(True)
        options.setId(imagefile)

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if FILTERTYPE != 'NONE':

        # apply filter
        log.info('Apply Filter  : ' + FILTERTYPE)
        log.info('Filter Radius : ' + str(FILTER_RADIUS))

        # apply the filter based on the choosen type
        imp = apply_filter(imp,
                           radius=FILTER_RADIUS,
                           filtertype=FILTERTYPE)

    if FILTERTYPE == 'NONE':
        log.info('No filter selected. Do nothing.')

    return imp
```


##### Parsring the inputs from the module

This part of the script is now fundamentally different compared to a local version of the script, where the parameters are directly read by using the script parameters. In case of APEER those parameters now have to be read from the JSON file.

Additionally we define some essential other parameters like the desired output format. Since APEER prefers to use OME-TIFF this is the best choice.

```python
# Parse Inputs of Module
INPUT_JSON = json.loads(os.environ['WFE_INPUT_JSON'])
IMAGEPATH = INPUT_JSON['IMAGEPATH']

# suffix for the filename of the saved data
SUFFIX_FL = '_FILTERED'

# parameters for filter
FILTERTYPE = INPUT_JSON['FILTERTYPE']
FILTER_RADIUS = INPUT_JSON['FILTER_RADIUS']
SAVEFORMAT = 'ome.tiff'

log.info('Starting ...')
log.info('Filename               : ' + IMAGEPATH)
log.info('Save Format used       : ' + SAVEFORMAT)
log.info('------------  START IMAGE ANALYSIS ------------')
```


##### Defining the file paths

In order to save the processed image with a correct name, it is required to define this `outputimagepath` correctly.

* get the basename of the imagefile and add `/output/` infront of it
* get the basename of the `outputimagepath` without the extension
* get the file extension and check this file already ended with ".ome"
  * yes - cut out that .ome in oder to avoid filenames like *test.ome_FILTERED.ome.tiff* later on
  * no - just leave it as it is
* put together the final path for the output image

```python
# define path for the output
outputimagepath = '/output/' + os.path.basename(IMAGEPATH)
basename = os.path.splitext(outputimagepath)[0]

# remove the extra .ome before reassembling the filename
if basename[-4:] == '.ome':
    basename = basename[:-4]
    log.info('New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT
```


##### Running the main image analysis pipeline

Now it is time to call the actual `run()` function to start the processing. For the example there is an optinal extra step built-in, which is measuring the time of execution. This can be quite useful to get *a feeling* for which step actually takes how long. Put this is purely optional.

* get the starting time by using `time.clock()`
* filter the image by strating the main processing pipeline by calling ``run()`` with the respective parameters
* get the time again and calculate the execution time


```python
# get the starting time of processing pipeline
start = time.clock()

# run image analysis pipeline
filtered_image = run(IMAGEPATH,
                     useBF=True,
                     series=0)

# get time at the end and calc duration of processing
end = time.clock()
log.info('Duration of whole Processing : ' + str(end - start))
```

##### Save the processed image and write the required output specifications of the module

Once the got the `filtered_image` as a result it mujst be saved as OME-TIFF using the BioFormats library. When running a script in headless mode it is required to use the `LociExporter` method with the respective `paramstring` that define sthe options.

* define the `paramstring` with the correct `outputimagepath` as part of the argument string
* save the image by calling `exporter.run()`
* at the end it is crucial to write all required output parameters to the JSON file. Check the *module_specification.json* for the correct naming
* finally exit your script using `os._exit()`

```python
start = time.clock()

# create the argument string for the BioFormats Exporter and save as OME.TIFF
paramstring = "outfile=" + outputimagepath + " " + "windowless=true compression=Uncompressed saveROI=false"
plugin = LociExporter()
plugin.arg = paramstring
exporter = Exporter(plugin, filtered_image)
exporter.run()

# get time at the end and calc duration of processing
end = time.clock()
log.info('Duration of saving as OME.TIFF : ' + str(end - start))

# write output JSON
log.info('Writing output JSON file ...')
output_json = {"FILTERED_IMAGE": outputimagepath}

with open("/output/" + INPUT_JSON['WFE_output_params_file'], 'w') as f:
    json.dump(output_json, f)

# finish
log.info('Done.')
os._exit()
```


#### Complete Script - Module version

This is the complete python script example wihich runs inside the APEER module.

```python
# @LogService log

# required import
import os
import json
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
import time

# helper function to apply the filetr

def getImageStack(imp):

    # get the stacks
    try:
        stack = imp.getStack()  # get the stack within the ImagePlus
        nslices = stack.getSize()  # get the number of slices
    except:
        stack = imp.getProcessor()
        nslices = 1

    return stack, nslices


def apply_filter(imp,
                 radius=5,
                 filtertype='MEDIAN'):

    # initialize filter
    filter = RankFilters()

    # create filter dictionary
    filterdict = {}
    filterdict['MEAN'] = RankFilters.MEAN
    filterdict['MIN'] = RankFilters.MIN
    filterdict['MAX'] = RankFilters.MAX
    filterdict['MEDIAN'] = RankFilters.MEDIAN
    filterdict['VARIANCE'] = RankFilters.VARIANCE
    filterdict['OPEN'] = RankFilters.OPEN
    filterdict['DESPECKLE'] = RankFilters.DESPECKLE

    # get the stack and number of slices
    stack, nslices = getImageStack(imp)

    for index in range(1, nslices + 1):
        # get the image processor
        ip = stack.getProcessor(index)
        # apply filter based on filtertype
        filter.rank(ip, radius, filterdict[filtertype])

    return imp


############################################################################


def run(imagefile, useBF=True, series=0):

    log.info('Image Filename : ' + imagefile)

    if not useBF:
        # using IJ static method
        imp = IJ.openImage(imagefile)

    if useBF:

        # initialize the importer options
        options = ImporterOptions()
        options.setOpenAllSeries(True)
        options.setShowOMEXML(False)
        options.setConcatenate(True)
        options.setAutoscale(True)
        options.setId(imagefile)

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if FILTERTYPE != 'NONE':

        # apply filter
        log.info('Apply Filter  : ' + FILTERTYPE)
        log.info('Filter Radius : ' + str(FILTER_RADIUS))

        # apply the filter based on the choosen type
        imp = apply_filter(imp,
                           radius=FILTER_RADIUS,
                           filtertype=FILTERTYPE)

    if FILTERTYPE == 'NONE':
        log.info('No filter selected. Do nothing.')

    return imp


#########################################################################

# Parse Inputs of Module
INPUT_JSON = json.loads(os.environ['WFE_INPUT_JSON'])
IMAGEPATH = INPUT_JSON['IMAGEPATH']

# suffix for the filename of the saved data
SUFFIX_FL = '_FILTERED'

# parameters for filter
FILTERTYPE = INPUT_JSON['FILTERTYPE']
FILTER_RADIUS = INPUT_JSON['FILTER_RADIUS']
SAVEFORMAT = 'ome.tiff'

log.info('Starting ...')
log.info('Filename               : ' + IMAGEPATH)
log.info('Save Format used       : ' + SAVEFORMAT)
log.info('------------  START IMAGE ANALYSIS ------------')

##############################################################

# define path for the output
outputimagepath = '/output/' + os.path.basename(IMAGEPATH)
basename = os.path.splitext(outputimagepath)[0]

# remove the extra .ome before reassembling the filename
if basename[-4:] == '.ome':
    basename = basename[:-4]
    log.info('New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT

#############   RUN MAIN IMAGE ANALYSIS PIPELINE ##########

# get the starting time of processing pipeline
start = time.clock()

# run image analysis pipeline
filtered_image = run(IMAGEPATH,
                     useBF=True,
                     series=0)

# get time at the end and calc duration of processing
end = time.clock()
log.info('Duration of whole Processing : ' + str(end - start))

###########################################################

start = time.clock()

# create the argument string for the BioFormats Exporter and save as OME.TIFF
paramstring = "outfile=" + outputimagepath + " " + "windowless=true compression=Uncompressed saveROI=false"
plugin = LociExporter()
plugin.arg = paramstring
exporter = Exporter(plugin, filtered_image)
exporter.run()

# get time at the end and calc duration of processing
end = time.clock()
log.info('Duration of saving as OME.TIFF : ' + str(end - start))

# write output JSON
log.info('Writing output JSON file ...')
output_json = {"FILTERED_IMAGE": outputimagepath}

with open("/output/" + INPUT_JSON['WFE_output_params_file'], 'w') as f:
    json.dump(output_json, f)

# finish
log.info('Done.')
os._exit()
```


#### Creating the Dockerfile for the APEER module

Each module on the platfrom is packaged into what is called a "Docker Container". Introducing Docker would far exceed this tutorial so if you don't know what Docker is we recommend that you start by reading some ressources online (e.g. [Getting Started](https://docs.Docker.com/get-started/)) to get familiar with the technology.

Below you see the Dockerfile for this module. In this file it is specified what the container should include.

```Dockerfile
# czsip/fiji_linux64_baseimage
# Author: sebi06
# Version: 1.0

# Use existing image: Pull base Fiji baseimage from docker hub
FROM czsip/fiji_linux64_baseimage:1.1.8

# add Fiji to path
ENV PATH $PATH:/Fiji.app/

# mount volumes
VOLUME [ "/input", "/output" ]

# copy scripts and files
COPY ./my_fijipyscript.py /Fiji.app/scripts

# define the starting script
COPY ./start.sh /
ENTRYPOINT ["sh","./start.sh"]
```

* pull the container image we want to build our module on from the main Docker website (i.e. the [Docker Hub](https://hub.Docker.com/)) this is accomplishe by using the *FROM* command and specifying the conatiner image, which is based on Ubuntu and included Fiji:

``FROM czsip/fiji_linux64_baseimage:1.1.8``


* Using `COPY` we then add all additional files we need into the Docker container.

* with the `VOLUME` command we specifiy the additional directories that are going to be mounted later by the for exposing files to and from the container. **This is WFE convention and will always be the same.**

* Finally we need to define the `ENTRYPOINT` for the Docker container. The entrypoint is the command executed during the start of the container. Here we execute a shell script once the container starts.


### Testing your module locally

If you are developing modules for the platform it is a good idea to install a local Docker environment. Docker is availabel for all major OS. 
For this tutorial we assume that you already have a local Docker installation and some basic knowledge how to use it. 
**Please refere to online ressources for in depth Docker tutorials.**

##### Building and running your module locally

To build your module container locally navigate to the folder containing all your files and run

```bash
docker build --rm -t test/apeer_test_fijimodule:latest .
```
This command tells Docker to execute a build:

* --rm: will remove intermediary containers after a successful build

* -t: specifies the name of your container

* .: docker will look for a file name *Dockerfile* and use it to build the container accordingly.

If you are running the build for the first time this may take a while because Docker needs to download the base container as well as executing all commands you specified in your dockerfile.
Once the build completed you can use the following command to display all local availabel docker containers.

```
docker images
```

With the build completed you now have the container available and can start it locally to see if everything is working as intended. Run the container using the input specified inside the *wfe.env* file:


##### Run the module locally

```shell
docker run -v C:\Test\input:/input -v C:\Test\output:/output -v C:\Test\params:/params camodules.azurecr.io/stack_generator:latest
```

* -v: docker will use a local folder and map it to a path inside the docker container. Here we are making two local folders available inside of the docker container as *\input* and *\output*.
* If all works out you should see the container starting and log output appearing on the command line. After the container completes the results can be found in *C:\Test\output\* in this example.

**Note**: One can also store all local files in one folder and map this location to the three different paths inside of the docker

**Important**: You might need to enable local file system access for the Docker client so it has permission to access the local folders (e.g Windows you need to open the "Setting > Sharing" in the Docker client and share the respective drive).

Usually the result should like this inside the terminal:

```shell
C:\Users\test\Apeer\fiji_module_template_b88fae21-48c18efc9fa8>docker run -it --rm -v c:\Temp\input:/input -v c:\Temp\output:/output --env-file wfe.env sebi/apeer_test_fijimodule:latest
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option PermSize=128m; support was removed in 8.0
Java HotSpot(TM) 64-Bit Server VM warning: Using incremental CMS is deprecated and will likely be removed in a future release
[INFO] Overriding BIOP Run Macro...; identifier: command:ch.epfl.biop.macrorunner.B_Run_Macro; jar: file:/Fiji.app/plugins/BIOP/B_Run_Macro-1.0.0-SNAPSHOT.jar
[INFO] Overriding Get Spine From Circle Rois; identifier: command:Cirlces_Based_Spine; jar: file:/Fiji.app/plugins/Max_Inscribed_Circles-1.1.0.jar
[INFO] Starting ...
[INFO] Filename               : /input/3d_nuclei_image_holes.ome.tiff
[INFO] Save Format used       : ome.tiff
[INFO] ------------  START IMAGE ANALYSIS ------------
[INFO] New basename for output :/output/3d_nuclei_image_holes
[INFO] Image Filename : /input/3d_nuclei_image_holes.ome.tiff
[INFO] Apply Filter  : MEDIAN
[INFO] Filter Radius : 5
[INFO] Duration of whole Processing : 18.8419955
[INFO] Duration of saving as OME.TIFF : 28.9042946
[INFO] Writing output JSON file ...
[INFO] Done.

C:\Users\test\Apeer\fiji_module_template_b88fae21-48c18efc9fa8>
```

**Now commit the complete code and push it to the repository. This will trigger a new build of your module.**


### Final Notes

This is the first version of this tutorial and it can certainly be improved. If you have suggestions or improvements please leave them in the [APEER Forum](https://forum.apeer.com/) and we will continously improve our tutorials.
