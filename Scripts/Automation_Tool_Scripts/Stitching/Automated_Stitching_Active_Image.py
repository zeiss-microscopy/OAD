#################################################################
# File       : Automated_Stitching_Active_Image.py
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

# Run Stitching automatically after acquisition

# get the active image document
image = Zen.Application.Documents.ActiveDocument

# get the stitching settings
Stitchset = r'Stitching_Channel_1.czips'

# create a function setting for the Stiching Function
functionsetting1 = Zen.Processing.Transformation.Geometric.Stitching(image)

# apply the setting
functionsetting1.Load(Stitchset)

print('Done.')
