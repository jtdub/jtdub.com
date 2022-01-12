---
layout: post
title: Logical Volume Management in Linux
date: '2012-10-01'
author: jtdub
tags:
- Linux
- Filesystems
- System Administration
- LVM
- packetgeek.net
---

LVM is a very powerful file system administration tool in Linux. It provides you with the ability to create, extend, resize, and even take snapshots of disk space on live systems. Here are my notes.  I created a new hard drive within my test VM. When the server booted, it sees the new drive as /dev/sda. The disk that's in use by Linux is /dev/vda.  To start, we'll need to partition /dev/sda. Note that you can only have four primary partitions on a single hard drive. Once you reach four primary partitions, if there is any space left on the disk, it will be unusable. Therefore, if you have a couple primary partitions, it's best to start using logical partitions.

```bash
[root@server1 ~]# fdisk -l | more

Disk /dev/sda: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000


Disk /dev/vda: 8589 MB, 8589934592 bytes
16 heads, 63 sectors/track, 16644 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x000a2c27

   Device Boot      Start         End      Blocks   Id  System
/dev/vda1   *           3        1018      512000   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/vda2            1018       16645     7875584   8e  Linux LVM
Partition 2 does not end on cylinder boundary.

Disk /dev/mapper/VolGroup-lv_root: 7021 MB, 7021264896 bytes
255 heads, 63 sectors/track, 853 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000


Disk /dev/mapper/VolGroup-lv_swap: 1040 MB, 1040187392 bytes
255 heads, 63 sectors/track, 126 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000
```

I then created a new 2GB primary partition on /dev/sda. This new primary partition is listed as a "Linux LVM" partition type Linux will see the partition as /dev/sda1. That leaves 6GB of free space in /dev/sda.

```bash
[root@server1 ~]# fdisk /dev/sda
Device contains neither a valid DOS partition table, nor Sun, SGI or OSF disklabel
Building a new DOS disklabel with disk identifier 0xf1c3811e.
Changes will remain in memory only, until you decide to write them.
After that, of course, the previous content won't be recoverable.

Warning: invalid flag 0x0000 of partition table 4 will be corrected by w(rite)

WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
         switch off the mode (command 'c') and change display units to
         sectors (command 'u').

Command (m for help): p

Disk /dev/sda: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0xf1c3811e

   Device Boot      Start         End      Blocks   Id  System

Command (m for help): n
Command action
   e   extended
   p   primary partition (1-4)
p
Partition number (1-4): 1
First cylinder (1-1044, default 1): 
Using default value 1
Last cylinder, +cylinders or +size{K,M,G} (1-1044, default 1044): +2G

Command (m for help): p

Disk /dev/sda: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0xf1c3811e

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1               1         262     2104483+  83  Linux

Command (m for help): t
Selected partition 1
Hex code (type L to list codes): 8e
Changed system type of partition 1 to 8e (Linux LVM)

Command (m for help): p

Disk /dev/sda: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0xf1c3811e

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1               1         262     2104483+  8e  Linux LVM

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

Before I start, I'm going to run the pvs, vgs, and lvs commands so that you can see that I haven't modified anything, yet. Then I'll add my /dev/sda1 to a "Physical Volume".

```bash
root@server1 ~]# pvs
  PV         VG       Fmt  Attr PSize PFree
  /dev/vda2  VolGroup lvm2 a--  7.51g    0 
[root@server1 ~]# vgs
  VG       #PV #LV #SN Attr   VSize VFree
  VolGroup   1   2   0 wz--n- 7.51g    0 
[root@server1 ~]# lvs
  LV      VG       Attr     LSize   Pool Origin Data%  Move Log Copy%  Convert
  lv_root VolGroup -wi-ao--   6.54g                                           
  lv_swap VolGroup -wi-ao-- 992.00m                                           
[root@server1 ~]# ls /dev/sda1
/dev/sda1
[root@server1 ~]# pvcreate /dev/sda1
  Writing physical volume data to disk "/dev/sda1"
  Physical volume "/dev/sda1" successfully created
```

Now is where you have to make your first decision. Do you want to create a new "Volume Group" or add the new drive to an existing "Volume Group". Both commands are simple. Creating a new volume group utilizes the vgcreate command, whereas extending the phsyical drive to an existing volume uses the vgextend command.

To be able to show both methods, I first extended the physical volume into an existing volume group via the vgextend command. I then removed the the physical volume from the volume group so that I could demostrate creating a new volume group. You don't need to run through both commands. It's just a decision that you need to make when you're creating your volumes.

```bash
root@server1 ~]# vgs
  VG       #PV #LV #SN Attr   VSize VFree
  VolGroup   1   2   0 wz--n- 7.51g    0 
[root@server1 ~]# vgextend VolGroup /dev/sda1
  Volume group "VolGroup" successfully extended
