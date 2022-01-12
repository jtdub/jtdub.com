---
layout: post
title: Filesystem I/O Speeds Benchmarking Perl Script
date: '2013-03-07'
author: jtdub
tags:
- Linux
- Filesystems
- Perl Tips
- packetgeek.net
---

I wrote a quick perl script to test the read and write speeds of a file system in Linux. Below is the contents of the script.

```bash
jtdub@db1 ~]$ cat iobenchmark.pl 
#!/usr/bin/perl

use strict;
use warnings;

my $ioFilePath = "/home/jtdub/iofile";
my $testNumber = "1";
my $ioStatsFile = "/home/jtdub/iostats.txt";
my $testLength = "10";

if(-e $ioStatsFile) {
	`rm -f $ioStatsFile`;
}

while ($testNumber <= $testLength) {
	if(-e $ioFilePath) {
		print "Removing $ioFilePath before starting the test. Test: $testNumber.\n";
		`rm -f $ioFilePath`;
	}
	open(STATS, ">> $ioStatsFile");
		print STATS "-----------------------------------------\n";
		print STATS "\nTesting write speeds. Test: $testNumber.\n\n";
		print STATS `dd if=/dev/zero of=$ioFilePath bs=1M count=500 2>> $ioStatsFile`;
		print STATS "\nTesting read speeds. Test $testNumber.\n\n";
		print STATS `dd if=$ioFilePath of=/dev/zero 2>> $ioStatsFile`;
		print STATS "-----------------------------------------\n\n";
	$testNumber++;		
}
close(STATS);
```
