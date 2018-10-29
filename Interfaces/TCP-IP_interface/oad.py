exp = Zen.Acquisition.Experiments.GetByName("ML_96_Wellplate_Castor.czexp")
img = Zen.Acquisition.Execute(exp)
Zen.Application.Documents.Add(img)
