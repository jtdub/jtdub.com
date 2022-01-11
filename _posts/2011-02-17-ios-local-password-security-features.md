---
layout: post
title: IOS Local Password Security Features
date: '2011-02-17'
author: jtdub
tags:
- IOS
- Security
- IOS Security
- packetgeek.net
---

I've been studying some of the security features built in to IOS. These mostly have to do with physical security and local password security built into IOS.

For instance, a feature that I've used for several years is the "service password-encryption" command. This command takes the plain-text passwords located in AUX, CON, TTY ports, and enable password command and encrypts them with a password hash derived from Cisco. It's not perfect, but will do in a pinch. One thing that you will want to do immediately after executing a "service password-encryption" is executing a "show run". The reason behind this is that the passwords won't change from plain-text to encrypted until that happens.

```bash
Router(config)#service ?
....
  password-encryption    Encrypt system passwords
....
```

If you are unable to protect your Cisco equipment physically, the best option is to disable the password recovery function. Be sure to have some other option to do password recoveries however, as you will not be able to do password recoveries from RMON.

This feature isn't listed as a command when executing a "?" command, but the command exists in IOS 12.3(14)T or newer.

Check out the documentation:

[no service password-recovery](http://www.cisco.com/en/US/docs/ios/12_3/12_3y/12_3ya8/gtnsvpwd.html)

```bash
Router(config)#no service ?
  alignment              Control alignment correction and logging
  compress-config        Compress the nvram configuration file
  config                 TFTP load config files
  dhcp                   Enable DHCP server and relay agent
  disable-ip-fast-frag   Disable IP particle-based fast fragmentation
  exec-callback          Enable exec callback
  exec-wait              Delay EXEC startup on noisy lines
  finger                 Allow responses to finger requests
  hide-telnet-addresses  Hide destination addresses in telnet command
  linenumber             enable line number banner for each exec
  nagle                  Enable Nagle's congestion control algorithm
  old-slip-prompts       Allow old scripts to operate with slip/ppp
  pad                    Enable PAD commands
  password-encryption    Encrypt system passwords
  prompt                 Enable mode specific prompt
  pt-vty-logging         Log significant VTY-Async events
  sequence-numbers       Stamp logger messages with a sequence number
  slave-log              Enable log capability of slave IPs
  tcp-keepalives-in      Generate keepalives on idle incoming network
                         connections
  tcp-keepalives-out     Generate keepalives on idle outgoing network
                         connections

Router(config)#no service password-recovery
WARNING:
Executing this command will disable password recovery me
chanism.
Do not execute this command without another plan for
password recovery.

Are you sure you want to continue? [yes/no]:
```

Other options include encrypting the passwords in MD5 using the "secret" sub command. For instance, "enable secret" and username james secret t0ps3cr37pwd". Unfortunately, the "secret" sub command isn't available on the AUX, TTY, or CON ports.

You can also set up minimum password lengths and password retry limits.

```bash
Router(config)#security ?
  authentication  Authentication security CLIs
  passwords       Password security CLIs

Router(config)#security auth
Router(config)#security authentication ?
  failure  Authentication failure logging

Router(config)#security authentication fa
Router(config)#security authentication failure ?
  rate  Authentication failure threshold rate

Router(config)#security authentication failure ra
Router(config)#security authentication failure rate ?
  <2-1024>  Authentication failure threshold rate

Router(config)#security authentication failure rate 5 ?
  log  log a message if the Authentication failures over the last one minute
       equalled this number

Router(config)#security authentication failure rate 5 l
Router(config)#security authentication failure rate 5 log ?
  

Router(config)#security pas
Router(config)#security passwords ?
  min-length  Minimum length of passwords

Router(config)#security passwords min
Router(config)#security passwords min-length ?
  <0-16>  Minimum length of all user/enable passwords

Router(config)#security passwords min-length 16 ?
  

Router(config)#enable ?
  last-resort  Define enable action if no TACACS servers respond
  password     Assign the privileged level password
  secret       Assign the privileged level secret
  use-tacacs   Use TACACS to check enable passwords

Router(config)#enable sec
Router(config)#enable secret ?
  0      Specifies an UNENCRYPTED password will follow
  5      Specifies an ENCRYPTED secret will follow
  LINE   The UNENCRYPTED (cleartext) 'enable' secret
  level  Set exec level password

Router(config)#enable secret
```
