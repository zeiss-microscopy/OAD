#################################################################
# File       : GA_time_concat.py
# Version    : 1.1
# Author     : czpse
# Date       : 15.05.2025
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# This macro can be used to automatically concatenate single
# time frames from a time-lapse Guided Acquisition. Make sure,
# all single time frame images are contained within one folder,
# and select this folder in the dialog window.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import os
import clr

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import FolderBrowserDialog, DialogResult

########## INPUT FROM USER #######################################

folder_dialog = FolderBrowserDialog()
folder_dialog.Description = "Please select folder containing detailed scans"
folder_dialog.UseDescriptionForTitle = True

result = folder_dialog.ShowDialog()

if result != DialogResult.OK:
    print("Cancelled")
    sys.exit()

parent_folder = folder_dialog.SelectedPath


################# FUNCTIONS ################################

def extractID(filename):
    """ logic to extract image ID; including Well Plate identifiers"""

    filename = filename.split("_")

    if len(filename) == 3:  # experiment not done in wells
        return filename[1]

    if len(filename) == 5:  # experiment done in wells
        filename[2] = filename[2][:1] + filename[2][1:].zfill(2)
        return "_".join(filename[1:4])

    raise Exception("Filename not correctly identified")


def filterDetailedScans(filelist):
    output_list = []

    # go through file list, test for correct file format and filter out overview scans
    for file in filelist:

        if not file.endswith("czi"):
            continue

        if not "DTScan" in file:
            continue

        output_list.append(file)

    return output_list


def loadImageSet(parent, filelist):
    loaded_images = []

    for image_name in filelist:
        abs_path = os.path.join(parent, image_name)
        loaded_images.append(Zen.Application.LoadImage(abs_path))

    return loaded_images


def sortScans(filelist):
    scan_dictionary = {}

    for filename in filelist:

        scanID = extractID(filename)

        if scanID in scan_dictionary:
            scan_dictionary[scanID].append(filename)
        else:
            scan_dictionary[scanID] = [filename]

    return scan_dictionary


def time_concat(image_list):
    while len(image_list) > 1:
        # pop first two images from list
        image1 = image_list.pop(0)
        image2 = image_list.pop(0)

        # combine two images
        image_new = Zen.Processing.TimeSeries.TimeConcat(image1, image2)

        # close input images
        image1.Close()
        image2.Close()

        # re-insert new image in beginning of list
        image_list.insert(0, image_new)

    return image_list[0]


############# MAIN LOOP ########################################

# list all files in specified folder
file_list = os.listdir(parent_folder)
# filter out all files other than detailed scans
file_list = filterDetailedScans(file_list)

# sort scans based on identifiers
scan_dictionary = sortScans(file_list)

for scanID in scan_dictionary.keys():
    image_path_list = scan_dictionary[scanID]  # load list with image names

    image_path_list.sort()  # sort path list

    image_list = loadImageSet(parent_folder, image_path_list)  # load images

    image = time_concat(image_list)

    image.Save(os.path.join(parent_folder, "{}.czi".format(scanID)))

    image.Close()

