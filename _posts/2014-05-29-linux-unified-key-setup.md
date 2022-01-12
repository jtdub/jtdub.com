---
layout: post
title: Linux Unified Key Setup
date: '2014-05-29'
author: jtdub
tags:
- LUKS
- Encryption
- packetgeek.net
---

Here are some notes that I took about setting up LUKS when studying for the RHCSA. I felt that this would be appropriate to post after the recent issues with [TrueCrypt](http://truecrypt.sourceforge.net/).

#### Disk Encryption
* LUKS - Linux Unified Key Setup
  * Create a new LUKS encrypted device:
    * cryptsetup luksFormat <device>
  * Establish access to the device:
    * cryptsetup luksOpen <device> <mapname>
      * /dev/mapper/&lt;mapname&gt;
  * Create the filesystem:
    * mkfs -t ext4 /dev/mapper/<mapname>
  * Mount the filesystem:
    * mount /dev/mapper/<mapname> /mnt
  * Make filesystem persistant:
    * vim /etc/fstab
      * /dev/mapper/<mapname> /cryptomount ext4 defaults 1 2
  * Removing access to an encrypted device:
    * Umount the filesystem, if mounted:
      * umount /mnt
    * cryptsetup luksClose mapname
  * To make LUKS devices available at boot time (persistance):
    * /etc/crypttab
      * <mapname> <device> [keyfile] [options]
    * To create a keyfile:
      * dd if=/dev/urandom of=/etc/keyfile bs=1k count=4
      * cryptsetup luksAddKey &lt;device&gt; /etc/keyfile
      * chmod 400 /etc/keyfile
  * To test LUKS functionality for persistance:
    * umount /cryptfs
    * cryptsetup luksClose mapname
    * #> bash
    * #> . /etc/init.d/functions
    * #> init_crypto 1
    * #> mount -a
    * #> ls /cryptfs

If I remember correctly, you can't do whole disk encryption with LUKS after the fact. Meaning, you can use LUKS to do whole disk encryption after the operating system has been installed. You can, however, create a back up of a partition like /home, encrypt it, then restore /home to your newly encrypted partition. I'll play around with this soon and get some solid details available for those of you looking for an TrueCrypt alternative for Linux. For now, I hope that this helps.
