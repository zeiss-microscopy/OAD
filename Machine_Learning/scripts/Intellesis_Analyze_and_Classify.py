#################################################################
# File        : Intellesis_Analyze_and_Classify.py
# Version     : 0.2.0
# Author      : czsrh
# Date        : 05.03.2021
# Institution : Carl Zeiss Microscopy GmbH
#
# Workflow Description
# -----------------------
# 
# 1 - Select the Image to be analyzed from open documents
# 2 - Select the CZIAS to be used for the image analysis
# 3 - Select the CZTOC object classification model (must macth one IA class name)
# 4 - Select the folder for the exported tables
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk.
#
# Copyright (c) 2021 Carl Zeiss AG, Germany. All Rights Reserved.
#
#################################################################

from System.IO import File, Directory, Path
import time
from datetime import datetime
import errno
from System import Array
from System import ApplicationException
from System import TimeoutException
import sys
from collections import *
clr.AddReference('System.Xml')
import System.Xml


class objclassmodel:
    def __init__(self, objmodelfile):

        # get the XMLdoc based on the actual model XML-file
        self.objmodelfile = objmodelfile
        self.modelxmldoc = System.Xml.XmlDocument()
        self.modelxmldoc.Load(objmodelfile)
        self_objmodel_name = None
        self.objmodel_id = None
        self.objmodel_regionclass = None
        self.objmodel_classnames = []
    
    # get name of object classification model
    def getobjmodelname(self):
        nodes = self.modelxmldoc.SelectNodes('ObjectClassificationModel/ModelName')
        for node in nodes:
            self.objmodel_name = node.InnerText
            
        return self.objmodel_name
        
    # get the ID of the object classification model
    def getobjmodelid(self):
        nodes = self.modelxmldoc.SelectNodes('ObjectClassificationModel/Id')
        for node in nodes:
            self.objmodel_id = node.InnerText

        return self.objmodel_id
        
    # get the name of the region class from IA to be classified by the model
    def getobjmodelregionclass(self):
        nodes = self.modelxmldoc.SelectNodes('ObjectClassificationModel/RegionClass')
        for node in nodes:
            self.objmodel_regionclass = node.InnerText
    
        return self.objmodel_regionclass
        
    # get the name of the object classes created by the model
    def getobjmodelclassnames(self):
        nodes = self.modelxmldoc.SelectNodes('ObjectClassificationModel/ObjectClasses')
        for node in nodes:
            for c in node.ChildNodes:
                self.objmodel_classnames.append(c.GetAttributeNode('Name').Value)
    
        return self.objmodel_classnames


def is_empty(any_structure):
    """Check if a "structure" might be empty

    :param any_structure: input structure
    :type any_structure: 
    :return: Boolean, depending on if the structure was empty or not
    :rtype: bool
    """
    # check is a structure is empty
    if any_structure:
        return False
    else:
        return True


def createfolder(basedir, formatstring='%Y-%m-%d_%H-%M-%S'):
    # construct new directoty name nased on date and time
    newdir = Path.Combine(basedir, datetime.now().strftime(formatstring))
    # check if the new directory (for whatever reasons) already exists
    try:
        newdir_exists = Directory.Exists(newdir)
        if not newdir_exists:
            # create new directory if is does not exist
            Directory.CreateDirectory(newdir)
        if newdir_exists:
            # raise error if it really already exists
            raise SystemExit
    except OSError as e:
        if e.errno != errno.EEXIST:
            newdir = None
            raise  # This was not a "directory exist" error..

    return newdir


def dircheck(basefolder):

    # check if the destination basefolder exists
    base_exists = Directory.Exists(basefolder)

    if base_exists:
        print('Selected Directory Exists: ', base_exists)
        # specify the desired output format for the folder, e.g. 2017-08-08_17-47-41
        format = '%Y-%m-%d_%H-%M-%S'
        # create the new directory
        newdir = createfolder(basefolder, formatstring=format)
        print('Created new directory: ', newdir)
    if not base_exists:
        Directory.CreateDirectory(basefolder)
        newdir = basefolder

    return newdir


def getshortfiles(filelist):
    files_short = []
    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short


def getclassnames(ias):

    # create empty dictionary
    iaclasses = {}
    # define root class, which is always there
    iaclasses['0'] = 'Root'
    classnames = ias.GetRegionClassNames()
    numclasses = len(classnames)

    for id in range(1, numclasses):
        try:
            cl = ias.GetRegionClass(id)
        except:
            cl = ias.GetRegionsClass(id)

        iaclasses[str(cl.ID)] = cl.Name
        print('ID - ClassName: ', cl.ID, cl.Name)

    return iaclasses


def run_analysis(image, iasname):

    # load analysis setting and analyze the image
    ias = ZenImageAnalysisSetting()
    ias.Load(iasname, ZenImageAnalysisSettingDirectory.User)
    Zen.Analyzing.Analyze(image, ias)

    return image


def create_table_all_objects(analyzed_image, savetable=False,
                                             savefolder=r'c:\temp'):

    # Create Zen table with results for all detected objects (parent class)
    all_obj = Zen.Analyzing.CreateRegionsTable(analyzed_image)

    if savetable:
        # save data table to the specified folder
        all_obj.Save(Path.Combine(savefolder, 'objects_all.csv'))

    return all_obj


