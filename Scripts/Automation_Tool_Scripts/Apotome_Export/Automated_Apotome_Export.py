# get the active document
image = Zen.Application.Documents.ActiveDocument

# rename it
image_name = image.Name.Replace('.czi', '_Apotome.czi')
image_filename = image.FileName.Replace(image.Name, image_name)

# check for the Apotome related special CZI Dimensions
nb_phase = image.Bounds.SizeH
if (nb_phase > 2):
    # do the processing
    apotome_image = Zen.Processing.Utilities.ApoTomeSimConvert(image,
                                                               ZenApoTomeProcessingMode.Sectioned,
                                                               ZenSimCorrectionMode.LocalIntensity,
                                                               ZenNormalizeMode.Clip,
                                                               ZenApoTomeFilter.Off,
                                                               False)
    # save the image and add it to the document area
    apotome_image.Save(image_filename)
    Zen.Application.Documents.Add(apotome_image)
