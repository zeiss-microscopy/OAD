# -*- coding: utf-8 -*-

#################################################################
# File        : segmentation_tools.py
# Version     : 0.1
# Author      : czsrh
# Date        : 20.04.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright (c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################


import sys
from time import process_time, perf_counter
import os
from glob import glob
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import imgfileutils as imf
from scipy import ndimage
from aicsimageio import AICSImage, imread
from skimage import exposure
from skimage.morphology import watershed, dilation
from skimage.feature import peak_local_max
from skimage.measure import label
from scipy.ndimage import distance_transform_edt
from skimage.segmentation import random_walker
from skimage import io, measure, segmentation
from skimage.filters import threshold_otsu, threshold_triangle, rank
from skimage.segmentation import clear_border
from skimage.color import label2rgb
from skimage.exposure import rescale_intensity
from skimage.util import invert
from skimage.filters import median, gaussian
from skimage.morphology import closing, square
from skimage.morphology import remove_small_objects, remove_small_holes
from skimage.morphology import disk, square, ball
from skimage.measure import label, regionprops
from MightyMosaic import MightyMosaic

try:
    print('Trying to find mxnet library ...')
    import mxnet
    from cellpose import plot, transforms
    from cellpose import models, utils

except ImportError as error:
    # Output expected ImportErrors.
    print(error.__class__.__name__ + ": " + error.msg)
    print('mxnet will not be used.')

try:
    print('Trying to find tensorflow library ...')
    # silence tensorflow output
    from silence_tensorflow import silence_tensorflow
    silence_tensorflow()
    import tensorflow as tf
    logging.getLogger("tensorflow").setLevel(logging.ERROR)
    print('TensorFlow Version : ', tf.version.GIT_VERSION, tf.__version__)
except ImportError as error:
    # Output expected ImportErrors.
    print(error.__class__.__name__ + ": " + error.msg)
    print('TensorFlow will not be used.')


def apply_watershed(binary, min_distance=10):
    """Apply normal watershed to a binary image

    :param binary: binary images from segmentation
    :type binary: NumPy.Array
    :param min_distance: minimum peak distance [pixel], defaults to 10
    :type min_distance: int, optional
    :return: mask - mask with separeted objects
    :rtype: NumPy.Array
    """

    # create distance map
    distance = ndimage.distance_transform_edt(binary)

    # determine local maxima
    local_maxi = peak_local_max(distance,
                                min_distance=min_distance,
                                indices=False,
                                labels=binary)

    # label maxima
    markers, num_features = ndimage.label(local_maxi)

    # apply watershed
    mask = watershed(-distance, markers,
                     mask=binary,
                     watershed_line=True).astype(np.int)

    return mask


def apply_watershed_adv(image2d,
                        segmented,
                        filtermethod_ws='median',
                        filtersize_ws=3,
                        min_distance=2,
                        radius=1):
    """Apply advanced watershed to a binary image

    :param image2d: 2D image with pixel intensities
    :type image2d: NumPy.Array
    :param segmented: binary images from initial segmentation
    :type segmented: NumPy.Array
    :param filtermethod_ws: choice of filter method, defaults to 'median'
    :type filtermethod_ws: str, optional
    :param filtersize_ws: size paramater for the selected filter, defaults to 3
    :type filtersize_ws: int, optional
    :param min_distance: minimum peak distance [pixel], defaults to 2
    :type min_distance: int, optional
    :param radius: radius for dilation disk, defaults to 1
    :type radius: int, optional
    :return: mask - binary mask with separated objects
    :rtype: NumPy.Array
    """

    # convert to float
    image2d = image2d.astype(np.float)

    # rescale 0-1
    image2d = rescale_intensity(image2d, in_range='image', out_range=(0, 1))

    # filter image
    if filtermethod_ws == 'median':
        image2d = median(image2d, selem=disk(filtersize_ws))
    if filtermethod_ws == 'gauss':
        image2d = gaussian(image2d, sigma=filtersize_ws, mode='reflect')

    # create the seeds
    peaks = peak_local_max(image2d,
                           labels=label(segmented),
                           min_distance=min_distance,
                           indices=False)

    # create the seeds
    seed = dilation(peaks, selem=disk(radius))

    # create watershed map
    watershed_map = -1 * distance_transform_edt(segmented)

    # create mask
    mask = watershed(watershed_map,
                     markers=label(seed),
                     mask=segmented,
                     watershed_line=True).astype(np.int)

    return mask


