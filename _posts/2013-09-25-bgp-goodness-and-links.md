---
layout: post
title: BGP Goodness and Links
date: '2013-09-25'
author: jtdub
tags:
- BGP
- packetgeek.net
---

I had my first real experience with playing with regular expressions in BGP this evening to manipulate traffic. In the instance below, I needed to give a lower preference to traffic that was learned from '65002' and was 4 AS hops out. I did this by creating an as-path access-list, using it in a route-map, and applying it to an eBGP neighbor.

```bash
ip as-path access-list 61 permit ^65002_[0-9]+_[0-9]+_[0-9]+$
route-map SomeBGPTransit-in permit 15
 match as-path 61
 set local-preference 90
end
wr mem
```

While I'm at it, I figured that I share the two links that have helped me the most with BGP. The first is the [BGP cheat sheet](http://media.packetlife.net/media/library/1/BGP.pdf). The second is [BGP Regular Expressions](http://blog.ine.com/2008/01/06/understanding-bgp-regular-expressions/).
