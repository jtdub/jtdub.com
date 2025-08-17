---
layout: post
title: 'RHCE Series: SSH and NTP'
date: '2012-10-27'
author: jtdub
tags:
- Linux
- NTP
- RHCE Study Notes
- OpenSSH
- SSH
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

#### SSH
* Configure key-based authentication.
* Configure additional options described in documentation.

#### NTP
* Synchronize time using other NTP peers.

In Red Hat 6 (and I'm sure in 5 as well), public key authentication is enabled by default, but if you're unsure, you can uncomment the option and verify that it is set to yes.

```bash
[root@server1 ~]# vim /etc/ssh/sshd_config 
[root@server1 ~]# egrep 'PubkeyAuthentication|AuthorizedKeysFile' /etc/ssh/sshd_config 
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
[root@server1 ~]# service sshd restart
Stopping sshd:                                             [  OK  ]
Starting sshd:                                             [  OK  ]
```

Once that is complete. We can go to our client pc, generate keys, and copy the public key over.

```bash
[root@client1 ~]# ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
c6:83:f5:86:ad:cf:06:d3:73:f6:22:8f:0a:a7:06:99 root@client1.example.com
The key's randomart image is:
+--[ RSA 2048]----+
|                 |
|                 |
|        .        |
|       + +       |
|     o. S.+      |
|    E  .o+o o    |
|     .. oo + .   |
|      .+ oo.. .  |
|     .. .o+o..   |
+-----------------+
[root@client1 ~]# ssh-copy-id -i ~/.ssh/id_rsa.pub 192.168.1.1
The authenticity of host '192.168.1.1 (192.168.1.1)' can't be established.
RSA key fingerprint is 40:f4:04:4b:68:53:92:55:82:f2:f4:68:db:0a:14:4f.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.1' (RSA) to the list of known hosts.
root@192.168.1.1's password: 
Now try logging into the machine, with "ssh '192.168.1.1'", and check in:

  .ssh/authorized_keys

to make sure we haven't added extra keys that you weren't expecting.
```

Once that has completed, we can ssh to 192.168.1.1 (server1) from client1 without a password, but use a private / public key exchange.

Now, let's configure ntp.

```bash
[root@client1 ~]# date
Sun Oct 28 04:32:13 CDT 2012
[root@client1 ~]# yum -y install ntp
[root@client1 ~]# grep server /etc/ntp.conf 
# Use public servers from the pool.ntp.org project.
server 0.centos.pool.ntp.org
server 1.centos.pool.ntp.org
server 2.centos.pool.ntp.org
#broadcast 192.168.1.255 autokey # broadcast server
#broadcast 224.0.1.1 autokey  # multicast server
#manycastserver 239.255.254.254  # manycast server
#server 127.127.1.0 # local clock
[root@client1 ~]# ntpdate 0.centos.pool.ntp.org
27 Oct 23:33:34 ntpdate[2707]: step time server 66.241.101.63 offset -17998.779036 sec
[root@client1 ~]# date
Sat Oct 27 23:33:37 CDT 2012
[root@client1 ~]# service ntpd start
Starting ntpd:                                             [  OK  ]
[root@client1 ~]# ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 mirror          204.9.54.119     2 u    8   64    1   48.895    1.225   0.000
 71.19.224.242   131.107.13.100   2 u    7   64    1   54.330    0.806   0.000
 ntp1.Housing.Be 128.32.206.55    2 u    6   64    1   51.920   -6.134   0.000
```

If you want to use other peers, you can modify the 'server' directive in /etc/ntpd.conf. Besure to use 'chkconfig' to make ntpd persistent.