def segment_threshold(image2d,
                      filtermethod='median',
                      filtersize=3,
                      threshold='triangle',
                      split_ws=True,
                      min_distance=30,
                      ws_method='ws_adv',
                      radius=1):
    """Segment an image using the following steps:
    - filter image
    - threshold image
    - apply watershed

    :param image2d: 2D image with pixel intensities
    :type image2d: NumPy.Array
    :param filtermethod: choice of filter method, defaults to 'median'
    :type filtermethod: str, optional
    :param filtersize: size paramater for the selected filter, defaults to 3
    :type filtersize: int, optional
    :param threshold: choice of thresholding method, defaults to 'triangle'
    :type threshold: str, optional
    :param split_ws: enable splitting using watershed, defaults to True
    :type split_ws: bool, optional
    :param min_distance: minimum peak distance [pixel], defaults to 30
    :type min_distance: int, optional
    :param ws_method: choice of watershed method, defaults to 'ws_adv'
    :type ws_method: str, optional
    :param radius: radius for dilation disk, defaults to 1
    :type radius: int, optional
    :return: mask - binary mask
    :rtype: NumPy.Array
    """

    # filter image
    if filtermethod == 'none':
        image2d_filtered = image2d
    if filtermethod == 'median':
        image2d_filtered = median(image2d, selem=disk(filtersize))
    if filtermethod == 'gauss':
        image2d_filtered = gaussian(image2d, sigma=filtersize, mode='reflect')

    # threshold image and run marker-based watershed
    binary = autoThresholding(image2d_filtered, method=threshold)

    # apply watershed
    if split_ws:

        if ws_method == 'ws':
            mask = apply_watershed(binary,
                                   min_distance=min_distance)

        if ws_method == 'ws_adv':
            mask = apply_watershed_adv(image2d, binary,
                                       min_distance=min_distance,
                                       radius=radius)

    if not split_ws:
        # label the objects
        mask, num_features = ndimage.label(binary)
        mask = mask.astype(np.int)

    return mask


def autoThresholding(image2d,
                     method='triangle',
                     radius=10,
                     value=50):
    """Autothreshold an 2D intensity image which is calculated using:
    binary = image2d >= thresh

    :param image2d: input image for thresholding
    :type image2d: NumPy.Array
    :param method: choice of thresholding method, defaults to 'triangle'
    :type method: str, optional
    :param radius: radius of disk when using local Otsu threshold, defaults to 10
    :type radius: int, optional
    :param value: manual threshold value, defaults to 50
    :type value: int, optional
    :return: binary - binary mask from thresholding
    :rtype: NumPy.Array
    """

    # calculate global Otsu threshold
    if method == 'global_otsu':
        thresh = threshold_otsu(image2d)

    # calculate local Otsu threshold
    if method == 'local_otsu':
        thresh = rank.otsu(image2d, disk(radius))

    if method == 'value_based':
        thresh = value

    if method == 'triangle':
        thresh = threshold_triangle(image2d)

    binary = image2d >= thresh

    return binary


def cutout_subimage(image2d,
                    startx=0,
                    starty=0,
                    width=100,
                    height=200):
    """Cutout a subimage ot of a bigger image

    :param image2d: the original image
    :type image2d: NumPy.Array
    :param startx: startx, defaults to 0
    :type startx: int, optional
    :param starty: starty, defaults to 0
    :type starty: int, optional
    :param width: width, defaults to 100
    :type width: int, optional
    :param height: height, defaults to 200
    :type height: int, optional
    :return: image2d - subimage cutted out from original image2d
    :rtype: NumPy.Array
    """

    image2d = image2d[starty: height, startx:width]

    return image2d


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
    :param filename: filename of the original image file - will be used to derive
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
    """[summary]

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
    """Get the labels for a well plate and create a data frame from the numpy array

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


def plot_results(image, mask, props, add_bbox=True):
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


