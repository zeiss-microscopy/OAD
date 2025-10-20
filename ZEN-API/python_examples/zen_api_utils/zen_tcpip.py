# -*- coding: utf-8 -*-

#################################################################
# File        : zen_tcpip.py
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

import os
import telnetlib
import time
from typing import Tuple, Union, List
from zen_api_utils.misc import set_logging


# create logger
logger = set_logging()


class ZenCommands:
    """
    Represents a collection of commands to be executed on a ZEN device using TCP-IP connection.

    Args:
        commandlist (List[str]): A list of commands to be executed.
        timeout (int, optional): The timeout value for the TCP-IP connection. Defaults to 200.
        port (int, optional): The port number for the TCP-IP connection. Defaults to 52757.
        verbose (bool, optional): Whether to print the executed commands. Defaults to True.
    """

    def __init__(
        self,
        commandlist: List[str],
        timeout: int = 200,
        port: int = 52757,
        verbose=True,
    ):
        """
        Initializes a new instance of the ZenCommands class.

        Args:
            commandlist (List[str]): A list of commands to be executed.
            timeout (int, optional): The timeout value for the TCP-IP connection. Defaults to 200.
            port (int, optional): The port number for the TCP-IP connection. Defaults to 52757.
            verbose (bool, optional): Whether to print the executed commands. Defaults to True.
        """

        # set the defaults
        self.commands = commandlist
        self.timeout = timeout
        self.port = port
        self.verbose = verbose

    def execute(self):
        """
        Executes the commands on the ZEN device using TCP-IP connection.
        """

        # open the TCP-IP connection to ZEN
        zentcp = ZenTCPIP()
        zentcp_connection = zentcp.tcp_open_port(timeout=self.timeout, port=self.port)

        # iterate over list and send the OAD macro line-by-line
        for command in self.commands:
            # print the current command and execute it

            if self.verbose:
                logger.info(f"TCP-IP: {command}")

            rt, an = zentcp.tcp_eval_expression_and_wait_for_ok(zentcp_connection, command, self.timeout)

        # finish and close TCP-IP connection to ZEN
        zentcp_connection.close()


class ZenTCPIP:
    def __init__(self):
        """Initialize the object to connect with ZEN over the
        TCP-IP port.
        """
        pass

    def tcp_open_port(self, timeout: int = 200, port: int = 52767, verbose=False) -> Union[telnetlib.Telnet, int]:
        """Open a connection to ZEN with a specified timeout and port number

        :param timeout: time in [s] the longest command is expected to take.
        When finishing earlier the next command will be send., defaults to 200
        :type timeout: int, optional
        :param port: port number used for the connection, defaults to 52767
        :type port: int, optional
        :param verbose: option to show or suppress additional output
        :type verbose: bool, optional
        :return: telnet connection
        :rtype: telnetlib.Telnet
        """

        telnet = 0
        success = False

        for i in range(timeout):
            try:
                telnet = telnetlib.Telnet("localhost", port)
                success = True
                if verbose:
                    logger.info(f"Opened Port: {port}")
                break
            except Exception as e:
                # print("type error: " + str(e)):
                logger.error(f"tcp_open_port: Unexpected error: {e}")

            # wait for a moment
            time.sleep(1)

        assert success is True

        line = telnet.read_until(os.linesep.encode("ascii"), 1)

        # show output to check if it is really working
        if verbose:
            logger.info("Received line: ", line.decode("utf-8"))

        if line == b"Welcome to ZEN PythonScript\r\n":
            return telnet
        else:
            return 0

    def tcp_eval_expression_and_wait_for_ok(
        self, telnet: telnetlib.Telnet, expression: str, timeout: float, verbose=False
    ) -> Tuple[str, str]:
        """Evaluate the given python expression within ZEN and expect
        an "OK" answer within given timeout (in seconds).
        Return True if "OK" was received within given timeout

        :param telnet: Telnet object
        :type telnet: telnetlib.Telnet
        :param expression: ZEN OAD command to be sent
        :type expression: string
        :param timeout: time in [s] the longest command is expected to take.
        When finishing earlier the next command will be send., defaults to 200
        :type timeout: int, optional
        :param verbose: option to show or suppress additional output
        :type verbose: bool, optional
        :return: answer
        :rtype: str
        """

        # execute the expression
        self.tcp_eval_expression(telnet, expression)

        # get the answer
        answer = self.tcp_read_answer(telnet, float(timeout))
        if verbose:
            logger.info(f"got {0}".format(answer))

        # empty the buffer
        self.tcp_read_all(telnet)

        return answer == "Ok", answer

    def tcp_eval_expression(self, telnet: telnetlib.Telnet, expression: str) -> None:
        """Evaluate the given python expression within ZEN

        :param telnet: [description]
        :type telnet: telnetlib.Telnet
        :param expression: ZEN OAD command to be sent
        :type expression: string
        """

        telnet.write(("EVAL " + expression).encode("ascii"))

    def tcp_read_answer(self, telnet: telnetlib.Telnet, timeout: float = 0.1) -> str:
        """Read the answer after sending an OAD command.

        :param telnet: Telnet object
        :type telnet: telnetlib.Telnet
        :param timeout: time in [s] waiting for an answer
        :type timeout: int, optional
        """

        # Read one line and remove line breaks
        line = telnet.read_until(os.linesep.encode("ascii"), float(timeout))
        answer = line.decode("utf-8")[0:-2]

        return answer

    def tcp_read_all(self, telnet: telnetlib.Telnet) -> None:
        """Read everything from the buffer.

        :param telnet: Telnet object
        :type telnet: telnetlib.Telnet
        """

        while True:
            line = telnet.read_until(os.linesep.encode("ascii"), 0.5)
            if line == b"":
                # read one more time to be sure
                line = telnet.read_until(os.linesep.encode("ascii"), 0.5)
                break
