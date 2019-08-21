# Announcement

![MIAP ZEISS OAD Workshop](/Images/Advertise_Zeiss_OAD_Workshop.png)


## MIAP Workshop: Expanding the ZEISS Microscopy Platform - Automation and Image Analysis Solutions based on OAD and APEER

### Location and Date

- **Center for Biological Systems Analysis (ZBSA) - Life Imaging Center (LIC)**

- **Albert-Ludwigs University Freiburg, Habsburgerstr. 49, 79104 Freiburg im Breisgau**

- **4-7 November 2019**

For more information and registration: [**MIAP ZEISS OAD and APEER Workshop**](https://miap.eu/miap-events/miap-workshops/2019-11-zeiss-oad-apeer/) or email to [**info@miap.eu**](mailto:info@miap.eu)

### Goal of the workshop

 The goal of this 4-day workshop is to teach and train participants how to employ the ZEISS software ecosystem for their own projects in image processing, analysis and microscope automation.

We will discuss the latest developments in image analysis and machine learning, including the novel free image processing platform [APEER](https://www.apeer.com), which enables users to exchange image processing modules and assemble them into powerful processing workflows. You will learn how to use APEER in the cloud and how to set up a local APEER solution based on the [ACQUIFER](https://www.acquifer.de/) HIVE system.

We will show best practices and application examples in a hands-on session focused on:

- How to automate image acquisition and analysis using OAD scripts ([Open Application Development](https://github.com/zeiss-microscopy/OAD))
- How to set up adaptive feedback experiment workflows in combination with APEER, Fiji/ImageJ etc.
- How to leverage the full potential of ZEN Blue and 3rd party image processing in your image processing and analysis workflows
- How to create your own APEER modules
- How to build your own local APEER server using the HIVE solution from ACQUIFER.

The workshop will include lectures, discussions and extensive hands-on sessions using the microscope infrastructure of the Life Imaging Center (LIC).

Participants are invited to give a talk about their workshop-related projects, research (requirements) and custom solutions. Participants are also encouraged to bring their own samples or experimental workflows, discuss them with the teachers and derive custom solutions for their individual microscopy and image analysis challenges. Please contact us in advance about the prerequisites.

- **Basic knowledge in light microscopy and scripting is required.**

- **Maximal number of participants: 15**

- **Deadline for applications: 8th of September 2019**

### Agenda

The agenda as PDF can be found here: [Workshop Agenda (PDF)](../Workshops/2019_MIAP_ZEISS_OAD/Agenda_Zeiss_OAD_v3.pdf) and here a a web document: [Workshop Agenda](../Workshops/2019_MIAP_ZEISS_OAD/2019_miap_zeiss_oad_agenda.md)

***

# Open Application Development (OAD)

ZEN Blue is an open, flexible and powerful image acquisition platform that allows controlling a wide range of microscopes systems. Additionally it offers various tools to automate microscopy workflows including acquisition, image analysis and image processing tasks.

In order to fulfill the request for automation the ZEN Blue platform offers various features and options, which are combined inside a concept called Open Application Development (OAD).

Its main components are:

*    **CZI image data format and its APIs**
*    **Python Scripting (OAD Simple API)**
*    **Interfaces to ZEN (TCP-IP, COM, Extensions)**
*    **Experiment Feedback - Adaptive Acquistion with Online Image Analysis**

***

![OAD Tools](/Images/ZEN_OAD_Tools_Slide.png)*ZEN OAD Tools*

***


## OAD - General Concept and Key Features

* **Open Application Development** (OAD) uses powerful **Python Scripts** to **simplify, customize** and **automate** your workflows.

* **Analyze** and **Exchange** data with applications like **Fiji, Python, Knime, CellProfiler, Icy, MATLAB, Excel** and …

* API for reading CZI image data using custom software
    * **ZeissImgLib (.NET)** to be used on Windows-based systems
    * **libCZI (C++)** for cross-platform applications
    * **BioFormats (CZIReader)** allow easy access to CZI files from many external applications using the BioFormats library

* **BioFormats Import** as a module inside ZEN Blue as well as **OME-TIFF Export**

* Create **“smart”** experiments with **Experiment Feedback** and modify the acquisition **On-the-fly** based on **Online Image Analysis** and **External Inputs** 

***

![OAD Interfaces](/Images/OAD_Overview.png)*OAD Interfaces*

***

![Automated Dynamics](/Videos/Automated_Physiology_IA.gif)*Automated Dynamics*

***

![External Software](/Videos/GuidedAcquisition_ZEN_Fiji.gif)*External Software*


***

## Links and References

* CZI Image Data Format for microscopes: http://www.zeiss.com/czi

* ZEISS OAD Forum: http://www.zeiss.com/zen-oad

* Open Source Cross-Platform API to read CZI: http://github.com/zeiss-microscopy/libCZI

* OAD - Open Application Development: https://github.com/zeiss-microscopy/OAD

* The OME-TIFF format: http://www.openmicroscopy.org/site/support/file-formats/ome-tiff

***

# Disclaimer

This is an collection of OAD scripts that is free to use for everybody. 
Carl Zeiss Microscopy GmbH's ZEN software undertakes no warranty concerning the use of those scripts, image analysis settings and ZEN experiments. Use them on your own risk.

Additionally Carl Zeiss Microscopy GmbH's ZEN software allows connection to the third party software packages.

Therefore Carl Zeiss Microscopy GmbH undertakes no warranty concerning those software packages, makes no representation that they will work on your system and/or hardware and will not be liable for any damages caused by the use of this extension.

By using any of thos examples you agree to this disclaimer.

Version: 2018.11.01

Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
