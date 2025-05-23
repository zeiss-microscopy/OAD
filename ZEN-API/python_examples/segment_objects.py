from czitools.metadata_tools import czi_metadata as czimd
from czitools.utils import misc
from pylibCZIrw import czi as pyczi
import os
import numpy as np
from skimage import measure, segmentation, morphology
from skimage.filters import threshold_otsu, threshold_triangle, rank, median, gaussian
from skimage.morphology import (
    white_tophat,
    black_tophat,
    disk,
    square,
    ball,
    closing,
    square,
)
from skimage.filters import median, gaussian
import pandas as pd
from tqdm.contrib.itertools import product
from typing import List, Dict, Tuple, Optional, Type, Any, Union
import matplotlib.pyplot as plt


def show_plot(img1: np.ndarray, img2: np.ndarray) -> None:
    # just for testing purposes

    # show the results
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    ax[0].imshow(img1, cmap="gray")
    ax[1].imshow(img2, cmap="gray")
    plt.show()


def subtract_background(image, elem="disk", radius=50, light_bg=False):
    """Background subtraction using structure element.
    Slightly adapted from: https://forum.image.sc/t/background-subtraction-in-scikit-image/39118/4

    :param image: input image
    :type image: NumPy.Array
    :param elem: type of the structure element, defaults to 'disk'
    :type elem: str, optional
    :param radius: size of structure element [pixel], defaults to 50
    :type radius: int, optional
    :param light_bg: light background, defaults to False
    :type light_bg: bool, optional
    :return: image with background subtracted
    :rtype: NumPy.Array
    """
    # use 'ball' here to get a slightly smoother result at the cost of increased computing time
    if elem == "disk":
        str_el = disk(radius)
    if elem == "ball":
        str_el = ball(radius)

    if light_bg:
        img_subtracted = black_tophat(image, str_el)
    if not light_bg:
        img_subtracted = white_tophat(image, str_el)

    return img_subtracted


def autoThresholding(
    image2d, method: str = "triangle", radius: int = 10, value: int = 50
) -> np.ndarray:
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
    if method == "global_otsu":
        thresh = threshold_otsu(image2d)

    # calculate local Otsu threshold
    if method == "local_otsu":
        thresh = rank.otsu(image2d, disk(radius))

    if method == "value_based":
        thresh = value

    if method == "triangle":
        thresh = threshold_triangle(image2d)

    binary = image2d >= thresh

    return binary


