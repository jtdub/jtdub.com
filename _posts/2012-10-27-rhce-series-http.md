---
layout: post
title: 'RHCE Series: HTTP'
date: '2012-10-27'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- Apache
- http
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

* Configure a virtual host.
* Configure private directories.
* Deploy a basic CGI application.
* Configure group-managed content.

Install apache: `yum -y install httpd httpd-manual links`

The httpd-manual is a great resource for information, but isn't needed. The links package is needed for the server-status utilities.

First, let's create our virtual hosts. We'll need to create our DocumentRoot directories.

```bash
[root@server1 ~]# mkdir /var/www/{server1.example.com,vhost.server1.example.com}
[root@server1 ~]# ls /var/www/
cgi-bin  error  html  icons  manual  server1.example.com  vhost.server1.example.com
```

Next, you'll need to edit the /etc/httpd/conf/httpd.conf

```bash
[root@server1 ~]# cd /etc/httpd/conf
[root@server1 conf]# vim httpd.conf 
[root@server1 conf]# tail httpd.conf 
#
NameVirtualHost *:80

 DocumentRoot /var/www/server1.example.com
 ServerName server1.example.com


 DocumentRoot /var/www/vhost.server1.example.com
 ServerName vhost.server1.example.com
```

When you enable virtual hosts in apache, the default website in /var/www/html will not work. You will have to add another virtual host if you want to serve content from that directory. In this configuration, apache will intercept the http headers and look at the destination url and direct traffic based upon that information.

Now that the httpd.conf has been modified, we'll need to restart apache.

```bash
[root@server1 ~]# service httpd restart
Stopping httpd:                                            [  OK  ]
Starting httpd:                                            [  OK  ]
[root@server1 ~]# httpd -S
VirtualHost configuration:
wildcard NameVirtualHosts and _default_ servers:
_default_:8443         server1.example.com (/etc/httpd/conf.d/nss.conf:84)
*:80                   is a NameVirtualHost
         default server server1.example.com (/etc/httpd/conf/httpd.conf:1011)
         port 80 namevhost server1.example.com (/etc/httpd/conf/httpd.conf:1011)
         port 80 namevhost vhost.server1.example.com (/etc/httpd/conf/httpd.conf:1015)
Syntax OK
[root@server1 ~]# apachectl status
                                   Not Found

   The requested URL /server-status was not found on this server.

     ----------------------------------------------------------------------

    Apache/2.2.15 (CentOS) Server at localhost Port 80
```

You'll notice that you can use the 'httpd -S' command to show the virtual hosts residing on the server. Let's create some content to view in the virtual hosts.

```bash
[root@server1 ~]# echo "server1.example.com" > /var/www/server1.example.com/index.htm
[root@server1 ~]# echo "vhost.server1.example.com" > /var/www/vhost.server1.example.com/index.htm
```

Now, let's try to view the content.

```bash
[root@server1 ~]# ping -c 1 server1.example.com
PING server1.example.com (192.168.1.1) 56(84) bytes of data.
64 bytes from server1.example.com (192.168.1.1): icmp_seq=1 ttl=64 time=0.042 ms

--- server1.example.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.042/0.042/0.042/0.000 ms
[root@server1 ~]# ping -c 1 vhost.server1.example.com
PING server1.example.com (192.168.1.1) 56(84) bytes of data.
64 bytes from server1.example.com (192.168.1.1): icmp_seq=1 ttl=64 time=0.028 ms

--- server1.example.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.028/0.028/0.028/0.000 ms
[root@server1 ~]# curl -I server1.example.com
HTTP/1.1 403 Forbidden
Date: Sun, 28 Oct 2012 02:54:16 GMT
Server: Apache/2.2.15 (CentOS)
Accept-Ranges: bytes
Content-Length: 5039
Connection: close
Content-Type: text/html; charset=UTF-8

[root@server1 ~]# curl -I vhost.server1.example.com
HTTP/1.1 403 Forbidden
Date: Sun, 28 Oct 2012 02:54:24 GMT
Server: Apache/2.2.15 (CentOS)
Accept-Ranges: bytes
Content-Length: 5039
Connection: close
Content-Type: text/html; charset=UTF-8
```

A quick peak at the error_log shows why we can't view the page(s).

