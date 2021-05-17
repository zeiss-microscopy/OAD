from aicspylibczi import CziFile
from aicsimageio import AICSImage
from apeer_ometiff_library import io
import tools.imgfile_tools as imf
import tools.fileutils as czt
import tools.segmentation_tools as sgt
import numpy as np
import os
from skimage import measure, segmentation, morphology
from skimage.morphology import disk, square
from skimage.filters import median, gaussian
import pandas as pd
import progressbar


def bbox2stageXY(image_stageX=0,
                 image_stageY=0,
                 sizeX=10,
                 sizeY=20,
                 scale=1.0,
                 xstart=20,
                 ystart=30,
                 bbox_width=5,
                 bbox_height=5
                 ):
    """Calculate the center of the bounding box as StageXY coordinate [micron]

    :param image_stageX: image center stageX [micron], defaults to 0
    :type image_stageX: int, optional
    :param image_stageY: image center stageY [micron], defaults to 0
    :type image_stageY: int, optional
    :param sizeX: number of pixel in X, defaults to 10
    :type sizeX: int, optional
    :param sizeY: number of pixel in Y, defaults to 20
    :type sizeY: int, optional
    :param scale: scaleXY [micron], defaults to 1.0
    :type scale: float, optional
    :param xstart: xstart of the bbox [pixel], defaults to 20
    :type xstart: int, optional
    :param ystart: ystart of the bbox [pixel], defaults to 30
    :type ystart: int, optional
    :param bbox_width: width of the bbox [pixel], defaults to 5
    :type bbox_width: int, optional
    :param bbox_height: height of the bbox [pixel], defaults to 5
    :type bbox_height: int, optional
    :return: bbox_center_stageX, bbox_center_stageY [micron]
    :rtype: float
    """

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


def execute(filepath,
            separator=';',
            filter_method='none',
            filter_size=3,
            threshold_method='triangle',
            min_objectsize=1000,
            min_holesize=100,
            saveformat='ome.tiff'
            ):

    print('--------------------------------------------------')
    print('FilePath : ', filepath)
    print(os.getcwd())
    print('File exists : ', os.path.exists(filepath))
    print('--------------------------------------------------')

    # define name for figure to be saved
    filename = os.path.basename(filepath)

    # get the metadata from the czi file
    md, additional_mdczi = imf.get_metadata(filepath)

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

    # index for channel
    chindex = 0

    # define maximum object sizes
    max_objectsize = 1000000000

    # define save format for mask
    adapt_dtype_mask = True
    dtype_mask = np.int8

    # check if it makes sense
    if min_holesize > min_objectsize:
        min_objectsize = min_holesize

    # read the czi mosaic image
    czi = CziFile(filepath)

    # get the shape of the data using aicspylibczi
    print('Dimensions   : ', czi.dims)
    print('Size         : ', czi.size)
    print('Shape        : ', czi.dims_shape())
    print('IsMosaic     : ', czi.is_mosaic())

    # read the mosaic pixel data
    mosaic = czi.read_mosaic(C=0, scale_factor=1.0)
    print('Mosaic Shape :', mosaic.shape)

    # get the mosiac as NumPy.Array - must it im memory !!!
    image2d = np.squeeze(mosaic, axis=0)
    md['SizeX_readmosaic'] = image2d.shape[1]
    md['SizeY_readmosaic'] = image2d.shape[0]

    image_counter = 0

    # initialize empty dataframe
    results = pd.DataFrame()

    # create the savename for the OME-TIFF
    if saveformat == 'ome.tiff':
        savename_seg = filename.split('.')[0] + '.ome.tiff'
    if saveformat == 'tiff':
        savename_seg = filename.split('.')[0] + '.tiff'

    for s in progressbar.progressbar(range(md['SizeS']), redirect_stdout=True):
        for t in range(md['SizeT']):
            for z in range(md['SizeZ']):

                values = {'S': s,
                          'T': t,
                          'Z': z,
                          'C': chindex,
                          'Number': 0}

        # filter image
        if filter_method == 'none' or filter_method == 'None':
            image2d_filtered = image2d
        if filter_method == 'median':
            image2d_filtered = median(image2d, selem=disk(filter_size))
        if filter_method == 'gauss':
            image2d_filtered = gaussian(image2d, sigma=filter_size, mode='reflect')

        # threshold image and run marker-based watershed
        binary = sgt.autoThresholding(image2d_filtered, method=threshold_method)

        # Remove contiguous holes smaller than the specified size
        mask = morphology.remove_small_holes(binary,
                                             area_threshold=min_holesize,
                                             connectivity=1,
                                             in_place=True)

        # remove small objects
        mask = morphology.remove_small_objects(mask,
                                               min_size=min_objectsize,
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
        props = props[(props['area'] >= min_objectsize) & (props['area'] <= max_objectsize)]

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

            # ax = vst.plot_segresults(image2d, mask, props,
            #                         add_bbox=True)

    # make sure the array as 5D of order (T, Z, C, X, Y) to write an correct OME-TIFF
    mask = imf.expand_dims5d(mask, md)

    # write the OME-TIFF suing apeer-ometiff-library
    io.write_ometiff(savename_seg, mask, omexml_string=None)

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

    # write the CSV data table
    print('Write to CSV File : ', filename)
    csvfile = os.path.splitext(filename)[0] + '_planetable.csv'
    results.to_csv(csvfile, sep=separator, index=False)

    # set the outputs
    outputs = {}
    outputs['segmented_image'] = savename_seg
    outputs['objects_table'] = csvfile

    return outputs


# test code locally
if __name__ == "__main__":

    filepath = './input/OverViewScan.czi'

    execute(filepath,
            separator=';',
            filter_method='none',
            filter_size=3,
            threshold_method='triangle',
            min_objectsize=100000,
            min_holesize=1000,
            saveformat='ome.tiff'
            )
