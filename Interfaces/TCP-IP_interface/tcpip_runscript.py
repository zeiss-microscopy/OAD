#################################################################
# File       : tcpip_runscript.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import tcpoad as tcp

timeout = 100
zentcpip = tcp.tcp_open_port(timeout=timeout)

runpy = True
runczmac = False

if runpy:
    # specify python script (*.py) containg the OAD commands
    inputfile = r'c:\Python_Projects\ZEN_TCPIP\oad.py'
    oadcommandlist = tcp.create_oadlist_frompy(inputfile, extension='.py')

if runczmac:
    # define OAD macro
    inputfile = r'c:\Python_Projects\ZEN_TCPIP\oad.czmac'
    # convert it to text
    oadpyscript = tcp.read_macro(inputfile)
    # creat a list of tuples out of that
    oadcommandlist = tcp.create_oadlist_fromczmac(oadpyscript)

# iterate over list and send the OAD macro line-by-line
for oadcommand in oadcommandlist:
    # print the current command
    print(oadcommand)
    # and execute
    rt, an = tcp.tcp_eval_expression_and_wait_for_ok(zentcpip, oadcommand, timeout)

# finish and close connection
zentcpip.close()
