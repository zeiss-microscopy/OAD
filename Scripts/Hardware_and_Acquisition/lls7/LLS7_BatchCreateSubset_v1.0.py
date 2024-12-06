#################################################################
# File       : LLS7_BatchCreateSubset.czmac
# Version    : 1.0
# Author     : aukelgas
# Date       : 13.04.2023
# Institution : Carl Zeiss Microscopy GmbH
#
# Use at your own Risk !!!
# Compatible with ZEN versions 3.7 and higher
#
#################################################################

from System.IO import File, Directory, Path
import xml.etree.ElementTree as ET
import os

# version number for dialog window
version = 1.0

# clear console output
Zen.Application.MacroEditor.ClearMessages()

# define default folders
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
graphfolder = 'D:\zeiss\Documents\Carl Zeiss\ZEN\Documents\Graphics'

# Initialize Dialog
Dialog = ZenWindow()
Dialog.AddFolderBrowser('imgfolder', '    Select Folder with Images to Subset', imgfolder)
#Dialog.AddFolderBrowser('graphfolder', '    Select Folder with Graphics Files', graphfolder)

# show the window
result = Dialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
imgfolder = str(result.GetValue('imgfolder'))

# get list of files to fuse
filelist = os.listdir(imgfolder)
filelist = [i for i in filelist if i.endswith('.czi') and not i.endswith('_MIP.czi')]

OutputFolder = str(imgfolder + "\Subsets")
Directory.CreateDirectory(OutputFolder)
print('---------------')
print(('Created new directory: ', OutputFolder))
print('---------------')

for j in range (0, len(filelist)):
    imgname = Path.Combine(imgfolder, filelist[j])
    print(imgname)
    Img = Zen.Application.LoadImage(imgname, False)
    basename = filelist[j][:-4]

    # get ROIs from graphics files
    xmlfile = 'D:/zeiss/Documents/Carl Zeiss/ZEN/Documents/Graphics/' + basename + '.cz'
    #print(xmlfile)
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    for child in root.findall('.//Rectangle'):
        ID = child.get('Id')
        print(("Processing ROI " + ID))
    
        SizeZ = Img.Bounds.SizeZ
        SizeY = Img.Bounds.SizeY
        PixelSizeZ = Img.Scaling.Z*1000
        
        GT = int(round(float(root.find(".//*[@Id='"+ID+"']/Geometry/Top").text)))
        GL = int(round(float(root.find(".//*[@Id='"+ID+"']/Geometry/Left").text)))
        GW = int(round(float(root.find(".//*[@Id='"+ID+"']/Geometry/Width").text)))
        GH = int(round(float(root.find(".//*[@Id='"+ID+"']/Geometry/Height").text)))
        GB = GT + GH
        
        Z1 = (SizeZ-1)*PixelSizeZ/145+0.5*SizeY*0.866
        Z2 = 0.5*SizeY*0.866
        
        m = (SizeZ-1)/(Z2-Z1)
        b = 1 - Z1 * m
        
        ZS = int(round(m*(GL+0.5*GW)+b)-GW)   # 0.69 is 100nm (deskewed) / 145nm (cover glass transformed)
        ZE = int(round(m*(GL+0.5*GW)+b)+GW)
        
        SubParameter = 'X('+str(GT)+'-'+str(GB)+')|Z('+str(ZS)+'-'+str(ZE)+')'   # NOTE: in non-deskewed data sets, Y is Y on the camera chip, Z is Range X of the volume scan
        #SubParameter = 'X('+str(GT)+'-'+str(GB)+')'
        SubImage = Zen.Processing.Utilities.CreateSubset(Img, SubParameter)
        Zen.Application.Documents.Add(SubImage)
        SubImage.Save(Path.Combine(OutputFolder, filelist[j][:-4] + '_Subset'+str(ID)+'.czi'))
        Zen.Application.Documents.ActiveDocument.Close()

