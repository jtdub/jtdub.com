---
layout: post
title: |-
  TelnetCisco.py - A Reusable Module for Accessing Cisco Devices with
  Python
date: '2014-02-17'
author: jtdub
tags:
- Cisco Administration Python Scripting
- Python Tips
- packetgeek.net
---

For one reason or another, Python seems to have been my go to scripting language of choice recently. One of the things that I've been working on is creating a reusable python library for accessing Cisco devices via telnet. It's pretty basic code right now, but I'll be expanding upon what I have soon and will be sharing via github.com as well. For now, here is my simple library.

```python
class TelnetCisco:
	
	def __init__(self, userName, userPass, enablePass, host):
		self.userName = userName
		self.userPass = userPass
		self.enablePass = enablePass
		self.host = host
		
	def getCreds(self):
		import getpass
		
		self.userName = raw_input("Username: ")
		self.userPass = getpass.getpass("User Password: ")
		self.enablePass = getpass.getpass("Enable Password: ")
		
		return self.userName, self.userPass, self.enablePass
		
	def credsFile(self, authfile):
		import os, sys
		
		if os.path.isfile(authfile):
			login = open(authfile, "r")
			self.userName = login.readline()
			self.userName = self.userName.replace("username = ", "")
			self.userName = self.userName.replace("\n", "")
			self.userPass = login.readline()
			self.userPass = self.userPass.replace("password = ", "")
			self.userPass = self.userPass.replace("\n", "")
			self.enablePass = login.readline()
			self.enablePass = self.enablePass.replace("enable = ", "")
			self.enablePass = self.enablePass.replace("\n", "")
			login.close()
		else:
			print "Error:", authfile, "doesn't exist!"
			sys.exit(2)
			
		return self.userName, self.userPass, self.enablePass

	def devLogin(self, devType):
		import telnetlib, re, sys
		
		TelnetCisco.devType = devType
		telnet = telnetlib.Telnet(self.host)
		
		#usermode = re.match("(.*)" + ">", ">")
		#enablemode = re.match("(.*)", "#")
		
		cmds2exe = ['show arp'] 
		
		if devType == "ios":
			telnet.read_until("Username: ", 20)
			telnet.write(self.userName + "\r")
			telnet.read_until("Password: ", 20)
			telnet.write(self.userPass + "\r")
			telnet.read_until(self.host + ">")
			telnet.write("enable\r")
			telnet.read_until("Password: ", 20)
			telnet.write(self.enablePass + "\r")
			telnet.read_until(self.host + "#")
			telnet.write("term length 0\r")
			telnet.read_until(self.host + "#")
			#telnet.write("show arp\r")
			#print telnet.read_until(self.host + "#")
			for command in cmds2exe:
				telnet.write(command + "\r")
				print telnet.read_until(self.host + "#")
			telnet.close()
		else:
			print "Error:", devType, "is unknown by this script.\n"
			sys.exit(2)
		
		return devType, self.host
		
	def codeDebug(self):
		print "### CODE DEBUG ###"
		print "Username:", self.userName
		print "User Password:", self.userPass
		print "Enable Password:", self.enablePass
		print "Host: ", self.host
		print "Device Type: ", TelnetCisco.devType
		print "### CODE DEBUG ###"
```

Usage is pretty simple. You need to specify a username, password, enable password, and host variable. To activate the module. The easiest way is to do it within the your python script.

```bash
import TelnetCisco

username = 'somejoe'
password = 'somepassword'
enable = 'someenable'
host = 'somerouter'

somejob = TelnetCisco(username, password, enable, host)
somejob.devLogin("ios")
```

Of course, the module also has options to specify a authentication file (credsFile(authfile)) or prompt prompt for your credentials (getCreds()). At the moment, the script only runs a 'show arp' on your devices. I'm still working on how I want to implement feeding commands to your devices. I'll post an update as I get more functionality working.
