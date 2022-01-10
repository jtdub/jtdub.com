---
layout: post
title: Making NAT work with the default Red Hat iptables ruleset
date: '2012-10-26'
author: jtdub
tags:
- IPTables
- Linux
- Firewall
- NAT
- packetgeek.net
---

Just a mental note.
<br/>
<br/>
<pre>sysctl -w net.ipv4.ip_forward=1 &gt;&gt; /etc/sysctl.conf<br/>iptables -I POSTROUTING -t nat -o eth0 -j MASQUERADE<br/>iptables -I FORWARD -i eth1 -o eth0 -m state --state NEW -j ACCEPT<br/>iptables -I FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT<br/>service iptables save<br/></pre>