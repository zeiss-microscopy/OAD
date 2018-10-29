# coding: utf-8

import tcpoad as tcp

timeout = 100
zentcpip = tcp.tcp_open_port(timeout=timeout)

runpy = True
runczmac = False

if runpy:
    # specify python script (*.py) containg the OAD commands
    inputfile = r'c:\Users\m1srh\OneDrive - Carl Zeiss AG\Python_Projects\ZEN_TCPIP\oad.py'
    oadcommandlist = tcp.create_oadlist_frompy(inputfile, extension='.py')

if runczmac:
    # define OAD macro
    inputfile = r'c:\Users\m1srh\OneDrive - Carl Zeiss AG\Python_Projects\ZEN_TCPIP\oad.czmac'
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
