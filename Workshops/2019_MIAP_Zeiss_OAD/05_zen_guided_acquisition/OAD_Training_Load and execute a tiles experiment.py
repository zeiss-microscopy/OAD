#######################################################
## A C Q U I S I T I O N 
##
## Macro name: Load and execute a TILES experiment
## Required files: MyTiles.czexp
## Required hardware: camera, microscope, scanningstage
##
## LOAD EXPERIMENT, EXECUTE EXPERIMENT,  DISPLAY AND SAVE ACQUIRED IMAGE AUTOMATICALLY
## (2x2 tiles of the scanningstage)
## 
#######################################################
##

from System.IO import File, Directory, FileInfo, Path


## Remove all open images
Zen.Application.Documents.RemoveAll()
##
## Define experiment
exp = ZenExperiment()


## Load experiment
exp.Load("OAD_Training_Exp",ZenSettingDirectory.User)
## Execute experiment, display acquired image
## Image is saved automatically in temp folder of AutoSavePath of Saving tab of Tools/Options menu
image = Zen.Acquisition.Execute(exp)

#get image name
img_filename = image.FileName
finfo = FileInfo(img_filename)
img_name = finfo.Name


## save image
path = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
fullPath = path + '\\' + img_name
image.Save(fullPath)

## Close image 
image.Close()
##
#######################################################
