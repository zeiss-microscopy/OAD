#################################################################
# File        : zentcontrol_short.py
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

import os
import pathlib

from zen_api_utils.zen_tcpip import ZenTCPIP


class ZenExperiment:
    def __init__(
        self,
        experiment: str = "test.czexp",
        savefolder: str = r"c:\zen_output",
        cziname: str = "myimage.czi",
    ):
        """Initialize a ZenExperiment object with default values to be used via
        the TCP-IP connection between Python and ZEN.

        :param experiment: name of the experiment, defaults to 'test.czexp'
        :type experiment: str, optional
        :param savefolder: folder to save the resulting CZI image, defaults to ``c:\\zen_output``
        :type savefolder: str, optional
        :param cziname: name of the CZI to be saved, defaults to 'myimage.czi'
        :type cziname: str, optional
        """

        # set the defaults
        self.experiment = experiment
        self.savefolder = savefolder
        self.cziname = cziname

    def startexperiment(self, timeout: int = 200, port: int = 52757) -> str | None:
        """Start the actual ZEN experiment. It will open a TCP-IP
        connection to ZEN and then send the list of commands

        :param timeout: [description], defaults to 200
        :type timeout: int, optional
        :param port: [description], defaults to 52757
        :type port: int, optional
        :return: full path of the saved CZI file
        :rtype: str
        """

        # get the list of existing CZI in the current folder
        czidocs = ZenDocuments()
        _, czifiles_short = czidocs.getfilenames(folder=self.savefolder, pattern="*.czi")

        # in case the czi does already exist do nothing
        if self.cziname in czifiles_short:
            print("CZI already exits inside:", self.savefolder, "Choose a different name.")
            return None

        # in case the czi does not already exist
        if self.cziname not in czifiles_short:

            # define the lists of commands to be send
            commandlist = [
                "from System.IO import File, Directory, Path",
                'outputfolder = r"' + self.savefolder + '"',
                'exp = Zen.Acquisition.Experiments.GetByName(r"' + self.experiment + '")',
                "exp.SetActive()",
                "img = Zen.Acquisition.Execute(exp)",
                'img.Save(Path.Combine(outputfolder, "' + self.cziname + '"))',
                "img.Close()",
            ]

            # open the TCP-IP connection to ZEN
            zentcp = ZenTCPIP()
            zentcp_connection = zentcp.tcp_open_port(timeout=timeout, port=port)

            # iterate over list and send the OAD macro line-by-line
            try:
                for command in commandlist:
                    print(command)
                    zentcp.tcp_eval_expression_and_wait_for_ok(zentcp_connection, command, timeout)
            finally:
                zentcp_connection.close()

            czifilepath = os.path.join(self.savefolder, self.cziname)

            return czifilepath


class ZenDocuments:
    def __init__(self):
        pass

    def getfilenames(self, folder: str = r"c:\temp", pattern: str = "*.czexp") -> tuple[list[str], list[str]]:
        """Get lists of all ZEN related files using a certain pattern.

        :param folder: file extension pattern, defaults to r"c:\temp"
        :type pattern: str, optional
        :param pattern: file extension pattern, defaults to "*.czexp"
        :type pattern: str, optional
        :return: list with full path and short names of files
        :rtype: list
        """

        # define the path and pattern
        directory = pathlib.Path(folder)

        # create empty lists for experiment names
        files_long = []
        files_short = []

        # fill the list
        for file in directory.glob(pattern):
            files_long.append(os.path.abspath(file))
            files_short.append(os.path.basename(file))

        return files_long, files_short
