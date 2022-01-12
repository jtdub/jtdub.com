---
layout: post
title: Working with Cisco Routers and Switches with Python
date: '2014-07-27'
author: jtdub
tags:
- Cisco Administration Python Scripting
- System Administration
- Miscellaneous Hacking
- Python Tips
- packetgeek.net
---

I've updated the pyMultiChange.py script. It now is fully functional, with the addition of enable mode functionality. With this script, you can take a list of routers and switches from a text file and execute a series of commands, from a text file, all from SSH. For example:

Here is the usage output, if you don't select the required arguments:

```bash
$ ./pyMultiChange.py
usage: pyMultiChange.py [-h] -d HOSTS -c COMMANDS [-v [VERBOSE]]
pyMultiChange.py: error: argument -d/--hosts is required
```

Here is the usage output, without verbose / debugging mode:

```bash
$ ./pyMultiChange.py -d hosts.txt -c commands.txt
Using existing credentials file.
*** SSH connection established to 172.16.1.1
*** Executing Command: sh ver
*** Closing Connection to 172.16.1.1
Using existing credentials file.
*** SSH connection established to 172.16.1.6
*** Executing Command: sh ver
*** Closing Connection to 172.16.1.6
```

Here is the usage output, with verbose / debugging mode:

```bash
$ ./pyMultiChange.py -d hosts.txt -c commands.txt -v
Using existing credentials file.
DEBUG:paramiko.transport:starting thread (client mode): 0x78b9510L
INFO:paramiko.transport:Connected (version 2.0, client Cisco-1.25)
DEBUG:paramiko.transport:kex algos:[u'diffie-hellman-group-exchange-sha1', u'diffie-hellman-group14-sha1', u'diffie-hellman-group1-sha1'] server key:[u'ssh-rsa'] client encrypt:[u'aes128-cbc', u'3des-cbc', u'aes192-cbc', u'aes256-cbc'] server encrypt:[u'aes128-cbc', u'3des-cbc', u'aes192-cbc', u'aes256-cbc'] client mac:[u'hmac-sha1', u'hmac-sha1-96', u'hmac-md5', u'hmac-md5-96'] server mac:[u'hmac-sha1', u'hmac-sha1-96', u'hmac-md5', u'hmac-md5-96'] client compress:[u'none'] server compress:[u'none'] client lang:[u''] server lang:[u''] kex follows?False
DEBUG:paramiko.transport:Ciphers agreed: local=aes128-cbc, remote=aes128-cbc
DEBUG:paramiko.transport:using kex diffie-hellman-group1-sha1; server key type ssh-rsa; cipher: local aes128-cbc, remote aes128-cbc; mac: local hmac-sha1, remote hmac-sha1; compression: local none, remote none
DEBUG:paramiko.transport:Switch to new keys ...
DEBUG:paramiko.transport:Adding ssh-rsa host key for 172.16.1.1: d9df7efac164fbf7828fa284d5a31e63
DEBUG:paramiko.transport:userauth is OK
INFO:paramiko.transport:Authentication (password) successful!
*** SSH connection established to 172.16.1.1
DEBUG:paramiko.transport:[chan 1] Max packet in: 34816 bytes
DEBUG:paramiko.transport:[chan 1] Max packet out: 4096 bytes
INFO:paramiko.transport:Secsh channel 1 opened.
DEBUG:paramiko.transport:[chan 1] Sesch channel 1 request ok
DEBUG:paramiko.transport:[chan 1] Sesch channel 1 request ok
*** Interactive SSH session established
*** Sending enable password
*** Successfully entered enable mode
*** Executing Command: sh ver
terminal length 0
darkstar#sh ver
Cisco IOS Software, C880 Software (C880DATA-UNIVERSALK9-M), Version 15.0(1)M7, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Fri 05-Aug-11 02:01 by prod_rel_team

ROM: System Bootstrap, Version 12.4(22r)YB5, RELEASE SOFTWARE (fc1)

darkstar uptime is 10 weeks, 6 days, 12 minutes
System returned to ROM by power-on
System restarted at 23:21:02 CST Mon May 12 2014
System image file is "flash:c880data-universalk9-mz.150-1.M7.bin"
Last reload type: Normal Reload


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

Cisco 881 (MPC8300) processor (revision 1.0) with 236544K/25600K bytes of memory.
Processor board ID FTX16038388

5 FastEthernet interfaces
1 Gigabit Ethernet interface
1 terminal line
1 Virtual Private Network (VPN) Module
1 cisco Embedded AP (s)
256K bytes of non-volatile configuration memory.
126000K bytes of ATA CompactFlash (Read/Write)


License Info:

License UDI:

-------------------------------------------------
Device#	  PID			SN
-------------------------------------------------
*0  	  CISCO881W-GN-A-K9     FTX16038388     



License Information for 'c880-data'
    License Level: advsecurity   Type: Permanent
    Next reboot license Level: advsecurity


Configuration register is 0x2102

darkstar#
*** Closing Connection to 172.16.1.1
Using existing credentials file.
DEBUG:paramiko.transport:EOF in transport thread
DEBUG:paramiko.transport:starting thread (client mode): 0x78b9250L
INFO:paramiko.transport:Connected (version 2.0, client Cisco-1.25)
DEBUG:paramiko.transport:kex algos:[u'diffie-hellman-group1-sha1'] server key:[u'ssh-rsa'] client encrypt:[u'aes128-cbc', u'3des-cbc', u'aes192-cbc', u'aes256-cbc'] server encrypt:[u'aes128-cbc', u'3des-cbc', u'aes192-cbc', u'aes256-cbc'] client mac:[u'hmac-sha1', u'hmac-sha1-96', u'hmac-md5', u'hmac-md5-96'] server mac:[u'hmac-sha1', u'hmac-sha1-96', u'hmac-md5', u'hmac-md5-96'] client compress:[u'none'] server compress:[u'none'] client lang:[u''] server lang:[u''] kex follows?False
DEBUG:paramiko.transport:Ciphers agreed: local=aes128-cbc, remote=aes128-cbc
DEBUG:paramiko.transport:using kex diffie-hellman-group1-sha1; server key type ssh-rsa; cipher: local aes128-cbc, remote aes128-cbc; mac: local hmac-sha1, remote hmac-sha1; compression: local none, remote none
DEBUG:paramiko.transport:Switch to new keys ...
DEBUG:paramiko.transport:Adding ssh-rsa host key for 172.16.1.6: 917d0abc26c16df9860f57e3a248db1c
DEBUG:paramiko.transport:userauth is OK
INFO:paramiko.transport:Authentication (password) successful!
*** SSH connection established to 172.16.1.6
DEBUG:paramiko.transport:[chan 1] Max packet in: 34816 bytes
DEBUG:paramiko.transport:[chan 1] Max packet out: 4096 bytes
INFO:paramiko.transport:Secsh channel 1 opened.
DEBUG:paramiko.transport:[chan 1] Sesch channel 1 request ok
DEBUG:paramiko.transport:[chan 1] Sesch channel 1 request ok
*** Interactive SSH session established
*** Sending enable password
*** Successfully entered enable mode
*** Executing Command: sh ver
terminal length 0
sgncs1#sh ver
Cisco IOS Software, C3550 Software (C3550-IPSERVICESK9-M), Version 12.2(44)SE6, RELEASE SOFTWARE (fc1)
Copyright (c) 1986-2009 by Cisco Systems, Inc.
Compiled Mon 09-Mar-09 20:28 by gereddy
Image text-base: 0x00003000, data-base: 0x012A99FC

ROM: Bootstrap program is C3550 boot loader

sgncs1 uptime is 5 weeks, 2 days, 20 hours, 12 minutes
System returned to ROM by power-on
System restarted at 03:21:32 CST Fri Jun 20 2014
System image file is "flash:c3550-ipservicesk9-mz.122-44.SE6.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

Cisco WS-C3550-24 (PowerPC) processor (revision G0) with 65526K/8192K bytes of memory.
Processor board ID CHK0644W0KC
Last reset from warm-reset
Running Layer2/3 Switching Image

Ethernet-controller 1 has 12 Fast Ethernet/IEEE 802.3 interfaces

Ethernet-controller 2 has 12 Fast Ethernet/IEEE 802.3 interfaces

Ethernet-controller 3 has 1 Gigabit Ethernet/IEEE 802.3 interface

Ethernet-controller 4 has 1 Gigabit Ethernet/IEEE 802.3 interface

24 FastEthernet interfaces
2 Gigabit Ethernet interfaces

The password-recovery mechanism is enabled.
384K bytes of flash-simulated NVRAM.
Base ethernet MAC Address: 00:0B:46:FE:D5:80
Motherboard assembly number: 73-5700-09
Power supply part number: 34-0966-02
Motherboard serial number: CAT064307TM
Power supply serial number: LIT063501PN
Model revision number: G0
Motherboard revision number: A0
Model number: WS-C3550-24-SMI
System serial number: CHK0644W0KC
Configuration register is 0x10F

sgncs1#
*** Closing Connection to 172.16.1.6
DEBUG:paramiko.transport:EOF in transport thread
```

