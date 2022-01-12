---
layout: post
title: |-
  RHCE Series: Use iptables to implement packet filtering and configure
  network address translation (NAT): Part 2
date: '2012-10-15'
author: jtdub
tags:
- IPTables
- Linux
- RHCE Study Notes
- packetgeek.net
---

In this second part, we'll discuss how to set up a NAT in Linux, using iptables. As in the previous blog, here are the stats of my VM's:

* server1:
  * eth0: dhcp has access to the Internet
  * eth1: static address of 192.168.101.1/24, internal network.
  * server1 acts as the firewall / NAT router
* client1:
  * eth0: static address of 192.168.101.101
  * client1 acts as a computer on an internal network.
* client2:
  * eth0: static address of 192.168.101.102
  * client2 acts as a computer on an internal network.

The first thing that we'll need to do is allow the computer to forward traffic between interfaces.

```bash
[root@server1 ~]# sysctl -a | grep net.ipv4| grep forward
net.ipv4.conf.all.forwarding = 0
net.ipv4.conf.all.mc_forwarding = 0
net.ipv4.conf.default.forwarding = 0
net.ipv4.conf.default.mc_forwarding = 0
net.ipv4.conf.lo.forwarding = 0
net.ipv4.conf.lo.mc_forwarding = 0
net.ipv4.conf.eth0.forwarding = 0
net.ipv4.conf.eth0.mc_forwarding = 0
net.ipv4.conf.eth1.forwarding = 0
net.ipv4.conf.eth1.mc_forwarding = 0
net.ipv4.ip_forward = 0
[root@server1 ~]# sysctl net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
[root@server1 ~]# vim /etc/sysctl.conf 
[root@server1 ~]# grep net.ipv4.ip_forward /etc/sysctl.conf 
net.ipv4.ip_forward = 1
```

Editing the /etc/sysctl.conf makes the setting persistent across reboots.

Since we made changes to iptables in the previous blog, I'll again give myself a clean slate to work with.

```bash
[root@server1 ~]# iptables -F
[root@server1 ~]# iptables -F -t nat
[root@server1 ~]# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
[root@server1 ~]# iptables -L -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```

I'll verify that my client computers can ping the gateway, each other, but can not get to the internet.

```bash
[root@client1 ~]# for i in 192.168.101.1 \
192.168.101.102 \
4.2.2.2; \
do ping -c 1 $i; done
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.543 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.543/0.543/0.543/0.000 ms
PING 192.168.101.102 (192.168.101.102) 56(84) bytes of data.
64 bytes from 192.168.101.102: icmp_seq=1 ttl=64 time=0.412 ms

--- 192.168.101.102 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.412/0.412/0.412/0.000 ms
PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.

--- 4.2.2.2 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 10000ms


[root@client2 ~]# for i in 192.168.101.1 \
192.168.101.101 \
4.2.2.2; \
do ping -c 1 $i; done
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.402 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.402/0.402/0.402/0.000 ms
PING 192.168.101.101 (192.168.101.101) 56(84) bytes of data.
64 bytes from 192.168.101.101: icmp_seq=1 ttl=64 time=0.224 ms

--- 192.168.101.101 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.224/0.224/0.224/0.000 ms
PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.

--- 4.2.2.2 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 10000ms
```

Now, I'll implement the NAT.

```bash
[root@server1 ~]# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
[root@server1 ~]# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
[root@server1 ~]# iptables -L -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
MASQUERADE  all  --  anywhere             anywhere            

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```

Now my client PC's can get out to the Internet:

```bash
[root@client1 ~]# ping -c 2 4.2.2.2
PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.
64 bytes from 4.2.2.2: icmp_seq=1 ttl=56 time=10.2 ms
64 bytes from 4.2.2.2: icmp_seq=2 ttl=56 time=9.96 ms

--- 4.2.2.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1011ms
rtt min/avg/max/mdev = 9.960/10.103/10.246/0.143 ms

[root@client2 ~]# ping -c 2 4.2.2.2
PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.
64 bytes from 4.2.2.2: icmp_seq=1 ttl=56 time=10.3 ms
64 bytes from 4.2.2.2: icmp_seq=2 ttl=56 time=9.98 ms

--- 4.2.2.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1011ms
rtt min/avg/max/mdev = 9.986/10.144/10.303/0.187 ms
```

This only works with the single line:

```bash
iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
```

because the default rule for the INPUT and FORWARD chains are to ACCEPT the traffic:

```bash
[root@client2 ~]# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
[root@client2 ~]# iptables -L -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```

Otherwise, you would need a couple extra rules to allow the traffic.

Those rules would be:

```bash
iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
```
