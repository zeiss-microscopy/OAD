- [ZEISS - Open Ecosystem for Integrated Machine Learning Workflows](#zeiss---open-ecosystem-for-integrated-machine-learning-workflows)
  - [Building Blocks of the Ecosystem](#building-blocks-of-the-ecosystem)
  - [Machine Learning versus Deep Learning](#machine-learning-versus-deep-learning)
    - [Main differences between Deep Learning and Machine Learning](#main-differences-between-deep-learning-and-machine-learning)
    - [Classical Machine or Deep Learning for Segmentation - When to use it?](#classical-machine-or-deep-learning-for-segmentation---when-to-use-it)
  - [Model-centric versus data-centric model development](#model-centric-versus-data-centric-model-development)
  - [ZEN and arivis Cloud Machine Learning - Overview](#zen-and-arivis-cloud-machine-learning---overview)
  - [Model Deployment across platforms](#model-deployment-across-platforms)
    - [Semantic Segmentation](#semantic-segmentation)
    - [Instance Segmentation](#instance-segmentation)
    - [Open formats allow to use models (DL Segmentation) anywhere](#open-formats-allow-to-use-models-dl-segmentation-anywhere)
- [Segmentation Methods in ZEN and arivis Pro](#segmentation-methods-in-zen-and-arivis-pro)
  - [ZEN Intellesis Segmentation](#zen-intellesis-segmentation)
  - [Key Features of Intellesis Segmentation](#key-features-of-intellesis-segmentation)
  - [Intellesis Segmentation - Tech Notes](#intellesis-segmentation---tech-notes)
  - [What is Feature Extraction](#what-is-feature-extraction)
  - [Feature Extraction  in ZEN Intellesis](#feature-extraction--in-zen-intellesis)
    - [What Implementation of the RandomForest is used by Intellesis](#what-implementation-of-the-randomforest-is-used-by-intellesis)
    - [How does a RandomForest Classifier work](#how-does-a-randomforest-classifier-work)
  - [Application Examples](#application-examples)
    - [Life Science](#life-science)
    - [Material Science](#material-science)
  - [General Workflows for Intellesis Segmentation in ZEN](#general-workflows-for-intellesis-segmentation-in-zen)
    - [How to train a simple Pixel Classifier for Segmentation Intellesis](#how-to-train-a-simple-pixel-classifier-for-segmentation-intellesis)
    - [How to use a model (trained on a single channel) inside an Image Analysis pipeline](#how-to-use-a-model-trained-on-a-single-channel-inside-an-image-analysis-pipeline)
    - [How to use a model (trained on all channels) inside an Image Analysis pipeline](#how-to-use-a-model-trained-on-all-channels-inside-an-image-analysis-pipeline)
  - [How train a model for Instance Segmentation](#how-train-a-model-for-instance-segmentation)
  - [How to use an Instance Segmentation model in ZEN](#how-to-use-an-instance-segmentation-model-in-zen)
    - [Integration into BioApps](#integration-into-bioapps)
    - [Integration into Material Workflows](#integration-into-material-workflows)
  - [Bringing CZANNs and ZEISS software ecosystem together](#bringing-czanns-and-zeiss-software-ecosystem-together)
    - [The challenges of deployment](#the-challenges-of-deployment)
    - [The czmodel PyPi package](#the-czmodel-pypi-package)
    - [How to create external models](#how-to-create-external-models)
  - [Importing a model into ZEN blue, ZEN core and arivis Pro](#importing-a-model-into-zen-blue-zen-core-and-arivis-pro)
    - [How to import a model in ZEN](#how-to-import-a-model-in-zen)
  - [Intellesis Segmentation - Scripting Integration](#intellesis-segmentation---scripting-integration)
  - [Application Example - Download Model for Robust Nucleus Detection using UNet](#application-example---download-model-for-robust-nucleus-detection-using-unet)
    - [UNet Nucleus Detector (GrayScale)](#unet-nucleus-detector-grayscale)
    - [UNet Nucleus Detector (RGB)](#unet-nucleus-detector-rgb)
    - [Example Networks - Conditions of Use](#example-networks---conditions-of-use)
  - [Integrated Workflows using trained models](#integrated-workflows-using-trained-models)
    - [Use Nucleus Detector inside a Zone-of-Influence workflow](#use-nucleus-detector-inside-a-zone-of-influence-workflow)
    - [Use trained model to reliably detect layers](#use-trained-model-to-reliably-detect-layers)
- [ZEN Intellesis Object Classification](#zen-intellesis-object-classification)
  - [Key Features of Intellesis Object Classification](#key-features-of-intellesis-object-classification)
  - [Intellesis Object Classification - Tech Notes](#intellesis-object-classification---tech-notes)
  - [General Workflows for Intellesis Object Classification](#general-workflows-for-intellesis-object-classification)
    - [Train and Classify](#train-and-classify)
    - [Intellesis Object Classification - Scripting Integration](#intellesis-object-classification---scripting-integration)
- [ZEN Intellesis Denoising](#zen-intellesis-denoising)
  - [The algorithm](#the-algorithm)
  - [Key Features Intellesis Denoising](#key-features-intellesis-denoising)
  - [What is Noise (inside images in microscopy)](#what-is-noise-inside-images-in-microscopy)
    - [Reasons for “Imperfection"](#reasons-for-imperfection)
    - [Main sources of Noise in microscopy](#main-sources-of-noise-in-microscopy)
    - [What is Noise2Void (simplified):](#what-is-noise2void-simplified)
    - [What pure Noise2Void cannot do:](#what-pure-noise2void-cannot-do)
  - [How to train and use a Noise2Void model in ZEN](#how-to-train-and-use-a-noise2void-model-in-zen)
  - [Understanding the training parameters](#understanding-the-training-parameters)
    - [Number of epochs](#number-of-epochs)
    - [Batch size](#batch-size)
    - [Window size](#window-size)
    - [Masking Ratio](#masking-ratio)
  - [Remarks and pitfalls](#remarks-and-pitfalls)
  - [TechNotes Intellesis Denoising](#technotes-intellesis-denoising)

---

# ZEISS - Open Ecosystem for Integrated Machine Learning Workflows

The [ZEN blue], [ZEN core] and [arivis Pro] software together with and the [arivis Cloud] platform offer various tools and solutions to integrate machine learning methods and Deep learning into image processing and analysis workflows.

The mission statement for the ecosystem can be described as:

<font size="5">"Put the scientist into the driver seat for Deep learning"</font>

and

<font size="5">"Better data beat better models."</font>

ZEN and ZEN Core are robust microscopy software packages, offering a broad spectrum of image analysis and processing tools tailored to support [standard microscopy workflows](#zeiss_ai1). From image acquisition to preprocessing, analysis, and final result presentation, these tools guide users through every step

<p><img src="./images/zeiss_ai.png" id="zeiss_ai1" title="Microscope Imaging Workflow" width="800"></p>

A [schematic representation](#zeiss_ai1) of a typical microscopy imaging workflow, illustrating the sequential steps from image acquisition to preprocessing, image analysis, classification, and result/report generation.

The ZEN software packages offer dedicated analysis tools alongside a versatile image analysis toolkit, incorporating powerful Machine Learning algorithms for different phases of the [workflow](#zeiss_ai2). For example, Noise2Void algorithm facilitates image denoising, while semantic and instance segmentation methods are available for image segmentation tasks. Additionally, the software supports Machine Learning driven object classification.
These solutions build upon established and widely recognized tools and frameworks like PyTorch, TensorFlow, and ONNX, and are fine-tuned for simplicity and seamless integration. They can be readily used within pre-configured workflows in ZEN and ZEN Core, such as Material Apps (for tasks like grain size analysis and layer thickness measurement) or Bio Apps (for tasks such as cell counting and gene expression analysis). The integration of AI within the ZEN software has revolutionized microscopy, enhancing speed, efficiency, and accuracy to unprecedented levels.

<p><img src="./images/zeiss_ai2.png" id="zeiss_ai2" title="Microscope Imaging Workflow with AI techniques" width="800"></p>

## Building Blocks of the Ecosystem

- **arivis Cloud incl arivis AI**
  - [arivis AI] for data-driven training of Deep Learning models (semantic and instance segmentation) incl. annotation tools
  - Models can be used inside ZEN and arivis Pro for various applications (2D and 3D Analysis, [BioApps], Material Modules etc.)
- **ZEN Intellesis Segmentation**
  - Local training of Pixel Classifier (based on Random Forrest)
  - Full Integration of all types models incl. Deep Learning into Image Analysis applications
- **ZEN Intellesis Object Classification**
  - Feature-based Object Classification
- **ZEN Intellesis Denoising**
  - Local training and usage of Noise2Void
- **arivis Pro**
  - Use DL models for segmentation, Classify Objects and use regression models
- **ZEISS ML-Stack** (Python)
  - czmodel, pylibCZIrw, cztile, ZeissPy, prismalearn, ...

---

## Machine Learning versus Deep Learning

The difference between those can be easily explained in a single sentence: Deep Learning is a special subset of general Machine learning, which is again a subset of Artificial Intelligence.
Therefore DeepLearning obviously is Machine Learning and Deep Learning algorithms are Machine Learning algorithms.

<p><img src="./images/ML_general-DeepLearning.png" title="Artificial Intelligence - Machine learning - Deep Learning" width="400"></p>

- Machine learning gives computers the ability to learn without being programmed explicitly for a specific task
- Two main categories exist: Supervised and Unsupervised methods

Deep learning itself consists of methods to analyze data using an approach that mimics the way a person would try to make sense of it. Deep Learning methods use a layered structure of algorithms called an artificial neural networks (ANN).

<p><img src="./images/ML_general-Neural%20Network.png" title="General Structure of a very simple neural network" width="400"></p>

ANNs have an input layer and obviously an output layer. The layers between are so-called hidden layers, which means their values cannot be observed (easily) during the training. An ANN gets "deeper" if the number of hidden layers increases.

- Deep Learning is a subset of Machine Learning
- Deep Learning is using "layered" algorithms called ANN

### Main differences between Deep Learning and Machine Learning

There are three major general differences (simplified:)

- typically Machine learning algorithms are rather" simple" compared to ANNs
- Deep Learning methods extract features automatically and learn what features work best
- classical Machine Learning methods are using features typically "engineered" by human intervention
- Deep Learning typically requires a lot more data due to the complex algorithms used

<p><img src="./images/ML_general-DL-ML-Input-Output.png" title="Difference between Machine Learning and Deep Learning" width="600"></p>

### Classical Machine or Deep Learning for Segmentation - When to use it?

Given the power of DL-based models one can argue that every segmentation problem should be approached using "Deep-learning" methods, but there is a more educated approach. The key is to understand the complexity of the actual segmentation task and and required accuracy for the subsequent image analysis.

In cases where one only needs to segment "bright blob on dark background" with the goal to count the number of objects using a classical threshold like Otsu etc. is a very valid and useful approach. As the segmentation tasks get more "challenging" one should start testing classical machine-learning or even deep-learning approaches

<p><img src="./images/seg_task.png" title="Complexity of Segmentation tasks" width="800"></p>

---

## Model-centric versus data-centric model development

Achieving robust segmentation of many classes across different imaging conditions is the ultimate goal of developing a Deep Learning segmentation model. However, it is challenging for the algorithm to learn all the complexity when provided only a few annotated objects within the large parameter space. In essence this approach try to improve the segmentation performance by adding more and better annotation instead of fine-tuning every model for a specific dataset.

<p><img src="./images/model_centric.jpg" title="Model-Centric vs. Data-centric model development" width="800"></p>

An import concept is therefore to make the annotation process as fast and efficient as possible, which is achived on our platform using the idea of **partial annotations". It basically means the the user only has to label a few objects. The typical workflow here is:

<p><img src="./images/partial_label1.png" title="Partial Labeling - Label a few objects and add background" width="800"></p>

- label a few objects per image
- start a training run
- inspect the results
- **add new labels in places where the model does not perform well (yet)**

<p><img src="./images/partial_label2.png" title="Partial Labeling - Label a few objects and add background" width="800"></p>

---

## ZEN and arivis Cloud Machine Learning - Overview

The sketch below outlines "the bigger" picture and vision and will be updated frequently. The most important points to consider here are:

- the “exchange” currency inside this ecosystem is the trained model
- the the open-source python package [czmodel] allows everybody to import their own models in [ZEN blue], [ZEN core] or [arivis Pro]
- skilled researchers and programmers can train their own models where the like and still deploy them for "their" users in [ZEN blue], [ZEN core] or [arivis Pro]
- one can get pre-trained models from ZEISS or get a trained model **as a service** (includes the label process)
- on the [arivis Cloud] platform it is possible to label your own data, train model and download it as *.czann file to be used in ZEN or [arivis Pro]

![Concept Train Anywhere](../Machine_Learning/images/train_anywhere.png)

## Model Deployment across platforms

![AI Model Development Overview](../Machine_Learning/images/AI_Model_Development_Overview.png)

### Semantic Segmentation

Deep-Learning Models for semantic segmentation can be trained on the [cloud platform](https://www.apeer.com/app/ai-toolkit/overview) or "externally" and then packaged as a CZANN file using the [czmodel](#the-czmodel-pypi-package). The artifact that is "shipped" is only the model and the actual platform, where the model will be used later, has to make sure all required dependencies are available

### Instance Segmentation

For the Instance Segmentation models the annotation and training process also takes place on the [cloud platform](https://www.apeer.com/app/ai-toolkit/overview) but the deployment is done differently compared to simple DL models for semantic segmentation.

AI Models for Instance Segmentation will be deployed including all code for DataIO, pre-processing, Inference and PostProcessing as a container, which can be deployed across platforms to ensure identical results.The artifact that is "shipped" i only the model & code inside a container and the actual platform, where the model will be used later, does not need to provide all rhe required packages to execute the actual AI model.

<p><img src="./images/new_deployment.png" title="Model-Centric vs. Data-centric model development" width="800"></p>

---

### Open formats allow to use models (DL Segmentation) anywhere

Below a "showcase" to demonstrate that the concept of being "open" and having a respective model formats works.

- train a *.czann model on APEER
- open the image in [Napari]
- import the model (requires a plugin) and run it

![Grain Size Analysis using DNN](../Machine_Learning/images/grainsize_czann_napari.png)

---

# Segmentation Methods in ZEN and arivis Pro

The three main software packages all offer a range of segmentation methods that can be used in various processing pipelines and tools.

- intensity and variance global and local thresholds
- semantic segmentation (Pixel Classification)
  - using RandomForrest (sklearn)
  - using Deep Learning (EfficientNet)
- instance segmentation using Deep Learning (Mask2Former)

<p><img src="./images/zen_seg.png" title="General Structure of a very simple neural network" width="1000"></p>

## ZEN Intellesis Segmentation

- Machine- and Deep Learning algorithms to **segment** images
- Full Integration into Image Analysis Workflows, Material Modules, [BioApps] and Guided Acquisition
- Import of externally trained Deep Neural networks

![Intellesis Segmentation](../Images/intellesis_segmentation_tool.png)

## Key Features of Intellesis Segmentation

- **Simple User Interface for Labelling and Training**

  - The tool aims for the non-expert by providing an **“easy-to-use” interface**.
  - The focus is to provide a **clean and simple workflow** to label the images and train a model.
  - Label your datasets using clean and simple UI in ZEN or by using [arivis AI]

<p><img src="../Machine_Learning/images/annotating_mitochondria.gif" title="Partial Annotation on APEER" width="600"></p>

- **Integration into Measurement and Processing Framework**

  - As segmentation is only the required first step for subsequent measurements the **integration into the actual measurement tools** is key.
  - Deep Learning models for semantic segmentation trainedAny Intellesis model can be **directly used inside Image Analysis workflows** as a segmentation method Deep Learning or RandomForrest
  - [arivis Pro] allows to import Deep Learning models

- **Open Platform - Import your own trained models**

  - Import your own model and use it seamlessly integrated in ZEN workflows and benefit from Image Tiling & Fusion client
  - Use the open-source python package [czmodel] to "package your model to be used in the ZEN ecosystem.

- **Support for Multi-dimensional Data Sets**

  - Intellesis, especially when considering the BioFormats option, can be used to **segment any image** incl. 3rd party file formats from other vendors
  - It can handle multi-dimensional data sets like 3D stacks, Tiles, Multi-Channel, …

---

## Intellesis Segmentation - Tech Notes

- Machine-Learning Tool for Pixel Classification powered by [Python]
- Real **Multi-Channel Feature Extraction** – all channels will be used to segment a pixel
- **Class Segmentation** – hierarchical structures with independent segmentation models per class
  - every object can be segmented using it individual model
- Feature Extraction using **Engineered Feature Sets** and **Deep Feature Extraction** (see also [Feature Extractors - Detailed Information](../Machine_Learning/Feature_Extractors/feature_extractors.md) and [Feature Extraction](#feature-extraction) for more details)
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
  - [PyPi package czmodel & public ANN Model Specification](https://pypi.org/project/czmodel/) to package trained models into ONNX files incl. metadata
- for inference Intellesis can also use the [Open Neural Network Exchange (ONNX)](https://onnx.ai) format
- Post processing using **Conditional Random Fields** (CRF) to improve the segmentation results
- Option to apply **confidence thresholds** to the segmentation results
- Processing functions for creating masks and **scripting integration** for advanced automation of machine learning workflows
- **Client-Server Architecture** (Zen Client - Python-Server) using a [REST-API](https://en.wikipedia.org/wiki/Representational_state_transfer)
- client-side tiling & fusion functionality to deal with large **Multi-Dimensional Data Sets**
- support for Nvidia GPUs (recommended is a 8GB GPU or better)

## What is Feature Extraction

In order to classify pixel using Machine-Learning Classifiers it is need to extract "features" from an image. This is usually done by applying different kind of filter. During tha training process it is not required to label the whole image - labeling can also be done on a subset of the image.

<p><img src="../Machine_Learning/images/feature_extraction.png" title="Feature Extraction for Machine Learning" width="1000"></p>

Sample courtesy of Prof. Jochen Herms, LMU München, Germany.

## Feature Extraction  in ZEN Intellesis

Intellesis Segmentation supports two different ways of segmenting an image:

- Feature Extraction with engineered feature sets followed by PixelClassification using a RandomForrest classifier
- Use Deep Neural networks for segmentation.
- for detailed information please see: [Feature Extractors](../Machine_Learning/Feature_Extractors/feature_extractors.md)
- the following lines always refer to the RandomForest classifier only.

### What Implementation of the RandomForest is used by Intellesis

- Intellesis is using the following open.source implementation: [scikit-learn - Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier)
- except for the number of estimators (= 25) Intellesis used the default values

### How does a RandomForest Classifier work

- Each decision tree in the forest considers a subset of features when forming “questions” and only has access to a subset set of the training data
- this increases diversity in the forest leading to more robust overall predictions and the name ‘Random Forest.’ 
- **Prediction** = average of all the individual decision tree estimates
- Regression task = predicting a continuous value of …
- **Classification task** = predict discrete class labels such as A or B
- Random Forest will take a **majority vote** for the predicted class
  
![RandomForest Classifier - Majority Vote](./images/randomforest1.png)

---

## Application Examples

ZEN can basically read any image data format using the BioFormats Import and Intellesis can therefore be used to segment **any multi-dimensional data set** that can be imported into the software. Shown below are images segmented using ZEN Intellesis Trainable Segmentation.

### Life Science

![ZEN Python](../Images/intellesis_ls_apps.png)

---

### Material Science

![ZEN Python](../Images/intellesis_ms_apps.png)

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

Watch the short videos below to see those steps in action:

![Intellesis - Train a model to segment a cell using a single channel](../Images/zenblue_simple_nucleus_segmentation_single_channel.gif) **Intellesis - Train a model to segment a cell using a single channel**

![Intellesis - Train a model to segment a cell using all channels (multispectral](../Images/zenblue_simple_nucleus_segmentation_multispectral.gif) **Intellesis - Train a model to segment a cell using all channels (multi-spectral)**

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

## How train a model for Instance Segmentation

On our [arivis Cloud] platform it is easily possible to label your data to train an AiModel for Instance Segmentation

## How to use an Instance Segmentation model in ZEN

In order to use Instance Segmentation models it is required to annotate data and trained a model on our [arivis cloud] platform. Once the training is finished the model and all the required code are packaged as a docker container and can be downloaded to your local platform.

![Instance Segmentation Workflow](../Machine_Learning/images/instance1.png)

- Importing or downloading the model (Ai Model Container) in ZEN

![Importing the AI Model Container in ZEN](../Machine_Learning/images/instance2.png)

- using the instance model inside the ZEN image analysis
- similar to semantic models every "class" inside the image analysis pipeline can use its own individual model (if required)

![Using the Instance model inside ZEN Image Analysis](../Machine_Learning/images/instance3.png)

- evaluate the results of the image analysis using the instance segmentation - here inside the Cell Counting [BioApps]

![Using the Instance model inside ZEN Image Analysis](../Machine_Learning/images/instance4.png)

### Integration into [BioApps]

Bio Apps comprise a streamlined suite of image analysis tools meticulously tailored for common tasks in cell biology and cancer research. These tools provide specialized solutions for tasks such as cell counting, cellular gene expression analysis, and nuclear translocation studies.

The cells displayed in the figure were imaged using a ZEISS Celldiscoverer 7 microscope, employing oblique contrast imaging to enhance cellular morphology and facilitate better segmentation. The channel corresponding to mCherry fluorescence is colored in pink and displayed alongside the cell channel, as shown in the top right in the [figure](#bioapp1) below. A Deep Learning model for instance segmentation, trained on the ZEISS arivis Cloud platform, was imported into the Gene Expression BioApp in ZEN to perform automated cellular segmentation.

<p><img src="./images/bioapps1.png" id="bioapp1" title="Gene Expression BioApp" width="800"></p>

An instance segmentation model trained on [arivis Cloud] is used for the segmentation of cells in the oblique channel. Following cell segmentation, mCherry-positive cells are identified to evaluate the expression rate. The result of analyzing a multi-well plate using the Gene-Expression Bio App as heatmap.

<p><img src="./images/bioapps2.png" id="bioapp1" title="Gene Expression BioApp  Heatmap" width="800"></p>

### Integration into Material Workflows

Using the same workflow it is also possible to train apply AiModel for Instance Segmentation in ZEN core material workflow, like Grain-Size Analysis ([MaterialApps](https://www.zeiss.com/microscopy/en/products/software/zeiss-zen-core.html#accordionItem-150111185))

![Using the Instance model inside ZEN Image Analysis](../Machine_Learning/images/grains_all.png)

- (TL) Aluminum (baker-stained) grains inside the arivis Cloud viewer label and segmented in arivis Cloud using Instance Segmentation.
- (TR) Results of a prediction using instance segmentation in arivis Cloud
- (B) The AiModel for Instance Segmentation integrated in ZEN core inside the Grains workflow.

The figures showcases the ZEN Core interface for grain size analysis. An instance segmentation model trained on ZEISS arivis Cloud is imported into ZEN Core to segment individual grains within an aluminum Barker etched sample. This segmentation process enables the extraction of the size distribution of individual grains, facilitating comprehensive analysis.

## Bringing CZANNs and ZEISS software ecosystem together

Training artificial neural networks (ANN) to tackle semantic segmentation problems has become a very popular task and an increasing number of solutions has become available that require little technical understanding to train ANNs. Of course, this statement does not hold for models highly optimized for specific use cases where solving the problem at hand requires a high amount of experience, creativity and some “magic”. However, in many cases it is possible to achieve decent results with widely used ANN model architectures, a sufficient amount of data and enough compute power.

While about a decade ago solving computer vision tasks required an expert to design algorithms and understand the math behind them, ANNs and simple-to-use frameworks like [TensorFlow](https://www.tensorflow.org/) and [PyTorch](https://pytorch.org/) allow learning those algorithms from data and therefore can be treated as a black-box even achieving super-human performance in some cases. This simplicity and the high expressiveness of neural network models are presumably the reason that ANNs have become extremely popular and there is literally no way around this technology in research as well as industry. It should, however, be mentioned here that it is still extremely helpful to understand what happens behind the scenes.

### The challenges of deployment

While in research the focus mostly lies on training and evaluating models, deployment is a different issue that poses different challenges. Especially in microscopy there usually are not only captured small images but stacks of images, time series of images or tiled scenes that are stitched to one large image of multiple or even hundreds of gigabytes. The training process, in contrast, is typically performed on small image crops (e.g. 256 x 256) such that the data for the calculations fits into the GPU or main memory of the employed machine. Applying a trained model on considerably larger images as mentioned above brings about several pitfalls that need to be handled.

The [ZEN Intellesis] infrastructure provides a solution for that problem. It applies a sophisticated tiling strategy that transforms multi-dimensional image captures – as they are generated by ZEISS microscopes – to image tiles of shape (height x width x color channels) where height and width are defined by the applied ANN model. Finally, it performs inference with the model and reassembles the resulting segmentation masks to fit the initially captured image. It therefore offers a solution to apply a trained ANN on large images without worrying too much about the required memory and the size of the image.

### The czmodel PyPi package

all our software tools allow to run predictions with custom segmentation DL models (Semantic Segmentation) trained "outside of ZEN". To be compatible "usable", a model has to comply with our specification and some meta data must be provided that is described in detail in the official CZANN model specification in the project description of our [czmodel package](https://pypi.org/project/czmodel/).

<p><img src="./images/czmodel_pypi.png" title="The CZMODEL package" width="800"></p>

- Open and standardized “container” to store ML models and metadata
- no new model format
- support for ONNX and TF2.SavedModels (legacy) models
- used by [ZEN blue], [ZEN core], [arivis AI] and [arivis Pro]
- **allows external data scientists to integrate their own models our tools**

For a simple example of such a pipeline see the attached Jupyter notebook (ready to be executed) in our [Colab Notebook](https://colab.research.google.com/github/zeiss-microscopy/OAD/blob/master/Machine_Learning/notebooks/czmodel/SingleClassSemanticSegmentation_PyTorch_5_0_0.ipynb). Note that the notebook is not to be understood as a best practice guide for training ANN models but rather illustrates the use of the [czmodel](https://pypi.org/project/czmodel/) library with a very simple model generation process that will usually be more sophisticated.

<p><img src="./images/package_czann.png" title="Package a model as CZANN" width="800"></p>

### How to create external models

- **the ZEISS Custom Solution Team, a researcher or any 3rd party trains its specific neural network**
- the PyPi package [czmodel](https://pypi.org/project/czmodel/) is used to convert and package the model as a *.czann file
- the *.czann file is imported into ZEN using the normal **Import** mechanisms

From here on the network can be used inside the ZEN Image Analysis, Processing functions, [BioApps], Material Modules and also inside [Guided Acquisition Workflows](https://github.com/zeiss-microscopy/OAD/tree/master/Guided_Acquisition)

## Importing a model into ZEN blue, ZEN core and arivis Pro

It is possible to export and import import models, which contain the trained segmentation or regression model (for example a Noise2Void model).

### How to import a model in ZEN

To Import a model in ZEN use the **Import** model function inside ZEN blue or ZEN core.

<p><img src="../Images/zen32_model_import_dialog.png" title="ZEN blue - Import Model" width="600"></p>

<p><img src="../Images/zen32_model_import_file.png" title="ZEN blue - Select CZMODEL or JSON file" width="600"></p>

<p><img src="../Images/zen_core30_model_import.png" title="ZEN core - Select CZMODEL or JSON file" width="600"></p>

---

## Intellesis Segmentation - Scripting Integration

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

## Application Example - Download Model for Robust Nucleus Detection using UNet

ZEN allows to import pre-trained neural networks and also provided some example that can be downloaded. Those networks can be used inside any segmentation or image analysis workflow in ZEN.

<p><img src="../Images/class_segmentation_cnn.png" title="Class Segmentation using pre-trained DNN" width="500"></p>

The trained networks for cell nucleus detection (available for download) are based on the well known UNet network architecture and are using a vgg16 encoder. The general structure is shown below. The numbers below the network layers represent the actual number of feature maps (per layer) and the array size is shown above the layers.

<p><img src="../Images/ZEN_UNet_vgg16_v1.png" title="UNet architecture for nucleus detection network" ></p>

### UNet Nucleus Detector (GrayScale)

UNet-based Deep Neural Network (TensorFlow 2) for cell nucleus detection (grayscale). This pre-trained network is suited for segmenting cell nuclei stained with a fluorescent dye. The output will be three different classes: nucleus, borders and background. It was trained with "best-effort" on the available training data and is provided "as is" without warranty of any kind

**Download here: [UNet Nucleus Segmentation (GrayScale)](https://caprodstorage.blob.core.windows.net/320949c9-6d78-4a40-bd58-253d2a3e6d4f/nucleus_segmentation_grayscale_v2.czmodel?sv=2018-03-28&sr=b&sig=nQREzvO5673WA7M7EAUwa4FDgd%2BMKn96XS%2FrxFl%2BF04%3D&se=9999-12-31T23%3A59%3A59Z&sp=r)**

### UNet Nucleus Detector (RGB)

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

# ZEN Intellesis Object Classification

- Machine Learning algorithms to **classify** objects inside analyzed images based on measure features

![Intellesis Object Classification - Training](./images/intellesis_toc_1.png)

![Intellesis Object Classification - Classification](./images/intellesis_toc_2.png)

## Key Features of Intellesis Object Classification

- **Simple User Interface for Labelling and Training**

  - The tool aims for the non-expert by providing an **“easy-to-use” interface**.
  - The focus is to provide a **clean and simple workflow** to label the segmented objects from an analyzed image and train an object classification model.

- **Integration into ZEN Measurement and Processing Framework**

  - Use a trained **Object Classifier** as an additional processing step after the Image Analysis.
  - Run Batch Classification our automate workflows using python scripting.

- **Support for Multi-dimensional Data Sets**

  - Intellesis Object Classification can be trained on any multidimensional dataset incl. 3rd party file formats from other vendors

---

## Intellesis Object Classification - Tech Notes

- **Required an analyzed image** with segmented objects created by any type of segmentation
- Real **Multi-Channel Feature Extraction** – all channels will be used extract intensity-based measurements for every segmented object
- **Geometrical and Shape Features** – all available features from the Image Analysis will be used automatically
- **Random Forrest Classifier** to process the feature table from the image analysis
- IP-Functions for Classification and Scripting Integration for Automation
- **Client-Server Architecture** (Zen Client - Python-Server) using a [REST-API](https://en.wikipedia.org/wiki/Representational_state_transfer)

## General Workflows for Intellesis Object Classification

![Intellesis - Workflows](../Machine_Learning/images/Workflows_Object_Classification_v6.png "Intellesis - Workflows")


### Train and Classify

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

# ZEN Intellesis Denoising

Starting with ZEN blue 3.6 and ZEN core 3.4 it is possible to train and use AI-powered denoising methods inside the ZEN software. The algorithm used is called Noise2Void (N2V) and is described in the paper [Noise2Void - Learning Denoising from Single Noisy Images](https://arxiv.org/abs/1811.10980).

## The algorithm

The denoising module in ZEN uses the Noise2Void (N2V) approach and has been shown to achieve state-of-the-art performance at denoising scientific images. Because N2V is a general-purpose algorithm that does not require prior knowledge of the specific noise distribution, it is ideal to denoise wide range of microscopy image modalities, including fluorescence microscopy, bright-field microscopy, and electron microscopy.

![ZEN Denoising](../Machine_Learning/images/denoise1.png)

## Key Features Intellesis Denoising

- **Simple User Interface for Labelling and Training**
  - Clean and simple training UI with just a few parameters to be adjusted
- **Integration into ZEN Processing Framework**
  - Use trained denoise and general regression models as a normal processing function
  - Scripting
- **Open Platform – Import your own trained networks for denoising and regression tasks**
  - **Import your own Noise2Void or Regression model and use it seamlessly integrated in ZEN workflows via *.czann format
  - Denosing or regression models in ZEN or V4D are packages as *.czann files and therefore it is easily possible to import your own model into ZEN.
  - For instructions on how to do this please check out the [Colab Notebook](https://colab.research.google.com/github/zeiss-microscopy/OAD/blob/master/Machine_Learning/notebooks/czmodel/Regresssion_PyTorch_5_0_0.ipynb)
- Support for Multi-dimensional Datasets
  - Import any multi-dimensional dataset incl. 3rd party file formats from other vendors

## What is Noise (inside images in microscopy)

Whenever one is imaging an object it is crucial to recognize that:

**_"Every image is an imperfect representation of the underlying structure that is being imaged!"_**

### Reasons for “Imperfection"

- Limited resolution because of the optics
- Uneven illumination or background
- Unwanted stray light or out-of-focus light
- Image artifacts
- **Noise**

![ZEN Denoising](../Machine_Learning/images/denoise3.png)**Image Imperfections**

All of the things above are "unwanted" but it is important to understand that methods like N2V can only help with the noise itself not with all the other undesired things in your image.

### Main sources of Noise in microscopy

- Shot Noise (due to the nature of light itself, Poisson Distribution)
- Detector Noise (due to the electronics etc., models as additive Gaussian noise)

### What is Noise2Void (simplified):

- it is a deep-learning based method to learn “the noise” from the image itself (no labels or ground truth need) in order to remove the noise
- by “masking” a pixel and therefore hiding it from the receptive field of the Deep Neural Network
- Assumption when using N2V: pixel-independent noise or so called "iid" (identically distributed samples)noise, which depends on detection method and the used detectors itself

### What pure Noise2Void cannot do:

- remove out-of-focus, stray light or background signal
- increase the resolution
- correct uneven illumination
- correct image artifacts

## How to train and use a Noise2Void model in ZEN

![ZEN Denoising](../Machine_Learning/images/ZENblue_N2V_Train_Denoise_1.gif)

The same video with sound and a transcript can be found here: [ZEN Denoising - Video with Sound and Transscript](https://www.youtube.com/watch?v=L0ccHmUKmBg)

## Understanding the training parameters

The Intellesis Denoising training interface shares a resemblance with the Intellesis machine learning training interface, making it user-friendly for both new and existing users to develop personalized denoising models. This training interface features four adjustable parameters, namely the number of epochs, batch size, window size, and masking ratio. While the default values may suffice, users may need to lower the batch size when using a resource-limited system (e.g., your work laptop). Further details on each of these parameters are available below.

### Number of epochs

The "number of epochs" refers to the number of times the training dataset is passed through the neural network during the training process. Each pass through the dataset is called an epoch. (an epoch consists of a fixed number of samples drawn from the dataset) In N2V, the number of epochs is a user-defined parameter that determines how many times the neural network will be trained on the full dataset. If the number of epochs is too short, the model may not be able to learn the underlying patterns in the data, resulting in under-fitting. On the other hand, if the number of epochs is too long, the model may start to memorize the training data, resulting in over-fitting making it less effective at denoising new images.

### Batch size

The "batch size" refers to the number of samples (image patches) that are processed by the neural network at once. During each epoch, the training dataset is typically divided into several smaller batches, and the neural network is updated based on the average loss across the batch. The batch size is another user-defined parameter that controls how many samples are processed in each batch. If the batch size is too small, the model may converge slowly and can result in poor generalization. If the batch size is too large, it may result in the model being unable to fit into memory, slowing down the training process, and potentially leading to poor generalization. The default batch size in ZEN is 64, but it is advisable to experiment with smaller sizes, such as 32 or 16, if memory errors occur.

### Window size

Given a pixel to be masked", the "window size" parameter determines the size of the surrounding area to sample replacement pixel. Specifically, N2V divides the input image into overlapping patches of a fixed size (determined by the window size parameter) and trains a neural network to predict the central pixel of each patch based on the other pixels in the patch. During inference (denoising), N2V processes the input image in a sliding-window fashion, applying the trained neural network to each patch in turn to produce a denoised output image. If the window size is too small, it may not capture enough information to properly denoise the image. If the window size is too large, it may include too much information, leading to over-fitting, increased computation time, and reduced performance. The default window size of 5 is optimal for most images.

### Masking Ratio

The "masking ratio" parameter determines the proportion of pixels within each patch that are randomly masked during N2V training. The best denoising performance is achieved by using sampling replacement pixels from the areas surrounding the masked pixels (not by replacing the masked pixel with zero) and N2V forces the neural network to learn a more robust representation of the underlying image structure, rather than simply memorizing the specific noise patterns in the input image. The masking ratio controls the level of noise injection during training, with higher values leading to more aggressive masking and generally better performance on noisy datasets. If the masking ratio is too small, the model may not be able to learn the noise distribution effectively, which can lead to poor denoising performance.
In general, the optimal values for these parameters will depend on the specific characteristics of the input image and the amount and type of noise present in the data. It is often necessary to experiment with different values to determine the best combination for a given task.

---

## Remarks and pitfalls

- if training images show only one type of structure, but later the model is applied to images with totally different structures, the model might “hallucinate”

- the performance of any denoising approach should be assessed based on the final goal of the analysis pipeline

- denoised images can be used to obtain certain features of the image, such as a more robust segmentation or localization of objects that is usually the basis for subsequent intensity measurements

- the effect of denoising on the quantifiability of the pixel intensities is a matter of ongoing research

- be careful when using N2V or any other method that modifies pixel values when the final application is something like FRET or Ratiometric Imaging, where the conclusion may directly depend on the pixel counts

- a nice summary of the benefits and possible limitation of AI-based denoising can be found here: [Imaging in focus: An introduction to denoising bioimages in the era of deep learning](https://www.sciencedirect.com/science/article/pii/S1357272521001588)

## TechNotes Intellesis Denoising

- Training of Noise2Void models is done locally – the training pipeline is part of the ZeissPy distribution (automatically installed with ZEN)
  - 8GB GPU (or better) is recommended for the training
  - model inference also works reasonable well on CPU only
- training Pipeline is using TensorFlow2 and is integrated into prismalearn package
- models are stored using the ONNX format
- Import of external N2V and general regression models is possible
- check [Colab notebooks](https://colab.research.google.com/github/zeiss-microscopy/OAD/blob/master/Machine_Learning/notebooks/czmodel/Regresssion_3_0_0.ipynb)
- Support of Denoising and Regression model inside [czmodel] package


[ZEN blue]: https://www.zeiss.com/microscopy/en/products/software/zeiss-zen.html
[ZEN core]: https://www.zeiss.com/microscopy/en/products/software/zeiss-zen-core.html
[PyPI]: https://pypi.org/
[czmodel]: https://pypi.org/project/czmodel/
[cztile]: https://pypi.org/project/cztile/
[arivis Cloud]: https://www.apeer.com/
[arivis Pro]: https://www.arivis.com/products/pro
[arivis AI]: https://www.apeer.com/app/ai-toolkit/overview
[Python]: https://www.python.org/
[Dask]: https://dask.org/
[Scikit-Learn]: https://scikit-learn.org/
[Tensorflow]: https://www.tensorflow.org/
[Napari]: https://napari.org/
[BioApps]: https://www.zeiss.com/microscopy/en/products/software/zeiss-zen/bio-apps.html
[ZEN Intellesis]: https://www.zeiss.com/microscopy/int/products/microscope-software/zen-intellesis-image-segmentation-by-deep-learning.html