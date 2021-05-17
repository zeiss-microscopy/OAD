from aicspylibczi import CziFile
from aicsimageio import AICSImage
from apeer_ometiff_library import io

import tools.imgfile_tools as imf
import tools.fileutils as czt
import tools.segmentation_tools as sgt
import tools.visu_tools as vst

import numpy as np

from skimage import measure, segmentation, morphology
from skimage.morphology import white_tophat, black_tophat, disk, square, ball, closing, square
from skimage.filters import threshold_otsu, threshold_triangle, median, gaussian
from skimage.measure import regionprops
from skimage.color import label2rgb
import pandas as pd
import progressbar


def bbox2stageXY(image_stageX=0,  # image center stageX [micron]
                 image_stageY=0,  # image center stageY [micron]
                 sizeX=10,  # number of pixel in X
                 sizeY=20,  # number of pixel in X
                 scale=1.0,  # scaleXY [micron]
                 xstart=20,  # xstart of the bbox [pixel]
                 ystart=30,  # Ystart of the bbox [pixel]
                 bbox_width=5,  # width of the bbox [pixel]
                 bbox_height=5  # height of the bbox [pixel]
                 ):

    # calculate the origin of the image in stage coordinates
    width = sizeX * scale
    height = sizeY * scale

    # get the origin (top-right) of the image [micron]
    X0_stageX = image_stageX - width / 2
    Y0_stageY = image_stageY - height / 2

    # calculate the coordinates of the bounding box as stage coordinates
    bbox_center_stageX = X0_stageX + (xstart + bbox_width / 2) * scale
    bbox_center_stageY = Y0_stageY + (ystart + bbox_height / 2) * scale

    return bbox_center_stageX, bbox_center_stageY

#########################################################################################


filename = r"C:\Users\m1srh\OneDrive - Carl Zeiss AG\Smart_Microscopy_Workshop\datasets\brain_slide\OverViewScan.czi"

# get the metadata from the czi file
md, additional_mdczi = imf.get_metadata(filename)

# to make it more readable
stageX = md['SceneStageCenterX']
stageY = md['SceneStageCenterY']

# toggle additional printed output
verbose = True

# define columns names for dataframe
cols = ['S', 'T', 'Z', 'C', 'Number']
objects = pd.DataFrame(columns=cols)

# optional dipslay of "some" results - empty list = no display
show_image = [0]

# scalefactor to read CZI
sf = 1.0

# threshold parameters - will be used depending on the segmentation method
filtermethod = 'none'
filtersize = 5
threshold = 'triangle'

# use watershed for splitting - ws or ws_adv
use_ws = False
ws_method = 'ws_adv'
min_distance = 5
radius_dilation = 1
chindex = 0

# define object sizes
minsize = 100000
maxsize = 1000000000

# define minimum hole size
minholesize = 1000

# define save format for mask
adapt_dtype_mask = True
dtype_mask = np.int8

# check if it makes sense
if minholesize > minsize:
    minsize = minholesize

# read the czi mosaic image
czi = CziFile(filename)
# Get the shape of the data
print('Dimensions   : ', czi.dims)
print('Size         : ', czi.size)
print('Shape        : ', czi.dims_shape())
print('IsMosaic     : ', czi.is_mosaic())

# read the mosaic pixel data
mosaic = czi.read_mosaic(C=0, scale_factor=1.0)
print('Mosaic Shape :', mosaic.shape)

image2d = np.squeeze(mosaic, axis=0)
md['SizeX_readmosaic'] = image2d.shape[1]
md['SizeY_readmosaic'] = image2d.shape[0]

image_counter = 0
results = pd.DataFrame()

# create the savename for the OME-TIFF
savename = filename.split('.')[0] + '.ome.tiff'
#savename = filename.split('.')[0] + '.tiff'