def segment_nuclei_cellpose(image2d, model,
                            channels=[0, 0],
                            rescale=None,
                            diameter=None):
    """Segment nucleus or cytosol using a cellpose model

    - define CHANNELS to run segmentation on
    - grayscale=0, R=1, G=2, B=3
    - channels = [cytoplasm, nucleus]
    - if NUCLEUS channel does not exist, set the second channel to 0
    - IF ALL YOUR IMAGES ARE THE SAME TYPE, you can give a list with 2 elements
    - channels = [0,0] # IF YOU HAVE GRAYSCALE
    - channels = [2,3] # IF YOU HAVE G=cytoplasm and B=nucleus
    - channels = [2,1] # IF YOU HAVE G=cytoplasm and R=nucleus


    :param image2d: 2D image
    :type image2d: NumPy.Array
    :param model: cellposemodel for segmentation
    :type model: cellpose model
    :param channels: channels used for segmentation[description], defaults to [0, 0]
    :type channels: list, optional
    :param rescale: if diameter is set to None, and rescale is not None,
    then rescale is used instead of diameter for resizing image, defaults to None
    :type rescale: float, optional
    :param diameter: Estimated diameter of objects. If set to None,
    then diameter is automatically estimated if size model is loaded, defaults to None
    :type diamter: list, optional
    :return: mask - binary mask
    :rtype: NumPy.Array
    """

    # define CHANNELS to run segmentation on
    # grayscale=0, R=1, G=2, B=3
    # channels = [cytoplasm, nucleus]
    # if NUCLEUS channel does not exist, set the second channel to 0

    # IF ALL YOUR IMAGES ARE THE SAME TYPE, you can give a list with 2 elements
    # channels = [0,0] # IF YOU HAVE GRAYSCALE
    # channels = [2,3] # IF YOU HAVE G=cytoplasm and B=nucleus
    # channels = [2,1] # IF YOU HAVE G=cytoplasm and R=nucleus

    # get the mask for a single image

    masks, _, _, _ = model.eval([image2d],
                                channels=channels,
                                diameter=diameter,
                                invert=False,
                                do_3D=False,
                                net_avg=True,
                                tile=False,
                                threshold=0.4,
                                rescale=rescale,
                                progress=None)

    # masks, _, _, _ = model.eval([image2d], rescale=rescale, channels=channels)

    return masks[0]


def set_device():
    """Check if GPU working, and if so use it

    :return: device - CPU or GPU
    :rtype: mxnet device
    """
    # check if GPU working, and if so use it
    use_gpu = utils.use_gpu()
    print('Use GPU: ', use_gpu)

    if use_gpu:
        device = mxnet.gpu()
    else:
        device = mxnet.cpu()

    return device


def load_cellpose_model(model_type='nuclei',
                        gpu=False,
                        net_avg=True,
                        batch_size=8):

    # load cellpose model for cell nuclei using GPU or CPU
    print('Loading Cellpose Model ...')

    # try to get the device
    try:
        device = set_device()
    except NameError as error:
        print(error.__class__.__name__ + ": " + error.msg)
        device = None

    if device is None:
        model = models.Cellpose(gpu=False,
                                model_type='nuclei',
                                net_avg=net_avg,
                                batch_size=batch_size)

    if device is not None:
        model = models.Cellpose(model_type=model_type,
                                net_avg=net_avg,
                                batch_size=batch_size,
                                device=device)

    # model = models.Cellpose(device=set_device(), model_type='nuclei')
    # model = models.Cellpose(device=mxnet.gpu(), model_type='nuclei')

    return model


def load_tfmodel(modelfolder='model_folder'):

    start = perf_counter()
    tfmodel = tf.keras.models.load_model(modelfolder)

    # Determine input shape required by the model and crop input image
    tile_height, tile_width = tfmodel.signatures["serving_default"].inputs[0].shape[1:3]
    end = perf_counter()
    print('Time to load TF2 model:', end - start)

    return tfmodel, tile_height, tile_width


