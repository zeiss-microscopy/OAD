from skimage import color, img_as_float, img_as_uint, io, exposure
from skimage.color import rgb2hed
import numpy as np
import tifffile as tf

"""
Example is based on this:

A. C. Ruifrok and D. A. Johnston
“Quantification of histochemical staining by color deconvolution”
Analytical and quantitative cytology and histology - the International Academy of Cytology [and] American Society of Cytology
Vol. 23, no. 4, pp. 291-9, Aug. 2001.

For more details please go to: https://scikit-image.org/docs/dev/api/skimage.color.html#skimage.color.hed2rgb

"""


def run(original_image_path):

    outputPathList = []

    # Read original image
    ihc_rgb = io.imread(original_image_path)

    # Process
    ihc_hed = rgb2hed(ihc_rgb)
    ihc_h = exposure.rescale_intensity(ihc_hed[:, :, 0], out_range=(0, 255))
    ihc_e = exposure.rescale_intensity(ihc_hed[:, :, 1], out_range=(0, 255))
    ihc_d = exposure.rescale_intensity(ihc_hed[:, :, 2], out_range=(0, 255))

    images = [ihc_h, ihc_e, ihc_d]
    outnames = ['Hematoxylin.tiff', 'Eosin.tiff', 'DAB.tiff']

    for img, out in zip(images, outnames):

        outputPathList.append(out)
        tf.imwrite(out, np.int16(img))

    tf.imwrite('HED.tiff', np.float16(ihc_hed))
    outputPathList.append('HED.tiff')

    print(outputPathList)

    # Return apeer output values as dictionary
    return {'processed_images': outputPathList}
