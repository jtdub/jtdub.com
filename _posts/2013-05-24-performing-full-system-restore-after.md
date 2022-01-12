---
layout: post
title: Performing a full system restore after a Linux server re-kick
date: '2013-05-24'
author: jtdub
tags:
- Bash Tips
- Linux
- Backup and Recovery
- packetgeek.net
---

Sometimes, a server becomes so corrupt that you need to re-install the operating system and perform a full system restore of the server from backups. After the OS re-install, but before you perform the restore, you need to create a backup of the files that are responsible for booting the server, defining the partition and file system layout, and naming the hardware. Once the full system restore has been completed, you should restore those files.

Here are the files that you should backup before performing the restore.
* /boot
* /etc/fstab
* /etc/grub.conf
* /etc/mtab
* /etc/udev
* /etc/modprobe.conf
* /etc/modprobe.d

Here is a script that will help you out backup the needed files

```bash
mkdir ~/backup_files; cd $_
for i in /boot /etc/fstab /etc/grub.conf /etc/mtab /etc/udev /etc/modprobe.conf /etc/modprobe.d; do
    cp -a $i ~/backup_files;
done
```

Here is a script that will help you restore the needed files

```bash
cd ~/backup_files
d=`date +%m-%d-%Y`

for i in `ls`; do
    if [[ $i == "boot" ]]; then
        cp -a /boot /boot.$d
        cp -a boot /
        restorecon -R /$i
    else
        if [[ -e /etc/$i ]]; then
            cp -a /etc/$i /etc/$i.$d
            cp -a $i /etc/$i
            restorecon -R /etc/$i
        fi
   fi
done
```
