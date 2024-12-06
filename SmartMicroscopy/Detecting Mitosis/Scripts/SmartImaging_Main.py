#################################################################
# File        : Smart_Imaging.czmac
# Version     : 1.0
# Author      : czpse
# Date        : 29.11.2022
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk. Especially be aware of the fact
# that automated stage movements might damage hardware if
# one starts an experiment and the the system is not setup
# and calibrated properly. Check everything in simulation mode first!
#
# Copyright(c) 2022 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import time
import math
import os
import sys
import shutil

OVERVIEW_BASE = r"C:\Users\m1pseide\Desktop\smart imaging\input images\overview_images\magazin"
OVERVIEW_RESERVOIR = r"C:\Users\m1pseide\Desktop\smart imaging\input images\overview_images\reservoir"

hw_delay = 1

# clear console output
Zen.Application.MacroEditor.ClearMessages()
# clear zen images
Zen.Application.Documents.RemoveAll()

#### INPUT FROM USER
# check the location of experiment setups and image analysis settings are stored
doc_folder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
image_folder = r"C:\Users\m1pseide\Desktop\smart imaging\output images"

# get list with all existing experiments and image analysis setup and a short version of that list
exp_files = os.listdir(os.path.join(doc_folder, "Experiment Setups"))
analysis_files = os.listdir(os.path.join(doc_folder, "Image Analysis Settings"))

# objective names
objective_names = [Zen.Devices.ObjectiveChanger.GetNameByPosition(i+1) 
                   for i in range(Zen.Devices.ObjectiveChanger.ItemsCount)]

# Initialize Dialog
dialog = ZenWindow()
dialog.Initialize("Adaptive Imaging")

# Overview Settings
dialog.AddLabel("==========Overview Experiment Parameters=============")
dialog.AddDropDown("overview_exp", "Experiment Setting", exp_files, 4)
dialog.AddDropDown("overview_objective", "Objective", objective_names, 1)
dialog.AddDropDown("analysis_file_name", "Analysis file", analysis_files, 6)
dialog.AddTextBox("total_time", "Total time (s)", "400")
dialog.AddTextBox("overview_time_step", "Time step (s)", "60")

# Detailed Settings
dialog.AddLabel("==========Detailed Experiment Parameters=============")
dialog.AddDropDown("detailed_exp", "Experiment Setting", exp_files, 3)
dialog.AddDropDown("detailed_objective", "Objective", objective_names, 3)
dialog.AddTextBox("detailed_time_step", "Time step (s)", "20")
dialog.AddTextBox("detailed_total_scans", "Number of detailed scans", "3")

# File Storage
dialog.AddLabel("==========File Storage=============")
dialog.AddFolderBrowser("image_folder", "Base folder", image_folder)

# Display dialog
result = dialog.Show()

# Exit macro if canceled
if result.HasCanceled:
    print("Run canceled by user")
    sys.exit()

# Get the input parameters
overview_exp_name = result.GetValue("overview_exp")
overview_objective = objective_names.index(result.GetValue("overview_objective")) + 1
overview_time_step = int(result.GetValue("overview_time_step"))

analysis_file_name = result.GetValue("analysis_file_name")
total_time = int(result.GetValue("total_time"))

detailed_exp_name = result.GetValue("detailed_exp")
detailed_objective = objective_names.index(result.GetValue("detailed_objective")) + 1
detailed_time_step = int(result.GetValue("detailed_time_step"))
detailed_total_scans = int(result.GetValue("detailed_total_scans"))

image_folder = result.GetValue("image_folder")

def loadOverview(index):
    """ helper function for simulated experiments; guarantees correct feeding of overview images into acquisition.
        Not relevant for real microscopy use."""
        
    # remove all base folder images
    for file in os.listdir(OVERVIEW_BASE):
        if file.endswith(".tif"):
            os.remove(os.path.join(OVERVIEW_BASE, file))

    # load next image
    nextOverview = os.listdir(OVERVIEW_RESERVOIR)[index]
              
    shutil.copy2(src=os.path.join(OVERVIEW_RESERVOIR, nextOverview),
                 dst=os.path.join(OVERVIEW_BASE, "image.tif"))
                 
