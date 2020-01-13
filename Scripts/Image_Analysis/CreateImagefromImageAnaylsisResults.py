#################################################################
# File       : CreateImagefromImageAnalysisResults.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# define the image file location here
imagefile = r'c:\Zen_Output\Count_Cells_DAPI_10_Frames.czi'

# this the the CZIAS created by the Image Analyis Wizard or manually
iasname = 'Count_Cells_DAPI.czias'

# Load analysis setting
ias = ZenImageAnalysisSetting()
ias.Load(iasname, ZenImageAnalysisSettingDirectory.User)
# Load image automatically
image = Zen.Application.LoadImage(imagefile, False)
Zen.Analyzing.Analyze(image, ias)
Zen.Application.Documents.Add(image)

# Choose your desired labeling method --&gt; there are more --&gt; try type ZenAnalyzerLabelImageMode. and use Intellisense
LabelMethods = {'10': ZenAnalyzerLabelImageMode.Contour2Class,
                '11': ZenAnalyzerLabelImageMode.Contour2ClassColor,
                '13': ZenAnalyzerLabelImageMode.Contour2Label,
                '14': ZenAnalyzerLabelImageMode.Contour2Unique,
                '15': ZenAnalyzerLabelImageMode.Contour2UniqueColor,
                '4': ZenAnalyzerLabelImageMode.RegionClass,
                '5': ZenAnalyzerLabelImageMode.RegionClassColor,
                '2': ZenAnalyzerLabelImageMode.RegionUnique,
                '3': ZenAnalyzerLabelImageMode.RegionUniqueColor}

# select method here
labelmethod = '3'

# Create an image with objects and label them with the selcted method
out = ZenImage()
Zen.Analyzing.AnalyzeToImage(image, out, ias, LabelMethods[labelmethod], ZenAnalyzerLabelImageInitMode.Default, ZenPixelType.Bgr24)
Zen.Application.Documents.Add(out)

# use the name of the original channel for the result
chName = image.Metadata.ChannelsText
# set channelname for output image
out.SetChannelName(0, chName)
