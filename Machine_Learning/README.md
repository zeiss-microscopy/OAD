# Machine Learning

## ZEN Intellesis Trainable Segmentation

Among many other powerful tools to process and analyze images the ZEN blue and ZEN core software platform offers the module **ZEN Intellesis Trainable Segmentation**, which is using machine-learning algorithms to segment images.

![Intellesis - Machine Learning Segmentation](../Images/intellesis_segmentation_tool.png)

## Key Features of Intellesis

- **Simple User Interface for Labelling and Training**

  - The tool aims for the non-expert by providing an **“easy-to-use” interface**.
  - The focus is to provide a **clean and simple workflow** to label the images and train a model.

- **Integration into ZEN Measurement Framework**

  - As segmentation is only the required first step for subsequent measurements the **integration into the actual measurement tools** is key.
  - Any Intellesis model can be **directly used inside Image Analysis workflows** as a segmentation tool.

- **Support for Multi-dimensional Data Sets**

  - Intellesis, especially when considering the BioFormats option, can be used to **segment any image** incl. 3rd party file formats from other vendors. It can handle multi-dimensional data sets like 3D stacks, Tiles, Multi-Channel, …

## Application Examples

ZEN can basically read any image data format using the BioFormats Import and Intellesis can therefore be used to segment **any multi-dimensional data set** that can be imported into the software. Shown below are images segmented using ZEN Intellesis Trainable Segmentation.

![ZEN Python](../Images/intellesis_ms_apps.png)

---

![ZEN Python](../Images/intellesis_ls_apps.png)

---

## Intellesis - Data Flow

The machine-learning part of Intellesis is entirely built upon Python-based tools.

![ZEN Python Modules](../Images/ZEN_Python_Tools.png)