def segment_zentf(image2d, model, classlabel):
    """Segment a singe [X, Y] 2D image using a pretrained segmentation
    model from the ZEN. The out will be a binary mask from the prediction
    of ZEN czmodel which is a TF.SavedModel with metainformation

    :param image2d: image to be segmented
    :type image2d: NumPy.Array
    :param model: trained TF2 model used for segmentation
    :type model: TF.SavedModel
    :param classlabel: Index for the class one is interested in
    :type classlabel: int
    :return: binary - binary mask of the specified class
    :rtype: NumPy.Array
    """

    # add add batch dimension (at the front) and channel dimension (at the end)
    image2d = image2d[np.newaxis, ..., np.newaxis]

    # Run prediction - array shape must be [1, 1024, 1024, 1]
    prediction = model.predict(image2d)[0]  # Removes batch dimension

    # Generate labels from one-hot encoded vectors
    prediction_labels = np.argmax(prediction, axis=-1)

    # get the desired class
    # background = 0, nuclei = 1 and borders = 2

    # extract desired class
    binary = np.where(prediction_labels == classlabel, 1, 0)

    return binary


def segment_zentf_tiling(image2d, model,
                         tilesize=1024,
                         classlabel=1,
                         overlap_factor=1):
    """Segment a singe [X, Y] 2D image using a pretrained segmentation
    model from the ZEN. The out will be a binary mask from the prediction
    of ZEN czmodel which is a TF.SavedModel with metainformation.

    Before the segmentation via the network will be applied
    the image2d will be tiled in order to match the tile size to the required
    batch tile size of the used network. Default is (1024, 1024)

    :param image2d: image to be segmented
    :type image2d: NumPy.Array
    :param model: trained TF2 model used for segmentation
    :type model: TF.SavedModel
    :param tilesize: required tile size for the segmentation model, defaults to 1024
    :type tilesize: int, optional
    :param classlabel: Index for the class one is interested in, defaults to 1
    :type classlabel: int, optional
    :param overlap_factor: overlap_factor of 2 = stride between each tile
    is only tile_shape/overlap_factor and therefore
    overlap_factor = 1 means no overlap, defaults to 1
    :type overlap_factor: int, optional
    :return: binary - binary mask of the specified class
    :rtype: Numpy.Array
    """

    # create tile image using MightMosaic
    image2d_tiled = MightyMosaic.from_array(image2d, (tilesize, tilesize),
                                            overlap_factor=overlap_factor,
                                            fill_mode='reflect')

    print('image2d_tiled shape : ', image2d_tiled.shape)
    # get number of tiles
    num_tiles = image2d_tiled.shape[0] * image2d_tiled.shape[1]
    print('Number of Tiles: ', num_tiles)

    # create array for the binary results
    binary_tiled = image2d_tiled

    ct = 0
    for n1 in range(image2d_tiled.shape[0]):
        for n2 in range(image2d_tiled.shape[1]):

            ct += 1
            print('Processing Tile : ', ct, ' Size : ', image2d_tiled[n1, n2, :, :].shape)

            # extract a tile
            tile = image2d_tiled[n1, n2, :, :]

            # get the binary from the prediction for a single tile
            binary_tile = segment_zentf(tile, model, classlabel=classlabel)

            # cats the result into the output array
            binary_tiled[n1, n2, :, :] = binary_tile

    # created fused binary and covert to int
    binary = binary_tiled.get_fusion().astype(int)

    return binary


def add_padding(image2d, input_height=1024, input_width=1024):
    """Add padding to an image if the size of that image is
    smaller than the required input width and input height

    :param image2d: 2d image
    :type image2d: NumPy.Array
    :param input_height: required height of the input image, defaults to 1024
    :type input_height: int, optional
    :param input_width: required width of the input image, defaults to 1024
    :type input_width: int, optional
    :return: image2d_padded - added image with teh required size
    :rtype: NumPy Array
    """

    if len(image2d.shape) == 2:
        isrgb = False
        image2d = image2d[..., np.newaxis]
    else:
        isrgb = True

    padding_height = input_height - image2d.shape[0]
    padding_width = input_width - image2d.shape[1]
    padding_left, padding_right = padding_width // 2, padding_width - padding_width // 2
    padding_top, padding_bottom = padding_height // 2, padding_height - padding_height // 2

    image2d_padded = np.pad(image2d, ((padding_top, padding_bottom), (padding_left, padding_right), (0, 0)), 'reflect')

    if not isrgb:
        image2d_padded = np.squeeze(image2d_padded, axis=2)

    return image2d_padded, (padding_top, padding_bottom, padding_left, padding_right)
