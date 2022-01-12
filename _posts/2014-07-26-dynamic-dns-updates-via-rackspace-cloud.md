---
layout: post
title: Dynamic DNS Updates via the Rackspace Cloud DNS
date: '2014-07-26'
author: jtdub
tags:
- DNS
- Python Tips
- Bind
- Rackspace
- packetgeek.net
---

Do you remember the old days when dyndns.org offered free sub domains, that pointed to your home internet connection? This service allowed you to access your home computer remotely, by hostname, without the need of remembering your IP Address.

I wrote a python script that does something similar. It uses the Rackspace Cloud API to manage an DNS A record of a domain that you own and is hosted with Rackspace.

Below is the code:

```bash
#!/usr/bin/env python
import pyrax, urllib, socket

'''Variables'''
username = '{USERNAME}'
api_key = '{API_KEY}'
domain_name = '{DOMAIN.COM}'
record_id = '{RECORD_ID}'
dyn_domain = '{DYNDNS_HOSTNAME}'
debug = True

'''Do not change these variables'''
ip = ''
domain = ''
record = ''

'''Functions'''
def get_ip():
	global ip, debug
	ip = urllib.urlopen('http://icanhazip.com')
	ip = ip.read()
	ip = ip.strip("\n")
	
	if debug:
		print "*** Current IP Address: %s" % ip
	
	return ip
	
def get_dyn_ip():
	global ip, debug, dyn_domain
	dyn_domain_ip = socket.gethostbyname(dyn_domain)
	
	if debug:
		print "*** Current IP Address: %s" % ip
		print "*** DNS A Record of %s: %s" % (dyn_domain, dyn_domain_ip)
	
	if ip == dyn_domain_ip:
		if debug:
			print "*** %s is already current for %s. Nothing to do." % (dyn_domain_ip, dyn_domain)
		exit(1)
	else:
		update_domain(ip)
	
	return ip

def rax_auth(user, api):
	global debug
	
	if debug:
		print "*** Username: %s, API_Key: %s" % (user, api)

	pyrax.set_setting('identity_type', 'rackspace')
	pyrax.set_credentials(user, api)

def get_domain(dns_domain, dns_record_id):
	global debug, domain, record

	if debug:
		print "*** Domain Name: %s, Record Id: %s" % (dns_domain, dns_record_id)

	domain = pyrax.cloud_dns.find(name=dns_domain)
	record = domain.get_record(dns_record_id)
	
	return domain, record

def update_domain(ip):
	global debug, username, api_key, domain_name, record_id
	
	rax_auth(username, api_key)
	get_domain(domain_name, record_id)
	if debug:
		print "*** Updated IP Address: %s" % ip
	record.update(data=ip)

'''Executing Functions'''
get_ip()
get_dyn_ip()
```

There are a couple things that still need to be added:
* Check to see if {dyn_domain} exists, if it doesn't, create it.
* Obtain the {record_id} automatically.

Given that, the current limitations are:
* Your hostname, needs to already exist. The script will only update the hostname, not create it. Example: thisismyhomepc.example.com
* You have to obain the record ID by hand.

In the examples, I'm going to be using CentOS 7. The first thing that I'm going to do is install EPEL, which will allow me to install the package 'pip'.

```bash
[jtdub@pyrax-test ~]$ sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm
Retrieving http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm
warning: /var/tmp/rpm-tmp.tb0sU3: Header V3 RSA/SHA256 Signature, key ID 352c64e5: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:epel-release-7-0.2               ################################# [100%]
[jtdub@pyrax-test ~]$ sudo yum -y install python-pip
Loaded plugins: fastestmirror
epel/x86_64/metalink                                                                                                                                              |  11 kB  00:00:00     
epel                                                                                                                                                              | 3.7 kB  00:00:00     
(1/2): epel/x86_64/group_gz                                                                                                                                       | 163 kB  00:00:00     
(2/2): epel/x86_64/primary_db                                                                                                                                     | 2.1 MB  00:00:00     
Loading mirror speeds from cached hostfile
 * base: centos.someimage.com
 * epel: mirrors.mit.edu
 * extras: mirrors.einstein.yu.edu
 * updates: centos.hostingxtreme.com
Resolving Dependencies
--> Running transaction check
---> Package python-pip.noarch 0:1.3.1-4.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=========================================================================================================================================================================================
 Package                                       Arch                                      Version                                           Repository                               Size
=========================================================================================================================================================================================
Installing:
 python-pip                                    noarch                                    1.3.1-4.el7                                       epel                                    315 k

Transaction Summary
=========================================================================================================================================================================================
Install  1 Package

Total download size: 315 k
Installed size: 1.0 M
Downloading packages:
python-pip-1.3.1-4.el7.noarch.rpm                                                                                                                                 | 315 kB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : python-pip-1.3.1-4.el7.noarch                                                                                                                                         1/1 
  Verifying  : python-pip-1.3.1-4.el7.noarch                                                                                                                                         1/1 

Installed:
  python-pip.noarch 0:1.3.1-4.el7                                                                                                                                                        

Complete!
[jtdub@pyrax-test ~]$
```

