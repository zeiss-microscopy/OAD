# -*- coding: utf-8 -*-

#################################################################
# File        : processing_tools.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from typing import Tuple, Optional, List, Literal, Union
from typing_extensions import Annotated
from pydantic import Field, validate_arguments

# from pydantic.error_wrappers import ValidationError
from skimage.filters import threshold_triangle, median, gaussian
from skimage.measure import label, regionprops_table, find_contours
from skimage.morphology import remove_small_objects, disk, ball, remove_small_holes
from skimage.morphology import white_tophat, black_tophat
from skimage import measure, segmentation
from skimage.filters import threshold_otsu
from skimage.color import label2rgb
from skimage.util import invert
import numpy as np

# from zenapi_tools import get_logger
from zenapi_tools import set_logging
from onnx_inference import OnnxInferencer
import pandas as pd
import os
from czitools.metadata_tools import czi_metadata as czimd
from czitools.utils import misc
from pylibCZIrw import czi as pyczi
from tqdm.contrib.itertools import product
from shapely.geometry import Polygon

# get the logger
# logger = get_logger()
logger = set_logging()


class ArrayProcessor:
    """
    A class used to process 2D arrays with various methods including filtering, thresholding, and object counting.

    Attributes
    ----------
    array : np.ndarray
        a 2D array to be processed

    Methods
    -------
    apply_median_filter(footprint: np.ndarray) -> np.ndarray:
        Applies a median filter to the array with the given footprint.

    apply_gaussian_filter(sigma: int) -> np.ndarray:
        Applies a gaussian filter to the array with the given sigma.

    apply_triangle_threshold() -> np.ndarray:
        Applies a triangle threshold to the array.

    apply_threshold(value: int, invert_result: bool = False) -> np.ndarray:
        Applies a threshold to the array with the given value and optionally inverts the result.

    apply_semantic_seg(inferencer: OnnxInferencer, class_index: int, use_gpu: bool = False) -> np.ndarray:
        Applies semantic segmentation to the array using the given inferencer and class index.

    apply_regression(inferencer: OnnxInferencer, use_gpu: bool = False) -> np.ndarray:
        Applies regression to the array using the given inferencer.

    count_objects(min_size: int = 10, label_rgb: bool = True, bg_label: int = 0) -> Tuple[np.ndarray, int]:
        Counts the objects in the array that are larger than the given size and optionally labels them in RGB.
    """

    def __init__(self, array):
        """
        Parameters
        ----------
        array : np.ndarray
            a 2D array to be processed
        """
        if isinstance(array, np.ndarray) and len(array.shape) == 2:
            self.array = array
        else:
            raise TypeError("Input should be a 2D array")

    def apply_gaussian_filter(self, sigma: int) -> np.ndarray:
        """
        Applies gaussian filter to the input array with given sigma.

        Parameters:
        sigma (int): Sigma value for gaussian filter

        Returns:
        np.ndarray: Gaussian filtered numpy array

        Raises:
        ValueError: If sigma parameter is invalid.
        """
        if isinstance(sigma, int) and sigma > 1:
            return gaussian(
                self.array, sigma=sigma, preserve_range=True, mode="nearest"
            ).astype(self.array.dtype)
        else:
            raise ValueError("Sigma parameter is invalid.")

    def apply_median_filter(self, filter_size: int) -> np.ndarray:
        """
        Applies median filter to the input array with given footprint.

        Parameters:
        filter_size (np.ndarray): Size of the Footprint for the median filter

        Returns:
        np.ndarray: Median filtered numpy array

        Raises:
        ValueError: If Footprint parameter is invalid.
        """
        if isinstance(filter_size, int):
            return median(self.array, footprint=disk(filter_size)).astype(
                self.array.dtype
            )
        else:
            raise ValueError("Filter Size parameter is invalid.")

    def apply_triangle_threshold(self) -> np.ndarray:
        """
        Applies triangle threshold to the input array.

        Returns:
        np.ndarray: Thresholded numpy array
        """

        # apply the threshold
        thresh = threshold_triangle(self.array)

        return self.array >= thresh

    def apply_otsu_threshold(self) -> np.ndarray:
        """
        Applies Otsu threshold to the input array.

        Returns:
        np.ndarray: Thresholded numpy array
        """

        # apply the threshold
        thresh = threshold_otsu(self.array)

        return self.array >= thresh

    def apply_threshold(self, value: int, invert_result: bool = False) -> np.ndarray:
        """
        Applies threshold to the input array.

        Parameters:
        value (int): Threshold value for the input array
        invert_result (bool): Invert the thresholded result (default False)

        Returns:
        np.ndarray: Thresholded numpy array

        Raises:
        ValueError: If threshold parameters are invalid.
        """
        if isinstance(value, int) and value >= 0 and (isinstance(invert_result, bool)):

            # apply the threshold
            self.array = self.array >= value

            if invert_result:
                self.array = invert(self.array)

            return self.array
        else:
            raise ValueError("Threshold parameters are invalid.")

    def apply_semantic_seg(
        self,
        inferencer: OnnxInferencer,
        class_index: int,
        input_shape: List[int],
        use_gpu: bool = False,
    ) -> np.ndarray:
        """
        Applies semantic segmentation to the input array using the provided inferencer.

        Parameters:
        inferencer (OnnxInferencer): Inferencer used for semantic segmentation
        class_index (int): Index of class to extract
        input_shape (List): Required shape of the model input.
        use_gpu (bool): Use GPU if available (default False)

        Returns:
        np.ndarray: Result of semantic segmentation

        Raises:
        ValueError: If one of input parameters is invalid.
        """

        if (
            self.array.shape[0] != input_shape[0]
            or self.array.shape[1] != input_shape[1]
        ):
            raise ValueError(
                f"Array shape {self.array.shape[0]}x{self.array.shape[1]} does not match the model input shape {input_shape[0]}x{input_shape[1]}."
            )

        if (
            isinstance(inferencer, OnnxInferencer)
            and isinstance(class_index, int)
            and class_index > 0
        ):

            # rescale - use with arivisAI models
            max_value = np.iinfo(self.array.dtype).max
            self.array = self.array / (max_value - 1)

            # run prediction
            self.array = inferencer.predict(
                [self.array[..., np.newaxis]], use_gpu=use_gpu
            )[0]

            # get the labels and add 1 to reflect the real values
            self.array = np.argmax(self.array, axis=-1) + 1

            # extract the correct class
            self.array = (self.array == class_index).astype(np.int16)

            return self.array
        else:
            raise ValueError("Parameters are invalid.")

    def apply_regression(
        self, inferencer: OnnxInferencer, input_shape: List[int], use_gpu: bool = False
    ) -> np.ndarray:
        """
        Applies regression to the input array using the provided inferencer.

        Parameters:
        inferencer (OnnxInferencer): Inferencer used for regression
        input_shape (List): Required shape of the model input.
        use_gpu (bool): Use GPU if available (default False)

        Returns:
        np.ndarray: Result of regression

        Raises:
        ValueError: If ONNX Inferencer is invalid.
        """

        if (
            self.array.shape[0] != input_shape[0]
            or self.array.shape[1] != input_shape[1]
        ):
            raise ValueError("Input shape does not match the model input shape.")

        if isinstance(inferencer, OnnxInferencer):

            # run prediction
            self.array = inferencer.predict(
                [self.array[..., np.newaxis]], use_gpu=use_gpu
            )[0]

            return self.array.astype(np.int16)
        else:
            raise ValueError("Onnx Inferencer Parameters are invalid.")

    def label_objects(
        self,
        min_size: int = 10,
        max_size: int = 100000000,
        fill_holes: bool = True,
        max_holesize: int = 1,
        label_rgb: bool = True,
        orig_image: Optional[np.ndarray] = None,
        bg_label: int = 0,
        measure_params: bool = False,
        measure_properties: Optional[Tuple[str]] = (
            "label",
            "area",
            "centroid",
            "bbox",
        ),
    ) -> Tuple[np.ndarray, int, pd.DataFrame]:
        """
        Counts objects in the input array and returns labeled image with the count.

        Parameters:
        min_size (int): Minimum size of the objects (default 10)
        max_size (int): Maximum size of the objects (default 100000000)
        fill_holes (bool): Option to fill holes (default True)
        max_holesize (int): Maximum size of holes to be filled (default 1)
        label_rgb (bool): Generate labeled RGB image (default True)
        orig_image (np.ndarray): original image data for overlay (default None)
        bg_label (int): Background label value (default 0)
        measure (bool): Use scikit-image to measure parameters (default False)
        measure_properties (tuple): Parameters to be measured (default ("label", "area", "centroid", "bbox"))

        Returns:
        Tuple[np.ndarray, int]: Labeled image and count of objects

        Raises:
        ValueError: If min_size parameter is invalid.
        """
        if (
            isinstance(min_size, int)
            and min_size >= 1
            and max_holesize >= 1
            and isinstance(fill_holes, bool)
        ):

            # Remove contiguous holes smaller than the specified size
            if not np.issubdtype(self.array.dtype, bool):
                self.array = remove_small_holes(
                    self.array.astype(bool), area_threshold=max_holesize, connectivity=1
                )
            else:
                self.array = remove_small_holes(
                    self.array, area_threshold=max_holesize, connectivity=1
                )

            # remove small objects
            if not np.issubdtype(self.array.dtype, bool):
                self.array = remove_small_objects(self.array.astype(bool), min_size)
            else:
                self.array = remove_small_objects(self.array, min_size)

            # clear the border
            self.array = segmentation.clear_border(self.array, bgval=bg_label)

            # label the particles
            self.array, num_label = label(
                self.array, background=bg_label, return_num=True, connectivity=2
            )

            # measure the specified parameters store in dataframe
            props = None

            if measure_params:
                if orig_image is None:

                    props = pd.DataFrame(
                        regionprops_table(
                            self.array.astype(np.uint16), properties=measure_properties
                        )
                    ).set_index("label")
                else:
                    props = pd.DataFrame(
                        regionprops_table(
                            self.array.astype(np.uint16),
                            intensity_image=orig_image,
                            properties=measure_properties,
                        )
                    ).set_index("label")

                    # filter objects by size
                props = props[(props["area"] >= min_size) & (props["area"] <= max_size)]

            # apply RGB labels
            if label_rgb:
                if orig_image is None:
                    self.array = label2rgb(self.array, image=None, bg_label=bg_label)
                else:
                    self.array = label2rgb(
                        self.array, image=orig_image, bg_label=bg_label
                    )

            return self.array, num_label, props
        else:
            raise ValueError("Parameters are invalid.")

    def subtract_background(
        image: np.ndarray,
        elem: Literal["disk", "ball"],
        radius: int = 50,
        light_bg: bool = False,
    ) -> np.ndarray:
        """Slightly adapted from: https://forum.image.sc/t/background-subtraction-in-scikit-image/39118/4

        Subtracts the background of a given image using a morphological operation.

        Parameters
        ----------
        image : numpy.ndarray
            The image to subtract the background from. Should be a two-dimensional grayscale image.
        elem : str, optional
            The shape of the structuring element to use for the morphological operation, either 'disk' or 'ball'.
            Defaults to 'disk'.
        radius : int, optional
            The radius of the structuring element to use. Should be a positive integer. Defaults to 50.
        light_bg : bool, optional
            If True, assume that the background is lighter than the foreground,
            otherwise assume that the background is darker than the foreground.
            Defaults to False.

        Returns
        -------
        numpy.ndarray
            The resulting image with the background subtracted.

        Raises
        ------
        ValueError
            If the `radius` parameter is not a positive integer, or if the `elem` parameter
            is not 'disk' or 'ball'.

        """

        if isinstance(radius, int) and elem in ["disk", "ball"] and radius > 0:
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

        else:
            raise ValueError("Parameters is invalid.")


