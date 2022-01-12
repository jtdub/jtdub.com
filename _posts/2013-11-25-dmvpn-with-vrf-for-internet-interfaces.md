---
layout: post
title: DMVPN with VRF's for the Internet interfaces and BGP
date: '2013-11-25'
author: jtdub
tags:
- DMVPN
- VRF
- BGP
- packetgeek.net
---

I've been playing with some different DMVPN configurations. In this scenario, I wanted the Internet facing interface to have a separate routing table, which I accomplished with a VRF. I also wanted to use a phase 2 DMVPN - which allows spokes to communicate directly to each other without having to send all traffic to the hub. The tricky part was getting the DMVPN tunnels to form over that interface. This is accomplished via the tunnel vrf command in the tunnel interface and specifying the vrf in the crypto keyring.

Here is my hub config:

```bash
DMVPN-HUB1-R1#$l0/0.102|interface Loopback0|interface Tunnel0|ip prefix-list 
ip vrf Internet
 rd 500:1
crypto keyring DMVPN vrf Internet
  pre-shared-key address 0.0.0.0 0.0.0.0 key test123
crypto isakmp policy 10
 authentication pre-share
 group 2
crypto ipsec transform-set DMVPN ah-sha-hmac esp-aes 256 
 mode transport
crypto ipsec profile DMVPN
 set transform-set DMVPN 
interface Loopback0
 ip vrf forwarding Internet
 ip address 151.0.0.1 255.255.255.0
interface Tunnel0
 bandwidth 1544
 ip address 10.0.1.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication test123
 ip nhrp map multicast dynamic
 ip nhrp network-id 1234
 ip tcp adjust-mss 1360
 load-interval 30
 cdp enable
 tunnel source Loopback0
 tunnel mode gre multipoint
 tunnel key 12345
 tunnel vrf Internet
 tunnel protection ipsec profile DMVPN
interface Serial0/0.102 point-to-point
 ip vrf forwarding Internet
 ip address 150.0.0.2 255.255.255.252
 frame-relay interface-dlci 102   
router bgp 500
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.0.1.2 remote-as 600
 neighbor 10.0.1.2 prefix-list TUN out
 no auto-summary
 !
 address-family ipv4 vrf Internet
  neighbor 150.0.0.1 remote-as 100
  neighbor 150.0.0.1 activate
  neighbor 150.0.0.1 send-community
  no synchronization
  network 151.0.0.0 mask 255.255.255.0
 exit-address-family
ip prefix-list BGP seq 5 permit 151.0.0.0/24
ip prefix-list TUN seq 5 permit 10.0.1.0/24
```

Here is my spoke config:

```bash
DMVPN-SPOKE1-R4#$interface Serial0/1/0|interface Tunnel0|interface Loopback0 
ip vrf Internet
 rd 600:1
crypto keyring DMVPN vrf Internet
  pre-shared-key address 0.0.0.0 0.0.0.0 key test123
crypto isakmp policy 10
 authentication pre-share
 group 2
crypto ipsec transform-set DMVPN ah-sha-hmac esp-aes 256 
 mode transport
crypto ipsec profile DMVPN
 set transform-set DMVPN 
interface Loopback0
 ip vrf forwarding Internet
 ip address 152.0.0.1 255.255.255.0
interface Tunnel0
 bandwidth 1544
 ip address 10.0.1.2 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication test123
 ip nhrp map multicast dynamic
 ip nhrp map 10.0.1.1 151.0.0.1
 ip nhrp map multicast 151.0.0.1
 ip nhrp network-id 1234
 ip nhrp nhs 10.0.1.1
 ip tcp adjust-mss 1360
 load-interval 30
 cdp enable
 tunnel source Loopback0
 tunnel mode gre multipoint
 tunnel key 12345
 tunnel vrf Internet
 tunnel protection ipsec profile DMVPN
interface Serial0/1/0
 ip vrf forwarding Internet
 ip address 150.0.0.10 255.255.255.252
 encapsulation ppp
 clock rate 1024000
router bgp 600
 no synchronization
 bgp router-id 152.0.0.1
 bgp log-neighbor-changes
 neighbor 10.0.1.1 remote-as 500
 neighbor 10.0.1.1 prefix-list TUN out
 no auto-summary
 !
 address-family ipv4 vrf Internet
  neighbor 150.0.0.9 remote-as 100
  neighbor 150.0.0.9 activate
  no synchronization
  network 152.0.0.0 mask 255.255.255.0
 exit-address-family
ip prefix-list BGP seq 5 permit 152.0.0.0/24
ip prefix-list TUN seq 5 permit 10.0.1.0/24
```

One of the scenarios that I wanted to play with was having BGP dynamically create peers. However, my specific version of code doesn't support dynamic BGP peers. If my code did support it, the BGP config would look something like:

