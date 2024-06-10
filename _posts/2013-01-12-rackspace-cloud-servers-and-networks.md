---
layout: post
title: Rackspace Cloud Servers and Networks with Open vSwitch and VXLAN between Data
  Centers
date: '2013-01-12'
author: jtdub
tags:
- Linux
- Software Defined Networking
- VXLAN
- SDN
- openvswitch
- packetgeek.net
---

I've been playing with Open vSwitch and the VXLAN patch that is available at: [https://github.com/mestery/ovs-vxlan](https://github.com/mestery/ovs-vxlan)

So far all my testing has been done on my Rackspace Cloud account. I realize that you wouldn't use VXLAN in a scenario like this on any production network, but for my testing, I thought that it would be good to have a physical separation of the networks. While I was able to get my VXLAN tunnel up, I haven't been able to get the traffic to completely pass from my test-dfw to my test-ord servers. The traffic is getting lost at some point where the traffic leaves the ovs-ord internal interface (eth2) destined to test-ord server. I believe that I either need to add some configuration to the open vswitch service or the Rackspace Cloud Networks is stripping some data as it leaves ovs-ord, destined to test-ord. I'm still trying to figure that piece out. Below is that I have so far, along with the testing and troubleshooting section at the bottom.

Here is a diagram of the lab:

<img height="128" src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/b1c60fc8-5884-4a52-e25a-1a1411bf0e00/public"/>

I started off by building the OVS servers that would be used to create the VXLAN tunnels would would pass traffic to the servers sitting behind them. To do this, I used the Rackspace Cloud Networks to create a private internal network in both the ORD and DFW data centers. All my servers would use eth2 to access that network and as the data centers are physically separated, my internal networks would be isolated from each other as well. I also used the Rackspace Cloud Servers to build the lab infrastructure. This includes four servers in total. Each running the Rackspace provided Fedora 17 image and all would be 512 meg instances.

First, I created all the instances, which are named as ovs-dfw, ovs-ord, test-dfw, test-ord. I then configured the ovs-{dfw, ord} instances.

#######################################

OVS Server Builds

#######################################

* Executed on both servers:

```bash
yum -y --disableexcludes=all update

for i in disable stop; do
for o in rpcbind.socket rpcbind.service iptables.service; do
systemctl $i $o;
done
done

reboot
```

Once the servers came back up, I wanted to verify the kernel version that was running. This will be needed when building the open vswitch kernel module RPM. My kernel version is: 3.3.4-5.fc17.x86_64. If your kernel version is different, then you will need to take note and make the appropriate changes when building the openvswitch kernel moduele. I'll be sure to remind you of this later, as those processes come up.

`uname -r`

After you've taken note of the running kernel version, we'll need to install the utilities needed to compile code, build RPMs, and troubleshoot networks. Note that I installed a kernel specific kernel-devel package - kernel-devel-3.3.4-5.fc17.x86_64. If your running kernel is different, then chage the package name to the appropriate kernel.

```bash
yum install -y openvswitch gcc make python-devel openssl-devel kernel-devel kernel-debug-devel git automake autoconf rpmdevtools kernel-devel-3.3.4-5.fc17.x86_64 tcpdump
```

Once the packages have installed, we can start downloading and building openvswitch packages needed to build the RPMs.

```bash
git clone https://github.com/mestery/ovs-vxlan.git
cd ovs-vxlan
git checkout vxlan
./boot.sh
./configure --with-linux=/lib/modules/`uname -r`/build
make dist
```

Now, we can start building the RPMs.

```bash
rpmdev-setuptree
cp openvswitch-1.9.90.tar.gz ~/rpmbuild/SOURCES/
cd ~/rpmbuild/SOURCES/
tar xvzf openvswitch-1.9.90.tar.gz
cd openvswitch-1.9.90/
rpmbuild -bb rhel/openvswitch-fedora.spec
```

Just a quick note. If you're not running the same kernel version that I am, then you will need to change the next line to reflect the kernel version that you are running, or it will error out.

