# Converts the input macro (*.czmac) file from python2 to python3 syntax.
#
# Parameters:
# -i or --input-file-path       Path to the file that needs to be converted
# -o or --output-file-path      Path to where the converted file needs to be stored (can be the same as input file path)
#
# Exit codes:
# *  0  Success
# * -1  Error: This is not a valid macro file
# * -2  Error: Failed to convert the python syntax
#
# Note: For this script to work you will need to install python "2to3" tool (e.g., "pip install 2to3").
#
# Example where the macro is converted to a new file:
# python ZeissMacroConverter.py -i "Macro_Python2.czmac" -o "Macro_Python3.czmac"
#
# Example where the macro is converted to the same file:
# python ZeissMacroConverter.py -i "Macro.czmac" -o "Macro.czmac"


import argparse
import codecs
import os
import subprocess
import re
from xml.etree import ElementTree


def convert_macro(input_file_path: str, output_file_path: str):
    print(f'Location of the macro file to convert: {input_file_path}')
    print(f'Location of the converted macro file: {output_file_path}')

    # Parse the input macro file
    macro_file_xml_document = ElementTree.parse(input_file_path)
    root_element = macro_file_xml_document.getroot()

    # Check if this file really contains a python2 script
    try:
        language_element = root_element.find('Language')

        if (language_element.text is not None and
                language_element.text != '' and
                not language_element.text.isspace() and
                language_element.text != 'Python'):
            print('Skipping macro: only python2 macro files need to be converted')
            return 0

        # Get the 'Text' element which contains the python script
        text_element = root_element.find('Text')
        python_script_contents = text_element.text
    except Exception as e:
        print('Error: This is not a valid macro file.')
        print('Details:')
        print(e)
        return -1

    # Prepare file path for the temporary python script file (needed for the python "2to3" tool)
    temp_python_script_file_path = output_file_path + '.py'

    try:
        # Store the python script to a temp file next to the output so that it can be converted
        print(f'Creating temporary python script file at [{temp_python_script_file_path}]...')

        with codecs.open(temp_python_script_file_path, 'w', 'utf-8') as python_script_file:
            python_script_file.write(python_script_contents)

        # Convert the python script from python2 to python3 syntax
        print('Converting temporary python script...')
        subprocess.call(
            args=['2to3', '-w', '-n', temp_python_script_file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

        # Read the python file contents
        print('Loading converted python script content...')
        with codecs.open(temp_python_script_file_path, 'r', 'utf-8') as python_script_file:
            python_script_file_contents = python_script_file.read().replace('\r\n', '\n')

        # Convert the use of "SomeObject.None" to "SomeObject['None']"
        pattern = r"(?<=[\s,=\.])(\w+)\.None"
        replacement = r"\1['None']"
        python_script_file_contents = re.sub(pattern, replacement, python_script_file_contents)

        # Store the python file contents back to the text element
        text_element.text = python_script_file_contents

        # Update the Language element to Python3
        language_element.text = 'Python3'

        # Store the converted macro to the output file
        print('Saving converted macro file...')

        with codecs.open(output_file_path, 'w', 'utf-8-sig') as output_file:
            output_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            output_file.write(ElementTree.tostring(
                element=root_element,
                encoding='unicode',
                short_empty_elements=False))
    except Exception as e:
        print('Error: Failed to convert the python syntax')
        print('Details:')
        print(str(e))
        return -2
    finally:
        # Delete the temporary python file
        if os.path.exists(temp_python_script_file_path):
            print('Deleting temporary python script file...')
            os.remove(temp_python_script_file_path)

    print('Successfully converted macro file')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file-path')
    parser.add_argument('-o', '--output-file-path')
    args = parser.parse_args()

    exit_code = convert_macro(args.input_file_path, args.output_file_path)
    exit(exit_code)


