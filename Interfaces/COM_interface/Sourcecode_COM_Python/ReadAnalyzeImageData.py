#################################################################
# File       : ReadAnalyzeImageData.py
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

from matplotlib import pyplot as plt, cm
import numpy as np
import mahotas
import wellplatetool as wp
import sys
import bftools as bf


def ReadImage(filename):

    urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'
    # specify bioformats_package.jar to use if required
    bfpackage = r'c:\Users\M1SRH\Documents\Software\BioFormats_Package\5.4.1\bioformats_package.jar'
    bf.set_bfpath(bfpackage)

    # get image meta-information
    MetaInfo = bf.get_relevant_metainfo_wrapper(filename, namespace=urlnamespace, bfpath=bfpackage, showinfo=False)
    img6d, readstate = bf.get_image6d(filename, MetaInfo['Sizes'])

    # show relevant image Meta-Information
    bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage)

    return img6d


def CountObjects(img6d):

    obj = np.zeros(img6d.shape[0])

    print('Start Processing ...',)
    steps = img6d.shape[0]/10

    # count cells with individual thresholds per frame
    for i in range(0, img6d.shape[0], 1):

        img = img6d[i, 0, 0, 0, :, :]
        T = mahotas.otsu(img)
        img = (img > T)
        img = mahotas.gaussian_filter(img, 0.5)
        labeled, numobjects = mahotas.label(img)
        obj[i] = numobjects
        if i % steps == 0:
            print('\b.',)
            sys.stdout.flush()

    print('Done!',)

    return obj, labeled


def DisplayData_1(obj, labeled):

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    cax = ax1.matshow(labeled, interpolation='nearest', cmap=cm.jet)
    cbar = fig1.colorbar(cax)
    ax1.set_title('Example - Labeled Objects')
    ax1.set_xlabel('X-dimension [pixel]')
    ax1.set_ylabel('Y-dimension [pixel]')

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.hist(obj, normed=0, facecolor='green', alpha=0.75)
    ax2.set_title('Distribution - Number of Objects')
    ax2.set_xlabel('Number')
    ax2.set_ylabel('Occurence')
    ax2.grid(True)

    wp.ShowPlateData(obj, 8, 12, 'Object Number')

    # show plots
    plt.show()


def DisplayData_2(obj, labeled):

    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax1 = fig.add_subplot(221)
    ax1.hist(obj, normed=0, facecolor='green', alpha=0.75)
    ax1.set_title('Distribution - Number of Objects')
    ax1.set_xlabel('Number')
    ax1.set_ylabel('Occurence')
    ax1.grid(True)

    ax2 = fig.add_subplot(222)
    ind = np.arange(obj.shape[0])
    ax2.bar(ind, obj, width=0.8, color='r')
    ax2.set_title('Follow Acquisition')
    ax2.set_ylabel('Number')
    ax2.set_xlim(0, obj.shape[0])
    ax2.grid(True)

    ax3 = fig.add_subplot(223)
    Nc = 12
    Nr = 8
    WellData, labelx, labely, fs = wp.ReturnPlateHeatmap(obj, Nr, Nc)
    cax = ax3.imshow(WellData, interpolation='nearest', cmap=cm.jet)
    cbar = fig.colorbar(cax)
    ax3.set_title('Objects per Well')
    ax3.set_xticks(np.arange(0, Nc, 1))
    ax3.set_xticklabels(labelx, fontsize=fs)
    ax3.set_yticks(np.arange(0, Nr, 1))
    ax3.set_yticklabels(labely, fontsize=fs)

    ax4 = fig.add_subplot(224)
    cax = ax4.matshow(labeled, interpolation='nearest', cmap=cm.jet)
    ax4.set_xlabel('X-dimension [pixel]')
    ax4.set_ylabel('Y-dimension [pixel]')

    # show plots
    plt.show()
