# get all available object classification models
ocmodels = ZenIntellesis.ObjectClassification.ListAvailableModels()

for obcmodel in ocmodels:
    print 'TOC Model Name:', obcmodel.Name, 'Description:', obcmodel.Description, 'Status:', obcmodel.Status
    training_images = obcmodel.TrainingImages
    print'\tTraining Images:'
    print'\t----------------------'
    for ti in training_images:
        print '\t' + ti

# select a specific model
myobjmodel = find_objclassmodel('Worms test 1 - cloned')
print('Use model:', myobjmodel.Name)

# import a model
model2import = r"C:\Testdata_Zeiss\Atomic\Object_Classification\Worms test 1 - cloned.cztoc"

# classify an analyzed image (inplace)
myobjmodel.Classify(image, appendFeatures=False) # Where is append feature option

# define IA class of interest
IAclass_all = 'Statistics worms'
IAclass_single = 'worms'

# define the object class of interest
objclass = 'live'

# export the table from the analyzed and classified image

# table for ALL objects (statistics) from the Image Analysis
table_all = Zen.Analyzing.CreateRegionsTable(image, IAclass_all)
Zen.Application.Documents.Add(table_all)

# table for SINGLE objects (the ones classified by the model) from the Image Analysis
table_single = Zen.Analyzing.CreateRegionTable(image, IAclass_single)

# extract a specific object class for from tbale by filtering
table_single.RemoveRows(lambda row: row[myobjmodel.Name] != objclass) # removes in place
