---
layout: post
title: 'RHCE Series: Configure the service to start when the system is booted.'
date: '2012-10-25'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- packetgeek.net
---

```bash
[root@server1 ~]# chkconfig --list httpd
httpd           0:off 1:off 2:off 3:off 4:off 5:off 6:off
[root@server1 ~]# chkconfig --level 345 httpd on
[root@server1 ~]# chkconfig --list httpd
httpd           0:off 1:off 2:off 3:on 4:on 5:on 6:off
[root@server1 ~]# chkconfig --level 345 httpd off
[root@server1 ~]# chkconfig --list httpd
httpd           0:off 1:off 2:off 3:off 4:off 5:off 6:off
[root@server1 ~]# chkconfig httpd off
[root@server1 ~]# chkconfig --list httpd
httpd           0:off 1:off 2:off 3:off 4:off 5:off 6:off
[root@server1 ~]# chkconfig --list
auditd          0:off 1:off 2:on 3:on 4:on 5:on 6:off
crond           0:off 1:off 2:on 3:on 4:on 5:on 6:off
httpd           0:off 1:off 2:off 3:off 4:off 5:off 6:off
ip6tables       0:off 1:off 2:on 3:on 4:on 5:on 6:off
iptables        0:off 1:off 2:on 3:on 4:on 5:on 6:off
lvm2-monitor    0:off 1:on 2:on 3:on 4:on 5:on 6:off
named           0:off 1:off 2:off 3:off 4:off 5:off 6:off
netconsole      0:off 1:off 2:off 3:off 4:off 5:off 6:off
netfs           0:off 1:off 2:off 3:on 4:on 5:on 6:off
network         0:off 1:off 2:on 3:on 4:on 5:on 6:off
portreserve     0:off 1:off 2:on 3:on 4:on 5:on 6:off
postfix         0:off 1:off 2:on 3:on 4:on 5:on 6:off
rdisc           0:off 1:off 2:off 3:off 4:off 5:off 6:off
restorecond     0:off 1:off 2:off 3:off 4:off 5:off 6:off
rsyslog         0:off 1:off 2:on 3:on 4:on 5:on 6:off
saslauthd       0:off 1:off 2:off 3:off 4:off 5:off 6:off
sshd            0:off 1:off 2:on 3:on 4:on 5:on 6:off
svnserve        0:off 1:off 2:off 3:off 4:off 5:off 6:off
sysstat         0:off 1:on 2:on 3:on 4:on 5:on 6:off
udev-post       0:off 1:on 2:on 3:on 4:on 5:on 6:off
xinetd          0:off 1:off 2:off 3:off 4:off 5:off 6:off
```
