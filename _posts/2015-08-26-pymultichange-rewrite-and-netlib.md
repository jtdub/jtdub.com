---
layout: post
title: pyMultiChange rewrite and Netlib
date: '2015-08-26'
author: jtdub
tags:
- Cisco Administration Python Scripting
- Python Tips
- packetgeek.net
---

I re-wrote '[pyMultiChange](https://github.com/jtdub/pyMultiChange)' around my new library for connecting and managing devices. Before I was using 'pyRouterLib', but now I've deprecated that library with the creation of my new library '[netlib](https://github.com/jtdub/netlib)'.

Netlib is super easy to use and is more complete than [pyRouterLib](https://github.com/jtdub/pyRouterLib) was. Utilizing Netlib, allowed me to cut the code in pyMultiChange by almost half and netlib is more flexible and user friendly.

To use netlib, first clone the git repo and install the necessary python libraries:

```bash
git clone https://github.com/jtdub/netlib.git
cd netlib
sudo pip install -r requirements.txt
sudo python setup.py install
```

After that, you're ready to go. Accessing network devices via telnet and ssh are currently supported. Both have a very similar API syntax, that is layed out in the README on github.

Here is an example of how to use the ssh module:

```python
$ python
>>> from netlib.conn_type import SSH
>>> conn = SSH('core1a', username='******', password='******')
>>> conn.connect()
'\r\ncore1a.sat>'
>>> conn.set_enable(enable_password='******')
'\r\ncore1a.sat#'
>>> conn.disable_paging()
>>> print(conn.command('show version'))
show version
Cisco IOS Software, C3750 Software (C3750-IPSERVICESK9-M), Version 12.2(55)SE9, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Mon 03-Mar-14 22:45 by prod_rel_team
Image text-base: 0x01000000, data-base: 0x02F00000

ROM: Bootstrap program is C3750 boot loader
BOOTLDR: C3750 Boot Loader (C3750-HBOOT-M) Version 12.2(44)SE5, RELEASE SOFTWARE (fc1)

core1a.sat uptime is 9 weeks, 5 days, 2 hours, 17 minutes
System returned to ROM by power-on
System restarted at 20:25:45 CST Fri Jun 19 2015
System image file is "flash:c3750-ipservicesk9-mz.122-55.SE9.bin"


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

cisco WS-C3750-24TS (PowerPC405) processor (revision L0) with 131072K bytes of memory.
Processor board ID CAT1042ZGKL
Last reset from power-on
6 Virtual Ethernet interfaces
24 FastEthernet interfaces
2 Gigabit Ethernet interfaces
The password-recovery mechanism is enabled.

512K bytes of flash-simulated non-volatile configuration memory.
Base ethernet MAC Address       : 00:19:E7:5F:8F:80
Motherboard assembly number     : 73-9677-10
Power supply part number        : 341-0034-01
Motherboard serial number       : CAT10415NLR
Power supply serial number      : DTH1037117A
Model revision number           : L0
Motherboard revision number     : A0
Model number                    : WS-C3750-24TS-S
System serial number            : CAT1042ZGKL
Top Assembly Part Number        : 800-25857-02
Top Assembly Revision Number    : D0
Version ID                      : V05
CLEI Code Number                : CNMV100CRE
Hardware Board Revision Number  : 0x01


Switch Ports Model              SW Version            SW Image                 
------ ----- -----              ----------            ----------               
*    1 26    WS-C3750-24TS      12.2(55)SE9           C3750-IPSERVICESK9-M     


Configuration register is 0xF

core1a.sat#
>>> conn.close()
```

How easy is that? I'm stoked about netlib. It should make rapidly creating code for interact with network devices pretty trivial. I'm experimenting with SNMP functionality, though it's not ready for prime time.

I also have a method for storing and reading user credentials, so that they don't have to be stored in the script, called every time a script is run, or entered manually for every device that is accessed.

Let me know what you think, add feature requests, or do a pull request. :)
