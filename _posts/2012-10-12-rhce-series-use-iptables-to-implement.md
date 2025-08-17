---
layout: post
title: |-
  RHCE Series: Use iptables to implement packet filtering and configure
  network address translation (NAT): Part 1
date: '2012-10-12'
author: jtdub
tags:
- IPTables
- Linux
- RHCE Study Notes
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

This section is on using IPTables to create a packet filtering firewall as well as implementing NAT with IPTables. My test environment are two stock installs of CentOS 6.3 in a virtualized environment.

The VM's:

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

The first thing that I did on server1 was make sure that I had a clean slate to work with. That included making sure that my firewall had a default setting of allowing all traffic, but wasn't forwarding any traffic. I also verified my interfaces and routing table.

```bash
[root@server1 ~]# iptables -F
[root@server1 ~]# service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[  OK  ]
[root@server1 ~]# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
[root@server1 ~]# ip addr show
1: lo:  mtu 16436 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0:  mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:54:00:f0:36:20 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.74/24 brd 192.168.122.255 scope global eth0
    inet6 fe80::5054:ff:fef0:3620/64 scope link 
       valid_lft forever preferred_lft forever
3: eth1:  mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:54:00:b3:38:d1 brd ff:ff:ff:ff:ff:ff
    inet 192.168.101.1/24 brd 192.168.101.255 scope global eth1
    inet6 fe80::5054:ff:feb3:38d1/64 scope link 
       valid_lft forever preferred_lft forever
[root@server1 ~]# ip route show
192.168.101.0/24 dev eth1  proto kernel  scope link  src 192.168.101.1 
192.168.122.0/24 dev eth0  proto kernel  scope link  src 192.168.122.74 
169.254.0.0/16 dev eth0  scope link  metric 1002 
169.254.0.0/16 dev eth1  scope link  metric 1003 
default via 192.168.122.1 dev eth0
```

I did the same thing on client1 and client2:

```bash
[root@client1 ~]# iptables -F
[root@client1 ~]# service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[  OK  ]
[root@client1 ~]# ip addr show
1: lo:  mtu 16436 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0:  mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:54:00:38:28:0a brd ff:ff:ff:ff:ff:ff
    inet 192.168.101.101/24 brd 192.168.101.255 scope global eth0
    inet6 fe80::5054:ff:fe38:280a/64 scope link 
       valid_lft forever preferred_lft forever
[root@client1 ~]# ip route show
192.168.101.0/24 dev eth0  proto kernel  scope link  src 192.168.101.101 
169.254.0.0/16 dev eth0  scope link  metric 1002 
default via 192.168.101.1 dev eth0 
[root@client1 ~]# ping -c 1 192.168.101.1 && ping -c 1 4.2.2.2
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.333 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.333/0.333/0.333/0.000 ms
PING 4.2.2.2 (4.2.2.2) 56(84) bytes of data.

--- 4.2.2.2 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 10000ms
```

Here is some of the functionality that IPTables provides:

```bash
[root@server1 ~]# iptables --help
iptables v1.4.7

Usage: iptables -[AD] chain rule-specification [options]
       iptables -I chain [rulenum] rule-specification [options]
       iptables -R chain rulenum rule-specification [options]
       iptables -D chain rulenum [options]
       iptables -[LS] [chain [rulenum]] [options]
       iptables -[FZ] [chain] [options]
       iptables -[NX] chain
       iptables -E old-chain-name new-chain-name
       iptables -P chain target [options]
       iptables -h (print this help information)

Commands:
Either long or short options are allowed.
  --append  -A chain  Append to chain
  --delete  -D chain  Delete matching rule from chain
  --delete  -D chain rulenum
    Delete rule rulenum (1 = first) from chain
  --insert  -I chain [rulenum]
    Insert in chain as rulenum (default 1=first)
  --replace -R chain rulenum
    Replace rule rulenum (1 = first) in chain
  --list    -L [chain [rulenum]]
    List the rules in a chain or all chains
  --list-rules -S [chain [rulenum]]
    Print the rules in a chain or all chains
  --flush   -F [chain]  Delete all rules in  chain or all chains
  --zero    -Z [chain [rulenum]]
    Zero counters in chain or all chains
  --new     -N chain  Create a new user-defined chain
  --delete-chain
            -X [chain]  Delete a user-defined chain
  --policy  -P chain target
    Change policy on chain to target
  --rename-chain
            -E old-chain new-chain
    Change chain name, (moving any references)
Options:
[!] --proto -p proto protocol: by number or name, eg. `tcp'
[!] --source -s address[/mask][...]
    source specification
