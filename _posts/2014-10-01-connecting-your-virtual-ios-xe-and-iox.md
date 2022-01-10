---
layout: post
title: Connecting Your Virtual IOS-XE and IOX-XR Lab To Your Physical Lab
date: '2014-10-01'
author: jtdub
tags:
- IOS
- Linux
- Software Defined Networking
- Virtualization
- CCNP SP Study Notes
- KVM
- IOS-XE
- openvswitch
- IOS-XR
- packetgeek.net
---

I've been building and using virtual IOS images, such as IOS-XE (CSR1000v) and IOS-XRv for a while now. It's been great to just spin up a lab, based upon what ever topology that I want, not have to worry about a mess of cables, or hear the mildly annoying hum of a rack of routers and switches running up my electric bill.
<br/>
<br/>
However, there are instances where running a physical lab makes sense. For example, the Cisco Switching images aren't where they need to be to be able to simulate live environments. There are a host of quirks, from creating bridging loops easily and crashing the images to FHRP's not having the desired functionality. Then there's the aspect of only being able to run so many virtual images on a single computer. Every now and then, I want to create a larger topology. I already have four switches and ten routers, so why not integrate my virtual lab environment and physical lab environment?
<br/>
<br/>
Recently, that's what I set out to do. I'm a Linux guy, so I've been using KVM as my hypervisor, for running my IOS images. I intended to continue doing that. The Linux computer that I'm currently running is Fedora 19. I know, I need to update it, but I've been too lazy to rebuild it lately. So, my examples are based on Fedora 19. If you're running a newer version of Fedora (20, soon to be 21), CentOS 7, or even Ubuntu, you'll need to modify your KVM configuration slightly. Ultimately, it should be compatible.
<br/>
<br/>
On my Fedora 19 computer, I'm using the qemu-kvm and openvswitch packages.
<br/>
<pre class="lang:default decode:true">[root@sgnhv ~]# rpm -qa | egrep 'openvswitch|qemu-kvm'<br/>openvswitch-test-2.0.1-1.fc19.noarch<br/>openvswitch-controller-2.0.1-1.fc19.x86_64<br/>python-openvswitch-2.0.1-1.fc19.noarch<br/>openvswitch-2.0.1-1.fc19.x86_64<br/>qemu-kvm-1.4.2-15.fc19.x86_64</pre>
<br/>
The first thing that you want to do is create a couple of init script for openvswitch. These scripts will allow you to create and tear down tap (virtual nics) interfaces, which your virtual IOS images will attach to on boot up.
<br/>
<pre class="lang:default decode:true">[root@sgnhv ~]# cat /usr/local/sbin/ovs-ifup <br/>#!/bin/sh<br/><br/>switch='ovs-br0'<br/>/sbin/ifconfig $1 0.0.0.0 up<br/>ovs-vsctl add-port ${switch} $1<br/>[root@sgnhv ~]# cat /usr/local/sbin/ovs-ifdown<br/>#!/bin/sh<br/><br/>switch='ovs-br0'<br/>/sbin/ifconfig $1 0.0.0.0 down<br/>ovs-vsctl del-port ${switch} $1</pre>
<br/>
Next, you need to create a bridge within openvswitch, and attach it to an unused physical nic. In my Fedora computer, I have my primary nic (p3p1), which is has the main IP Address that I use to access the computer remotely, then I have a secondary nic (enps4s0u1) that I'm allocating to openvswitch.
<br/>
<pre class="lang:default decode:true">** Physical NIC's on my Fedora Computer<br/>[root@sgnhv ~]# ip addr show p3p1<br/>2: p3p1: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000<br/>    link/ether 80:ee:73:53:f5:47 brd ff:ff:ff:ff:ff:ff<br/>    inet6 fe80::82ee:73ff:fe53:f547/64 scope link <br/>       valid_lft forever preferred_lft forever<br/>[root@sgnhv ~]# ip addr show enp4s0u1<br/>3: enp4s0u1: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc pfifo_fast state UP group default qlen 1000<br/>    link/ether 00:0a:cd:20:5f:be brd ff:ff:ff:ff:ff:ff<br/>    inet6 fe80::20a:cdff:fe20:5fbe/64 scope link <br/>       valid_lft forever preferred_lft forever<br/><br/>** Creating a bridge and allocating a physical NIC to the bridge<br/>[root@sgnhv ~]# ovs-vsctl show<br/>a8b9ccc7-fa12-46a1-a6c0-acd6dddf49e3<br/>    ovs_version: "2.0.1"<br/>[root@sgnhv ~]# ovs-vsctl add-br ovs-br0<br/>[root@sgnhv ~]# ovs-vsctl add-port ovs-br0 enp4s0u1<br/>[root@sgnhv ~]# ovs-vsctl show<br/>a8b9ccc7-fa12-46a1-a6c0-acd6dddf49e3<br/>    Bridge "ovs-br0"<br/>        Port "enp4s0u1"<br/>            Interface "enp4s0u1"<br/>        Port "ovs-br0"<br/>            Interface "ovs-br0"<br/>                type: internal<br/>    ovs_version: "2.0.1"</pre>
<br/>
At this point, my physical nic, enp4s0u1, is already attached to a switch port on my physical lab. The switch port on the physical lab is in a trunking state. This is all you have to do for openvswitch, as it will automatically trunk the interface to the physical nic.
<br/>
<br/>
Next, It's time to spin up my virtual IOS image. Here is my configuration:
<br/>
<pre class="lang:default decode:true">qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/ios-xrv-test.img \<br/>-serial telnet::8001,server,nowait \<br/>-net nic,model=virtio,vlan=2,macaddr=80:02:00:00:80:01 \<br/>-net tap,ifname=tap8001,vlan=2,script=/usr/local/sbin/ovs-ifup,downscript=/usr/local/sbin/ovs-ifdown \<br/>-net nic,model=virtio,macaddr=80:01:00:00:11:00 \<br/>-net tap,ifname=1g000,script=/usr/local/sbin/ovs-ifup,downscript=/usr/local/sbin/ovs-ifdown <br/></pre>
<br/>
On the first line, I simply tell KVM to create an instance with 2.5 GB of RAM and pointed to the image:
<br/>
<pre class="lang:default decode:true">qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/ios-xrv-test.img</pre>
<br/>
On the second line, I told KVM to create a serial connection and attach it to TCP port 8001 on the hypervisor. You can think of this as a console port on your physical gear.
<br/>
<pre class="lang:default decode:true">-serial telnet::8001,server,nowait</pre>
<br/>
The third and fourth line belong together. These two lines specify my MGMT interface on the IOS-XRv device, I'm attaching it to vlan 2, as my current lab Layer 2 management is on vlan 2. I'm also creating a tap interface called 'tap8001'. Notice that the ovs-ifup and ovs-ifdown scripts are called to create and tear down the interface.
<br/>
<pre class="lang:default decode:true">-net nic,model=virtio,vlan=2,macaddr=80:02:00:00:80:01 \<br/>-net tap,ifname=tap8001,vlan=2,script=/usr/local/sbin/ovs-ifup,downscript=/usr/local/sbin/ovs-ifdown</pre>
<br/>
Finally, the last two lines create interface gig0/0/0/0 on the IOS-XRv image. On these two lines, I don't specify to attach to any specific vlans, as I'll be creating sub interfaces and creating a router on a stick. It also calls the ovs-ifup and ovs-ifdown scripts to create and tear down the tap interface '1g000'.
<br/>
<pre class="lang:default decode:true">-net nic,model=virtio,macaddr=80:01:00:00:11:00 \<br/>-net tap,ifname=1g000,script=/usr/local/sbin/ovs-ifup,downscript=/usr/local/sbin/ovs-ifdown</pre>
<br/>
The config executes without any errors.
<br/>
<pre class="lang:default decode:true">[root@sgnhv ~]# qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/ios-xrv-test.img \<br/>&gt; -serial telnet::8001,server,nowait \<br/>&gt; -net nic,model=virtio,vlan=2,macaddr=80:02:00:00:80:01 \<br/>&gt; -net tap,ifname=tap8001,vlan=2,script=/usr/local/sbin/ovs-ifup,downscript=/usr/local/sbin/ovs-ifdown \<br/>&gt; -net nic,model=virtio,macaddr=80:01:00:00:11:00 \<br/>&gt; -net tap,ifname=1g000,script=/usr/local/sbin/ovs-ifup,downscript=/usr/local/sbin/ovs-ifdown <br/>QEMU 1.4.2 monitor - type 'help' for more information<br/>(qemu) <br/></pre>
<br/>
You can see that the ovs-ifup and ovs-ifdown scripts work as intended.
<br/>
<pre class="lang:default decode:true">[root@sgnhv ~]# ovs-vsctl show<br/>a8b9ccc7-fa12-46a1-a6c0-acd6dddf49e3<br/>    Bridge "ovs-br0"<br/>        Port "1g000"<br/>            Interface "1g000"<br/>        Port "tap8001"<br/>            Interface "tap8001"<br/>        Port "enp4s0u1"<br/>            Interface "enp4s0u1"<br/>        Port "ovs-br0"<br/>            Interface "ovs-br0"<br/>                type: internal<br/>    ovs_version: "2.0.1"<br/></pre>
<br/>
I'm also able to telnet to TCP port 8001 and gain access to the device.
<br/>
<pre class="lang:default decode:true">[root@sgnhv ~]# telnet localhost 8001<br/>Trying ::1...<br/>telnet: connect to address ::1: Connection refused<br/>Trying 127.0.0.1...<br/>Connected to localhost.<br/>Escape character is '^]'.<br/><br/><br/>User Access Verification<br/><br/>Username: admin<br/>Password: <br/><br/><br/>RP/0/0/CPU0:ios#<br/></pre>
<br/>
From here, I can configure the device to participate in my existing physical lab. In this simple test, I'll configure gig0/0/0/0.100 to connect to a physical router with the IP Address of 10.0.100.2, join OSPF, and MPLS LDP.
<br/>
<pre class="lang:default decode:true">RP/0/0/CPU0:ios#config t<br/>Wed Oct  1 17:05:46.748 UTC<br/>RP/0/0/CPU0:ios(config)#hostname xr1<br/>RP/0/0/CPU0:ios(config)#commit<br/>Wed Oct  1 17:06:02.507 UTC<br/>RP/0/0/CPU0:Oct  1 17:06:02.537 : ike[225]: %SECURITY-IKE-4-WARNING : You may want to configure a domain-name <br/>RP/0/0/CPU0:xr1(config)#int lo0<br/>RP/0/0/CPU0:xr1(config-if)#ipv4 address 10.10.100.1/32<br/>RP/0/0/CPU0:xr1(config-if)#commit<br/>Wed Oct  1 17:06:14.466 UTC<br/>RP/0/0/CPU0:xr1(config-if)#no shut<br/>RP/0/0/CPU0:xr1(config-if)#<br/>RP/0/0/CPU0:xr1(config-if)#<br/>RP/0/0/CPU0:xr1(config-if)#exit   <br/>RP/0/0/CPU0:xr1(config)#int gigabitEthernet 0/0/0/0 <br/>RP/0/0/CPU0:xr1(config-if)#no shut<br/>RP/0/0/CPU0:xr1(config-if)#exit<br/>RP/0/0/CPU0:xr1(config)#int gigabitEthernet 0/0/0/0.100<br/>RP/0/0/CPU0:xr1(config-subif)#dot1q vlan 100<br/>RP/0/0/CPU0:xr1(config-subif)#ipv4 address 10.0.100.1/30<br/>RP/0/0/CPU0:xr1(config-subif)#no shut<br/>RP/0/0/CPU0:xr1(config-subif)#commit<br/>Wed Oct  1 17:06:48.313 UTC<br/>RP/0/0/CPU0:Oct  1 17:06:48.323 : ifmgr[223]: %PKT_INFRA-LINK-3-UPDOWN : Interface GigabitEthernet0/0/0/0, changed state to Down <br/>RP/0/0/CPU0:Oct  1 17:06:48.353 : ifmgr[223]: %PKT_INFRA-LINK-3-UPDOWN : Interface GigabitEthernet0/0/0/0, changed state to Up <br/>RP/0/0/CPU0:xr1(config-subif)#end<br/>RP/0/0/CPU0:xr1#ping 10.0.100.1<br/>Wed Oct  1 17:06:59.503 UTC<br/>Type escape sequence to abort.<br/>Sending 5, 100-byte ICMP Echos to 10.0.100.1, timeout is 2 seconds:<br/>!!!!!<br/>Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms<br/>RP/0/0/CPU0:xr1#ping 10.0.100.2<br/>Wed Oct  1 17:07:01.923 UTC<br/>Type escape sequence to abort.<br/>Sending 5, 100-byte ICMP Echos to 10.0.100.2, timeout is 2 seconds:<br/>!!!!!<br/>Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms<br/>RP/0/0/CPU0:xr1#config t<br/>Wed Oct  1 17:07:06.132 UTC<br/>RP/0/0/CPU0:xr1(config)#router ospf 64512<br/>RP/0/0/CPU0:xr1(config-ospf)#auto-cost reference-bandwidth 100<br/>RP/0/0/CPU0:xr1(config-ospf)#area 0<br/>RP/0/0/CPU0:xr1(config-ospf-ar)#interface gigabitEthernet 0/0/0/0.100<br/>RP/0/0/CPU0:xr1(config-ospf-ar-if)#ne<br/>neighbor  network  <br/>RP/0/0/CPU0:xr1(config-ospf-ar-if)#network point-to-point <br/>RP/0/0/CPU0:xr1(config-ospf-ar-if)#exit<br/>RP/0/0/CPU0:xr1(config-ospf-ar)#interface lo0<br/>RP/0/0/CPU0:xr1(config-ospf-ar-if)#passive <br/>RP/0/0/CPU0:xr1(config-ospf-ar-if)#commit<br/>Wed Oct  1 17:07:44.640 UTC<br/>RP/0/0/CPU0:xr1(config-ospf-ar-if)#end<br/>RP/0/0/CPU0:xr1#sh ospf neighbor <br/>Wed Oct  1 17:07:50.749 UTC<br/><br/>* Indicates MADJ interface<br/><br/>Neighbors for OSPF 64512<br/><br/>Neighbor ID     Pri   State           Dead Time   Address         Interface<br/>10.10.10.1      1     FULL/  -        00:00:39    10.0.100.2      GigabitEthernet0/0/0/0.100<br/>    Neighbor is up for 00:00:03<br/><br/>Total neighbor count: 1<br/>RP/0/0/CPU0:xr1#config t<br/>Wed Oct  1 17:07:53.169 UTC<br/>RP/0/0/CPU0:xr1(config)#mpls ldp<br/>RP/0/0/CPU0:xr1(config-ldp)#interface gigabitEthernet 0/0/0/0.100<br/>RP/0/0/CPU0:xr1(config-ldp-if)#commit<br/>Wed Oct  1 17:08:06.268 UTC<br/>RP/0/0/CPU0:xr1(config-ldp-if)#end<br/>RP/0/0/CPU0:xr1#sh mpls ldp neighbor <br/>Wed Oct  1 17:08:17.277 UTC<br/><br/>Peer LDP Identifier: 10.10.10.1:0<br/>  TCP connection: 10.10.10.1:646 - 10.10.100.1:44516<br/>  Graceful Restart: No<br/>  Session Holdtime: 180 sec<br/>  State: Oper; Msgs sent/rcvd: 15/15; Downstream-Unsolicited<br/>  Up time: 00:00:08<br/>  LDP Discovery Sources:<br/>    GigabitEthernet0/0/0/0.100<br/>  Addresses bound to this peer:<br/>    10.0.10.1        10.0.10.5        10.0.10.9        10.0.100.2       <br/>    10.0.101.2       10.10.10.1       <br/></pre>
<br/>
And there you have it. My virtual lab has successfully been integrated to my physical lab.
