#################################################################
# File        : czmac2python.py
# Author      : sebi06
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2024 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import lxml.etree as ET
from pathlib import Path
import os
from shutil import rmtree


def get_script(filename):

    try:
        # get the tree and find the script
        tree = ET.ElementTree(file=filename)
        root = tree.getroot()

        # get the actual text
        script = tree.find("Text").text
    except OSError as e:
        print("Could not read file: ", filename, e)
        script = None

    return script


# define the parent directory
parent_directory = (
    r"C:\Users\m1srh\OneDrive - Carl Zeiss AG\Tools_Backups\Backup_ZEN_Macros\Macros_py"
)

# get all file paths
paths = Path(parent_directory).glob("**/*.czmac")

# loop over all file paths
for path in paths:

    # because path is object not string - convert it
    print("Converting: ", str(path))

    # get the python script as text
    script = get_script(str(path))

    if script is not None:
        # extract the filename and and the correct extension
        filename_py = os.path.splitext(str(path))[0] + ".py"

        # write the actual script to a *.py file
        with open(filename_py, "w") as file:
            file.write(script)

        # close the file
        file.close()

        # remove the *czmac files
        if path.is_file():
            path.unlink()
            print("Removed File: ", str(path))
        elif path.is_dir():
            rmtree(path)
            print("Removed Directory: ", str(path))

    if script is None:
        print("Problem with File: ", path)

print("Done.")
