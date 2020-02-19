# ANN Model Specification
This document specifies the requirements for an artificial neural network (ANN) model and the additionally required metadata to enable execution of the model inside the ZEN Intellesis infrastructure.

## Core network structure and file format  

To be usable in the SegmentationService infrastructure a neural network model must comply with the specified rules below.
- The model must be provided as a [TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model). 
- All operations in the contained execution graph must be supported by TensorFlow 2.0.0.
- The model currently must provide one input and one output node. Multiple inputs and outputs are not supported.
- The shape of the input node must have 4 dimensions where the first dimension specifies the batch size, the second and third dimensions specify the width and height of the expected input image and the third dimension represents the number of color channels.
- The batch dimension of the input node must be undefined or 1.
- The spatial dimension of the input image implicitly defines the maximum tile size of the model. Our infrastructure will ensure that all input images exactly match the specified dimensions. The spatial dimensions of the input node must be such that the model can be evaluated on the minimum required hardware (currently 8GB GPU memory) without running out of memory.
- The output node must have the same shape as the input node except for the last dimension that represents the class probabilities. The size of the last dimension of the output must be the number of classes. The values of the output tensor must represent the class probabilities for each pixel. I.e. values must lie in the [0...1] range and summing the output over the last dimension must produce an all-1 tensor (within numeric accuracy). Softmax activation can be used to turn logits into such probabilities.
- All types of pre-processing and post-processing (except the currently supported Conditional Random Field post-processing) e.g. normalization, standardization, down-sampling etc. must be included in the provided TensorFlow model so that no further action by the inference engine is needed before or after inference to obtain the expected results. 

## Model Metadata
Executing an ANN model within the Intellesis infrastructure requires additional meta information that needs to be provided along with the serialized model specified by the [Core network structure and file format](#core-network-structure-and-file-format).
Meta information for the ANN model must be provided in a separate JSON file adhering to [RFC8259](https://tools.ietf.org/html/rfc8259) that must contain the following attributes:
- **BorderSize (Type: int)**: For Intellesis models this attribute defines the size of the border that needs to be added to an input image such that there are no border effects visible in the required area of the generated segmentation mask. For deep architectures this value can be infeasibly large so that the border size must be defined in a way that the border effects are “acceptable” in the ANN model creator’s opinion.
- **ColorHandling (Type: string)**: Specifies how color (RGB and RGBA) pixel data are converted to one or more channels of scalar pixel data. Possible values are: 
  - ConvertToMonochrome (Converts color to gray scale)
  - SplitRgb (Keeps the pixel representation in RGB space)
- **PixelType (Type: string)**: The expected input type of the model. Possible values are:
  - **Gray8**: 8 bit unsigned
  - **Gray16**: 16 bit unsigned
  - **Gray32Float**: 4 byte IEEE float
  - **Bgr24**: 8 bit triples, representing the color channels Blue, Green and Red
  - **Bgr48**: 16 bit triples, representing the color channels Blue, Green and Red
  - **Bgr96Float**: Triple of 4 byte IEEE float, representing the color channels Blue, Green and Red
  - **Bgra32**: 8 bit triples followed by an alpha (transparency) channel
  - **Gray64ComplexFloat**: 2 x 4 byte IEEE float, representing real and imaginary part of a complex number
  - **Bgr192ComplexFloat**: A triple of 2 x 4 byte IEEE float, representing real and imaginary part of a complex number, for the color channels Blue, Green and Red
- **Classes (Type: array, Value type: string)**: A list of class names corresponding to the output dimensions of the predicted segmentation mask. If the last dimension of the prediction has shape n the provided list must be of length n.
- **ModelPath (Type: string)**: The path to the exported neural network model. Can be absolute or relative to the JSON file.


The file may also contain the following optional attributes:
- **TestImageFile (Type: string)**: The path to a test image in a format supported by ZEN. This image is used for basic validation of the converted model inside ZEN. Can be absolute or relative to the JSON file.
- **LicenseFile (Type: string)**: The path to a license file that is added to the generated CZModel. Can be absolute or relative to the JSON file.

Json files can contain escape sequences and \\-characters in paths must be escaped with \\\\.  

The following code snippet shows an example for a valid metadata file:
```json
{
  "BorderSize": 90,
  "ColorHandling": "ConvertToMonochrome",
  "PixelType": "Gray16",
  "Classes": ["Background", "Interesting Object", "Foreground"],
  "ModelPath": "C:\\tf\\saved\\model\\folder\\",
  "TestImageFile": "C:\\test-image.png",
  "LicenseFile": "C:\\LICENSE.txt"
}
```
