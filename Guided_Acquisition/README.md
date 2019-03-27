## Guided Acquisition

### Key Facts

* **Run Overview Experiment**
* **Use Image Analysis to automatically detect "objects"**
* **Modify experiments based on those parameters**
* **Execute the modified experiment for all detected objects**

### General Workflow Description

For a growing number of applications, it will be crucial to acquire data in a smart way. One way to achieve this goal is to build a smart microscope, which essentially means creating smart software workflows to control the hardware based on image analysis results.

#### Idea or Task:

* Scan or inspect a large area (or a long period of time).
* Detect an "interesting" object.
* Acquire detailed data for every event.
* Automate the workflow to minimize user bias.

First of all it is important to define what a **Object of Interest** can actually be. Example would be an object that meets specific criteria, for example:

* Size
* Brightness
* Shape
* Intensity
* Combinations of the above

It could be something quite simple. For instance one can have lots of cells, that are stained with blue dye, and only a few of them (maybe where the transfection worked …) are also expressing GFP.
The idea here would be to detect all cells that are positive for both colors and acquire an z-Stack for every cell that meets those criteria. Therefore this kind of application requires three major tasks:

* **Define the Overview Scan Experiment.**
* **Define the object detection rules, e.g. setup image analysis.**
* **Define the Detailed Scan(s) to be carried out in case of a "positive" object.**

### Main Workflow Description

* Acquire some sample data showing a object of interest.
* Setup an Image Analysis Pipeline to detect those events.
* Define an experiment which does the Overview Scan.
* Define an experiment which does the Detailed Scan.

The goal of this tutorial is to create an automated workflow that can be used to easily setup a **Guided Acquisition**. This requires some knowledge about the OAD macro environment and its **scripting language Python**.

***

![Workflow - Actionable Information ](/images/GuidedAcq_NEW.png)*Workflow Guided Acquisition*

***

![Workflow - Actionable Information using OAD](/images/Guided_Acquisition_PPTX_Slide.png)*Guided Acquisition using scripting*

***

### Detailed WorkFlow Diagram

![Workflow - Guided Acquisition diagram](/images/GuidedAcq_Script_Diagram_v2.png)*General Worklow diagram for Guided Acquisition*

***

### Application Example - Mitosis Detection using camera and LSM

An especially interesting option is to combine the power of a camera-based overview scan with the optional sectioning capabilities of an LSM. Such an workflow can be easily configured in ZEN Blue by setting up the respective experiment for the overview scan with camera detection using a low magnification and the LSM-based detail scan, e.g. Z-Stack, using a high NA objective.

Since ZEN Blue 2.5 this software has a module called **ZEN Connect**, which allows combining and correlating images inside one sample-centric workspace. Every acquired image by either the camera or the LSM) will be placed here based on the XY stage coordinates. Therefore the **Correlative Workspace (CWS)** is ideally suited to display the results of an Guided Acquisition workflow.

More information about ZEN Connect can be found here: [ZEN Connect](https://www.zeiss.com/microscopy/int/products/microscope-software/zen-connect-image-overlay-and-correlative-microscopy.html)

![Overview Scan inside the Correlative Workspace](/images/GA_Mitosis_CWS_Overview.png)*Overview Scan inside the Correlative Workspace*

***

![Overlay of "positive" object and detailed image](/images/GA_Mitosis_CWS_Overlay.png)*Overlay of "positive" object and detailed image* 

***

![Side-by-Side view of overview in CWS and detailed image](/images/GA_Mitosis_CWS_Detail_ZEN.png)*Side-by-Side view of overview in CWS and detailed image*

***

## Disclaimer

**This is an application note that is free to use for everybody. Use it on your own risk. Especially be aware of the fact that automated stage movements might damage hardware if the system is setup properly. Please check everything in simulation mode first!**

Carl Zeiss Microscopy GmbH's ZEN software allows connection to the third party software, Python. Therefore Carl Zeiss Microscopy GmbH undertakes no warranty concerning Python, makes no representation that Python will work on your hardware, and will not be liable for any damages caused by the use of this extension. By running this example you agree to this disclaimer.