Once that is installed, we can install the python module that we'll need, which is pyrax - which is the Rackspace Python SDK for their Cloud.

```bash
[jtdub@pyrax-test ~]$ sudo pip install pyrax
Downloading/unpacking pyrax
  Downloading pyrax-1.9.0.tar.gz (308kB): 308kB downloaded
  Running setup.py egg_info for package pyrax
    
Downloading/unpacking python-novaclient>=2.13.0 (from pyrax)
  Downloading python-novaclient-2.18.1.tar.gz (254kB): 254kB downloaded
  Running setup.py egg_info for package python-novaclient
    
    Installed /tmp/pip-build-root/python-novaclient/pbr-0.10.0-py2.7.egg
    [pbr] Processing SOURCES.txt
    warning: LocalManifestMaker: standard file '-c' not found
    
    warning: no previously-included files found matching '.gitignore'
    warning: no previously-included files found matching '.gitreview'
    warning: no previously-included files matching '*.pyc' found anywhere in distribution
    warning: no previously-included files found matching '.gitignore'
    warning: no previously-included files found matching '.gitreview'
Downloading/unpacking rackspace-novaclient (from pyrax)
  Downloading rackspace-novaclient-1.4.tar.gz
  Running setup.py egg_info for package rackspace-novaclient
    
Downloading/unpacking keyring (from pyrax)
  Downloading keyring-3.8.zip (84kB): 84kB downloaded
  Running setup.py egg_info for package keyring
    
    warning: no previously-included files found matching '.hg/last-message.txt'
Downloading/unpacking requests>=2.2.1 (from pyrax)
  Downloading requests-2.3.0.tar.gz (429kB): 429kB downloaded
  Running setup.py egg_info for package requests
    
Downloading/unpacking six>=1.5.2 (from pyrax)
  Downloading six-1.7.3.tar.gz
  Running setup.py egg_info for package six
    
    no previously-included directories found matching 'documentation/_build'
Downloading/unpacking mock (from pyrax)
  Downloading mock-1.0.1.tar.gz (818kB): 818kB downloaded
  Running setup.py egg_info for package mock
    
    warning: no files found matching '*.png' under directory 'docs'
    warning: no files found matching '*.css' under directory 'docs'
    warning: no files found matching '*.html' under directory 'docs'
    warning: no files found matching '*.js' under directory 'docs'
Downloading/unpacking pbr>=0.6,!=0.7,<1.0 (from python-novaclient>=2.13.0->pyrax)
  Downloading pbr-0.10.0.tar.gz (77kB): 77kB downloaded
  Running setup.py egg_info for package pbr
    [pbr] Processing SOURCES.txt
    warning: LocalManifestMaker: standard file '-c' not found
    
    warning: no previously-included files found matching '.gitignore'
    warning: no previously-included files found matching '.gitreview'
    warning: no previously-included files matching '*.pyc' found anywhere in distribution
    warning: no previously-included files found matching '.gitignore'
    warning: no previously-included files found matching '.gitreview'
    warning: no previously-included files matching '*.pyc' found anywhere in distribution
Downloading/unpacking argparse (from python-novaclient>=2.13.0->pyrax)
  Downloading argparse-1.2.1.tar.gz (69kB): 69kB downloaded
  Running setup.py egg_info for package argparse
    
    warning: no previously-included files matching '*.pyc' found anywhere in distribution
    warning: no previously-included files matching '*.pyo' found anywhere in distribution
    warning: no previously-included files matching '*.orig' found anywhere in distribution
    warning: no previously-included files matching '*.rej' found anywhere in distribution
    no previously-included directories found matching 'doc/_build'
    no previously-included directories found matching 'env24'
    no previously-included directories found matching 'env25'
    no previously-included directories found matching 'env26'
    no previously-included directories found matching 'env27'
Downloading/unpacking iso8601>=0.1.9 (from python-novaclient>=2.13.0->pyrax)
  Downloading iso8601-0.1.10.tar.gz
  Running setup.py egg_info for package iso8601
    
Downloading/unpacking PrettyTable>=0.7,<0.8 (from python-novaclient>=2.13.0->pyrax)
  Downloading prettytable-0.7.2.tar.bz2
  Running setup.py egg_info for package PrettyTable
    
Downloading/unpacking simplejson>=2.0.9 (from python-novaclient>=2.13.0->pyrax)
  Downloading simplejson-3.6.0.tar.gz (70kB): 70kB downloaded
  Running setup.py egg_info for package simplejson
    
Downloading/unpacking Babel>=1.3 (from python-novaclient>=2.13.0->pyrax)
  Downloading Babel-1.3.tar.gz (3.4MB): 3.4MB downloaded
  Running setup.py egg_info for package Babel
    
    warning: no previously-included files matching '*' found under directory 'docs/_build'
    warning: no previously-included files matching '*.pyc' found under directory 'tests'
    warning: no previously-included files matching '*.pyo' found under directory 'tests'
Downloading/unpacking rackspace-auth-openstack (from rackspace-novaclient->pyrax)
  Downloading rackspace-auth-openstack-1.3.tar.gz
  Running setup.py egg_info for package rackspace-auth-openstack
    
Downloading/unpacking os-diskconfig-python-novaclient-ext (from rackspace-novaclient->pyrax)
  Downloading os_diskconfig_python_novaclient_ext-0.1.2.tar.gz
  Running setup.py egg_info for package os-diskconfig-python-novaclient-ext
    
Downloading/unpacking rax-scheduled-images-python-novaclient-ext (from rackspace-novaclient->pyrax)
  Downloading rax_scheduled_images_python_novaclient_ext-0.2.2.tar.gz
  Running setup.py egg_info for package rax-scheduled-images-python-novaclient-ext
    
Downloading/unpacking os-networksv2-python-novaclient-ext (from rackspace-novaclient->pyrax)
  Downloading os_networksv2_python_novaclient_ext-0.21.tar.gz
  Running setup.py egg_info for package os-networksv2-python-novaclient-ext
    
Downloading/unpacking os-virtual-interfacesv2-python-novaclient-ext (from rackspace-novaclient->pyrax)
  Downloading os_virtual_interfacesv2_python_novaclient_ext-0.15.tar.gz
  Running setup.py egg_info for package os-virtual-interfacesv2-python-novaclient-ext
    
Downloading/unpacking rax-default-network-flags-python-novaclient-ext (from rackspace-novaclient->pyrax)
  Downloading rax_default_network_flags_python_novaclient_ext-0.2.4.tar.gz
  Running setup.py egg_info for package rax-default-network-flags-python-novaclient-ext
    
Requirement already satisfied (use --upgrade to upgrade): pip in /usr/lib/python2.7/site-packages (from pbr>=0.6,!=0.7,<1.0->python-novaclient>=2.13.0->pyrax)
Downloading/unpacking pytz>=0a (from Babel>=1.3->python-novaclient>=2.13.0->pyrax)
  Downloading pytz-2014.4.tar.bz2 (159kB): 159kB downloaded
  Running setup.py egg_info for package pytz
    
Installing collected packages: pyrax, python-novaclient, rackspace-novaclient, keyring, requests, six, mock, pbr, argparse, iso8601, PrettyTable, simplejson, Babel, rackspace-auth-openstack, os-diskconfig-python-novaclient-ext, rax-scheduled-images-python-novaclient-ext, os-networksv2-python-novaclient-ext, os-virtual-interfacesv2-python-novaclient-ext, rax-default-network-flags-python-novaclient-ext, pytz
  Running setup.py install for pyrax
    /usr/bin/python -O /tmp/tmpB0aWjs.py
    removing /tmp/tmpB0aWjs.py
    
  Running setup.py install for python-novaclient
    [pbr] Reusing existing SOURCES.txt
    Installing nova script to /usr/bin
  Running setup.py install for rackspace-novaclient
    
  Running setup.py install for keyring
    
    warning: no previously-included files found matching '.hg/last-message.txt'
    Installing keyring script to /usr/bin
  Running setup.py install for requests
    
  Running setup.py install for six
    
    no previously-included directories found matching 'documentation/_build'
  Running setup.py install for mock
    
    warning: no files found matching '*.png' under directory 'docs'
    warning: no files found matching '*.css' under directory 'docs'
    warning: no files found matching '*.html' under directory 'docs'
    warning: no files found matching '*.js' under directory 'docs'
  Running setup.py install for pbr
    [pbr] Reusing existing SOURCES.txt
  Running setup.py install for argparse
    
    warning: no previously-included files matching '*.pyc' found anywhere in distribution
    warning: no previously-included files matching '*.pyo' found anywhere in distribution
    warning: no previously-included files matching '*.orig' found anywhere in distribution
    warning: no previously-included files matching '*.rej' found anywhere in distribution
    no previously-included directories found matching 'doc/_build'
    no previously-included directories found matching 'env24'
    no previously-included directories found matching 'env25'
    no previously-included directories found matching 'env26'
    no previously-included directories found matching 'env27'
  Running setup.py install for iso8601
    
  Running setup.py install for PrettyTable
    
  Running setup.py install for simplejson
    building 'simplejson._speedups' extension
    gcc -pthread -fno-strict-aliasing -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv -DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv -fPIC -I/usr/include/python2.7 -c simplejson/_speedups.c -o build/temp.linux-x86_64-2.7/simplejson/_speedups.o
    unable to execute gcc: No such file or directory
    ***************************************************************************
    WARNING: The C extension could not be compiled, speedups are not enabled.
    Failure information, if any, is above.
    I'm retrying the build without the C extension now.
    ***************************************************************************
    
    ***************************************************************************
    WARNING: The C extension could not be compiled, speedups are not enabled.
    Plain-Python installation succeeded.
    ***************************************************************************
  Running setup.py install for Babel
    
    warning: no previously-included files matching '*' found under directory 'docs/_build'
    warning: no previously-included files matching '*.pyc' found under directory 'tests'
    warning: no previously-included files matching '*.pyo' found under directory 'tests'
    Installing pybabel script to /usr/bin
  Running setup.py install for rackspace-auth-openstack
    
  Running setup.py install for os-diskconfig-python-novaclient-ext
    
  Running setup.py install for rax-scheduled-images-python-novaclient-ext
    
  Running setup.py install for os-networksv2-python-novaclient-ext
    
  Running setup.py install for os-virtual-interfacesv2-python-novaclient-ext
    
  Running setup.py install for rax-default-network-flags-python-novaclient-ext
    
  Running setup.py install for pytz
    
Successfully installed pyrax python-novaclient rackspace-novaclient keyring requests six mock pbr argparse iso8601 PrettyTable simplejson Babel rackspace-auth-openstack os-diskconfig-python-novaclient-ext rax-scheduled-images-python-novaclient-ext os-networksv2-python-novaclient-ext os-virtual-interfacesv2-python-novaclient-ext rax-default-network-flags-python-novaclient-ext pytz
Cleaning up...
```