```bash
[root@server1 ~]# tail -f /var/log/httpd/error_log 
[Sat Oct 27 21:48:58 2012] [notice] SELinux policy enabled; httpd running as context unconfined_u:system_r:httpd_t:s0
[Sat Oct 27 21:48:58 2012] [notice] suEXEC mechanism enabled (wrapper: /usr/sbin/suexec)
[Sat Oct 27 21:48:58 2012] [notice] Digest: generating secret for digest authentication ...
[Sat Oct 27 21:48:58 2012] [notice] Digest: done
[Sat Oct 27 21:48:59 2012] [notice] Apache/2.2.15 (Unix) DAV/2 mod_nss/2.2.15 NSS/3.13.1.0 Basic ECC configured -- resuming normal operations
[Sat Oct 27 21:49:06 2012] [error] [client 127.0.0.1] File does not exist: /var/www/server1.example.com/server-status
[Sat Oct 27 21:54:16 2012] [error] [client 192.168.1.1] Directory index forbidden by Options directive: /var/www/server1.example.com/
[Sat Oct 27 21:54:24 2012] [error] [client 192.168.1.1] Directory index forbidden by Options directive: /var/www/vhost.server1.example.com/
[Sat Oct 27 21:54:56 2012] [error] [client 192.168.1.1] Directory index forbidden by Options directive: /var/www/server1.example.com/
[Sat Oct 27 21:55:06 2012] [error] [client 192.168.1.1] Directory index forbidden by Options directive: /var/www/vhost.server1.example.com/
```

Notice, that I labeled the index files index.htm. Be default, index.html and index.html.var are the default index pages AND apache, by default, doesn't print a directory listing as a default index page if a index.html or index.html.var page doesn't exist. So, to fix this, I had to add index.htm to the "DirectoryIndex" directive in the httpd.conf

```bash
#
# DirectoryIndex: sets the file that Apache will serve if a directory
# is requested.
#
# The index.html.var file (a type-map) is used to deliver content-
# negotiated documents.  The MultiViews Option can be used for the 
# same purpose, but it is much slower.
#
DirectoryIndex index.html index.html.var index.htm
```

Now, let's try this again.

```bash
[root@server1 ~]# vim /etc/httpd/conf/httpd.conf 
[root@server1 ~]# service httpd restart
Stopping httpd:                                            [  OK  ]
Starting httpd:                                            [  OK  ]
[root@server1 ~]# 
[root@server1 ~]# 
[root@server1 ~]# curl -I server1.example.com
HTTP/1.1 200 OK
Date: Sun, 28 Oct 2012 03:05:43 GMT
Server: Apache/2.2.15 (CentOS)
Last-Modified: Sun, 28 Oct 2012 02:52:13 GMT
ETag: "4d12-14-4cd15a3d274c1"
Accept-Ranges: bytes
Content-Length: 20
Connection: close
Content-Type: text/html; charset=UTF-8

[root@server1 ~]# curl -I vhost.server1.example.com
HTTP/1.1 200 OK
Date: Sun, 28 Oct 2012 03:05:54 GMT
Server: Apache/2.2.15 (CentOS)
Last-Modified: Sun, 28 Oct 2012 02:52:26 GMT
ETag: "4d32-1a-4cd15a49dd342"
Accept-Ranges: bytes
Content-Length: 26
Connection: close
Content-Type: text/html; charset=UTF-8

[root@server1 ~]# curl vhost.server1.example.com
vhost.server1.example.com
[root@server1 ~]# curl server1.example.com
server1.example.com
[root@server1 ~]# ls -Z /var/www/
drwxr-xr-x. root root system_u:object_r:httpd_sys_script_exec_t:s0 cgi-bin
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 error
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 html
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 icons
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 manual
drwxr-xr-x. root root unconfined_u:object_r:httpd_sys_content_t:s0 server1.example.com
drwxr-xr-x. root root unconfined_u:object_r:httpd_sys_content_t:s0 vhost.server1.example.com
[root@server1 ~]# ls -Z /var/www/*example.com/
/var/www/server1.example.com/:
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 index.htm

/var/www/vhost.server1.example.com/:
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 index.htm
```

Now, the sites are working. So, let's go on to the next objective of configuring private directories.

We'll set up vhost.server1.example.com to create a private directory with.

```bash
[root@server1 ~]# htpasswd -cm /var/www/vhost.server1.example.com/.htpasswd james
New password: 
Re-type new password: 
Adding password for user james
[root@server1 ~]# cat /var/www/vhost.server1.example.com/.htpasswd 
james:$apr1$dTUr3R1T$l77COVCwfP0ZKoF05Vq081
[root@server1 ~]# vim /etc/httpd/conf/httpd.conf 
[root@server1 ~]# tail -6 /etc/httpd/conf/httpd.conf 

 AuthType Basic
 AuthName "Private"
 AuthUserFile /var/www/vhost.server1.example.com/.htpasswd
 Require valid-user

[root@server1 ~]# service httpd restart
Stopping httpd:                                            [  OK  ]
Starting httpd:                                            [  OK  ]
[root@server1 ~]# curl -I vhost.server1.example.com
HTTP/1.1 401 Authorization Required
Date: Sun, 28 Oct 2012 03:42:59 GMT
Server: Apache/2.2.15 (CentOS)
WWW-Authenticate: Basic realm="Private"
Connection: close
Content-Type: text/html; charset=iso-8859-1

[root@server1 ~]# curl --user james:testuser vhost.server1.example.com
vhost.server1.example.com
```

Now, let's go ahead and set up group managed content, then we'll deploy a cgi application.

