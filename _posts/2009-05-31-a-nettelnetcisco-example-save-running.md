---
layout: post
title: A Net::Telnet::Cisco Example (Save Running Configuration)
date: '2009-05-31'
author: jtdub
tags:
- Cisco Administration Perl Scripting
- Perl Tips
- packetgeek.net
---

This is a simple perl script that uses the `Net::Telnet::Cisco` perl module to save the running configuration on a Cisco IOS router or switch. It could be modified to be automated very easily.

```perl
#!/usr/bin/perl

$confDir = '/home/james/cisco_configs';
$user  = "changeme";
$pass  = "changeme";
$enable  = "changeme";

use Time::localtime;
use Net::Telnet::Cisco;

$tm = localtime;
($hour,$min,$day,$month,$year) = ($tm->hour,$tm->min,$tm->mday,$tm->mon,$tm->year);
$month += 1;
$year += 1900;

if($ARGV[0]) {
 $ip = $ARGV[0];
 my $session = Net::Telnet::Cisco->new(Host => "$ip");
 $session->login("$user", "$pass");
 $session->enable("$enable");
 my @output = $session->cmd("show configuration");
 open(CONFIG, ">>$confDir/$ip-$month$day$year-$hour$min.txt") 
                or die "Can't open $confDir/$ip-$month$day$year-$hour$min.txt\n";
  print CONFIG @output;
 close(CONFIG);
 $session->close;
 print "\n$ip has been backed up successfully.\n";
} else {
        print "Error: You must specify an IP Address to connect to.\n";
        print "$0 \n";
}
```
