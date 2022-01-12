---
layout: post
title: Linux Encrypted Filesystems
date: '2012-09-30'
author: jtdub
tags:
- Linux
- Filesystems
- Security
- Encryption
- packetgeek.net
---

In the age of mobile devices that contain private information, whether it's personal or business information, encrypting your devices is a good idea. Filesystem encryption allows you to encrypt a single partition or even an entire hard drive. When configuring correctly, this will help mitigate privacy issues from stolen devices.

One of the solutions for encrypting a file system in Linux is to use LUKS. LUKS stands for "Linux Unified Key Setup".

I created a logical volume to use as a test bed for the encrypted file system:

```bash
[root@sgnhv ~]# lvs
  LV         VG       Attr     LSize   Pool Origin Data%  Move Log Copy%  Convert
  lv_data    vg_sgnhv -wi-ao-- 500.00g                                                                                      
  lv_root    vg_sgnhv -wi-ao--  50.00g                                           
  lv_swap    vg_sgnhv -wi-ao--   5.88g                                           

[root@sgnhv ~]# lvcreate -n lv_crypto -L 1G vg_sgnhv
  Logical volume "lv_crypto" created

[root@sgnhv ~]# lvs
  LV         VG       Attr     LSize   Pool Origin Data%  Move Log Copy%  Convert
  lv_crypto  vg_sgnhv -wi-a---   1.00g                                           
  lv_data    vg_sgnhv -wi-ao-- 500.00g                                                                                      
  lv_root    vg_sgnhv -wi-ao--  50.00g                                           
  lv_swap    vg_sgnhv -wi-ao--   5.88g
```

As you can see, I have a new 1 GB logical volume called `lv_crypto`. Now it's time to get into the nitty gritty of setting up LUKS. The first thing that we need to do is encrypt the `lv_crypto` volume with the `luksFormat` extension.

```bash
[root@sgnhv ~]# cryptsetup luksFormat /dev/vg_sgnhv/lv_crypto

WARNING!
========
This will overwrite data on /dev/vg_sgnhv/lv_crypto irrevocably.

Are you sure? (Type uppercase yes): YES
Enter LUKS passphrase: 
Verify passphrase:
```

Now that we have the lv_crypto logical volume encrypted, we need to use the `luksOpen` extension to create a device mapper to crypt_dev_mapper. The device mapper acts as an interface between dm-crypt and the device. From there, we can create the file system and mount it.

```bash
[root@sgnhv ~]# ls /dev/mapper/
control             vg_sgnhv-lv_data  vg_sgnhv-lv_libvirt  vg_sgnhv-lv_swap
vg_sgnhv-lv_crypto  vg_sgnhv-lv_home  vg_sgnhv-lv_root

[root@sgnhv ~]# cryptsetup luksOpen /dev/vg_sgnhv/lv_crypto crypt_dev_mapper
Enter passphrase for /dev/vg_sgnhv/lv_crypto:
```

As you can see, there is now a device mapper called `crypt_dev_mapper`, which is the device mapper that dm-crypt created to interact with the data in the encrypted volume. There is also `vg_sgnhv-lv_crypto`, which is the encrypted logical volume. From here on out, we'll be interacting with `crypt_dev_mapper`. If you create your file system directly on the `lv_crypto` logical volume, you will over-write the encryption, rendering it a normal everyday logical volume.

```bash
[root@sgnhv ~]# ls /dev/mapper/
control           vg_sgnhv-lv_crypto  vg_sgnhv-lv_home     vg_sgnhv-lv_root
crypt_dev_mapper  vg_sgnhv-lv_data    vg_sgnhv-lv_libvirt  vg_sgnhv-lv_swap
```

As mentioned, we'll create the file system on the dm-crypt created device mapper. In this case, I'm using the ext4 file system.

```bash
[root@sgnhv ~]# mkfs -t ext4 /dev/mapper/crypt_dev_mapper 
mke2fs 1.41.12 (17-May-2010)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
65408 inodes, 261632 blocks
13081 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=268435456
8 block groups
32768 blocks per group, 32768 fragments per group
8176 inodes per group
Superblock backups stored on blocks: 
 32768, 98304, 163840, 229376

Writing inode tables: done                            
Creating journal (4096 blocks): done
Writing superblocks and filesystem accounting information: done

This filesystem will be automatically checked every 26 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.
```

By issuing the `blkid` command, you can see that the `lv_crypto` logical volume is labeled a a `crytpo_LUKS` file system type and the `crypt_dev_mapper` is labeled as a ext4 file system type.

```bash
[root@sgnhv ~]# blkid | grep crypt
/dev/mapper/vg_sgnhv-lv_crypto: UUID="993b91fd-e3f2-4764-9453-3e6bf64c44b9" TYPE="crypto_LUKS" 
/dev/mapper/crypt_dev_mapper: UUID="4b034d56-2216-43af-86ac-98b9abb0a3fe" TYPE="ext4" 
```

Once the filesystem has been created, you can now mount the drive and start writing data to it, as seen below.

