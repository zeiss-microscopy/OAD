# Tutorial: Using ImageJ/Fiji scripts in APEER modules - Create your own module

This tutorial describe how to create an APEER module based on an existing ImageJ / Fiji python script or how to easily adapt such a script for APEER.

**To follow this tutorial basic python scripting knowledge is required.**

## Goal of the tutorial

Create a module that based on ImageJ/Fiji scripting language Python.

## Introduction

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


### Script Parameters

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

![Fiji Script Parameters - User Interface](./images/Fiji_Scriptparameter_UI.png)

### Complete Example Script - Local Fiji version

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

#################################################################
# File        : my_fijipyscript_local.py
# Version     : 0.0.8
# Author      : czsrh
# Date        : 20.02.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# The idea of this module is to provide a template showing some of the required
# code parts in order to create modules based on Fiji. The chosen processing step
# is just an example for your image analysis pipeline
#
# ATTENTION: Use at your own risk.
#
# Copyright(c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# required imports
import os
import json
import time
import sys
from collections import OrderedDict
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
from org.scijava.log import LogLevel
from loci.plugins.util import LociPrefs
from loci.plugins.out import Exporter
from loci.plugins import LociExporter
from loci.formats import ImageReader
from loci.formats import MetadataTools
from loci.formats.in import ZeissCZIReader
from loci.formats.in import DynamicMetadataOptions
from ome.units import UNITS


######### HELPER FUNCTIONS ##############

# helper function to apply the filter
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
    stack = imp.getStack()  # get the stack within the ImagePlus
    nslices = stack.getSize()  # get the number of slices

    # apply filter based on filtertype
    if filtertype in filterdict:
        for index in range(1, nslices + 1):
            ip = stack.getProcessor(index)
            filter.rank(ip, radius, filterdict[filtertype])
    else:
        print("Argument 'filtertype': {filtertype} not found")

    return imp


def get_metadata(imagefile, imageID=0):

    metainfo = {}

    # initialize the reader and get the OME metadata
    reader = ImageReader()
    omeMeta = MetadataTools.createOMEXMLMetadata()
    metainfo['ImageCount_OME'] = omeMeta.getImageCount()
    reader.setMetadataStore(omeMeta)
    reader.setId(imagefile)
    metainfo['SeriesCount_BF'] = reader.getSeriesCount()
    reader.close()

    # read dimensions TZCXY from OME metadata
    metainfo['SizeT'] = omeMeta.getPixelsSizeT(imageID).getValue()
    metainfo['SizeZ'] = omeMeta.getPixelsSizeZ(imageID).getValue()
    metainfo['SizeC'] = omeMeta.getPixelsSizeC(imageID).getValue()
    metainfo['SizeX'] = omeMeta.getPixelsSizeX(imageID).getValue()
    metainfo['SizeY'] = omeMeta.getPixelsSizeY(imageID).getValue()

    # store info about stack
    if metainfo['SizeZ'] == 1:
        metainfo['is3d'] = False
    elif metainfo['SizeZ'] > 1:
        metainfo['is3d'] = True

    # get the scaling for XYZ
    physSizeX = omeMeta.getPixelsPhysicalSizeX(0)
    physSizeY = omeMeta.getPixelsPhysicalSizeY(0)
    physSizeZ = omeMeta.getPixelsPhysicalSizeZ(0)

    if physSizeX is not None:
        metainfo['ScaleX'] = round(physSizeX.value(), 3)
        metainfo['ScaleY'] = round(physSizeY.value(), 3)
    if physSizeX is None:
        metainfo['ScaleX'] = None
        metainfo['ScaleY'] = None

    if physSizeZ is not None:
        metainfo['ScaleZ'] = round(physSizeZ.value(), 3)
    if physSizeZ is None:
        metainfo['ScaleZ'] = None

    # sort the dictionary
    metainfo =  OrderedDict(sorted(metainfo.items()))

    return metainfo

############################################################################

if not HEADLESS:
    # clear the console automatically when not in headless mode
    uiService.getDefaultUI().getConsolePane().clear()


