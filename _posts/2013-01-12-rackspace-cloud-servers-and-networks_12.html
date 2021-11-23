---
layout: post
title: Rackspace Cloud Servers and Networks with Open vSwitch and VXLANbetween Data
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

I've been playing with Open vSwitch and the VXLAN patch that is available at:
<br/>
<br/>
<a href="https://github.com/mestery/ovs-vxlan" target="_blank">
 https://github.com/mestery/ovs-vxlan
</a>
<br/>
<br/>
So far all my testing has been done on my Rackspace Cloud account. I realize that you wouldn't use VXLAN in a scenario like this on any production network, but for my testing, I thought that it would be good to have a physical separation of the networks. While I was able to get my VXLAN tunnel up, I haven't been able to get the traffic to completely pass from my test-dfw to my test-ord servers. The traffic is getting lost at some point where the traffic leaves the ovs-ord internal interface (eth2) destined to test-ord server. I believe that I either need to add some configuration to the open vswitch service or the Rackspace Cloud Networks is stripping some data as it leaves ovs-ord, destined to test-ord. I'm still trying to figure that piece out. Below is that I have so far, along with the testing and troubleshooting section at the bottom.
<br/>
<br/>
Here is a diagram of the lab:
<br/>
<br/>
<div class="separator" style="clear: both; text-align: center;">
 <a href="/images/VXLAN-LAB.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;">
  <img border="0" data-original-height="298" data-original-width="744" height="128" src="/images/VXLAN-LAB.png" width="320"/>
 </a>
