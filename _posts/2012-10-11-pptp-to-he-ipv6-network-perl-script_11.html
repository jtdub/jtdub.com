---
layout: post
title: PPTP to HE IPv6 Network Perl Script
date: '2012-10-11'
author: jtdub
tags:
- Linux
- IPv6
- Perl Tips
- packetgeek.net
---

I forgot about this. This was a perl script that I used to use to connect to Hurricane Electric IPv6 Network via PPTP. Last I checked, their pptp servers were offline. Bummer for those who can't do IPv6 in IP tunneling. Requires the pptp-setup package.
<pre>#!/usr/bin/perl<br/><br/>$pptpServer     = "HE_PPTPSERVER";<br/>$pptpUsername   = "USERNAME";<br/>$pptpPassword   = "PASSWORD";<br/><br/>$tunRemote      = "TUN_DESTIPADDR";<br/>$tunClient      = "TUN_CLIENTIPADDR";<br/><br/>$client6        = "TUN_IPV6ADDR";<br/><br/>if(!$ARGV[0]) {<br/>        print "$0 [start | stop]\n";<br/>} elsif($ARGV[0] eq "start") {<br/>        `pptpsetup --create ipv6 --server $pptpServer --username $pptpUsername --password $pptpPassword --start`;<br/>        `ip tunnel add sixbone mode sit remote $tunRemote local $tunClient ttl 255 dev ppp0`;<br/>        `ip link set sixbone up`;<br/>        `ip addr add $client6 dev sixbone`;<br/>        `ip route add ::/0 dev sixbone`;<br/>        `ip route add 2000::/3 dev sixbone`;<br/>} elsif($ARGV[0] eq "stop") {<br/>        `ip route del ::/0 dev sixbone`;<br/>        `ip route del 2000::/3 dev sixbone`;<br/>        `ip addr del $client6 dev sixbone`;<br/>        `ip link set sixbone down`;<br/>        `ip tunnel del sixbone`;<br/>        `pptpsetup --delete ipv6`;<br/>        @ps = `ps ax | grep pptp`;<br/>        foreach $proc (@ps) {<br/>                @pid = split(/ +/,$proc);<br/>                `kill -9 $pid[1]`;<br/>        };<br/>} else {<br/>        print "$0 [start | stop]\n";<br/>}<br/></pre>