def run(imagefile, useBF=True,
                   series=0,
                   filtertype='MEDIAN',
                   filterradius='5'):

    log.log(LogLevel.INFO, 'Image Filename : ' + imagefile)

    # get basic image metainfo
    metainfo = get_metadata(imagefile, imageID=series)
    for k, v in metainfo.items():
        log.log(LogLevel.INFO, str(k) + ' : ' + str(v))

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
        options.setStitchTiles(True)

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if filtertype != 'NONE':

        # apply filter
        log.log(LogLevel.INFO, 'Apply Filter  : ' + filtertype)
        log.log(LogLevel.INFO, 'Filter Radius : ' + str(filterradius))

        # apply the filter based on the chosen type
        imp = apply_filter(imp,
                           radius=filterradius,
                           filtertype=filtertype)

    if filtertype == 'NONE':
        log.log(LogLevel.INFO, 'No filter selected. Do nothing.')

    return imp


#########################################################################

# the the filename
IMAGEPATH = FILENAME.toString()

# suffix for the filename of the saved data
SUFFIX_FL = '_FILTERED'
SAVEFORMAT = 'ome.tiff'

# log some outputs
log.log(LogLevel.INFO, 'Starting ...')
log.log(LogLevel.INFO, 'Filename               : ' + IMAGEPATH)
log.log(LogLevel.INFO, 'Save Format used       : ' + SAVEFORMAT)
log.log(LogLevel.INFO, '------------  START IMAGE ANALYSIS ------------')

##############################################################

# define path for the output
outputimagepath = '/output/' + os.path.basename(IMAGEPATH)
basename = os.path.splitext(outputimagepath)[0]

