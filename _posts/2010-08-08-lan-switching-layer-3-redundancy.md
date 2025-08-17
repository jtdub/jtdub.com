---
layout: post
title: LAN Switching Layer 3 Redundancy Protocols
date: '2010-08-08'
author: jtdub
tags:
- GLBP
- High Availability
- LAN Switching
- CCNP Study Notes
- HSRP
- Layer 3 Switching
- VRRP
- packetgeek.net
---

<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

#### HSRP

[Hot Standby Routing Protocol](http://www.cisco.com/en/US/tech/tk648/tk362/tk321/tsd_technology_support_sub-protocol_home.html), or HSRP, is a Cisco proprietary redundancy routing protocol. It's typically used in the distribution layer of a LAN. It works is by having two or more layer three devices that communicate with each other via multicast address 224.0.0.2 to UDP port 1985. In a typical configuration there will be a active router and a standby router. Each router has it's own physical IP Address and they share a virtual IP Address, which hosts on the LAN use as their default gateway. If the standby router detects that the active router is unavailable, then it will assume the active router role by assigning itself the virtual IP Address. There can only be a single active router in an HSRP group, but there can be multiple standby routers.

HSRP has an election process to determine which router is used as the active router. The router configured with the highest HSRP priority is determined to be the active router. In the event of multiple routers with identical priorities, then the router with the highest IP Address wins the active router election.

The preempt option in HSRP enables a router to resume the forwarding router role.

The hello default is 3 seconds and the hold time default is 10 seconds. When changing the default hello and hold times, the hold time would be at least three times the value of the hello timer.

HSRP is defined by RFC 2281..

**Active Router Interface Config**

```bash
interface FastEthernet0/0
 ip address 10.10.10.3 255.255.255.0
 duplex auto
 speed auto
 standby 1 ip 10.10.10.1
 standby 1 priority 150
 standby 1 preempt
end
```

**Active Router show output**

```bash
host-vlan3#show standby
FastEthernet0/0 - Group 1
  State is Active
    9 state changes, last state change 00:13:44
  Virtual IP address is 10.10.10.1
  Active virtual MAC address is 0000.0c07.ac01
    Local virtual MAC address is 0000.0c07.ac01 (default)
  Hello time 3 sec, hold time 10 sec
    Next hello sent in 0.520 secs
  Preemption enabled
  Active router is local
  Standby router is 10.10.10.2, priority 120 (expires in 8.253 sec)
  Priority 150 (configured 150)
  IP redundancy name is "hsrp-Fa0/0-1" (default)
```

**Standby Router Interface Config**

```bash
interface FastEthernet0/0
 ip address 10.10.10.2 255.255.255.0
 duplex auto
 speed auto
 standby 1 ip 10.10.10.1
 standby 1 priority 120
end
```

**Standby Router show output**

```bash
host-vlan2#show standby
FastEthernet0/0 - Group 1
  State is Standby
    10 state changes, last state change 00:12:07
  Virtual IP address is 10.10.10.1
  Active virtual MAC address is 0000.0c07.ac01
    Local virtual MAC address is 0000.0c07.ac01 (default)
  Hello time 3 sec, hold time 10 sec
    Next hello sent in 1.476 secs
  Preemption disabled
  Active router is 10.10.10.3, priority 150 (expires in 7.712 sec)
  Standby router is local
  Priority 120 (configured 120)
  IP redundancy name is "hsrp-Fa0/0-1" (default)
```

**Output from sh ip arp**

```bash
host-vlan2#show ip arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.10.10.2              -   000a.b7e9.8180  ARPA   FastEthernet0/0
Internet  10.10.10.3             38   000f.8f6d.ab60  ARPA   FastEthernet0/0
Internet  10.10.10.1              0   0000.0c07.ac01  ARPA   FastEthernet0/0
```

In some instances, your routers participating in an HSRP group connect to different devices on their uplinks. If HSRP doesn't have any method of tracking when there is an uplink failure, then HSRP doesn't do a very good job of maintaining an active connection to external resources. In those cases, you should implement interface tracking in HSRP. This is done using the `standby 1 track uplink interface priority decrement` command on the HSRP interface.

The `uplink interface` is the interface on your router that you want HSRP to monitor it's status. This interface would connect to the upstream device and probably isn't participating in HSRP directly. It's important to want to track the status of the interface so that HSRP can fail over to the other router in the event of a uplink failure.

The `priority decrement` is how much HSRP should automatically decrement it's priority to make the interface go into standby. This value should lower the value enough to no longer be the highest priority in the HSRP group.

Here is the debug output from the standby router going into active mode, as the primary active router becomes unavailable (via the "shut" command on the interface) and then becomes the standby router again.

```bash
host-vlan2#debug standby
HSRP debugging is on
*Mar  5 22:12:57.990: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:12:58.186: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:13:00.990: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:13:01.186: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:13:03.994: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:13:04.186: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:13:06.994: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:13:07.186: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:13:10.186: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:13:13.186: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:13:16.186: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:13:16.994: HSRP: Fa0/0 Grp 1 Standby: c/Active timer expired (10.10.10.3)
*Mar  5 22:13:16.994: HSRP: Fa0/0 Grp 1 Active router is local, was 10.10.10.3
*Mar  5 22:13:16.994: HSRP: Fa0/0 Grp 1 Standby router is unknown, was local
*Mar  5 22:13:16.994: HSRP: Fa0/0 Grp 1 Standby -> Active
*Mar  5 22:13:16.994: %HSRP-6-STATECHANGE: FastEthernet0/0 Grp 1 state Standby -> Active
*Mar  5 22:13:16.994: HSRP: Fa0/0 Grp 1 Redundancy "hsrp-Fa0/0-1" state Standby -> Active
*Mar  5 22:13:16.994: HSRP: Fa0/0 Redirect adv out, Active, active 1 passive 1
*Mar  5 22:13:16.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:19.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:19.998: HSRP: Fa0/0 Grp 1 Redundancy group hsrp-Fa0/0-1 state Active -> Active
*Mar  5 22:13:22.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:22.998: HSRP: Fa0/0 Grp 1 Redundancy group hsrp-Fa0/0-1 state Active -> Active
*Mar  5 22:13:25.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:28.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:31.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:34.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:37.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:40.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:43.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:46.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:49.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:51.798: HSRP: Fa0/0 REDIRECT adv in, Passive, active 0, passive 1, from 10.10.10.3
*Mar  5 22:13:52.998: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Active  pri 120 vIP 10.10.10.1
*Mar  5 22:13:53.002: HSRP: Fa0/0 REDIRECT adv in, Active, active 1, passive 2, from 10.10.10.3
*Mar  5 22:13:53.002: HSRP: Fa0/0 Grp 1 Coup   in  10.10.10.3 Listen  pri 150 vIP 10.10.10.1
*Mar  5 22:13:53.002: HSRP: Fa0/0 Grp 1 Active: j/Coup rcvd from higher pri router (150/10.10.10.3)
*Mar  5 22:13:53.002: HSRP: Fa0/0 Grp 1 Active router is 10.10.10.3, was local
*Mar  5 22:13:53.002: HSRP: Fa0/0 Grp 1 Active -> Speak
*Mar  5 22:13:53.002: %HSRP-6-STATECHANGE: FastEthernet0/0 Grp 1 state Active -> Speak
*Mar  5 22:13:53.002: HSRP: Fa0/0 Grp 1 Redundancy "hsrp-Fa0/0-1" state Active -> Speak
*Mar  5 22:13:53.006: HSRP: Fa0/0 Redirect adv out, Passive, active 0 passive 1
*Mar  5 22:13:53.006: HSRP: Fa0/0 API MAC address update
*Mar  5 22:13:53.006: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Speak   pri 120 vIP 10.10.10.1
*Mar  5 22:13:53.010: HSRP: Fa0/0 REDIRECT adv in, Active, active 1, passive 1, from 10.10.10.3
*Mar  5 22:13:53.010: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:13:55.998: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:13:56.006: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Speak   pri 120 vIP 10.10.10.1
*Mar  5 22:13:58.998: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:13:59.006: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Speak   pri 120 vIP 10.10.10.1
*Mar  5 22:14:02.002: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:14:02.006: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Speak   pri 120 vIP 10.10.10.1
*Mar  5 22:14:03.002: HSRP: Fa0/0 Grp 1 Speak: d/Standby timer expired (unknown)
*Mar  5 22:14:03.002: HSRP: Fa0/0 Grp 1 Standby router is local
*Mar  5 22:14:03.002: HSRP: Fa0/0 Grp 1 Speak -> Standby
*Mar  5 22:14:03.002: HSRP: Fa0/0 Grp 1 Redundancy "hsrp-Fa0/0-1" state Speak -> Standby
*Mar  5 22:14:03.002: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:14:05.002: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:14:06.002: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:14:08.002: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:14:09.002: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:14:11.002: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:14:12.002: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
*Mar  5 22:14:14.006: HSRP: Fa0/0 Grp 1 Hello  in  10.10.10.3 Active  pri 150 vIP 10.10.10.1
*Mar  5 22:14:15.002: HSRP: Fa0/0 Grp 1 Hello  out 10.10.10.2 Standby pri 120 vIP 10.10.10.1
```

#### VRRP

[Virtual Routing Redundancy Protocol](http://www.cisco.com/en/US/docs/ios/12_0st/12_0st18/feature/guide/st_vrrpx.html), or VRRP, serves the same purpose as HSRP, with many of the same features, but is an IEEE standard.

VRRP is defined by [RFC 2338](http://www.faqs.org/rfcs/rfc2338.html).

**Master VRRP Router Interface Config**

```bash
interface FastEthernet0/0
 ip address 10.10.10.3 255.255.255.0
 duplex auto
 speed auto
 vrrp 1 ip 10.10.10.1
 vrrp 1 priority 150
end
```

**Master VRRP Router sh output**

```bash
host-vlan3#sh vrrp
FastEthernet0/0 - Group 1
  State is Master
  Virtual IP address is 10.10.10.1
  Virtual MAC address is 0000.5e00.0101
  Advertisement interval is 1.000 sec
  Preemption is enabled
    min delay is 0.000 sec
 Priority is 150
  Master Router is 10.10.10.3 (local), priority is 150
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.414 sec
```

**Backup VRRP Router Interface config**

```bash
interface FastEthernet0/0
 ip address 10.10.10.2 255.255.255.0
 duplex auto
 speed auto
 vrrp 1 ip 10.10.10.1
 vrrp 1 priority 120
end


**Backup VRRP Router sh output**

```bash
host-vlan2#sh vrrp
FastEthernet0/0 - Group 1
  State is Backup
  Virtual IP address is 10.10.10.1
  Virtual MAC address is 0000.5e00.0101
  Advertisement interval is 1.000 sec
  Preemption enabled
  Priority is 120
  Master Router is 10.10.10.3, priority is 150
  Master Advertisement interval is 1.000 sec
  Master Down interval is 3.531 sec (expires in 2.683 sec)
```

Here is the output of the backup vrrp router turning into a master and then backup again.

```bash
host-vlan2#debug vrrp
VRRP debugging is on
*Mar  5 22:27:32.954: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:32.954: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:33.958: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:33.958: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:34.958: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:34.958: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:35.958: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:35.962: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:36.962: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:36.962: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:37.962: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:37.962: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:38.966: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:38.966: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:39.966: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:39.966: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:40.970: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:27:40.970: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:27:44.502: VRRP: Grp 1 Event - Master down timer expired
*Mar  5 22:27:44.502: %VRRP-6-STATECHANGE: Fa0/0 Grp 1 state Backup -> Master
*Mar  5 22:27:44.502: VRRP: tbridge_smf_update failed
*Mar  5 22:27:44.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:45.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:46.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:47.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:48.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:49.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:50.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:51.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:52.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:53.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:54.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:55.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:56.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:57.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:58.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:27:59.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:00.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:01.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:02.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:03.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:04.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:05.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:06.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:07.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:08.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:09.502: VRRP: Grp 1 sending Advertisement checksum 52F1
*Mar  5 22:28:09.970: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:28:09.970: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:28:09.970: %VRRP-6-STATECHANGE: Fa0/0 Grp 1 state Master -> Backup
*Mar  5 22:28:10.970: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:28:10.970: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:28:11.974: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:28:11.974: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:28:12.974: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:28:12.974: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:28:13.974: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:28:13.974: VRRP: Grp 1 Event - Advert higher or equal priority
*Mar  5 22:28:14.978: VRRP: Grp 1 Advertisement priority 150, ipaddr 10.10.10.3
*Mar  5 22:28:14.978: VRRP: Grp 1 Event - Advert higher or equal priority
```

It doesn't appear that VRRP has the ability to perform interface tracking, but could be an option to use in multi-vendor networks.

#### GLBP

[Gateway Load Balancing Protocol](http://www.cisco.com/en/US/docs/ios/12_2t/12_2t15/feature/guide/ft_glbp.html), or GLBP, is another Cisco proprietary protocol. It was created with the idea of better utilizing the network resources while still performing the same functionality as HSSRP and VRRP. GLBP performs automatic selection and simultaneous use of multiple available gateways as well as automatic failover in the event of a failure. With HSRP and VRRP, the load balancing and attempt to fully utilize available network resources is a manual process and be burdensome on the network administrator.

GLBP communicates via multicast address 224.0.0.102 to UDP 3222.

**Active Router Interface Config**

```bash
interface FastEthernet0/0
 ip address 10.10.10.3 255.255.255.0
 duplex auto
 speed auto
 glbp 1 ip 10.10.10.1
 glbp 1 priority 150
 glbp 1 preempt
end
```

**Active Router sh output**

```bash
host-vlan3#sh glbp
FastEthernet0/0 - Group 1
  State is Active
    2 state changes, last state change 00:08:28
  Virtual IP address is 10.10.10.1
  Hello time 3 sec, hold time 10 sec
    Next hello sent in 1.453 secs
  Redirect time 600 sec, forwarder time-out 14400 sec
  Preemption disabled
  Active is local
  Standby is 10.10.10.2, priority 120 (expires in 7.664 sec)
  Priority 150 (configured)
  Weighting 100 (default 100), thresholds: lower 1, upper 100
  Load balancing: round-robin
  There are 2 forwarders (1 active)
  Forwarder 1
    State is Active
      1 state change, last state change 00:08:18
    MAC address is 0007.b400.0101 (default)
    Owner ID is 000f.8f6d.ab60
    Redirection enabled
    Preemption enabled, min delay 30 sec
    Active is local, weighting 100
  Forwarder 2
    State is Listen
    MAC address is 0007.b400.0102 (learnt)
    Owner ID is 000a.b7e9.8180
    Redirection enabled, 599.343 sec remaining (maximum 600 sec)
    Time to live: 14399.343 sec (maximum 14400 sec)
    Preemption enabled, min delay 30 sec
    Active is 10.10.10.2 (primary), weighting 100 (expires in 9.343 sec)
```

**Active Router *sh ip arp* output**

```bash
host-vlan3#sh ip arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.10.10.2              8   000a.b7e9.8180  ARPA   FastEthernet0/0
Internet  10.10.10.3              -   000f.8f6d.ab60  ARPA   FastEthernet0/0
Internet  10.10.10.1              -   0007.b400.0101  ARPA   FastEthernet0/0
```

**Standby Router Interface Config**

```bash
interface FastEthernet0/0
 ip address 10.10.10.2 255.255.255.0
 duplex auto
 speed auto
 glbp 1 ip 10.10.10.1
 glbp 1 priority 120
end
```

**Standby Router sh output**

```bash
host-vlan2#sh glbp
FastEthernet0/0 - Group 1
  State is Standby
    1 state change, last state change 00:04:17
  Virtual IP address is 10.10.10.1
  Hello time 3 sec, hold time 10 sec
    Next hello sent in 0.836 secs
  Redirect time 600 sec, forwarder time-out 14400 sec
  Preemption disabled
  Active is 10.10.10.3, priority 150 (expires in 8.456 sec)
  Standby is local
  Priority 120 (configured)
  Weighting 100 (default 100), thresholds: lower 1, upper 100
  Load balancing: round-robin
  There are 2 forwarders (1 active)
  Forwarder 1
    State is Listen
    MAC address is 0007.b400.0101 (learnt)
    Owner ID is 000f.8f6d.ab60
    Time to live: 14398.452 sec (maximum 14400 sec)
    Preemption enabled, min delay 30 sec
    Active is 10.10.10.3 (primary), weighting 100 (expires in 8.452 sec)
  Forwarder 2
    State is Active
      1 state change, last state change 00:04:22
    MAC address is 0007.b400.0102 (default)
    Owner ID is 000a.b7e9.8180
    Preemption enabled, min delay 30 sec
    Active is local, weighting 100
```

**Standby Router *sh ip arp* output**

```bash
host-vlan2#sh ip arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.10.10.2              -   000a.b7e9.8180  ARPA   FastEthernet0/0
Internet  10.10.10.3              5   000f.8f6d.ab60  ARPA   FastEthernet0/0
Internet  10.10.10.1              -   0007.b400.0102  ARPA   FastEthernet0/0
```

Here is the output from a debug from the standby router. As you can see GLBP load balances by continuously moving the virutal IP Address from one router to the other. You can also see where the standby router becomes active in a failure, then becomes standby again.

```bash
host-vlan2#debug glbp
GLBP debugging is on
*Mar  5 22:57:22.550: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:57:24.630: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:25.550: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:57:27.630: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:28.550: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:57:30.630: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:33.630: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:36.630: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:38.554: GLBP: Fa0/0 1 Standby: g/Active timer expired (10.10.10.3)
*Mar  5 22:57:38.554: GLBP: Fa0/0 1 Active router IP is local, was 10.10.10.3
*Mar  5 22:57:38.554: GLBP: Fa0/0 1 Standby router is unknown, was local
*Mar  5 22:57:38.554: GLBP: Fa0/0 1 Standby -> Active
*Mar  5 22:57:38.554: %GLBP-6-STATECHANGE: FastEthernet0/0 Grp 1 state Standby -> Active
*Mar  5 22:57:38.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:38.554: GLBP: Fa0/0 1.1 Listen: g/Active timer expired
*Mar  5 22:57:38.558: GLBP: Fa0/0 1.1 Listen -> Active
*Mar  5 22:57:38.558: %GLBP-6-FWDSTATECHANGE: FastEthernet0/0 Grp 1 Fwd 1 state Listen -> Active
*Mar  5 22:57:38.558: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VF 1 Active  pri 135 vMAC 0007.b400.0101
*Mar  5 22:57:41.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:44.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:47.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:50.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:53.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:56.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:57:59.554: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:02.558: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:05.562: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:08.562: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:08.562: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Speak   pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:11.562: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Active  pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:11.562: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Speak   pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:11.566: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:11.566: GLBP: Fa0/0 1 Active router IP is 10.10.10.3, was local
*Mar  5 22:58:11.566: GLBP: Fa0/0 1 Active: k/Hello rcvd from higher pri Active router (150/10.10.10.3)
*Mar  5 22:58:11.566: GLBP: Fa0/0 1 Active -> Speak
*Mar  5 22:58:11.566: %GLBP-6-STATECHANGE: FastEthernet0/0 Grp 1 state Active -> Speak
*Mar  5 22:58:11.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Speak   pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:14.562: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:14.570: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Speak   pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:17.566: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:17.570: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Speak   pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:20.566: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:20.570: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Speak   pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:21.566: GLBP: Fa0/0 1 Speak: f/Standby timer expired (unknown)
*Mar  5 22:58:21.566: GLBP: Fa0/0 1 Standby router is local
*Mar  5 22:58:21.566: GLBP: Fa0/0 1 Speak -> Standby
*Mar  5 22:58:21.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:23.566: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:24.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:26.566: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:27.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:29.570: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000
*Mar  5 22:58:30.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 135 vMAC 0007.b400.0101 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:30.570: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:58:30.570: GLBP: Fa0/0 1.1 Active: i/Hello rcvd from higher pri Active router (167/10.10.10.3)
*Mar  5 22:58:30.570: GLBP: Fa0/0 1.1 Active -> Listen
*Mar  5 22:58:30.570: %GLBP-6-FWDSTATECHANGE: FastEthernet0/0 Grp 1 Fwd 1 state Active -> Listen
*Mar  5 22:58:30.570: GLBP: Fa0/0 API MAC address update
*Mar  5 22:58:32.570: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:58:33.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:35.570: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:58:36.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:38.570: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:58:39.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
*Mar  5 22:58:41.574: GLBP: Fa0/0 Grp 1 Hello  in  10.10.10.3 VG Active  pri 150 vIP 10.10.10.1 hello 3000, hold 10000 VF 1 Active  pri 167 vMAC 0007.b400.0101
*Mar  5 22:58:42.566: GLBP: Fa0/0 Grp 1 Hello  out 10.10.10.2 VG Standby pri 120 vIP 10.10.10.1 hello 3000, hold 10000 VF 2 Active  pri 167 vMAC 0007.b400.0102
```
