---
layout: post
title: Prepping Ubuntu Server Edition to run as a DMVPN.
date: '2009-05-31'
author: jtdub
tags:
- Ubuntu SE
- VPN
- Perl Tips
- packetgeek.net
---

After reading about the open source implementation of NHRP, I decided that I would play around with it a bit to see where it's at, development wise. I have a VMWare Session of Ubuntu 9.04 (Server Edition) that I use to geek out on stuff like this. It's nice, because at a click of a button I can have a default install, by reverting to my default snap shot.

I've determined that the packages that you need to install, on a default install of Ubuntu SE are:

* openssh-server
* quagga
* ipsec-tools
* racoon
* gcc
* git
* git-core
* pkg-config
* libc-ares-dev
* make

Gcc, make, git, git-core, pkg-config, and libc-ares-dev are the packages required to compile openNHRP from source. They can probably be uninstalled after it's been compiled. :)

Openssh-server is just used to admin the box remotely. It's easier to do everything over ssh, rather than through the vm window.

Quagga is the routing software. It's not required to install opennhrp, but I figured I might as well install it. Same goes for ipsec-tools.

Iproute2, which supports the GRE implementation, is installed by default, so we don't need to worry about it.

I wrote a quick perl script to run on Ubuntu to check to see whether the packages are installed. If they aren't it installs them via apt-get.
```perl
#!/usr/bin/perl

@software = ('openssh-server','ipsec-tools','racoon','quagga','gcc',
     'git','git-core','pkg-config','libc-ares-dev','make');

foreach $pkg (@software) {
    chomp($pkg);
    @dpkg = `dpkg -l | grep $pkg`;
    if(!@dpkg) {
         print "Getting: $pkg\n";
        `sudo apt-get -y install $pkg`;
    } else {
         print "$pkg is already installed.\n";
    }
}
```

After you run that perl script, opennhrp is ready to install. Download the latest version from http://sourceforge.net/projects/opennhrp/, unpack the contents, then run make and make install. That's it! Now to play with configurations.
