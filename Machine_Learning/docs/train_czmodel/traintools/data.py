import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
#import cv2

from pathlib import Path

from tkinter import filedialog
from tkinter import *

import albumentations as A

#from lib.model import define_modeltype

#TEST_SIZE = 0.2

def load_training_paths():

    # change to current script path
    abspath = os.path.abspath(sys.argv[0])
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # request input and output image path from user
    root = Tk()
    root.withdraw()
    input_path = filedialog.askdirectory(title="select folder with input images",
                                     initialdir=os.path.join(os.getcwd(), "data"))
    output_path = filedialog.askdirectory(title="select folder with output images",
                                     initialdir=Path(input_path).parent)
    model_path = Path(input_path).parent
    print("Directory for input images...", input_path)
    print("Directory for output image...", output_path)

    return input_path, output_path

def load_prediction_paths():

    # change to current script path
    abspath = os.path.abspath(sys.argv[0])
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # ask folder for input images and network model from user
    root = Tk()
    root.withdraw()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    input_path = filedialog.askdirectory(title="select folder with input images",
                                         initialdir=os.path.join(os.getcwd(), "data"))
    model_path = filedialog.askopenfilename(title="select model",
                                            initialdir=Path(input_path).parent)

    print("Directory for input images...", input_path)
    print("File path for model...", model_path)

    return input_path, model_path

def load_data(inputPath, filelist):

    data = np.array([cv2.imreadmulti(os.path.join(inputPath, file),
                                     flags=cv2.IMREAD_UNCHANGED)[1] for file in filelist])

    data = np.swapaxes(data, 1, 3)
    return np.swapaxes(data, 1, 2)

def load_training_data(inputPath, outputPath):

    filelist = os.listdir(outputPath)

    data_input = load_data(inputPath, filelist)
    data_output = load_data(outputPath, filelist)

    train_input, valid_input, train_output, valid_output = train_test_split(data_input, data_output,
                                                                            shuffle=True,
                                                                            test_size=TEST_SIZE)

    return (train_input, valid_input), (train_output, valid_output)

def load_prediction_data(inputPath):
    """
    :param inputPath: folder containing images to be predicted
    :return: data = numpy array with image data already properly preprocessed;
             filelist = list of original image names
    """
    filelist = os.listdir(inputPath) # get image file names

    data = load_data(inputPath, filelist) # load data path
    data = preprocess_images(data) # preprocess data (uint to floating point...)

    return data, filelist


def random_crop_and_pad_image_and_label(image, label, size):
    """Randomly crops image together with labels.

    Args:
      image: A Tensor with shape [D_1, ..., D_K, N]
      label: A Tensor with shape [D_1, ..., D_K, M]
      size: A Tensor with shape [K] indicating the crop size.
    Returns:
      A tuple of (cropped_image, cropped_label).
    """
    
    combined = tf.concat([image, label], axis=-1)
    image_shape = tf.shape(image)
    combined_pad = tf.image.pad_to_bounding_box(combined, 0, 0,
                                                tf.maximum(size[0], image_shape[0]),
                                                tf.maximum(size[1], image_shape[1]))
    
    last_label_dim = tf.shape(label)[-1]
    last_image_dim = tf.shape(image)[-1]
    
    combined_crop = tf.image.random_crop(combined_pad,
                                         size=tf.concat([size, [last_label_dim + last_image_dim]],
                                                        axis=0))
    
    return (combined_crop[:, :, :last_image_dim], combined_crop[:, :, last_image_dim:])


def reorder_labels(mask):
    for i, unique_value in enumerate(np.unique(mask)):
        mask[mask == unique_value] = i
    return mask

def aug_wo_crop():
    transform = A.Compose([
                    A.HorizontalFlip(p=1.0),
                    A.VerticalFlip(p=1.0),
                    A.RandomRotate90(p=1.0),
                    A.Transpose(p=1.0),
                    A.ShiftScaleRotate(shift_limit=0.01, scale_limit=0.04, rotate_limit=0, p=1.0),
                    A.Blur(p=1.0, blur_limit = 3),
                    A.OneOf([
                        A.ElasticTransform(p=1.0, alpha=120, sigma=120 * 0.05, alpha_affine=120 * 0.03),
                        A.GridDistortion(p=1.0),
                        A.OpticalDistortion(p=1.0, distort_limit=1, shift_limit=0.1)                  
                    ],
                    p=1.0)
                ], p = 1)
    
    return transform


def aug_crop_only(image_size = 256, crop_prob = 1):
    transform = A.Compose([
                    A.RandomCrop(width = image_size, height = image_size, p=crop_prob)], p = 1)
    return transform



