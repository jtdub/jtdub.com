---
layout: post
title: A New Approach to Defending Against DDoS Attacks
date: '2016-10-21'
author: jtdub
tags:
- network security
- DDoS
- Security
- Miscellaneous Hacking
- Net Nuetrality
- Network Connectivity
- packetgeek.net
---

DDoS (Distributed Denial of Service) attacks are getting larger, more sophisticated, and more pervasive. Just today (October 21, 2016), DDoS attacks against [Dyn, Inc](http://dyn.com/) have impacted the availability of sites such as [Twitter](https://twitter.com/), [Netflix](https://www.netflix.com/browse), [Github](https://github.com/), and [Spotify](https://www.spotify.com/us/).

Typical DDoS mitigation strategies rely on defending the victim (destination) as close to the destination as possible. This can happen in a number of ways.

One defense strategy is to redirect traffic, destined to the victim, through an alternative network that is designed to identify malicious traffic, drop the malicious traffic, before sending the legitimate traffic to the victim. This generally works well for volumetric or protocol based attacks. However, this requires that a network with a vast amount of capacity be available and sitting idle, except in times of attacks.

Another defense strategy is to utilize network and application firewalls, sitting in front of the destination, to identify the malicious traffic and drop it before sending the legitimate traffic to the destination. This generally works fine for some protocol and application based attacks.

Then, in some cases, volumetric attacks are so large, that they completely overwhelm the destination network. In this case, they use a BGP community, known as Remote Triggered Black Holes (RTBH) to tell their upstream service providers to drop traffic destined to the victim before it even reaches the destination network. In this case, the victim is sacrificed for the availability of rest of the network. This is typically the worst case scenario, as the victim still goes offline, conceding a victory to the attacker.

These countermeasures obviously are not going to scale with ever growing attacks. This is why we need the architects and builders of the Internet to come together to standardize on a new method of defending against the these attacks. We need a global community of real time analytics that identify malicious sources and use RTBH techniques to automatically take the offending sources off the Internet, instead of the victims. This technique will require that every Internet provider agree on a standard, and abide by it.
