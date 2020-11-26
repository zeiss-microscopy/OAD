# -*- coding: utf-8 -*-

#################################################################
# File        : visutools.py
# Version     : 0.1
# Author      : czsrh
# Date        : 16.05.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
from skimage.color import label2rgb


def create_heatmap(platetype=96):
    """Create empty heatmap array based on the platetype

    :param platetype: [description], defaults to 96
    :type platetype: int, optional
    :return: heatmap_array - empty array with the shape of the wellplate
    :rtype: NumPy.Array
    """

    # create heatmap based on the platetype
    nr, nc = getrowandcolumn(platetype=platetype)
    heatmap_array = np.full([nr, nc], np.nan)

    return heatmap_array


def showheatmap(heatmap, parameter2display,
                fontsize_title=12,
                fontsize_label=10,
                colormap='Blues',
                linecolor='black',
                linewidth=1.0,
                save=False,
                # savename='Heatmap.png',
                robust=True,
                filename='Test.czi',
                dpi=100):
    """Plot a heatmap for a wellplate from a dataframe.

    :param heatmap: Pandas DataFrame with the heatmap data for a wellplate
    :type heatmap: Pandas.dataFrame
    :param parameter2display: Measurement parameter to be displays as heatmap
    :type parameter2display: str
    :param fontsize_title: font size of title, defaults to 12
    :type fontsize_title: int, optional
    :param fontsize_label: font size of labels, defaults to 10
    :type fontsize_label: int, optional
    :param colormap: Specifies which colormap to use for the heatmap, defaults to 'Blues'
    :type colormap: str, optional
    :param linecolor: Specifies the color of the line between the wells, defaults to 'black'
    :type linecolor: str, optional
    :param linewidth: Specifies the line width between the wells, defaults to 1.0
    :type linewidth: float, optional
    :param save: Option to save the heapmap as PNG image, defaults to False
    :type save: bool, optional
    :param robust: If True and vmin or vmax are absent, the colormap range is
    computed with robust quantiles instead of the extreme values., defaults to True
    :type robust: bool, optional
    :param filename: filename of the original image - will be used to derive
    the filename for the PNG image to be saved, defaults to 'Test.czi'
    :type filename: str, optional
    :param dpi: dpi, defaults to 100
    :type dpi: int, optional
    :return: savename - filename of the saved plot
    :rtype: str
    """

    # create figure with subplots
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # create the heatmap
    ax = sns.heatmap(heatmap,
                     ax=ax,
                     cmap=colormap,
                     linecolor=linecolor,
                     linewidths=linewidth,
                     square=True,
                     robust=robust,
                     annot=False,
                     cbar_kws={"shrink": 0.68})

    # customize the plot to your needs
    ax.set_title(parameter2display,
                 fontsize=fontsize_title,
                 fontweight='normal')

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_label)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize_label)

    # modify the labels of the colorbar
    cax = plt.gcf().axes[-1]
    cax.tick_params(labelsize=fontsize_label)

    if save:
        savename = filename[:-4] + '_HM_' + parameter2display + '.png'
        fig.savefig(savename,
                    dpi=dpi,
                    orientation='portrait',
                    transparent=False)
        print('Heatmap image saved as: ', savename)
    else:
        savename = None

    return savename


def getrowandcolumn(platetype=96):
    """Returns the number of rows and columns for a given wellplate type

    :param platetype: number total wells of plate (6, 24, 96, 384 or 1536), defaults to 96
    :type platetype: int, optional
    :return: nr - number of rows of wellplate
    :rtype: int
    :return: nc - number of columns for wellplate
    :rtype: int
    """

    platetype = int(platetype)

    if platetype == 6:
        nr = 2
        nc = 3
    elif platetype == 24:
        nr = 4
        nc = 6
    elif platetype == 96:
        nr = 8
        nc = 12
    elif platetype == 384:
        nr = 16
        nc = 24
    elif platetype == 1536:
        nr = 32
        nc = 48

    return nr, nc


def convert_array_to_heatmap(hmarray, nr, nc):
    """Get the labels for a well plate and create a data frame
    from the numpy array.

    :param hmarray: The numpy array containing the actual heatmap
    :type hmarray: NumPy.Array
    :param nr: number of rows for the well plate
    :type nr: int
    :param nc: number of columns for the well plate
    :type nc: int
    :return: A Pandas dataframe with the respective row and columns labels
    :rtype: Pandas.DataFrame
    """

    lx, ly = extract_labels(nr, nc)
    heatmap_dataframe = pd.DataFrame(hmarray, index=ly, columns=lx)

    return heatmap_dataframe


def extract_labels(nr, nc):
    """[summary]

    :param nr: number of rows of the wellplate, e.g. 8 (A-H) for a 96 wellplate
    :type nr: [type]
    :param nc: number of columns of the wellplate, e.g. 12 (1-12) for a 96 wellplate
    :type nc: [type]
    :return: lx - list containing the actual row IDs for the selected wellplate
    :rtype: list
    :return: ly - list containing the actual column IDs for the selected wellplate
    :rtype: list
    """

    # labeling schemes
    labelX = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
              '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
              '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', ]

    labelY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']

    lx = labelX[0:nc]
    ly = labelY[0:nr]

    return lx, ly


def plot_segresults(image, mask, props, add_bbox=True):
    """Display the results of the segmentation

    :param image: 2d image with the original data
    :type image: NumPy.Array
    :param mask: binary mask from the segmentation
    :type mask: NumPy.Array
    :param props: region props with scikit-image
    :type props: list (of region properties)
    :param add_bbox: show the bounding box on the original image, defaults to True
    :type add_bbox: bool, optional
    """

    # create overlay image
    image_label_overlay = label2rgb(mask, image=image, bg_label=0)

    fig, ax = plt.subplots(1, 2, figsize=(16, 8))

    ax[0].imshow(image,
                 cmap=plt.cm.gray,
                 interpolation='nearest',
                 clim=[image.min(), image.max() * 0.5])

    ax[1].imshow(image_label_overlay,
                 clim=[image.min(), image.max() * 0.5])

    ax[0].set_title('Original', fontsize=12)
    ax[1].set_title('Masks', fontsize=12)

    if add_bbox:
        ax[0] = add_boundingbox(props, ax[0])

    plt.show()

    return ax


def add_boundingbox(props, ax2plot):
    """Add bounding boxes for objects to the current axes

    :param props: list of measured regions
    :type props: list
    :param ax2plot: matplot axis where the bounding boxes should be added
    :type ax2plot: axes
    :return: ax2plot - the axes including the bounding boxes
    :rtype: axes
    """

    for index, row in props.iterrows():

        minr = row['bbox-0']
        minc = row['bbox-1']
        maxr = row['bbox-2']
        maxc = row['bbox-3']
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False,
                                  edgecolor='red',
                                  linewidth=1)
        ax2plot.add_patch(rect)

    return ax2plot
