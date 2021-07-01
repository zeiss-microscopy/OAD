- [ZEN and APEER-ML - Open Ecosystem for Integrated Machine Learning Workflows](#zen-and-apeer-ml---open-ecosystem-for-integrated-machine-learning-workflows)
  - [Machine Learning versus Deep Learning](#machine-learning-versus-deep-learning)
  - [Main differences between Deep Learning and Machine Learning](#main-differences-between-deep-learning-and-machine-learning)
  - [ZEN and APEER Machine Learning - Overview](#zen-and-apeer-machine-learning---overview)
- [ZEN Intellesis Trainable Segmentation and Object Classification](#zen-intellesis-trainable-segmentation-and-object-classification)
  - [ZEN Intellesis Trainable Segmentation](#zen-intellesis-trainable-segmentation)
    - [Key Features of Intellesis Segmentation](#key-features-of-intellesis-segmentation)
    - [Intellesis Segmentation - Tech Notes](#intellesis-segmentation---tech-notes)
    - [Feature Extraction](#feature-extraction)
      - [What Implementation of the RandomForest is used by Intellesis](#what-implementation-of-the-randomforest-is-used-by-intellesis)
      - [How does a RandomForest work](#how-does-a-randomforest-work)
  - [ZEN Intellesis Object Classification](#zen-intellesis-object-classification)
    - [Key Features of Intellesis Object Classification](#key-features-of-intellesis-object-classification)
    - [Intellesis Object Classification - Tech Notes](#intellesis-object-classification---tech-notes)
  - [Application Examples](#application-examples)
    - [Life Science](#life-science)
    - [Material Science](#material-science)
  - [Intellesis - Data Flow](#intellesis---data-flow)
  - [General Workflows for Intellesis Segmentation in ZEN](#general-workflows-for-intellesis-segmentation-in-zen)
    - [How to train a simple Pixel Classifier for Segmentation Intellesis](#how-to-train-a-simple-pixel-classifier-for-segmentation-intellesis)
    - [How to use a model (trained on a single channel) inside an Image Analysis pipeline](#how-to-use-a-model-trained-on-a-single-channel-inside-an-image-analysis-pipeline)
    - [How to use a model (trained on all channels) inside an Image Analysis pipeline](#how-to-use-a-model-trained-on-all-channels-inside-an-image-analysis-pipeline)
  - [Importing a CZMODEL into ZEN blue or ZEN core](#importing-a-czmodel-into-zen-blue-or-zen-core)
    - [How to import a model in ZEN](#how-to-import-a-model-in-zen)
    - [Importing externally trained networks into ZEN](#importing-externally-trained-networks-into-zen)
    - [Example Workflow - Train and Import a network to segment a stack](#example-workflow---train-and-import-a-network-to-segment-a-stack)
    - [Intellesis Segmentation - Scripting Integration](#intellesis-segmentation---scripting-integration)
  - [Model Downloads](#model-downloads)
    - [Application Example - Robust Nucleus Detection using UNet](#application-example---robust-nucleus-detection-using-unet)
      - [UNet Nucleus Detector (GrayScale)](#unet-nucleus-detector-grayscale)
      - [UNet Nucleus Detector (RGB)](#unet-nucleus-detector-rgb)
    - [Example Networks - Conditions of Use](#example-networks---conditions-of-use)
  - [Integrated Workflows using trained models](#integrated-workflows-using-trained-models)
    - [Use Nucleus Detector inside a Zone-of-Influence workflow](#use-nucleus-detector-inside-a-zone-of-influence-workflow)
    - [Use trained model to reliably detect layers](#use-trained-model-to-reliably-detect-layers)
  - [General Workflows for Intellesis Object Classification](#general-workflows-for-intellesis-object-classification)
    - [Train an Object Classification Model](#train-an-object-classification-model)
    - [Intellesis Object Classification - Scripting Integration](#intellesis-object-classification---scripting-integration)

---

# ZEN and APEER-ML - Open Ecosystem for Integrated Machine Learning Workflows

The ZEN software and the APEER platform offer various tools and solution to integrate machine learning methods into image processing and analysis workflows. Depending on the specific workflow one might need only ZEN blue or ZEN core. For other workflows also the APEER-ML as a cloud-based training platform for Deep Neural Networks will play an important role.

## Machine Learning versus Deep Learning

The difference between those can be easily explained in a single sentence: Deep Learning is a special subset of general Machine learning, which is again a subset of Artificial Intelligence.
Therefore DeepLearning obviously is Machine Learning and Deep Learning algorithms are Machine Learning algorithms.

<p><img src="./images/ML_general-DeepLearning.png" title="Artificial Intelligence - Machine learning - Deep Learning" width="400"></p>

- Machine learning gives computers the ability to learn without being programmed explicitly for a specific task
- Two main categories exist: Supervised and Unsupervised methods

Deep learning itself consists of methods to analyze data using an approach that mimics the way a person would try to make sense of it. Deep Learning methods use a layered structure of algorithms called an artificial neural networks (ANN).

<p><img src="./images/ML_general-Neural%20Network.png" title="General Strcuture of a very simple neural network" width="400"></p>

ANNs have an input layer and obviously an output layer. The layers between are so-called hidden layers, which means their values cannot be observed (easily) during the training. An ANN gets "deeper" if the number of hidden layers increases.

- Deep Learning is a subset of Machine Learning
- Deep Learning is using "layered" algorithms called ANN

## Main differences between Deep Learning and Machine Learning

There are three major general differences (simplified:)

- typically Machine learning algorithms are rather" simple" compared to ANNs
- Deep Learning methods extract features automatically and learn what features work best
- classical Machine Learning methods are using features typically "engineered" by human intervention
- Deep Learning typically requires a lot more data due to the complex algorithms used

<p><img src="./images/ML_general-DL-ML-Input-Output.png" title="Difference between Machine Learning and Deep Learning" width="600"></p>

---

## ZEN and APEER Machine Learning - Overview

The sketch below outlines "the bigger" picture and vision and will be updated frequently. The most important points to consider here are:

- the “exchange” currency inside this ecosystem is the trained model (czmodel)
- the the open-source python package [**czmodel**](https://pypi.org/project/czmodel/) allows everybody to import their own models in ZEN
- skilled researchers and programmers can train their own models where the like and still deploy them for "their" users in ZEN or on the APEER platform
- one can get pre-trained models from ZEISS or get a trained model **as a service** (includes the label process)
- on the [APEER platform](www.apeer.com) it is possible to label your own data, train model and download it as czmodel for ZEN

![ZEN Machine Learning Landscape](../Images/ZEN_ML_Landscape_simple.png)

---

# ZEN Intellesis Trainable Segmentation and Object Classification

Among many other powerful tools to process and analyze images the ZEN blue and ZEN core software platform offers two major ML-based modules:

## ZEN Intellesis Trainable Segmentation

- Machine- and Deep Learning algorithms to **segment** images
- Import externally trained Deep Neural networks

![Intellesis Segmentation](../Images/intellesis_segmentation_tool.png)

### Key Features of Intellesis Segmentation

- **Simple User Interface for Labelling and Training**

  - The tool aims for the non-expert by providing an **“easy-to-use” interface**.
  - The focus is to provide a **clean and simple workflow** to label the images and train a model.
  - Label your datasets using clean and simple UI in ZEN or by using [APEER Annotate](https://www.apeer.com/annotate)

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

### Intellesis Segmentation - Tech Notes

- Machine-Learning Tool for Pixel Classification powered by **[Python](https://www.python.org), [Dask](https://dask.org/), [Scikit-Learn](https://scikit-learn.org/)** and **[Tensorflow 2](https://www.tensorflow.org/)**
- Real **Multi-Channel Feature Extraction** – all channels will be used to segment a pixel
- **Class Segmentation** – hierarchical structures with independent segmentation models per class
  - every object can be segmented using it individual model
- Feature Extraction using **Engineered Feature Sets** and **Deep Feature Extraction** (see also [Feature Extractors - Detailed Information](../Machine_Learning/Feature_Extractors/feature_extractors.md) and [Feature Extraction](#feature-Extraction) for more details)
  - Engineered Default Feature Sets (CPU)
    - 25 or 33 Features
  - Neural Network (vgg19) Layers for Feature Extraction (GPU)
    - 64, 128 (red. 50) or 256 (red. 70) Features for 1st, 2nd or 3rd layer of network
- Pixel Classification by proven and established **Random Forrest Classifier**
- **Basic Features use CPU for Feature Extraction** and CPU for Classification
- **Deep Features use GPU (if exist) for feature extraction** and CPU for Classification
- Option to **Download** pre-trained DNNs for image segmentation
- Option to **Import** pre-trained DNNs for image segmentation
  - currently two pre-trained networks are available
  - **[PyPi package czmodel & public ANN Model Specification](https://pypi.org/project/czmodel/)** to convert trained TF2 models into CZMODEL files
- for inference Intellesis can also use the **[Open Neural Network Exchange (ONNX)](https://onnx.ai)** format
- Post processing using **Conditional Random Fields** (CRF) to improve the segmentation results
- Option to apply **confidence thresholds** to the segmentation results
- Processing functions for creating masks and **scripting integration** for advanced automation of machine learning workflows
- **Client-Server Architecture** (Zen Client - Python-Server) using a [REST-API](https://en.wikipedia.org/wiki/Representational_state_transfer)
- client-side tiling & fusion functionality to deal with large **Multi-Dimensional Data Sets**
- support for Nvidia GPUs (recommended is a 8GB GPU or better)


### Feature Extraction

Intellesis Segmentation supports two different ways of segmenting an image:

- Feature Extraction with engineered feature sets followed by PixelClassification using a RandomForrest classifier
- Use Deep Neural networks for segmentation.
- for detailed information please see: **[Feature Extractors](../Machine_Learning/Feature_Extractors/feature_extractors.md)**
- the following lines always refer to the RandomForest classifier only.

#### What Implementation of the RandomForest is used by Intellesis

- Intellesis is using the following open.source implentation: **[scikit-learn - Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier)**
- except for the number of estimators (=25) Intellesis used the default values

#### How does a RandomForest work

- Each decision tree in the forest considers a subset of features when forming “questions” and only has access to a subset set of the training data
- this increases diversity in the forest leading to more robust overall predictions and the name ‘Random Forest.’ 
- **Prediction** = average of all the individual decision tree estimates
- Regression task = predicting a continuous value of …
- **Classification task** = predict discrete class labels such as A or B
- Random Forest will take a **majority vote** for the predicted class
  
![RandomForest Classifier - Majority Vote](./images/randomforest1.png)





---

## ZEN Intellesis Object Classification

- Machine Learning algorithms to **classify** objects inside analyzed images based on measure features

![Intellesis Object Classification - Training](./images/intellesis_toc_1.png)

![Intellesis Object Classification - Classification](./images/intellesis_toc_2.png)

### Key Features of Intellesis Object Classification

- **Simple User Interface for Labelling and Training**

  - The tool aims for the non-expert by providing an **“easy-to-use” interface**.
  - The focus is to provide a **clean and simple workflow** to label the segmented objects from an analyzed image and train an object classification model.

- **Integration into ZEN Measurement and Processing Framework**

  - Use a trained **Object Classifier** as an additional processing step after the Image Analysis.
  - Run Batch Classification our automate workflows using python scripting.

- **Support for Multi-dimensional Data Sets**

  - Intellesis Object Classification can be trained on any multidimensional dataset incl. 3rd party file formats from other vendors

---


### Intellesis Object Classification - Tech Notes

- **Required an analyzed image** with segmented objects created by any type of segmentation
- Real **Multi-Channel Feature Extraction** – all channels will be used extract intensity-based measurements for every segmented object
- **Geometrical and Shape Features** – all available features from the Image Analysis will be used automatically
- **Random Forrest Classifier** to process the feature table from the image analysis
- IP-Functions for Classification and Scripting Integration for Automation
- **Client-Server Architecture** (Zen Client - Python-Server) using a [REST-API](https://en.wikipedia.org/wiki/Representational_state_transfer)

## Application Examples

ZEN can basically read any image data format using the BioFormats Import and Intellesis can therefore be used to segment **any multi-dimensional data set** that can be imported into the software. Shown below are images segmented using ZEN Intellesis Trainable Segmentation.

### Life Science

![ZEN Python](../Images/intellesis_ms_apps.png)

---

### Material Science

![ZEN Python](../Images/intellesis_ls_apps.png)

---

## Intellesis - Data Flow

The machine-learning part of Intellesis is entirely built upon Python-based tools.

![ZEN Python Modules](../Images/ZEN_Python_Tools.png)

The actual segmentation service is completely written in [Python](https://www.python.org) and is using proven and established open-source machine-learning libraries to segment the images. More [detailed information](https://www.zeiss.com/microscopy/int/website/landingpages/zen-intellesis.html) and specific information regarding [ZEN core](https://www.zeiss.com/microscopy/int/products/microscope-software/zen-core.html#module) are available on the respective websites.

To be able to handle even large multi-dimensional data sets, the software has a built-in data manager that takes care of splitting and distributing the workload depending on the available computational resources.

![Intellesis - Data Flow - Training](../Images/intellesis_dataflow_training.png "Intellesis - ML Data Flow - Training")**Intellesis - Data Flow - Training**

---

![Intellesis - Data Flow - Prediction](../Images/intellesis_dataflow_prediction.png "Intellesis - ML Data Flow - Prediction")**Intellesis - Data Flow - Prediction**

---

## General Workflows for Intellesis Segmentation in ZEN

![Intellesis - Workflows](../Images/intellesis_workflows.png "Intellesis - Workflows")

---

### How to train a simple Pixel Classifier for Segmentation Intellesis

Training pixel classifier in Intellesis is very simple and just requires the following steps:

1. Create a new model and start the training UI.
2. Import one (or more) training images in order to label them.
3. Make up your mind if one wants to train on a single channel only or by using a spectral information.
4. Label cell nuclei and background.
5. Press Train & Segment and check the results.
6. Go back to 4. and label where the segmentation is not correct.
7. Press Finish when done to save the trained model.

> **IMPORTANT**: If a model was trained one a single channel only it can be used to segment single channel images only. If all channels where used during the training the model can be only use to segment images with a "matching" channel number.

Watch the short videos below to see those steps in action.

---

![Intellesis - Train a model to segment a cell using a single channel](../Images/zenblue_simple_nucleus_segmentation_single_channel.gif) **Intellesis - Train a model to segment a cell using a single channel**

---

![Intellesis - Train a model to segment a cell using all channels (multispectral](../Images/zenblue_simple_nucleus_segmentation_multispectral.gif) **Intellesis - Train a model to segment a cell using all channels (multispectral)**

---

### How to use a model (trained on a single channel) inside an Image Analysis pipeline

Once the model is trained it can be directly used inside an Image Analysis pipeline as part of the segmentation step. sThe required steps are:

1. Create a new Image analysis setting.
2. Define the class names, for "all the objects" and for the **single objects** and choose a color.
3. Assign the correct channel to the class **single objects**
4. Inside the segmentation step use the **Select** button to choose the segmentation method **Intellesis Trainable Class Segmenter**.
5. Select you model one just trained.
6. Select the class of interest, eg. the **nuclei**.
7. Check the segmentation preview and modify additional post-processing parameters, eg. filter out small objects.
8. Define the features to be measure and pre-configure a simple visualization of the results (can be modified later still).
9. Press **Finish** to save the setting and now use **Analyze** to run the image analysis.
10. Inspect the results.

> **IMPORTANT**: It is crucial to understand that a model trained on a single channel have to be assigned to the respective objects that should be segmented with the model. This very flexible approach allows to segment different structures using individual models or classical segmentation approached also inside hierarchical objects structures (with sub-objects etc).

Watch the short video below to see those steps in action.

![Intellesis - Use a trained model for segmentation inside an Image Analysis Setting](../Images/zenblue_use_simple_nucleus_single_channel_segmentation_in_IA.gif) **Intellesis - Use a trained model for segmentation inside an Image Analysis Setting**

---

### How to use a model (trained on all channels) inside an Image Analysis pipeline

If the model was trained on all channels of an image it can be directly used to create an image analysis setting with a pre-defined class structure. The required steps are:

1. Right-Click on the model and press **Create Image Analysis Setting**.
2. Enter the desired name for the setting.
3. Open the newly created Image Analysis setting (based on the class structure of the trained model). There is no need to assign any classes etc. since this is derived from the model directly.
4. Check the segmentation preview and modify additional post-processing parameters, eg. filter out small objects.
5. Define the features to be measure and pre-configure a simple visualization of the results (can be modified later still).
6. Press **Finish** to save the setting and now use **Analyze** to run the image analysis.
7. Inspect the results.

> **IMPORTANT**: The very simple and fast way to create an Image Analysis setting directly from model trained on multiple channels ahs the benefit of being able to use it directly without the need to setup classes. The limitation on the other side is that the object class structure is fixed (1:1 match between classes inside the trained model and classes for the image analysis). Therefore the limitation is that the class structure of the image analysis can not be modified nor it is possible to deal with sub-objects etc.

Watch the short video below to see those steps in action.

![Intellesis - Use a trained model (all channels) to directly create an Image Analysis Setting](../Images/zenblue_use_simple_nucleus_multispectral_segmentation_in_IA.gif) **Intellesis - Use a trained model (all channels) to directly create an Image Analysis Setting**

---

## Importing a CZMODEL into ZEN blue or ZEN core

It is possible to export and import import \*.czmodel files, which contain the trained segmentation model, in ZEN blue and in ZEN core.

### How to import a model in ZEN

To Import a model in ZEN use the **Import** model function inside ZEN blue or ZEN core.

<p><img src="../Images/zen32_model_import_dialog.png" title="ZEN blue - Import Model" width="600"></p>

<p><img src="../Images/zen32_model_import_file.png" title="ZEN blue - Select CZMODEL or JSON file" width="600"></p>

<p><img src="../Images/zen_core30_model_import.png" title="ZEN core - Select CZMODEL or JSON file" width="600"></p>

---

### Importing externally trained networks into ZEN

Starting with ZEN blue 3.2 and ZEN core 3.1 it will be possible to import externally trained models into ZEN. To import such a file just use the normal import function mentioned above. The general idea here is:

![Importing External Networks](../Images/intellesis_dataflow_czmodel.png)

- the ZEISS Custom-Solution Team, a researcher or any 3rd party trains its specific neural network
- The **[PyPi package czmodel](https://pypi.org/project/czmodel/)** is used to concert and package the network into a CZMODEL file
- the file is imported into ZEN using the normal **Import** mechanism
- from here on the network can be used inside the ZEN Image Analysis and Processing Function and also inside **[Guided Acquisition Workflows](https://github.com/zeiss-microscopy/OAD/tree/39dbefaaaf4ede1492a4f9c8c12ea56f9b90cb0e/Guided_Acquisition)**

For more details please se the **[Importing External Networks](../Machine_Learning/docs/README.md)**

### Example Workflow - Train and Import a network to segment a stack

To illustrate the general idea of using externally trained networks the followings steps have to be considered.

- A model was trained inside a jupyter notebook
- By using the **CZMODEL** the saved model was packed to be then imported in ZEN
- **If needed the process of labeling the data and training a network can be also provide by ZEISS as a commercial service.**
- The result of your own training or the training service will be a trained model ready to be in your own environment, on the APEER platform or inside the ZEN software platform.

![Intellesis - Use imported DNN to segment your data](../Images/workflow_model_em1.png)

To illustrate the workflow a public available dataset with labels: [Segmentation of neuronal structures in EM stacks challenge](https://imagej.net/Segmentation_of_neuronal_structures_in_EM_stacks_challenge_-_ISBI_2012.html#Test_data) was used to trains a simple network.

![Intellesis - Use imported DNN to segment your data](../Images/dnn_em-membranes_segmented_1.gif)

---

### Intellesis Segmentation - Scripting Integration

Most functions regarding Intellesis Segmentation can be scripted via Python in ZEN in order to automate and customize workflows. Check out the [scripts](../Machine_Learning/scripts/README.md) for some simple examples.

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

---

## Model Downloads

ZEN allows to import pre-trained neural networks and also provided some example that can be downloaded. Those networks can be used inside any segmentation or image analysis workflow in ZEN.

<p><img src="../Images/class_segmentation_cnn.png" title="Class Segmentation using pre-trained DNN" width="500"></p>

### Application Example - Robust Nucleus Detection using UNet

The trained networks for cell nucleus detection (available for download) are based on the well known UNet network architecture and are using a vgg16 encoder. The general structure is shown below. The numbers below the network layers represent the actual number of feature maps (per layer) and the array size is shown above the layers.

<p><img src="../Images/ZEN_UNet_vgg16_v1.png" title="UNet architecture for nucleus detection network" ></p>

#### UNet Nucleus Detector (GrayScale)

UNet-based Deep Neural Network (TensorFlow 2) for cell nucleus detection (grayscale). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

**Download here: [UNet Nucleus Segmentation (GrayScale)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nucleus_segmentation_grayscale_v2.czmodel?sv=2018-03-28&sr=b&sig=nQREzvO5673WA7M7EAUwa4FDgd%2BMKn96XS%2FrxFl%2BF04%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

#### UNet Nucleus Detector (RGB)

UNet-based Deep Neural Network (TensorFlow 2) for cell nucleus detection (RGB). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

**Download here: [UNet Nucleus Segmentation (RGB)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nuclei_segmentation_rgb_v2.czmodel?sv=2018-03-28&sr=b&sig=aHs0r5ovW1ELEgCOhjUq3nYVqCuhAhTT2nttjWI5rdU%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

---

### Example Networks - Conditions of Use

_These pre-trained networks were trained with "best-effort" on the available training data and is (are) provided "as is" without warranty of any kind. The licensor assumes no responsibility for the functionality and fault-free condition of the pre-trained network under conditions which are not in the described scope. Be aware that no pre-trained network will perform equally good on any sample, especially not on samples it was not trained for. Therefore, use such pre-trained networks at your own risks and it is up to the user to evaluate and decide if the obtained segmentation results are valid for the images currently segmented using such a network. For details see the respective chapter in the Online Help / Documentation. By downloading and using the networks I agree to the above terms._

---

## Integrated Workflows using trained models

### Use Nucleus Detector inside a Zone-of-Influence workflow

Once an externally trained model is imported (or was trained in ZEN) it can be plugged into any ZEN image analysis pipeline using a feature called **Class Segmentation**. The general idea is to set up a measurement hierarchy for the objects and the plugin trained models were needed, for example to robustly detect stained cell nuclei.

This approach also allows to mix machine-learning based segmentation with classical methods like "simple" threshold approaches. As an example, the robust nucleus detection using a pre-trained network is an ideal segmentation method to be used to segment the \*\*Primary Objects" inside a so-called "Zone-of-Influence" segmentation as shown below

1. Plugin the imported model into the class **Primary Objects** to robustly detect the stained cell nuclei inside a specific channel
2. Use this primary object to define a **Ring** around every detect cell nucleus
3. Define further subclasses as needed and segment them using other ML models or by applying an automated threshold
4. Run the complete image analysis pipeline incl. the model execution without having to worry about tile sizes, patches etc. and visualize the results easily

![Class Segmentation - Plugin UNet to detect cell nuclei](../Images/class_seg_DNN1.png)

![Class Segmentation - Easily analyze data and visualize the results](../Images/class_seg_DNN2.png)

### Use trained model to reliably detect layers

Trained models can be also used inside so-called "Material Modules" like **Layer Thickness**, which is outlined below.

1. Train a pixel classifier direct in ZEN
2. Run the "Layer Thickness" workflow
3. Plug-in the model into the segmentation step
4. Robustly detect the layers inside the segmented image
5. Measure the thickness of this layers correctly

![Layer Thickness Measurement - Train a model to robustly detect the layers](../Images/intellesis_layer_thickness1.png)

---

## General Workflows for Intellesis Object Classification

![Intellesis - Workflows](../Machine_Learning/images/Workflows_Object_Classification_v6.png "Intellesis - Workflows")

### Train an Object Classification Model

![Intellesis Object Classification - Train a model to classify objects](../Machine_Learning/images/ZEN_blue_Object_Classification3.gif "Train ad Classify") Intellesis Object Classification - Trained and Classify workflow. Images taken from: [Broad Bioimage Benchmark Collection](https://bbbc.broadinstitute.org/BBBC010)

### Intellesis Object Classification - Scripting Integration

Most functions regarding Intellesis Object Classification can be scripted via Python in ZEN in order to automate and customize workflows. Check out the [scripts](../Machine_Learning/scripts/README.md) for some simple examples.

```python
def find_objclassmodel(name):
    """ Finds an object classifier model given its Name.

    Arguments:
        name: string
              The name of the object classifier model to look for.

    Returns: IZenIntellesisObjClassModel
             The first object classifier model with the specified name
             or None, if no such model exists.
    """
    objclass_models = ZenIntellesis.ObjectClassification.ListAvailableModels()
    
    return next((m for m in objclass_models if m.Name == name), None)

# get all available object classification models
ocmodels = ZenIntellesis.ObjectClassification.ListAvailableModels()

for obcmodel in ocmodels:
    print 'TOC Model Name:', obcmodel.Name, 'Description:', obcmodel.Description, 'Status:', obcmodel.Status
    training_images = obcmodel.TrainingImages
    print '\tTraining Images:'
    print '\t----------------------'
    for ti in training_images:
        print '\t' + ti

# select a specific model
myobjmodel = find_objclassmodel('testmodel')

# classify an analyzed image (inplace)
myobjmodel.Classify(image, appendFeatures=False)

# import an classification model
imported_objclass_model = ZenIntellesis.ObjectClassification.ImportModel(model2import, True)

```