```bash
root@sgnhv ~]# mount /dev/mapper/crypt_dev_mapper /mnt/

[root@sgnhv ~]# df -h
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/vg_sgnhv-lv_root
                       50G  7.5G   40G  16% /
tmpfs                 1.9G  388K  1.9G   1% /dev/shm
/dev/md127p1          485M  128M  332M  28% /boot
/dev/mapper/vg_sgnhv-lv_data
                      493G  103G  365G  22% /data
/dev/mapper/crypt_dev_mapper
                     1006M   18M  938M   2% /mnt

[root@sgnhv ~]# dd if=/dev/urandom of=/mnt/somedata bs=1M count=10
10+0 records in
10+0 records out
10485760 bytes (10 MB) copied, 1.23517 s, 8.5 MB/s

[root@sgnhv ~]# ls /mnt/
lost+found  somedata

[root@sgnhv ~]# df -h
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/vg_sgnhv-lv_root
                       50G  7.5G   40G  16% /
tmpfs                 1.9G  388K  1.9G   1% /dev/shm
/dev/md127p1          485M  128M  332M  28% /boot
/dev/mapper/vg_sgnhv-lv_data
                      493G  103G  365G  22% /data
/dev/mapper/crypt_dev_mapper
                     1006M   28M  928M   3% /mnt
[root@sgnhv ~]# umount /mnt/
```

Once you've accessed the data that you needed, you can umount and close the dm-crypt device mapper, which will remove the `crypt_dev_mapper` device. The `luksClose` extension closes the interface with the device mapper.

```bash
[root@sgnhv ~]# cryptsetup luksClose crypt_dev_mapper
```

Now accessing the encrypted device using the `luksOpen` and `luksClose` extension is fine. In fact, a simple bash or perl script could be written to help facilitate the process. Every time you use the `luksOpen` extension, LUKS will ask you for the passphrase that you used initially set up.

However, if you want your system to initialize the encrypted file system and even mount it at boot, you will need to follow a few extra steps.

The first option is simply adding the dm-crypt device mapper name and the logical volume path to the /etc/crypttab file. This will create the dm-crypt mapper on boot. This will also require that you be present at the console when the computer boots up, as the computer will ask you for the LUKS passphrase before it maps the dm-crypt mapper. If you're not available at the console, then the boot will hang until you enter the passphrase.

```bash
[root@sgnhv ~]# vim /etc/crypttab 
[root@sgnhv ~]# cat /etc/crypttab 
crypt_dev_mapper /dev/vg_sgnhv/lv_crypto
```

There is however, an option of using a key file. To make a key file, you must create a file with some random data. Then you can use the `luksAddKey` extension to create the key.

```bash
[root@sgnhv ~]# dd if=/dev/urandom of=/etc/crypt_dev_mapper.key bs=1k count=4
[root@sgnhv ~]# cryptsetup luksAddKey /dev/vg_sgnhv/lv_crypto /etc/crypt_dev_mapper.key 
Enter any passphrase: 
```

Once the key has been created, you can add the key path in the /etc/crypttab file in the third column. In the crypttab man page, it states the third column is for adding a password. This is incorrect and it will not work if you enter the passphrase there.

Also, be sure to make the key file only readable to root, otherwise when when init_crypt function initializes and looks at the permissions of the file, it will give you a warning about it being insecure. In some instances, it will refuse to read the file, thus failing to mount the encrypted file system.

```bash
[root@sgnhv ~]# vim /etc/crypttab 
[root@sgnhv ~]# cat /etc/crypttab 
crypt_dev_mapper /dev/vg_sgnhv/lv_crypto /etc/crypt_dev_mapper.key
[root@sgnhv ~]# chmod 400 /etc/crypt_dev_mapper.key 
```

Once that is setup, you can modify your /etc/fstab to have the file system mounted at boot.

```bash
[root@sgnhv ~]# vim /etc/fstab 
[root@sgnhv ~]# tail -1 /etc/fstab 
/dev/mapper/crypt_dev_mapper /crypt  ext4 defaults 1 0
```

You can test the functionality out, without rebooting by doing the following:

```bash
[root@sgnhv ~]# cryptsetup luksClose /dev/mapper/crypt_dev_mapper 
[root@sgnhv ~]# bash
[root@sgnhv ~]# . /etc/init.d/functions 
[root@sgnhv ~]# init_crypto 1
[root@sgnhv ~]# mount -a                                   [  OK  ]
[root@sgnhv ~]# df -h | grep crypt
/dev/mapper/crypt_dev_mapper
                     1006M   18M  938M   2% /crypt
```

As you can see, the encrypted file system was mounted without asking for a passphrase. This configuration will be persistent across reboots.

Now for a public service announcement. It's actually more food for thought. If you are having your computer mount your encrypted file system on boot without any kind of interaction to authenticate the process, what good does it do to encrypt the file system in the first place?

For my personal preference, encrypting a notebooks entire filesystem or even a tablet or smart phone should be the course of action. In Linux, that can be done during the install. Otherwise, I'd propose something like [TruCrypt](http://www.truecrypt.org/). Other than that, encrypting thumb drives would be handy.
