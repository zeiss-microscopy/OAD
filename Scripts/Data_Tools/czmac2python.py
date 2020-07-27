#################################################################
# File       : czmac2python.py
# Version    : 0.2
# Author     : czsrh
# Date       : 27.07.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import lxml.etree as ET
from pathlib import Path
import os
from shutil import rmtree


def get_script(filename):
    """Extract the script text from a *.czmac file, which is an xml file.

    :param filename: filename of the *.czmac file
    :type filename: str
    :return: text of the actual script
    :rtype: str
    """

    try:
        # get the tree and find the script
        tree = ET.ElementTree(file=filename)
        root = tree.getroot()

        # get the actual text
        script = tree.find('Text').text
    except OSError as e:
        print('Could not read file: ', filename, e)
        script = None

    return script


# define the parent directory - do a backup before running the script !
parent_directory = r'C:\Users\Public\Documents\Carl Zeiss\ZEN\Documents\Macros'

# get all file paths ending with *.czmac
paths = Path(parent_directory).glob('**/*.czmac')

# loop over all file paths
for path in paths:

    # because path is object not string - convert it
    print('Converting: ', str(path))

    # get the python script as text
    script = get_script(str(path))

    if script is not None:
        # extract the filename and and the correct extension
        filename_py = os.path.splitext(str(path))[0] + '.py'

        # write the actual csript to a *.py file
        with open(filename_py, 'w') as file:
            file.write(script)

        # close the file
        file.close()

        # remove the *czmac files
        if path.is_file():
            path.unlink()
            print('Removed File: ', str(path))
        elif path.is_dir():
            rmtree(path)
            print('Removed Directory: ', str(path))

    if script is None:
        print('Problem with File: ', path_in_str)

print('Done.')
