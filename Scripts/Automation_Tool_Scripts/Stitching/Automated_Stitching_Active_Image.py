# Run Stitching automatically after acquisition

# get the active image document
image = Zen.Application.Documents.ActiveDocument

# get the stitching settings
Stitchset = r'Stitching_Channel_1.czips'

# create a function setting for the Stiching Function
functionsetting1 = Zen.Processing.Transformation.Geometric.Stitching(image)

# apply the setting
functionsetting1.Load(Stitchset)

print('Done.')
