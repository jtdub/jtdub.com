---
layout: post
title: Cisco VIRL - Bare Metal Install Tips and Lessons Learned
date: '2014-12-03'
author: jtdub
tags:
- Linux
- Miscellaneous Hacking
- Cisco VIRL
- Misc.
- packetgeek.net
---

In my first post on VIRL -  "[Cisco VIRL Status? Digital Paper Weight](http://www.packetgeek.net/2014/12/cisco-virl-status-digital-paper-weight/)", I shared my frustration with not being able to get my system to activate with Cisco. Come to find out, I'm a dim wit. That is, in the 'Salt ID and domain' section, I mistakenly left the *.pem* suffix in the name. Ironically, I blurred out that section, in an attempt to retain some privacy. However, if I hadn't somebody may have rightly pointed out my error.

Given that, The VIRL install isn't a point and click and all is good in router land. There are some details here and there, that should be ironed out. In this post, I'll list some of the items that stood out, as I installed, found a quirk, and re-installed.

I did a bare-metal install. That is, I installed it on a physical computer, rather than a VM. The first quirk that I noticed is that udev immediately renamed eth0 to p3p1. Not a huge deal, however, the install requires that you have Internet access. By default, eth0 is set to DHCP an address, for Internet connectivity. After booting into the LiveCD environment, I needed to get network connectivity. To do this, I needed to get p3p1 and address. You can verify that eth0 has been renamed and what it's been renamed to by executing `dmesg | grep eth0` from a terminal prompt.

Here's my steps:

*Note: I make some assumptions:*
* 172.16.1.1 is the default gateway
* An address will be obtained via DHCP
* p3p1 is the name of the renamed ethernet interface
* Open xterm
* Sudo to root
  * sudo su -
* Use sed to rename eth0 to p3p1 in /etc/network/interfaces
  * sed -i 's/eth0/p3p1/g' /etc/network/interfaces
* Restart the network stack
  * service networking restart
* Verify that you have an IP Address
  * ip addr show dev p3p1
* Verify network connectivity
  * ping -c 1 172.16.1.1
  * ping -c 1 4.2.2.2
  * ping -c 1 google.com

If you need to assign a static IP Address, you'll need to manually edit the /etc/network/interfaces file.
* Using your favorite text editor, open /etc/network/interfaces
* In the p3p1 section, replace dhcp with static
* Modify the config so that it resembles the below example:

```
auto p3p1
iface p3p1 inet static
     address 172.16.1.51
     netmask 255.255.255.192
     gateway 172.16.1.1
```

Remember to substitute the 172.16.x.x addresses and netmask for your specific network. Also, leave the dns-nameservers section in, but change the name servers to suite your network.
* After the necessary changes have been made, save the changes and exit the file.
* Restart the network stack.
  * service network restart
* After doing this, it may be necessary to restart the individual network interface, so that it pulls its current settings
  * ifdown p3p1
  * ifup p3p1

From here, the install should be ready to go. After the install is complete and the computer has been rebooted. Here are some of the notes that I made.
* Cisco mistakenly left Cisco internal network specific name servers in the /etc/ntp.conf. This needs to be changed. It can be quickly done via sed.
  * sudo sed -i 's/ntp.esl.cisco.com/pool.ntp.org/g' /etc/ntp.conf
* After the change has been made, stop the NTP service
  * sudo service ntp stop
* SYNC the system clock
  * sudo ntpd -gq pool.ntp.org
* Start NTP
  * sudo service ntp start
* From here, the activation should work properly. Don't be a dim wit, like myself, and leave the *.pem* suffix on the Salt ID and domain.

After that, It's a mater of editing the /etc/virl.ini file. Take note that all the variables are lower case with under scores ("_") between words in a variable. There are at least two variables that mistakenly have upper case letters, thus won't be recognized by the automation and skipped - forcing you to either re-install or hack your way through the remainder of the install. Here are the variables that I noticed:
* *Static_IP* should be *static_ip*
* *internalnet_IP* should be *internalnet_ip*

I also noticed that the 'dummy' interfaces don't work above the number 4 - I attempted to create a dummy interface scheme that matched my ip prefixes. That didn't work out to well. I'm also noticed that the *internalnet* section changes itself to 172.16.10.0/24 - according to /etc/network/interfaces and MySQL, but it's completely different in my /etc/virl.ini and I'm not certain where it's getting that prefix from, yet.

Once you get VIRL up and working, copy your /etc/virl.ini file off to another computer. That way, if you have to re-install, you can make quick work of the re-install.

I'm sure that I'll find more things. As I do, I'll take notes of them and post updates.

