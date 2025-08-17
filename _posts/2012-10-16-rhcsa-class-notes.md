---
layout: post
title: RHCSA Class Notes
date: '2012-10-16'
author: jtdub
tags:
- LUKS
- RHCSA Study Notes
- SELinux
- Kernel Tuning
- Linux
- Apache
- NFS
- Cron
- Autofs
- upstart
- LVM
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

Here are some notes from a recent RHCSA class.

#### Boot process

* RHEL 6 uses upstart instead of init. Upstart is setup to call the init scripts. [Upstart](http://upstart.ubuntu.com/)

#### Networking

* disable NetworkManager and edit /etc/sysconfig/network and /etc/sysconfig/network-scripts/ifcfg-* by hand.
  * for i in NetworkManager; do service $i stop; chkconfig $i off; done

#### Cron

* Time  statements are OR’ed together, NOT AND’ed together. So Sunday, January 2  would be January 2 OR Sunday. To get around that, you’ll need to script  out the day of the week.

#### Disk Encryption

* LUKS - Linux Unified Key Setup
  * Create a new LUKS encrypted device:
    * cryptsetup luksFormat
  * Establish access to the device:
    * cryptsetup luksOpen
      * /dev/mapper/
  * Create the filesystem:
    * mkfs -t ext4 /dev/mapper/
  * Mount the filesystem:
    * mount /dev/mapper/
  * Make filesystem persistant:
    * vim /etc/fstab
      * /dev/mapper/cryptomount ext4 defaults 1 2
  * Removing access to an encrypted device:
    * Umount the filesystem, if mounted:
      * umount /mnt
    * cryptsetup luksClose mapname
  * To make LUKS devices available at boot time (persistance):
    * /etc/crypttab
      * [keyfile] [options]
  * To create a keyfile:
    * dd if=/dev/urandom of=/etc/keyfile bs=1k count=4
    * cryptsetup luksAddKey
    * chmod 400 /etc/keyfile
  * To test LUKS functionality for persistance:
    * umount /cryptfs
    * cryptsetup luksClose mapname
    * #> bash
    * #> . /etc/init.d/functions
    * #> init_crypto 1
    * #> mount -a
    * #> ls /cryptfs

#### SELinux

* Every process or object has a SELinux context:
  * identity:role:domain/type
* The SELinux policy controls:
  * What identities can use which roles
  * What roles can enter which domains
  * What domains can access which types
* To change the context of a file, you can use the chcon command:
  * chcon -R --reference=/var/www/html
* To restore the default labeling from the policy and apply the contexts to file:
  * restorecon -R
* To change the SELinux mode during boot, you can pass the ‘enforcing=0’ option to the kernel in GRUB.
* Tools:
  * sestatus
  * setenforce | getenforce
  * policycoreutils
  * setroubleshoot
  * system-config-selinux &lt;- part of policycoreutils-gui in RHEL.
  * setsebool | getsebool
  * chcon
  * restorecon

#### Kernel Tuning

* Kernel documentation package: kernel-doc
  * yum -y install kernel-doc
  * /usr/share/doc/kernel-doc-2.6.32/Documentation/sysctl
* sysctl -a
  * displays all current values
* sysctl -w
  * sets a value
* sysctl -p
  * reads the /etc/sysctl.conf and loads the values into the kernel
* /etc/sysctl.conf
  * File location to make changes persistent
  * sysctl -w >> /etc/sysctl.conf

#### LVM

* Create a Volume
  * pvcreate /dev/sda4
  * vgcreate VolGroup01 /dev/sda4
    * -s flag will allow you to change the physical extent size. Default is 4MB and can be changed in increments of power of 2.
  * lvcreate -n Volname01 [ -L 10G || -l +100%FREE || -l +50 {# of extents} ] VolGroup01
* Resizing a volume
  * vgextend
  * lvextend { -l <+extents> | -L <+size> }
  * resize2fs
    * lvresize -r {-l <+extents> | -L <+size> }
      * ‘-r’ - Resize logical volume and filesystem at the sametime.
  * lvreduce -r { -l | -L }
* Snapshots
  * create snapshots
    * lvcreate -s { -l | -L } -n
  * remove snapshots
    * lvremove -f
  *  You  will need space available in the volume group of your logical volume to  be able to create a snapshot. A snapshot logical volume does not need  to be the same size of the logical volume, but will need to be large  enough to contain the data of the logical volume.
  * You can grow the file system while it is mounted, but before shrinking it must first be unmounted.

#### NFS

* showmount -e server1
  * Confirm that services are running on the machine.
* rpcinfo -p server1
  * See shared filesystems.

####  Apache

* Documentation Package:
  * httpd-manual
* Documentation Location:
  * http://localhost/manual

####  Autofs

* Mounting NFS Home directories:
  * vi /etc/auto.master
    * /home/nfs    /etc/auto.nfs
  * vi /etc/auto.nfs
    * * server:/home/nfs/&
