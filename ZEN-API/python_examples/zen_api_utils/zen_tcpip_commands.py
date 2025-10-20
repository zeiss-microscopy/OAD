# -*- coding: utf-8 -*-

#################################################################
# File        : zen_tcpip_commands.py
# Author      : czsrh
# Institution : Carl Zeiss Microscopy GmbH
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk.
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################


from typing import List
from zen_api_utils.misc import set_logging
from zen_api_utils.zen_tcpip import ZenCommands

# create logger
logger = set_logging()


def add_image(czi_path: str) -> List[str]:
    """
    Adds an image to the Zen application.

    Args:
        czi_path (str): The path to the CZI file.

    Returns:
        list: A list of commands to be sent.

    """
    # define the lists of commands to be send
    commandlist = [
        'img = Zen.Application.LoadImage(r"' + czi_path + '", False)',
        "Zen.Application.Documents.Add(img)",
    ]

    return commandlist


def set_experiment_active(experiment_name: str) -> List[str]:
    """
    Sets the specified experiment as active.

    Args:
        experiment_name (str): The name of the experiment to set as active.

    Returns:
        List[str]: A list of commands to be sent.

    """
    # define the lists of commands to be sent
    commandlist = [
        'myexp = Zen.Acquisition.Experiments.GetByName("' + experiment_name + '")',
        "myexp.SetActive()",
    ]

    return commandlist


def run_experiment_and_save_image(experiment_name: str, savefolder: str, cziname: str) -> List[str]:
    """
    Runs an experiment and saves the resulting image.

    Args:
        experiment_name (str): The name of the experiment to run.
        savefolder (str): The folder path where the image will be saved.
        cziname (str): The name of the image file.

    Returns:
        list: A list of commands to be sent.

    """
    # define the lists of commands to be send
    commandlist = [
        "from System.IO import File, Directory, Path",
        'outputfolder = r"' + savefolder + '"',
        'exp = Zen.Acquisition.Experiments.GetByName(r"' + experiment_name + '")',
        "exp.SetActive()",
        "img = Zen.Acquisition.Execute(exp)",
        'img.Save(Path.Combine(outputfolder, "' + cziname + '"))',
        "img.Close()",
    ]

    return commandlist


# Test Code locally
if __name__ == "__main__":

    czi_path = r"F:\AzureDevOps\RMS_Users\Playground\ZEN_API\data\OverViewScan.czi"

    commandlist = add_image(czi_path)
    my_commands = ZenCommands(commandlist, timeout=200, port=52757)
    my_commands.execute()