</div>
<br/>
<br/>
I started off by building the OVS servers that would be used to create the VXLAN tunnels would would pass traffic to the servers sitting behind them. To do this, I used the Rackspace Cloud Networks to create a private internal network in both the ORD and DFW data centers. All my servers would use eth2 to access that network and as the data centers are physically separated, my internal networks would be isolated from each other as well. I also used the Rackspace Cloud Servers to build the lab infrastructure. This includes four servers in total. Each running the Rackspace provided Fedora 17 image and all would be 512 meg instances.
<br/>
<br/>
First, I created all the instances, which are named as ovs-dfw, ovs-ord, test-dfw, test-ord. I then configured the ovs-{dfw, ord} instances.
<br/>
<br/>
#######################################
<br/>
OVS Server Builds
<br/>
#######################################
<br/>
<br/>
* Executed on both servers:
<br/>
<pre>yum -y --disableexcludes=all update<br/><br/>for i in disable stop; do<br/>for o in rpcbind.socket rpcbind.service iptables.service; do<br/>systemctl $i $o;<br/>done<br/>done<br/><br/>reboot</pre>
<br/>
Once the servers came back up, I wanted to verify the kernel version that was running. This will be needed when building the open vswitch kernel module RPM. My kernel version is: 3.3.4-5.fc17.x86_64. If your kernel version is different, then you will need to take note and make the appropriate changes when building the openvswitch kernel moduele. I'll be sure to remind you of this later, as those processes come up.
<br/>
<br/>
<br/>
<pre>uname -r</pre>
<br/>
After you've taken note of the running kernel version, we'll need to install the utilities needed to compile code, build RPMs, and troubleshoot networks. Note that I installed a kernel specific kernel-devel package - kernel-devel-3.3.4-5.fc17.x86_64. If your running kernel is different, then chage the package name to the appropriate kernel.
<br/>
<pre>yum install -y openvswitch gcc make python-devel openssl-devel kernel-devel kernel-debug-devel git automake autoconf rpmdevtools kernel-devel-3.3.4-5.fc17.x86_64 tcpdump</pre>
<br/>
Once the packages have installed, we can start downloading and building openvswitch packages needed to build the RPMs.
<br/>
<br/>
<br/>
<pre>git clone https://github.com/mestery/ovs-vxlan.git<br/>cd ovs-vxlan<br/>git checkout vxlan<br/>./boot.sh<br/>./configure --with-linux=/lib/modules/`uname -r`/build<br/>make dist</pre>
<br/>
Now, we can start building the RPMs.
<br/>
<br/>
<br/>
<pre>rpmdev-setuptree<br/>cp openvswitch-1.9.90.tar.gz ~/rpmbuild/SOURCES/<br/>cd ~/rpmbuild/SOURCES/<br/>tar xvzf openvswitch-1.9.90.tar.gz<br/>cd openvswitch-1.9.90/<br/>rpmbuild -bb rhel/openvswitch-fedora.spec</pre>
<br/>
Just a quick note. If you're not running the same kernel version that I am, then you will need to change the next line to reflect the kernel version that you are running, or it will error out.
<br/>
<br/>
<br/>
<pre>sed -i 's/#%define kernel 3.1.5-1.fc16.x86_64/%define kernel 3.3.4-5.fc17.x86_64/' rhel/openvswitch-kmod-fedora.spec<br/>rpmbuild -bb rhel/openvswitch-kmod-fedora.spec</pre>
<br/>
Now, let's install the newly minted RPMs!
<br/>
<br/>
<br/>
<pre>cd ~/rpmbuild/RPMS/x86_64/<br/>rpm -Uvh *</pre>
<br/>
Once that is completed, enable the open vswitch services to start at boot and start the services.
<br/>
<br/>
<br/>
<pre>systemctl enable openvswitch.service<br/>systemctl restart openvswitch.service</pre>
<br/>
Now that the hard part is done, we can verify that open vswitch is running and functioning properly before going on to creating the VXLAN tunnels.
<br/>
<br/>
<br/>
<pre>ps -ae | grep ovs<br/>ovs-vsctl show</pre>
<br/>
Once open vswitch has been verified, let's configure it for VXLAN! Where */ip_addr_of_remote_server/* is, replace that with the IP Address of the remote OVS server. So, on the OVS-DFW server, you should put the IP Address of the OVS-ORD server and vise versa. Those IP Addresses on the Rackspace Cloud servers reside on eth0.
<br/>
<pre>ip addr show dev eth0 | grep inet | head -1 | awk '{print $2}' | cut -d / -f 1<br/><br/>eth2=/etc/sysconfig/network-scripts/ifcfg-eth2; \<br/>sed -i 's/IPADDR/#IPADDR/g' $eth2; \<br/>sed -i 's/NETMASK/#NETMASK/g' $eth2; \<br/>sed -i 's/DNS/#DNS/g' $eth2; \<br/>sed -i 's/static/none/g' $eth2<br/>ip addr flush dev eth2<br/>ip addr show dev eth2<br/>ovs-vsctl add-br br0<br/>ovs-vsctl add-port br0 eth2<br/>ovs-vsctl add-port br0 vx0 -- set interface vx0 type=vxlan options:remote_ip=*/ip_addr_of_remote_server/*<br/>ovs-vsctl show</pre>
<br/>
That's it! The VXLAN tunnels have been built and we're now ready to work on the test-{dfw, ord} servers. This setup is easy. All we need to do is set up IP Addresses on the eth2 interfaces. For this test, I'm using 192.168.1.11 as the test-dfw server and 192.168.1.12 as the test-ord server. When I created the internal networks on my cloud account, I left the default CIDR as 192.168.3.0/24. I'll want to change this configuration on the servers, so that they boot with the IP Addresses that I want to use.
<br/>
<br/>
#######################################
<br/>
TEST-DFW eth2 configuration
<br/>
#######################################
<br/>
<br/>
<br/>
<pre>eth2=/etc/sysconfig/network-scripts/ifcfg-eth2; \<br/>sed -i 's/192.168.3.[0-9]/192.168.1.11/g' $eth2<br/>ip addr flush dev eth2<br/>ip addr add 192.168.1.11/24 dev eth2<br/>ip addr show dev eth2</pre>
<br/>
<br/>
<br/>
#######################################
<br/>
TEST-ORD eth2 configuration
<br/>
#######################################
<br/>
<br/>
<br/>
<pre>eth2=/etc/sysconfig/network-scripts/ifcfg-eth2; \<br/>sed -i 's/192.168.3.[0-9]/192.168.1.12/g' $eth2<br/>ip addr flush dev eth2<br/>ip addr add 192.168.1.12/24 dev eth2<br/>ip addr show dev eth2</pre>
<br/>
<br/>
<br/>
#######################################
<br/>
Test connectivity from test-dfw to test-ord
<br/>
#######################################
<br/>
<br/>
We'll do this in steps. I'll initiate a ping from test-dfw to test-ord. This will be done in steps.
<br/>
* On test-dfw, I'll start a ping to test-ord (ping 192.168.1.2).
<br/>
* On ovs-ord, I'll use tcpdump to listen for traffic on br0 and eth2
<br/>
* On test-ord, I'll use tcpdump to listen for traffic on eth2
<br/>
* If I don't receive a ping reply or traffic is lost along the path, I'll set VXLAN connectivity by assigning IP Addresses on the br0 interfaces of ovs-dfw (192.168.1.1) and ovs-ord (192.168.1.2). While I have addreses assigned to the br0 interfaces of ovs-{dfw, ord}, I'll test connectivity directly to their local LAN connected servers. On ovs-dfw, I'll ping test-dfw and on ovs-ord, I'll ping test-ord.
<br/>
<pre>[root@test-dfw ~]# ping 192.168.1.12<br/>PING 192.168.1.12 (192.168.1.12) 56(84) bytes of data.<br/>From 192.168.1.11 icmp_seq=1 Destination Host Unreachable<br/>From 192.168.1.11 icmp_seq=2 Destination Host Unreachable<br/>From 192.168.1.11 icmp_seq=3 Destination Host Unreachable<br/>From 192.168.1.11 icmp_seq=4 Destination Host Unreachable<br/>From 192.168.1.11 icmp_seq=5 Destination Host Unreachable</pre>
<br/>
<pre>[root@ovs-ord ~]# tcpdump -i br0 -XX -vvv -e -c 5<br/>tcpdump: WARNING: br0: no IPv4 address assigned<br/>tcpdump: listening on br0, link-type EN10MB (Ethernet), capture size 65535 bytes<br/>05:05:08.627796 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:09.628891 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:10.631546 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:12.629095 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:13.631575 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>5 packets captured<br/>5 packets received by filter<br/>0 packets dropped by kernel<br/>[root@ovs-ord ~]# tcpdump -i eth2 -XX -vvv -e -c 5<br/>tcpdump: WARNING: eth2: no IPv4 address assigned<br/>tcpdump: listening on eth2, link-type EN10MB (Ethernet), capture size 65535 bytes<br/>05:05:40.637676 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:41.637641 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:42.639147 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:44.643446 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>05:05:45.639364 bc:76:4e:04:82:f2 (oui Unknown) &gt; Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.1.12 tell 192.168.1.11, length 28<br/> 0x0000:  ffff ffff ffff bc76 4e04 82f2 0806 0001  .......vN.......<br/> 0x0010:  0800 0604 0001 bc76 4e04 82f2 c0a8 010b  .......vN.......<br/> 0x0020:  0000 0000 0000 c0a8 010c                 ..........<br/>5 packets captured<br/>5 packets received by filter<br/>0 packets dropped by kernel</pre>
<br/>
<pre>[root@test-ord ~]# date<br/>Sun Jan 13 05:11:08 UTC 2013<br/>[root@test-ord ~]# tcpdump -i eth2 -XX -vvv -e -c 5<br/>tcpdump: listening on eth2, link-type EN10MB (Ethernet), capture size 65535 bytes<br/>^C<br/>0 packets captured<br/>0 packets received by filter<br/>0 packets dropped by kernel<br/>[root@test-ord ~]# date<br/>Sun Jan 13 05:11:24 UTC 2013</pre>
<br/>
<pre>[root@ovs-dfw ~]# ip addr add 192.168.1.1/24 dev br0<br/>[root@ovs-dfw ~]# ping -c2 192.168.1.2<br/>PING 192.168.1.2 (192.168.1.2) 56(84) bytes of data.<br/>64 bytes from 192.168.1.2: icmp_req=1 ttl=64 time=60.5 ms<br/>64 bytes from 192.168.1.2: icmp_req=2 ttl=64 time=25.7 ms<br/><br/>--- 192.168.1.2 ping statistics ---<br/>2 packets transmitted, 2 received, 0% packet loss, time 1001ms<br/>rtt min/avg/max/mdev = 25.734/43.163/60.593/17.430 ms<br/>[root@ovs-dfw ~]# ping -c2 192.168.1.11<br/>PING 192.168.1.11 (192.168.1.11) 56(84) bytes of data.<br/>64 bytes from 192.168.1.11: icmp_req=1 ttl=64 time=252 ms<br/>64 bytes from 192.168.1.11: icmp_req=2 ttl=64 time=1.10 ms<br/><br/>--- 192.168.1.11 ping statistics ---<br/>2 packets transmitted, 2 received, 0% packet loss, time 1001ms<br/>rtt min/avg/max/mdev = 1.102/126.650/252.198/125.548 ms</pre>
<br/>
<pre>[root@ovs-ord ~]# ip addr add 192.168.1.2/24 dev br0<br/>[root@ovs-ord ~]# <br/>[root@ovs-ord ~]# ping -c2 192.168.1.1<br/>PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.<br/>64 bytes from 192.168.1.1: icmp_req=1 ttl=64 time=29.1 ms<br/>64 bytes from 192.168.1.1: icmp_req=2 ttl=64 time=26.8 ms<br/><br/>--- 192.168.1.1 ping statistics ---<br/>2 packets transmitted, 2 received, 0% packet loss, time 1001ms<br/>rtt min/avg/max/mdev = 26.899/28.039/29.180/1.152 ms<br/>[root@ovs-ord ~]# ping -c2 192.168.1.12<br/>PING 192.168.1.12 (192.168.1.12) 56(84) bytes of data.<br/>64 bytes from 192.168.1.12: icmp_req=1 ttl=64 time=33.8 ms<br/>64 bytes from 192.168.1.12: icmp_req=2 ttl=64 time=1.42 ms<br/><br/>--- 192.168.1.12 ping statistics ---<br/>2 packets transmitted, 2 received, 0% packet loss, time 1002ms<br/>rtt min/avg/max/mdev = 1.423/17.622/33.821/16.199 ms</pre>
<br/>
#######################################
<br/>
tpcdump of a successful ping between ovs-ord and test-ord
<br/>
#######################################
<br/>
<pre>[root@test-ord ~]# tcpdump -i eth2 -XX -vvv -e -c 5<br/>tcpdump: listening on eth2, link-type EN10MB (Ethernet), capture size 65535 bytes<br/>05:14:42.582679 bc:76:4e:10:5c:74 (oui Unknown) &gt; bc:76:4e:10:5a:89 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 84)<br/>    192.168.1.2 &gt; test-ord: ICMP echo request, id 13043, seq 1, length 64<br/> 0x0000:  bc76 4e10 5a89 bc76 4e10 5c74 0800 4500  .vN.Z..vN.\t..E.<br/> 0x0010:  0054 0000 4000 4001 b74a c0a8 0102 c0a8  .T..@.@..J......<br/> 0x0020:  010c 0800 a434 32f3 0001 c242 f250 0000  .....42....B.P..<br/> 0x0030:  0000 a670 0700 0000 0000 1011 1213 1415  ...p............<br/> 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%<br/> 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &amp;'()*+,-./012345<br/> 0x0060:  3637                                     67<br/>05:14:42.582755 bc:76:4e:10:5a:89 (oui Unknown) &gt; bc:76:4e:10:5c:74 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 43535, offset 0, flags [none], proto ICMP (1), length 84)<br/>    test-ord &gt; 192.168.1.2: ICMP echo reply, id 13043, seq 1, length 64<br/> 0x0000:  bc76 4e10 5c74 bc76 4e10 5a89 0800 4500  .vN.\t.vN.Z...E.<br/> 0x0010:  0054 aa0f 0000 4001 4d3b c0a8 010c c0a8  .T....@.M;......<br/> 0x0020:  0102 0000 ac34 32f3 0001 c242 f250 0000  .....42....B.P..<br/> 0x0030:  0000 a670 0700 0000 0000 1011 1213 1415  ...p............<br/> 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%<br/> 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &amp;'()*+,-./012345<br/> 0x0060:  3637                                     67<br/>05:14:43.583017 bc:76:4e:10:5c:74 (oui Unknown) &gt; bc:76:4e:10:5a:89 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 84)<br/>    192.168.1.2 &gt; test-ord: ICMP echo request, id 13043, seq 2, length 64<br/> 0x0000:  bc76 4e10 5a89 bc76 4e10 5c74 0800 4500  .vN.Z..vN.\t..E.<br/> 0x0010:  0054 0000 4000 4001 b74a c0a8 0102 c0a8  .T..@.@..J......<br/> 0x0020:  010c 0800 7b2e 32f3 0002 c342 f250 0000  ....{.2....B.P..<br/> 0x0030:  0000 ce75 0700 0000 0000 1011 1213 1415  ...u............<br/> 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%<br/> 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &amp;'()*+,-./012345<br/> 0x0060:  3637                                     67<br/>05:14:43.583067 bc:76:4e:10:5a:89 (oui Unknown) &gt; bc:76:4e:10:5c:74 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 43536, offset 0, flags [none], proto ICMP (1), length 84)<br/>    test-ord &gt; 192.168.1.2: ICMP echo reply, id 13043, seq 2, length 64<br/> 0x0000:  bc76 4e10 5c74 bc76 4e10 5a89 0800 4500  .vN.\t.vN.Z...E.<br/> 0x0010:  0054 aa10 0000 4001 4d3a c0a8 010c c0a8  .T....@.M:......<br/> 0x0020:  0102 0000 832e 32f3 0002 c342 f250 0000  ......2....B.P..<br/> 0x0030:  0000 ce75 0700 0000 0000 1011 1213 1415  ...u............<br/> 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%<br/> 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &amp;'()*+,-./012345<br/> 0x0060:  3637                                     67<br/>05:14:44.584026 bc:76:4e:10:5c:74 (oui Unknown) &gt; bc:76:4e:10:5a:89 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 84)<br/>    192.168.1.2 &gt; test-ord: ICMP echo request, id 13043, seq 3, length 64<br/> 0x0000:  bc76 4e10 5a89 bc76 4e10 5c74 0800 4500  .vN.Z..vN.\t..E.<br/> 0x0010:  0054 0000 4000 4001 b74a c0a8 0102 c0a8  .T..@.@..J......<br/> 0x0020:  010c 0800 8628 32f3 0003 c442 f250 0000  .....(2....B.P..<br/> 0x0030:  0000 c27a 0700 0000 0000 1011 1213 1415  ...z............<br/> 0x0040:  1617 1819 1a1b 1c1d 1e1f 2021 2223 2425  ...........!"#$%<br/> 0x0050:  2627 2829 2a2b 2c2d 2e2f 3031 3233 3435  &amp;'()*+,-./012345<br/> 0x0060:  3637                                     67<br/>5 packets captured<br/>6 packets received by filter<br/>0 packets dropped by kernel</pre>
<br/>
