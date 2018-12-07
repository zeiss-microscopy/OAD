#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################################
# File       : XYZ
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Insitution :
#
# Extract the python script from ZEN OAD macro or the Feedback Scripts from ZEN Experiments.
# Can be used on single files or on a complete folder.
#
# Usage:
#
# C: \mydir > extract_script - f experiment.czexp - -> experiment.py
# C: \mydir > extract_script - f oadmacro.czmac - -> oadmacro.py
# C: \mydir > extract_script - f mydir\experiment_and_macros - -> loops over all files
#
# !!! Attention: It does overwrite existing * .py files inside that directory !!!
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
################################################################################################


import argparse
import os
import xml.etree.cElementTree as ET


def read_experiment(filename):
    """
    Extract the experiment Feedback Script from ZEN experiment file: *.czexp
    :param filename: 
    :return: script_complete
    """

    tree = ET.ElementTree(file=filename)
    print(filename)
    pre = tree.find('./ExperimentFeedback/PreScript')
    loop = tree.find('./ExperimentFeedback/LoopScript')
    post = tree.find('./ExperimentFeedback/PostScript')

    script = [None] * 3
    script[0] = pre.text
    script[1] = loop.text
    script[2] = post.text

    for i in range(0, 3, 1):
        if (script[i] == None):
            script[i] = ""

    spacer1 = "### -------------------- PreScript ---------------------------------------------- ###\n\n\n"
    spacer2 = "\n\n\n### -------------------- LoopScript --------------------------------------------- ###\n\n\n"
    spacer3 = "\n\n\n### -------------------- PostScript --------------------------------------------- ###\n\n\n"

    script_complete = spacer1 + script[0] + spacer2 + script[1] + spacer3 + script[2]

    return script_complete


def read_macro(filename):
    """
    Extract the experiment Feedbackl Script from ZEN experiment file: *.czmac
    :param filename: 
    :return: pyscript
    """
    print(filename)
    tree = ET.ElementTree(file=filename)
    pyscript = tree.find('Text')

    return pyscript.text


def writefile(filename):
    """
    Write extracted data to python script inside the same directory
    :param filename: 
    :return: newfilename
    """

    basename_woext = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    print('Detected Extension: ', extension)
    newfilename = basename_woext + '.py'
    print('New filename: ', newfilename)

    if extension == '.czexp':
        content = read_experiment(filename)
    elif extension == '.czmac':
        content = read_macro(filename)

    with open(newfilename, 'w+') as f:
        f = open(newfilename, 'w+')
        f.write(content)
        f.close()

    return newfilename


def process_dir(dirname):
    """
    Loop over all files inside the directory
    :param dirname: 
    :return: None
    """

    for fn in os.listdir(dirname):
        file2process = os.path.join(dirname, fn)
        print('Processing File: ', file2process)

        # only process *.czexp or *.czmac files
        extension = os.path.splitext(file2process)[1]
        if extension == '.czexp' or extension == '.czmac':
            writefile(file2process)
        else:
            print('Skipping File: ', file2process)


# --------------------------------------------------------------------------

# setup commandline parameters
parser = argparse.ArgumentParser(description='Read Filename or Directory.')
parser.add_argument('-f', action='store', dest='name')

# get the arguments
args = parser.parse_args()

file_or_dir = args.name
print(type(file_or_dir))
# remove quotation marks in case they were used from the command line
name = file_or_dir.replace('"', '')

# check if argument is a file or directory and process
if os.path.isdir(name):
    print('Detected Directory: ', name)
    process_dir(name)

elif os.path.isfile(name):
    print('Detected File: ', name)
    # convert the Feedback Script or ZEN Macro to Python script
    newfilename = writefile(name)
    print('Converted: ', name, ' to: ', newfilename)