```bash
! Configuration for the HUB
router bgp 500
 neighbor spokes peer-group
 bgp listen range 10.0.1.0/24 peer-group spokes
 neighbor spokes remote-as 600
 neighbor spokes next-hop-self
 neighbor spokes send-community

! Configuration for the Spokes
router bgp 600
 neighbor 10.0.1.1 remote-as 500
 neighbor 10.0.1.1 allowas-in 1
```

Update:

I had an interesting idea. Having the hub's and the spokes in the same BGP ASN. Having the DMVPN hubs act as BGP route reflectors and having the spoke connect to the hubs. As the hubs are route reflectors, they will propagate all routes about the spokes to all other spokes. In a DMVPN phase 2 scenario, this would allow the spokes to communicate next to each other as the spokes know about each other through BGP next-hop. I set it up in my lab and it actually works pretty well.

Here the BGP configuration from my hub:

```bash
DMVPN-HUB1-R1#sh run | s router bgp
router bgp 500
 template peer-policy spokes
  route-reflector-client
  soft-reconfiguration inbound
  send-community
 exit-peer-policy
 !
 template peer-session spokes
  remote-as 500
 exit-peer-session
 !
 no synchronization
 bgp cluster-id 10.0.1.1
 bgp log-neighbor-changes
 network 10.10.10.0 mask 255.255.255.0
 neighbor spokes peer-group
 neighbor 10.0.1.2 inherit peer-session spokes
 neighbor 10.0.1.2 inherit peer-policy spokes
 neighbor 10.0.1.3 inherit peer-session spokes
 neighbor 10.0.1.3 inherit peer-policy spokes
 no auto-summary
 !
 address-family ipv4 vrf Internet
  neighbor 150.0.0.1 remote-as 100
  neighbor 150.0.0.1 activate
  neighbor 150.0.0.1 send-community
  neighbor 150.0.0.1 allowas-in
  no synchronization
  network 151.0.0.0 mask 255.255.255.0
 exit-address-family
```

Here is the BGP configuration from one of my spokes:

```bash
DMVPN-SPOKE1-R4#sh run | s router bgp
router bgp 500
 template peer-policy hub
  prefix-list TUN out
  soft-reconfiguration inbound
  send-community
 exit-peer-policy
 !
 template peer-session hub
  remote-as 500
 exit-peer-session
 !
 no synchronization
 bgp log-neighbor-changes
 network 10.10.20.0 mask 255.255.255.0
 neighbor 10.0.1.1 inherit peer-session hub
 neighbor 10.0.1.1 inherit peer-policy hub
 no auto-summary
 !
 address-family ipv4 vrf Internet
  neighbor 150.0.0.9 remote-as 100
  neighbor 150.0.0.9 activate
  neighbor 150.0.0.9 send-community
  neighbor 150.0.0.9 allowas-in
  no synchronization
  network 152.0.0.0 mask 255.255.255.0
 exit-address-family
```

Here is the isakmp session status, BGP table, and trace route to a neighbor spoke from the DMVPN-SPOKE1-R4 spoke.

```bash
DMVPN-SPOKE1-R4#sh crypto isakmp sa
dst             src             state          conn-id slot status
151.0.0.1       152.0.0.1       QM_IDLE              1    0 ACTIVE
152.0.0.1       153.0.0.1       QM_IDLE              2    0 ACTIVE

DMVPN-SPOKE1-R4#sh ip bgp sum
BGP router identifier 10.10.20.1, local AS number 500
BGP table version is 14, main routing table version 14
3 network entries using 351 bytes of memory
3 path entries using 156 bytes of memory
6/2 BGP path/bestpath attribute entries using 744 bytes of memory
1 BGP rrinfo entries using 24 bytes of memory
2 BGP AS-PATH entries using 48 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1323 total bytes of memory
BGP activity 14/6 prefixes, 18/10 paths, scan interval 60 secs

Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.0.1.1        4   500     263     252       14    0    0 03:42:25        2
DMVPN-SPOKE1-R4#sh ip bgp 
BGP table version is 14, local router ID is 10.10.20.1
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*>i10.10.10.0/24    10.0.1.1                 0    100      0 i
*> 10.10.20.0/24    0.0.0.0                  0         32768 i
*>i10.10.30.0/24    10.0.1.3                 0    100      0 i
DMVPN-SPOKE1-R4#ping 10.10.30.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.30.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 4/13/24 ms
DMVPN-SPOKE1-R4#tracero
DMVPN-SPOKE1-R4#traceroute 10.10.30.1

Type escape sequence to abort.
Tracing the route to 10.10.30.1

  1 10.0.1.3 4 msec 4 msec * 
```

One way to make this scale, without manual intervention of having to add neighbor relationships in BGP would be to have the dynamic neighbor relations statement in the DMVPN hubs. In my lab set up, BGP works pretty well in a DMVPN environment.
