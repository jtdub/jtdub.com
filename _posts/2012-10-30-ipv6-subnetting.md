---
layout: post
title: IPv6 Subnetting
date: '2012-10-30'
author: jtdub
tags:
- Subnetting
- IPv6
- packetgeek.net
---

Subnetting IPv6 is just like IPv4, that is it uses the powers of two to determine the subnet mask. IPv6 doesn't use a subnet mask, per say. Instead it uses slash notation. For example /64, /48, etc. The slash notation is known as a prefix.
<br/>
<br/>
IPv6 has 8 x 16 bit, colon (:) separated addresses that are 128 bits in length. In IPv6, if a 16 bit field has leading zeros, the leading zeros are dropped from the address. Also, if a 16 bit field has all zeros, then all the zeros can be dropped from the address and will be represented as with a double colon (::). However, the double colon can only occur once. If there are multiple fields that contain all zeros, then one field can be represented with the double colon (::), while the remaining fields will be represented with a single zero (:0:) Another thing to notice is that IPv6 uses Hexadecimal addresses, rather than plain decimal.
<br/>
<br/>
For instance, the example below has a leading zero in the second 16 bit field.
<br/>
<br/>
2001:
<span style="background-color: yellow;">
 0470
</span>
:1f0f/48
<br/>
<br/>
Another way to write that network out is to drop the leading zero:
<br/>
<br/>
2001:
<span style="background-color: yellow;">
 470
</span>
:1f0f/48
<br/>
<br/>
However, if the last two fields contained all zeros. The second field could be represented with the double colon (::), while the third field could be represented with a single 0.
<br/>
<br/>
2001::0/48
<br/>
<br/>
Easy, right? Now, I know what you're thinking. You're thinking, "James, didn't you say that IPv6 Addresses contained 128 bit addresses? I only see 48 bits."
<br/>
<br/>
You're correct. The difference is the prefix, or slash notation at the end of the address. The address 2001:470:1f0f/48 represents a network and not a complete address. The equivalent, in IPv4, would be 192.168.1.0/24. That also represents a network and could tell a network engineer what the usable IP Address range is. IPv6 isn't different, except we do not have to list out the remaining address space for the host bits. However, we could do that by doing 2001:470:1f0f::0:0:0:0/48, which has a usable host IP Address range of 2001:470:1f0f:0:0:0 - 2001:470:1f0f:ffff:ffff:ffff:ffff.
<br/>
<br/>
Now again, I know what you're thinking. "How many addresses does that represent". The answer is 2^80 or 1.2089258e+24.
<br/>
<br/>
Now consider that the IPv4 address space has approximately 4.3 billion addresses (2^32 = 4,294,967,296). Out of those, only about 250 million addresses are usable. That's because the address space has been broken up into smaller chunks, and as you know, each subnet has a network address and a broadcast address that can be assigned to computers. There is also private address ranges (RFC 1918 - 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16) which can't be routed through the Internet, but only reside on private LAN's and only access the Internet through NAT. There is the 127.0.0.0/8 network used for loop back addresses, Class D networks which is used for multicast, and Class E which is 'experimental' and isn't used. That's a whole lot of wasted address space.
<br/>
<br/>
IPv6 on the other hand is a lot more efficient with address space and there is more address space than any one person will ever need. In fact, every single individual can have an entire Internet worth of address space, in IPv6, and everybody will still have unique addresses. Even better, there will be room to spare. For reference, the IPv6 Address space is 2^128 or 3.4028237e+38. I can't even count that high. :)
<br/>
<br/>
So, enough rambling. How do you subnet the darn things? Simple.
<br/>
<br/>
Let's pretend that your ISP assigns you, 2001:470:1f0f/48. Great! You have more addresses than you'll ever need, but I hope that you're network is layer two only, as that doesn't help you much. :)
<br/>
<br/>
Right now, it's a common practice for your ISP to hand you a /48 prefix, and then you can take that and break it down to /64 prefixes.
<br/>
<br/>
Let's do this.
<br/>
<br/>
2001:470:1f0f:
<span style="background-color: yellow;">
 0
