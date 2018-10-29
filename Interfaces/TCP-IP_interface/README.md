# TCP/IP Interface

A modern digital light microscopy workstation with its software as provided by the
manufacturer is hardly able to fulfill every single customer requirement. There is a need to (i)
seamlessly integrate a software package into a given workflow, (ii) to combine software
packages. ZEN 2 offers an TCP/IP concept which allows the skilled programmer to integrate
the ZEN software in his workflow independent of operating system and software languages
or development packages. Thus the TCP/IP concept allows you combine ZEN functionality
with any software on any platform.

There are two general situations which are interesting for programmers.
First, programmers use the TCP/IP concept locally on one computer. As ZEN is running on
Windows the client program runs on the same computer and also uses the Windows
operating system. In this situation the TCP/IP concept is used primarily as an interface. The
TCP/IP interface is a good alternative to the COM interface that ZEN offers in addition.
Please keep in mind that the COM interface cannot be addressed from one .Net application
to another. This has been blocked by Microsoft for whatever reason. As ZEN blue is written
under .Net your application will fail to use the ZEN-COM interface in case your software is
written under .Net as well. The TCP/IP interface is better tested and a lot easier to use than
the COM interface.

The second interesting scenario is to drive ZEN from another computer which has an
arbitrary operating system and any programming language. In this case it is clear that both
computers have to be connected via a TCP/IP network and as ZEN brings his own TCP/IP
listener the client software must also have access to a library that allows sending and
receiving messages via TCP/IP. In this case some additional networking knowledge
concerning firewalls and allowed ports etc. within a company or facility network is necessary
to successfully establish a connection between computers.

Our practical experience showed that this TCP/IP approach works very well when software
packages are combined that have very little in common. A typical example is a workflow that
consists of several steps managed by an established workflow software. Generally the
operating systems and/or the software technologies do not match. Usually integration of ZEN
into this workflow can be done with a minimum of effort by using the TCP/IP capabilities of
ZEN.

Why are the efforts of integration done with a minimum amount of time? There are two
reasons for that. First of all TCP/IP is a fundamental technology that is widely known and
used. Second, the commands sent to ZEN driving the imaging software are the same that
are used within a macro. Therefore the commands can be easily tested within the Macro
Environment before they are used to send them via TCP/IP. In addition to that several
macros can be written and saved within the ZEN Macro Environment. Each of these macros
can be executed via TCP/IP by sending ‘run macroname’.

In most cases this very easy approach already fulfills the needs of customers to acquire an image and to do image
processing or analysis afterwards. Typically the macro saves the data to a special location
where the next step of the workflow expect them to be. In the following workflow step otherprocessing
and analysis software packages may work with the data or a feeder is driven by the workflow system to
bring new images to the microscope.

![TCP-IP_Interface_Kitty](/images/TCP-IP_Kitty.png)

![TCP-IP_Interface_Example](/images/Send_Single_Commands_TCP-IP.gif)
