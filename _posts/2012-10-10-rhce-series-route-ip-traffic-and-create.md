---
layout: post
title: 'RHCE Series: Route IP traffic and create static routes'
date: '2012-10-10'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- Routing Protocols
- packetgeek.net
---

As I start preparing for the RHCE exam, I'm attempting to go through each exam objective one by one and put together my notes on the subjects. I'll try to go trough each exam objective in the order that it's listed on it's page, but I may skip around a little bit on the objectives that very vague on what exactly they want. This first set of notes is on routing IP traffic and static routes. Enjoy.

There are two installed packages that can provide the same routing and information and allow you to create static routes. Those packages are net-tools and iproute.

```bash
[root@server1 ~]# yum provides /sbin/ifconfig
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
net-tools-1.60-110.el6_2.x86_64 : Basic networking tools
Repo        : sgn
Matched from:
Filename    : /sbin/ifconfig

net-tools-1.60-110.el6_2.x86_64 : Basic networking tools
Repo        : installed
Matched from:
Other       : Provides-match: /sbin/ifconfig

[root@server1 ~]# rpm -ql net-tools
/bin/dnsdomainname
/bin/domainname
/bin/hostname
/bin/netstat
/bin/nisdomainname
/bin/ypdomainname
/etc/ethers
/sbin/arp
/sbin/ether-wake
/sbin/ifconfig
/sbin/ipmaddr
/sbin/iptunnel
/sbin/mii-diag
/sbin/mii-tool
/sbin/nameif
/sbin/plipconfig
/sbin/route
/sbin/slattach
/usr/share/doc/net-tools-1.60
/usr/share/doc/net-tools-1.60/COPYING
/usr/share/locale/cs/LC_MESSAGES/net-tools.mo
/usr/share/locale/de/LC_MESSAGES/net-tools.mo
/usr/share/locale/et_EE/LC_MESSAGES/net-tools.mo
/usr/share/locale/fr/LC_MESSAGES/net-tools.mo
/usr/share/locale/pt_BR/LC_MESSAGES/net-tools.mo
/usr/share/man/de/man1/dnsdomainname.1.gz
/usr/share/man/de/man1/domainname.1.gz
/usr/share/man/de/man1/hostname.1.gz
/usr/share/man/de/man1/nisdomainname.1.gz
/usr/share/man/de/man1/ypdomainname.1.gz
/usr/share/man/de/man5/ethers.5.gz
/usr/share/man/de/man8/arp.8.gz
/usr/share/man/de/man8/ifconfig.8.gz
/usr/share/man/de/man8/netstat.8.gz
/usr/share/man/de/man8/plipconfig.8.gz
/usr/share/man/de/man8/route.8.gz
/usr/share/man/de/man8/slattach.8.gz
/usr/share/man/fr/man1/dnsdomainname.1.gz
/usr/share/man/fr/man1/domainname.1.gz
/usr/share/man/fr/man1/hostname.1.gz
/usr/share/man/fr/man1/nisdomainname.1.gz
/usr/share/man/fr/man1/ypdomainname.1.gz
/usr/share/man/fr/man5/ethers.5.gz
/usr/share/man/fr/man8/arp.8.gz
/usr/share/man/fr/man8/ifconfig.8.gz
/usr/share/man/fr/man8/netstat.8.gz
/usr/share/man/fr/man8/plipconfig.8.gz
/usr/share/man/fr/man8/route.8.gz
/usr/share/man/fr/man8/slattach.8.gz
/usr/share/man/man1/dnsdomainname.1.gz
/usr/share/man/man1/domainname.1.gz
/usr/share/man/man1/hostname.1.gz
/usr/share/man/man1/nisdomainname.1.gz
/usr/share/man/man1/ypdomainname.1.gz
/usr/share/man/man5/ethers.5.gz
/usr/share/man/man8/arp.8.gz
/usr/share/man/man8/ether-wake.8.gz
/usr/share/man/man8/ifconfig.8.gz
/usr/share/man/man8/ipmaddr.8.gz
/usr/share/man/man8/iptunnel.8.gz
/usr/share/man/man8/mii-diag.8.gz
/usr/share/man/man8/mii-tool.8.gz
/usr/share/man/man8/nameif.8.gz
/usr/share/man/man8/netstat.8.gz
/usr/share/man/man8/plipconfig.8.gz
/usr/share/man/man8/route.8.gz
/usr/share/man/man8/slattach.8.gz
/usr/share/man/pt/man1/dnsdomainname.1.gz
/usr/share/man/pt/man1/domainname.1.gz
/usr/share/man/pt/man1/hostname.1.gz
/usr/share/man/pt/man1/nisdomainname.1.gz
/usr/share/man/pt/man1/ypdomainname.1.gz
/usr/share/man/pt/man8/arp.8.gz
/usr/share/man/pt/man8/ifconfig.8.gz
/usr/share/man/pt/man8/netstat.8.gz
/usr/share/man/pt/man8/route.8.gz


[root@server1 ~]# yum provides /sbin/ip
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
iproute-2.6.32-20.el6.x86_64 : Advanced IP routing and network device configuration tools
Repo        : sgn
Matched from:
Filename    : /sbin/ip

iproute-2.6.32-20.el6.x86_64 : Advanced IP routing and network device configuration tools
Repo        : installed
Matched from:
Other       : Provides-match: /sbin/ip

[root@server1 ~]# rpm -ql iproute
/etc/iproute2
/etc/iproute2/ematch_map
/etc/iproute2/rt_dsfield
/etc/iproute2/rt_protos
/etc/iproute2/rt_realms
/etc/iproute2/rt_scopes
/etc/iproute2/rt_tables
/etc/sysconfig/cbq
/etc/sysconfig/cbq/avpkt
/etc/sysconfig/cbq/cbq-0000.example
/sbin/cbq
/sbin/ifcfg
/sbin/ip
/sbin/rtmon
/sbin/tc
/usr/lib64/tc
/usr/lib64/tc/m_xt.so
/usr/sbin/arpd
/usr/sbin/lnstat
/usr/sbin/nstat
/usr/sbin/rtacct
/usr/sbin/ss
/usr/share/doc/iproute-2.6.32
/usr/share/doc/iproute-2.6.32/README
/usr/share/doc/iproute-2.6.32/README.decnet
/usr/share/doc/iproute-2.6.32/README.distribution
/usr/share/doc/iproute-2.6.32/README.iproute2+tc
/usr/share/doc/iproute-2.6.32/README.lnstat
/usr/share/man/man8/arpd.8.gz
/usr/share/man/man8/cbq.8.gz
/usr/share/man/man8/ifcfg.8.gz
/usr/share/man/man8/ip.8.gz
/usr/share/man/man8/lnstat.8.gz
/usr/share/man/man8/nstat.8.gz
/usr/share/man/man8/routel.8.gz
/usr/share/man/man8/rtacct.8.gz
/usr/share/man/man8/rtmon.8.gz
/usr/share/man/man8/ss.8.gz
/usr/share/man/man8/tc-bfifo.8.gz
/usr/share/man/man8/tc-cbq-details.8.gz
/usr/share/man/man8/tc-cbq.8.gz
/usr/share/man/man8/tc-htb.8.gz
/usr/share/man/man8/tc-pfifo.8.gz
/usr/share/man/man8/tc-pfifo_fast.8.gz
/usr/share/man/man8/tc-prio.8.gz
/usr/share/man/man8/tc-red.8.gz
/usr/share/man/man8/tc-sfq.8.gz
/usr/share/man/man8/tc-tbf.8.gz
/usr/share/man/man8/tc.8.gz
/usr/share/tc
/usr/share/tc/normal.dist
/usr/share/tc/pareto.dist
/usr/share/tc/paretonormal.dist
```

