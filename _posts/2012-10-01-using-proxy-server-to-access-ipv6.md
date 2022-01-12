---
layout: post
title: Using a Proxy Server to access the IPv6 Internet?
date: '2012-10-01'
author: jtdub
tags:
- Linux
- System Administration
- Proxy
- Squid
- packetgeek.net
---

I had an idea recently. Could a person use an http proxy server to access the IPv6 portions of the Internet? The answer is, yes.

To test this out, I spun up a cloud server at [Rackspace](http://www.rackspace.com/). Rackspace assigns IPv6 Addresses to their 'Next Generation' Cloud Servers. In this instance, I used Linux and installed squid and httpd-tools.

```bash
[root@proxy ~]# ip addr show dev eth0
2: eth0:  mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether bc:76:4e:04:54:39 brd ff:ff:ff:ff:ff:ff
    inet 198.61.201.31/24 brd 198.61.201.255 scope global eth0
    inet6 2001:4800:780e:510:e026:3332:ff04:5439/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::be76:4eff:fe04:5439/64 scope link 
       valid_lft forever preferred_lft forever
[root@proxy ~]# history | grep yum
    2  yum -y install squid
   28  yum -y --disableexcludes=all update
   58  yum -y install setroubleshoot
   63  yum whatprovides "*/finger"
   87  yum search squid
  124  yum whatprovides "*/htpasswd"
  125  yum install --help
  126  yum deplist httpd_tools
  127  yum install httpd_tools
  128  yum deplist httpd-tools
  129  yum install httpd-tools
  195  history | grep yum
[root@proxy ~]# head -n 50 /etc/squid/squid.conf
#
# Recommended minimum configuration:
#
acl manager proto cache_object
#acl localhost src 127.0.0.1/32 ::1
#acl to_localhost dst 127.0.0.0/8 0.0.0.0/32 ::1

auth_param basic program /usr/lib64/squid/ncsa_auth /etc/squid/passwd
acl sgn proxy_auth REQUIRED
http_access allow sgn
http_access deny all

# Example rule allowing access from your local networks.
# Adapt to list your (internal) IP networks from where browsing
# should be allowed
#acl localnet src 10.0.0.0/8 # RFC1918 possible internal network
#acl localnet src 172.16.0.0/12 # RFC1918 possible internal network
#acl localnet src 192.168.0.0/16 # RFC1918 possible internal network
#acl localnet src fc00::/7       # RFC 4193 local private network range
#acl localnet src fe80::/10      # RFC 4291 link-local (directly plugged) machines

acl SSL_ports port 443
acl Safe_ports port 80  # http
acl Safe_ports port 21  # ftp
acl Safe_ports port 443  # https
acl Safe_ports port 70  # gopher
acl Safe_ports port 210  # wais
acl Safe_ports port 1025-65535 # unregistered ports
acl Safe_ports port 280  # http-mgmt
acl Safe_ports port 488  # gss-http
acl Safe_ports port 591  # filemaker
acl Safe_ports port 777  # multiling http
acl CONNECT method CONNECT

#
# Recommended minimum Access Permission configuration:
#
# Only allow cachemgr access from localhost
#http_access allow manager localhost
#http_access deny manager

# Deny requests to certain unsafe ports
#http_access deny !Safe_ports

# Deny CONNECT to other than secure SSL ports
http_access deny CONNECT !SSL_ports

# We strongly recommend the following be uncommented to protect innocent
# web applications running on the proxy server who think the only
# one who can access services on "localhost" is a local user
[root@proxy ~]# history | grep htpasswd
  124  yum whatprovides "*/htpasswd"
  130  htpasswd 
  131  htpasswd -cm /etc/squid/passwd someuser
  197  history | grep htpasswd
[root@proxy ~]# cat /etc/squid/passwd 
someuser:$apr1$SjAEUZGj$3FhI5utUY/Bp1ARFa4fhDwaDjTjCsE$ClKtuD/
[root@proxy ~]# iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere            state RELATED,ESTABLISHED 
ACCEPT     icmp --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:ssh 
ACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:squid 
REJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited 

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
REJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited 

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination 
```


As you can see, all that I did with squid was set it up to allow connections from authenticated users rather than IP Addresses. This would allow somebody to be mobile and still use the proxy. I then used 'htpasswd' from the httpd-tools package to generate the /etc/squid/passwd file, and finally, I opened up squid on the firewall.

The only other changes would need to be made on your local machine. You would need to use DNS servers that served AAAA records. Googles servers do this. 8.8.8.8 and 8.8.4.4. Your local ISP may serve the AAAA records as well. You can test this with the dig or nslookup command.

```bash
dig aaaa packetgeek.net @ns1.rackspace.com
```

Lastly, you'll need to configure your browser to point to your proxy server. As you can see in the screenshot below. The IP Address from [http://www.whatismyipv6.com/](http://www.whatismyipv6.com/) is listed as the IPv6 Address of my proxy server.

<img height="200" src="/images/Screen+Shot+2012-10-01+at+1.21.14+PM.png"/>
