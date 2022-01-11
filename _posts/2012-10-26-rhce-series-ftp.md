---
layout: post
title: 'RHCE Series: FTP'
date: '2012-10-26'
author: jtdub
tags:
- vsftpd
- Linux
- RHCE Study Notes
- FTP
- packetgeek.net
---

* Configure anonymous-only download.

Install vsftpd: `yum -y install vsftpd`

vsftpd is configured to allow anonymous downloads by default. So you'll need to disable non-anonymous logins.

```bash
[root@server1 vsftpd]# pwd
/etc/vsftpd
[root@server1 vsftpd]# cat vsftpd.conf 
# Example config file /etc/vsftpd/vsftpd.conf
#
# The default compiled in settings are fairly paranoid. This sample file
# loosens things up a bit, to make the ftp daemon more usable.
# Please see vsftpd.conf.5 for all compiled in defaults.
#
# READ THIS: This example file is NOT an exhaustive list of vsftpd options.
# Please read the vsftpd.conf.5 manual page to get a full idea of vsftpd's
# capabilities.
#
# Allow anonymous FTP? (Beware - allowed by default if you comment this out).
anonymous_enable=YES
#
# Uncomment this to allow local users to log in.
local_enable=YES
#
# Uncomment this to enable any form of FTP write command.
write_enable=YES
```

We need to change the highlighted options to NO.

Open the firewall and make persistent at boot.

```bash
iptables -I INPUT -p tcp --dport 21 -j ACCEPT
service iptables save
```

Start vsftpd and make it persistent at boot:

```bash
 service vsftpd start
 chkconfig vsftpd on
```

Let's test out the anonymous ftp. I created a 10MB file in /var/ftp/pub.

```bash
[root@server1 vsftpd]# cd /var/ftp/pub/
[root@server1 pub]# ls
[root@server1 pub]# dd if=/dev/urandom of=data bs=1M count=10
10+0 records in
10+0 records out
10485760 bytes (10 MB) copied, 1.3125 s, 8.0 MB/s
[root@server1 pub]# ls -alh
total 11M
drwxr-xr-x. 2 root root 4.0K Oct 26 23:47 .
drwxr-xr-x. 3 root root 4.0K Oct 26 23:34 ..
-rw-r--r--. 1 root root  10M Oct 26 23:47 data


[root@client1 ~]# ftp 192.168.1.1
Connected to 192.168.1.1 (192.168.1.1).
220 (vsFTPd 2.2.2)
Name (192.168.1.1:root): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
227 Entering Passive Mode (192,168,1,1,223,231).
ftp: connect: No route to host
```

What happened above is that by default the ftp server uses passive ftp mode and the firewall is blocking the > 1024 port that the connection is trying to open.

What we'll need to do is enable ftp connection tracking and make it persistent at boot.

```bash
[root@server1 log]# modprobe -l | grep ftp
kernel/net/netfilter/nf_conntrack_ftp.ko
kernel/net/netfilter/nf_conntrack_tftp.ko
kernel/net/netfilter/ipvs/ip_vs_ftp.ko
kernel/net/ipv4/netfilter/nf_nat_ftp.ko
kernel/net/ipv4/netfilter/nf_nat_tftp.ko
[root@server1 log]# modprobe nf_conntrack_ftp


[root@client1 ~]# ftp 192.168.1.1
Connected to 192.168.1.1 (192.168.1.1).
220 (vsFTPd 2.2.2)
Name (192.168.1.1:root): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
227 Entering Passive Mode (192,168,1,1,163,155).
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Oct 27 04:47 pub
226 Directory send OK.
ftp> cd pub
250 Directory successfully changed.
ftp> ls
227 Entering Passive Mode (192,168,1,1,98,124).
150 Here comes the directory listing.
-rw-r--r--    1 0        0        10485760 Oct 27 04:47 data
226 Directory send OK.
ftp> get data
local: data remote: data
227 Entering Passive Mode (192,168,1,1,232,180).
150 Opening BINARY mode data connection for data (10485760 bytes).
226 Transfer complete.
10485760 bytes received in 0.139 secs (75407.82 Kbytes/sec)
```

To make the changes persistent, you'll need to add an entry in /etc/sysconfig/iptables-config:

```bash
[root@server1 sysconfig]# grep MODULES iptables-config
IPTABLES_MODULES="ip_conntrack_ftp"
IPTABLES_MODULES_UNLOAD="yes"
[root@server1 sysconfig]# service iptables restart
iptables: Flushing firewall rules:                         [  OK  ]
iptables: Setting chains to policy ACCEPT: filter nat      [  OK  ]
iptables: Unloading modules:                               [  OK  ]
iptables: Applying firewall rules:                         [  OK  ]
iptables: Loading additional modules: ip_conntrack_ftp     [  OK  ]
```