Once you've installed the needed modules, you can verify that they are available for use.

```bash
[jtdub@pyrax-test ~]$ python
Python 2.7.5 (default, Jun 17 2014, 18:11:42) 
[GCC 4.8.2 20140120 (Red Hat 4.8.2-16)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyrax
>>> dir(pyrax)
['AutoScaleClient', 'CloudBlockStorageClient', 'CloudDNSClient', 'CloudDatabaseClient', 'CloudLoadBalancerClient', 'CloudMonitorClient', 'CloudNetworkClient', 'CloudServer', 'ConfigParser', 'ImageClient', 'QueueClient', 'Settings', 'StorageClient', 'USER_AGENT', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', '_assure_identity', '_client_classes', '_create_client', '_create_identity', '_cs_auth_plugin', '_cs_client', '_cs_exceptions', '_cs_shell', '_environment', '_get_service_endpoint', '_http_debug', '_id_type', '_import_identity', '_logger', '_make_agent_name', '_require_auth', '_safe_region', 'absolute_import', 'auth_with_token', 'authenticate', 'autoscale', 'base_identity', 'clear_credentials', 'client', 'client_class_for_service', 'cloud_blockstorage', 'cloud_databases', 'cloud_dns', 'cloud_loadbalancers', 'cloud_monitoring', 'cloud_networks', 'cloudblockstorage', 'clouddatabases', 'clouddns', 'cloudfiles', 'cloudloadbalancers', 'cloudmonitoring', 'cloudnetworks', 'cloudservers', 'config_file', 'connect_to_autoscale', 'connect_to_cloud_blockstorage', 'connect_to_cloud_databases', 'connect_to_cloud_dns', 'connect_to_cloud_loadbalancers', 'connect_to_cloud_monitoring', 'connect_to_cloud_networks', 'connect_to_cloudfiles', 'connect_to_cloudservers', 'connect_to_images', 'connect_to_queues', 'connect_to_services', 'create_context', 'default_encoding', 'default_region', 'exc', 'exceptions', 'get_encoding', 'get_environment', 'get_http_debug', 'get_setting', 'http', 'identity', 'image', 'images', 'inspect', 'keyring', 'keyring_auth', 'keystone_identity', 'list_environments', 'logging', 'manager', 'object_storage', 'os', 'queueing', 'queues', 'rax_identity', 're', 'regions', 'resource', 'services', 'set_credential_file', 'set_credentials', 'set_default_region', 'set_environment', 'set_http_debug', 'set_setting', 'settings', 'utils', 'version', 'warnings', 'wraps']
>>> import urllib
>>> dir(urllib)
['ContentTooShortError', 'FancyURLopener', 'MAXFTPCACHE', 'URLopener', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__version__', '_asciire', '_ftperrors', '_have_ssl', '_hexdig', '_hextochr', '_hostprog', '_is_unicode', '_localhost', '_noheaders', '_nportprog', '_passwdprog', '_portprog', '_queryprog', '_safe_map', '_safe_quoters', '_tagprog', '_thishost', '_typeprog', '_urlopener', '_userprog', '_valueprog', 'addbase', 'addclosehook', 'addinfo', 'addinfourl', 'always_safe', 'base64', 'basejoin', 'c', 'ftpcache', 'ftperrors', 'ftpwrapper', 'getproxies', 'getproxies_environment', 'i', 'localhost', 'noheaders', 'os', 'pathname2url', 'proxy_bypass', 'proxy_bypass_environment', 'quote', 'quote_plus', 're', 'reporthook', 'socket', 'splitattr', 'splithost', 'splitnport', 'splitpasswd', 'splitport', 'splitquery', 'splittag', 'splittype', 'splituser', 'splitvalue', 'ssl', 'string', 'sys', 'test1', 'thishost', 'time', 'toBytes', 'unquote', 'unquote_plus', 'unwrap', 'url2pathname', 'urlcleanup', 'urlencode', 'urlopen', 'urlretrieve']
>>> import socket
>>> dir(socket)
['AF_APPLETALK', 'AF_ASH', 'AF_ATMPVC', 'AF_ATMSVC', 'AF_AX25', 'AF_BLUETOOTH', 'AF_BRIDGE', 'AF_DECnet', 'AF_ECONET', 'AF_INET', 'AF_INET6', 'AF_IPX', 'AF_IRDA', 'AF_KEY', 'AF_LLC', 'AF_NETBEUI', 'AF_NETLINK', 'AF_NETROM', 'AF_PACKET', 'AF_PPPOX', 'AF_ROSE', 'AF_ROUTE', 'AF_SECURITY', 'AF_SNA', 'AF_TIPC', 'AF_UNIX', 'AF_UNSPEC', 'AF_WANPIPE', 'AF_X25', 'AI_ADDRCONFIG', 'AI_ALL', 'AI_CANONNAME', 'AI_NUMERICHOST', 'AI_NUMERICSERV', 'AI_PASSIVE', 'AI_V4MAPPED', 'BDADDR_ANY', 'BDADDR_LOCAL', 'BTPROTO_HCI', 'BTPROTO_L2CAP', 'BTPROTO_RFCOMM', 'BTPROTO_SCO', 'CAPI', 'EAI_ADDRFAMILY', 'EAI_AGAIN', 'EAI_BADFLAGS', 'EAI_FAIL', 'EAI_FAMILY', 'EAI_MEMORY', 'EAI_NODATA', 'EAI_NONAME', 'EAI_OVERFLOW', 'EAI_SERVICE', 'EAI_SOCKTYPE', 'EAI_SYSTEM', 'EBADF', 'EINTR', 'HCI_DATA_DIR', 'HCI_FILTER', 'HCI_TIME_STAMP', 'INADDR_ALLHOSTS_GROUP', 'INADDR_ANY', 'INADDR_BROADCAST', 'INADDR_LOOPBACK', 'INADDR_MAX_LOCAL_GROUP', 'INADDR_NONE', 'INADDR_UNSPEC_GROUP', 'IPPORT_RESERVED', 'IPPORT_USERRESERVED', 'IPPROTO_AH', 'IPPROTO_DSTOPTS', 'IPPROTO_EGP', 'IPPROTO_ESP', 'IPPROTO_FRAGMENT', 'IPPROTO_GRE', 'IPPROTO_HOPOPTS', 'IPPROTO_ICMP', 'IPPROTO_ICMPV6', 'IPPROTO_IDP', 'IPPROTO_IGMP', 'IPPROTO_IP', 'IPPROTO_IPIP', 'IPPROTO_IPV6', 'IPPROTO_NONE', 'IPPROTO_PIM', 'IPPROTO_PUP', 'IPPROTO_RAW', 'IPPROTO_ROUTING', 'IPPROTO_RSVP', 'IPPROTO_TCP', 'IPPROTO_TP', 'IPPROTO_UDP', 'IPV6_CHECKSUM', 'IPV6_DSTOPTS', 'IPV6_HOPLIMIT', 'IPV6_HOPOPTS', 'IPV6_JOIN_GROUP', 'IPV6_LEAVE_GROUP', 'IPV6_MULTICAST_HOPS', 'IPV6_MULTICAST_IF', 'IPV6_MULTICAST_LOOP', 'IPV6_NEXTHOP', 'IPV6_PKTINFO', 'IPV6_RECVDSTOPTS', 'IPV6_RECVHOPLIMIT', 'IPV6_RECVHOPOPTS', 'IPV6_RECVPKTINFO', 'IPV6_RECVRTHDR', 'IPV6_RECVTCLASS', 'IPV6_RTHDR', 'IPV6_RTHDRDSTOPTS', 'IPV6_RTHDR_TYPE_0', 'IPV6_TCLASS', 'IPV6_UNICAST_HOPS', 'IPV6_V6ONLY', 'IP_ADD_MEMBERSHIP', 'IP_DEFAULT_MULTICAST_LOOP', 'IP_DEFAULT_MULTICAST_TTL', 'IP_DROP_MEMBERSHIP', 'IP_HDRINCL', 'IP_MAX_MEMBERSHIPS', 'IP_MULTICAST_IF', 'IP_MULTICAST_LOOP', 'IP_MULTICAST_TTL', 'IP_OPTIONS', 'IP_RECVOPTS', 'IP_RECVRETOPTS', 'IP_RETOPTS', 'IP_TOS', 'IP_TTL', 'MSG_CTRUNC', 'MSG_DONTROUTE', 'MSG_DONTWAIT', 'MSG_EOR', 'MSG_OOB', 'MSG_PEEK', 'MSG_TRUNC', 'MSG_WAITALL', 'MethodType', 'NETLINK_DNRTMSG', 'NETLINK_FIREWALL', 'NETLINK_IP6_FW', 'NETLINK_NFLOG', 'NETLINK_ROUTE', 'NETLINK_USERSOCK', 'NETLINK_XFRM', 'NI_DGRAM', 'NI_MAXHOST', 'NI_MAXSERV', 'NI_NAMEREQD', 'NI_NOFQDN', 'NI_NUMERICHOST', 'NI_NUMERICSERV', 'PACKET_BROADCAST', 'PACKET_FASTROUTE', 'PACKET_HOST', 'PACKET_LOOPBACK', 'PACKET_MULTICAST', 'PACKET_OTHERHOST', 'PACKET_OUTGOING', 'PF_PACKET', 'RAND_add', 'RAND_egd', 'RAND_status', 'SHUT_RD', 'SHUT_RDWR', 'SHUT_WR', 'SOCK_DGRAM', 'SOCK_RAW', 'SOCK_RDM', 'SOCK_SEQPACKET', 'SOCK_STREAM', 'SOL_HCI', 'SOL_IP', 'SOL_SOCKET', 'SOL_TCP', 'SOL_TIPC', 'SOL_UDP', 'SOMAXCONN', 'SO_ACCEPTCONN', 'SO_ATTACH_FILTER', 'SO_BINDTODEVICE', 'SO_BROADCAST', 'SO_BSDCOMPAT', 'SO_DEBUG', 'SO_DETACH_FILTER', 'SO_DONTROUTE', 'SO_ERROR', 'SO_KEEPALIVE', 'SO_LINGER', 'SO_NO_CHECK', 'SO_OOBINLINE', 'SO_PASSCRED', 'SO_PASSSEC', 'SO_PEERCRED', 'SO_PEERNAME', 'SO_PEERSEC', 'SO_PRIORITY', 'SO_RCVBUF', 'SO_RCVBUFFORCE', 'SO_RCVLOWAT', 'SO_RCVTIMEO', 'SO_REUSEADDR', 'SO_REUSEPORT', 'SO_SECURITY_AUTHENTICATION', 'SO_SECURITY_ENCRYPTION_NETWORK', 'SO_SECURITY_ENCRYPTION_TRANSPORT', 'SO_SNDBUF', 'SO_SNDBUFFORCE', 'SO_SNDLOWAT', 'SO_SNDTIMEO', 'SO_TIMESTAMP', 'SO_TIMESTAMPNS', 'SO_TYPE', 'SSL_ERROR_EOF', 'SSL_ERROR_INVALID_ERROR_CODE', 'SSL_ERROR_SSL', 'SSL_ERROR_SYSCALL', 'SSL_ERROR_WANT_CONNECT', 'SSL_ERROR_WANT_READ', 'SSL_ERROR_WANT_WRITE', 'SSL_ERROR_WANT_X509_LOOKUP', 'SSL_ERROR_ZERO_RETURN', 'SocketType', 'StringIO', 'TCP_CONGESTION', 'TCP_CORK', 'TCP_DEFER_ACCEPT', 'TCP_INFO', 'TCP_KEEPCNT', 'TCP_KEEPIDLE', 'TCP_KEEPINTVL', 'TCP_LINGER2', 'TCP_MAXSEG', 'TCP_MD5SIG', 'TCP_MD5SIG_MAXKEYLEN', 'TCP_NODELAY', 'TCP_QUICKACK', 'TCP_SYNCNT', 'TCP_WINDOW_CLAMP', 'TIPC_ADDR_ID', 'TIPC_ADDR_NAME', 'TIPC_ADDR_NAMESEQ', 'TIPC_CFG_SRV', 'TIPC_CLUSTER_SCOPE', 'TIPC_CONN_TIMEOUT', 'TIPC_CRITICAL_IMPORTANCE', 'TIPC_DEST_DROPPABLE', 'TIPC_HIGH_IMPORTANCE', 'TIPC_IMPORTANCE', 'TIPC_LOW_IMPORTANCE', 'TIPC_MEDIUM_IMPORTANCE', 'TIPC_NODE_SCOPE', 'TIPC_PUBLISHED', 'TIPC_SRC_DROPPABLE', 'TIPC_SUBSCR_TIMEOUT', 'TIPC_SUB_CANCEL', 'TIPC_SUB_PORTS', 'TIPC_SUB_SERVICE', 'TIPC_TOP_SRV', 'TIPC_WAIT_FOREVER', 'TIPC_WITHDRAWN', 'TIPC_ZONE_SCOPE', '_GLOBAL_DEFAULT_TIMEOUT', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '_closedsocket', '_delegate_methods', '_fileobject', '_m', '_realsocket', '_socket', '_socketmethods', '_socketobject', '_ssl', 'create_connection', 'errno', 'error', 'fromfd', 'gaierror', 'getaddrinfo', 'getdefaulttimeout', 'getfqdn', 'gethostbyaddr', 'gethostbyname', 'gethostbyname_ex', 'gethostname', 'getnameinfo', 'getprotobyname', 'getservbyname', 'getservbyport', 'has_ipv6', 'herror', 'htonl', 'htons', 'inet_aton', 'inet_ntoa', 'inet_ntop', 'inet_pton', 'm', 'meth', 'ntohl', 'ntohs', 'os', 'p', 'partial', 'setdefaulttimeout', 'socket', 'socketpair', 'ssl', 'sslerror', 'sys', 'timeout', 'warnings']
```

