---
layout: post
title: 'RHCE Series: SMTP'
date: '2012-10-27'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- Sendmail
- SMTP
- Postfix
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

* Configure a mail transfer agent (MTA) to accept inbound email from other systems.
* Configure an MTA to forward (relay) email through a smart host.

```bash
[root@server1 postfix]# vim /etc/postfix/main.cf
[root@server1 postfix]# service postfix restart
Shutting down postfix:                                     [  OK  ]
Starting postfix:                                          [  OK  ]
[root@server1 postfix]# egrep 'myhostname|mydomain|inet_interfaces|mydestination' /etc/postfix/main.cf 
myhostname = server1.example.com
mydomain = example.com
inet_interfaces = localhost, $myhostname 
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
```

Now that postfix is setup, let's send mail.

```bash
[root@client1 ~]# mail root@example.com
Subject: test
Hello. This is a test.
.
EOT
```

Now to check the logs on the mail server and check the message.

```bash
Oct 28 00:33:19 server1 postfix/smtpd[4556]: connect from client1.example.com[192.168.1.11]
Oct 28 00:33:19 server1 postfix/smtpd[4556]: A312D4D42: client=client1.example.com[192.168.1.11]
Oct 28 00:33:19 server1 postfix/cleanup[4559]: A312D4D42: message-id=<20121028053319 .81b8f3fccc=".81b8f3fccc" client1.example.com="client1.example.com">
Oct 28 00:33:19 server1 postfix/qmgr[4554]: A312D4D42: from=, size=649, nrcpt=1 (queue active)
Oct 28 00:33:19 server1 postfix/smtpd[4556]: disconnect from client1.example.com[192.168.1.11]
Oct 28 00:33:20 server1 postfix/local[4560]: A312D4D42: to=, relay=local, delay=0.59, delays=0.24/0.22/0/0.14, dsn=2.0.0, status=sent (delivered to mailbox)
Oct 28 00:33:20 server1 postfix/qmgr[4554]: A312D4D42: removed


[root@server1 postfix]# mail
Heirloom Mail version 12.4 7/29/08.  Type ? for help.
"/var/spool/mail/root": 1 message 1 new
>N  1 root                  Sun Oct 28 00:33  21/793   "test"
& 1
Message  1:
From root@client1.example.com  Sun Oct 28 00:33:20 2012
Return-Path: 
X-Original-To: root@example.com
Delivered-To: root@example.com
Date: Sun, 28 Oct 2012 00:33:19 -0500
To: root@example.com
Subject: test
User-Agent: Heirloom mailx 12.4 7/29/08
Content-Type: text/plain; charset=us-ascii
From: root@client1.example.com (root)
Status: R

Hello. This is a test.
```

Now, let's set up a mail relay to forward mail to client1.example.com

We need to add an entry called `relayhost` to `/etc/postfix/main.cf` on server1.example.com. Then restart postfix.

```bash
relayhost = client1.example.com</pre>




[root@server1 ~]# mail root@example.com
Subject: test 
this is a test.
.
EOT
[root@server1 ~]# tail -f /var/log/maillog 
Oct 28 00:45:37 server1 postfix/postfix-script[4797]: starting the Postfix mail system
Oct 28 00:45:37 server1 postfix/master[4798]: daemon started -- version 2.6.6, configuration /etc/postfix
Oct 28 00:45:37 server1 postfix/qmgr[4801]: 590394D43: from=<>, size=2479, nrcpt=1 (queue active)
Oct 28 00:45:42 server1 postfix/smtp[4803]: 590394D43: to=, relay=client1.example.com[192.168.1.11]:25, delay=856, delays=851/0.03/5/0.08, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 5B1293FCCD)
Oct 28 00:45:42 server1 postfix/qmgr[4801]: 590394D43: removed
Oct 28 00:45:57 server1 postfix/pickup[4800]: 00CB44D43: uid=0 from=
Oct 28 00:45:57 server1 postfix/cleanup[4809]: 00CB44D43: message-id=<20121028054557 .00cb44d43=".00cb44d43" server1.example.com="server1.example.com">
Oct 28 00:45:57 server1 postfix/qmgr[4801]: 00CB44D43: from=, size=444, nrcpt=1 (queue active)
Oct 28 00:45:57 server1 postfix/smtp[4803]: 00CB44D43: to=, relay=client1.example.com[192.168.1.11]:25, delay=0.26, delays=0.21/0/0/0.04, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 1B9B43FCCD)
Oct 28 00:45:57 server1 postfix/qmgr[4801]: 00CB44D43: removed


Oct 28 00:45:57 localhost postfix/smtpd[2980]: connect from unknown[192.168.1.1]
Oct 28 00:45:57 localhost postfix/smtpd[2980]: 1B9B43FCCD: client=unknown[192.168.1.1]
Oct 28 00:45:57 localhost postfix/cleanup[2984]: 1B9B43FCCD: message-id=<20121028054557 .00cb44d43=".00cb44d43" server1.example.com="server1.example.com">
Oct 28 00:45:57 localhost postfix/qmgr[2978]: 1B9B43FCCD: from=, size=628, nrcpt=1 (queue active)
Oct 28 00:45:57 localhost postfix/smtpd[2980]: disconnect from unknown[192.168.1.1]
Oct 28 00:45:57 localhost postfix/local[2985]: 1B9B43FCCD: to=, relay=local, delay=0.07, delays=0.04/0/0/0.03, dsn=2.0.0, status=sent (delivered to mailbox)
Oct 28 00:45:57 localhost postfix/qmgr[2978]: 1B9B43FCCD: removed

[root@client1 postfix]# mail
Heirloom Mail version 12.4 7/29/08.  Type ? for help.
"/var/spool/mail/root": 2 messages 2 new
>N  1 Mail Delivery System  Sun Oct 28 00:45  78/2739  "Undelivered Mail Returned to Sender"
 N  2 root                  Sun Oct 28 00:45  21/772   "test"
& 2
Message  2:
From root@server1.example.com  Sun Oct 28 00:45:57 2012
Return-Path: 
X-Original-To: root@example.com
Delivered-To: root@example.com
Date: Sun, 28 Oct 2012 00:45:56 -0500
To: root@example.com
Subject: test
User-Agent: Heirloom mailx 12.4 7/29/08
Content-Type: text/plain; charset=us-ascii
From: root@server1.example.com (root)
Status: R

this is a test.
```

Be sure to chkconfig postfix to ensure it will be persistent at boot and you'll need to make sure that iptables will allow the smtp traffic as well.
