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
<br/>
<ul>
 <br/>
 <li>
  server1:
  <br/>
  <ul>
   <br/>
   <li>
    eth0: dhcp has access to the Internet
   </li>
   <br/>
   <li>
    eth1: static address of 192.168.101.1/24, internal network.
   </li>
   <br/>
   <li>
    Server1 acts as the firewall / NAT router
   </li>
   <br/>
  </ul>
  <br/>
 </li>
 <br/>
 <li>
  client1:
  <br/>
  <ul>
   <br/>
   <li>
    eth0: static address of 192.168.101.101
   </li>
   <br/>
   <li>
    Client1 acts as a computer on an internal network.
   </li>
   <br/>
  </ul>
  <br/>
 </li>
 <br/>
 <li>
  client2:
  <br/>
  <ul>
   <br/>
   <li>
    eth0: static address of 192.168.101.102
   </li>
   <br/>
   <li>
    Client2 acts as a computer on an internal network.
   </li>
   <br/>
  </ul>
  <br/>
 </li>
 <br/>
</ul>
<br/>
The first thing that we'll need to do is allow the computer to forward traffic between interfaces.
<br/>
<pre>[root@server1 ~]# sysctl -a | grep net.ipv4| grep forward<br/>net.ipv4.conf.all.forwarding = 0<br/>net.ipv4.conf.all.mc_forwarding = 0<br/>net.ipv4.conf.default.forwarding = 0<br/>net.ipv4.conf.default.mc_forwarding = 0<br/>net.ipv4.conf.lo.forwarding = 0<br/>net.ipv4.conf.lo.mc_forwarding = 0<br/>net.ipv4.conf.eth0.forwarding = 0<br/>net.ipv4.conf.eth0.mc_forwarding = 0<br/>net.ipv4.conf.eth1.forwarding = 0<br/>net.ipv4.conf.eth1.mc_forwarding = 0<br/>net.ipv4.ip_forward = 0<br/>[root@server1 ~]# sysctl net.ipv4.ip_forward=1<br/>net.ipv4.ip_forward = 1<br/>[root@server1 ~]# vim /etc/sysctl.conf <br/>[root@server1 ~]# grep net.ipv4.ip_forward /etc/sysctl.conf <br/>net.ipv4.ip_forward = 1</pre>
<br/>
Editing the /etc/sysctl.conf makes the setting persistent across reboots.
<br/>
<br/>
Since we made changes to iptables in the previous blog, I'll again give myself a clean slate to work with.
<br/>
<pre>[root@server1 ~]# iptables -F<br/>[root@server1 ~]# iptables -F -t nat<br/>[root@server1 ~]# iptables -L<br/>Chain INPUT (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain FORWARD (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain OUTPUT (policy ACCEPT)<br/>target     prot opt source               destination         <br/>[root@server1 ~]# iptables -L -t nat<br/>Chain PREROUTING (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain POSTROUTING (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain OUTPUT (policy ACCEPT)<br/>target     prot opt source               destination</pre>
<br/>
I'll verify that my client computers can ping the gateway, each other, but can not get to the internet.
<br/>
<br/>
<br/>
<pre>[root@client1 ~]# for i in 192.168.101.1 \<br/>192.168.101.102 \<br/>4.2.2.2; \<br/>do ping -c 1 $i; done<br/>PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.<br/>64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.543 ms<br/><br/>--- 192.168.101.1 ping statistics ---<br/>1 packets transmitted, 1 received, 0% packet loss, time 0ms<br/>rtt min/avg/max/mdev = 0.543/0.543/0.543/0.000 ms<br/>PING 192.168.101.102 (192.168.101.102) 56(84) bytes of data.<br/>64 bytes from 192.168.101.102: icmp_seq=1 ttl=64 time=0.412 ms<br/><br/>--- 192.168.101.102 ping statistics ---<br/>1 packets transmitted, 1 received, 0% packet loss, time 0ms<br/>rtt min/avg/max/mdev = 0.412/0.412/0.412/0.000 ms<br/>PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.<br/><br/>--- 4.2.2.2 ping statistics ---<br/>1 packets transmitted, 0 received, 100% packet loss, time 10000ms</pre>
<br/>
<pre>[root@client2 ~]# for i in 192.168.101.1 \<br/>192.168.101.101 \<br/>4.2.2.2; \<br/>do ping -c 1 $i; done<br/>PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.<br/>64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.402 ms<br/><br/>--- 192.168.101.1 ping statistics ---<br/>1 packets transmitted, 1 received, 0% packet loss, time 0ms<br/>rtt min/avg/max/mdev = 0.402/0.402/0.402/0.000 ms<br/>PING 192.168.101.101 (192.168.101.101) 56(84) bytes of data.<br/>64 bytes from 192.168.101.101: icmp_seq=1 ttl=64 time=0.224 ms<br/><br/>--- 192.168.101.101 ping statistics ---<br/>1 packets transmitted, 1 received, 0% packet loss, time 0ms<br/>rtt min/avg/max/mdev = 0.224/0.224/0.224/0.000 ms<br/>PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.<br/><br/>--- 4.2.2.2 ping statistics ---<br/>1 packets transmitted, 0 received, 100% packet loss, time 10000ms</pre>
<br/>
Now, I'll implement the NAT.
<br/>
<br/>
<br/>
<pre>[root@server1 ~]# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE<br/>[root@server1 ~]# iptables -L<br/>Chain INPUT (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain FORWARD (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain OUTPUT (policy ACCEPT)<br/>target     prot opt source               destination         <br/>[root@server1 ~]# iptables -L -t nat<br/>Chain PREROUTING (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain POSTROUTING (policy ACCEPT)<br/>target     prot opt source               destination         <br/>MASQUERADE  all  --  anywhere             anywhere            <br/><br/>Chain OUTPUT (policy ACCEPT)<br/>target     prot opt source               destination</pre>
<br/>
Now my client PC's can get out to the Internet:
<br/>
<br/>
<br/>
<pre>[root@client1 ~]# ping -c 2 4.2.2.2<br/>PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.<br/>64 bytes from 4.2.2.2: icmp_seq=1 ttl=56 time=10.2 ms<br/>64 bytes from 4.2.2.2: icmp_seq=2 ttl=56 time=9.96 ms<br/><br/>--- 4.2.2.2 ping statistics ---<br/>2 packets transmitted, 2 received, 0% packet loss, time 1011ms<br/>rtt min/avg/max/mdev = 9.960/10.103/10.246/0.143 ms<br/><br/>[root@client2 ~]# ping -c 2 4.2.2.2<br/>PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.<br/>64 bytes from 4.2.2.2: icmp_seq=1 ttl=56 time=10.3 ms<br/>64 bytes from 4.2.2.2: icmp_seq=2 ttl=56 time=9.98 ms<br/><br/>--- 4.2.2.2 ping statistics ---<br/>2 packets transmitted, 2 received, 0% packet loss, time 1011ms<br/>rtt min/avg/max/mdev = 9.986/10.144/10.303/0.187 ms</pre>
<br/>
This only works with the single line:
<br/>
<br/>
iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
<br/>
<br/>
because the default rule for the INPUT and FORWARD chains are to ACCEPT the traffic:
<br/>
<br/>
<br/>
<pre class="crayon-selected">[root@client2 ~]# iptables -L<br/>Chain INPUT (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain FORWARD (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain OUTPUT (policy ACCEPT)<br/>target     prot opt source               destination         <br/>[root@client2 ~]# iptables -L -t nat<br/>Chain PREROUTING (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain POSTROUTING (policy ACCEPT)<br/>target     prot opt source               destination         <br/><br/>Chain OUTPUT (policy ACCEPT)<br/>target     prot opt source               destination</pre>
<br/>
Otherwise, you would need a couple extra rules to allow the traffic.
<br/>
<br/>
Those rules would be:
<br/>
iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
<br/>
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
<br/>
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
