#################################################################
# File       : Automated_Apotome_Processing.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

# Run ApoTome Processing automatically after acquisition

Outputfolder = r'C:\\ZEN_Output'

# Read Active Image &amp; prepare Output Image

image = Zen.Application.Documents.ActiveDocument

# Process ApoTome Active Raw Image

nb_phase = image.Bounds.SizeH
apotome_image = Zen.Processing.Utilities.ApoTomeSimConvert(image,
                                                           ZenApoTomeProcessingMode.Sectioned,
                                                           ZenSimCorrectionMode.LocalIntensity,
                                                           ZenNormalizeMode.Clip,
                                                           ZenApoTomeFilter.Off,
                                                           False)

# add newly create image to the document area
Zen.Application.Documents.Add(apotome_image)

# Save Processed file
image_name = image.Name.Replace('.czi', '_Apotome.czi')
imageName = Path.Combine(Outputfolder, image_name)
apotome_image.Save(imageName)

print('Done.')
