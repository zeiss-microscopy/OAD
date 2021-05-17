from aicspylibczi import CziFile
from aicsimageio import AICSImage, imread, imread_dask
import tools.imgfile_tools as imf
import tools.fileutils as czt
import tools.napari_tools as nap
import numpy as np
import zarr
import dask
import dask.array as da
from dask import delayed
from itertools import product
import napari

# filename = r"testdata\Tumor_H+E_small2.czi"
#filename = r"C:\Testdata_Zeiss\CD7\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small.czi"
#filename = r"C:\Testdata_Zeiss\CD7\Z-Stack_DCV\CellDivision_T=15_Z=20_CH=2_DCV.czi"
#filename = r"C:\Testdata_Zeiss\CD7\Mouse Kidney_40x0.95_3CD_JK_comp.czi"
#filename = r"C:\Testdata_Zeiss\DTScan_ID4_small.czi"
#filename = r"C:\Testdata_Zeiss\DTScan_ID4.czi"
#filename = r"D:\Temp\input\DTScan_ID4-nokeeptiles.czi"
#filename = r"C:\Testdata_Zeiss\CD7\testwell96.czi"
#filename = r"C:\Testdata_Zeiss\CZI_Testfiles\S=2_3x3_Z=4_CH=2.czi"
#filename = r"C:\Testdata_Zeiss\LatticeLightSheet\LS_Mitosis_T=150-300.czi"
#filename = r"C:\Users\m1srh\Downloads\Halo_CZI_small.czi"
filename = r"C:\Testdata_Zeiss\OverViewScan.czi"

######################################################################

# get the metadata from the czi file
md, additional_mdczi = imf.get_metadata(filename)

use_aicsimageio = True
use_pylibczi = False
use_dask_delayed = True

# decide which tool to use to read the image
if md['ImageType'] != 'czi':
    use_aicsimageio = True
elif md['ImageType'] == 'czi' and md['czi_isMosaic'] is False:
    use_aicsimageio = True
elif md['ImageType'] == 'czi' and md['czi_isMosaic'] is True:
    use_aicsimageio = False
    use_pylibczi = True


# check if CZI has T or Z dimension
hasT = False
hasZ = False

if 'T' in md['dims_aicspylibczi']:
    hasT = True
if 'Z' in md['dims_aicspylibczi']:
    hasZ = True

if use_aicsimageio:
    img = AICSImage(filename)

    if use_dask_delayed:
        print('Using AICSImageIO to read the image (Dask Delayed Reader).')
        all_scenes_array = img.get_image_data()
    if not use_dask_delayed:
        print('Using AICSImageIO to read the image.')
        all_scenes_array = img.get_image_dask_data()

if not use_aicsimageio and use_pylibczi is True:

    # read CZI using aicspylibczi
    czi = CziFile(filename)

    # for testing
    # Get the shape of the data
    print('Dimensions   : ', czi.dims)
    print('Size         : ', czi.size)
    print('Shape        : ', czi.dims_shape())
    print('IsMoasic     : ', czi.is_mosaic())
    if czi.is_mosaic():
        print('Mosaic Size  : ', czi.read_mosaic_size())

    # get the required shape for all and single scenes
    shape_all, shape_single, same_shape = czt.get_shape_allscenes(czi, md)
    print('Required_Array Shape for all scenes: ', shape_all)
    for sh in shape_single:
        print('Required Array Shape for single scenes: ', sh)

    #array_type = 'dask'
    array_type = 'zarr'
    #array_type = 'numpy'

    if array_type == 'zarr':

        # define array to store all channels
        print('Using aicspylibCZI to read the image (ZARR array).')

        # option 1
        # all_scenes_array = zarr.create(tuple(shape_all),
        #                               dtype=md['NumPy.dtype'],
        #                               chunks=True)

        # option 2
        all_scenes_array = zarr.open(r'c:\Temp\czi_scene_all.zarr', mode='w',
                                     shape=shape_all,
                                     chunks=True,
                                     dtype=md['NumPy.dtype'])

    if array_type == 'numpy':
        print('Using aicspylibCZI to read the image (Numpy.Array).')
        all_scenes_array = np.empty(shape_all, dtype=md['NumPy.dtype'])

    if array_type == 'zarr' or array_type == 'numpy':

        # loop over all scenes
        for s in range(md['SizeS']):
            # get the CZIscene for the current scene
            single_scene = czt.CZIScene(czi, md, sceneindex=s)
            out = czt.read_czi_scene(czi, single_scene, md, array_type=array_type)
            all_scenes_array[s, :, :, :, :, :] = np.squeeze(out, axis=0)

        print(all_scenes_array.shape)

    elif array_type == 'dask':

        def dask_load_sceneimage(czi, s, md):

            # get the CZIscene for the current scene
            single_scene = czt.CZIScene(czi, md, sceneindex=s)
            out = czt.read_czi_scene(czi, single_scene, md)
            return out

        sp = shape_all[1:]

        # create dask stack of lazy image readers
        print('Using aicspylibCZI to read the image (Dask.Array) + Delayed Reading.')
        lazy_process_image = dask.delayed(dask_load_sceneimage)  # lazy reader

        lazy_arrays = [lazy_process_image(czi, s, md) for s in range(md['SizeS'])]

        dask_arrays = [
            da.from_delayed(lazy_array, shape=sp, dtype=md['NumPy.dtype'])
            for lazy_array in lazy_arrays
        ]
        # Stack into one large dask.array
        all_scenes_array = da.stack(dask_arrays, axis=0)
        print(all_scenes_array.shape)


# show array inside napari viewer
with napari.gui_qt():

    viewer = napari.Viewer()

    layers = nap.show_napari(viewer, all_scenes_array, md,
                             blending='additive',
                             adjust_contrast=True,
                             gamma=0.85,
                             add_mdtable=True,
                             rename_sliders=True)
