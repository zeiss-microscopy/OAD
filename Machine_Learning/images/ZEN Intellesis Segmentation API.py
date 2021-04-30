def runmodel(image, model,
             use_confidence=False,
             confidence_threshold=0,
             format='MultiChannel',
             extractclass=False,
             class2extract_id=0,
             addseg=False,
             adapt_pixeltype=True):

	# define the desired output format
    if format == 'MultiChannel':
      	# output image will have one channel per model class
        segf = ZenSegmentationFormat.MultiChannel
    if format == 'Labels':
      	# output image will have one channel with distinct labels per model class
        segf = ZenSegmentationFormat.Labels

    # classify pixels using a trained model incl import deep-learning models
    if use_confidence:
        try:
            # run the segmentation and apply confidence threshold to segmented image
            outputs = Zen.Processing.Segmentation.TrainableSegmentationWithProbabilityMap(image, model, segf)
            seg_image = outputs[0]
            conf_map = outputs[1]
            print('Apply Confidence Threshold to segmented image.')
            seg_image = Zen.Processing.Segmentation.MinimumConfidence(seg_image, conf_map, confidence_threshold)
            conf_map.Close()
            del outputs
        except ApplicationException as e:
            seg_image = None
            print('Application Exception : ', e.Message)

    if not use_confidence:
        try:
            # run just the segmentation
            seg_image = Zen.Processing.Segmentation.TrainableSegmentation(image, model, segf)
        except ApplicationException as e:
            seg_image = None
            print('Application Exception : ', e.Message)

    return seg_image