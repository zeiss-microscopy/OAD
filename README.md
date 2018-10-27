# Open Application Development (OAD)

ZEN Blue is an open, flexible and powerful image acquisition platform that allows controlling a wide range of microscopes systems. Additionally it offers various tools to automate workflows including acquisition and image analysis tasks.

In order to fulfill the request for automation the ZEN Blue platform offers various features and options, which are combined inside a concept called Open Application Development (OAD).

Its main components are:

*    CZI image data format and its APIs
*    Python Scripting (OAD Simple API) 
*    Interfaces to ZEN (TCP-IP, COM, Extensions)
*    Experiment Feedback (Adaptive Acquistion with Online Image Analysis)   

***
![Screenshot of GUI](/images/ZEN_OAD_Tools_Slide.png)
***

## OAD - General Concept and Key Features

* **Open Application Development** (OAD) uses powerful **Python Scripts** to **simplify, customize** and **automate** your workflows.

* **Analyze** and **Exchange** data with applications like **Fiji, Python, Knime, CellProfiler, Icy, MATLAB, Excel** and …

* The** CZI-API for .NET (ZeissImgLib)** and for **C++ (libCZI)** and **BioFormats(CZIReader)** allow easy access to CZI files from many external applications. (OME-TIFF Export and Import in ZEN Blue is possible)

* **BioFormats Impor**t as a module inside ZEN Blue

* Create **“smart”** experiments with **Experiment Feedback** and modify the acquisition **On-the-fly** based on **Online Image Analysis** and **External Inputs** 

***
![Screenshot of GUI](/images/OAD_Overview.png)
***

## Links and Referneces

* CZI Image Data Format for microscopes: http://www.zeiss.com/czi

* ZEISS OAD Forum: http://www.zeiss.com/zen-oad

* Open Source Cross-Platform API to read CZI: http://github.com/zeiss-microscopy/libCZI

* The OME-TIFF format: http://www.openmicroscopy.org/site/support/file-formats/ome-tiff

***

# Disclaimer

This is an collection of OAD scripts that is free to use for everybody.
Carl Zeiss Microscopy GmbH's ZEN software undertakes no warranty concerning the use of those scripts. Use them on your own risk.

Additionally Carl Zeiss Microscopy GmbH's ZEN software allows connection to the third party software packages.

Therefore Carl Zeiss Microscopy GmbH undertakes no warranty concerning those software packages, makes no representation that they will work on your system and/or hardware and will not be liable for any damages caused by the use of this extension.

By using any of thos examples you agree to this disclaimer.

Version: 2018.10.14
