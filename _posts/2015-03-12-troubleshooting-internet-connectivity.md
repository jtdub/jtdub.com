---
layout: post
title: Troubleshooting Internet Connectivity
date: '2015-03-12'
author: jtdub
tags:
- troubleshooting
- Network Connectivity
- Rackspace
- packetgeek.net
---

This evening, I noticed that I was having some horrible Internet connectivity issues, from home. Trying to stream anything online? Forget it. Frustrated, I started troubleshooting the issue, fully expecting that I would end up opening up a trouble ticket with my ISP, sending them all my available troubleshooting information, and asking them to resolve their issue.

Turns out, the issue was a simple fix - on my side, but I figured that I would provide my troubleshooting steps as a learning experience for anybody whom runs across this page.

Background information: My home Internet connectivity is provided by Cable Internet with a 30Mbps downstream / 5Mbps upstream.

The first thing that I did was go to http://speedtest.rackspace.com. From this page, you can run the OOKLA speedtest application from any of their data centers. This provides excellent information on download &amp; upload speeds, latency, and jitter. I ran the test from the Dallas and Chicago data centers. Right off the bat, I noticed that I was getting a fraction of the download speed that my Internet service is configured for. This can be seen below:

<img src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/fad74037-a2e4-479e-1965-620b94ea0d00/public"/>

<img src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/9067939b-fc09-4304-d860-3bb59f5dbc00/public"/>

This immediately pointed to a real issue, but I didn't yet have all the information that I needed to take to my ISP. Next, I used an application called MTR. MTR is a traceroute application, that when ran correctly makes it visually easy to spot potential network issues. I ran an MTR report destined to one of my cloud servers at Rackspace.

```bash
~]# mtr --report --mpls --show-ips --report-cycles=100 xxxxxxxxxxxxxxxxxxxxxxxxx
Start: Fri Mar 13 01:50:12 2015
HOST: xxxxxxxxxxxxxxxxxxxx        Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- 172.16.1.1                 0.0%   100    2.3   2.1   0.8  10.7   1.1
  2.|-- 172.16.0.34                0.0%   100    0.9   1.1   0.7  15.9   1.4
  3.|-- 192.168.0.1                0.0%   100    1.8   2.2   1.5  20.9   2.3
  4.|-- cpe-24-160-128-1.satx.res  9.0%   100   14.1  19.1   9.6  37.9   7.6
  5.|-- 24.28.133.9                4.0%   100   30.6  33.3  17.1  64.2   8.1
  6.|-- be12.lvoktxad01r.texas.rr  7.0%   100   17.5  18.2   9.5  44.7   6.4
  7.|-- agg21.snavtxuu02r.texas.r 21.0%   100   36.8  19.2  10.1  46.2   8.2
  8.|-- agg23.hstqtxl301r.texas.r 21.0%   100   18.4  26.0  14.9  45.3   7.9
  9.|-- bu-ether46.hstqtx0209w-bc 20.0%   100   20.8  26.3  15.3  46.1   9.1
 10.|-- bu-ether12.dllstx976iw-bc  2.0%   100   22.6  29.9  18.6  53.7   8.0
 11.|-- 0.ae4.pr1.dfw10.tbone.rr.  9.0%   100   23.5  25.2  17.5  50.6   6.9
 12.|-- 66.109.11.22               5.0%   100   28.1  25.1  17.4  44.7   6.1
 13.|-- ae8.er1.dfw2.us.zip.zayo.  5.0%   100   23.3  26.0  18.3  66.5   8.3
 14.|-- 128.177.70.86.IPYX-076520 12.0%   100   24.0  26.7  18.4  47.3   6.8
 15.|-- 10.25.1.71                18.0%   100   36.5  26.7  18.1  49.8   7.0
 16.|-- be42.coreb.dfw1.rackspace 21.0%   100   26.4  30.0  19.5  50.4   8.4
 17.|-- po2.coreb-core9.core9.dfw 17.0%   100   27.2  31.9  21.7  64.5   9.4
 18.|-- core9.aggr160b-3.dfw2.rac  5.0%   100   22.4  30.2  21.2  50.7   7.9
 19.|-- xxxxxxxxxxxxxxxxxxxxxxxxx  7.0%   100   26.0  26.9  20.2  47.6   5.5
```

