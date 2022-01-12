---
layout: post
title: Cisco Zone Based Firewall and UDP based Traceroute
date: '2013-04-11'
author: jtdub
tags:
- IOS
- IOS Security
- Cisco Firewalls
- Cisco Zone Based Firewall
- packetgeek.net
---

I've been using the Cisco Zone Based Firewall features in IOS for a little while now. Mostly at home and in a lab environment. One of the things that was kind of frustrating was that was the lack of outbound traceroute support from the trusted network to the untrusted network. I only use Linux and MacOS X at work and at home, so I never tried it out with a Microsoft based computer. I've also haven't really been able to spend a lot of time to really debug the issue. Recently, I did some digging through the documentation on Cisco's website and it hit me and it was such a simple answer. Linux/UNIX based operating systems use a UDP method for sending traceroute packets, while Windows based operating systems use a ICMP based method. As UDP is a connectionless protocol and there isn't any method for keeping a state table for UDP packets in the firewall, you have to allow ICMP host-unreachables and time-exceeded packets IN to the untrusted interface, destined for the trusted network. Here is a sample configuration.

```bash
jtdub-rtr#sh run | s ^ip access-list extended udp-icmp|^class-map|^policy-map|^zone|^interface Vlan[1,2]|^interface FastEthernet0
class-map type inspect match-any UDP_ICMP
  match access-group name udp-icmp
class-map type inspect match-any All_Protocols
  match protocol icmp
  match protocol tcp
  match protocol udp
policy-map type inspect Traceroute
  class type inspect UDP_ICMP
   pass
  class class-default
   drop
policy-map type inspect All_Protocols
   class type inspect All_Protocols
    inspect 
  class class-default
   drop
policy-map type inspect UnTrusted
  class class-default
   drop
zone security Trusted
zone security Internet
zone-pair security Trusted source Trusted destination Internet
  service-policy type inspect All_Protocols
zone-pair security Internet source Internet destination Trusted
  service-policy type inspect Traceroute
interface FastEthernet0
  ip address dhcp
  ip verify unicast source reachable-via rx allow-default 101
  no ip redirects
  no ip unreachables
  no ip proxy-arp
  ip nbar protocol-discovery
  ip nat outside
  ip virtual-reassembly
  zone-member security Internet
  duplex auto
  speed auto
  no cdp enable
interface Vlan1
  ip address 172.16.1.1 255.255.255.0
  no ip redirects
  no ip unreachables
  no ip proxy-arp
  ip nat inside
  ip virtual-reassembly
  zone-member security Trusted
interface Vlan2
  ip address 172.16.2.1 255.255.255.0
  no ip redirects
  no ip unreachables
  no ip proxy-arp
  ip nat inside
  ip virtual-reassembly
  zone-member security Trusted
ip access-list extended udp-icmp
  permit icmp any any time-exceeded
  permit icmp any any host-unreachable
```

As you can see, there is an extended ip access-list called udp-icmp that permits time-exceeded and host-unreachable icmp types, then a class map called UDP_ICMP was created to match that access-list, Then a policy-map called Traceroute was created to allow that class-map, from there, the policy-map was applied to a zone-member and applied to the untrusted interface.
