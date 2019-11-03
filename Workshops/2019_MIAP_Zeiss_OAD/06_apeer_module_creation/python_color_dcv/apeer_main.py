from apeer_dev_kit import adk
import color_dcv

if __name__ == "__main__":

    inputs = adk.get_inputs()
    outputs = color_dcv.run(inputs['ihc_image'])
    adk.set_file_output('processed_images', outputs['processed_images'])
    adk.finalize()
