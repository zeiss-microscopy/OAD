from apeer_dev_kit import adk
import segment_objects
import numpy as np
import os


if __name__ == "__main__":
    inputs = adk.get_inputs()

    # run the processing script
    outputs = segment_objects.execute(inputs['overview_image'],
                                      separator=';',
                                      filter_method=inputs['filter_method'],
                                      filter_size=int(inputs['filter_size']),
                                      threshold_method=inputs['threshold_method'],
                                      min_objectsize=int(inputs['min_objectsize']),
                                      min_holesize=int(inputs['min_holesize']),
                                      saveformat='ome.tiff'
                                      )

    # write the results to the outputs
    adk.set_file_output('segmented_image', outputs['segmented_image'])
    adk.set_file_output('objects_table', outputs['objects_table'])

    # finalize module
    adk.finalize()
    os._exit(0)
