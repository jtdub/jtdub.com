---
layout: post
title: 'RHCSA Version 8: Operating Running Systems'
date: '2022-01-10'
author: jtdub
tags:
- packetgeek.net 
- RHCSA Study Notes
- Linux
- Redhat
---

### Boot, reboot, and shut down a system normally

### Boot systems into different targets manually

### Interrupt the boot process in order to gain access to a system

> TLDR; 
> 1) Reboot
> 2) At Grub Menu, select rescue kernel and press `e`
> 3) At the end of the `linux` kernel line, remove `rhgb quiet` and add `rd.break enforcing=0`

In order to recover the root password of a system, you must have console access to the server in order to modify the boot loader to boot into single user mode. 

When you're first prompted with the boot menu, press down down arrow on the keyboard to stop the boot timer. Then scroll through your boot menu options until the rescue kernel is highlighted. With the rescue kernel highlighted, press the `e` button to edit the rescue boot options.

<img src="/images/rhcsa/grub-menu1.png" alt="Grub Menu" width=600>

In the Grub edit menu, locate the line that starts with `linux`. The command may span multiple lines and will end with `rhgb quiet`. Go to the end of the line.

<img src="/images/rhcsa/grub-menu2.png" alt="Grub Menu: Edit" width=600>

Remove `rhgb quiet` from the command and add `rd.break enforcing=0`. Once complete, press the `Ctrl-X` key sequence to continue booting to the rescue mode.

<img src="/images/rhcsa/grub-menu3.png" alt="Grub Menu:Single User Mode" width=600>

At this point, the system will boot into single user mode and will boot into a `switch_root:/#` prompt. The `/sysroot` filesystem will mount in read-only mode. This can be verified by executing: `mount | grep /sysroot`. You'll need to remount the filesystem as read-write. To to this execute, `mount -o rw,remount /sysroot`. The `mount | grep /sysroot` command will verify that it's mounted as read-write.

With the system booted into single user mode and the `/sysroot` volume mounted with read-write permissions, you will need to change the root to /sysroot. This can be done by executing `chroot /sysroot`. Once completed, execute the `passwd` command to change the root password. Once completed type `exit` twice and the system will reboot. At this point, you will be able to login with the new root password.

When the system has booted back to normal, the security context must be restored for the shadow file. This can be done by executing `restorecon /etc/shadow`. `ls -Z /etc/shadow` can be used to view the current security context.

### Identify CPU/memory intensive processes and kill processes

### Adjust process scheduling

### Manage tuning profiles

### Locate and interpret system log files and journals

### Preserve system journals

### Start, stop, and check the status of network services

### Securely transfer files between systems