for s in progressbar.progressbar(range(md['SizeS']), redirect_stdout=True):
    for t in range(md['SizeT']):
        for z in range(md['SizeZ']):

            values = {'S': s,
                      'T': t,
                      'Z': z,
                      'C': chindex,
                      'Number': 0}

    # filter image
    if filtermethod == 'none' or filtermethod == 'None':
        image2d_filtered = image2d
    if filtermethod == 'median':
        image2d_filtered = median(image2d, selem=disk(filtersize))
    if filtermethod == 'gauss':
        image2d_filtered = gaussian(image2d, sigma=filtersize, mode='reflect')

    # threshold image and run marker-based watershed
    binary = sgt.autoThresholding(image2d_filtered, method=threshold)

    # remove small holes
    mask = morphology.remove_small_holes(binary,
                                         area_threshold=minholesize,
                                         connectivity=1,
                                         in_place=True)

    # remove small objects
    mask = morphology.remove_small_objects(mask,
                                           min_size=minsize,
                                           in_place=True)

    # clear the border
    mask = segmentation.clear_border(mask,
                                     bgval=0,
                                     in_place=True)

    # label the objects
    mask = measure.label(binary)

    # adapt pixel type of mask
    if adapt_dtype_mask:
        mask = mask.astype(dtype_mask, copy=False)

    # measure region properties
    to_measure = ('label',
                  'area',
                  'centroid',
                  'bbox')

    # measure the specified parameters store in dataframe
    props = pd.DataFrame(
        measure.regionprops_table(
            mask,
            intensity_image=image2d,
            properties=to_measure
        )
    ).set_index('label')

    # filter objects by size
    props = props[(props['area'] >= minsize) & (props['area'] <= maxsize)]

    # add well information for CZI metadata
    try:
        props['WellId'] = md['Well_ArrayNames'][s]
        props['Well_ColId'] = md['Well_ColId'][s]
        props['Well_RowId'] = md['Well_RowId'][s]
    except (IndexError, KeyError) as error:
        # Output expected ImportErrors.
        print('Key not found:', error)
        print('Well Information not found. Using S-Index.')
        props['WellId'] = s
        props['Well_ColId'] = s
        props['Well_RowId'] = s

    # add plane indices
    props['S'] = s
    props['T'] = t
    props['Z'] = z
    props['C'] = chindex

    # count the number of objects
    values['Number'] = props.shape[0]

    # update dataframe containing the number of objects
    objects = objects.append(pd.DataFrame(values, index=[0]), ignore_index=True)
    results = results.append(props, ignore_index=True)

    image_counter += 1
    # optional display of results
    if image_counter - 1 in show_image:
        print('Well:', props['WellId'].iloc[0], 'Index S-C:', s, chindex, 'Objects:', values['Number'])

        ax = vst.plot_segresults(image2d, mask, props,
                                 add_bbox=True)

# make sure the array as 5D of order (T, Z, C, X, Y) to write an correct OME-TIFF
mask = imf.expand_dims5d(mask, md)

# write the OME-TIFF suing apeer-ometiff-library
io.write_ometiff(savename, mask, omexml_string=None)

# rename columns in pandas datatable
results.rename(columns={'bbox-0': 'ystart',
                        'bbox-1': 'xstart',
                        'bbox-2': 'yend',
                        'bbox-3': 'xend'},
               inplace=True)

# calculate the bbox width in height in [pixel] and [micron]
results['bbox_width'] = results['xend'] - results['xstart']
results['bbox_height'] = results['yend'] - results['ystart']
results['bbox_width_scaled'] = results['bbox_width'] * md['XScale']
results['bbox_height_scaled'] = results['bbox_height'] * md['XScale']

# calculate the bbox center StageXY
results['bbox_center_stageX'], results['bbox_center_stageY'] = bbox2stageXY(image_stageX=stageX,
                                                                            image_stageY=stageY,
                                                                            sizeX=md['SizeX'],
                                                                            sizeY=md['SizeY'],
                                                                            scale=md['XScale'],
                                                                            xstart=results['xstart'],
                                                                            ystart=results['ystart'],
                                                                            bbox_width=results['bbox_width'],
                                                                            bbox_height=results['bbox_height'])

# show results
print(results)
print('Done.')
