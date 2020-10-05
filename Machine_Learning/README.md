- [ZEN - Open Ecosystem for Integrated Machine Learning Workflows](#zen---open-ecosystem-for-integrated-machine-learning-workflows)
  - [ZEN Intellesis Trainable Segmentation](#zen-intellesis-trainable-segmentation)
  - [2. Key Features of Intellesis](#2-key-features-of-intellesis)
  - [3. ZEN ML Landscape](#3-zen-ml-landscape)
  - [4. Application Examples](#4-application-examples)
  - [5. Intellesis - Data Flow](#5-intellesis---data-flow)
  - [6. Technical Specifications](#6-technical-specifications)
  - [7. General Workflows for Intellesis in ZEN](#7-general-workflows-for-intellesis-in-zen)
  - [8. Importing a CZMODEL into ZEN blue or ZEN core](#8-importing-a-czmodel-into-zen-blue-or-zen-core)
    - [8.1. How to import a model in ZEN](#81-how-to-import-a-model-in-zen)
    - [8.2. Importing externally trained networks into ZEN](#82-importing-externally-trained-networks-into-zen)
    - [8.3. Example Workflow - Tarin and Import a network to segment a stack](#83-example-workflow---tarin-and-import-a-network-to-segment-a-stack)
  - [9. Model Downloads](#9-model-downloads)
    - [9.1. Application Example - Robust Nucleus Detection using UNet](#91-application-example---robust-nucleus-detection-using-unet)
      - [9.1.1. UNet Nucleus Detector (GrayScale)](#911-unet-nucleus-detector-grayscale)
      - [9.1.2. UNet Nucleus Detector (RGB)](#912-unet-nucleus-detector-rgb)
    - [9.2. Example Networks - Conditions of Use](#92-example-networks---conditions-of-use)
  - [10. Integrated Workflows using trained models](#10-integrated-workflows-using-trained-models)
    - [10.1. Use UNet Nucleus Detector for Zone-of-Influence workflow](#101-use-unet-nucleus-detector-for-zone-of-influence-workflow)
    - [10.2. Use trained model to reliably detect layers](#102-use-trained-model-to-reliably-detect-layers)
  - [11. Scripting Integration](#11-scripting-integration)

---

# ZEN - Open Ecosystem for Integrated Machine Learning Workflows

## ZEN Intellesis Trainable Segmentation

Among many other powerful tools to process and analyze images the ZEN blue and ZEN core software platform offers the module **ZEN Intellesis Trainable Segmentation**, which is using machine-learning algorithms to segment images.

![Intellesis - Machine Learning Segmentation](../Images/intellesis_segmentation_tool.png)

## 2. Key Features of Intellesis

- **Simple User Interface for Labelling and Training**

  - The tool aims for the non-expert by providing an **“easy-to-use” interface**.
  - The focus is to provide a **clean and simple workflow** to label the images and train a model.
  - Label your datasets using clean and simple UI in ZEN Intellesis or using [APEER Annotate](https://www.apeer.com/annotate)

- **Integration into ZEN Measurement and Processing Framework**

  - As segmentation is only the required first step for subsequent measurements the **integration into the actual measurement tools** is key.
  - Any Intellesis model can be **directly used inside Image Analysis workflows** as a segmentation tool.

- **Open Platform - Import your own trained models**

  - Import your own model and use it seamlessly integrated in ZEN workflows and benefit from Image Tiling & Fusion client
  - Use the open-source python package [**czmodel**](https://pypi.org/project/czmodel/) to "package your model to be used in the ZEN ecosystem.

- **Support for Multi-dimensional Data Sets**

  - Intellesis, especially when considering the BioFormats option, can be used to **segment any image** incl. 3rd party file formats from other vendors
  - It can handle multi-dimensional data sets like 3D stacks, Tiles, Multi-Channel, …

---

## 3. ZEN ML Landscape

The sketch below outlines "the bigger" picture and vision and will be updated frequently. The most important points to consider here are:

- the “exchange” currency inside this ecosystem is the trained model (czmodel)
- the the open-source python package [**czmodel**](https://pypi.org/project/czmodel/) allows everybody to import their own models in ZEN
- skilled researcher nad programmers can train theri models where the like and still deploy the for "their" users in ZEN or on the APEER platform
- one can use pre-trained models from ZEISS or get a model trained as a service (includes the label process)
- on the [APEER platform](www.apeer.com) it is possible to label your own data and train model (coming soon)

![ZEN Machine Learning Landscape](../Images/ZEN_ML_Landscape_simple.png)

---

## 4. Application Examples

ZEN can basically read any image data format using the BioFormats Import and Intellesis can therefore be used to segment **any multi-dimensional data set** that can be imported into the software. Shown below are images segmented using ZEN Intellesis Trainable Segmentation.

![ZEN Python](../Images/intellesis_ms_apps.png)

---

![ZEN Python](../Images/intellesis_ls_apps.png)

---

## 5. Intellesis - Data Flow

The machine-learning part of Intellesis is entirely built upon Python-based tools.

![ZEN Python Modules](../Images/ZEN_Python_Tools.png)

The actual segmentation service is completely written in [Python](https://www.python.org) and is using proven and established open-source machine-learning libraries to segment the images. More [detailed information](https://www.zeiss.com/microscopy/int/website/landingpages/zen-intellesis.html) and specific information regarding [ZEN core](https://www.zeiss.com/microscopy/int/products/microscope-software/zen-core.html#module) are available on the respective websites.

To be able to handle even large multi-dimensional data sets, the software has a built-in data manager that takes care of splitting and distributing the workload depending on the available computational resources.

![Intellesis - ML Data Flow - Training](../Images/intellesis_dataflow_training.png "Intellesis - ML Data Flow - Training")**Intellesis - ML Data Flow - Training**

---

![Intellesis - ML Data Flow - Prediction](../Images/intellesis_dataflow_prediction.png "Intellesis - ML Data Flow - Prediction")**Intellesis - ML Data Flow - Prediction**

---

## 6. Technical Specifications

- Machine-Learning Tool for Pixel Classification powered by **[Python](https://www.python.org), [Dask](https://dask.org/), [Scikit-Learn](https://scikit-learn.org/)** and **[Tensorflow 2](https://www.tensorflow.org/)**
- Real **Multi-Channel Feature Extraction** – all channels will be used to segment a pixel
- **Class Segmentation** – hierarchical structures with independent segmentation per class
  - every object can be segmented using it individual model
- Feature Extraction using **Engineered Feature Sets** and **Deep Feature Extraction** (see also [Feature Extractors](../Machine_Learning/Feature_Extractors/feature_extractors.md) for more details)
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

## 7. General Workflows for Intellesis in ZEN

![Intellesis - Workflows](../Images/intellesis_workflows.png "Intellesis - Workflows")

---

## 8. Importing a CZMODEL into ZEN blue or ZEN core

It is possible to export and import import \*.czmodel files, which contain the trained segmentation model, in ZEN blue and in ZEN core.

### 8.1. How to import a model in ZEN

To Import a model in ZEN use the **Import** model function inside ZEN blue or ZEN core.

<p><img src="../Images/zen32_model_import_dialog.png" title="ZEN blue - Import Model" width="600"></p>

<p><img src="../Images/zen32_model_import_file.png" title="ZEN blue - Select CZMODEL or JSON file" width="600"></p>

<p><img src="../Images/zen_core30_model_import.png" title="ZEN core - Select CZMODEL or JSON file" width="600"></p>

---

### 8.2. Importing externally trained networks into ZEN

Starting with ZEN blue 3.2 and ZEN core 3.1 it will be possible to import externally trained models into ZEN. To import such a file just use the normal import function mentioned above. The general idea here is:

![Importing External Networks](../Images/intellesis_dataflow_czmodel.png)

- the ZEISS Custom-Solution Team, a researcher or any 3rd party trains its specific neural network
- The **[PyPi package czmodel](https://pypi.org/project/czmodel/)** is used to concert and package the network into a CZMODEL file
- the file is imported into ZEN using the normal **Import** mechanism
- from here on the network can be used inside the ZEN Image Analysis and Processing Function and also inside **[Guided Acquisition Workflows](https://github.com/zeiss-microscopy/OAD/tree/39dbefaaaf4ede1492a4f9c8c12ea56f9b90cb0e/Guided_Acquisition)**

For more details please se the **[Importing External Networks](../Machine_Learning/docs/README.md)**

### 8.3. Example Workflow - Tarin and Import a network to segment a stack

To illustrate the general idea of using externally trained networks the followings steps have to be considered.

- A model was trained inside a jupyter notebook
- By using the **CZMODEL** the saved model was packed to be then imported in ZEN
- **If needed the process of labeling the data and training a network can be also provide by ZEISS as a commercial service.**
- The result of your own training or the training service will be a trained model ready to be in your own environment, on the APEER platform or inside the ZEN software platform.

![Intellesis - Use imported DNN to segment your data](../Images/workflow_model_em1.png)

To illustrate the workflow a public available dataset with labels: [Segmentation of neuronal structures in EM stacks challenge](https://imagej.net/Segmentation_of_neuronal_structures_in_EM_stacks_challenge_-_ISBI_2012.html#Test_data) was used to trains a simple network.

![Intellesis - Use imported DNN to segment your data](../Images/dnn_em-membranes_segmented_1.gif)

---

## 9. Model Downloads

ZEN allows to import pre-trained neural networks and also provided some example that can be downloaded. Those networks can be used inside any segmentation or image analysis workflow in ZEN.

<p><img src="../Images/class_segmentation_cnn.png" title="Class Segmentation using pre-trained DNN" width="500"></p>

### 9.1. Application Example - Robust Nucleus Detection using UNet

The trained networks for cell nucleus detection (available for download) are based on the well known UNet network architecture and are using a vgg16 encoder. The general structure is shown below. The numbers below the network layers represent the actual number of feature maps (per layer) and the array size is shown above the layers.

<p><img src="../Images/ZEN_UNet_vgg16_v1.png" title="UNet architecture for nucleus detection network" ></p>

#### 9.1.1. UNet Nucleus Detector (GrayScale)

UNet-based Deep Neural Network (TensorFlow 2) for cell nucleus detection (grayscale). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

**Download here: [UNet Nucleus Segmentation (GrayScale)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nucleus_segmentation_grayscale_v2.czmodel?sv=2018-03-28&sr=b&sig=nQREzvO5673WA7M7EAUwa4FDgd%2BMKn96XS%2FrxFl%2BF04%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

#### 9.1.2. UNet Nucleus Detector (RGB)

UNet-based Deep Neural Network (TensorFlow 2) for cell nucleus detection (RGB). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

**Download here: [UNet Nucleus Segmentation (RGB)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nuclei_segmentation_rgb_v2.czmodel?sv=2018-03-28&sr=b&sig=aHs0r5ovW1ELEgCOhjUq3nYVqCuhAhTT2nttjWI5rdU%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

---

### 9.2. Example Networks - Conditions of Use

_These pre-trained networks were trained with "best-effort" on the available training data and is (are) provided "as is" without warranty of any kind. The licensor assumes no responsibility for the functionality and fault-free condition of the pre-trained network under conditions which are not in the described scope. Be aware that no pre-trained network will perform equally good on any sample, especially not on samples it was not trained for. Therefore, use such pre-trained networks at your own risks and it is up to the user to evaluate and decide if the obtained segmentation results are valid for the images currently segmented using such a network. For details see the respective chapter in the Online Help / Documentation. By downloading and using the networks I agree to the above terms._

---

## 10. Integrated Workflows using trained models

### 10.1. Use UNet Nucleus Detector for Zone-of-Influence workflow

Once an externally trained model is imported (or was trained in ZEN) it can be plugged into any ZEN image analyis pipeline using a feature called **Class Segmentation**. The general idea is to set up a measurement hierachy for the objects and the plugin trained models were needed, for example to robustly detect stained cell nuclei.

This approach also allows to mix machine-learning based segmentation with classical methods like "simple" thresholding approaches. As an example, the rocust nucleus detection using a pre-trained network is an ideal segmentation method to be used to segment the \*\*Primary Objects" inside a so-called "Zone-of-Influence" segmentation as shown below

1. Plugin the imported model into the class **Primary Objects** to robustly detect the stained cell nuclei inside a specific channel
2. Use this primary object to define a **Ring** around every detect cell nucleus
3. Define further subclasses as needed and segment them using other models or by applying an automated threshold
4. Run the complete image analysis pipeline incl. the model execution without having to worry about tile sizes, patches etc. and visualize the results easily

![Class Segmentation - Plugin UNet to detect cell nuclei](../Images/class_seg_dnn1.png)

![Class Segmentation - Easily analyze data and visualize the results](../Images/class_seg_dnn2.png)

### 10.2. Use trained model to reliably detect layers

Trained models can be also used inside so-called "Material Modules" like **Layer Thickness**, which is outlined below.

1. Train a pixel classifier direct in ZEN
2. Run the "Layer Thickness" workflow
3. Plug-in the model into the segmentation step
4. Robustly detect the layers inside the segmented image
5. Measure the thickness of this layers correctly

![Layer Thickness Measurement - Train a model to robustly detect the layers](../Images/intellesis_layer_thickness1.png)

---

## 11. Scripting Integration

Most functions regarding Intellesis can be scripted via Python in ZEN in order to automate and customize workflows. Check out the [scripts](../Machine_Learning/scripts/README.md) for some simple examples.

```python
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