def create_time_series(image_path):
    """ creates time series out of stored detailed scan (after main loop completed)"""
    
    parent = os.path.dirname(image_path)
    file_name = os.path.basename(image_path) + ".czi"
    
    temp_images = []
    for image in os.listdir(image_path):
        temp_images.append(Zen.Application.LoadImage(os.path.join(image_path, image)))
            
    while len(temp_images) &gt; 1:
    
        image1 = temp_images.pop(0)
        image2 = temp_images.pop(0)
        
        temp_images.insert(0, Zen.Processing.TimeSeries.TimeConcat(image1, image2))
        image1.Close(), image2.Close()
        
    for image in os.listdir(image_path):
        os.remove(os.path.join(image_path, image))
        
    os.rmdir(image_path)
    temp_images[0].Save(os.path.join(parent, file_name))
    temp_images[0].Close()

def timer():
    """ little helper function for scheduling """
    return time.time() - start_time

class Experiment:

    def __init__(self, exp_id, exp_name, objective, time_step, is_overview = False, 
                 analysis_file_name = None, center_position = None):
        
        self.exp_id = exp_id
        
        self.storage_path = os.path.join(image_folder, self.exp_id) # parent path to store images
        self.counter = 0 # counter for stored images
        
        self.experiment = Zen.Acquisition.Experiments.GetByName(exp_name)
        self.is_overview = is_overview
        self.objective = objective
        
        self.time_step = time_step
        self.last_time = timer() - time_step
        
        if center_position == None:
            self.center_position = [Zen.Devices.Stage.ActualPositionX, Zen.Devices.Stage.ActualPositionY]
        else:
            self.center_position = center_position
        
        if self.is_overview:
            # initiate analysis setting
            self.analysis_setting = ZenImageAnalysisSetting()
            self.analysis_setting.Load(analysis_file_name)
            
            # list for images pending analysis
            self.images = []
            
    def acquire(self):
    
        # set proper objective and 
        self.set_objective()
        Zen.Devices.Stage.MoveTo(self.center_position[0], self.center_position[1])
        time.sleep(hw_delay) # give hardware time to adjust
    
        # execute experiment, store acquisition time
        print("acquiring...", self.exp_id, "at ", timer(), "; most recent ", self.last_time)
        self.last_time = timer()
        image = Zen.Acquisition.Execute(self.experiment)
        
        # store images in list for later image analysis (if overview image)
        if self.is_overview:
            self.images.append(image)
            # remove image from active display
            Zen.Application.Documents.Remove(image, askForSave = False)
        else:    # for detailed image, we can directly store it away
            # single image now should be saved and can be closed 
            self.save_image(image)
        
    def analyze_least_recent(self):
        """ analyzes last acquired image and returns centerX and centerY positions
            of identified objects"""
        if self.is_overview:
            image = self.images.pop(0)
            
            # Analyse image
            Zen.Analyzing.Analyze(image, self.analysis_setting)
            # Create Zen table with results for each single object
            regions_tab = Zen.Analyzing.CreateRegionTable(image)
            soi = regions_tab.GetBoundsColumnInfoFromImageAnalysis(True) # access to certain columns
            
            # object center positions in stage coordinates
            center_positions = [[regions_tab.GetValue(index, soi.CenterXColumnIndex),
                                 regions_tab.GetValue(index, soi.CenterYColumnIndex)]
                                 for index in range(regions_tab.RowCount)]
            
            # save the image
            self.save_image(image)
            
            # center_positions of identified regions is what is relevant for detailed scans
            return center_positions
    
    def close(self):
        
        self.experiment.Close()
    
    def get_acquisition_priority(self):
        return timer() - (self.last_time + self.time_step)
        
    def remove_stored_images(self):
        print("remove files from incomplete experiment...", self.exp_id)
        if os.path.exists(self.storage_path):
            # remove all base folder images
            for file in os.listdir(self.storage_path):
                os.remove(os.path.join(self.storage_path, file))
            
            os.rmdir(self.storage_path)
            
    def save_image(self, image):
    
        if not os.path.exists(self.storage_path):
            os.mkdir(self.storage_path)
            
        path = os.path.join(self.storage_path, "image_" + str(self.counter).zfill(4) + ".czi")
        print("Save image in...", path)
        image.Save(path)
        self.counter += 1
        image.Close()
        
    def set_objective(self):
        """ sets objective for overview and detailed experiments"""
        
        if not Zen.Devices.ObjectiveChanger.ActualPosition == self.objective:
            Zen.Devices.ObjectiveChanger.TargetPosition = self.objective
            Zen.Devices.ObjectiveChanger.Apply()
            
            
