---
layout: post
title: IPv4 Subnetting Made Easy
date: '2012-10-29'
author: jtdub
tags:
- Subnetting
- IPv4
- CCNA Study Notes
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

Many people are intimidated by the idea of subnetting a block of IP Addresses. In reality, it's much easier than what it appears and with some practice it can be easily done in a persons head, on the fly.

There are two things that a person needs to know, so that they understand how the process works. Those two things are binary and the powers of two. We use binary and the powers of two to calculate the block size of a subnet, the number of hosts a subnet will have, and the number of subnets that a sub-network can accommodate.

An IP Address of made up of four numbers, separated by a period. Each number represents an octet, which is one byte long. Eight bits make up a byte. Binary is a computer language that has two functions; on or off. The "1" in binary is "on" and the "0" is "off". These binary digits are counted from right to left to determine what an decimal number value is of an octet.

Each byte can have a value of up to 255, starting with zero. Counting in binary goes against logic to those of us who were taught that we read left to right. Counting in binary is done right to left.

As an example,

`00110000`

has a decimal value of 48. Starting at the 0 on the right, you count 1, 2, 4, 8, 16, 32, 64, 128. Or if you want to go backwards (left to right), 128, 64, 32, 16, 8, 4, 2, 1 See what I mean with the powers of two? Now, the only binary digits that you count are the 1's. You take the binary digits and add them together. In this example, binary digits in position 32 and 16 are turned on (1) and the remaining digits are turned off (0). So, add 32 and 16 together to get the value of 48.

Let's write out a subnet mask in binary format.

`11111111.11111111.11111111.11000000`

In this example, the decimal format for the subnet mask is:

255.255.255.192

Now let's  look at the last octet to determine:

1) How we determine the subnet mask
2) 1 bits on, 6 bits off
3) Block size, that is the size of a subnet
4) Number of subnets and hosts.

We determined the subnet mask by looking at the octet that has off (0) bits, which is the last octet.

`.11000000`

Counting the on bits, 128 + 64 = 192.

Now, to determine how many the size of a subnet (block size), we'll use the powers of two and count the off bits.

`.11000000`

*2^6 (or 1,2,4,8,16,32)* The block size in this case is 32.

To determine the number of subnets, you have to use the powers of two and count the on bits.

*2^2 = 4*. So the number of subnets is 4.

Which IPv4 IP Addresses, each subnet has a network address (the first address in a subnet and defines the start position of a network) and a broadcast address (the last address in a subnet and is used for broadcasting in a network). These addresses can not be assigned to computers.

For instance: 192.168.1.0/24, The network address is 192.168.1.0, while the broadcast address is 192.168.1.255. This means that the only addresses that are able to be assigned to computers are 192.168.1.1 - 192.168.1.254. The network address and broadcast address are determined by the subnet mask.

Class A and B networks are subnetted the exact same way. The difference is that you will also utilize the trailing octets in your calculations for the block size and usable number of hosts (computer assignable addresses).

For instance,

`11111111.11111111.11110000.00000000`

The decimal notation for this subnet mask is 255.255.240.0.

It's block size is 4096. The number of subnets available are 16 and the usable hosts per subnet are 4094 addresses.
