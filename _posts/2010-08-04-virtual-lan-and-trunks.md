---
layout: post
title: Virtual LAN's and Trunks
date: '2010-08-04'
author: jtdub
tags:
- LAN Switching
- VLAN
- CCNA Study Notes
- VLAN Trunking
- CCNP Study Notes
- packetgeek.net
---

Virtual LAN, also known as VLAN, is exactly as it sounds. It's a method of having several virtual LAN's on a single switch or even on an enterprise campus LAN. It's completely driven by software and is strictly layer 2. Just as physical LAN's, you can connect VLAN's together with layer 3 devices, either routers or switches capable of providing layer three services.

A switch port can operate in three modes. Those modes are access, trunk and hybrid.

An access port is typically how ports are setup that connect to workstations, printers, etc. They can only be apart of a single vlan, with one exception. Hosts connected to access ports are oblivious to what vlan that they are on. Hosts can communicate with other hosts on the same vlan, but are not able to communicate with hosts on other vlan's with out passing through a layer three device, such as a router.

Now the one exception to an access port only being able to pass traffic for a single vlan is when an access port is configured with a voice vlan, as well as a data vlan. In this configuration an IP phone is plugged into the switch port and the PC is plugged into the phone. The switch port then puts voice traffic on one vlan and data on another vlan. This allows for better security as well as quality of service for the voice traffic.

Trunk ports generally are the connections between switches. They allow switches to pass multiple vlan's through them to other switches. That way you can have multiple vlan's that span many switches within a enterprise LAN. Trunks can also connect switches to routers, known as *router on a stick.* This allows a router to connect to multiple vlan's to route traffic through a single connection. Beware though, using a *router on a stick* configuration can significantly hinder your network performance as it will be the bottleneck of the network. The only instance where a *router on a stick* gains much use is for low traffic, small branch sites. Nowadays, layer 3 switches are used to route traffic internally on an enterprise.

There are a few different trunking protocols. In the Ethernet world, there are two methods; ISL and 802.1q. ISL stands for Inter-Switch Link and is a Cisco proprietary trunking protocol.

ISL:
* Only carries 1000 VLANs
* Encapsulates the frame, which add overhead
* Must be point-to-point
* does not have a separate QoS field

Since ISL encapsulates the entire frame it can support other protocols besides Ethernet. It can support Token Ring, FDDI, and ATM.

802.1q is an open standard trunking protocol. Since it's open, it can be used with multiple vendors. Rather than encapsulating the entire frame, 802.1q adds a tag to the existing Ethernet header. 802.1q had a priority field for better QoS support and has a rich protocol support. It can support:

* Ethernet
* Token Ring
* 4095 VLANs
* Common Spanning Tree
* Multiple Spanning Tree
* Rapid Spanning Tree

The native vlan is not tagged on the trunk.

**Command Sets:**

*Interface Configuration mode:*

```bash
CSW1(config-if)#switchport mode ?
  access        Set trunking mode to ACCESS unconditionally
  dot1q-tunnel  Set trunking mode to DOT1Q TUNNEL unconditionally
  dynamic       Set trunking mode to dynamically negotiate access or trunk mode
  trunk         Set trunking mode to TRUNK unconditionally

CSW1(config-if)#switchport access ?
  vlan  Set VLAN when interface is in access mode

CSW1(config-if)#switchport trunk ?
  allowed        Set allowed VLAN characteristics when interface is in trunking
                 mode
  encapsulation  Set trunking encapsulation when interface is in trunking mode
  native         Set trunking native characteristics when interface is in
                 trunking mode
  pruning        Set pruning VLAN characteristics when interface is in trunking
                 mode

CSW1(config-if)#switchport voice ?
  vlan  Vlan for voice traffic
```