Above, you will see the package description, as well as the files that are installed with each package. Net-tools is the old tools and are pretty much kept around for compatibility. I personally like the output of the ifconfig and the route command better than I do the ip command, but as ifconfig and route are pretty much depreciated and will be going away at some point, I'll focus my notes on the command sequence of the ip command.

ip command structure:

```bash
[root@server1 ~]# ip route help
Usage: ip route { list | flush } SELECTOR
       ip route get ADDRESS [ from ADDRESS iif STRING ]
                            [ oif STRING ]  [ tos TOS ]
       ip route { add | del | change | append | replace | monitor } ROUTE
SELECTOR := [ root PREFIX ] [ match PREFIX ] [ exact PREFIX ]
            [ table TABLE_ID ] [ proto RTPROTO ]
            [ type TYPE ] [ scope SCOPE ]
ROUTE := NODE_SPEC [ INFO_SPEC ]
NODE_SPEC := [ TYPE ] PREFIX [ tos TOS ]
             [ table TABLE_ID ] [ proto RTPROTO ]
             [ scope SCOPE ] [ metric METRIC ]
INFO_SPEC := NH OPTIONS FLAGS [ nexthop NH ]...
NH := [ via ADDRESS ] [ dev STRING ] [ weight NUMBER ] NHFLAGS
OPTIONS := FLAGS [ mtu NUMBER ] [ advmss NUMBER ]
           [ rtt TIME ] [ rttvar TIME ] [reordering NUMBER ]
           [ window NUMBER] [ cwnd NUMBER ] [ initcwnd NUMBER ]
           [ ssthresh NUMBER ] [ realms REALM ] [ src ADDRESS ]
           [ rto_min TIME ] [ hoplimit NUMBER ] 
TYPE := [ unicast | local | broadcast | multicast | throw |
          unreachable | prohibit | blackhole | nat ]
TABLE_ID := [ local | main | default | all | NUMBER ]
SCOPE := [ host | link | global | NUMBER ]
FLAGS := [ equalize ]
MP_ALGO := { rr | drr | random | wrandom }
NHFLAGS := [ onlink | pervasive ]
RTPROTO := [ kernel | boot | static | NUMBER ]
TIME := NUMBER[s|ms|us|ns|j]
```