```bash
sed -i 's/#%define kernel 3.1.5-1.fc16.x86_64/%define kernel 3.3.4-5.fc17.x86_64/' rhel/openvswitch-kmod-fedora.spec
rpmbuild -bb rhel/openvswitch-kmod-fedora.spec
```

Now, let's install the newly minted RPMs!

```bash
cd ~/rpmbuild/RPMS/x86_64/
rpm -Uvh *
```

Once that is completed, enable the open vswitch services to start at boot and start the services.

```bash
systemctl enable openvswitch.service
systemctl restart openvswitch.service
```

Now that the hard part is done, we can verify that open vswitch is running and functioning properly before going on to creating the VXLAN tunnels.

```bash
ps -ae | grep ovs
ovs-vsctl show
```

Once open vswitch has been verified, let's configure it for VXLAN! Where */ip_addr_of_remote_server/* is, replace that with the IP Address of the remote OVS server. So, on the OVS-DFW server, you should put the IP Address of the OVS-ORD server and vise versa. Those IP Addresses on the Rackspace Cloud servers reside on eth0.

```bash
ip addr show dev eth0 | grep inet | head -1 | awk '{print $2}' | cut -d / -f 1

eth2=/etc/sysconfig/network-scripts/ifcfg-eth2; \
sed -i 's/IPADDR/#IPADDR/g' $eth2; \
sed -i 's/NETMASK/#NETMASK/g' $eth2; \
sed -i 's/DNS/#DNS/g' $eth2; \
sed -i 's/static/none/g' $eth2
ip addr flush dev eth2
ip addr show dev eth2
ovs-vsctl add-br br0
ovs-vsctl add-port br0 eth2
ovs-vsctl add-port br0 vx0 -- set interface vx0 type=vxlan options:remote_ip=*/ip_addr_of_remote_server/*
ovs-vsctl show
```

That's it! The VXLAN tunnels have been built and we're now ready to work on the test-{dfw, ord} servers. This setup is easy. All we need to do is set up IP Addresses on the eth2 interfaces. For this test, I'm using 192.168.1.11 as the test-dfw server and 192.168.1.12 as the test-ord server. When I created the internal networks on my cloud account, I left the default CIDR as 192.168.3.0/24. I'll want to change this configuration on the servers, so that they boot with the IP Addresses that I want to use.

#######################################

TEST-DFW eth2 configuration

#######################################

```bash
eth2=/etc/sysconfig/network-scripts/ifcfg-eth2; \
sed -i 's/192.168.3.[0-9]/192.168.1.11/g' $eth2
ip addr flush dev eth2
ip addr add 192.168.1.11/24 dev eth2
ip addr show dev eth2
```

#######################################

TEST-ORD eth2 configuration

#######################################

```bash
eth2=/etc/sysconfig/network-scripts/ifcfg-eth2; \
sed -i 's/192.168.3.[0-9]/192.168.1.12/g' $eth2
ip addr flush dev eth2
ip addr add 192.168.1.12/24 dev eth2
ip addr show dev eth2
```

#######################################

Test connectivity from test-dfw to test-ord

#######################################

We'll do this in steps. I'll initiate a ping from test-dfw to test-ord. This will be done in steps.

* On test-dfw, I'll start a ping to test-ord (ping 192.168.1.2).
* On ovs-ord, I'll use tcpdump to listen for traffic on br0 and eth2
* On test-ord, I'll use tcpdump to listen for traffic on eth2
* If I don't receive a ping reply or traffic is lost along the path, I'll set VXLAN connectivity by assigning IP Addresses on the br0 interfaces of ovs-dfw (192.168.1.1) and ovs-ord (192.168.1.2). While I have addreses assigned to the br0 interfaces of ovs-{dfw, ord}, I'll test connectivity directly to their local LAN connected servers. On ovs-dfw, I'll ping test-dfw and on ovs-ord, I'll ping test-ord.

