## Intellesis and Machine Learning

The ZEN software platform has various built-in image segmentation function. One of those tolls is called ZEN Intellesis Trainable Segmentation, which is using machine-learning algorithms to segment images. More information can be found here:


[Intellesis Trainable Segmentation](https://www.zeiss.com/microscopy/int/website/landingpages/zen-intellesis.html)

![ZEN Intellesis Trainable Segmentation](/Images/ZEN_Intellesis_Cover.png)

***

### Main Features of Software Module

* **Simple User Interface for Labelling and Training**
* **Integration into ZEN Measurement Framework**
* **Support for Multi-dimensional Datasets**

    - Real Multi-Channel Feature Extraction
    - Engineered Feature Sets and Deep Feature Extraction on GPU
    - Pixel Classification by Random Forrest Classifier
    - Classification post-processing by Conditional Random Field
    - Scriptable segmentation functions for advanced automation
    - SW Trial License and bundle with Image Analysis available
    - Client-Server Architecture using REST-APIs

***

### Applications

ZEN can basically read any image data format using the BioFormats Import and Intellesis can therefore be used to segment **any multi-dimensional dataset** that can be imported into the software. Shown below are imaged segmented using Intellesis.

***

![ZEN Python](/Images/intellesis_ms_apps.png)

*Intellesis - Material Science Applications*

***

![ZEN Python](/Images/intellesis_ls_apps.png)

*Intellesis - Life Science Applications*

***

### Software

The actual segmentation service is completly written in Python and is using proven and established open-source machine-learning libraries to segment the images.

To be able to handle even large multi-dimensional datasets, the software has a built-in data manager that takes care of splitting nad distributing the workload depending on the availbale computation resources.

***

![ZEN Python](/Images/intellesis_dataflow.png)

*Intellesis - DataFlow*

***

Due to the fact that the SegmentationService is written completely in Python is can be used a module on the APEER platform. The complete SegmenationService is running inside a Linux-based docker container.

![Intellesis on APEER](/Images/intellesis_apeer.png)

*APEER Workflow using the Intellesis SegmentationService as a module*

***

If you want to test this platform, register here:

[APEER Platfrom](https://www.apeer.com/app/#/home)

To read about the newest developments on APEER read the blog:

[APEER Blog](https://www.apeer.com/app/#/home)

***

## Scripts

### ZEN_Intellesis_Simple_Test.py

This simple script demonstrated the different possibilities to segment an image using a trained model. The result of such a segmentation is a mask image, which has either as many channels as the models has classes, or one channel containing a distinct label for every class.

![ZEN Python](/Images/intellesis_segoptions.png)

*(top left) - raw image data data (top right) segmented image (bottom left) segmeneted with confidence threshold and (bottom right) probobility map image*

### Intellesis_Batch_Tool.py

![ZEN Python](/Images/intellesis_batch.png)

*Intellesis - Batch Tool*

***

The Intellesis Batch Tool allows you to automate and simplify the following tasks:

- Select a model to segment images
- Specify the desired output format for the mask image
- Optional Probability Treshold that can be appied to mask image
- Optional Extraction of a specific singkle class
- Option to add the mask image to the original image
- Selection of output folder with file extension filter

Beside this tool is is alos possible to run a segmenation using the ZEN built-in batch tool, hwich does not require this script but offers less addtional options.
