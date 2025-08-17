---
layout: post
title: Layer 3 LAN Switching
date: '2010-08-08'
author: jtdub
tags:
- LAN Switching
- CCNP Study Notes
- Layer 3 Switching
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

As enterprise LANs grow, there becomes a need to break up LANs with routers. Traditionally, routers have performed the layer 3 functionality, but in today's high-speed LANs there is a need to be able to forward packets much quicker than the traditional routers have been able to. That is where layer 3 switches come into play.

Layer 3 switches can turn on routing by executing the "ip routing" command from the global configuration mode. From there you can create routed interfaces either by using vlan interfaces, which is the likely interface at the distribution layer or on physical Ethernet interfaces by executing the "no switchport" command, then assigning the physical interface an IP Address.

With large networks, topology-based switches may still be too slow. Then you will need to utilize hardwre based layer 3 switching. In hardware based layer 3 switching, the switch can utilize Policy Feature Cards (PFC) and Distributed Feature Cards (DFC) to route traffic at the hardware level. The hardware will do a packet rewrite on the egress port and alter the following fields:

* Layer 2 (MAC) destination address
* Layer 2 (MAC) source address
* Layer 3 IP TTL
* Layer 3 checksum
* Layer 2 (MAC) checksum, aka FCS

Any packets that can't be handled by the hardware will then be sent to the switches MSFC (Multi-Layer Switch Feature Card), which is a software based router.

The switch that uses the PFC, DFC, and MSFC is the Catalyst 6500 switch. Hardware layer 3 switching does not replace routing and routing protocols. It provides IP unicast layer 3 switching locally on each module.

Chassis based switches utilize a centralized forwarding architecture, which enhances LAN performance and can become even better with the use of distributed forwarding as an upgrade.

When CEF (Cisco Express Forwarding) is used a chassis based switch can forward up to 30 mpps per system or when using a dCEF daughter card can deliver 48 mpps sustained throughput per slot.
