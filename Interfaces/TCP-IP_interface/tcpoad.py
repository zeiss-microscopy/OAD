#################################################################
# File       : tcpoad.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import os
import telnetlib
import time
import sys
from xml.etree.cElementTree import Element, ElementTree


def tcp_open_port(timeout=60, port=52757):

    # Opens tcp connection to ZEN blue via port 52757 with given timeout (in seconds).
    # Return a telnet connection

    telnet = 0
    success = False

    for i in range(timeout):
        try:
            telnet = telnetlib.Telnet("localhost", port)
            success = True
            print('Opened Port: ', port)
            break
        except:
            print("tcp_open_port: Unexpected error:", sys.exc_info()[0])

        # wait for a moment
        time.sleep(1)

    assert success is True

    line = telnet.read_until(os.linesep.encode('ascii'), 1)
    # show output to check if it is really working
    print('Recieved line: ', line.decode('utf-8'))

    if line == b'Welcome to ZEN PythonScript\r\n':
        return telnet
    else:
        return 0


def tcp_eval_expression(telnet, expression):

    # Evaluate the given python expression within ZEN
    telnet.write(("EVAL " + expression).encode('ascii'))


def tcp_eval_expression_and_wait_for_ok(telnet, expression, timeout):

    # Evaluate the given python expression within ZEN and expect an "OK" answer within given timeout (in seconds)
    # Return True if "OK" was received within given timeout

    tcp_eval_expression(telnet, expression)

    answer = tcp_read_answer(telnet, float(timeout))
    print("got {0}".format(answer))

    # empty the buffer
    tcp_read_all(telnet)

    return answer == "Ok", answer


def tcp_read_all(telnet):

    while True:
        line = telnet.read_until(os.linesep.encode('ascii'), 0.5)
        #print("tcp_read_all: '{0}'".format(line))
        if line == b'':
            # read one more time to be sure
            line = telnet.read_until(os.linesep.encode('ascii'), 0.5)
            #print("tcp_read_all: '{0}'".format(line))
            break


def tcp_read_answer(telnet, timeout=0.1):

    # Read one line and remove line breaks
    line = telnet.read_until(os.linesep.encode('ascii'), float(timeout))
    #print("tcp_read_answer: '{0}' in {1}".format(line, float(timeout)))

    return line.decode('utf-8')[0:-2]


def tcp_clear_all(telnet):
    while True:
        line = telnet.read_until(os.linesep.encode('ascii'), 1)
        if line == b'':
            # read one more time to be sure
            line = telnet.read_until(os.linesep.encode('ascii'), 1)
            break


def create_czmac_from_pythonfile(macro_filename, python_filename):
    """   
    Create a czmac file out of the given python file.
    Write the macro into the given 'macroname' file.
    """

    # Read python content from given file
    with open(python_filename, 'rt') as python:
        python_content = python.read()

    # Create czmac xml structure
    script_node = Element("Script")
    script_node.set("Version", "1.0")

    language_node = Element("Language")
    language_node.text = "Python"
    script_node.append(language_node)

    text_node = Element("Text")
    text_node.text = python_content
    script_node.append(text_node)

    doc = ElementTree(script_node)

    # write czmac to given filename
    doc.write(macro_filename)


def create_czmac(macro_filename, macro_lines):

    # write a czmac file with the given OAD macro lines

    # Prepare python content
    python_content = ""
    for line in macro_lines:
        python_content += line + "\n"

    # Create czmac xml structure
    script_node = Element("Script")
    script_node.set("Version", "1.0")

    language_node = Element("Language")
    language_node.text = "Python"
    script_node.append(language_node)

    text_node = Element("Text")
    text_node.text = python_content
    script_node.append(text_node)

    doc = ElementTree(script_node)

    # write czmac to given filename
    doc.write(macro_filename)


def create_oadlist_frompy(inputfile, extension='.py'):

    # open file
    inputfile = open(inputfile, 'r')
    # create empty list
    myListofTuples = list()
    # read file line-by-line
    for line in inputfile.readlines():
        myListofTuples.append(line)

    return myListofTuples


def create_oadlist_fromczmac(pytext):

    # create empty list
    myListofTuples = list()
    # read file line-by-line
    myListofTuples = pytext.split('\n')

    return myListofTuples


def read_macro(filename):
    # Extract the OAD script code from ZEN macro file: *.czmac

    print('Reading OAD Macro: ', filename)
    tree = ElementTree(file=filename)
    pyscript = tree.find('Text').text

    return pyscript