ip route {list, add, delete}:

```bash
[root@server1 ~]# ip route list
192.168.122.0/24 dev eth0  proto kernel  scope link  src 192.168.122.101 
169.254.0.0/16 dev eth0  scope link  metric 1002 
default via 192.168.122.1 dev eth0 
[root@server1 ~]# ip route add 192.168.100.0/24 via 192.168.122.1 dev eth0
[root@server1 ~]# ip route list
192.168.100.0/24 via 192.168.122.1 dev eth0 
192.168.122.0/24 dev eth0  proto kernel  scope link  src 192.168.122.101 
169.254.0.0/16 dev eth0  scope link  metric 1002 
default via 192.168.122.1 dev eth0 
[root@server1 ~]# ip route del 192.168.100.0/24 via 192.168.122.1 dev eth0
[root@server1 ~]# ip route list
192.168.122.0/24 dev eth0  proto kernel  scope link  src 192.168.122.101 
169.254.0.0/16 dev eth0  scope link  metric 1002 
default via 192.168.122.1 dev eth0
```

Let's break it down:

<ul>
 <br/>
 <li>
  'ip route add' - add a route
 </li>
 <br/>
 <li>
  192.168.100.0/24 - the destination network
 </li>
 <br/>
 <li>
  'via 192.168.122.1' - the gateway to reach the 192.168.100.0/24 network.
 </li>
 <br/>
 <li>
  'dev eth0' - the interface to send the traffic to both the gateway and destination network.
 </li>
 <br/>
</ul>

The 'dev eth0' is optional.

To make static routes persistent, you can create a static-routes file in /etc/sysconfig/. This file is already referenced in the network init script.

```bash
[root@server1 ~]# grep route /etc/init.d/network
 # Add non interface-specific static-routes.
 if [ -f /etc/sysconfig/static-routes ]; then
    grep "^any" /etc/sysconfig/static-routes | while read ignore args ; do
              /sbin/route add -$args
```

The 'static-routes' file has a similar syntax to the 'route' command. The reason for that is because the network init script uses the route command when it reads the static-routes file! That syntax is:

An example would be:

```bash
[root@server1 sysconfig]# cat static-routes 
any net 192.168.100.0 netmask 255.255.255.0 gw 192.168.122.1 dev eth0
```

The next option would be to add a route-dev file in /etc/sysconfig/network-scripts.

An example of this file would be:

```bash
[root@server1 network-scripts]# cat route-eth0 
192.168.100.0/24 via 192.168.122.1 dev eth0
```
