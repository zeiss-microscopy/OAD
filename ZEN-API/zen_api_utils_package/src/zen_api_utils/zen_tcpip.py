#################################################################
# File        : zen_tcpip.py
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

import socket
import time

from zen_api_utils.misc import set_logging

# create logger
logger = set_logging()


class ZenTCPConnection:
    """Buffered line-oriented TCP connection used by ZEN's PythonScript interface."""

    def __init__(self, connection: socket.socket):
        self._connection = connection
        self._buffer = bytearray()

    def write(self, data: bytes) -> None:
        self._connection.sendall(data)

    def read_until(self, expected: bytes, timeout: float | None = None) -> bytes:
        if not expected:
            raise ValueError("expected delimiter must not be empty")

        deadline = time.monotonic() + timeout if timeout is not None else None
        while True:
            delimiter_index = self._buffer.find(expected)
            if delimiter_index >= 0:
                end_index = delimiter_index + len(expected)
                result = bytes(self._buffer[:end_index])
                del self._buffer[:end_index]
                return result

            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return self._take_buffer()
                self._connection.settimeout(remaining)
            else:
                self._connection.settimeout(None)

            try:
                data = self._connection.recv(4096)
            except TimeoutError:
                return self._take_buffer()

            if not data:
                return self._take_buffer()
            self._buffer.extend(data)

    def _take_buffer(self) -> bytes:
        result = bytes(self._buffer)
        self._buffer.clear()
        return result

    def close(self) -> None:
        self._connection.close()


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
        commandlist: list[str],
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
        try:
            for command in self.commands:
                if self.verbose:
                    logger.info(f"TCP-IP: {command}")

                zentcp.tcp_eval_expression_and_wait_for_ok(zentcp_connection, command, self.timeout)
        finally:
            zentcp_connection.close()


class ZenTCPIP:
    def __init__(self):
        """Initialize the object to connect with ZEN over the
        TCP-IP port.
        """
        pass

    def tcp_open_port(self, timeout: int = 200, port: int = 52767, verbose=False) -> ZenTCPConnection:
        """Open a connection to ZEN with a specified timeout and port number

        :param timeout: time in [s] the longest command is expected to take.
        When finishing earlier the next command will be send., defaults to 200
        :type timeout: int, optional
        :param port: port number used for the connection, defaults to 52767
        :type port: int, optional
        :param verbose: option to show or suppress additional output
        :type verbose: bool, optional
        :return: TCP connection
        :rtype: ZenTCPConnection
        """

        deadline = time.monotonic() + timeout
        connection: ZenTCPConnection | None = None
        last_error: OSError | None = None
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            try:
                socket_connection = socket.create_connection(("localhost", port), timeout=min(remaining, 1.0))
                connection = ZenTCPConnection(socket_connection)
                if verbose:
                    logger.info(f"Opened Port: {port}")
                break
            except OSError as error:
                last_error = error
                logger.debug(f"tcp_open_port: Connection attempt failed: {error}")
                time.sleep(min(1.0, max(0.0, deadline - time.monotonic())))

        if connection is None:
            raise ConnectionError(f"Could not connect to ZEN on port {port}") from last_error

        line = connection.read_until(b"\n", 1)

        # show output to check if it is really working
        if verbose:
            logger.info(f"Received line: {line.decode('utf-8')}")

        if line.rstrip(b"\r\n") == b"Welcome to ZEN PythonScript":
            return connection

        connection.close()
        raise ConnectionError("ZEN returned an unexpected TCP/IP greeting")

    def tcp_eval_expression_and_wait_for_ok(
        self, telnet: ZenTCPConnection, expression: str, timeout: float, verbose=False
    ) -> tuple[bool, str]:
        """Evaluate the given python expression within ZEN and expect
        an "OK" answer within given timeout (in seconds).
        Return True if "OK" was received within given timeout

        :param telnet: ZEN TCP connection
        :type telnet: ZenTCPConnection
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
            logger.info(f"got {answer}")

        # empty the buffer
        self.tcp_read_all(telnet)

        return answer == "Ok", answer

    def tcp_eval_expression(self, telnet: ZenTCPConnection, expression: str) -> None:
        """Evaluate the given python expression within ZEN

        :param telnet: ZEN TCP connection
        :type telnet: ZenTCPConnection
        :param expression: ZEN OAD command to be sent
        :type expression: string
        """

        telnet.write(("EVAL " + expression).encode("ascii"))

    def tcp_read_answer(self, telnet: ZenTCPConnection, timeout: float = 0.1) -> str:
        """Read the answer after sending an OAD command.

        :param telnet: ZEN TCP connection
        :type telnet: ZenTCPConnection
        :param timeout: time in [s] waiting for an answer
        :type timeout: int, optional
        """

        # Read one line and remove line breaks
        line = telnet.read_until(b"\n", float(timeout))
        answer = line.decode("utf-8").rstrip("\r\n")

        return answer

    def tcp_read_all(self, telnet: ZenTCPConnection) -> None:
        """Read everything from the buffer.

        :param telnet: ZEN TCP connection
        :type telnet: ZenTCPConnection
        """

        while True:
            line = telnet.read_until(b"\n", 0.5)
            if line == b"":
                # read one more time to be sure
                line = telnet.read_until(b"\n", 0.5)
                break