def bbox2stageXY(
    image_stageX=0,
    image_stageY=0,
    sizeX=10,
    sizeY=20,
    scale=1.0,
    xstart=20,
    ystart=30,
    bbox_width=5,
    bbox_height=5,
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

    # calculate the width and height of the image in [micron]
    width = sizeX * scale
    height = sizeY * scale

    # get the origin (top-right) of the image [micron]
    X0_stageX = image_stageX - width / 2
    Y0_stageY = image_stageY - height / 2

    # calculate the coordinates of the bounding box as stage coordinates
    bbox_center_stageX = X0_stageX + (xstart + bbox_width / 2) * scale
    bbox_center_stageY = Y0_stageY + (ystart + bbox_height / 2) * scale

    return bbox_center_stageX, bbox_center_stageY


def execute(
    filepath: str,
    separator: str = ";",
    filter_method: str = "none",
    filter_size: int = 3,
    threshold_method: str = "triangle",
    min_objectsize: int = 1000,
    max_holesize: int = 100,
):
    """Main function that executed the workflow.

    :param filepath: file path of the CZI image
    :type filepath: tsr
    :param separator: sepeartor for the CSV table, defaults to ';'
    :type separator: str, optional
    :param filter_method: smoothing filer, defaults to 'none'
    :type filter_method: str, optional
    :param filter_size: kernel size or radius of filter element, defaults to 3
    :type filter_size: int, optional
    :param threshold_method: threshold method, defaults to 'triangle'
    :type threshold_method: str, optional
    :param min_objectsize: minimum object size, defaults to 1000
    :type min_objectsize: int, optional
    :param max_holesize: maximum object size, defaults to 100
    :type max_holesize: int, optional
    :return: outputs
    :rtype: dict
    """

    print("--------------------------------------------------")
    print("FilePath : ", filepath)
    print(os.getcwd())
    print("File exists : ", os.path.exists(filepath))
    print("--------------------------------------------------")

    # define name for figure to be saved
    filename = os.path.basename(filepath)

    # get the metadata from the czi file
    # get the metadata
    mdata = czimd.CziMetadata(filepath)

    # define columns names for dataframe
    cols = ["S", "T", "Z", "C", "Number"]
    objects = pd.DataFrame(columns=cols)

    # optional display of "some" results - empty list = no display
    show_image = [0]

    # scalefactor to read CZI
    sf = 1.0

    # index for channel - currently only single channel images are supported !
    chindex = 0

    # define maximum object sizes
    max_objectsize = 1000000000

    # check if it makes sense
    if max_holesize > min_objectsize:
        min_objectsize = max_holesize

    # check if dimensions are None (because they do not exist for that image)
    size_c = misc.check_dimsize(mdata.image.SizeC, set2value=1)
    size_z = misc.check_dimsize(mdata.image.SizeZ, set2value=1)
    size_t = misc.check_dimsize(mdata.image.SizeT, set2value=1)
    size_s = misc.check_dimsize(mdata.image.SizeS, set2value=1)

    # to make it more readable extract values from metadata dictionary
    stageX = mdata.sample.scene_stageX[0]
    stageY = mdata.sample.scene_stageY[0]

    # create the savename
    savename_seg = filename.split(".")[0] + "_seg.czi"

    # initialize empty dataframe
    results = pd.DataFrame()

    # write new CZI
    with pyczi.create_czi(savename_seg, exist_ok=True) as czidoc_w:
        with pyczi.open_czi(filepath) as czidoc_r:

            # main loop over all S- T - Z slices
            for (
                s,
                t,
                z,
            ) in product(range(size_s), range(size_t), range(size_z)):

                values = {"S": s, "T": t, "Z": z, "C": chindex, "Number": 0}

                # read 2D plane in case there are (no) scenes
                if mdata.image.SizeS is None:
                    img2d = czidoc_r.read(
                        plane={"T": t, "Z": z, "C": chindex}, zoom=sf
                    )[..., 0]
                else:
                    img2d = czidoc_r.read(
                        plane={"T": t, "Z": z, "C": chindex}, zoom=sf, scene=s
                    )[..., 0]

                # preprocessing - filter the image
                if filter_method == "none" or filter_method == "None":
                    image2d_filtered = img2d
                if filter_method == "median":
                    image2d_filtered = median(img2d, footprint=disk(filter_size))
                if filter_method == "gauss":
                    image2d_filtered = gaussian(
                        img2d, sigma=filter_size, mode="reflect"
                    )

                # threshold image
                mask = autoThresholding(image2d_filtered, method=threshold_method)

                # Remove contiguous holes smaller than the specified size
                mask = morphology.remove_small_holes(
                    mask, area_threshold=max_holesize, connectivity=1
                )

                # remove small objects
                mask = morphology.remove_small_objects(mask, min_size=min_objectsize)

                # clear the border
                mask = segmentation.clear_border(mask, bgval=0)

                # label the objects
                mask = measure.label(mask)

                # measure region properties
                to_measure = ("label", "area", "centroid", "bbox")

                # measure the specified parameters store in dataframe
                props = pd.DataFrame(
                    measure.regionprops_table(
                        mask, intensity_image=img2d, properties=to_measure
                    )
                ).set_index("label")

                # filter objects by size
                props = props[
                    (props["area"] >= min_objectsize)
                    & (props["area"] <= max_objectsize)
                ]

                # add well information for CZI metadata
                try:
                    props["WellId"] = mdata.sample.well_array_names[s]
                    props["Well_ColId"] = mdata.sample.well_colID[s]
                    props["Well_RowId"] = mdata.sample.well_rowID[s]
                except (IndexError, KeyError) as error:
                    # Output expected ImportErrors.
                    print("Key not found:", error)
                    print("Well Information not found. Using S-Index.")
                    props["WellId"] = s
                    props["Well_ColId"] = s
                    props["Well_RowId"] = s

                # add plane indices
                props["S"] = s
                props["T"] = t
                props["Z"] = z
                props["C"] = chindex

                # count the number of objects
                values["Number"] = props.shape[0]

                # update dataframe containing the number of objects
                objects = pd.concat(
                    [objects, pd.DataFrame(values, index=[0])], ignore_index=True
                )
                results = pd.concat([results, props], ignore_index=True)

                # add new axis for CZI writing and adapt pixel type
                mask = mask.astype("uint8")[..., np.newaxis]

                # write the plane with shape (Y, X, 1) to the new CZI file
                czidoc_w.write(
                    data=mask.astype("uint8"),
                    plane={"T": t, "Z": z, "C": chindex},
                    scene=s,
                )

            # write scaling the the new czi and check if valid scaling exists
        if mdata.scale.X is None:
            mdata.scale.X = 1.0
        if mdata.scale.Y is None:
            mdata.scale.Y = 1.0
        if mdata.scale.Y is None:
            mdata.scale.Z = 1.0

        czidoc_w.write_metadata(
            document_name=savename_seg,
            channel_names={0: mdata.channelinfo.names[chindex] + "_seg"},
            scale_x=mdata.scale.X * 10**-6,
            scale_y=mdata.scale.Y * 10**-6,
            scale_z=mdata.scale.Z * 10**-6,
        )

        # rename columns in pandas datatable
        results.rename(
            columns={
                "bbox-0": "ystart",
                "bbox-1": "xstart",
                "bbox-2": "yend",
                "bbox-3": "xend",
            },
            inplace=True,
        )

        # calculate the bbox width in height in [pixel] and [micron]
        results["bbox_width"] = results["xend"] - results["xstart"]
        results["bbox_height"] = results["yend"] - results["ystart"]
        results["bbox_width_scaled"] = results["bbox_width"] * mdata.scale.X
        results["bbox_height_scaled"] = results["bbox_height"] * mdata.scale.Y

        # calculate the bbox center StageXY
        results["bbox_center_stageX"], results["bbox_center_stageY"] = bbox2stageXY(
            image_stageX=stageX,
            image_stageY=stageY,
            sizeX=mdata.image.SizeX,
            sizeY=mdata.image.SizeY,
            scale=mdata.scale.X,
            xstart=results["xstart"],
            ystart=results["ystart"],
            bbox_width=results["bbox_width"],
            bbox_height=results["bbox_height"],
        )

    # show results
    print(results)
    print("Done.")

    # write the CSV data table
    print("Write to CSV File : ", filename)
    csvfile = os.path.splitext(filename)[0] + "_seg_planetable.csv"
    results.to_csv(csvfile, sep=separator, index=False)

    # set the outputs
    outputs = {}
    outputs["segmented_image"] = savename_seg
    outputs["objects_table"] = csvfile

    return outputs


# test code locally
if __name__ == "__main__":

    filepath = r"input\OverViewScan_small.czi"

    execute(
        filepath,
        separator=";",
        filter_method="median",
        filter_size=3,
        threshold_method="triangle",
        min_objectsize=100000,
        max_holesize=1000,
    )