The actual segmentation service is completely written in [Python](https://www.python.org) and is using proven and established open-source machine-learning libraries to segment the images.

To be able to handle even large multi-dimensional data sets, the software has a built-in data manager that takes care of splitting and distributing the workload depending on the available computational resources.

![ZEN Python](../Images/intellesis_dataflow.png "Intellesis - Data Flow")

More [detailed information](https://www.zeiss.com/microscopy/int/website/landingpages/zen-intellesis.html) and specific information regarding [ZEN core](https://www.zeiss.com/microscopy/int/products/microscope-software/zen-core.html#module) are available on the websites.

---

## Technical Specifications

- Machine-Learning Tool for Pixel Classification powered by **[Python](https://www.python.org), [Dask](https://dask.org/), [Scikit-Learn](https://scikit-learn.org/)** and **[Tensorflow 2](https://www.tensorflow.org/)**
- Real **Multi-Channel Feature Extraction** – all channels will be used to segment a pixel
- **Class Segmentation** – hierarchical structures with independent segmentation per class
  - every object can be segmented using it individual model
- Feature Extraction using **Engineered Feature Sets** and **Deep Feature Extraction**
  - Engineered Default Feature Sets (CPU)
    - 25 or 33 Features
  - Neural Network (vgg19) Layers for Feature Extraction (GPU)
    - 64, 128 (red. 50) or 256 (red. 70) Features for 1st, 2nd or 3rd layer of network
- Pixel Classification by proven and established **Random Forrest Classifier**
- Option to **Download** pre-trained DNNs for image segmentation (ZEN blue 3.1)
- Option to **Import** pre-trained DNNs for image segmentation(> ZEN blue 3.2)
  - currently two pre-trained networks are available
  - **[PyPi package czmodel & public ANN Model Specification](https://pypi.org/project/czmodel/)** to convert trained TF2 models into CZMODEL files
- Post processing using **Conditional Random Fields** (CRF) to improve the segmentation results
- Option to apply **confidence thresholds** to the segmentation results
- Processing functions for creating masks and **scripting integration** for advanced automation of machine learning workflows
- **Client-Server Architecture** (Zen Client - Python-Server) using a [REST-API](https://en.wikipedia.org/wiki/Representational_state_transfer)
- client-side tiling & fusion functionality to deal with large **Multi-Dimensional Data Sets**
- support for Nvidia GPUs

---

## General Workflows for Intellesis in ZEN

![Intellesis - Workflows](../Images/intellesis_workflows.png "Intellesis - Workflows")

---

## Importing a CZMODEL into ZEN blue or ZEN core

It is to import CZMODEL files in ZEN blue and in ZEN core.

### How to import a model in ZEN

To Import a model in ZEN use the **Import** model function inside ZEN blue or ZEN core.

<!--

![ZEN blue - Import Model](../Images/zen32_model_import_dialog.png "ZEN blue - Import Model")
*ZEN blue - Import Model*

![Select CZMODEL or JSON file](../Images/zen32_model_import_file.png "ZEN blue - Select CZMODEL or JSON file")
_ZEN blue - Select CZMODEL or JSON file_

![Select CZMODEL or JSON file](../Images/zen_core30_model_import.png)

-->

<p><img src="../Images/zen32_model_import_dialog.png" title="ZEN blue - Import Model" width="500"></p>

<p><img src="../Images/zen32_model_import_file.png" title="ZEN blue - Select CZMODEL or JSON file" width="500"></p>

<p><img src="../Images/zen_core30_model_import.png" title="ZEN core - Select CZMODEL or JSON file" width="500"></p>

---

### Importing externally trained networks into ZEN

Starting with ZEN blue 3.2 and ZEN core 3.1 it will be possible to import externally trained models into ZEN. To import such a file just use the normal import function mentioned above. The general idea here is:

![Importing External Networks](../Images/intellesis_dataflow_czmodel.png)

- the ZEISS Custom-Solution Team, a researcher or any 3rd party trains its specific neural network
- The **[PyPi package czmodel](https://pypi.org/project/czmodel/)** is used to concert and package the network into a CZMODEL file
- the file is imported into ZEN using the normal **Import** mechanism

For more details please se the **[Importing External Networks](../Machine_Learning/docs/README.md)**

### Downloading a model (ZEN blue 3.1 only)

ZEN blue 3.1 has the option to download pre-trained networks from ZEISS. Such networks are fully integrated into the ZEN Image Analysis framework and can be used the same way as the other Intellesis models using pixel classification.

<!--
![ZEN Intellesis - Model Download](../Images/intellesis_model_download.png)
-->

<p><img src="../Images/intellesis_model_download.png" title="ZEN blue 3.1 - Model Download" width="400"></p>

---

## Model Downloads

ZEN allows to import pre-trained neural networks and also provided some example that can be downloaded. Those networks can be used inside any segmentation or image analysis workflow in ZEN.

<p><img src="../Images/class_segmentation_cnn.png" title="Class Segmentation using pre-trained DNN" width="500"></p>


### Nucleus Detection using UNet

The trained networks for cell nucleus detection (available for download) are based on the well known UNet network architecture and are using a vgg16 encoder. The general structure is shown below. The numbers below the network layers represent the actual number of feature maps (per layer) and the array size is shown above the layers.

<p><img src="../Images/ZEN_UNet_vgg16_v1.png" title="UNet architecture for nucleus detetction network" ></p>


#### UNet Nucleus Detector (GrayScale)

UNet-based Deep Neural Network (TensorFlow 2) for cell nucleus detection (grayscale). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

**Download here: [UNet Nucleus Segmentation (GrayScale)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nucleus_segmentation_grayscale_v2.czmodel?sv=2018-03-28&sr=b&sig=nQREzvO5673WA7M7EAUwa4FDgd%2BMKn96XS%2FrxFl%2BF04%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

#### UNet Nucleus Detector (RGB)

UNet-based Deep Neural Network (TensorFlow 2) for cell nucleus detection (RGB). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

**Download here: [UNet Nucleus Segmentation (RGB)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nuclei_segmentation_rgb_v2.czmodel?sv=2018-03-28&sr=b&sig=aHs0r5ovW1ELEgCOhjUq3nYVqCuhAhTT2nttjWI5rdU%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

---

### Conditions of Use

_These pre-trained networks were trained with "best-effort" on the available training data and is (are) provided "as is" without warranty of any kind. The licensor assumes no responsibility for the functionality and fault-free condition of the pre-trained network under conditions which are not in the described scope. Be aware that no pre-trained network will perform equally good on any sample, especially not on samples it was not trained for. Therefore, use such pre-trained networks at your own risks and it is up to the user to evaluate and decide if the obtained segmentation results are valid for the images currently segmented using such a network. For details see the respective chapter in the Online Help / Documentation. By downloading and using the networks I agree to the above terms._

### Scripting Integration

Most functions regarding Intellesis can be scripted via Python in ZEN in order to automate and customize workflows. Check out the [scripts](../Machine_Learning/scripts/README.md) for some simple examples.

````python
def classify(image, model,
             use_confidence=True,
             confidence_threshold=0,
             format=ZenSegmentationFormat.MultiChannel):

    # classify pixels using a trained model
    if use_confidence:
        try:
            # run the segmentation and apply confidence threshold to segmented image
            outputs = Zen.Processing.Segmentation.TrainableSegmentationWithProbabilityMap(image, model, segf)
            seg_image = outputs[0]
            prop_map = outputs[1]
            seg_image = Zen.Processing.Segmentation.MinimumConfidence(seg_image, prop_map, confidence_threshold)
            prop_map.Close()
            del outputs
        except ApplicationException as e:
            seg_image = None
            print('Application Exception : '), e.Message

    if not use_confidence:
        try:
            # run the segmentation
            seg_image = Zen.Processing.Segmentation.TrainableSegmentation(image, model, segf)
        except ApplicationException as e:
            seg_image = None
            print('Application Exception : '), e.Message

    return seg_image
    ```
````
