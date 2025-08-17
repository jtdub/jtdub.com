---
layout: post
title: VLAN Trunking Protocol
date: '2010-07-27'
author: jtdub
tags:
- LAN Switching
- CCNA Study Notes
- CCNP Study Notes
- VTP
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

VLAN Trunking Protocol, aka VTP, is a Cisco proprietary protocol that allows Cisco switches to manage your VLAN database across all switches in your LAN through a central switch. This is done via a client / server environment.

A switch can operate in three VTP modes. The first is server mode. This is the VTP server which hosts the VLAN database and other switches on the LAN communicate to obtain a copy of the VTP database. In server mode, a network admin can add and remove VLANs at will.

The second is client mode. This is a VTP client. These switches communicate with the VTP server to obtain the database. A network admin can not add or remove VLANs manually from a switch in client mode.

And finally the the third mode is transparent mode. In transparent mode, the switch does not communicate with the VTP server and does not act as a VTP client. The network admin can add and remove VLANs from a switch in transparent mode and it will also allow VTP traffic to pass through it to other switches participating in the VTP domain.

Misconfigured, VTP can cause a major headache, but fortunately, troubleshooting VTP is pretty straight forward.

1. For VTP to propagate to switches in VTP client mode, they need to be connected as trunk ports. Switches connected together in access mode will not propagate any VTP changes.

2. The "Configuration Revision" number should be the highest on the server VTP switch. If the client has a higher revision number, then it will fail to obtain updates from the server. If a switch is introduced to the network that is running in VTP server mode, has the same VTP domain name as your server, and has the same password that you've setup in your VTP domain, then it will over-write your VLAN database throughout your network.

3. The "Configuration last modified" should list the IP Address of your VTP server switch. If it's not, then you have a rogue VTP server on your network.

```bash
accessswitch#sh vtp status
VTP Version                     : 2
Configuration Revision          : 9
Maximum VLANs supported locally : 255
Number of existing VLANs        : 8
VTP Operating Mode              : Client
VTP Domain Name                 : rad
VTP Pruning Mode                : Disabled
VTP V2 Mode                     : Enabled
VTP Traps Generation            : Disabled
MD5 digest                      : 0x01 0x00 0xE6 0x40 0xE3 0x87 0x06 0x8C 
Configuration last modified by 10.10.10.1 at 3-1-93 00:07:31
```
Fixing the issues are pretty straightforward, though may take a lot of manual input if you have a lot of VLANS.

1. If your client switches are not accepting updates from the server, verify that they are connected to the upstream switches via a trunking protocol. If that's correct, make sure that the "Configuration Revision" isn't higher than your VTP server. If it is, you can zero out the revision by changing to domain to null, changing the switch to server mode, then reconfiguring VTP in client mode.

2. If you have a rogue switch on the network that has taken over the role as VTP server, either remove the offending switch, or join it to the network in VTP client mode, then go to your VTP server and re-enter all your VLAN information in. 

*You do have your VLAN information documented, right?*

Other than that; use version 2, enable VTP pruning, use unique domain names, and use passwords on your VTP domain. If you're very paranoid, set all your switches to transparent mode and update the VLAN database on your switch infrastructure manually.

**Commands Sets:**

*User EXEC mode:*
* show vtp counters
* show vtp status
* show vlan

*Global Configuration mode:*

```bash
CSW1(config)#vtp ?
  domain     Set the name of the VTP administrative domain.
  file       Configure IFS filesystem file where VTP configuration is stored.
  interface  Configure interface as the preferred source for the VTP IP updater
             address.
  mode       Configure VTP device mode
  password   Set the password for the VTP administrative domain
  pruning    Set the adminstrative domain to permit pruning
  version    Set the adminstrative domain to VTP version
CSW1(config)#vlan ?
  WORD        ISL VLAN IDs 1-4094
  access-map  Create vlan access-map or enter vlan access-map command mode
  dot1q       dot1q parameters
  filter      Apply a VLAN Map
  internal    internal VLAN
```

*VLAN Configuration mode:*

```bash
CSW1(config-vlan)#?
VLAN configuration commands:
  are           Maximum number of All Route Explorer hops for this VLAN (or
                zero if none specified)
  backupcrf     Backup CRF mode of the VLAN
  bridge        Bridging characteristics of the VLAN
  exit          Apply changes, bump revision number, and exit mode
  media         Media type of the VLAN
  mtu           VLAN Maximum Transmission Unit
  name          Ascii name of the VLAN
  no            Negate a command or set its defaults
  parent        ID number of the Parent VLAN of FDDI or Token Ring type VLANs
  private-vlan  Configure a private VLAN
  remote-span   Configure as Remote SPAN VLAN
  ring          Ring number of FDDI or Token Ring type VLANs
  said          IEEE 802.10 SAID
  shutdown      Shutdown VLAN switching
  state         Operational state of the VLAN
  ste           Maximum number of Spanning Tree Explorer hops for this VLAN (or
                zero if none specified)
  stp           Spanning tree characteristics of the VLAN
  tb-vlan1      ID number of the first translational VLAN for this VLAN (or
                zero if none)
  tb-vlan2      ID number of the second translational VLAN for this VLAN (or
                zero if none)
```
