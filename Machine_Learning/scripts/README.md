# Intellesis - Scripts

## ZEN_Intellesis_Simple_Test.py

The [script](../scripts/ZEN_Intellesis_Simple_Test.py) demonstrates the different possibilities to segment an image using a trained model. The result of such a segmentation is a mask image, which has either as many channels as the models has classes, or one channel containing a distinct label for every class.

![ZEN Intellesis Segmentation Options](../../Images/intellesis_segoptions.png "ZEN Intellesis Segmentation Options")

- (top left) - raw image data data
- (top right) segmented image
- (bottom left) segmented with confidence threshold
- (bottom right) probability map image

---

## Intellesis_Segmentation_Tool.py

<!--
![ZEN Intellesis Segmentation Tool](../../Images/intellesis_batch.png)_ZEN Intellesis Segmentation Tool_
-->

<p><img src="../../Images/intellesis_batch.png" title="Intellesis Segmentation Tool" width="400"></p>

The [Intellesis Segmentation Tool](../scripts/Intellesis_Segmentation_Tool.py) allows you to automate and simplify the following tasks:

- Select a model to segment images
- Specify the desired output format for the mask image
- Optional Confidence Threshold that can be applied to mask image
- Optional Extraction of a specific single class
- Option to add the mask image to the original image
- Selection of output folder with file extension filter
- Option to segment all image inside a folder or only apply to active image

Beside this tool is is also possible to run a segmentation using the ZEN built-in batch tool, which does not require this script but offers less additional options.

---

## Intellesis_Segmentation_Tool_singleCH.py

The [Intellesis Segmentation Tool Single Channel](../scripts/Intellesis_Segmentation_Tool_singleCH.py) allows you to automate and simplify the following tasks:

- It uses the current active image as an input
- Specify the channel to be segmented and the model to be uses in step 1
- Specify the desired class (for the selected model) and other option in step 2
- Apply segmentation to the selected channel
- Optionally add the mask to the original multi-channel image

Beside this tool is is also possible to run a segmentation using the ZEN built-in batch tool, which does not require this script but offers less additional options.

<!--
![ZEN Intellesis Segmentation Tool - Single Channel](../../Images/intellesis_batch_singleCH1.png)_Intellesis Segmentation Tool Single Channel - Step 1_
-->

<p><img src="../../Images/intellesis_batch_singleCH1.png" title="Intellesis Segmentation Tool Single Channel - Step 1" width="500"></p>

<!--
![ZEN Intellesis Segmentation Tool - Single Channel](../../Images/intellesis_batch_singleCH2.png)_Intellesis Segmentation Tool Single Channel - Step 2_
-->

<p><img src="../../Images/intellesis_batch_singleCH2.png" title="Intellesis Segmentation Tool Single Channel - Step 2" width="500"></p>

<!--
![ZEN Intellesis Segmentation Tool - Single Channel](../../Images/intellesis_batch_singleCH_result.png)_Segmented green channel (bottom left)_
-->

<p><img src="../../Images/intellesis_batch_singleCH_result.png" title="Segmented green channel (bottom left)" width="500"></p>

## ZenIntellesis_API.py

The [script](../scripts/ZenIntellesis.py) demonstrates some additional function to manage model files.

```python
def find_model(name):
    """ Finds a model given its Name.

    Arguments:
        name: string
            The name of the model to look for.

    Returns: IZenIntellesisModel
        The first model with the specified name
        or None, if no such model exists.
    """
    models = ZenIntellesis.ListAvailableSegmentationModels()
    return next((m for m in models if m.Name == name), None)

modelname = 'Grains_MET101'

# find the model by name
model = find_model(modelname)

print 'Modelname : ', model.Name
print 'Model Status : ', model.Status
print model.

training_images = model.TrainingImages
for ti in training_images:
    print ti


# show all feature extractors.
all_feature_sets = ZenIntellesis.GetAvailableFeatureSets()
for fs in  all_feature_sets:
    print fs

# show all postprocessings
all_postprocessings = ZenIntellesis.GetAvailablePostProcessings()
for ps in all_postprocessings:
    print ps
```

## Intellesis_CompareTwoFeatureExtractors_UI.py

This [script](Intellesis_CompareTwoFeatureExtractors_UI.py) can be used to compare two feature extractors for a trained model.

- Select the image the model should be applied to
- Select the feature extractors and post-processings to be compared
- Optional: Define a substring in order to do the compare

<p><img src="../../Images/intellesis_compare_features.png" title="Intelleis Model Compare Tool" width="500"></p>

<p><img src="../../Images/intellesis_compare_features_result.png" title="MutiView - Compare two results" width="700"></p>
