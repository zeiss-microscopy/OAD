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
