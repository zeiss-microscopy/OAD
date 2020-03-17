# Pre-trained Model

## How to import

This is simple - just use the **Import** model function inside ZEN.

![Open Import Model Dialog](../../Images/zen32_model_import_dialog.png)

![Select CZMODEL or JSON file](../../Images/zen32_model_import_file.png)

---

## Models - Pixel Classification

An example for a trained model ready to be used inside ZEN blue or ZEN core see:

[Model - Pixel Classification](../Machine_Learning/models/../../models/models_pixel_classification/XRM_Sandstone_Default_Features_Demo.czmodel).

It can be applied to [3D XRM Stack Sandstone](../Machine_Learning/../testdata/XRM_Testimage.czi) dataset.

---

## Models - Pre-Trained ANN for Segmentation

ZEN allows to import pre-trained neural networks. Currently ZEISS provided the following examples for such networks:

### UNet - Nucleus Detector GrayScale

UNet-based Deep Neural Network for cell nucleus detection (grayscale). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

To download the network click here: **[UNet Nucleus Segmentation (GrayScale)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nucleus_segmentation_grayscale_v2.czmodel?sv=2018-03-28&sr=b&sig=nQREzvO5673WA7M7EAUwa4FDgd%2BMKn96XS%2FrxFl%2BF04%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

### UNet - Nucleus Detector RGB

UNet-based Deep Neural Network for cell nucleus detection (RGB). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

To download the network click here: **[UNet Nucleus Segmentation (RGB)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nuclei_segmentation_rgb_v2.czmodel?sv=2018-03-28&sr=b&sig=aHs0r5ovW1ELEgCOhjUq3nYVqCuhAhTT2nttjWI5rdU%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

## Conditions of Use

_This pre-trained network was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind. The licensor assumes no responsibility for the functionality and fault-free condition of the pre-trained network under conditions which are not in the described scope. For details see the respective chapter in the Online Help / Documentation. By downloading I agree to the above terms._
