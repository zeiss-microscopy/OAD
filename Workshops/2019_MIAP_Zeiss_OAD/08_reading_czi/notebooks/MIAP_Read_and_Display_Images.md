```python
#################################################################
# File       : MIAP_Read_and_Display_Images.ipynb
# Version    : 0.1
# Author     : czsrh
# Date       : 02.11.2019
# Insitution : Carl Zeiss Microscopy GmbH
#
# Disclaimer: Just for testing - Use at your own risk.
# Feedback or Improvements are welcome.
##################################################################
```

Here we do all the required imports.


```python
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

from apeer_ometiff_library import io, processing, omexmlClass
import czifile as zis
import xmltodict
import os
import numpy as np
import ipywidgets as widgets
import napari
import imgfileutils as imf
import xml.etree.ElementTree as ET
```


```python
# define your testfiles here

imgdict = {
    1:r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small.czi',
    2:r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small.ome.tiff',
    3:r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small_Fiji.ome.tiff',
    4:r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=15_Z=20_CH=2_DCV.czi',
    5:r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\NeuroSpheres_DCV_A635_A488_A405.czi',
    6:r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CZI_DimorderTZC.czi'
}

filename = imgdict[1]
```


```python
# get CZI object and read array
czi = zis.CziFile(filename)
mdczi = czi.metadata()
czi.close()

# parse the XML into a dictionary
metadatadict_czi = xmltodict.parse(mdczi)
```


```python
# change file name
xmlfile = filename.replace('.czi', '_CZI_MetaData.xml')

# get the element tree
tree = ET.ElementTree(ET.fromstring(mdczi))

# write xml to disk
tree.write(xmlfile, encoding='utf-8', method='xml')

print('Write special CZI XML metainformation for: ', xmlfile)
```

    Write special CZI XML metainformation for:  C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small_CZI_MetaData.xml
    


```python
# or much shorter
xmlczi = imf.writexml_czi(filename)
print(xmlczi)
```

    C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small_CZI_MetaData.xml
    


```python
# create dictionary for the interesting CZI metadata
czimd = {}

czimd['Experiment'] = metadatadict_czi['ImageDocument']['Metadata']['Experiment']
czimd['HardwareSetting'] = metadatadict_czi['ImageDocument']['Metadata']['HardwareSetting']
czimd['CustomAttributes'] = metadatadict_czi['ImageDocument']['Metadata']['CustomAttributes']
czimd['Information'] = metadatadict_czi['ImageDocument']['Metadata']['Information']
czimd['PixelType'] = czimd['Information']['Image']['PixelType']
```


