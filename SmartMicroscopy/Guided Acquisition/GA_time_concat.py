

#################################################################
# File       : GA_time_concat.py
# Version    : 1.0
# Author     : czpse
# Date       : 15.05.2025
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# This macro can be used to automatically concatenate single 
# time frames from a time-lapse Guided Acquisition. Make sure,
# all single time frame images are contained within one folder,
# and set the path to the folder in the macro ("parent_folder").
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import os

# folder with detailed scans; make sure folder doesnt contain other data;
parent_folder = r"[Absolute path to folder]"

def extractID(filename, indexStart, indexEnd):
    """ logic to extract image ID; including Well Plate identifiers"""
    
    filename = filename.split("_")[indexStart:indexEnd]
    
    wellRow = filename[1][:1]
    wellColumn = filename[1][1:].zfill(2)
    
    filename[1] = wellRow + wellColumn
    
    return "_".join(filename)

def loadImageSet(parent, image_set):

    loaded_images = []
    
    for image_name in image_set:
        
        abs_path = os.path.join(parent, image_name)
        loaded_images.append(Zen.Application.LoadImage(abs_path))
        
    return loaded_images      

def sortScans(image_list):
    
    scan_dictionary = {}
    
    for image in image_list:
        
        scanID = extractID(image, 1, 4)
        
        if scanID in scan_dictionary:
            scan_dictionary[scanID].append(image)
        else:
            scan_dictionary[scanID] = [image]
            
    return scan_dictionary
    
def time_concat(image_list):

    while len(image_list) &gt; 1:
    
        # pop first two images from list
        image1 = image_list.pop(0)
        image2 = image_list.pop(0)
        
        # combine two images
        image_new = Zen.Processing.TimeSeries.TimeConcat(image1, image2)
        
        # re-insert new image in beginning of list
        image_list.insert(0, image_new)
    
    return image_list[0]


### MAIN LOOP ####

image_path_list = os.listdir(parent_folder)
scan_dictionary = sortScans(image_path_list)

for ID in scan_dictionary.keys():
    
    image_path_list = scan_dictionary[ID] # load list with image names
    
    image_path_list.sort() # sort path list
   
    image_list = loadImageSet(parent_folder, image_path_list) # load images

    image = time_concat(image_list)
    
    image.Save(os.path.join(parent_folder, "{}.czi".format(ID)))
    
    image.Close()
