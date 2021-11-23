---
layout: post
title: Rackspace Performance vs Standard Cloud Server Disk I/O
date: '2013-11-22'
author: jtdub
tags:
- Filesystems
- Rackspace
- packetgeek.net
---

I just spun up a Rackspace High Performance Cloud Server and ran some i/o benchmarks on it and compared it to one of my standard cloud servers. Here are my findings.
<br/>
<br/>
This is the script that I ran to gather I/O stats:
<br/>
<br/>
<br/>
<pre class="lang:default decode:true">#!/usr/bin/perl<br/><br/>use strict;<br/>use warnings;<br/><br/>my $ioFilePath = "/root/iofile";<br/>my $testNumber = "1";<br/>my $ioStatsFile = "/root/iostats.txt";<br/>my $testLength = "10";<br/><br/>if(-e $ioStatsFile) {<br/>    `rm -f $ioStatsFile`;<br/>}<br/><br/>while ($testNumber &lt;= $testLength) {<br/>    if(-e $ioFilePath) {<br/>        print "Removing $ioFilePath before starting the test. Test: $testNumber.\n";<br/>        `rm -f $ioFilePath`;<br/>    }<br/>    open(STATS, "&gt;&gt; $ioStatsFile");<br/>        print STATS "-----------------------------------------\n";<br/>        print STATS "\nTesting write speeds. Test: $testNumber.\n\n";<br/>        print STATS `dd if=/dev/zero of=$ioFilePath bs=1M count=2048 2&gt;&gt; $ioStatsFile`;<br/>        print STATS "\nTesting read speeds. Test $testNumber.\n\n";<br/>        print STATS `dd if=$ioFilePath of=/dev/zero 2&gt;&gt; $ioStatsFile`;<br/>        print STATS "-----------------------------------------\n\n";<br/>    $testNumber++;        <br/>}<br/>close(STATS);<br/></pre>
<br/>
<br/>
As you can see, it's a simple test that writes 2GB of 0's to a file, turns around and reads it, then runs the test nine more times.
<br/>
<br/>
First, here are the stats from my standard cloud server:
<br/>
<br/>
<br/>
<pre class="lang:default decode:true">-----------------------------------------<br/><br/>Testing write speeds. Test: 1.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 22.2371 s, 96.6 MB/s<br/><br/>Testing read speeds. Test 1.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 25.4539 s, 84.4 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 2.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 20.1222 s, 107 MB/s<br/><br/>Testing read speeds. Test 2.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 23.5922 s, 91.0 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 3.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 16.7066 s, 129 MB/s<br/><br/>Testing read speeds. Test 3.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 22.2455 s, 96.5 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 4.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 16.0221 s, 134 MB/s<br/><br/>Testing read speeds. Test 4.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 22.5168 s, 95.4 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 5.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 15.4431 s, 139 MB/s<br/><br/>Testing read speeds. Test 5.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 22.5327 s, 95.3 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 6.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 15.9895 s, 134 MB/s<br/><br/>Testing read speeds. Test 6.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 23.5538 s, 91.2 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 7.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 15.9522 s, 135 MB/s<br/><br/>Testing read speeds. Test 7.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 23.3412 s, 92.0 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 8.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 16.306 s, 132 MB/s<br/><br/>Testing read speeds. Test 8.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 22.0596 s, 97.3 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 9.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 15.1251 s, 142 MB/s<br/><br/>Testing read speeds. Test 9.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 22.169 s, 96.9 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 10.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 16.9925 s, 126 MB/s<br/><br/>Testing read speeds. Test 10.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 22.6342 s, 94.9 MB/s<br/>-----------------------------------------</pre>
<br/>
<br/>
Average Write Speed: 127.46 MB/s
<br/>
Average Read Speed: 93.49 MB/s
<br/>
<br/>
Now here are the results from the High Performance Server:
<br/>
<br/>
<br/>
<pre class="lang:default decode:true">-----------------------------------------<br/><br/>Testing write speeds. Test: 1.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 6.65244 s, 323 MB/s<br/><br/>Testing read speeds. Test 1.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 12.4408 s, 173 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 2.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 8.77157 s, 245 MB/s<br/><br/>Testing read speeds. Test 2.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 11.7669 s, 183 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 3.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.14636 s, 518 MB/s<br/><br/>Testing read speeds. Test 3.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 12.9577 s, 166 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 4.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.13664 s, 519 MB/s<br/><br/>Testing read speeds. Test 4.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 11.2337 s, 191 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 5.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.22346 s, 508 MB/s<br/><br/>Testing read speeds. Test 5.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 12.9633 s, 166 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 6.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.12969 s, 520 MB/s<br/><br/>Testing read speeds. Test 6.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 12.8751 s, 167 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 7.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.2136 s, 510 MB/s<br/><br/>Testing read speeds. Test 7.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 12.1281 s, 177 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 8.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.20004 s, 511 MB/s<br/><br/>Testing read speeds. Test 8.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 12.2221 s, 176 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 9.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.20901 s, 510 MB/s<br/><br/>Testing read speeds. Test 9.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 13.1822 s, 163 MB/s<br/>-----------------------------------------<br/><br/>-----------------------------------------<br/><br/>Testing write speeds. Test: 10.<br/><br/>2048+0 records in<br/>2048+0 records out<br/>2147483648 bytes (2.1 GB) copied, 4.17714 s, 514 MB/s<br/><br/>Testing read speeds. Test 10.<br/><br/>4194304+0 records in<br/>4194304+0 records out<br/>2147483648 bytes (2.1 GB) copied, 11.1146 s, 193 MB/s<br/>-----------------------------------------</pre>
<br/>
<br/>
Average Write Speed: 467.8 MB/s
<br/>
Average Read Speed: 175.5 MB/s
<br/>
<br/>
<br/>
<pre class="lang:default decode:true">(467.8 - 127.46) / 127.46 = 2.67<br/>(175.5 - 93.49) / 93.49 = .877</pre>
<br/>
<br/>
<br/>
As you can see, given my simple test, High Performance Cloud Servers have a write speed that is 267% faster and a read speed that is 88% faster than the standard Cloud Servers from Rackspace. Pretty interesting!