# remove the extra .ome before reassembling the filename
if basename[-4:] == '.ome':
    basename = basename[:-4]
    log.log(LogLevel.INFO, 'New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT

#############   RUN MAIN IMAGE ANALYSIS PIPELINE ##########

# get the starting time of processing pipeline
start = time.clock()

# run image analysis pipeline
filtered_image = run(IMAGEPATH,
                     useBF=True,
                     series=0,
                     filtertype=FILTERTYPE,
                     filterradius=FILTER_RADIUS)

# get time at the end and calc duration of processing
end = time.clock()
log.log(LogLevel.INFO, 'Duration of whole Processing : ' + str(end - start))

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
log.log(LogLevel.INFO, 'Duration of saving as OME-TIFF : ' + str(end - start))

# show the image
filtered_image.show()

# finish
log.log(LogLevel.INFO, 'Done.')
```

## Structure and Files of APEER module repository

Below you see an overview of the files we will generate for this tutorial.
All these files except the Dockerfile and the json will be utilized within the Docker Container.

```shell
├── Dockerfile                  (the file necessary to generate the Docker container)
├── module_specification.json   (module input/output and GUI specification for the WFE)
├── my_fijipyscript.py          (the actual Fiji script)
├── start.sh                    (shell script to run Fiji script from the command line)
└── wfe.env                     (file for defining environment variables for local test runs)
```

### Prerequisites - How to create a Docker Container with Fiji inside

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
# Prerequisites
# - download latest fiji_linux64 from web
# - copy Fiji.app folder it to the folder where your dockerfile is placed
# place your additional fiji scripts inside the root folder
# run docker file to built the image and enjoy

# Pull base JDK-8 image only if using Fiji that doe not already contain a JDK.
#FROM java:8-jre

FROM ubuntu:latest

# get additional stuff
RUN apt-get update
RUN apt-get install -y apt-utils software-properties-common
RUN apt-get upgrade -y

# get Xvfb virtual X server and configure
RUN apt-get install -y xvfb x11vnc x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps
RUN apt-get install -y libxrender1 libxtst6 libxi6
COPY ./font.conf /etc/fonts/fonts.conf

# copy fiji
COPY ./Fiji.app /Fiji.app

# copy Fiji and other scripts or files
COPY ./fijipytools.py /Fiji.app/scripts

# Setting ENV for Xvfb and Fiji
ENV DISPLAY :99

# add Fiji tp PATH
ENV PATH $PATH:/Fiji.app/

# add Fiji-Update sites only works when connected to the internet
RUN ./Fiji.app/ImageJ-linux64 --ij2 --headless --update update
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site 3DImageJSuite http://sites.imagej.net/Tboudier/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BAR http://sites.imagej.net/Tiago/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site EMBL-CBA http://sites.imagej.net/EMBL-CBA/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BASIC http://sites.imagej.net/BaSiC/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BIG-EPFL http://sites.imagej.net/BIG-EPFL/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BioVoxxel http://sites.imagej.net/BioVoxxel/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site CMP-BIAtools http://sites.imagej.net/CMP-BIA/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site IBMP-CNRS http://sites.imagej.net/Mutterer/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site IJPB-plugins http://sites.imagej.net/IJPB-plugins/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site ImageScience http://sites.imagej.net/ImageScience/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site IMCFUniBasel http://sites.imagej.net/UniBas-IMCF/
#RUN ./Fiji.app/ImageJ-linux64 --update add-update-site MOSAICToolSuite http://mosaic.mpi-cbg.de/Downloads/update/Fiji/MosaicToolsuite
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site CLIX-Assistant https://sites.imagej.net/clijx-assistant/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site CLIX-Assistant-Extensions https://sites.imagej.net/clijx-assistant-extensions/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site PTBIOP http://biop.epfl.ch/Fiji-Update
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site CLIJ http://sites.imagej.net/clij
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site CLIJ2 http://sites.imagej.net/clij2
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site StarDist http://sites.imagej.net/StarDist
#RUN ./Fiji.app/ImageJ-linux64 --update add-update-site TensorFlow https://sites.imagej.net/TensorFlow/
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site CSBDeep https://sites.imagej.net/CSBDeep
RUN ./Fiji.app/ImageJ-linux64 --update add-update-site BigDataProcessor https://sites.imagej.net/BigDataProcessor/
RUN ./Fiji.app/ImageJ-linux64 --ij2 --headless --update update
RUN ./Fiji.app/ImageJ-linux64 --ij2 --headless

```

When the login was successful start the build and push the new container.

```bash
docker build -t xyz/fiji_linux64_baseimage:tag .

docker push xyz/fiji_linux64_baseimage:tag
```

That's it. Now this container can be used later when creating the actual module.


### Module Creation: Step-by-Step

There is no specific order in which the files from above have to be created, so feel free to start with the file you prefer.

### Module Specifications

The module specification are the same as you have seen in previous tutorials (See [Module Specification Tutorial](https://docs.apeer.com/documentation/module-specification "Module Specification Tutorial"))

In brief you need to supply a JSON file that specifies your inputs, outputs and if neccessary how the UI for the module looks like in case the user can interact with the module. In our case this specification file looks like this:

```json
{
  "spec": {
    "inputs": {
      "IMAGEPATH": {
        "type:file": {
          "format": ["czi", "tiff", "png", "jpeg", "ome-tiff"]
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
          "format": ["ome-tiff"]
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
              "key": "MEDIAN",
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


![APEER - Module UI based on JSON file](./images/apeer_module_UI.png)

### Shell script for the Docker Entry Point

As discussed above when a container is executed it will run the command supplied by the *ENTRYPOINT* parameters.
On our example we execute a shell script that contains the following command below. In essence we start ImageJ with the argument to run our python script

Make sure that the variable `SCRIPT` inside the bash script is specified correctly.

```shell
#!/bin/sh
SCRIPT=/Fiji.app/scripts/my_fijipyscript.py

/Fiji.app/ImageJ-linux64 --ij2 --headless --console --run $SCRIPT
```

### Defining the WFE file for local testing (optional)

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

### Main Python Script - my_fijipyscript.py

The desired core function of the APEER module are the same as for the local version of this script:

* Read the image using BioFormats
* Apply a filter to that image using the specified radius
* Save the resulting image as OME-TIFF using BioFormats
* Create some logs to provide some information about what is happening 

The main task is to read the JSON parameters for the APEER module UI and use them instead of the script parameters of the original local Fiji version. During the following steps the main function of this script will be explained in more detail. The crucial things are directly commented inside the respective code snippets.

#### Import of modules

One important thing one has to to at the beginning is the define the required inputs. Which one are needed obviously depend from the actul script. Worth mentioning is the first line `# @LogService log`, which is required to enable the logging. This is very useful for debugging purposes later on.

```python
# required imports
import os
import json
import time
import sys
from collections import OrderedDict
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
from org.scijava.log import LogLevel
from loci.plugins.util import LociPrefs
from loci.plugins.out import Exporter
from loci.plugins import LociExporter
from loci.formats import ImageReader
from loci.formats import MetadataTools
from loci.formats.in import ZeissCZIReader
from loci.formats.in import DynamicMetadataOptions
from ome.units import UNITS
```

#### Define useful *helper* functions needed

Often it is usefule to define some *helper* functions inside the script, that can be used later inside the main part of the script code in order to structure the script and make it readable easily

For our example we need two of those function. The 1st one is called `get_metadata` and is used to get the respective metadata from the image.

The 2nd one `apply_filter` is the more interesting function for our example. This one is applying the selected filter to an image based on the selected parameters. As an input it needs:

* an *ImagePlus* object, which is the actual image
* the type of filter to be applied
* the kernel size to be used for the filter

Inside the function the correct command to apply the filter *is looked up* inside the dictionary by using the `filtertype` string. Finally the selected filter is apllied to every slice of the image stack using a simple loop.

```python
def get_metadata(imagefile, imageID=0):

    metainfo = {}

    # initialize the reader and get the OME metadata
    reader = ImageReader()
    omeMeta = MetadataTools.createOMEXMLMetadata()
    metainfo['ImageCount_OME'] = omeMeta.getImageCount()
    reader.setMetadataStore(omeMeta)
    reader.setId(imagefile)
    metainfo['SeriesCount_BF'] = reader.getSeriesCount()
    reader.close()

    # read dimensions TZCXY from OME metadata
    metainfo['SizeT'] = omeMeta.getPixelsSizeT(imageID).getValue()
    metainfo['SizeZ'] = omeMeta.getPixelsSizeZ(imageID).getValue()
    metainfo['SizeC'] = omeMeta.getPixelsSizeC(imageID).getValue()
    metainfo['SizeX'] = omeMeta.getPixelsSizeX(imageID).getValue()
    metainfo['SizeY'] = omeMeta.getPixelsSizeY(imageID).getValue()

    # store info about stack
    if metainfo['SizeZ'] == 1:
        metainfo['is3d'] = False
    elif metainfo['SizeZ'] > 1:
        metainfo['is3d'] = True

    # get the scaling for XYZ
    physSizeX = omeMeta.getPixelsPhysicalSizeX(0)
    physSizeY = omeMeta.getPixelsPhysicalSizeY(0)
    physSizeZ = omeMeta.getPixelsPhysicalSizeZ(0)

    if physSizeX is not None:
        metainfo['ScaleX'] = round(physSizeX.value(), 3)
        metainfo['ScaleY'] = round(physSizeY.value(), 3)
    if physSizeX is None:
        metainfo['ScaleX'] = None
        metainfo['ScaleY'] = None

    if physSizeZ is not None:
        metainfo['ScaleZ'] = round(physSizeZ.value(), 3)
    if physSizeZ is None:
        metainfo['ScaleZ'] = None

    # sort the dictionary
    metainfo =  OrderedDict(sorted(metainfo.items()))

    return metainfo


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
    stack = imp.getStack()  # get the stack within the ImagePlus
    nslices = stack.getSize()  # get the number of slices

    # apply filter based on filtertype
    if filtertype in filterdict:
        for index in range(1, nslices + 1):
            ip = stack.getProcessor(index)
            filter.rank(ip, radius, filterdict[filtertype])
    else:
        print("Argument 'filtertype': {filtertype} not found")

    return imp
```

#### Define the main image analysis pipeline

This part of the code contains the main function that is used to run the actual image analysis pipeline. The reason for creating such an extra function is that one can easily cut out this part of the script an re-use somewhere else. For our example the crucial steps inside this function are:

* Open the image by using **BioFormats**
  * when using BioFromats it is required to set the respective options
  * since an image can have many image series, it is also needed to extract the desired ImageSeries. In our example we just use the 1st one for simplicity reasons
* Apply the filter to the image by calling the helper function `apply_filter()` from above
  * In case `NONE` was slected, the script will basically just do nothing and retun the unfiltered image
  * additional it creates some logging output

```python
def run(imagefile, useBF=True,
                   series=0,
                   filtertype='MEDIAN',
                   filterradius='5'):

    log.log(LogLevel.INFO, 'Image Filename : ' + imagefile)

    # get basic image metainfo
    metainfo = get_metadata(imagefile, imageID=series)
    for k, v in metainfo.items():
        log.log(LogLevel.INFO, str(k) + ' : ' + str(v))

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
        options.setStitchTiles(True)

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if filtertype != 'NONE':

        # apply filter
        log.log(LogLevel.INFO, 'Apply Filter  : ' + filtertype)
        log.log(LogLevel.INFO, 'Filter Radius : ' + str(filterradius))

        # apply the filter based on the chosen type
        imp = apply_filter(imp,
                           radius=filterradius,
                           filtertype=filtertype)

    if filtertype == 'NONE':
        log.log(LogLevel.INFO, 'No filter selected. Do nothing.')

    return imp
```


#### Parsing the inputs from the module

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
FILTER_RADIUS = int(INPUT_JSON['FILTER_RADIUS'])
SAVEFORMAT = 'ome.tiff'

log.log(LogLevel.INFO, 'Starting ...')
log.log(LogLevel.INFO, 'Filename               : ' + IMAGEPATH)
log.log(LogLevel.INFO, 'Save Format used       : ' + SAVEFORMAT)
log.log(LogLevel.INFO, '------------  START IMAGE ANALYSIS ------------')
```


#### Defining the file paths

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
    log.log(LogLevel.INFO, 'New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT
```


#### Running the main image analysis pipeline

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
                     series=0,
                     filtertype=FILTERTYPE,
                     filterradius=FILTER_RADIUS)

# get time at the end and calc duration of processing
end = time.clock()
log.log(LogLevel.INFO, 'Duration of whole Processing : ' + str(end - start))
```

#### Save the processed image and write the required output specifications of the module

Once the got the `filtered_image` as a result it mujst be saved as OME-TIFF using the BioFormats library. When running a script in headless mode it is required to use the `LociExporter` method with the respective `paramstring` that define sthe options.

* define the `paramstring` with the correct `outputimagepath` as part of the argument string
* save the image by calling `exporter.run()`
* at the end it is crucial to write all required output parameters to the JSON file. Check the *module_specification.json* for the correct naming
* finally exit your script using `os._exit()`

```python
start = time.clock()

# create the argument string for the BioFormats Exporter and save as OME.TIFF
paramstring = "outfile=[" + outputimagepath + "] windowless=true compression=Uncompressed saveROI=false"
plugin = LociExporter()
plugin.arg = paramstring
exporter = Exporter(plugin, filtered_image)
exporter.run()

# get time at the end and calc duration of processing
end = time.clock()
log.log(LogLevel.INFO, 'Duration of saving as OME.TIFF : ' + str(end - start))

# write output JSON
log.log(LogLevel.INFO, 'Writing output JSON file ...')
output_json = {"FILTERED_IMAGE": outputimagepath}

with open("/output/" + INPUT_JSON['WFE_output_params_file'], 'w') as f:
    json.dump(output_json, f)

# finish
log.log(LogLevel.INFO, 'Done.')

# exit
os._exit()
```

### Complete Script - Module version

This is the complete python script example which runs inside the APEER module.

```python
# @LogService log

#################################################################
# File        : my_fijipyscript.py
# Version     : 0.0.8
# Author      : czsrh
# Date        : 20.02.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# The idea of this module is to provide a template showing some of the required
# code parts in order to create modules based on Fiji. The chosen processing step
# is just an example for your image analysis pipeline
#
# ATTENTION: Use at your own risk.
#
# Copyright(c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# required imports
import os
import json
import time
import sys
from collections import OrderedDict
from java.lang import Double, Integer
from ij import IJ, ImagePlus, ImageStack, Prefs
from ij.process import ImageProcessor, LUT
from ij.plugin.filter import RankFilters
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.plugins import LociExporter
from loci.plugins.out import Exporter
from ij.io import FileSaver
from org.scijava.log import LogLevel
from loci.plugins.util import LociPrefs
from loci.plugins.out import Exporter
from loci.plugins import LociExporter
from loci.formats import ImageReader
from loci.formats import MetadataTools
from loci.formats.in import ZeissCZIReader
from loci.formats.in import DynamicMetadataOptions
from ome.units import UNITS


######### HELPER FUNCTIONS ##############

# helper function to apply the filter
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
    stack = imp.getStack()  # get the stack within the ImagePlus
    nslices = stack.getSize()  # get the number of slices

    # apply filter based on filtertype
    if filtertype in filterdict:
        for index in range(1, nslices + 1):
            ip = stack.getProcessor(index)
            filter.rank(ip, radius, filterdict[filtertype])
    else:
        print("Argument 'filtertype': {filtertype} not found")

    return imp


def get_metadata(imagefile, imageID=0):

    metainfo = {}

    # initialize the reader and get the OME metadata
    reader = ImageReader()
    omeMeta = MetadataTools.createOMEXMLMetadata()
    metainfo['ImageCount_OME'] = omeMeta.getImageCount()
    reader.setMetadataStore(omeMeta)
    reader.setId(imagefile)
    metainfo['SeriesCount_BF'] = reader.getSeriesCount()
    reader.close()

    # read dimensions TZCXY from OME metadata
    metainfo['SizeT'] = omeMeta.getPixelsSizeT(imageID).getValue()
    metainfo['SizeZ'] = omeMeta.getPixelsSizeZ(imageID).getValue()
    metainfo['SizeC'] = omeMeta.getPixelsSizeC(imageID).getValue()
    metainfo['SizeX'] = omeMeta.getPixelsSizeX(imageID).getValue()
    metainfo['SizeY'] = omeMeta.getPixelsSizeY(imageID).getValue()

    # store info about stack
    if metainfo['SizeZ'] == 1:
        metainfo['is3d'] = False
    elif metainfo['SizeZ'] > 1:
        metainfo['is3d'] = True

    # get the scaling for XYZ
    physSizeX = omeMeta.getPixelsPhysicalSizeX(0)
    physSizeY = omeMeta.getPixelsPhysicalSizeY(0)
    physSizeZ = omeMeta.getPixelsPhysicalSizeZ(0)

    if physSizeX is not None:
        metainfo['ScaleX'] = round(physSizeX.value(), 3)
        metainfo['ScaleY'] = round(physSizeY.value(), 3)
    if physSizeX is None:
        metainfo['ScaleX'] = None
        metainfo['ScaleY'] = None

    if physSizeZ is not None:
        metainfo['ScaleZ'] = round(physSizeZ.value(), 3)
    if physSizeZ is None:
        metainfo['ScaleZ'] = None

    # sort the dictionary
    metainfo =  OrderedDict(sorted(metainfo.items()))

    return metainfo


############################################################################


def run(imagefile, useBF=True,
                   series=0,
                   filtertype='MEDIAN',
                   filterradius='5'):

    log.log(LogLevel.INFO, 'Image Filename : ' + imagefile)

    # get basic image metainfo
    metainfo = get_metadata(imagefile, imageID=series)
    for k, v in metainfo.items():
        log.log(LogLevel.INFO, str(k) + ' : ' + str(v))


    if not useBF:
        # using IJ static method
        imp = IJ.openImage(imagefile)

    if useBF:
        # initialize the importer options for BioFormats
        options = ImporterOptions()
        options.setOpenAllSeries(True)
        options.setShowOMEXML(False)
        options.setConcatenate(True)
        options.setAutoscale(True)
        options.setId(imagefile)
        options.setStitchTiles(True)

        # open the ImgPlus
        imps = BF.openImagePlus(options)
        imp = imps[series]

    # apply the filter
    if filtertype != 'NONE':

        # apply filter
        log.log(LogLevel.INFO, 'Apply Filter  : ' + filtertype)
        log.log(LogLevel.INFO, 'Filter Radius : ' + str(filterradius))

        # apply the filter based on the chosen type
        imp = apply_filter(imp,
                           radius=filterradius,
                           filtertype=filtertype)

    if filtertype == 'NONE':
        log.log(LogLevel.INFO, 'No filter selected. Do nothing.')

    return imp


#########################################################################

# Parse Inputs of Module
INPUT_JSON = json.loads(os.environ['WFE_INPUT_JSON'])
IMAGEPATH = INPUT_JSON['IMAGEPATH']

# suffix for the filename of the saved data
SUFFIX_FL = '_FILTERED'

# parameters for filter
FILTERTYPE = INPUT_JSON['FILTERTYPE']
FILTER_RADIUS = int(INPUT_JSON['FILTER_RADIUS'])
SAVEFORMAT = 'ome.tiff'

# log some outputs
log.log(LogLevel.INFO, 'Starting ...')
log.log(LogLevel.INFO, 'Filename               : ' + IMAGEPATH)
log.log(LogLevel.INFO, 'Save Format used       : ' + SAVEFORMAT)
log.log(LogLevel.INFO, '------------  START IMAGE ANALYSIS ------------')

##############################################################

# define path for the output
outputimagepath = '/output/' + os.path.basename(IMAGEPATH)
basename = os.path.splitext(outputimagepath)[0]

# remove the extra .ome before reassembling the filename
if basename[-4:] == '.ome':
    basename = basename[:-4]
    log.log(LogLevel.INFO, 'New basename for output :' + basename)

# save processed image
outputimagepath = basename + SUFFIX_FL + '.' + SAVEFORMAT

#############   RUN MAIN IMAGE ANALYSIS PIPELINE ##########

# get the starting time of processing pipeline
start = time.clock()

# run image analysis pipeline
filtered_image = run(IMAGEPATH,
                     useBF=True,
                     series=0,
                     filtertype=FILTERTYPE,
                     filterradius=FILTER_RADIUS)

# get time at the end and calc duration of processing
end = time.clock()
log.log(LogLevel.INFO, 'Duration of Processing : ' + str(end - start))

###########################################################

start = time.clock()

# create the argument string for the BioFormats Exporter and save as OME.TIFF
paramstring = "outfile=[" + outputimagepath + "] windowless=true compression=Uncompressed saveROI=false"
plugin = LociExporter()
plugin.arg = paramstring
exporter = Exporter(plugin, filtered_image)
exporter.run()

# get time at the end and calc duration of processing
end = time.clock()
log.log(LogLevel.INFO, 'Duration of saving as OME.TIFF : ' + str(end - start))

# create output JSON
log.log(LogLevel.INFO, 'Writing output JSON file ...')

output_json = {"FILTERED_IMAGE": outputimagepath}

# write output JSON
with open("/output/" + INPUT_JSON['WFE_output_params_file'], 'w') as f:
    json.dump(output_json, f)

# finish and exit
log.log(LogLevel.INFO, 'Done.')
os._exit()
```


### Creating the Dockerfile for the APEER module

Each module on the platfrom is packaged into what is called a "Docker Container". Introducing Docker would far exceed this tutorial so if you don't know what Docker is we recommend that you start by reading some ressources online (e.g. [Getting Started](https://docs.Docker.com/get-started/)) to get familiar with the technology.

Below you see the Dockerfile for this module. In this file it is specified what the container should include.

```Dockerfile
# Use exiszing image: Pull base Fiji baseimage from docker hub
FROM czsip/fiji_linux64_baseimage:1.3.7

# add Fiji to path
ENV PATH $PATH:/Fiji.app/

# mount volumes
VOLUME [ "/input", "/output" ]

# copy other scripts or files (when required)
COPY ./my_fijipyscript.py /Fiji.app/scripts

# define the starting script
COPY ./start.sh /
ENTRYPOINT ["sh","./start.sh"]
```

* pull the container image we want to build our module on from the main Docker website (i.e. the [Docker Hub](https://hub.Docker.com/)) this is accomplishe by using the *FROM* command and specifying the conatiner image, which is based on Ubuntu and included Fiji:

``FROM czsip/fiji_linux64_baseimage:1.3.7``


* Using `COPY` we then add all additional files we need into the Docker container.

* with the `VOLUME` command we specifiy the additional directories that are going to be mounted later by the for exposing files to and from the container. **This is WFE convention and will always be the same.**

* Finally we need to define the `ENTRYPOINT` for the Docker container. The entrypoint is the command executed during the start of the container. Here we execute a shell script once the container starts.

### Building and running your module locally

If you are developing modules for the platform it is a good idea to install a local Docker environment. Docker is availabel for all major OS.
For this tutorial we assume that you already have a local Docker installation and some basic knowledge how to use it.
**Please refere to online ressources for in depth Docker tutorials.**

To build your module container locally navigate to the folder containing all your files and run

```bash
docker build --rm -t test/apeer_test_fijimodule:latest .
```

This command tells Docker to execute a build:

* --rm = will remove intermediary containers after a successful build

* -t = specifies the name of your container

* . = docker will look for a file name *Dockerfile* and use it to build the container accordingly.

If you are running the build for the first time this may take a while because Docker needs to download the base container as well as executing all commands you specified in your dockerfile.
Once the build completed you can use the following command to display all local availabel docker containers.

```dockerfile
docker images
```

With the build completed you now have the container available and can start it locally to see if everything is working as intended. Run the container using the input specified inside the *wfe.env* file:

#### Run the module locally

You need to define a wfe.env file first, which looks like this:

```JSON
WFE_INPUT_JSON={"SCRIPT":"/Fiji.app/scripts/my_fijipyscript.py","IMAGEPATH":"/input/01_DAPI.ome.tiff","FILTERTYPE":"MEDIAN","FILTER_RADIUS":9,"WFE_output_params_file":"/output.json"}
```

**On Windows:**

```bash
docker run -it --rm -v %cd%\input:/input -v %cd%\output:/output --env-file wfe.env test/apeer_test_fijimodule:latest
```

**On Linux:**

```bash
docker run -it --rm -v ${pwd}/input:/input -v ${pwd}/output:/output --env-file wfe.env test/apeer_test_fijimodule:latest
```

* -v: docker will use a local folder and map it to a path inside the docker container. Here we are making two local folders available inside of the docker container as *\input* and *\output*.
* If all works out you should see the container starting and log output appearing on the command line. 

**Note**: One can also store all local files in one folder and map this location to the three different paths inside of the docker

**Important**: You might need to enable local file system access for the Docker client so it has permission to access the local folders (e.g Windows you need to open the "Setting > Sharing" in the Docker client and share the respective drive).

Usually the result should like this inside the terminal:

```shell
C:\Apeer_Modules\fiji_module_template_b88fae21-a305-4afb-b70b-48c18efc9fa8>docker run -it --rm -v %cd%\input:/input -v %cd%\output:/output --env-file wfe.env test/apeer_test_fijimodule:latest      
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option PermSize=128m; support was removed in 8.0
Java HotSpot(TM) 64-Bit Server VM warning: Using incremental CMS is deprecated and will likely be removed in a future release
[WARNING] Not overwriting extension 'py':
        proposed = net.haesleinhuepf.clijx.te_oki.TeOkiLanguage [file:/Fiji.app/plugins/clijx-assistant_-0.4.2.21.jar
        existing = org.scijava.plugins.scripting.jython.JythonScriptLanguage [file:/Fiji.app/jars/scripting-jython-1.0.0.jar
[WARNING] Not overwriting extension 'ijm':
        proposed = net.clesperanto.macro.interpreter.ClEsperantoMacroLanguage [file:/Fiji.app/plugins/clijx-assistant_-0.4.2.21.jar
        existing = net.imagej.legacy.plugin.IJ1MacroLanguage [file:/Fiji.app/jars/imagej-legacy-0.37.4.jar
[INFO] Overriding BIOP Run Macro...; identifier: command:ch.epfl.biop.macrorunner.B_Run_Macro; jar: file:/Fiji.app/plugins/BIOP/B_Run_Macro-1.0.0-SNAPSHOT.jar
[INFO] Overriding Get Spine From Circle Rois; identifier: command:Cirlces_Based_Spine; jar: file:/Fiji.app/plugins/Max_Inscribed_Circles-1.1.0.jar
[INFO] Overriding Batch Merge Split Chip; identifier: command:de.embl.cba.bdp2.batch.LuxendoBatchMergeSplitChipCommand; jar: file:/Fiji.app/jars/fiji-plugin-bigDataProcessor2-0.4.0.jar
[INFO] Overriding Open Multiple XML/HDF5; identifier: command:de.embl.cba.bdv.utils.viewer.OpenMultipleImagesCommand; jar: file:/Fiji.app/jars/bdv-utils-0.3.5.jar
[INFO] Overriding Visualise vector field (experimental); identifier: command:net.haesleinhuepf.clijx.piv.visualisation.VisualiseVectorFieldsPlugin; jar: file:/Fiji.app/plugins/clijx_-0.30.1.21.jar
[INFO] Overriding Print text; identifier: command:de.embl.cba.cluster.commands.PrintTextCommand; jar: file:/Fiji.app/jars/fiji-slurm-0.6.0.jar
[INFO] Starting ...
[INFO] Filename               : /input/01_DAPI.ome.tiff
[INFO] Save Format used       : ome.tiff
[INFO] ------------  START IMAGE ANALYSIS ------------
[INFO] New basename for output :/output/01_DAPI
[INFO] Image Filename : /input/01_DAPI.ome.tiff
OMETiffReader initializing /input/01_DAPI.ome.tiff
Reading IFDs
Populating metadata
[INFO] ImageCount_OME : 0
[INFO] ScaleX : 0.454
[INFO] ScaleY : 0.454
[INFO] ScaleZ : 1.0
[INFO] SeriesCount_BF : 1
[INFO] SizeC : 1
[INFO] SizeT : 1
[INFO] SizeX : 1376
[INFO] SizeY : 1104
[INFO] SizeZ : 1
[INFO] is3d : False
Reading IFDs
Populating metadata
Reading IFDs
Populating metadata
[INFO] Apply Filter  : MEDIAN
[INFO] Filter Radius : 9
[INFO] Duration of Processing : 2.2557772
[INFO] Duration of saving as OME.TIFF : 1.4881731
[INFO] Writing output JSON file ...
[INFO] Done.
```

**Now commit the complete code and push it to the repository. This will trigger a new build of your module.**


## Final Notes

This is the first version of this tutorial and it can certainly be improved. If you have suggestions or improvements please leave them in the [APEER Forum](https://forum.apeer.com/) and we will continously improve our tutorials.
