---
layout: post
title: Updating my Python Scripts to access Cisco Devices
date: '2014-07-26'
author: jtdub
tags:
- Cisco Administration Python Scripting
- Python Tips
- packetgeek.net
---

I've been working to migrate my python scripts, that access Cisco routers and switches to utilize SSH. I'm building out a 'pyRouterLib' class, that currently doesn't have much functionality, but I'm going to be building it out a lot more in the coming months. I'm also working on my pyMultiChange script, so that it utilizes SSH as well. Currently, the work is going well, although, there is still more work to go.

Here is the pyRouterLib library:

```python
#!/usr/bin/env python

class pyRouterLib:
	'''
	Requirments:
	*** Modules:
		os, getpass, paramiko, logging
	'''
	
	def __init__(self, host):
		self.host = host
	
	''' Granular debugging that assists in trouble shooting issues '''
	def debug(self):
		import logging
		logging.basicConfig(level=logging.DEBUG)
	
	''' Define where to get user credentials '''
	def get_creds(self):
		from os.path import expanduser
		import os.path
		homeDir = expanduser("~")
		credsFile = ".tacacslogin"
		credsFile = homeDir + "/" + credsFile
		
		if os.path.isfile(credsFile):
			print "Using existing credentials file."
			credsFileLocation = open(credsFile)
			self.username = credsFileLocation.readline()
			self.username = self.username.strip('\n')
			self.password = credsFileLocation.readline()
			self.password = self.password.strip('\n')
			self.enable = credsFileLocation.readline()
			self.enable = self.enable.strip('\n')
			credsFileLocation.close()
		else:
			import getpass
			print "You have not created a credentials file. Lets create one..."
			self.username = raw_input("Username: ")
			self.password = getpass.getpass("User Password: ")
			self.enable = getpass.getpass("Enable Password: ")
			
			authFile = open(credsFile, 'w+')
			authFile.write(self.username + "\n")
			authFile.write(self.password + "\n")
			authFile.write(self.enable + "\n")
			authFile.close()
				
			print "Your credentials file has been created and is located at: "
			print credsFile + "\n"

		username = self.username
		password = self.password
		enable = self.enable
		
		return username, password, enable
```

Here is the pyMultiShow.py script, which utilizes the pyRouterLib to obtain user credentials:

```python
#!/usr/bin/env python

from pyRouterLib import *
import os, argparse, paramiko, time

''' Define hosts file, command file, verbose variables '''
hosts_file = ''
cmd_file = ''
verbose = False

def arguments():
	''' Function to define the script command line arguments '''
	global hosts_file, cmd_file, verbose
	
	parser = argparse.ArgumentParser(description='A Python implementation of MultiChange, which allows you to make mass changes to routers and switches via SSH.')
	parser.add_argument('-d', '--hosts', help='Specify a host file', required=True)
	parser.add_argument('-c', '--commands', help='Specify a commands file', required=True)
	parser.add_argument('-v', '--verbose', nargs='?', default=False, help='Enables a verbose debugging mode')

	args = vars(parser.parse_args())

	if args['hosts']:
		hosts_file = args['hosts']
	if args['commands']:
		cmd_file = args['commands']
	if args['verbose'] == None:
		verbose = True
	
	return hosts_file, cmd_file, verbose

arguments()

''' open the hosts file and commands file and execute each command on every host '''
if os.path.isfile(hosts_file):
	hosts = open(hosts_file, 'r')
	for host in hosts:
		host = host.strip("\n")
		
		''' use pyRouterLib to grab the user authentication credentials '''
		rlib = pyRouterLib(host)
		creds = rlib.get_creds()
		username = creds[0]
		password = creds[1]
		enable = creds[2]
		
		''' Enable verbose debugging '''
		if verbose:
			rlib.debug()
		
		remoteConnectionSetup = paramiko.SSHClient()
		remoteConnectionSetup.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remoteConnectionSetup.connect(host, username=username, password=password, allow_agent=False, look_for_keys=False)
		print "*** SSH connection established to %s" % host
		remoteConnection = remoteConnectionSetup.invoke_shell()
		print "*** Interactive SSH session established"
		cmds = open(cmd_file, 'r')
		for command in cmds:
			remoteConnection.send(command)
			print "*** Executing Command: %s" % command
			if verbose:
				time.sleep(2)
				output = remoteConnection.recv(10000)
				print output
		cmds.close()
		print "*** Closing Connection to %s" % host
	hosts.close()
```

Both can be accessed from my [github](https://github.com/jtdub/pyRouterLib).