```bash
[root@test-dfw ~]# ping 192.168.1.12
PING 192.168.1.12 (192.168.1.12) 56(84) bytes of data.
From 192.168.1.11 icmp_seq=1 Destination Host Unreachable
From 192.168.1.11 icmp_seq=2 Destination Host Unreachable
From 192.168.1.11 icmp_seq=3 Destination Host Unreachable
From 192.168.1.11 icmp_seq=4 Destination Host Unreachable
From 192.168.1.11 icmp_seq=5 Destination Host Unreachable


[root@ovs-ord ~]# tcpdump -i br0 -XX -vvv -e -c 5
tcpdump: WARNING: br0: no IPv4 address assigned
tcpdump: listening on br0, link-type EN10MB (Ethernet), capture size 65535 bytes
05:05:08.627796 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:09.628891 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:10.631546 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:12.629095 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:13.631575 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
5 packets captured
5 packets received by filter
0 packets dropped by kernel
[root@ovs-ord ~]# tcpdump -i eth2 -XX -vvv -e -c 5
tcpdump: WARNING: eth2: no IPv4 address assigned
tcpdump: listening on eth2, link-type EN10MB (Ethernet), capture size 65535 bytes
05:05:40.637676 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:41.637641 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:42.639147 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:44.643446 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
05:05:45.639364 bc:76:4e:04:82:f2 (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28
 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......
 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......
 0x0020:  0000 0000 0000 c0a8 010c                 ..........
5 packets captured
5 packets received by filter
0 packets dropped by kernel


[root@test-ord ~]# date
Sun Jan 13 05:11:08 UTC 2013
[root@test-ord ~]# tcpdump -i eth2 -XX -vvv -e -c 5
tcpdump: listening on eth2, link-type EN10MB (Ethernet), capture size 65535 bytes
^C
0 packets captured
0 packets received by filter
0 packets dropped by kernel
[root@test-ord ~]# date
Sun Jan 13 05:11:24 UTC 2013


[root@ovs-dfw ~]# ip addr add 192.168.1.1/24 dev br0
[root@ovs-dfw ~]# ping -c2 192.168.1.2
PING 192.168.1.2 (192.168.1.2) 56(84) bytes of data.
64 bytes from 192.168.1.2: icmp_req=1 ttl=64 time=60.5 ms
64 bytes from 192.168.1.2: icmp_req=2 ttl=64 time=25.7 ms

--- 192.168.1.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 25.734/43.163/60.593/17.430 ms
[root@ovs-dfw ~]# ping -c2 192.168.1.11
PING 192.168.1.11 (192.168.1.11) 56(84) bytes of data.
64 bytes from 192.168.1.11: icmp_req=1 ttl=64 time=252 ms
64 bytes from 192.168.1.11: icmp_req=2 ttl=64 time=1.10 ms

--- 192.168.1.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.102/126.650/252.198/125.548 ms


[root@ovs-ord ~]# ip addr add 192.168.1.2/24 dev br0
[root@ovs-ord ~]# 
[root@ovs-ord ~]# ping -c2 192.168.1.1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_req=1 ttl=64 time=29.1 ms
64 bytes from 192.168.1.1: icmp_req=2 ttl=64 time=26.8 ms

--- 192.168.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 26.899/28.039/29.180/1.152 ms
[root@ovs-ord ~]# ping -c2 192.168.1.12
PING 192.168.1.12 (192.168.1.12) 56(84) bytes of data.
64 bytes from 192.168.1.12: icmp_req=1 ttl=64 time=33.8 ms
64 bytes from 192.168.1.12: icmp_req=2 ttl=64 time=1.42 ms

--- 192.168.1.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.423/17.622/33.821/16.199 ms
```

#######################################

tpcdump of a successful ping between ovs-ord and test-ord

#######################################

