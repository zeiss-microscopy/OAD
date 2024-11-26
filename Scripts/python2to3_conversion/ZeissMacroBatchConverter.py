# Searches for all macro (*.czmac) files at the root directory and converts them from python2 to python3 syntax.
#
# Parameters:
# Path to the root directory that contains macro files
#
# Exit codes:
# *  0  Success
# * -1  Error: the path does not exist
#
# Note: For this script to work you will need to install python "2to3" tool (e.g., "pip install 2to3") and you will need
# the ZeissMacroConverter.py script.
#
# Example:
# python ZeissMacroBatchConverter.py "C:\OAD_Macros"


import argparse
import os
import ZeissMacroConverter


def convert_macros(path: str):
    if not os.path.exists(path):
        print(f"Error: the path [{path}] does not exist")
        return -1

    # Search for all macro files in the path
    for root, dirs, files in os.walk(path):
        # Convert all macro files in the current directory
        for file_name in files:
            # Check if this file is a macro file
            base_name, file_extension = os.path.splitext(file_name)
            print(f"Processing file: {file_name}")
            if file_extension.lower() != ".czmac":
                continue

            # Convert the macro file
            file_path = os.path.join(root, file_name)
            result = ZeissMacroConverter.convert_macro(
                input_file_path=file_path, output_file_path=file_path
            )

            if result != 0:
                return result

    print("Successfully converted all macro files")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    exit_code = convert_macros(args.path)
    exit(exit_code)
