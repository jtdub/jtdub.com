---
layout: post
title: SELinux - Listing Available Contexts
date: '2012-10-29'
author: jtdub
tags:
- SELinux
- Linux
- RHCE Study Notes
- packetgeek.net
---

As you know, I've been studying for the RHCE exam. One of the things that I was unsure about with SELinux was how to find all the available contexts. It's easy to find booleans with the 'getsebool' command, but what about a context?

```bash
[root@sgnhv ~]# ls -Z /var/lib/ | grep virt
drwxr-xr-x. root    root    system_u:object_r:virt_var_lib_t:s0 libvirt
```

There are TONS of contexts. Today, I found my answer. It's the 'seinfo' command.

```bash
[root@sgnhv ~]# yum provides "*/seinfo"
Loaded plugins: fastestmirror, refresh-packagekit, security
Determining fastest mirrors
epel/metalink                                                                                                                                                 |  13 kB     00:00     
 * base: bay.uchicago.edu
 * epel: www.gtlib.gatech.edu
 * extras: mirrors.easynews.com
 * updates: centosmirror.quintex.com
base                                                                                                                                                          | 3.7 kB     00:00     
epel                                                                                                                                                          | 4.3 kB     00:00     
extras                                                                                                                                                        | 3.5 kB     00:00     
updates                                                                                                                                                       | 3.5 kB     00:00     
setools-console-3.3.7-4.el6.x86_64 : Policy analysis command-line tools for SELinux
Repo        : base
Matched from:
Filename    : /usr/bin/seinfo
[root@sgnhv ~]# yum install setools-console
...
Installed:
  setools-console.x86_64 0:3.3.7-4.el6 
[root@sgnhv ~]# seinfo -t | grep samba
   samba_secrets_t
   samba_unconfined_script_exec_t
   samba_net_t
   samba_var_t
   samba_net_exec_t
   samba_net_tmp_t
   samba_unconfined_net_t
   samba_unconfined_script_t
   sambagui_exec_t
   samba_share_t
   samba_initrc_exec_t
   sambagui_t
   samba_etc_t
   samba_log_t
```
