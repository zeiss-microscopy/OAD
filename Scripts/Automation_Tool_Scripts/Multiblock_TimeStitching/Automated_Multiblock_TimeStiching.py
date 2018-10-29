#
# Generated automatically a timestitching for MultiBlock acquisition (ie: Experiment Designer)

# get the active image document
image= Zen.Application.Documents.ActiveDocument

if image.IsZenMultiBlockImage:
    # get number of blocks
    block_count= image.AcquisitionBlockCount
    
    # loop over blocks and stitch
    for i in range (0, block_count):
        timestitching = Zen.Processing.Utilities.MultiBlockTimeStitching(image, image.SelectBlockIndices(i))
        Zen.Application.Documents.Add(timestitching)

print('Done.')
