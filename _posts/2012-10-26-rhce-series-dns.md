---
layout: post
title: 'RHCE Series: DNS'
date: '2012-10-26'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- DNS
- Bind
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

* Configure a caching-only name server.
* Configure a caching-only name server to forward DNS queries.
* Note: Candidates are not expected to configure master or slave name servers.

Install bind: `yum -y install bind`

Setup caching-only name server with forwarders.

```bash
[root@server1 etc]# cat named.conf
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
 listen-on port 53 { any; }; //listen on any network
 listen-on-v6 port 53 { any; }; //listen on any network
 directory  "/var/named";
 dump-file  "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
 allow-query     { 192.168.1.0/24; }; //define who to allow queries from
 forwarders { 8.8.8.8; }; //add this line to forward queries
 recursion yes;

 dnssec-enable yes;
 dnssec-validation yes;
 dnssec-lookaside auto;

 /* Path to ISC DLV key */
 bindkeys-file "/etc/named.iscdlv.key";

 managed-keys-directory "/var/named/dynamic";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
 type hint;
 file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

Open up the firewall: 

```bash
iptables -I INPUT -p udp --dport 53 -j ACCEPT
service iptables save
```

Start the service and make it persistent at boot:

```bash
service named start
chkconfig named on
```