</span>
:0:0:0:0/48
<br/>
<br/>
The /64 prefix would pertain to the fourth 16 bit field, or the first zero, colon separated field in the example above. 48 + 16 = 64, after all. :) Breaking the /48 prefix into multiple /64 prefixes will allot you 65536 networks, each network will provide you with 1.8446744e+19 address. Do you think that you can manage? :)
<br/>
<br/>
Let's list a few of those networks out:
<br/>
<br/>
2001:470:1f0f:0/64
<br/>
2001:470:1f0f:1/64
<br/>
...
<br/>
2001:470:1f0f:ffff/64
<br/>
<br/>
Get the idea? You can also break that out into even smaller networks by going to the next 16 bit field separator, like /80 or /96 or /112
<br/>
<br/>
A /80 prefix, out of a /48 will allot you 4294967296 networks with a total address space of 2.8147498e+14 addresses.
<br/>
<br/>
A /96 prefix, out of a /48 will allot you 2.8147498e+14 networks with a total address space of 4294967296 addresses
<br/>
<br/>
And a /112 prefix, out of a /48 will allot you 1.8446744e+19 networks with a total address space of 65536 addresses.
<br/>
<br/>
Tell me, how could you possibly run out of addresses?
<br/>
<br/>
I hope that you're getting the grasp of this. However, let me try to break this down even further. Let's go back to our taking a/48 prefix and breaking it down int /64 prefixes.
<br/>
<br/>
<span style="background-color: orange;">
 2001:470:1f0f
</span>
:
<span style="background-color: lime;">
 0
</span>
:
<span style="background-color: yellow;">
 0:0:0:0
</span>
<br/>
<br/>
I've broken the above address into three colors. The first color is
<span style="background-color: orange;">
 orange
</span>
and consists of 2001:470:1f0f, the second color is
<span style="background-color: lime;">
 green
</span>
and consists of the first colon separated 0, and the third color is
<span style="background-color: yellow;">
 yellow
</span>
and consists of the remaining colon separated zeros.
<br/>
<br/>
The first section consists of the global prefix. This section of the address space is called a global prefix and is the network space that your ISP provides to you as the /48 prefix. Now, if your ISP provided you with a /64, the global prefix would be 2001:470:1f0f:0 and the same shift would occur for a /80, a /96, and a /112, etc, but we're focused on a /48 prefix.
<br/>
<br/>
The second field, is the subnet. and this number will increment from 0 - ffff (remember hexadecimal numbers instead of binary). This is the field that you will use to define your networks with layer three boundaries. You can compare this to IPv4 networks, like 192.168.0.0/24 and 192.168.1.0/24 are two different networks that are separated by layer three boundaries. To make the networks communicate with each other, you'll need to add a router to the mix.
<br/>
<br/>
Lastly, the remaining address space, in yellow, is dedicated to host addresses. 0:0:0:0 - ffff:ffff:ffff:ffff is the usable host range. IPv6 has a really cool feature, that will most likely replace DHCP (even though there is DHCPv6 for IPv6 networks), called Autoconf. Autoconf allows automatic allocation of IPv6 Addresses and the host portion of the IPv6 address will be your computers mac address. Each mac address is unique to each computer, which is perfect! For example, if my mac address is 123:456:789:0ab, then my IPv6 address via autoconf would be 2001:470:1f0f:0:123:456:789:ab, assuming that my subnet was 0. If you've been around the IT industry long enough to remember IPX/SPX from the novel days, then this should be a familiar concept to you.
<br/>
<br/>
Whoo.... That was a lot of rambling. I'm sure that I'll come back and edit this soon, as I just did this off the top of my head and I'm sure that there are some errors. If you have any questions, please ask and I'll attempt to clarify. :)