In my example, I'm going to use the hostname of myhomepc.jtdub.com, which points to 192.168.1.1. While still in the python prompt, I'm going to call the pyrax module to get the {record_id}, which in this example output is id: 'A-2222222'.

```python
>>> import pyrax
>>> pyrax.set_setting('identity_type', 'rackspace')
>>> pyrax.set_credentials('{username}', '{api_key}')
>>> domain = pyrax.cloud_dns.find(name="jtdub.com")
>>> record = domain.get_record('')
>>> print record
<CloudDNSRecord domain_id=0000000, records=[{u'updated': u'2013-07-31T06:17:35.000+0000', u'name': u'www.jtdub.com', u'created': u'2012-06-07T23:56:27.000+0000', u'type': u'A', u'ttl': 300, u'data': u'174.143.185.156', u'id': u'A-0000000'}, {u'updated': u'2013-07-31T06:17:44.000+0000', u'name': u'jtdub.com', u'created': u'2012-06-07T23:58:31.000+0000', u'type': u'A', u'ttl': 300, u'data': u'174.143.185.156', u'id': u'A-1111111'}, {u'updated': u'2014-07-26T21:37:24.000+0000', u'name': u'myhomepc.jtdub.com', u'created': u'2014-07-26T21:37:24.000+0000', u'type': u'A', u'ttl': 300, u'data': u'192.168.1.1', u'id': u'A-2222222'},}], totalEntries=13>
>>>
>>> record = domain.get_record('A-2222222')
>>> print record
<CloudDNSRecord data=192.168.1.1, domain_id=0000000, id=A-2222222, name=myhomepc.jtdub.com, ttl=300, type=A>
```