def bbox2stageXY(
    *,
    image_stageX: float = 0,
    image_stageY: float = 0,
    sizeX: int = 10,
    sizeY: int = 20,
    scale: float = 1.0,
    xstart: int = 20,
    ystart: int = 30,
    bbox_width: int = 5,
    bbox_height: int = 5,
):
    """
    Calculate the center of the bounding box as StageXY coordinates [micron]

    Args:
        image_stageX: the StageX coordinate [micron] of the center of the image
        image_stageY: the StageY coordinate [micron] of the center of the image
        sizeX: the size of the image along the x-axis [pixels]
        sizeY: the size of the image along the y-axis [pixels]
        scale: the scaling factor for the image [micron/pixel]
        xstart: the x-coordinate of the top-left corner of the bounding box [pixels]
        ystart: the y-coordinate of the top-left corner of the bounding box [pixels]
        bbox_width: the width of the bounding box [pixels]
        bbox_height: the height of the bounding box [pixels]

    Returns:
        A tuple containing the StageXY coordinate [micron] of the center of the bounding box
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


def xy2stageXY(
    *,
    image_stageX: float = 0,
    image_stageY: float = 0,
    sizeX: int = 10,
    sizeY: int = 20,
    scale: float = 1.0,
    x: Union[int, float, List[Union[int, float]]] = [20.0],
    y: Union[int, float, List[Union[int, float]]] = [30.0],
):
    # check if x and y are actually lists
    if not isinstance(x, list):
        x = [x]
    if not isinstance(y, list):
        y = [y]

    # calculate the width and height of the image in [micron]
    width = sizeX * scale
    height = sizeY * scale

    # get the origin (top-right) of the image [micron]
    X0_stageX = image_stageX - width / 2
    Y0_stageY = image_stageY - height / 2

    # calculate the coordinates of the bounding box as stage coordinates
    x_stageX = X0_stageX + [i * scale for i in x]
    y_stageY = Y0_stageY + [i * scale for i in y]

    return x_stageX, y_stageY


@validate_arguments
def segment_czi(
    filepath: str,
    savepath: str,
    chindex: Annotated[int, Field(strict=True, ge=0)] = 0,
    zoomlevel: Annotated[float, Field(strict=True, gt=0.1, le=1.0)] = 1.0,
    filter_method: Literal[None, "none", "median", "gaussian"] = None,
    filter_size: Annotated[int, Field(strict=True, ge=1)] = 3,
    min_objectsize: Annotated[int, Field(strict=True, ge=1)] = 1000,
    max_holesize: Annotated[int, Field(strict=True, ge=10)] = 100,
    add_polygons: bool = False,
) -> Tuple[str, pd.DataFrame, str, pd.DataFrame]:
    """
    Segment a CZI file and save the segmented image, object properties, and CSV file.

    Args:
        filepath (str): The path to the CZI file.
        savepath (str): The directory where the segmented image and CSV file will be saved.
        chindex (int, optional): The channel index to segment. Defaults to 0.
        zoomlevel (float, optional): The zoom level for image processing. Defaults to 1.0.
        filter_method (Literal[None, "none", "median", "gaussian"], optional): The filter method to apply. Defaults to None.
        filter_size (int, optional): The size of the filter. Defaults to 3.
        min_objectsize (int, optional): The minimum object size to consider. Defaults to 1000.
        max_holesize (int, optional): The maximum hole size to consider. Defaults to 100.
        add_polygons (bool, optional): Whether to add polygons to the results. Defaults to False.

    Returns:
        Tuple[str, pd.DataFrame, str, pd.DataFrame]: A tuple containing the path to the segmented image,
                                                     individual object properties dataframe, CSV file path and overall objects numbers.
    """

    # get the metadata at once as one big class
    mdata = czimd.CziMetadata(filepath)

    # define columns names for pandas dataframe
    cols = ["S", "T", "Z", "C", "Number"]
    objects = pd.DataFrame(columns=cols)

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
    name_seg = misc.get_fname_woext(mdata.filename)
    savepath_seg = os.path.join(savepath, name_seg) + "_seg.czi"

    # initialize empty dataframe
    results = pd.DataFrame()
    results.assign(S=None, T=None, Z=None, C=None)

    if add_polygons:
        results["polygon"] = None
        results["polygon_scaled"] = None

    # write new CZI
    with pyczi.create_czi(savepath_seg, exist_ok=True) as czidoc_w:
        with pyczi.open_czi(filepath) as czidoc_r:

            # main loop over all S-T-Z slices
            for (
                s,
                t,
                z,
            ) in product(range(size_s), range(size_t), range(size_z)):

                values = {"S": s, "T": t, "Z": z, "C": chindex, "Number": 0}

                # read 2D plane in case there are (no) scenes
                if mdata.image.SizeS is None:
                    img2d = czidoc_r.read(
                        plane={"T": t, "Z": z, "C": chindex}, zoom=zoomlevel
                    )[..., 0]
                else:
                    img2d = czidoc_r.read(
                        plane={"T": t, "Z": z, "C": chindex}, zoom=zoomlevel, scene=s
                    )[..., 0]

                ap = ArrayProcessor(img2d)

                # preprocessing - filter the image
                if filter_method is None:
                    processed = img2d

                if filter_method == "median":
                    processed = ArrayProcessor(img2d).apply_median_filter(
                        footprint=disk(filter_size)
                    )
                if filter_method == "gaussian":
                    processed = ArrayProcessor(img2d).apply_gaussian_filter(
                        sigma=filter_size
                    )

                # segment the image
                processed = ArrayProcessor(processed).apply_triangle_threshold()

                ap = ArrayProcessor(processed)
                processed, num_objects, props = ap.label_objects(
                    min_size=min_objectsize,
                    max_size=max_objectsize,
                    label_rgb=False,
                    orig_image=None,
                    bg_label=0,
                    measure_params=True,
                    measure_properties=("label", "area", "centroid", "bbox"),
                )

                # add well information for CZI metadata
                try:
                    props["WellId"] = mdata.sample.well_array_names[s]
                    props["Well_ColId"] = mdata.sample.well_colID[s]
                    props["Well_RowId"] = mdata.sample.well_rowID[s]
                except (IndexError, KeyError) as e:
                    logger.warning(f"No Well Information found for Scene: {s}")
                    props["WellId"] = s
                    props["Well_ColId"] = s
                    props["Well_RowId"] = s

                # add plane indices
                props["S"] = s
                props["T"] = t
                props["Z"] = z
                props["C"] = chindex

                # count the number of objects and update the dataframe
                values["Number"] = props.shape[0]
                objects = pd.concat(
                    [objects, pd.DataFrame(values, index=[0])], ignore_index=True
                )

                results = pd.concat([results, props], ignore_index=True)

                if add_polygons:

                    # add the polygons to the results for the current 2d plane of the CZI
                    results["polygon"] = create_xypoints(processed)
                    all_xy_scaled = []

                    # convert polygons to stageXY in [microns]
                    for obj_id in range(results.shape[0]):

                        # get list with X and Y positions for polygon
                        xpos, ypos = xy2stageXY(
                            image_stageX=stageX,
                            image_stageY=stageY,
                            sizeX=mdata.image.SizeX,
                            sizeY=mdata.image.SizeY,
                            scale=mdata.scale.X,
                            x=results["polygon"][obj_id][1],
                            y=results["polygon"][obj_id][0],
                        )

                        all_xy_scaled.append([xpos.tolist(), ypos.tolist()])

                    # add the polygon points for the objects for the current 2d plane
                    results["polygon_scaled"] = all_xy_scaled

                # add new axis for CZI writing and adapt pixel type
                processed = processed.astype("uint8")[..., np.newaxis]

                # write the plane with shape (Y, X, 1) to the new CZI file
                czidoc_w.write(
                    data=processed.astype("uint8"),
                    plane={"T": t, "Z": z, "C": chindex},
                    scene=s,
                )

        # check if valid scaling exists
        if mdata.scale.X is None:
            mdata.scale.X = 1.0
        if mdata.scale.Y is None:
            mdata.scale.Y = 1.0
        if mdata.scale.Y is None:
            mdata.scale.Z = 1.0

        czidoc_w.write_metadata(
            document_name=savepath_seg,
            channel_names={0: mdata.channelinfo.names[chindex] + "_seg"},
            scale_x=mdata.scale.X * 10**-6 * (1 / zoomlevel),
            scale_y=mdata.scale.Y * 10**-6 * (1 / zoomlevel),
            scale_z=mdata.scale.Z * 10**-6,
        )

        # rename columns in pandas data table
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

    logger.info(f"Finished writing to Segmented CZI File: {savepath_seg}")

    # write the CSV data table
    csvfile = misc.get_fname_woext(mdata.filename) + "_seg.csv"
    savepath_csv = os.path.join(savepath, csvfile)
    logger.info(f"Write to CSV File: {savepath_csv}")
    results.to_csv(savepath_csv, sep=";", index=False)

    return (savepath_seg, results, savepath_csv, objects)


def create_xypoints(segmented_image: np.ndarray) -> List[List]:
    """
    Create XY points from a segmented image.

    Args:
        segmented_image (np.ndarray): The segmented image.

    Returns:
        List[List]: A list of XY points for each polygon in the segmented image.
    """

    # find the contours
    contours = find_contours(segmented_image, level=0)

    # create list of polygons
    polygons = []
    for p in contours:
        poly = Polygon(p)
        poly = poly.simplify(5, preserve_topology=True)
        polygons.append(poly)

    all_xy_pos = []

    for p in polygons:

        # extract individual polygon
        xpos = p.exterior.coords.xy[0].tolist()
        ypos = p.exterior.coords.xy[1].tolist()
        xy_pos = [xpos, ypos]
        all_xy_pos.append(xy_pos)

    return all_xy_pos
