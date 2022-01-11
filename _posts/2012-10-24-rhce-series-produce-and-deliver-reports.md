---
layout: post
title: 'RHCE Series: Produce and deliver reports on system utilization'
date: '2012-10-24'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- System Administration
- packetgeek.net
---

The sysstat package provides several utilities for system monitoring and generating reports based upon system utilization.

```bash
[root@server1 ~]# yum -y install sysstat

....

Installed:
  sysstat.x86_64 0:9.0.4-20.el6                                                                                             

Complete!

[root@server1 ~]# rpm -qi sysstat
Name        : sysstat                      Relocations: (not relocatable)
Version     : 9.0.4                             Vendor: CentOS
Release     : 20.el6                        Build Date: Fri 22 Jun 2012 05:12:35 AM CDT
Install Date: Thu 25 Oct 2012 08:35:39 AM CDT      Build Host: c6b7.bsys.dev.centos.org
Group       : Applications/System           Source RPM: sysstat-9.0.4-20.el6.src.rpm
Size        : 826040                           License: GPLv2+
Signature   : RSA/SHA1, Sun 24 Jun 2012 05:19:23 PM CDT, Key ID 0946fca2c105b9de
Packager    : CentOS BuildSystem <http: bugs.centos.org="bugs.centos.org">
URL         : http://perso.orange.fr/sebastien.godard/
Summary     : The sar and iostat system monitoring commands
Description :
This package provides the sar and iostat commands for Linux. Sar and
iostat enable system monitoring of disk, network, and other IO
activity.
[root@server1 ~]# rpm -ql sysstat
/etc/cron.d/sysstat
/etc/rc.d/init.d/sysstat
/etc/sysconfig/sysstat
/etc/sysconfig/sysstat.ioconf
/usr/bin/cifsiostat
/usr/bin/iostat
/usr/bin/mpstat
/usr/bin/pidstat
/usr/bin/sadf
/usr/bin/sar
/usr/lib64/sa
/usr/lib64/sa/sa1
/usr/lib64/sa/sa2
/usr/lib64/sa/sadc
/usr/share/doc/sysstat-9.0.4
/usr/share/doc/sysstat-9.0.4/CHANGES
/usr/share/doc/sysstat-9.0.4/COPYING
/usr/share/doc/sysstat-9.0.4/CREDITS
/usr/share/doc/sysstat-9.0.4/FAQ
/usr/share/doc/sysstat-9.0.4/README
/usr/share/doc/sysstat-9.0.4/TODO
/usr/share/locale/af/LC_MESSAGES/sysstat.mo
/usr/share/locale/da/LC_MESSAGES/sysstat.mo
/usr/share/locale/de/LC_MESSAGES/sysstat.mo
/usr/share/locale/es/LC_MESSAGES/sysstat.mo
/usr/share/locale/fi/LC_MESSAGES/sysstat.mo
/usr/share/locale/fr/LC_MESSAGES/sysstat.mo
/usr/share/locale/id/LC_MESSAGES/sysstat.mo
/usr/share/locale/it/LC_MESSAGES/sysstat.mo
/usr/share/locale/ja/LC_MESSAGES/sysstat.mo
/usr/share/locale/ky/LC_MESSAGES/sysstat.mo
/usr/share/locale/lv/LC_MESSAGES/sysstat.mo
/usr/share/locale/mt/LC_MESSAGES/sysstat.mo
/usr/share/locale/nb/LC_MESSAGES/sysstat.mo
/usr/share/locale/nl/LC_MESSAGES/sysstat.mo
/usr/share/locale/nn/LC_MESSAGES/sysstat.mo
/usr/share/locale/pl/LC_MESSAGES/sysstat.mo
/usr/share/locale/pt/LC_MESSAGES/sysstat.mo
/usr/share/locale/pt_BR/LC_MESSAGES/sysstat.mo
/usr/share/locale/ro/LC_MESSAGES/sysstat.mo
/usr/share/locale/ru/LC_MESSAGES/sysstat.mo
/usr/share/locale/sk/LC_MESSAGES/sysstat.mo
/usr/share/locale/sv/LC_MESSAGES/sysstat.mo
/usr/share/locale/vi/LC_MESSAGES/sysstat.mo
/usr/share/locale/zh_CN/LC_MESSAGES/sysstat.mo
/usr/share/locale/zh_TW/LC_MESSAGES/sysstat.mo
/usr/share/man/man1/cifsiostat.1.gz
/usr/share/man/man1/iostat.1.gz
/usr/share/man/man1/mpstat.1.gz
/usr/share/man/man1/pidstat.1.gz
/usr/share/man/man1/sadf.1.gz
/usr/share/man/man1/sar.1.gz
/usr/share/man/man8/sa1.8.gz
/usr/share/man/man8/sa2.8.gz
/usr/share/man/man8/sadc.8.gz
/var/log/sa

[root@server1 ~]# iostat
Linux 2.6.32-279.el6.x86_64 (server1.sgn.local)  10/25/2012  _x86_64_ (1 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.01    0.00    0.01    0.23    0.00   99.76

Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
sda               0.00         0.12         0.12     244551     239834
vda               0.11         0.22         1.39     455274    2848540
dm-0              0.18         0.21         1.39     439698    2848448
dm-1              0.00         0.00         0.00       3952          0

[root@server1 ~]# mpstat 
Linux 2.6.32-279.el6.x86_64 (server1.sgn.local)  10/25/2012  _x86_64_ (1 CPU)

08:39:18 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest   %idle
08:39:18 AM  all    0.01    0.00    0.01    0.23    0.00    0.00    0.00    0.00   99.76
[root@server1 ~]# pidstat
Linux 2.6.32-279.el6.x86_64 (server1.sgn.local)  10/25/2012  _x86_64_ (1 CPU)

08:39:28 AM       PID    %usr %system  %guest    %CPU   CPU  Command
08:39:28 AM         1    0.00    0.00    0.00    0.00     0  init
08:39:28 AM         4    0.00    0.00    0.00    0.00     0  ksoftirqd/0
08:39:28 AM         6    0.00    0.00    0.00    0.00     0  watchdog/0
08:39:28 AM         7    0.00    0.00    0.00    0.00     0  events/0
08:39:28 AM        13    0.00    0.00    0.00    0.00     0  sync_supers
08:39:28 AM        14    0.00    0.00    0.00    0.00     0  bdi-default
08:39:28 AM        16    0.00    0.00    0.00    0.00     0  kblockd/0
08:39:28 AM        23    0.00    0.00    0.00    0.00     0  khubd
08:39:28 AM        24    0.00    0.00    0.00    0.00     0  kseriod
08:39:28 AM        27    0.00    0.00    0.00    0.00     0  khungtaskd
08:39:28 AM        28    0.00    0.00    0.00    0.00     0  kswapd0
08:39:28 AM       354    0.00    0.00    0.00    0.00     0  kdmflush
08:39:28 AM       375    0.00    0.00    0.00    0.00     0  jbd2/dm-0-8
08:39:28 AM       450    0.00    0.00    0.00    0.00     0  udevd
08:39:28 AM       853    0.00    0.00    0.00    0.00     0  kauditd
08:39:28 AM      1013    0.00    0.00    0.00    0.00     0  flush-253:0
08:39:28 AM      1071    0.00    0.00    0.00    0.00     0  auditd
08:39:28 AM      1096    0.00    0.00    0.00    0.00     0  rsyslogd
08:39:28 AM      1130    0.00    0.00    0.00    0.00     0  sshd
08:39:28 AM      1207    0.00    0.00    0.00    0.00     0  master
08:39:28 AM      1216    0.00    0.00    0.00    0.00     0  qmgr
08:39:28 AM      1217    0.00    0.00    0.00    0.00     0  crond
08:39:28 AM      1230    0.00    0.00    0.00    0.00     0  mingetty
08:39:28 AM      1542    0.00    0.00    0.00    0.00     0  dmeventd
08:39:28 AM     21155    0.00    0.00    0.00    0.00     0  xinetd
08:39:28 AM     25169    0.00    0.00    0.00    0.00     0  sshd
08:39:28 AM     25173    0.00    0.00    0.00    0.00     0  bash
08:39:28 AM     25223    0.00    0.00    0.00    0.00     0  pickup
08:39:28 AM     25237    0.00    0.00    0.00    0.00     0  pidstat

[root@server1 ~]# man sar

       count  records at interval second intervals. If the count parameter is not set, all the records saved in
       the file will be selected.  Collection of data in this manner is useful  to  characterize  system  usage
       over a period of time and determine peak usage hours.

       Note:     The sar command only reports on local activities.

</http:>
```