```python
# show some metadata
for key, value in czimd['Information']['Image'].items():
    # print all key-value pairs for the dictionary
    print(key, ' : ', value)

```

    SizeX  :  256
    SizeY  :  256
    SizeB  :  1
    OriginalCompressionMethod  :  Uncompressed
    OriginalEncodingQuality  :  100
    AcquisitionDateAndTime  :  2016-02-12T09:41:02.4915604Z
    SizeC  :  2
    SizeZ  :  15
    SizeT  :  10
    ComponentBitCount  :  14
    PixelType  :  Gray16
    Dimensions  :  OrderedDict([('Channels', OrderedDict([('Channel', [OrderedDict([('@Id', 'Channel:0'), ('@Name', 'LED555'), ('ExcitationWavelength', '553'), ('EmissionWavelength', '568'), ('DyeId', 'McNamara-Boswell-0046'), ('DyeDatabaseId', '66071726-cbd4-4c41-b371-0a6eee4ae9c5'), ('Color', '#FFFF7E00'), ('Fluor', 'Alexa Fluor 555'), ('ExposureTime', '100000000'), ('IlluminationType', 'Epifluorescence'), ('ContrastMethod', 'Fluorescence'), ('PixelType', 'Gray16'), ('ComponentBitCount', '14'), ('AcquisitionMode', 'WideField'), ('IlluminationWavelength', OrderedDict([('SinglePeak', '567'), ('Ranges', '540-570')])), ('DetectionWavelength', None), ('DetectorSettings', OrderedDict([('Binning', '1,1'), ('Detector', OrderedDict([('@Id', 'Detector:Axiocam 506')]))])), ('LightSourcesSettings', OrderedDict([('LightSourceSettings', OrderedDict([('Intensity', '50.00 %'), ('LightSource', OrderedDict([('@Id', 'LightSource:1')]))]))])), ('FilterSetRef', OrderedDict([('@Id', 'FilterSet:1')]))]), OrderedDict([('@Id', 'Channel:1'), ('@Name', 'LED470'), ('ExcitationWavelength', '493'), ('EmissionWavelength', '517'), ('DyeId', 'McNamara-Boswell-0038'), ('DyeDatabaseId', '66071726-cbd4-4c41-b371-0a6eee4ae9c5'), ('Color', '#FF00FF33'), ('Fluor', 'Alexa Fluor 488'), ('ExposureTime', '200000000'), ('IlluminationType', 'Epifluorescence'), ('ContrastMethod', 'Fluorescence'), ('PixelType', 'Gray16'), ('ComponentBitCount', '14'), ('AcquisitionMode', 'WideField'), ('IlluminationWavelength', OrderedDict([('SinglePeak', '469'), ('Ranges', '450-488')])), ('DetectionWavelength', None), ('DetectorSettings', OrderedDict([('Binning', '1,1'), ('Detector', OrderedDict([('@Id', 'Detector:Axiocam 506')]))])), ('LightSourcesSettings', OrderedDict([('LightSourceSettings', OrderedDict([('Intensity', '50.00 %'), ('LightSource', OrderedDict([('@Id', 'LightSource:2')]))]))])), ('FilterSetRef', OrderedDict([('@Id', 'FilterSet:2')]))])])])), ('Tracks', OrderedDict([('Track', [OrderedDict([('@Id', 'Track:2'), ('ChannelRefs', OrderedDict([('ChannelRef', OrderedDict([('@Id', 'Channel:0')]))]))]), OrderedDict([('@Id', 'Track:3'), ('ChannelRefs', OrderedDict([('ChannelRef', OrderedDict([('@Id', 'Channel:1')]))]))])])])), ('T', OrderedDict([('StartTime', '2016-02-12T09:41:02.4915604Z'), ('Positions', OrderedDict([('List', OrderedDict([('Offsets', '0 60.075 120.151 180.226 240.302 300.377 360.453 420.528 480.603 540.679')]))]))])), ('Z', OrderedDict([('XYZHandedness', 'Undefined'), ('ZAxisDirection', 'Undefined'), ('StartPosition', '-3.52'), ('Positions', OrderedDict([('List', OrderedDict([('Offsets', '0 0.32 0.64 0.96 1.28 1.6 1.92 2.24 2.56 2.88 3.2 3.52 3.84 4.16 4.48')]))]))]))])
    ObjectiveSettings  :  OrderedDict([('RefractiveIndex', '1.33'), ('Medium', 'Water'), ('CorrectionControllerMode', 'Glass Thin'), ('CorrectionControllerBottomThickness', '175'), ('ObjectiveRef', OrderedDict([('@Id', 'Objective:1')]))])
    Specimen  :  OrderedDict([('CoverglassThickness', '175'), ('CoverglassRefractiveIndex', '1.52'), ('CoverglassOffset', '995'), ('CoverglassMaterial', 'Glass')])
    MicroscopeRef  :  OrderedDict([('@Id', 'Microscope:1')])
    TubeLenses  :  OrderedDict([('TubeLensRef', OrderedDict([('@Id', 'TubeLens:1')]))])
    SpatialRelations  :  OrderedDict([('PixelToStageTransform', OrderedDict([('RotateFlipScaleTranslateImplicitScale', OrderedDict([('Rotate', '0'), ('Flip', OrderedDict([('@X', 'false'), ('@Y', 'false')])), ('Translate', OrderedDict([('@X', '16971.264400244756'), ('@Y', '18619.585960423425')]))]))]))])
    

### Remark

As one can clearly see there are a lot of metadata not all of them are needed for every workflow.


```python
# read metadata and array differently for OME-TIFF or CZI data
if filename.lower().endswith('.ome.tiff') or filename.lower().endswith('.ome.tif'):
    
    # Return value is an array of order (T, Z, C, X, Y)
    (array, omexml) = io.read_ometiff(filename)
    metadata = imf.get_metadata(filename, series=0)
    
if filename.lower().endswith('.czi'):

    # get the array and the metadata
    array, metadata = imf.get_array_czi(filename)
```


