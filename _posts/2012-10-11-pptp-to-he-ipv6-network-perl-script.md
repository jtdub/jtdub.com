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

```bash
#!/usr/bin/perl

$pptpServer     = "HE_PPTPSERVER";
$pptpUsername   = "USERNAME";
$pptpPassword   = "PASSWORD";

$tunRemote      = "TUN_DESTIPADDR";
$tunClient      = "TUN_CLIENTIPADDR";

$client6        = "TUN_IPV6ADDR";

if(!$ARGV[0]) {
        print "$0 [start | stop]\n";
} elsif($ARGV[0] eq "start") {
        `pptpsetup --create ipv6 --server $pptpServer --username $pptpUsername --password $pptpPassword --start`;
        `ip tunnel add sixbone mode sit remote $tunRemote local $tunClient ttl 255 dev ppp0`;
        `ip link set sixbone up`;
        `ip addr add $client6 dev sixbone`;
        `ip route add ::/0 dev sixbone`;
        `ip route add 2000::/3 dev sixbone`;
} elsif($ARGV[0] eq "stop") {
        `ip route del ::/0 dev sixbone`;
        `ip route del 2000::/3 dev sixbone`;
        `ip addr del $client6 dev sixbone`;
        `ip link set sixbone down`;
        `ip tunnel del sixbone`;
        `pptpsetup --delete ipv6`;
        @ps = `ps ax | grep pptp`;
        foreach $proc (@ps) {
                @pid = split(/ +/,$proc);
                `kill -9 $pid[1]`;
        };
} else {
        print "$0 [start | stop]\n";
}
```
