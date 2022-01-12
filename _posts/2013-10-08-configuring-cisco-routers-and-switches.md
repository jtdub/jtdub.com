---
layout: post
title: Configuring Cisco routers and switches with Python
date: '2013-10-08'
author: jtdub
tags:
- Cisco Administration Python Scripting
- IOS
- Python Tips
- Cisco Administration Perl Scripting
- packetgeek.net
---
**Update**: I've updated the multichange script a lot since I first wrote about it. You can use the category function to see the [various posts](http://www.packetgeek.net/category/python-tips/).

You can also look at [pyRouterLib](https://github.com/jtdub/pyRouterLib) and [pyMultiChange](https://github.com/jtdub/pyMultiChange).

In my new job role, I've been rediscovering the limitations of the Perl Module [Net::Telnet::Cisco](http://search.cpan.org/~joshua/Net-Telnet-Cisco-1.10/Cisco.pm) when executing mass changes to network devices, so I've been looking for alternatives. Particularly, Net::Telnet::Cisco doesn't play nicely with NX-OS, IOS-XR, or Arista EOS - without a major re-write. So, I've been experimenting with a Python implementation. Below is what I have so far, which is working well, but is far from production ready.

```python
#!/usr/bin/env python

import getpass
import sys
import telnetlib
import os

# Variables
tacacs = '.tacacslogin'
commandsfile = 'commands.txt'
hostsfile = 'hosts.txt'
devicetype = "ios"
verbose = "yes"

def userlogin():
    # Getting login credentials
    global username, password, enable
    if os.path.isfile(tacacs):
        login = open(tacacs, "r")
        username = login.readline()
        username = username.replace("\n", "")
        password = login.readline()
        password = password.replace("\n", "")
        enable = login.readline()
        enable = enable.replace("\n", "")
        login.close()
    else:
        print tacacs, "not found.\n"
        username = raw_input("Username: ")
        password = getpass.getpass("User Password: ")
        enable = getpass.getpass("Enable Password: ")

    return username, password, enable

def login(devicetype):
    # Logging in with username, password, and eable password
    global username, password, enable
    if devicetype == "nexus":
        telnet.read_until("Login: ")
        telnet.write(str(username) + "\n")
    else:
        telnet.read_until("Username: ")
        telnet.write(str(username) + "\n")

    if password:
        telnet.read_until("Password: ")
        telnet.write(str(password) + "\n")

    if devicetype == "ios":
        if enable:
            telnet.read_until(host2login + '>')
            telnet.write("enable\n")
            telnet.read_until("Password: ")
            telnet.write(str(enable) + "\n")

def sessioncommands():
    # Executing commands on the host
    global commands
    print "Executing Commands on", host2login
    if os.path.isfile(commandsfile):
        commands = open(commandsfile, "r")
        try:
            for cmd2exe in commands:
                telnet.write(cmd2exe)
        finally:
            commands.close()
    else:
        print commandsfile, " doesn't exist"
        telnet.write("exit\n")
    # Displaying the results
    if verbose == "yes":
        output = telnet.read_all()
        if "% " in output:
            print "Error: ", output
            sys.exit()
        else:
            print output

    print "Logging out of", host2login

# Doing work 
userlogin()
if os.path.isfile(hostsfile):
    hosts = open(hostsfile, "r")
    while 1:
        host2login = hosts.readline()
        host2login = host2login.replace("\n", "")
        print "Logging into", host2login
        if not host2login:
            break
        else:
            telnet = telnetlib.Telnet(host2login)
            login(devicetype)
            sessioncommands()
    hosts.close()
else:
    host2login = raw_input("Host: ")
    print "Logging into", host2login
    telnet = telnetlib.Telnet(host2login)
    login(devicetype)
    sessioncommands()
```

I need to implement the [getops](http://docs.python.org/2/library/getopt.html#module-getopt) Python module to make it more command line friendly. I'm sure that I'll also find some tweaks that I need to make here and there as I experiment with other devices. So far, it works pretty well with IOS devices. I'll post updates as it becomes more stable, user friendly, and over all useful. This is just what I've come up with in a couple hours of tinkering and reteaching myself Python.
