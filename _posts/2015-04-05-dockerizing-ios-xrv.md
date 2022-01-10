---
layout: post
title: Dockerizing IOS-XRv
date: '2015-04-05'
author: jtdub
tags:
- Linux
- Software Defined Networking
- Miscellaneous Hacking
- SDN
- NFV
- Cisco VIRL
- Docker
- KVM
- openvswitch
- IOS-XR
- packetgeek.net
---

I've been playing with docker off and on for about a year or so now. One of my ideas, with Docker, is to use it for my network lab. These days, I've mostly virtualized my lab. Lately, been doing a lot of it in VIRL, but this hasn't stopped me from tinkering.
<br/>
<br/>
For a while, I've had a base docker container that sets up Open vSwitch and KVM. Once the docker container is started, you can access the container and spin up VM's or play with Open vSwitch. The Dockerfile to set this container up can be found on my
<a href="https://github.com/jtdub/docker-centos-kvm-ovs" target="_blank" title="Docker, CentOS, KVM, OVS">
 github
</a>
.
<br/>
<br/>
The next iteration of this was to actually have the VM in the container and have it boot up directly. I did this with IOS-XRv. It's a pretty straight forward set up. The Dockerfile uses centos:6 as its base, installs a couple yum repositories, installs needed packages, and adds the associated files. When it's all done, you have a docker container that will run the IOS-XRv. You can spin this container up and down at will. It's pretty nifty.
<br/>
<br/>
My next goal in this set up is to have the container generate dynamic mac addresses for IOS-XRv when it boots up. Currently the mac addresses are hard coded. The reasoning for this is that I eventually want Open vSwitch to connect to a 'controller' Open vSwitch via VXLAN or GRE. The purpose of this is to spin up multiple containers and have them all connect to each other. This will make the lab environment much more flexible and scalable.
<br/>
<br/>
Anyways, check out the
<a href="https://github.com/jtdub/docker-ios-xrv/blob/master/Dockerfile" target="_blank" title="CentOS, KVM, OVS, and IOS-XRv!">
 docker-ios-xrv github
</a>
for the README, Dockerfile, and associated files. I'll post more when I have updates.
