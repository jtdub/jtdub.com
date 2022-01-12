---
layout: post
title: OpenNHRP is now available via RPM
date: '2012-10-02'
author: jtdub
tags:
- Linux
- DMVPN
- System Administration
- VPN
- OpenNHRP
- Open Source Alternatives
- RPM
- packetgeek.net
---

After a LONG hiatus, I'm finally starting to work on my Open Source implementation of DMVPN, again. So far, I've started off by taking the [OpenNHRP](http://sourceforge.net/projects/opennhrp/) source code and building RPM files. I made no changes to the source code itself. Heck, I don't even consider myself a developer. I just built the RPM binaries so that a person could build a DMVPN device without needing to have developer tools installed on the device itself. It should be a little more secure that way. :)

Currently, the RPM files are being built in a CentOS 6 x86_64 environment. However, if this is something that people like, I will entertain building the RPM's for 32 bit environment or possibly deb packages for ubuntu / debian based environments.

The binary and source RPM's are available right now! I'm still testing them to make sure everything is working properly.  You can get the package by installing the repository:

```bash
[root@server ~]# curl http://tools.packetgeek.net/pgn.repo -o /etc/yum.repos.d/pgn.repo
[root@server ~]# yum search opennhrp
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: centosmirror.quintex.com
 * extras: centosmirror.quintex.com
 * updates: centosmirror.quintex.com
============================================================ N/S Matched: opennhrp ============================================================
opennhrp.x86_64 : OpenNHRP implements NBMA Next Hop Resolution Protocol (as defined in RFC 2332). It makes it possible to create dynamic
                : multipoint VPN Linux router using NHRP, GRE and IPsec. It aims to be Cisco DMVPN compatible.

  Name and summary matches only, use "search all" for everything.
[root@server ~]# yum install opennhrp
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: centosmirror.quintex.com
 * extras: centosmirror.quintex.com
 * updates: centosmirror.quintex.com
Setting up Install Process
Resolving Dependencies
--> Running transaction check
---> Package opennhrp.x86_64 0:0.13.1-1.el6 will be installed
--> Processing Dependency: libcares.so.2()(64bit) for package: opennhrp-0.13.1-1.el6.x86_64
--> Running transaction check
---> Package c-ares.x86_64 0:1.7.0-6.el6 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

===============================================================================================================================================
 Package                           Arch                            Version                                 Repository                     Size
===============================================================================================================================================
Installing:
 opennhrp                          x86_64                          0.13.1-1.el6                            pgn                            62 k
Installing for dependencies:
 c-ares                            x86_64                          1.7.0-6.el6                             base                           53 k

Transaction Summary
===============================================================================================================================================
Install       2 Package(s)

Total download size: 115 k
Installed size: 230 k
Is this ok [y/N]: y
Downloading Packages:
(1/2): c-ares-1.7.0-6.el6.x86_64.rpm                                                                                    |  53 kB     00:00     
(2/2): opennhrp-0.13.1-1.el6.x86_64.rpm                                                                                 |  62 kB     00:00     
-----------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                          203 kB/s | 115 kB     00:00     
Running rpm_check_debug
Running Transaction Test
Transaction Test Succeeded
Running Transaction
Warning: RPMDB altered outside of yum.
  Installing : c-ares-1.7.0-6.el6.x86_64                                                                                                   1/2 
  Installing : opennhrp-0.13.1-1.el6.x86_64                                                                                                2/2 
  Verifying  : opennhrp-0.13.1-1.el6.x86_64                                                                                                1/2 
  Verifying  : c-ares-1.7.0-6.el6.x86_64                                                                                                   2/2 

Installed:
  opennhrp.x86_64 0:0.13.1-1.el6                                                                                                               

Dependency Installed:
  c-ares.x86_64 0:1.7.0-6.el6                                                                                                                  

Complete!
```

Have fun! I look forward to getting an open source of a DMVPN implementation up and running soon! Leave a comment if you have any comments or questions.
