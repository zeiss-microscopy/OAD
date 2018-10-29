# -*- coding: utf-8 -*-
"""
File: RunZenfromPython.py
Date: 03.05.2017
Author: Sebastian Rhode
Version: 1.1

This Python script demonstrates the capabilities of the .COM interface
to establish a connection between ZEN Blue and Python.
This connection allows to use ZEN Blue OAD Simple-API objects from
within a python script.

Requirements:
    
- bftools.py, czitools.py, misctooly.py
- tifffile
- czifile.py
- mahotas
"""

import win32com.client
import os
import ReadAnalyzeImageData as rad

# Define place to store the CZI file
savefolder = 'C:\\Python_ZEN_Output\\'
# check if the folder already exists
try:
    os.makedirs(savefolder)
except OSError:
    if not os.path.isdir(savefolder):
        raise

# Import the ZEN OAD Scripting into Python
Zen = win32com.client.GetActiveObject("Zeiss.Micro.Scripting.ZenWrapperLM")

# Define the experiment to be executed
ZEN_Experiment = "ML_96_Wellplate_Castor.czexp"

# run the experiment in ZEN and save the data to the specified folder
exp = Zen.Acquisition.Experiments.GetByName(ZEN_Experiment)
img = Zen.Acquisition.Execute(exp)

# Show the image in ZEN
Zen.Application.Documents.Add(img)

# Use the correct save method - it is polymorphic ... :)
filename = savefolder + img.Name_2
img.Save_2(filename)

# get the actual CZI image data using Python wrapper for BioFormats
img6d = rad.ReadImage(filename)

# Analyze the images - Example: Count Cells
obj, labeled = rad.CountObjects(img6d)

# Display some data
rad.DisplayData_2(obj, labeled)