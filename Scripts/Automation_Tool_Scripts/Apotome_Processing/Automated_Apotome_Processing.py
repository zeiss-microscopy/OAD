# Run ApoTome Processing automatically after acquisition

Outputfolder = r'C:\\ZEN_Output'

# Read Active Image &amp; prepare Output Image

image = Zen.Application.Documents.ActiveDocument

# Process ApoTome Active Raw Image

nb_phase = image.Bounds.SizeH
apotome_image = Zen.Processing.Utilities.ApoTomeSimConvert(image,
                                                           ZenApoTomeProcessingMode.Sectioned,
                                                           ZenSimCorrectionMode.LocalIntensity,
                                                           ZenNormalizeMode.Clip,
                                                           ZenApoTomeFilter.Off,
                                                           False)

# add newly create image to the document area
Zen.Application.Documents.Add(apotome_image)

# Save Processed file
image_name = image.Name.Replace('.czi', '_Apotome.czi')
imageName = Path.Combine(Outputfolder, image_name)
apotome_image.Save(imageName)

print('Done.')