```bash
[root@test-ord ~]# tcpdump -i eth2 -XX -vvv -e -c 5
tcpdump: listening on eth2, link-type EN10MB (Ethernet), capture size 65535 bytes
05:14:42.582679 bc:76:4e:10:5c:74 (oui Unknown) > bc:76:4e:10:5a:89 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.1.2 > test-ord: ICMP echo request, id 13043, seq 1, length 64
 0x0000:  bc76 4e10 5a89 bc76 4e10 5c74 0800 4500  .vN.Z..vN.\t..E.
 0x0010:  0054 0000 4000 4001 b74a c0a8 0102 c0a8  .T..@.@..J......
 0x0020:  010c 0800 a434 32f3 0001 c242 f250 0000  .....42....B.P..
 0x0030:  0000 a670 0700 0000 0000 1011 1213 1415  ...p............
 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%
 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &'()*+,-./012345
 0x0060:  3637                                     67
05:14:42.582755 bc:76:4e:10:5a:89 (oui Unknown) > bc:76:4e:10:5c:74 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 43535, offset 0, flags [none], proto ICMP (1), length 84)
    test-ord > 192.168.1.2: ICMP echo reply, id 13043, seq 1, length 64
 0x0000:  bc76 4e10 5c74 bc76 4e10 5a89 0800 4500  .vN.\t.vN.Z...E.
 0x0010:  0054 aa0f 0000 4001 4d3b c0a8 010c c0a8  .T....@.M;......
 0x0020:  0102 0000 ac34 32f3 0001 c242 f250 0000  .....42....B.P..
 0x0030:  0000 a670 0700 0000 0000 1011 1213 1415  ...p............
 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%
 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &'()*+,-./012345
 0x0060:  3637                                     67
05:14:43.583017 bc:76:4e:10:5c:74 (oui Unknown) > bc:76:4e:10:5a:89 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.1.2 > test-ord: ICMP echo request, id 13043, seq 2, length 64
 0x0000:  bc76 4e10 5a89 bc76 4e10 5c74 0800 4500  .vN.Z..vN.\t..E.
 0x0010:  0054 0000 4000 4001 b74a c0a8 0102 c0a8  .T..@.@..J......
 0x0020:  010c 0800 7b2e 32f3 0002 c342 f250 0000  ....{.2....B.P..
 0x0030:  0000 ce75 0700 0000 0000 1011 1213 1415  ...u............
 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%
 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &'()*+,-./012345
 0x0060:  3637                                     67
05:14:43.583067 bc:76:4e:10:5a:89 (oui Unknown) > bc:76:4e:10:5c:74 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 43536, offset 0, flags [none], proto ICMP (1), length 84)
    test-ord > 192.168.1.2: ICMP echo reply, id 13043, seq 2, length 64
 0x0000:  bc76 4e10 5c74 bc76 4e10 5a89 0800 4500  .vN.\t.vN.Z...E.
 0x0010:  0054 aa10 0000 4001 4d3a c0a8 010c c0a8  .T....@.M:......
 0x0020:  0102 0000 832e 32f3 0002 c342 f250 0000  ......2....B.P..
 0x0030:  0000 ce75 0700 0000 0000 1011 1213 1415  ...u............
 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%
 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &'()*+,-./012345
 0x0060:  3637                                     67
05:14:44.584026 bc:76:4e:10:5c:74 (oui Unknown) > bc:76:4e:10:5a:89 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.1.2 > test-ord: ICMP echo request, id 13043, seq 3, length 64
 0x0000:  bc76 4e10 5a89 bc76 4e10 5c74 0800 4500  .vN.Z..vN.\t..E.
 0x0010:  0054 0000 4000 4001 b74a c0a8 0102 c0a8  .T..@.@..J......
 0x0020:  010c 0800 8628 32f3 0003 c442 f250 0000  .....(2....B.P..
 0x0030:  0000 c27a 0700 0000 0000 1011 1213 1415  ...z............
 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%
 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &'()*+,-./012345
 0x0060:  3637                                     67
5 packets captured
6 packets received by filter
0 packets dropped by kernel
```