class DetailedExperimentContainer:

    def __init__(self, exp_name, objective, time_step, total_scans):
        
        self.exp_name = exp_name
        self.objective = objective
        self.experiments = []
        
        self.time_step = time_step
        self.total_scans = total_scans
        
        self.experiment_counter = 0 # counter to keep track of 
        
        self.distance_threshold = 10 # threshold to find existing regions
        
    def add_regions(self, center_positions):
    
        print("adding regions...")
        for position in center_positions:
            if not self.region_existing(position):
            
                experiment = Experiment(exp_id = "detailed_" + str(self.experiment_counter).zfill(4), 
                                        exp_name = self.exp_name,
                                        objective = self.objective,
                                        time_step = self.time_step, 
                                        center_position = position)
               
                self.experiments.append(experiment)
                self.experiment_counter += 1
                
        print("number of experiments", len(self.experiments))
        
    def acquire_detailed(self):
        
        # fetch experiment with least recent acquisition
        experiment = self.get_least_recent_detailed_exp()
        
        # acquire experiment
        experiment.acquire()
        print("images acquired...", experiment.counter, "from total", self.total_scans)
        
        # retire experiment if total number of scans are reached
        if experiment.counter == self.total_scans:
            print("closing experiment", experiment.exp_id)
            self.experiments.remove(experiment)
            experiment.close()
            
    def close(self):
        print("closing detailed experiment container")
        
        # erase and close experiments that remained incomplete
        for exp in self.experiments:
            exp.remove_stored_images()
            exp.close()
            
        # create time series of all valid experiments
        for folder in os.listdir(image_folder):
            if folder != "overview":
                create_time_series(os.path.join(image_folder, folder))
        
        
    def region_existing(self, position):
        """ compares position with the positions of existing detailed experiments, and returns True,
            if there is a detailed experiment within a certain vicinity, defined by self.threshold"""
            
        for exp in self.experiments: # compare with every detailed experiment
            distance = math.sqrt((exp.center_position[0] - position[0])**2 + (exp.center_position[1] - position[1])**2)
            if distance &lt; self.distance_threshold:
               print("same region:", exp.center_position, position, distance)
               return True
        
        return False
        
    def get_least_recent_detailed_exp(self):
        """ sorts the experiments by last acquisition time points and return experiment 
            with least rectent acquisition """
        
        if len(self.experiments) &gt; 0:
            self.experiments.sort(key = lambda exp : exp.last_time)
            return self.experiments[0]
            
        else:
            return None
            
    def get_max_acquisition_priority(self):
        
        # get the detailed experiment with the least recent acquisition
        experiment = self.get_least_recent_detailed_exp()
        if not experiment == None:
            # return time difference between expected acquisition and current time
            return experiment.get_acquisition_priority()
        else:
            return 0

#### MAIN STARTING NOW #####

### parameters to control the loop flow
start_time = time.time() # to measure rounds of acquisition, both overview and detailed; in seconds

### INITIALIZE EXPERIMENT OBJECTS
# experiment objects
overview_exp = Experiment(exp_id = "overview",
                          exp_name = overview_exp_name, 
                          objective = overview_objective, 
                          time_step = overview_time_step,
                          is_overview = True,
                          analysis_file_name=analysis_file_name) 

detailed_con = DetailedExperimentContainer(exp_name = detailed_exp_name, 
                                           objective = detailed_objective, 
                                           time_step = detailed_time_step, 
                                           total_scans = detailed_total_scans)


### MAIN LOOP
while timer() &lt; total_time:

    #algorithm should decide whether overview or detailed scan are more urgent
    overview_priority = overview_exp.get_acquisition_priority()
    detailed_priority = detailed_con.get_max_acquisition_priority()
    
    # is any acquisition urgent?
    if overview_priority &gt; 0 or detailed_priority &gt; 0:
        if overview_priority &gt; detailed_priority: # run overview acquisition
            loadOverview(overview_exp.counter) # helper function for loading images in simulated experiment
            overview_exp.acquire()
        
        else: # run detailed acquisition
            detailed_con.acquire_detailed() # acquires the most urgent detailed experiment
            
    elif len(overview_exp.images) &gt; 0: # acquisition not urgent; let's analyze the least recent overview, if new image available
        
        ### ANALYZE LAST OVERVIEW IMAGE
        print("analyzing overview at...", timer())
        center_positions = overview_exp.analyze_least_recent()
        
        # add newly identified regions to detailed scan container
        detailed_con.add_regions(center_positions)
        
        
### THINGS TO DO TO FINISH THE RUN
detailed_con.close()
print("closing overview experiment")
overview_exp.close()
