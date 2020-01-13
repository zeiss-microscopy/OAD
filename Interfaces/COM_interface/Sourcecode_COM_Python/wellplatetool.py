#################################################################
# File       : wellplatetool.py
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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def ExtractLabels(Nr, Nc):

    # labeling schemes        
    LabelX = ['01','02','03','04','05','06','07','08','09','10','11','12',
              '13','14','15','16','17','18','19','20','21','22','23','24',
              '25','26','27','28','29','30','31','32','33','34','35','36',
              '37','38','39','40','41','42','43','44','45','46','47','48',]
    
    LabelY = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
              'Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF'] 
    
    Lx = LabelX[0:Nc]
    Ly = LabelY[0:Nr]
    
    return Lx, Ly


def ShowPlateData(data, Nr, Nc, parameter):
    
    # reshape data to create 2D matrix
    WellData = data.reshape(Nr, Nc)
    [labelx, labely] = ExtractLabels(Nr, Nc)

    # create figure
    fig = plt.figure(figsize=(6, 4), dpi=100)
    ax1 = fig.add_subplot(111)
    # set colormap
    cmap = cm.jet
    # show the well plate as an image
    cax = ax1.imshow(WellData, interpolation='nearest', cmap=cmap)
    # determine an appropriate font size
    if Nr <= 32 and Nr > 16:
        fs = 7
    elif Nr <= 16 and Nr > 8:
        fs = 9
    elif Nr <= 8:
        fs = 11
    # format the display
    ax1.set_xticks(np.arange(0, Nc, 1))
    ax1.set_xticklabels(labelx, fontsize=fs)
    ax1.set_yticks(np.arange(0, Nr, 1))
    ax1.set_yticklabels(labely, fontsize=fs)
    ax1.set_title(parameter)
    cbar = fig.colorbar(cax)
    
    #return fig


def ReturnPlateHeatmap(data, Nr, Nc):

    # reshape data to create 2D matrix
    WellData = data.reshape(Nr, Nc)
    [labelx, labely] = ExtractLabels(Nr, Nc)

    # determine an appropriate font size
    if Nr <= 32 and Nr > 16:
        fs = 7
    elif Nr <= 16 and Nr > 8:
        fs = 9
    elif Nr <= 8:
        fs = 11

    return WellData, labelx, labely, fs