[!] --destination -d address[/mask][...]
    destination specification
[!] --in-interface -i input name[+]
    network interface name ([+] for wildcard)
 --jump -j target
    target for rule (may load target extension)
  --goto      -g chain
                              jump to chain with no return
  --match -m match
    extended match (may load extension)
  --numeric -n  numeric output of addresses and ports
[!] --out-interface -o output name[+]
    network interface name ([+] for wildcard)
  --table -t table table to manipulate (default: `filter')
  --verbose -v  verbose mode
  --line-numbers  print line numbers when listing
  --exact -x  expand numbers (display exact values)
[!] --fragment -f  match second or further fragments only
  --modprobe=  try to insert modules using this command
  --set-counters PKTS BYTES set the counter during insert/append
[!] --version -V  print package version.
```

The remaining functionality can be found in 'man iptables'. There is A LOT of functionality! However, the RHCE objectives state that you should be able to create a packet filtering firewall. Note that it doesn't state anything about needing to create a modern stateful packet inspection firewall. It also states that you should be able to create a NAT.

Let's start with a packet filtering firewall. IPtables reads the rules from the top down and will process it's responses based upon the first matching rule.

In this first example. I created two rules. The first one blocks all ICMP traffic from 192.168.101.101 (client1), while the second permits all ICMP traffic from 192.168.101.102 (client2).

```bash
[root@server1 ~]# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
[root@server1 ~]# ping -c 1 192.168.101.101
PING 192.168.101.101 (192.168.101.101) 56(84) bytes of data.
64 bytes from 192.168.101.101: icmp_seq=1 ttl=64 time=0.434 ms

--- 192.168.101.101 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.434/0.434/0.434/0.000 ms
[root@server1 ~]# ping -c 1 192.168.101.102
PING 192.168.101.102 (192.168.101.102) 56(84) bytes of data.
64 bytes from 192.168.101.102: icmp_seq=1 ttl=64 time=0.263 ms

--- 192.168.101.102 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.263/0.263/0.263/0.000 ms
[root@server1 ~]# iptables -I INPUT -s 192.168.101.101/32 -p icmp -j REJECT
[root@server1 ~]# iptables -I INPUT -s 192.168.101.102/32 -p icmp -j ACCEPT
[root@server1 ~]# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     icmp --  192.168.101.102      anywhere            
REJECT     icmp --  192.168.101.101      anywhere            reject-with icmp-port-unreachable 

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
[root@server1 ~]# ping -c 1 192.168.101.101
PING 192.168.101.101 (192.168.101.101) 56(84) bytes of data.

--- 192.168.101.101 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 10000ms

[root@server1 ~]# ping -c 1 192.168.101.102
PING 192.168.101.102 (192.168.101.102) 56(84) bytes of data.
64 bytes from 192.168.101.102: icmp_seq=1 ttl=64 time=0.569 ms

--- 192.168.101.102 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.569/0.569/0.569/0.000 ms
```

As you can see in the example above, I started out with a default, permit anything, rule set. I then verified that I could ping both client1 and client2. Finally, I applied the two rules and attempted to ping the hosts again. The ping request to client1 failed, while was successful on client2.

Now, why did the server fail to ping client1 when we wanted pings from client1 to server1 to fail? The answer is that when server1 sent a ping (echo-request), client1 responded to the ping (echo). Since the rule blocks ALL icmp types. The rule blocked the response (echo) from client1, but allowed the echo-request from server1.

Below are the attempted ping requests from client1 and client2 before and after I applied the firewall rules to block icmp.

```bash
###Before###
[root@client1 ~]# ping -c 1 192.168.101.1
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.320 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.320/0.320/0.320/0.000 ms
[root@client1 ~]# ping -c 1 192.168.101.102
PING 192.168.101.102 (192.168.101.102) 56(84) bytes of data.
64 bytes from 192.168.101.102: icmp_seq=1 ttl=64 time=1.16 ms

--- 192.168.101.102 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 1ms
rtt min/avg/max/mdev = 1.166/1.166/1.166/0.000 ms
###After###
[root@client1 ~]# ping -c 1 192.168.101.1
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
From 192.168.101.1 icmp_seq=1 Destination Port Unreachable

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms

[root@client1 ~]# ping -c 1 192.168.101.102
PING 192.168.101.102 (192.168.101.102) 56(84) bytes of data.
64 bytes from 192.168.101.102: icmp_seq=1 ttl=64 time=0.270 ms

--- 192.168.101.102 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.270/0.270/0.270/0.000 ms



###Before###
[root@client2 ~]# ping -c 1 192.168.101.1
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.526 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.526/0.526/0.526/0.000 ms
[root@client2 ~]# ping -c 1 192.168.101.101
PING 192.168.101.101 (192.168.101.101) 56(84) bytes of data.
64 bytes from 192.168.101.101: icmp_seq=1 ttl=64 time=0.236 ms

--- 192.168.101.101 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.236/0.236/0.236/0.000 ms
###After###
[root@client2 ~]# ping -c 1 192.168.101.1
PING 192.168.101.1 (192.168.101.1) 56(84) bytes of data.
64 bytes from 192.168.101.1: icmp_seq=1 ttl=64 time=0.531 ms

--- 192.168.101.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.531/0.531/0.531/0.000 ms
[root@client2 ~]# ping -c 1 192.168.101.101
PING 192.168.101.101 (192.168.101.101) 56(84) bytes of data.
64 bytes from 192.168.101.101: icmp_seq=1 ttl=64 time=0.749 ms

--- 192.168.101.101 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.749/0.749/0.749/0.000 ms
```

Let's break down the IPTables ruleset:

```bash
iptables -I INPUT -s 192.168.101.101/32 -p icmp -j REJECT
```

Directly after the iptables command, you have the '-I' switch followed by the word INPUT. iptables `-I INPUT`.

The -I option specifies insert and INPUT is the chain name. INPUT is for incoming traffic.

Here are some other options:

```bash
  --append  -A chain  Append to chain
  --delete  -D chain  Delete matching rule from chain
  --delete  -D chain rulenum
    Delete rule rulenum (1 = first) from chain
  --insert  -I chain [rulenum]
    Insert in chain as rulenum (default 1=first)
  --replace -R chain rulenum
    Replace rule rulenum (1 = first) in chain
  --list    -L [chain [rulenum]]
    List the rules in a chain or all chains
  --list-rules -S [chain [rulenum]]
    Print the rules in a chain or all chains
  --flush   -F [chain]  Delete all rules in  chain or all chains
  --zero    -Z [chain [rulenum]]
    Zero counters in chain or all chains
  --new     -N chain  Create a new user-defined chain
  --delete-chain
            -X [chain]  Delete a user-defined chain
  --policy  -P chain target
    Change policy on chain to target
  --rename-chain
            -E old-chain new-chain
    Change chain name, (moving any references)
```

Be default, in the `filter` table there are three chains. Those types are INPUT, FORWARD, and OUTPUT. In the `nat` table there are PREROUTING, POSTROUTING, and OUTPUT. You can also create new chains with the -N switch.

The next option was to specify a source with `-s 192.168.101.101/32`. With this you can specify entire subnets, individual IP Addresses, hostname, or you can get creative and specify custom chains with groups of addresses. Another common option is the -i option, which lets you specify the incoming interface.

After specifying a source you need to specify a destination. If the -d is left off, all traffic will hit the filter. Next is the protocol with the -p option. In this case, `-p icmp`. You can use tcp, udp, udplite, icmp, esp, ah, sctp, or all as protocols. With tcp or udp, you will also specify port numbers with the --dport or --sport option, depending on source or destination port. You can specify a single port like `--dport 22`, a range of ports like `--dport 20:23`, or individual ports like `--dport 21,22,25`.

Lastly, you decide what to do with the traffic with the -j option. The most common options are ACCEPT, DROP, and REJECT. In this case I decided to accept the traffic. `-j ACCEPT`.

As this was a rather long section. I'll split this into two parts. Part two will cover NAT.
