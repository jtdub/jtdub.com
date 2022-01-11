---
layout: post
title: Playing with Openvswitch.
date: '2012-12-29'
author: jtdub
tags:
- Linux
- Software Defined Networking
- SDN
- openvswitch
- packetgeek.net
---

I've been playing with openvswitch a little bit this evening. Here are some notes that I took for a very basic configuration on Ubuntu 12.04.

------------------------------------------------------------

Documentation References

------------------------------------------------------------

* [http://networkstatic.net/openflow-openvswitch-lab/](http://networkstatic.net/openflow-openvswitch-lab/)
* [http://openvswitch.org/support/config-cookbooks/vlan-configuration-cookbook/](http://openvswitch.org/support/config-cookbooks/vlan-configuration-cookbook/)
* [https://help.ubuntu.com/community/BridgingNetworkInterfaces](https://help.ubuntu.com/community/BridgingNetworkInterfaces)

------------------------------------------------------------

Install, Update, and Configure Ubuntu

------------------------------------------------------------

Installed Ubuntu 12.04 from a thumb drive.
- Started with an 80 GB drive / 4 GB RAM
- Chose custom partitioning
- 500 MB /boot partition
- 4 GB swap partition
- 10 GB / partition
- remaining untouched (~65 GB) will be converted to LVM later.

```bash
apt-get -y install vim openssh-server lvm2
apt-get -y update
apt-get -y dist-upgrade
reboot

apt-get -y purge network-manager

echo "auto eth0
iface eth0 inet static
address 172.16.2.11
netmask 255.255.255.0
network 172.16.2.0
broadcast 172.16.2.255
dns-nameservers 172.16.2.1
gateway 172.16.2.1" >> /etc/network/interfaces

/etc/init.d/networking restart 
```

------------------------------------------------------------

Install Openvswitch

------------------------------------------------------------

```bash
apt-get -y install openvswitch-datapath-source bridge-utils
module-assistant auto-install openvswitch-datapath
apt-get -y install openvswitch-brcompat openvswitch-common 
```

------------------------------------------------------------

Test Openvswitch Install

------------------------------------------------------------

```bash
service openvswitch-switch status
ovs-vsctl show 
```

------------------------------------------------------------

Configure Openvswitch

------------------------------------------------------------

The first thing that we'll want to do is enable bridging compatibility.

Bridging will act as the interface between the hypervisor physical network cards and the virtual machines. This will be controlled by openvswitch.

```bash
sed -i 's/# BRCOMPAT=no/BRCOMPAT=yes/g' /etc/default/openvswitch-switch
service openvswitch-switch restart 
```

Once the bridging compatibility has been enabled and openvswitch restarted, we'll need to define a bridging interface and add the physical nic to the bridge.

*/ NOTE: This should be performed on the physical computer as it will bring down the networking to the host /*

```bash
sed -i 's/eth0/br0/g' /etc/network/interfaces
echo "auto eth0
iface eth0 inet manual
up ip link set eth0 up" >> /etc/network/interfaces
ovs-vsctl add-br br0
ovs-vsctl add-port br0 eth0
/etc/init.d/networking restart
```

At this point, the networking should be working again and you should be able to log into the host remotely.