You look at the 'loss%' column, you will notice that the MTR reports packet loss, starting at hop 4. This packet loss continues at every hop in the path. Hop 4 is the gateway of my Cable Internet. This suggests that the actual network issue exists between my cable modem and my providers router. To further solidify this finding, I ran a 100 count ping to that same server, hosted at Rackspace.

```bash
--- xxxxxxxxxxxxxxxxxxxxxxxxx ping statistics ---
100 packets transmitted, 91 packets received, 9.0% packet loss
round-trip min/avg/max/stddev = 19.296/31.589/49.183/7.557 ms
Fri Mar 13 01:53:43 CDT 2015
```

Indeed, the ping saw the same packet loss. Before opening a ticket with my Internet provider, I decided to power cycle my cable modem. After my cable modem was back online, I ran the same tests.

First with the speed tests.

<img src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/fe05fe22-4fff-4768-c8aa-84ca3084cf00/public"/>

<img src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/89eef152-bbdd-4dbb-788f-92165fb07e00/public"/>

Huge difference! Next, I ran the same MTR report.

```bash
~]# mtr --report --mpls --show-ips --report-cycles=100 xxxxxxxxxxxxxxxxxxxxxxxxx
Start: Fri Mar 13 01:59:19 2015
HOST: xxxxxxxxxxxxxxxxxxxx        Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- 172.16.1.1                 0.0%   100    2.4   2.1   0.9   7.5   0.8
  2.|-- 172.16.0.34                0.0%   100    0.8   0.9   0.7   2.2   0.1
  3.|-- 192.168.0.1                0.0%   100    2.5   2.3   1.5  13.9   1.6
  4.|-- cpe-24-160-128-1.satx.res  0.0%   100   13.0  15.0   9.4  24.2   2.8
  5.|-- 24.28.133.9                0.0%   100   22.7  30.3  15.1  66.2   6.6
  6.|-- be12.lvoktxad01r.texas.rr  0.0%   100   17.6  14.5   9.1  26.4   3.0
  7.|-- agg21.snavtxuu02r.texas.r  0.0%   100   19.8  16.0   9.7  31.6   4.2
  8.|-- agg23.hstqtxl301r.texas.r  0.0%   100   17.3  20.9  13.2  40.8   4.5
  9.|-- bu-ether46.hstqtx0209w-bc  0.0%   100   25.9  22.5  14.3  52.4   5.5
 10.|-- bu-ether12.dllstx976iw-bc  0.0%   100   22.9  24.8  18.2  42.0   3.8
 11.|-- 0.ae4.pr1.dfw10.tbone.rr.  0.0%   100   26.2  24.2  17.2  75.7   7.1
 12.|-- 66.109.11.22               0.0%   100   18.4  23.7  16.9  42.8   4.3
 13.|-- ae8.er1.dfw2.us.zip.zayo.  0.0%   100   25.5  23.8  16.8  61.7   6.4
 14.|-- 128.177.70.86.IPYX-076520  0.0%   100   29.6  24.7  19.1  37.5   3.0
 15.|-- 10.25.1.71                 0.0%   100   29.1  24.3  17.6  47.0   4.6
 16.|-- be42.coreb.dfw1.rackspace  0.0%   100   22.6  24.6  19.1  45.2   3.7
 17.|-- po2.coreb-core9.core9.dfw  0.0%   100   26.6  26.5  19.9  37.2   3.5
 18.|-- core9.aggr160b-3.dfw2.rac  0.0%   100   23.9  26.9  19.9  41.7   3.7
 19.|-- xxxxxxxxxxxxxxxxxxxxxxxxx  0.0%   100   39.6  25.4  19.1  39.6   3.1
```

Notice how the packet loss is completely gone now? Finally, I ran the same 100 count ping.

```bash
 --- xxxxxxxxxxxxxxxxxxxxxxxxx ping statistics ---
100 packets transmitted, 100 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 20.903/29.353/62.735/4.888 ms
Fri Mar 13 02:00:56 CDT 2015
```

Confirmed. No packet loss. As you can see, the issue ended up being that my cable modem needed to be power cycled. No inundating my Internet provider with a trouble ticket tonight.

Simple tools, such as MTR, traceroute, and ping can provide a lot of information about network connectivity problems. At the very least, they can assist you in narrowing down where to look.
