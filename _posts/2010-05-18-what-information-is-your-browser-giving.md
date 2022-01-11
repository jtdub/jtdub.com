---
layout: post
title: What information is your browser giving away?
date: '2010-05-18'
author: jtdub
tags:
- Perl Tips
- Online Privacy
- packetgeek.net
---

This morning, there was an article where the EFF is claiming that just because you turn off cookies and javascript in your browser doesn't mean that you're not giving away information. Unfortunately, they are very correct. Your browser will give away ALL kinds of information about your computer; such as operating system, browser type / version number, browser plugin's, etc.

I've used this exact same information for years to gain information about visitors on a site that I couldn't physically monitor the logs. What I did was use a CGI script, written in perl, to modify the HTTP header to point to an transparent image that was 1 pixel high and wide. It's very easy to hide an image when it's transparent and only a single pixel.

The information that this script grabbed were IP Address, date / time the image was accessed, browser user agent, and the referring URL. That's enough information for me to get an idea of what content people are looking at and to even identify unique and repeat users.

Here is a sample script that I've used before.

```perl
#!/usr/bin/perl -w

use DBI;

my $imgurl = "http://www.domain.com/mytracker/images/1by1.gif";

print "Cache-control: no-cache\n";
print "Content-type: image/gif\n";
print "Location: $imgurl\n\n";

$refer = "$ENV{HTTP_REFERER}";
$ipaddr = "$ENV{REMOTE_ADDR}";
$browser = "$ENV{HTTP_USER_AGENT}";

my $dbh = DBI->connect("DBI:mysql:database=mytracker;host=localhost", "username", "password", {'RaiseError' => 1});

my $rows = $dbh->do("INSERT INTO trackerlogs (id, date, referurl, ipaddress, useragent) VALUES ('', NOW(), '$refer', '$ipaddr', '$browser')");
```

Here's an example of the information that the log generates:

<table border="1" cellpadding="1" cellspacing="1">
 <tr>
  <td>
   2009-10-11 19:54:06
  </td>
  <td>
   127.0.0.1
  </td>
  <td>
   http://www.domain.com/referringurl.htm
  </td>
  <td>
   Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; FunWebProducts; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618; AskTB5.3)
  </td>
 </tr>
</table>

Here's a link to the article:
[EFF Browser Fingerprints Article](http://www.theregister.co.uk/2010/05/17/browser_fingerprint/)
