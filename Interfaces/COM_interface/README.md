## COM-Interface

### MATLAB - Example

This application note will explain how create a workﬂow using the ZEN-MATLAB connection. The basic idea is to control everything from within MATLAB (Master).

The ZEN Image Acquisition (Slave) software is "only" doing the image acquisition. The
signal to start the experiment is send from MATLAB to ZEN.

When the experiment is finished, the CZI data are imported into MATLAB using BioFormats and "some" simple image analysis is carried out to underline the workﬂow concept.

For more detailed information please goto: [Control ZEN Blue and the microscope from MATLAB](https://de.mathworks.com/matlabcentral/fileexchange/50079-control-zen-blue-and-the-microscope-from-matlab?requestedDomain=www.mathworks.com)

***

![COM MATLAB_Running](../../images/ZEN_ML_Running.png)

***


![COM_MATLAB_Result](../../images/ZEN_MATLAB_Result_Figure.png)

***

### Python Example

This application note will explain how to create a workﬂow using the ZEN-Python connection. The basic idea is to control everything from within Python (Master). While ZEN internally is using IronPython, this notes describes how to control ZEN from within
a CPython implementation.

The ZEN Image Acquisition (Slave) software is "only" doing the image acquisition. The signal to start the experiment is send from Python to ZEN.

When the experiment is fnished, the CZI data are imported into Python using BioFormats and "some" simple image analysis is carried out to underline the workﬂow concept.

***

![COM_Python_Running Result](../../images/ZEN_Python_Running_Results_1.png)

***

![COM_Python_Running Result](../../images/ZEN_Python_Running_Results_2.png)