def create_table_single_objects(analyzed_image, savetable=False,
                                                savefolder=r'c:\temp'):

    # Create Zen table with results for each single object
    single_obj = Zen.Analyzing.CreateRegionTable(analyzed_image)
    
    if savetable:
        # show and save data tables to the specified folder
        single_obj.Save(Path.Combine(savefolder, 'objects_single.csv'))

    return single_obj


def find_objclassmodel(name):
    """ Finds an object classifier model given its Name.

    Arguments:
        name: string
              The name of the object classifier model to look for.

    Returns: IZenIntellesisObjClassModel
             The first object classifier model with the specified name
             or None, if no such model exists.
    """
    objclass_models = ZenIntellesis.ObjectClassification.ListAvailableModels()
    
    return next((m for m in objclass_models if m.Name == name), None)

##############################################################################################################

# default folder for output
default_folder = r'c:\Temp\output'

# clear output console
Zen.Application.MacroEditor.ClearMessages()

CZIfiles_short = []
CZIdict = {}

# get all open documents
opendocs = Zen.Application.Documents
for doc in opendocs:
    image = Zen.Application.Documents.GetByName(doc.Name)

    if image.FileName.EndsWith('.czi'):
        # get the filename of the current document only when it ends with '.czi'
        CZIfiles_short.append(Path.GetFileName(image.FileName))
        CZIdict[Path.GetFileName(image.FileName)] = image.FileName

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
format = '%Y-%m-%d_%H-%M-%S'

# get list with all existing image analysis setups and a short version of that list
ipfiles = Directory.GetFiles(Path.Combine(docfolder, 'Image Analysis Settings'), '*.czias')
ipfiles_short = getshortfiles(ipfiles)

# get list with all existing models and a short version of that list
objmodelfolder = Path.Combine(docfolder, 'ObjectClassificationModels')
objmodelfiles = Directory.GetFiles(objmodelfolder, '*.xml')

if is_empty(objmodelfiles):
    # catch exception in case the folder contains no models at all
    message = 'No modelfiles found in specified folder: '
    print(message, objmodelfolder)
    raise SystemExit

# get the list of filename use only the basefilename
objmodelfiles_short = getshortfiles(objmodelfiles)

objmodel_dict_regionclass = {}
objmodel_dict_objclass = {}

for objmodelfile in objmodelfiles:
    
    # initialize new objclassmodel
    myobjmodel = objclassmodel(objmodelfile)
    
    # get information about the selected model
    model_name = myobjmodel.getobjmodelname()
    objmodel_dict_regionclass[model_name] = myobjmodel.getobjmodelregionclass()
    objmodel_dict_objclass[model_name] = myobjmodel.getobjmodelclassnames()

# get all available object classification models
tocmodels = ZenIntellesis.ObjectClassification.ListAvailableModels()
tocmodel_list = []

for tocmodel in tocmodels:
    tocmodel_list.append(tocmodel.Name)

# sort the list
tocmodel_list.sort()

# Initialize Dialog
iac = ZenWindow()
iac.Initialize('Intellesis - Analyze and Classify - Version : 0.2.0')

# add components to dialog
iac.AddLabel('1) Select Image Document  -------------------------------------------')
iac.AddDropDown('czi', 'Select CZI Image Document', CZIfiles_short, 0)
iac.AddLabel('2) Select Image Analysis to detect objects  -------------------------')
iac.AddDropDown('ip_pipe', 'Image Analysis Pipeline', ipfiles_short, 0)
iac.AddLabel('3) Select Object Classifier Model  ----------------------------------')
iac.AddDropDown('tocmodel', 'Object Classification Model', tocmodel_list, 0)
iac.AddCheckbox('append', 'Append Features used for Classification', False)
iac.AddLabel('4) Results Tables  --------------------------------------------------')
iac.AddCheckbox('saveresults', 'Save Data as CSVs', False)
iac.AddFolderBrowser('outfolder', 'Savefolder Location', default_folder)

# show the window
result = iac.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
cziname = result.GetValue('czi')
czidocument = CZIdict[cziname]
toc_modelname = str(result.GetValue('tocmodel'))
append_features = result.GetValue('append')
iasname = str(result.GetValue('ip_pipe'))
savetables = result.GetValue('saveresults')
savefolder = str(result.GetValue('outfolder'))

# check directory and create if not existing
savefolder = dircheck(savefolder)

# get the active CZI image document
# get the active image document
image = Zen.Application.Documents.GetByName(cziname)
Zen.Application.Documents.ActiveDocument = image

# run the image analysis
image = run_analysis(image, iasname=iasname)

# run the object classification on the analyzed image
# select a specific model
myobjmodel = find_objclassmodel(toc_modelname)
print('Use model:', myobjmodel.Name)
print('Model - RegionClass    : ', objmodel_dict_regionclass[toc_modelname])
print('Model - Object Classes : ', objmodel_dict_objclass[toc_modelname])

# classify an analyzed image (inplace)
myobjmodel.Classify(image, appendFeatures=append_features)
image.Save()

if savetables:
    print('Saving DataTables as CSV to folder: ', savefolder)

# export the tables from the analyzed and classified image
table_all_obj = create_table_all_objects(image, savetable=True, savefolder=savefolder)
table_single_obj =  create_table_single_objects(image, savetable=True, savefolder=savefolder)

# add table to ZEN document area
Zen.Application.Documents.Add(table_all_obj)
Zen.Application.Documents.Add(table_single_obj)