Finally, here is the code:

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
		if verbose:
			print "*** Interactive SSH session established"
		
		time.sleep(1)
		is_enable = remoteConnection.recv(1000)
		if "#" not in is_enable:
			remoteConnection.send("enable\n")
			time.sleep(1)
			if_enable = remoteConnection.recv(1000)
			if "Password:" in if_enable:
				if verbose:
					print "*** Sending enable password"
				remoteConnection.send(enable)
				remoteConnection.send("\n")
		
			time.sleep(2)
			is_enable = remoteConnection.recv(1000)
		
			if "#" in is_enable:
				if verbose:
					print "*** Successfully entered enable mode"
			
				remoteConnection.send("terminal length 0\n")
			else:
				if verbose:
					print "*** Entering enable mode was unsuccessful"
		else:
			remoteConnection.send("terminal length 0\n")
			if verbose:
				print "*** User: %s already has enable privileges" % username
		
		cmds = open(cmd_file, 'r')
		for command in cmds:
			command = command.strip()
			remoteConnection.send(command)
			remoteConnection.send("\n")
			print "*** Executing Command: %s" % command
			if verbose:
				time.sleep(2)
				output = remoteConnection.recv(10000)
				print output
		cmds.close()
		print "*** Closing Connection to %s" % host
	hosts.close()
```

I'm going to continue working on building out the pyRouterLib module, as there is so much functionality that could be added to that. I'll keep you updated on the progress. As always, updates will be posted to my [github](https://github.com/jtdub/pyRouterLib).
