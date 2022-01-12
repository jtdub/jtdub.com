---
layout: post
title: Multi Change and Netlib Updates
date: '2016-06-22'
author: jtdub
tags:
- Cisco Administration Python Scripting
- Python Tips
- Network Programmability
- DevOps
- Network DevOps
- packetgeek.net
---

I've implemented some new changes to pyMultiChange and netlib. The biggest change affects both netlib and pyMultiChange. In netlib, I ripped out both the 'simple_creds' and 'simple_yaml' methods, as both stored user credentials in plain text on the computer that you used them on.

Instead, utilizing the 'keyring' python module, I created a new class called 'KeyRing'. Using 'KeyRing' is simple. It implements three methods. These methods are 'get_creds', 'set_creds', and 'del_creds'.

'get_creds' will attempt to retrieve the credentials for a username, if the credentials exist. If they do not exist, 'get_creds' will automatically call the 'set_creds' method.

```python
>>> from netlib.user_keyring import KeyRing
>>> creds = KeyRing(username='testuser')
>>> creds.get_creds()
No credentials keyring exist. Creating new credentials.
Enter your user password: 
Confirm your user password: 
Enter your enable password: 
Confirm your enable password: 
>>> print creds.get_creds()
{'username': 'testuser', 'enable': u'test', 'password': u'testpass'}
>>> 
```

'set_creds' does exactly what it sounds like. It allows you to set your credentials. If no user credentials exist, it creates a new keyring. However, if user credentials do exist, it over-writes the credentials.

```python
>>> creds.set_creds()
Enter your user password: 
Confirm your user password: 
Enter your enable password: 
Confirm your enable password: 
>>> print creds.get_creds()
{'username': 'testuser', 'enable': u'enable123', 'password': u'test123'}
```

Finally, 'del_creds' deletes a user's credentials from an existing keyring.

```python
>>> creds.del_creds()
Enter your user password: 
Deleting keyring credentials for testuser
```

The '[keyring](https://pypi.python.org/pypi/keyring)' python library utilizes your operating systems native methods for storing passwords. For Example, in Mac OS X, it will utilize the KeyChain functionality, In Linux, it will use dbus, and in Microsoft Windows, it utilizes the Credential Vault. There are also methods available for you to create your own backend. Much more secure than the ~/.tacacslogin or ~/.tacacs.yml files that used to be created from the old methods.

As expected, this change was implemented into pyMultiChange. Doing so, required that new command line arguments needed to be implemented. There are actually several new command line arguments, since the last time that I wrote about pyMultiChange. I'll go over them here.

```bash
usage: multi_change.py [-h] -u USERNAME [--delete-creds [DELETE_CREDS]]
                       [--set-creds [SET_CREDS]] [-d DEVICES] [-c COMMANDS]
                       [-s [SSH]] [-t [TELNET]] [-o [OUTPUT]] [-v [VERBOSE]]
                       [--delay DELAY] [--buffer BUFFER]
                       [--threaded [THREADED]] [-m MAXTHREADS]

Managing network devices with python

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Specify your username.
  --delete-creds [DELETE_CREDS]
                        Delete credentials from keyring.
  --set-creds [SET_CREDS]
                        set keyring credentials.
  -d DEVICES, --devices DEVICES
                        Specifies a host file
  -c COMMANDS, --commands COMMANDS
                        Specifies a commands file
  -s [SSH], --ssh [SSH]
                        Default: Use the SSH protocol
  -t [TELNET], --telnet [TELNET]
                        Use the Telnet protocol
  -o [OUTPUT], --output [OUTPUT]
                        Verbose command output
  -v [VERBOSE], --verbose [VERBOSE]
                        Debug script output
  --delay DELAY         Change the default delay exec between commands
  --buffer BUFFER       Change the default SSH output buffer
  --threaded [THREADED]
                        Enable process threading
  -m MAXTHREADS, --maxthreads MAXTHREADS
                        Define the maximum number of threads
```

The first, is that multi_change.py now requires that you specify a username for all actions. This allows multi_change.py to interact with the keyring to set, extract, and delete credentials.

```bash
usage: multi_change.py [-h] -u USERNAME [--delete-creds [DELETE_CREDS]]
                       [--set-creds [SET_CREDS]] [-d DEVICES] [-c COMMANDS]
                       [-s [SSH]] [-t [TELNET]] [-o [OUTPUT]] [-v [VERBOSE]]
                       [--delay DELAY] [--buffer BUFFER]
                       [--threaded [THREADED]] [-m MAXTHREADS]
multi_change.py: error: argument -u/--username is required
```

When you specify a username, multi_change.py immediately attempts to extract the credentials for the user. If they don't exist, multi_change.py will prompt you to set the credentials.

```bash
$ multi_change.py -u testuser
No credentials keyring exist. Creating new credentials.
Enter your user password: 
Confirm your user password: 
Enter your enable password: 
Confirm your enable password:
```

You can also utilize the '--set-creds' command line argument to either set credentials for a new user or over-write the credentials for an existing user.

```bash
$ multi_change.py -u testuser --set-creds
Enter your user password: 
Confirm your user password: 
Enter your enable password: 
Confirm your enable password:
```

Like wise, you can use the '--delete-creds' to delete existing creds.

```bash
$ multi_change.py -u testuser --delete-creds
Enter your user password: 
Deleting keyring credentials for testuser
```

Beyond that, the option to utilize threading was created. With the threading ability, you also get the ability to specify the number of threads and the delay factor between command execution.

For example, the below series of command line arguments enable threading, utilizing 50 threads, create a delay factor of 5 seconds, and will display the command output.

```bash
$ multi_change.py -u testuser -d hosts.txt -c commands.txt --threaded -m 50 --delay 5 -o
```

This is very handy for running a common command set across a large number of devices very quickly.

Beyond that, there are a few under the hood enhancements.

* Protocol failover will no longer happen. Meaning that if a device fails to login via SSH, it will no longer failover to attempt to login via telnet and vise versa.
* Login failures are logged in a file called 'failure.log'. This file is created in the local folder that you're running 'multi_change.py' in.
* multi_change.py will now only read the commands file once, rather than reading it for every device that it attempts to make changes on.
* pyMultiChange and netlib are now python installable packages. Meaning that you can run their 'setup.py' files and they will be installed as native python packages, allowing them to be called from anywhere on the OS.

Both packages are available on github.com:

* [netlib](https://github.com/jtdub/netlib)
* [pyMultiChange](https://github.com/jtdub/pyMultiChange)