```bash
[root@server1 ~]# echo "sysadmin: james user1 user2" > /var/www/vhost.server1.example.com/.htgroup 
[root@server1 ~]# cat /var/www/vhost.server1.example.com/.htgroup 
sysadmin: james user1 user2
[root@server1 ~]# vim /etc/httpd/conf/httpd.conf 
[root@server1 ~]# tail -7 /etc/httpd/conf/httpd.conf 

 AuthType Basic
 AuthName "Private"
 AuthUserFile /var/www/vhost.server1.example.com/.htpasswd
 AuthGroupFile /var/www/vhost.server1.example.com/.htgroup
 Require group sysadmin

[root@server1 ~]# service httpd restart
Stopping httpd:                                            [  OK  ]
Starting httpd:                                            [  OK  ]
[root@server1 ~]# curl -I vhost.server1.example.com
HTTP/1.1 401 Authorization Required
Date: Sun, 28 Oct 2012 03:49:50 GMT
Server: Apache/2.2.15 (CentOS)
WWW-Authenticate: Basic realm="Private"
Connection: close
Content-Type: text/html; charset=iso-8859-1

[root@server1 ~]# curl --user james:testuser vhost.server1.example.com
vhost.server1.example.com
```

This time, the user 'james' was allowed because the user was in the 'sysadmin' group. Now the cgi application.

```bash
[root@server1 ~]# vim /var/www/cgi-bin/hello.cgi
[root@server1 ~]# chmod +x /var/www/cgi-bin/hello.cgi 
[root@server1 ~]# cat /var/www/cgi-bin/hello.cgi 
#!/usr/bin/perl

print "Content-type: text/html\r\n\n";

print "Hello!\n";
[root@server1 ~]# curl -I server1.example.com/cgi-bin/hello.cgi
HTTP/1.1 200 OK
Date: Sun, 28 Oct 2012 04:01:36 GMT
Server: Apache/2.2.15 (CentOS)
Connection: close
Content-Type: text/html; charset=UTF-8

[root@server1 ~]# curl server1.example.com/cgi-bin/hello.cgi
Hello!
```

The last and final objective, though not on the RHCE offical list, it's a useful tool for working with httpd servers. Setting up the server-status tool.

First, you'll need to edit the httpd.conf.

```bash
#
# Allow server status reports generated by mod_status,
# with the URL of http://servername/server-status
# Change the ".example.com" to match your domain to enable.
#
ExtendedStatus On

    SetHandler server-status
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1 

[root@server1 ~]# service httpd restart
Stopping httpd:                                            [  OK  ]
Starting httpd:                                            [  OK  ]
[root@server1 ~]# apachectl fullstatus
                       Apache Server Status for localhost

   Server Version: Apache/2.2.15 (Unix) DAV/2 mod_nss/2.2.15 NSS/3.13.1.0
   Basic ECC

   Server Built: Feb 13 2012 22:31:42

     ----------------------------------------------------------------------

   Current Time: Saturday, 27-Oct-2012 23:07:09 CDT

   Restart Time: Saturday, 27-Oct-2012 23:06:51 CDT

   Parent Server Generation: 0

   Server uptime: 18 seconds

   Total accesses: 1 - Total Traffic: 2 kB

   CPU Usage: u.08 s.01 cu0 cs0 - .5% CPU load

   .0556 requests/sec - 113 B/second - 2048 B/request

   1 requests currently being processed, 7 idle workers

 __W_____........................................................
 ................................................................
 ................................................................
 ................................................................

   Scoreboard Key:
   "_" Waiting for Connection, "S" Starting up, "R" Reading Request,
   "W" Sending Reply, "K" Keepalive (read), "D" DNS Lookup,
   "C" Closing connection, "L" Logging, "G" Gracefully finishing,
   "I" Idle cleanup of worker, "." Open slot with no current process

Srv PID   Acc  M CPU  SS Req Conn Child Slot  Client          VHost           Request     
                                                                           GET            
0-0 3474 0/1/1 _ 0.09 4  5   0.0  0.00  0.00 127.0.0.1 server1.example.com /server-status 
                                                                           HTTP/1.1       
                                                                           GET            
2-0 3476 0/0/0 W 0.00 0  0   0.0  0.00  0.00 127.0.0.1 server1.example.com /server-status 
                                                                           HTTP/1.1       

     ----------------------------------------------------------------------

    Srv  Child Server number - generation                            
    PID  OS process ID                                               
    Acc  Number of accesses this connection / this child / this slot 
     M   Mode of operation                                           
    CPU  CPU usage, number of seconds                                
    SS   Seconds since beginning of most recent request              
    Req  Milliseconds required to process most recent request        
   Conn  Kilobytes transferred this connection                       
   Child Megabytes transferred this child                            
   Slot  Total megabytes transferred this slot                       

     ----------------------------------------------------------------------

    Apache/2.2.15 (CentOS) Server at localhost Port 80
```

<br/>

You can use `apachectl status|fullstatus` to get real time statistics of the web server utilization.
