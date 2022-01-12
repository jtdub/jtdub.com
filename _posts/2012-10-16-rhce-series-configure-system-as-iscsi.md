---
layout: post
title: |-
  RHCE Series: Configure a system as an iSCSI initiator that persistently
  mounts an iSCSI target.
date: '2012-10-16'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- ISCSI
- packetgeek.net
---

Creating an iscsi target isn't part of the RHCE objectives, but I'll show my commands here so that you can create your own target for testing.

```bash
[root@server1 ~]# yum -y install scsi-target-utils
Loaded plugins: fastestmirror, refresh-packagekit, security
Loading mirror speeds from cached hostfile
 * base: mirrors.versaweb.com
 * extras: mirror.rackspace.com
 * updates: mirrors.greenmountainaccess.net
....
Installed:
  scsi-target-utils.x86_64 0:1.0.24-2.el6 

Complete!

[root@server1 ~]# dd if=/dev/zero of=/targetfs bs=1M count=512
512+0 records in
512+0 records out
536870912 bytes (537 MB) copied, 15.153 s, 35.4 MB/s

[root@server1 ~]# vim /etc/tgt/targets.conf 
[root@server1 ~]# tail -4 /etc/tgt/targets.conf 

 backing-store /targetfs
 initiator 192.168.101.0/24

[root@server1 ~]# service tgtd start
Starting SCSI target daemon:                               [  OK  ]
[root@server1 ~]# chkconfig tgtd on
[root@server1 ~]# tgtadm --mode target --op show
Target 1: iqn.192.168.101.1.target
    System information:
        Driver: iscsi
        State: ready
    I_T nexus information:
    LUN information:
        LUN: 0
            Type: controller
            SCSI ID: IET     00010000
            SCSI SN: beaf10
            Size: 0 MB, Block size: 1
            Online: Yes
            Removable media: No
            Prevent removal: No
            Readonly: No
            Backing store type: null
            Backing store path: None
            Backing store flags: 
        LUN: 1
            Type: disk
            SCSI ID: IET     00010001
            SCSI SN: beaf11
            Size: 537 MB, Block size: 512
            Online: Yes
            Removable media: No
            Prevent removal: No
            Readonly: Yes
            Backing store type: rdwr
            Backing store path: /targetfs
            Backing store flags: 
    Account information:
    ACL information:
        ALL
```

Once you have your target created. You can get to the actual portion of the RHCE objective. The first thing that you'll need to do is make sure that the iscsi initiator utilities are installed.


```bash
[root@client1 ~]# yum -y install iscsi-initiator-utils
Loaded plugins: fastestmirror, refresh-packagekit, security
Loading mirror speeds from cached hostfile
 * base: centos.mirror.constant.com
 * extras: mirror.trouble-free.net
 * updates: mirror.flhsi.com
...
Running Transaction
  Installing : iscsi-initiator-utils-6.2.0.872-41.el6.x86_64                                                                                                                         1/1 
  Verifying  : iscsi-initiator-utils-6.2.0.872-41.el6.x86_64                                                                                                                         1/1 

Installed:
  iscsi-initiator-utils.x86_64 0:6.2.0.872-41.el6                                                                                                                                        

Complete!
```

Now, you're ready to start playing with iscsi!

```bash
[root@client1 ~]# iscsiadm -m discovery -t sendtargets -p 192.168.101.1
Starting iscsid:                                           [  OK  ]
192.168.101.1:3260,1 iqn.192.168.101.1.target
[root@client1 ~]# chkconfig iscsid --list
iscsid          0:off 1:off 2:off 3:on 4:on 5:on 6:off
```

The iscsid service is controlled by the iscsi service. iscsid controls iscsi communications and iscsi automatically logs in and out of targets.

Once a target is discovered, it will be remembered. You can see your known targets with: `iscsiadm -m node -o show`

```bash
[root@client1 ~]# service iscsi start
Starting iscsi:                                            [  OK  ]
[root@client1 ~]# dmesg | tail -20
libcxgbi:ddp_setup_host_page_size: system PAGE 4096, ddp idx 0.
Chelsio T3 iSCSI Driver cxgb3i v2.0.0 (Jun. 2010)
iscsi: registered transport (cxgb3i)
Chelsio T4 iSCSI Driver cxgb4i v0.9.1 (Aug. 2010)
iscsi: registered transport (cxgb4i)
cnic: Broadcom NetXtreme II CNIC Driver cnic v2.5.10 (March 21, 2012)
Broadcom NetXtreme II iSCSI Driver bnx2i v2.7.2.2 (Apr 26, 2012)
iscsi: registered transport (bnx2i)
iscsi: registered transport (be2iscsi)
scsi2 : iSCSI Initiator over TCP/IP
scsi 2:0:0:0: RAID              IET      Controller       0001 PQ: 0 ANSI: 5
scsi 2:0:0:1: Direct-Access     IET      VIRTUAL-DISK     0001 PQ: 0 ANSI: 5
sd 2:0:0:1: [sda] 1048576 512-byte logical blocks: (536 MB/512 MiB)
sd 2:0:0:1: [sda] Write Protect is on
sd 2:0:0:1: [sda] Mode Sense: 49 00 80 08
sd 2:0:0:1: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
 sda: unknown partition table
sd 2:0:0:1: [sda] Attached SCSI disk
scsi 2:0:0:0: Attached scsi generic sg0 type 12
sd 2:0:0:1: Attached scsi generic sg1 type 0
[root@client1 ~]# chkconfig iscsi on
```

To make sure that your iscsi drives are mounted persistent on each boot, you'll need to make sure that the iscsi service starts at boot.

As you can see, my iscsi presented drive is sda. From here, the drive is handled just like you would any other drive - fdisk, mkfs, mount, and add it to the /etc/fstab.

```bash
root@client1 ~]# fdisk -l /dev/sda

Disk /dev/sda: 536 MB, 536870912 bytes
17 heads, 61 sectors/track, 1011 cylinders
Units = cylinders of 1037 * 512 = 530944 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000
```
