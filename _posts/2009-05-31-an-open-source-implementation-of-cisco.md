---
layout: post
title: An Open Source Implementation of Cisco's Dynamic Multipoint VPN (DMVPN)
date: '2009-05-31'
author: jtdub
tags:
- VPN
- Open Source Alternatives
- packetgeek.net
---
For a few years, Cisco has had a pretty innovative VPN solution called "Dynamic Multipoint VPN". In essence, it's a traditional hub and spoke VPN design, except that when two, or more, spokes want to communicate directly with each other, they initiate a dynamic IPSEC tunnel with each other instead of sending the traffic to the hub, where the hub would route the traffic to the destination spoke. If you're confused, the "hub" would be the main office where all VPN sessions are initiated to and the "spoke" are the branch offices.


Why does this matter? There are two HUGE reasons: bandwidth and ease of operation. If two spokes need to send data back and forth to each other over the VPN, it doesn't make sense that the data should be sent from spoke 1, to the hub, to spoke 2. Doing this doubles the amount of Internet bandwidth that you need. That's a lot of wasted money. For the people configuring the VPN devices, it's an added complexity to add all kinds of VPN tunnels to each branch turning your VPN network into a mesh design. Could you imagine doing that with hundreds or thousands of branch offices? It would be an administration night mare. So essentially, either way you look at it, DMVPN could save your organization a ton of money in total cost of ownership and on bandwidth. Your network admins will love you for it.


How is DMVPN achieved? It uses all the same tricks as traditional hub and spoke VPN; IPSEC, GRE, a dynamic routing protocol, along with a fairly new protocol called Next Hop Resolution Protocol. "NHRP is an Address Resolution Protocol (ARP)-like protocol that dynamically maps nonbroadcast multiaccess (NBMA) network. With NHRP, systems attached to an NBMA network can dynamically learn the NBMA (physical) address of the other systems that are part of that network, allowing these systems to directly communicate." (Cisco.com) Pretty cool, right?


It now looks like the Open Source community is putting together the last piece of the DMVPN puzzle. For years there have been open source implementations of IPSEC, GRE, and dynamic routing protocols, such as OSPF. (It's a shame that EIGRP is proprietary to Cisco.) Now there is a NHRP implementation in the works, that looks promising. I'm sure that I'll be keeping up with the progress.


Maybe Vyatta will implement this? hmmm...


<a href="http://www.faqs.org/rfcs/rfc2332.html">
 RFC 2332 - NBMA Next Hop Resolution Protocol
</a>

Open Source Related Links:

<a href="http://sourceforge.net/projects/opennhrp">
 OpenNHRP
</a>

<a href="http://www.quagga.net/">
 Quagga Routing Software
</a>

<a href="http://www.linuxfoundation.org/en/Net%3AIproute2">
 Iproute2 - Open Source GRE implementation
</a>

<a href="http://www.strongswan.org/">
 StrongSwan - IPSEC for Linux
</a>

<a href="http://www.openswan.org/">
 OpenSwan - Another IPSEC for Linux
</a>

Cisco Related Links:

<a href="http://www.cisco.com/en/US/docs/ios/12_4/ip_addr/configuration/guide/hadnhrp_ps6350_TSD_Products_Configuration_Guide_Chapter.html">
 Cisco's implementation of NHRP
</a>

<a href="http://www.cisco.com/en/US/tech/tk583/tk372/technologies_configuration_example09186a008014bcd7.shtml">
 Configuring DMVPN using GRE over IPSEC between multiple routers
</a>

<a href="http://www.cisco.com/en/US/prod/collateral/iosswrel/ps6537/ps6586/ps6635/ps6658/DMVPN_Overview.pdf">
 DMVPN Overview
</a>
