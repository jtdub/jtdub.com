---
layout: post
title: 'Mental Note: Tracking L3 Glean Attacks'
date: '2014-11-28'
author: jtdub
tags:
- network security
- IOS
- Routing Protocols
- L3 glean
- cisco
- Layer 3 Switching
- packetgeek.net
---

Here's a handy debug command for tracking L3 Glean attacks on IOS based Cisco routers / L3 switches.

```
debug platform packet all receive buffer
```
```
show platform cpu packet buffered | i src|dst
```

From there, you can take the output, paste the contents into a file, then use some Linux foo to determine the attacker.

```
cat file.txt | awk '{print $2}' | sort | uniq -c | sort
```

Supporting documentation: [Built-in CPU Sniffer](http://www.cisco.com/c/en/us/support/docs/switches/catalyst-4000-series-switches/65591-cat4500-high-cpu.html#tool2)
