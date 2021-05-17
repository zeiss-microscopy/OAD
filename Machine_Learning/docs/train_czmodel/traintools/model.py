import os
import tensorflow as tf
from tensorflow.keras.layers import Concatenate, Input, Conv2D, BatchNormalization, Activation, MaxPool2D
from tensorflow.keras.layers import Dropout, Conv2DTranspose, UpSampling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from czmodel.util.preprocessing import PerImageStandardization
#import segmentation_models as sm

def build_model(start_filters,
                numchannels=1,
                numclasses=2,
                perimagestd=False,
                kernelsize=3,
                learning_rate=1e-3,
                dropout=0.15,
                metrics='categorical_accuracy'):

    # generate layers
    inputs = Input((None, None, numchannels))

    # standardize per image
    if perimagestd:
        inputs = PerImageStandardization()(inputs)

    # conv part
    conv1 = conv_block(inputs, start_filters * 1)
    #conv1 = conv_block(standardized_inputs, start_filters * 1)
    pool1 = MaxPool2D((2, 2))(conv1)
    pool1 = Dropout(dropout)(pool1)

    conv2 = conv_block(pool1, start_filters * 2)
    pool2 = MaxPool2D((2, 2))(conv2)
    pool2 = Dropout(dropout * 2)(pool2)

    conv3 = conv_block(pool2, start_filters * 4)
    pool3 = MaxPool2D((2, 2))(conv3)
    pool3 = Dropout(dropout * 2)(pool3)

    conv4 = conv_block(pool3, start_filters * 8)
    pool4 = MaxPool2D((2, 2))(conv4)
    pool4 = Dropout(dropout * 2)(pool4)
    
    #conv5 = conv_block(pool4, start_filters * 16)
    #pool5 = MaxPool2D((2, 2))(conv5)
    #pool5 = Dropout(dropout * 2)(pool5)

    # Middle
    convm = conv_block(pool4, start_filters * 16)

    # upconv part
    #deconv5 = UpSampling2D()(convm)
    #uconv5 = Concatenate()([deconv5, conv5])
    #uconv5 = Dropout(dropout * 2)(uconv5)
    #uconv5 = conv_block(uconv5, start_filters * 16)
    
    deconv4 = UpSampling2D()(convm)
    uconv4 = Concatenate()([deconv4, conv4])
    uconv4 = Dropout(dropout * 2)(uconv4)
    uconv4 = conv_block(uconv4, start_filters * 8)

    deconv3 = UpSampling2D()(uconv4)
    uconv3 = Concatenate()([deconv3, conv3])
    uconv3 = Dropout(dropout * 2)(uconv3)
    uconv3 = conv_block(uconv3, start_filters * 4)

    deconv2 = UpSampling2D()(uconv3)
    uconv2 = Concatenate()([deconv2, conv2])
    uconv2 = Dropout(dropout * 2)(uconv2)
    uconv2 = conv_block(uconv2, start_filters * 2)

    deconv1 = UpSampling2D()(uconv2)
    uconv1 = Concatenate()([deconv1, conv1])
    uconv1 = Dropout(dropout * 2)(uconv1)
    uconv1 = conv_block(uconv1, start_filters * 1)
    output_layer = Conv2D(numclasses, 1, padding='same', activation='softmax')(uconv1)

    model = Model(inputs=inputs, outputs=output_layer)
    
    if metrics == 'categorical_accuracy':
    
        model.compile(
            loss="categorical_crossentropy",
            optimizer=Adam(lr=learning_rate),
            metrics=['categorical_accuracy']
        )
        
    if metrics == 'iou':
    
        model.compile(
            loss="categorical_crossentropy",
            optimizer=Adam(lr=learning_rate),
            metrics=[tf.keras.metrics.MeanIoU(num_classes=numclasses)]
        )

    return model