[root@server1 ~]# vgs
  VG       #PV #LV #SN Attr   VSize VFree
  VolGroup   2   2   0 wz--n- 9.51g 2.00g
[root@server1 ~]# vgreduce -A y VolGroup /dev/sda1
  Removed "/dev/sda1" from volume group "VolGroup"
[root@server1 ~]# vgcreate VolGroup01 /dev/sda1
  Volume group "VolGroup01" successfully created
[root@server1 ~]# vgs
  VG         #PV #LV #SN Attr   VSize VFree
  VolGroup     1   2   0 wz--n- 7.51g    0 
  VolGroup01   1   0   0 wz--n- 2.00g 2.00g
```

From here on, I'll continue with the new volume group "VolGroup01". After we have extended or created a new volume group, we'll need to create the actual logical volume. That includes needing to made a decision on the name of the volume, as well as the size of the volume. For this test, I'm going to create a volume called data and make it 1GB. That will leave 1GB for expansion or new volumes.

```bash
[root@server1 ~]# lvcreate -n data -L 1G VolGroup01
  Logical volume "data" created
[root@server1 ~]# pvs
  PV         VG         Fmt  Attr PSize PFree
  /dev/sda1  VolGroup01 lvm2 a--  2.00g 1.00g
  /dev/vda2  VolGroup   lvm2 a--  7.51g    0 
[root@server1 ~]# vgs
  VG         #PV #LV #SN Attr   VSize VFree
  VolGroup     1   2   0 wz--n- 7.51g    0 
  VolGroup01   1   1   0 wz--n- 2.00g 1.00g
[root@server1 ~]# lvs
  LV      VG         Attr     LSize   Pool Origin Data%  Move Log Copy%  Convert
  lv_root VolGroup   -wi-ao--   6.54g                                           
  lv_swap VolGroup   -wi-ao-- 992.00m                                           
  data    VolGroup01 -wi-a---   1.00g 
```

Once that is completed. You can create a file system, mount it, and start writing data to it.

```bash
[root@server1 ~]# mkfs -t ext4 /dev/VolGroup01/data 
mke2fs 1.41.12 (17-May-2010)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
65536 inodes, 262144 blocks
13107 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=268435456
8 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
 32768, 98304, 163840, 229376

Writing inode tables: done                            
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done

This filesystem will be automatically checked every 39 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.
[root@server1 ~]# mkdir /data
[root@server1 ~]# mount /dev/VolGroup01/data /data/
[root@server1 ~]# df -h
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/VolGroup-lv_root
                      6.5G  830M  5.3G  14% /
tmpfs                 246M     0  246M   0% /dev/shm
/dev/vda1             485M   32M  429M   7% /boot
/dev/mapper/VolGroup01-data
                     1008M   34M  924M   4% /data
[root@server1 ~]# dd if=/dev/urandom of=/data/somefile bs=1M count=20
20+0 records in
20+0 records out
20971520 bytes (21 MB) copied, 2.44909 s, 8.6 MB/s
[root@server1 ~]# md5sum /data/somefile > /data/somefile.md5sum
[root@server1 ~]# cat /data/somefile.md5sum 
9437503c5996490b3518861e4d3754a7  /data/somefile
```

Now let's say that I wanted to resize the volume. That could be done with the lvresize, lvextend, or lvreduce commands. Depending on what exactly you're wanting to do, but the lvresize is generally a better universal command as it will allow you to make the volume larger as well as shrink the volume. Shrinking a volume can be tricky, particularly if you have data on it. It's always a best practice to fensure that you have a proper backup of the volume, before you resize it. One of the switches with the lvresize command that will make life easier is the '-r' switch, which is the resize2fs, switch. When this switch is enabled, it will unmount the volume, which is needed to shrink the volume, but not extend the volume. It will also run a file system check on the volume and make sure that no data will get lost somewhere in translation, and remount the volume. Just be prepared to execute a restore if the process fails.

```bash
[root@server1 ~]# lvresize --help
  lvresize: Resize a logical volume

lvresize
 [-A|--autobackup y|n]
 [--alloc AllocationPolicy]
 [-d|--debug]
 [-f|--force]
 [-h|--help]
 [-i|--stripes Stripes [-I|--stripesize StripeSize]]
 {-l|--extents [+|-]LogicalExtentsNumber[%{VG|LV|PVS|FREE|ORIGIN}] |
  -L|--size [+|-]LogicalVolumeSize[bBsSkKmMgGtTpPeE]}
 [-n|--nofsck]
 [--noudevsync]
 [-r|--resizefs]
 [-t|--test]
 [--type VolumeType]
 [-v|--verbose]
 [--version]
 LogicalVolume[Path] [ PhysicalVolumePath... ]

