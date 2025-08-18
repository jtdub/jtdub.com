---
layout: post
title: Cisco VIRL Status? Digital Paper Weight
date: '2014-12-03'
author: jtdub
tags:
- Miscellaneous Hacking
- Cisco VIRL
- Misc.
- packetgeek.net
---
**Update:** *I fixed the issue. Turns out, I'm a dim wit. There is an updated post, with tips and lessons learned, [here](http://www.packetgeek.net/2014/12/cisco-virl-bare-metal-install-tips-and-lessons-learned/)*.

I was excited that VIRL was finally released. On impulse, I went ahead and bought it, even though I thought it was a little pricey. So far, I haven't had any luck with it. It appears that I'm not the only one.

For my install, I chose bare-metal, as I had the computer to spare. The install is a little clunky, but I worked my way through it. Udev changed the designated eth0 device to p3p1, which I'm used to and made the necessary changes in /etc/network/interfaces. After the install, you're supposed to configure NTP and activate the VIRL instance with Cisco's salt infrastructure. This is where the rub comes in. No matter what I do or try, I can't get it to register.

I've configured NTP - and verified that I had a proper NTP association per these two support threads:

* [Activation Error](http://community.dev-innovate.com/t/activation-error/743)
* [VIRL Time and NTP Requirements](http://community.dev-innovate.com/t/virl-time-and-ntp-requirements/783)

I've verified that my VIRL instance can ping the Cisco salt infrastructure. I can also telnet to their service ports. From my view. It should be working, but no matter what I do, I get this screen:

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/c2d737c4-02c3-4b3e-a61d-d37897bb6b00/public"
   alt="Network diagram or configuration screenshot"
   loading="lazy" %}

I'm also a little irritated with the VIRL support forums, as I can't post this screen shot, because I'm a 'new users'. The best that I can do is link to it.

If you know what I may be doing wrong - or if you know of a fix, shoot me a DM on [twitter](http://twitter.com/packetgeeknet).
