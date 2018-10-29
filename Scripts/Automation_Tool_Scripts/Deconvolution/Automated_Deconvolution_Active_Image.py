# Run Deconvolution automatically after acquisition

from System.IO import File, Directory, FileInfo, Path

OutImage = r'C:\\ZEN_Output'

image = Zen.Application.Documents.ActiveDocument

DCVset = r'Lucy_Richardson_DCV.czips'
functionsetting1 = Zen.Processing.Deconvolution.Settings.DeconvolutionSetting(image)
functionsetting1.Load(DCVset, ZenSettingDirectory.User)

# apply DCV setting to image

dcv = Zen.Processing.Deconvolution.Deconvolution(image, functionsetting1)
fileNameWE = image.Name.Substring(0, image.Name.Length - 4)
newFileName = fileNameWE + '_dcv' + '.czi'
imageName = Path.Combine(OutImage, newFileName)
dcv.Save(imageName)

# End