[root@server1 ~]# lvresize -r -L -500M /dev/VolGroup01/data 
Do you want to unmount "/data"? [Y|n] y
fsck from util-linux-ng 2.17.2
/dev/mapper/VolGroup01-data: 13/65536 files (7.7% non-contiguous), 17756/262144 blocks
resize2fs 1.41.12 (17-May-2010)
Resizing the filesystem on /dev/mapper/VolGroup01-data to 134144 (4k) blocks.
The filesystem on /dev/mapper/VolGroup01-data is now 134144 blocks long.

  Reducing logical volume data to 524.00 MiB
  Logical volume data successfully resized
[root@server1 ~]# df -h /data
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/VolGroup01-data
                      514M   53M  435M  11% /data
[root@server1 ~]# ls /data/
lost+found  somefile  somefile.md5sum
[root@server1 ~]# md5sum /data/somefile
9437503c5996490b3518861e4d3754a7  /data/somefile
[root@server1 ~]# cat /data/somefile.md5sum 
9437503c5996490b3518861e4d3754a7  /data/somefile

[root@server1 ~]# lvresize -r -l +100%FREE /dev/VolGroup01/data 
  Extending logical volume data to 2.00 GiB
  Logical volume data successfully resized
resize2fs 1.41.12 (17-May-2010)
Filesystem at /dev/mapper/VolGroup01-data is mounted on /data; on-line resizing required
old desc_blocks = 1, new_desc_blocks = 1
Performing an on-line resize of /dev/mapper/VolGroup01-data to 525312 (4k) blocks.
The filesystem on /dev/mapper/VolGroup01-data is now 525312 blocks long.

[root@server1 ~]# md5sum /data/somefile
9437503c5996490b3518861e4d3754a7  /data/somefile
[root@server1 ~]# cat /data/somefile.md5sum 
9437503c5996490b3518861e4d3754a7  /data/somefile
```

As you can see, I shrunk the volume by 500M, verified that the data remained in tact and then grew the volume to the full space (extents) remaining. One of the gotchas with shrinking a volume is to make sure that nothing is accessing the volume that you want to shrink. You can accomplish this with the lsof command. If there are applications or people accessing the volume, you'll need to either stop the application or get the person to leave the volume as their working directory.

One of the other cool features with LVM is being able to take snapshots. This can be accomplished with the lvcreate command in conjunction with the '-s' switch. You will need to have sufficiant space within your volume group to accomplish this.

```bash
[root@server1 ~]# lvcreate -s /dev/VolGroup01/data -L 250M -n data-snapshot
  Rounding up size to full physical extent 252.00 MiB
  Volume group "VolGroup01" has insufficient free space (0 extents): 63 required.
[root@server1 ~]# vgs
  VG         #PV #LV #SN Attr   VSize VFree
  VolGroup     1   2   0 wz--n- 7.51g    0 
  VolGroup01   1   1   0 wz--n- 2.00g    0 
[root@server1 ~]# lvresize -r -L 1GB /dev/VolGroup01/data 
Do you want to unmount "/data"? [Y|n] y
fsck from util-linux-ng 2.17.2
/dev/mapper/VolGroup01-data: 13/139264 files (15.4% non-contiguous), 22448/525312 blocks
resize2fs 1.41.12 (17-May-2010)
Resizing the filesystem on /dev/mapper/VolGroup01-data to 262144 (4k) blocks.
The filesystem on /dev/mapper/VolGroup01-data is now 262144 blocks long.

  Reducing logical volume data to 1.00 GiB
  Logical volume data successfully resized
[root@server1 ~]# lvs
  LV      VG         Attr     LSize   Pool Origin Data%  Move Log Copy%  Convert
  lv_root VolGroup   -wi-ao--   6.54g                                           
  lv_swap VolGroup   -wi-ao-- 992.00m                                           
  data    VolGroup01 -wi-ao--   1.00g                                           
[root@server1 ~]# lvcreate -s /dev/VolGroup01/data -L 250M -n data-snapshot
  Rounding up size to full physical extent 252.00 MiB
  Logical volume "data-snapshot" created
[root@server1 ~]# lvs
  LV            VG         Attr     LSize   Pool Origin Data%  Move Log Copy%  Convert
  lv_root       VolGroup   -wi-ao--   6.54g                                           
  lv_swap       VolGroup   -wi-ao-- 992.00m                                           
  data          VolGroup01 owi-aos-   1.00g                                           
  data-snapshot VolGroup01 swi-a-s- 252.00m      data     0.00                        
[root@server1 ~]# mount /dev/VolGroup01/data-snapshot /mnt/
[root@server1 ~]# md5sum /mnt/somefile
9437503c5996490b3518861e4d3754a7  /mnt/somefile
[root@server1 ~]# md5sum /data/somefile
9437503c5996490b3518861e4d3754a7  /data/somefile
```

As you can see, since I had previously extended the volume to encompass the full space, I had no space left over on the volume group. I then needed to reduce the size of the logical volume to make space available in the volume group for the snapshot creation.
