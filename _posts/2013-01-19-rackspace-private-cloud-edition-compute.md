---
layout: post
title: Rackspace Private Cloud Edition - Compute Setup
date: '2013-01-19'
author: jtdub
tags:
- Openstack
- Private Cloud Edition
- Rackspace
- packetgeek.net
---

I finally got a chance to sit down and play with pre-built Open Stack 'Private Cloud Edition' built by Rackspace. Once it's installed, you can spin up instances right out of the box, but there are a few nuances to getting a functional platform for remote access and serving. I figured that I'd do a run through of the install and the initial changes that I made to get my install working.

The first thing that you need to do is obtain the Private Cloud Edition (PCE) iso. The iso can be downloaded for FREE at the Rackspace website - [http://www.rackspace.com/cloud/private/](http://www.rackspace.com/cloud/private/). Once it's downloaded and you have a bootable thumb drive or DVD, you're ready to rock! The system requirements for Installing PCE on the Rackspace website are pretty stout. They list the controller node as needing 16 GB of RAM, 144 GB of disk space, and a dual socket CPU with dual cores or a single quad core. Then they list the compute node as needing the same specs with the exception of RAM, which they list as 32 GB. Those are more of recommendations. I installed the compute and controller node (all-in-one) on a single desktop PC with a single dual core CPU, 4 GB of RAM, and a 80 GB hard drive. For testing purposes, this is completely fine. The requirement that is needed is that your CPU's will need to support virtualization technologies (VT-x), as the underlying hypervisor runs on KVM.

The install is a pretty painless process. The first screen prompts you for a EULA, then how what you want to install - Controller, Compute, or All-in-One.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/42dae73b-4219-4b6d-ec45-67e386c7e300/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

After that, you set up the IP Address of the server, the netblock assigned to VM's, (the default is 172.31.0.0/24 - I left this default), and the user accounts (admin Open Stack account, Open Stack user account, and server local user account). After that it's a matter of the automated installer installing the packages. Once it's done installing, it will boot up and you'll be ready to play!

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/c811d5a7-1fdc-446b-08c9-561a4b8f7b00/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

If you've ever used the Rackspace public cloud, you will notice that the UI looks very familiar. Though, if you prefer, the UI can be changed to the default Open Stack UI. The first thing that we'll want to do when we log in is to grab your API credentials, so that you can easily use the command line tools. To do this, log in with your admin account, select the 'Settings' link at the top right of the screen, then select the "OpenStack API" tab, select 'admin' as the project, and finally press the "Download RC File" button.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/24b4efb0-41ef-44e0-9dfa-4af24c7fe400/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

Once the openrc.sh file is downloaded, you can copy it to your PCE server so that we can begin configuring what needs to be configured from the command line. As you can see below, I used scp to copy the file to the server.

```bash
[jtdub@jtdub-desktop Downloads]$ scp openrc.sh james@172.16.2.254:/home/james/.novarc
james@172.16.2.254's password: 
openrc.sh 
```

After the file is copied to the server, we'll ssh to the server and use the CLI tools to configure floating IP Addresses. The one thing that I've noticed while playing around with Open Stack is that, at least in my limited experience, the 'nova-manage' and chef commands will not properly execute unless you have administrative privileges on the server, therefore, I generally go ahead and 'sudo su -' to root while I'm using the 'nova-manage' and chef commands, but will continue to utilize my non-privileged account for using the 'nova' command.

So, let's add a floating IP Address range. My PCE All-in-One server is currently sitting on the 172.16.2.0/24 network. 172.16.2.1 is the router, 172.16.2.254 is the PCE server, and there is another computer on 172.16.2.12. I want to add a range of addresses that will be on the 172.16.2.0/24 network, but will not conflict with existing hosts. For testing purposes, I do not need a large number of addresses, so I decided to carve out a section of my 172.16.2.0/24 network to assign as floating IP Addresses to instances that spin up. In my case, I only need about 16 addresses, so I chose to use the prefix of 172.16.2.32/28. That will tell Open Stack to assign addresses 172.16.2.33 - 46 to VM instances as they spin up and will re-claim those addresses as the instances are torn down. This allows me to continue to utilize the 172.16.2.0/24 network without conflict.

```bash
james@openstack:~$ sudo su -
root@openstack:~# source /home/james/.novarc 
Please enter your OpenStack Password: 
root@openstack:~# nova-manage floating create --pool=172.16.2.32-net --ip_range=172.16.2.32/28
2013-01-19 23:49:15 DEBUG nova.utils [req-99d8cbf4-8821-4c3d-afc7-9a584cfc1748 None None] backend <module 'nova.db.sqlalchemy.api' from '/usr/lib/python2.7/dist-packages/nova/db/sqlalchemy/api.pyc'> __get_backend /usr/lib/python2.7/dist-packages/nova/utils.py:502
root@openstack:~# nova-manage floating list
2013-01-19 23:49:22 DEBUG nova.utils [req-034aa938-a81f-428b-be81-96895607bb4c None None] backend <module 'nova.db.sqlalchemy.api' from '/usr/lib/python2.7/dist-packages/nova/db/sqlalchemy/api.pyc'> __get_backend /usr/lib/python2.7/dist-packages/nova/utils.py:502
None 172.16.2.33 None 172.16.2.32-net br0
None 172.16.2.34 None 172.16.2.32-net br0
None 172.16.2.35 None 172.16.2.32-net br0
None 172.16.2.36 None 172.16.2.32-net br0
None 172.16.2.37 None 172.16.2.32-net br0
None 172.16.2.38 None 172.16.2.32-net br0
None 172.16.2.39 None 172.16.2.32-net br0
None 172.16.2.40 None 172.16.2.32-net br0
None 172.16.2.41 None 172.16.2.32-net br0
None 172.16.2.42 None 172.16.2.32-net br0
None 172.16.2.43 None 172.16.2.32-net br0
None 172.16.2.44 None 172.16.2.32-net br0
None 172.16.2.45 None 172.16.2.32-net br0
None 172.16.2.46 None 172.16.2.32-net br0
```

At this point, I should spend a little bit of time to describe how the networking for VM instances is going to work. When we initially installed PCE, we were prompted with a screen asking us for a CIDR block for Nova fixed (VM) networking. The default is 172.31.0.0/24

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/3998ff99-622e-4391-a3ef-132aee79db00/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

One IP Address on the 172.31.0.0/24 will be allocated to the br0 interface of your PCE server and the remaining will be assigned to your instances as they boot up. The br0 interface will also contain the IP Address of your PCE server. In this case, that IP Address will be 172.16.2.254.

```bash
root@openstack:~# ip addr show br0
3: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
    link/ether 00:23:ae:90:aa:7c brd ff:ff:ff:ff:ff:ff
    inet 172.31.0.5/24 brd 172.31.0.255 scope global br0
    inet 172.16.2.254/24 brd 172.16.2.255 scope global br0
    inet6 fe80::4858:14ff:fe72:7112/64 scope link 
       valid_lft forever preferred_lft forever
root@openstack:~# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.16.2.1      0.0.0.0         UG    100    0        0 br0
169.254.123.0   0.0.0.0         255.255.255.0   U     0      0        0 chefbr0
172.16.2.0      0.0.0.0         255.255.255.0   U     0      0        0 br0
172.31.0.0      0.0.0.0         255.255.255.0   U     0      0        0 br0
```

The br0 interface is a bridge interface that connects the VM network to the physical interface, eth0. Open Stack then routes (layer 3) traffic coming from eth0 to the 172.31.0.0/24 network. It also uses iptables to create a PAT/NAT, so that the instances can communicate on the network, and the internet if you allow it. However, computers outside the PCE environment can't communicate with the VM instances directly, because those computers will be unaware of the 172.31.0.0/24 network. This is where the floating IP Addresses come into play. The floating IP Addresses create a one-to-one NAT mapping a VM instance to an address in your floating IP Address range. In this case, my floating IP Address range is 172.16.2.32/28. Also, by default, the PCE iptables rules are very restrictive and don't allow incoming traffic to communicate with the VM instances. To allow this traffic, you will have to create or edit security groups. This will come later on. Below is a diagram of the PCE network environment.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/673064c6-b357-4a3f-3281-dfd29be17500/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

Now that we understand how the networking works, let's log back into the UI as a normal user. As the normal user, we're going to edit our default security group to define what traffic we want to allow to our VM instances, we'll add a couple floating IP Addresses to our project, create keypairs that will be used to allow us to access our VM, we'll add a pre-built Fedora 17 image to our default images, and finally, we'll spin up an instance and verify that we can access it from an outside computer.

Once we login as our normal user, the first thing that we'll do is edit our default security group to define what traffic that we want to allow to our VM instances from the outside world by default. In my test, I am going to allow ICMP echo (code -1, type -1), all UDP traffic, and all TCP traffic. To access the security groups, select the "Access &amp; Security" tab along the top menu, locate the "Security Groups" section, and press the "Edit Rules" on the default group.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/2c075f52-96d6-4c3b-da0e-77d496eafe00/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

Once you've located that screen, enter your rules.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/203625f7-3134-491f-e328-b60d17f17300/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

Now that the security group has been edited, we'll go ahead and add floating IP Addresses, which are on the same "Access &amp; Security" page. To do this, press the "Allocate IP To Project" button, select your pool, if you have multiple IP Address pools, and press the  "Allocate IP" button. You can add as many IP Addresses as you need for your project. By default, there are quotas in place that limits a "project" to 10 floating IP Addresses. This quota can be changed and will be discussed later on.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/bba31e09-d977-44bd-cd57-f2ab34b24200/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

Lastly, on the same "Access &amp; Security" page let's generate encryption key pairs that will be used to access our VM instances. In the "Keypairs" section, press the "Create Keypair" button. This will bring up a screen that will allow you to name the key pair.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/ad39fb0b-7ac0-4be4-28bb-0d382a49d100/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

Once the keypair has been generated, you'll be prompted to download a pem file. Do so, and then add the keypair to your keys for ssh. In Linux, you use the ssh-add command. As this is a private key, you won't want any other users to be able to read the key, so be sure to change the permissions on the file so that only your account can access the file.

```bash
[jtdub@jtdub-desktop Downloads]$ chmod 600 jtdub-keypair.pem 
[jtdub@jtdub-desktop Downloads]$ ssh-add jtdub-keypair.pem 
Identity added: jtdub-keypair.pem (jtdub-keypair.pem)
```

We're at the light at the end of the tunnel! If you wanted to, you could now just spin up VM instances utilizing the default images that come with PCE. However, I'm going to download a pre-built image of Fedora 17, so that I can demonstrate how to import images. The Fedora 17 image that I'm going to use can be downloaded at [http://berrange.fedorapeople.org/images/](http://berrange.fedorapeople.org/images/). In your UI, still logged in as the unprivileged user, select the "Images &amp; Snapshots" tab. Once there, select the "Create Image" button, fill out the information on the form, and press the "Create Image" button.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/9676cf50-5427-4bf7-d523-349a84324800/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

Now, you just wait for the image to download. It will take a little while depending on the speed of your Internet connection, as well as the size of the image.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/038862de-b802-4304-06c1-fdb482e1f000/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

When the image download completes, we can finally create our first instance. This can be accomplished from the "Instances" tab, in the UI, by pressing the "Launch Instance" button. On the Launch Instance page there are several options. It's best to spend a few minutes to get familiar with the options. I'll give a run down of the settings that I used.

* Details Tab:
  * "Image", I selected my newly minted fedora17-image.
  * "Instance Name", I chose the name f17-test
  * "Flavor", I left a m1.tiny (512MB / RAM) instance.
* Access &amp; Security Tab:
  * "Keypair", I chose my jtdub-keypair

After that, I pressed the "Launch" button. In no time flat, my first instance was up and running. The only other thing that I need to do is associate a floating IP Address to the VM instance.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/1ddfc8d4-d33f-4f12-79e1-48ac304b3100/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/7d8fad17-aacc-4ffa-4600-f3f377776f00/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

To associate a floating IP Address to an instance, locate your VM Instance on the "Instances" page, drop down the menu on the "Create Snapshot" button, and select "Associate Floating IP". Once the "Manage Floating IP Associations" page pulls up, select and IP Address and press the "Associate" button.

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/c38ecb4e-3f43-4940-800a-6abe175dc300/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/3b1218ed-919a-486a-530f-af6cafbdbc00/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

That's it! The first instance is up and running and should be remotely accessible! To test it, I'll ssh to the instance.

```bash
[jtdub@jtdub-desktop ~]$ ping -c2 172.16.2.33
PING 172.16.2.33 (172.16.2.33) 56(84) bytes of data.
64 bytes from 172.16.2.33: icmp_seq=1 ttl=62 time=0.870 ms
64 bytes from 172.16.2.33: icmp_seq=2 ttl=62 time=0.801 ms

--- 172.16.2.33 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.801/0.835/0.870/0.045 ms
[jtdub@jtdub-desktop ~]$ ssh -l root 172.16.2.33
The authenticity of host '172.16.2.33 (172.16.2.33)' can't be established.
RSA key fingerprint is 3d:ec:47:85:9c:72:9b:3c:87:b6:0a:25:fa:7d:0b:d9.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '172.16.2.33' (RSA) to the list of known hosts.
[root@f17-test ~]# ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether fa:16:3e:77:9d:16 brd ff:ff:ff:ff:ff:ff
    inet 172.31.0.2/24 brd 172.31.0.255 scope global eth0
    inet6 fe80::f816:3eff:fe77:9d16/64 scope link tentative dadfailed 
       valid_lft forever preferred_lft forever
```

That's it! We now have a PCE compute cloud running. Whew! LONG blog! So for now, I'll wrap this up. Soon, I'll create another much shorter blog to show how to modify the UI back to the default Open Stack UI, if you prefer. In that same blog, I'll also talk about project quotas and how to modify them. That's it for now! Thanks for reading.

Documentation References:
* [http://docs.openstack.org/trunk/openstack-compute/admin/content/ch_getting-started-with-openstack.html](http://docs.openstack.org/trunk/openstack-compute/admin/content/ch_getting-started-with-openstack.html)
* [http://www.rackspace.com/knowledge_center/getting-started/rackspace-private-cloud](http://www.rackspace.com/knowledge_center/getting-started/rackspace-private-cloud)
