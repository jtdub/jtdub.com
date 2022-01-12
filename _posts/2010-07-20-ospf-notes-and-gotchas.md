---
layout: post
title: OSPF Notes and Gotchas
date: '2010-07-20'
author: jtdub
tags:
- Routing Protocols
- OSPF
- IGP's
- packetgeek.net
---

Open Shortest Path First (OSPF) is an open standard routing protocol that is used as an interior gateway routing protocol (IGP). Because OSPF is an open standard, it will inter-operate with many network gear vendors, with some configuration tweaks.

Link = Interface. Interfaces are added to OSFP via the network command.

Router ID = RID = an identifier. typically from a loopback interface or the highest ip address on a router. The router with the highest RID will be the router that propagates changes through the network. This router is called the designated router.  The router with the second highest RID will act as it's backup. This is called the backup designated router It's a best practice to add loopback interfaces with the highest IP Addresses being the core routers of the WAN. Use /32 addressing scheme in your loopback interfaces.

Neighbor = routers that have a common interface

Adjacency = a relationship that allows routers to share routing information

OSPF, by default, uses multicast or propagate changes to other adjacent routers. If your WAN doesn't support multicast then you will need to make two additional changes to your configuration. First you will need to setup your WAN interface as a non-broadcast interface. In Cisco routers you will issue the "ip ospf network non-broadcast" command. Then you will need to manually specify your adjacency neighbor relationships with the neighbor command in the OSPF process.

If you're using multi-vendor equipment for your OSPF routed WAN, then you will most likely need to manually specify Hello, Dead, and Wait timers.

With Cisco routers, by default, if a router loses adjacency (loses connection, hardware failure, software glitch, etc); it will take OSPF 40 seconds to propagate the routing changes through the network. It will either drop the route(s) completely if there isn't a redundant path or it will propagate an alternate path.
