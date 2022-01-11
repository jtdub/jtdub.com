---
layout: post
title: |-
  RHCE Series: Use /proc/sys and sysctl to modify and set kernel runtime
  parameters.
date: '2012-10-16'
author: jtdub
tags:
- Kernel Tuning
- Linux
- RHCE Study Notes
- packetgeek.net
---

Kernel tuning is pretty easy. There are a couple of ways of doing it. The old way of modifying kernel perimeters was by modifying the /proc.

For example:

```bash
[root@server1 ~]# cat /proc/sys/net/ipv4/icmp_echo_ignore_all 
0
```

If I were to change that to a 0 to a 1, server1 would drop all icmp echo packets, thus ignoring ping requests.

```bash
[root@client1 ~]# echo "Before kernel tuning" && ping -c 1 192.168.101.1
Before kernel tuning
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.598 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.598/0.598/0.598/0.000 ms


[root@server1 ~]# echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all 
[root@server1 ~]# 


[root@client1 ~]# echo "After kernel tuning" && ping -c 1 192.168.101.1
After kernel tuning
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 10000ms
```

You can also use the sysctl command to do the same thing:

```bash
[root@server1 ~]# sysctl -a | grep icmp | grep echo
net.ipv4.icmp_echo_ignore_all = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1


[root@client1 ~]# echo "Before kernel tuning" && ping -c 1 192.168.101.1
Before kernel tuning
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 10000ms


[root@server1 ~]# sysctl net.ipv4.icmp_echo_ignore_all=0
net.ipv4.icmp_echo_ignore_all = 0


[root@client1 ~]# echo "After kernel tuning" && ping -c 1 192.168.101.1
After kernel tuning
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.590 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.590/0.590/0.590/0.000 ms
```

To make any changes persistent on boot up, you'll need to put them in the /etc/sysctl.conf

```bash
[root@server1 ~]# sysctl net.ipv4.icmp_echo_ignore_all=0 >> /etc/sysctl.conf 
[root@server1 ~]# tail -1 /etc/sysctl.conf 
net.ipv4.icmp_echo_ignore_all = 0
```

Practice care when outputting kernel paremeters to the /etc/sysctl.conf. There are already some values specified and you output using > instead of >>, then you'll overwrite those values. Got backups?

You can also see all kernel tunable values by issuing a `sysctl -a`.