def conv_block(inputs, filters, kernel_size=3, initializer='he_normal'):

    x = Conv2D(filters, kernel_size, padding="same", kernel_initializer=initializer)(inputs)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    x = Conv2D(filters, kernel_size, padding="same", kernel_initializer=initializer)(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    return x

def build_unet(backbone='mobilenet',
               numclasses=2,
               activation='softmax',
               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
               metrics=['accuracy',sm.metrics.IOUScore(threshold=0.5)],
               weights=[1],
               encoder_weights='imagenet',
               encoder_freeze=True):

    # backbones = ['mobilenet','mobilenetv2','inceptionv3','resnet18','resnet34','resnet50','resnet101','resnet152'])

    #Model
    model = sm.Unet(backbone, encoder_weights=encoder_weights,classes=numclasses, activation=activation, encoder_freeze=encoder_freeze)
    model.compile('adam', loss, metrics, loss_weights=weights)
    
    return model


import numpy as np
import keras.backend as K
import tensorflow as tf

def metrics_np(y_true, y_pred, metric_name, metric_type='standard', drop_last = True, mean_per_class=False, verbose=False):
    """ 
    Compute mean metrics of two segmentation masks, via numpy.
    
    IoU(A,B) = |A & B| / (| A U B|)
    Dice(A,B) = 2*|A & B| / (|A| + |B|)
    
    Args:
        y_true: true masks, one-hot encoded.
        y_pred: predicted masks, either softmax outputs, or one-hot encoded.
        metric_name: metric to be computed, either 'iou' or 'dice'.
        metric_type: one of 'standard' (default), 'soft', 'naive'.
          In the standard version, y_pred is one-hot encoded and the mean
          is taken only over classes that are present (in y_true or y_pred).
          The 'soft' version of the metrics are computed without one-hot 
          encoding y_pred.
          The 'naive' version return mean metrics where absent classes contribute
          to the class mean as 1.0 (instead of being dropped from the mean).
        drop_last = True: boolean flag to drop last class (usually reserved
          for background class in semantic segmentation)
        mean_per_class = False: return mean along batch axis for each class.
        verbose = False: print intermediate results such as intersection, union
          (as number of pixels).
    Returns:
        IoU/Dice of y_true and y_pred, as a float, unless mean_per_class == True
          in which case it returns the per-class metric, averaged over the batch.
    
    Inputs are B*W*H*N tensors, with
        B = batch size,
        W = width,
        H = height,
        N = number of classes
    """
    
    assert y_true.shape == y_pred.shape, 'Input masks should be same shape, instead are {}, {}'.format(y_true.shape, y_pred.shape)
    assert len(y_pred.shape) == 4, 'Inputs should be B*W*H*N tensors, instead have shape {}'.format(y_pred.shape)
    
    flag_soft = (metric_type == 'soft')
    flag_naive_mean = (metric_type == 'naive')
    
    num_classes = y_pred.shape[-1]
    # if only 1 class, there is no background class and it should never be dropped
    drop_last = drop_last and num_classes>1
    
    if not flag_soft:
        if num_classes>1:
            # get one-hot encoded masks from y_pred (true masks should already be in correct format, do it anyway)
            y_pred = np.array([ np.argmax(y_pred, axis=-1)==i for i in range(num_classes) ]).transpose(1,2,3,0)
            y_true = np.array([ np.argmax(y_true, axis=-1)==i for i in range(num_classes) ]).transpose(1,2,3,0)
        else:
            y_pred = (y_pred > 0).astype(int)
            y_true = (y_true > 0).astype(int)
    
    # intersection and union shapes are batch_size * n_classes (values = area in pixels)
    axes = (1,2) # W,H axes of each image
    intersection = np.sum(np.abs(y_pred * y_true), axis=axes) # or, np.logical_and(y_pred, y_true) for one-hot
    mask_sum = np.sum(np.abs(y_true), axis=axes) + np.sum(np.abs(y_pred), axis=axes)
    union = mask_sum  - intersection # or, np.logical_or(y_pred, y_true) for one-hot
    
    if verbose:
        print('intersection (pred*true), intersection (pred&true), union (pred+true-inters), union (pred|true)')
        print(intersection, np.sum(np.logical_and(y_pred, y_true), axis=axes), union, np.sum(np.logical_or(y_pred, y_true), axis=axes))
    
    smooth = .001
    iou = (intersection + smooth) / (union + smooth)
    dice = 2*(intersection + smooth)/(mask_sum + smooth)
    
    metric = {'iou': iou, 'dice': dice}[metric_name]
    
    # define mask to be 0 when no pixels are present in either y_true or y_pred, 1 otherwise
    mask =  np.not_equal(union, 0).astype(int)
    # mask = 1 - np.equal(union, 0).astype(int) # True = 1
    
    if drop_last:
        metric = metric[:,:-1]
        mask = mask[:,:-1]
    
    # return mean metrics: remaining axes are (batch, classes)
    # if mean_per_class, average over batch axis only
    # if flag_naive_mean, average over absent classes too
    if mean_per_class:
        if flag_naive_mean:
            return np.mean(metric, axis=0)
        else:
            # mean only over non-absent classes in batch (still return 1 if class absent for whole batch)
            return (np.sum(metric * mask, axis=0) + smooth)/(np.sum(mask, axis=0) + smooth)
    else:
        if flag_naive_mean:
            return np.mean(metric)
        else:
            # mean only over non-absent classes
            class_count = np.sum(mask, axis=0)
            return np.mean(np.sum(metric * mask, axis=0)[class_count!=0]/(class_count[class_count!=0]))
        
def mean_iou_np(y_true, y_pred, **kwargs):
    """
    Compute mean Intersection over Union of two segmentation masks, via numpy.
    
    Calls metrics_np(y_true, y_pred, metric_name='iou'), see there for allowed kwargs.
    """
    return metrics_np(y_true, y_pred, metric_name='iou', **kwargs)

def mean_dice_np(y_true, y_pred, **kwargs):
    """
    Compute mean Dice coefficient of two segmentation masks, via numpy.
    
    Calls metrics_np(y_true, y_pred, metric_name='dice'), see there for allowed kwargs.
    """
    return metrics_np(y_true, y_pred, metric_name='dice', **kwargs)