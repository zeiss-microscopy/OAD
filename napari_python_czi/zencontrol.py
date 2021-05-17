# -*- coding: utf-8 -*-

#################################################################
# File        : zentcontrol.py
# Version     : 0.4
# Author      : czsrh
# Date        : 23.01.2020
# Institution : Carl Zeiss Microscopy GmbH
#
# Disclaimer: This tool is purely experimental. Feel free to
# use it at your own risk.
#
# Copyright(c) 2020 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import os
import sys
import pathlib
import telnetlib
import time


class ZenExperiment():
    def __init__(self, experiment='test.czexp',
                 savefolder=r'c:\zen_output',
                 cziname='myimage.czi'):
        """Initialize a ZenExperiment object with default values to be used via
        the TCP-IP connection between Python and ZEN.

        :param experiment: name of the experiment, defaults to 'test.czexp'
        :type experiment: str, optional
        :param savefolder: folder to save the resulting CZI image, defaults to r'c:\zen_output'
        :type savefolder: regexp, optional
        :param cziname: name of the CZI to be saved, defaults to 'myimage.czi'
        :type cziname: str, optional
        """

        # set the defaults
        self.experiment = experiment
        self.savefolder = savefolder
        self.cziname = cziname

    def startexperiment(self, timeout=200, port=52757):
        """ Start the actual ZEN experiment. It will open a TCP-IP
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
        czifiles_long, czifiles_short = czidocs.getfilenames(folder=self.savefolder,
                                                             pattern='*.czi')

        # in case the czi does already exist do nothing
        if self.cziname in czifiles_short:
            print('CZI already exits. Choose a different name.')
            return None

        # in case the czi does not already exist
        if self.cziname not in czifiles_short:

            # define the lists of commands to be send
            commandlist = ['from System.IO import File, Directory, Path',
                           'outputfolder = r"' + self.savefolder + '"',
                           'exp = Zen.Acquisition.Experiments.GetByName(r"' + self.experiment + '")',
                           'exp.SetActive()',
                           'img = Zen.Acquisition.Execute(exp)',
                           'img.Save(Path.Combine(outputfolder, "' + self.cziname + '"))',
                           'img.Close()'
                           ]

            # open the TCP-IP connection to ZEN
            zentcp = ZenTCPIP()
            zentcp_connection = zentcp.tcp_open_port(timeout=timeout, port=port)

            # iterate over list and send the OAD macro line-by-line
            for command in commandlist:
                # print the current command and execute it
                print(command)
                rt, an = zentcp.tcp_eval_expression_and_wait_for_ok(zentcp_connection, command, timeout)

            # finish and close TCP-IP connection to ZEN
            zentcp_connection.close()

            czifilepath = os.path.join(self.savefolder, self.cziname)

            return czifilepath


class ZenDocuments():
    def __init__(self):
        pass

    def getfilenames(self, folder=r'c:\temp',
                     pattern="*.czexp"):
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


class ZenTCPIP():
    def __init__(self):
        """Initialize the object to connect with ZEN over the
        TCP-IP port.
        """
        pass

    def tcp_open_port(self, timeout=200, port=52767):
        """Open a connection to ZEN with a specified timeout and port number

        :param timeout: time in [s] the longest command is expected to take.
        When finishing earlier the next command will be send., defaults to 200
        :type timeout: int, optional
        :param port: port number used for the connection, defaults to 52767
        :type port: int, optional
        :return: telnet connection
        :rtype: telnetlib.Telnet
        """

        telnet = 0
        success = False

        for i in range(timeout):
            try:
                telnet = telnetlib.Telnet("localhost", port)
                success = True
                print('Opened Port: ', port)
                break
            except Exception as e:
                # print("type error: " + str(e)):
                print("tcp_open_port: Unexpected error:", e)

            # wait for a moment
            time.sleep(1)

        assert success is True

        line = telnet.read_until(os.linesep.encode('ascii'), 1)
        # show output to check if it is really working
        print('Received line: ', line.decode('utf-8'))

        if line == b'Welcome to ZEN PythonScript\r\n':
            return telnet
        else:
            return 0

    def tcp_eval_expression_and_wait_for_ok(self, telnet, expression, timeout):
        """ Evaluate the given python expression within ZEN and expect
        an "OK" answer within given timeout (in seconds).
        Return True if "OK" was received within given timeout

        :param telnet: Telnet object
        :type telnet: telnetlib.Telnet
        :param expression: ZEN OAD command to be sent
        :type expression: string
        :param timeout: time in [s] the longest command is expected to take.
        When finishing earlier the next command will be send., defaults to 200
        :type timeout: int, optional
        :return: answer
        :rtype: str
        """

        # execute the expression
        self.tcp_eval_expression(telnet, expression)

        # get the answer
        answer = self.tcp_read_answer(telnet, float(timeout))
        print("got {0}".format(answer))

        # empty the buffer
        self.tcp_read_all(telnet)

        return answer == "Ok", answer

    def tcp_eval_expression(self, telnet, expression):
        """Evaluate the given python expression within ZEN

        :param telnet: [description]
        :type telnet: telnetlib.Telnet
        :param expression: ZEN OAD command to be sent
        :type expression: string
        """

        telnet.write(("EVAL " + expression).encode('ascii'))

    def tcp_read_answer(self, telnet, timeout=0.1):
        """Read the answer after sending an OAD command.

        :param telnet: Telnet object
        :type telnet: telnetlib.Telnet
        :param timeout: time in [s] waiting for an answer
        :type timeout: int, optional
        """

        # Read one line and remove line breaks
        line = telnet.read_until(os.linesep.encode('ascii'), float(timeout))
        answer = line.decode('utf-8')[0:-2]

        return answer

    def tcp_read_all(self, telnet):
        """Read everything from the buffer.

        :param telnet: Telnet object
        :type telnet: telnetlib.Telnet
        """

        while True:
            line = telnet.read_until(os.linesep.encode('ascii'), 0.5)
            if line == b'':
                # read one more time to be sure
                line = telnet.read_until(os.linesep.encode('ascii'), 0.5)
                break
