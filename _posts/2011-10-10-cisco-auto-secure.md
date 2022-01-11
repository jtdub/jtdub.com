---
layout: post
title: Cisco Auto Secure
date: '2011-10-10'
author: jtdub
tags:
- IOS
- Security
- IOS Security
- packetgeek.net
---

I recently found a new command to help with the securing of Cisco Routers. The command is "[auto secure](http://www.cisco.com/univercd/cc/td/doc/product/software/ios123/123newft/123_1/ftatosec.htm)", which is executed from privileged enable mode. When executed, it asks a few questions and executes several commands based on security best practices for Cisco Routers. Below is an example from a router in my test lab.

```bash
2610-4#sh run
Building configuration...
Current configuration : 750 bytes
!
version 12.3
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname 2610-4
!
boot-start-marker
boot-end-marker
!
!
no aaa new-model
ip subnet-zero
ip cef
!
!
!
!
!
!
!
!
interface Ethernet0/0
 no ip address
 shutdown
 half-duplex
!
interface Serial1/0
 ip address 10.1.0.1 255.255.255.0
 encapsulation ppp
 clock rate 128000
!
interface Serial1/1
 no ip address
 shutdown
!
interface Serial1/2
 no ip address
 shutdown
!
interface Serial1/3
 ip address 10.0.1.2 255.255.255.0
!
router ospf 1
 router-id 10.0.1.2
 log-adjacency-changes
 network 10.0.1.0 0.0.0.255 area 0
 network 10.1.0.0 0.0.0.255 area 2
!
ip http server
ip classless
!
!
!
line con 0
line aux 0
line vty 0 4
!
!
end
2610-4#auto
2610-4#auto se
2610-4#auto secure
                --- AutoSecure Configuration ---
*** AutoSecure configuration enhances the security of
the router, but it will not make it absolutely resistant
to all security attacks ***
AutoSecure will modify the configuration of your device.
All configuration changes will be shown. For a detailed
explanation of how the configuration changes enhance security
and any possible side effects, please refer to Cisco.com for
Autosecure documentation.
At any prompt you may enter '?' for help.
Use ctrl-c to abort this session at any prompt.
If this device is being managed by a network management station,
AutoSecure configuration may block network management traffic.
Continue with AutoSecure? [no]: yes
Gathering information about the router for AutoSecure
Is this router connected to internet? [no]:
Securing Management plane services...
Disabling service finger
Disabling service pad
Disabling udp & tcp small servers
Enabling service password encryption
Enabling service tcp-keepalives-in
Enabling service tcp-keepalives-out
Disabling the cdp protocol
Disabling the bootp server
Disabling the http server
Disabling the finger service
Disabling source routing
Disabling gratuitous arp
Here is a sample Security Banner to be shown
at every access to device. Modify it to suit your
enterprise requirements.
Authorized Access only
  This system is the property of So-&-So-Enterprise.
  UNAUTHORIZED ACCESS TO THIS DEVICE IS PROHIBITED.
  You must have explicit permission to access this
  device. All activities performed on this device
  are logged. Any violations of access policy will result
  in disciplinary action.
Enter the security banner {Put the banner between
k and k, where k is any character}:
#
Authorized Access only
  This system is the property of So-&-So-Enterprise.
  UNAUTHORIZED ACCESS TO THIS DEVICE IS PROHIBITED.
  You must have explicit permission to access this
  device. All activities performed on this device
  are logged. Any violations of access policy will result
  in disciplinary action.
#
Enable secret is either not configured or
 is the same as the enable password
Enter the new enable secret:
Confirm the enable secret :
Enable password is not configured or its length
is less than minimum no. of characters configured
Enter the new enable password:
Confirm the enable password:
Configuration of local user database
Enter the username: james
Enter the password:
Confirm the password:
Configuring AAA local authentication
Configuring Console, Aux and VTY lines for
local authentication, exec-timeout, and transport
Configuring interface specific AutoSecure services
Disabling the following ip services on all interfaces:
 no ip redirects
 no ip proxy-arp
 no ip unreachables
 no ip directed-broadcast
 no ip mask-reply
Securing Forwarding plane services...
Enabling CEF (This might impact the memory requirements for your platform)
This is the configuration generated:
no service finger
no service pad
no service udp-small-servers
no service tcp-small-servers
service password-encryption
service tcp-keepalives-in
service tcp-keepalives-out
no cdp run
no ip bootp server
no ip http server
no ip finger
no ip source-route
no ip gratuitous-arps
banner #
Authorized Access only
  This system is the property of So-&-So-Enterprise.
  UNAUTHORIZED ACCESS TO THIS DEVICE IS PROHIBITED.
  You must have explicit permission to access this
  device. All activities performed on this device
  are logged. Any violations of access policy will result
  in disciplinary action.
#
security passwords min-length 6
security authentication failure rate 10 log
enable secret 5 $1$U3Md$NLdPY5lpIOUf8Ht9L5omi/
enable password 7 00141215170A5955
username james password 7 082B4D5900405D40
aaa new-model
aaa authentication login local_auth local
line console 0
 login authentication local_auth
 exec-timeout 5 0
 transport output telnet
line aux 0
 login authentication local_auth
 exec-timeout 10 0
 transport output telnet
line vty 0 4
 login authentication local_auth
 transport input telnet
service timestamps debug datetime localtime show-timezone msec
service timestamps log datetime localtime show-timezone msec
logging facility local2
logging trap debugging
service sequence-numbers
logging console critical
logging buffered
int Ethernet0/0
 no ip redirects
 no ip proxy-arp
 no ip unreachables
 no ip directed-broadcast
 no ip mask-reply
int Serial1/0
 no ip redirects
 no ip proxy-arp
 no ip unreachables
 no ip directed-broadcast
 no ip mask-reply
int Serial1/1
 no ip redirects
 no ip proxy-arp
 no ip unreachables
 no ip directed-broadcast
 no ip mask-reply
int Serial1/2
 no ip redirects
 no ip proxy-arp
 no ip unreachables
 no ip directed-broadcast
 no ip mask-reply
int Serial1/3
 no ip redirects
 no ip proxy-arp
 no ip unreachables
 no ip directed-broadcast
 no ip mask-reply
ip cef
!
end

Apply this configuration to running-config? [yes]: yes
Applying the config generated to running-config
2610-4#
2610-4#sh run
Building configuration...
Current configuration : 2122 bytes
!
version 12.3
no service pad
service tcp-keepalives-in
service tcp-keepalives-out
service timestamps debug datetime msec localtime show-timezone
service timestamps log datetime msec localtime show-timezone
service password-encryption
service sequence-numbers
!
hostname 2610-4
!
boot-start-marker
boot-end-marker
!
security authentication failure rate 10 log
security passwords min-length 6
logging buffered 4096 debugging
logging console critical
enable secret 5 $1$U3Md$NLdPY5lpIOUf8Ht9L5omi/
enable password 7 00141215170A5955
!
aaa new-model
!
!
aaa authentication login local_auth local
aaa session-id common
ip subnet-zero
no ip source-route
no ip gratuitous-arps
ip cef
!
!
!
no ip bootp server
!
username james password 7 082B4D5900405D40
!
!
!
!
interface Ethernet0/0
 no ip address
 no ip redirects
 no ip unreachables
 no ip proxy-arp
 shutdown
 half-duplex
!
interface Serial1/0
 ip address 10.1.0.1 255.255.255.0
 no ip redirects
 no ip unreachables
 no ip proxy-arp
 encapsulation ppp
 clock rate 128000
!
interface Serial1/1
 no ip address
 no ip redirects
 no ip unreachables
 no ip proxy-arp
 shutdown
!
interface Serial1/2
 no ip address
 no ip redirects
 no ip unreachables
 no ip proxy-arp
 shutdown
!
interface Serial1/3
 ip address 10.0.1.2 255.255.255.0
 no ip redirects
 no ip unreachables
 no ip proxy-arp
!
router ospf 1
 router-id 10.0.1.2
 log-adjacency-changes
 network 10.0.1.0 0.0.0.255 area 0
 network 10.1.0.0 0.0.0.255 area 2
!
no ip http server
ip classless
!
!
logging trap debugging
logging facility local2
no cdp run
banner motd ^C
Authorized Access only
  This system is the property of So-&-So-Enterprise.
  UNAUTHORIZED ACCESS TO THIS DEVICE IS PROHIBITED.
  You must have explicit permission to access this
  device. All activities performed on this device
  are logged. Any violations of access policy will result
  in disciplinary action.
^C
!
line con 0
 exec-timeout 5 0
 login authentication local_auth
 transport output telnet
line aux 0
 login authentication local_auth
 transport output telnet
line vty 0 4
 login authentication local_auth
 transport input telnet
!
!
```