Replace {username} and {api_key} with your rackspace cloud account username and api key. Now that we have the necessary information, we can edit the variables of the script and run it!

```python
[jtdub@pyrax-test ~]$ git clone https://github.com/jtdub/pyraxDynDNS.git
Cloning into 'pyraxDynDNS'...
remote: Counting objects: 13, done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 13 (delta 3), reused 6 (delta 1)
Unpacking objects: 100% (13/13), done.
[jtdub@pyrax-test ~]$ cd pyraxDynDNS/
[jtdub@pyrax-test pyraxDynDNS]$ vim pyraxDynDNS.py
[jtdub@pyrax-test pyraxDynDNS]$ chmod +x pyraxDynDNS.py
```

Here's my first run of the script. Here you can see that it determines my public IP Address, then determines the DNS A record of my {dyn_domain} hostname. As they are different, it authenticates to the API and makes a call to update the DNS A record of myhomepc.jtdub.com with my current public IP Address.

```bash
[jtdub@pyrax-test pyraxDynDNS]$ ./pyraxDynDNS.py
*** Current IP Address: 240.0.0.1
*** Current IP Address: 240.0.0.1
*** DNS A Record of myhomepc.jtdub.com: 192.168.1.1
*** Username: {username}, API_Key: {api_key}
*** Domain Name: jtdub.com, Record Id: A-2222222
*** Updated IP Address: 240.0.0.1
```

I gave DNS a five minutes to update, then I ran the script again. This time, the script determined that my current public IP Address is the same as my DNS A record of myhomepc.jtdub.com, so it didn't even attempt to authenticate to the API to make any changes.

```bash
[jtdub@pyrax-test pyraxDynDNS]$ ./pyraxDynDNS.py 
*** Current IP Address: 240.0.0.1
*** Current IP Address: 240.0.0.1
*** DNS A Record of myhomepc.jtdub.com: 240.0.0.1
*** 240.0.0.1 is already current for myhomepc.jtdub.com. Nothing to do.
```

Pretty nifty, right? From here, you can put the script into a cron job to run once a day, or however often you want. There you go! Custom dynamic DNS hostname, to access your home PC, using the Rackspace Cloud!

The script can be found on [github](https://github.com/jtdub/pyraxDynDNS).

Here is more information on the [Rackspace SDK](https://developer.rackspace.com/docs/cloud-dns/getting-started/?lang=python)
