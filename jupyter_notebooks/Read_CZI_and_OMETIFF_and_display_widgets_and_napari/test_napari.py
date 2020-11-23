import imgfileutils as imf
from aicsimageio import AICSImage, imread, imread_dask
# from aicsimageio.writers import ome_tiff_writer
# from aicspylibczi import CziFile
# import czifile


#filename = r'testdata/CellDivision_T=10_Z=15_CH=2_DCV_small.czi'
#filename = r"C:\Users\m1srh\OneDrive - Carl Zeiss AG\Testdata_Zeiss\Castor\Z-Stack_DCV\NeuroSpheres_DCV.czi"
#filename = r"C:\Users\m1srh\OneDrive - Carl Zeiss AG\Testdata_Zeiss\AiryScan\FoLu_mCherryEB3_GFPMito_2_Airyscan Processing.czi"
filename = r"C:\Users\m1srh\Documents\GitHub\czi_demos\testdata\CellDivision_T=10_Z=15_CH=2_DCV_small.ome.tiff"

md, addmd = imf.get_metadata(filename)

img = AICSImage(filename)
stack = img.get_image_data()

layers = imf.show_napari(stack, md,
                         blending='additive',
                         gamma=0.85,
                         add_mdtable=False,
                         rename_sliders=True)