```python
# outout the shape of the returned numpy array

# shape of numpy array
print('Array Shape: ', array.shape)

# dimension order from metadata
print('Dimension Order (BioFormats) : ', metadata['DimOrder BF Array'])

# shape and dimension entry from CZI file as returned by czifile.py
print('CZI Array Shape : ', metadata['Shape'])
print('CZI Dimension Entry : ', metadata['Axes'])
```

    Array Shape:  (1, 10, 2, 15, 256, 256)
    Dimension Order (BioFormats) :  None
    CZI Array Shape :  (1, 10, 2, 15, 256, 256, 1)
    CZI Dimension Entry :  BTCZYX0
    


```python
# show dimensions and scaling
print('SizeT : ', metadata['SizeT'])
print('SizeZ : ', metadata['SizeZ'])
print('SizeC : ', metadata['SizeC'])
print('SizeX : ', metadata['SizeX'])
print('SizeY : ', metadata['SizeY'])
print('XScale: ', metadata['XScale'])
print('YScale: ', metadata['YScale'])
print('ZScale: ', metadata['ZScale'])
```

    SizeT :  10
    SizeZ :  15
    SizeC :  2
    SizeX :  256
    SizeY :  256
    XScale:  0.091
    YScale:  0.091
    ZScale:  0.32
    


```python
# show all the metadata
for key, value in metadata.items():
    # print all key-value pairs for the dictionary
    print(key, ' : ', value)
```

    Directory  :  C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV
    Filename  :  CellDivision_T=10_Z=15_CH=2_DCV_small.czi
    Extension  :  czi
    ImageType  :  czi
    Name  :  None
    AcqDate  :  2016-02-12T09:41:02.4915604Z
    TotalSeries  :  None
    SizeX  :  256
    SizeY  :  256
    SizeZ  :  15
    SizeC  :  2
    SizeT  :  10
    Sizes BF  :  None
    DimOrder BF  :  None
    DimOrder BF Array  :  None
    DimOrder CZI  :  {'B': 0, 'S': -1, 'T': 1, 'C': 2, 'Z': 3, 'Y': 4, 'X': 5, '0': 6}
    Axes  :  BTCZYX0
    Shape  :  (1, 10, 2, 15, 256, 256, 1)
    isRGB  :  None
    ObjNA  :  1.2
    ObjMag  :  50.0
    ObjID  :  Objective:1
    ObjName  :  Plan-Apochromat 50x/1.2
    ObjImmersion  :  Water
    XScale  :  0.091
    YScale  :  0.091
    ZScale  :  0.32
    XScaleUnit  :  µm
    YScaleUnit  :  µm
    ZScaleUnit  :  µm
    DetectorModel  :  Axiocam 506
    DetectorName  :  Axiocam506m
    DetectorID  :  Detector:Axiocam 506
    InstrumentID  :  None
    Channels  :  ['AF555', 'AF488']
    ImageIDs  :  []
    PixelType  :  Gray16
    SizeM  :  1
    SizeB  :  1
    SizeS  :  1
    SW-Name  :  ZEN 3.1 (blue edition)
    SW-Version  :  3.1.0.0000
    TubelensMag  :  1.0
    ObjNominalMag  :  50.0
    


```python
# display data using ipy widgets
if metadata['Extension'] == 'ome.tiff':
    ui, out = imf.create_ipyviewer_ome_tiff(array, metadata)
if metadata['Extension'] == 'czi':
    ui, out = imf.create_ipyviewer_czi(array, metadata)

display(ui, out)
```

    0 38276
    


    Output()



    VBox(children=(IntSlider(value=1, continuous_update=False, description='Blocks:', disabled=True, max=1, min=1)…



```python
import time

# switch to qt5 backend for napari viewer and wait a few seconds
%gui qt5
time.sleep(5)
```


```python
# try to configure napari automatiaclly based on metadata
imf.show_napari(array, metadata)
```


```python
# configure napari viewer manually - check array shape and dimensions order carefully 
    
# get the scalefactors
scalefactors = imf.get_scalefactor(metadata)
print(scalefactors)

array = np.squeeze(array, axis=(0, 1))

viewer = napari.Viewer()
# add every channel as a single layer
for ch in range(metadata['SizeC']):
    chname = metadata['Channels'][ch]
    viewer.add_image(array[ch, :, :, :], name=chname, scale=(1, scalefactors['zx'], 1, 1))
```

jupyter nbconvert MIAP_Read_and_Display_Images.ipynb --to slides --post serve
