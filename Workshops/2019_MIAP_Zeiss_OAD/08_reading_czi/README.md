### Reading CZI and other image file formats

This session will provide some detailed information about the CZI image file format

#### The CZI File Format

A core component of every image acquisition software is obviously the used image file format.
In case of ZEISS microscopy control software this image format is called **CZI**, which is is an open format. Detailed specifications can be found here: **[CZI - Image Format for Microscopes](https://www.zeiss.com/microscopy/int/products/microscope-software/zen/czi.html)**

In order get get access to to technical specifications plese use the following link: **[CZI Format License request](https://www.zeiss.com/microscopy/int/products/microscope-software/czi/czi-download.html)**

***

#### BIO-FORMATS and OME-TIFF

Without any doubt the OME-TIFF image file format: **[OME-TIFF Format](https://docs.openmicroscopy.org/ome-model/6.0.0/ome-tiff/index.html)** especially when combined with the power of the BioFormats library: **[BIO-FORMATS](https://www.openmicroscopy.org/bio-formats/)**

***

#### Available Tools

For easily reading CZI and OME-TIFF images with various options have a look at the following scripts:

* **[czireader_complete.py](https://github.com/zeiss-microscopy/OAD/blob/master/Apeer/fiji_scripts/czireader_complete.py)**

* **[fijipytools.py](https://github.com/zeiss-microscopy/OAD/blob/master/Apeer/fiji_scripts/fijipytools.py)**

For reading and displaying CZI and OME_TIFF files inside a Jupyter notebook please go here:

* **[Read_and_Display_Images_using_Widgets_and_Napari](https://github.com/zeiss-microscopy/OAD/tree/master/jupyter_notebooks/Read_CZI_and_OMETIFF_and_display_widgets_and_napari)**
