---
layout: post
title: Linux File Server for Apple Time Machine Backups
date: '2013-02-04'
author: jtdub
tags:
- Linux
- netatalk
- afp
- Apple TimeMachine
- packetgeek.net
---

I got Apple Time Machine backups working with my Linux file server. Apple allows you to perform backups over the network utilizing the AFP (Apple Filing Protocol), via the Time Machine app. There is an open source implementation of afp in the netatalk package. Here is a quick and dirty run down of how I configured netatalk to work as my storage location for my apple backups.

```bash
[root@sgnhv ~]# cd /etc/netatalk/
[root@sgnhv netatalk]# for i in afpd.conf AppleVolumes.default; do echo "### $i ####"; grep -v ^# $i | grep -v ^$; done
### afpd.conf ####
- -mimicmodel TimeCapsule6,106 -setuplog "default log_warn /var/log/afpd.log"
[Global]
mimic model = TimeCapsule6,106
log level = default:warn
log file = /var/log/afpd.log
hosts allow = 172.16.1.0/24
[TimeMachine]
path = /timemachine
valid users = jtdubb
time machine = yes
### AppleVolumes.default ####
:DEFAULT: options:upriv,usedots
/timemachine	TimeMachine	allow:jtdubb options:usedots,upriv,tm

[root@sgnhv netatalk]# history | egrep 'afppasswd|chkconfig netatalk|service netatalk'
  786  service netatalk restart
  795  afppasswd -a jtdubb
  867  chkconfig netatalk on
```

As you can see, the configuration is similar to a samba configuration, with a couple minor exceptions.

[http://netatalk.sourceforge.net/](http://netatalk.sourceforge.net/)
