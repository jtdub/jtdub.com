---
layout: post
title: Think that you have a compromised Red Hat based system?
date: '2012-10-12'
author: jtdub
tags:
- Linux
- Security
- RPM
- packetgeek.net
---

Use RPM to search for modified binaries.

`rpm -Va | grep ^..5`

This one-liner will use the RPM database to compare md5sums of all installed files and will give you a report of all files that have been changed from the default install. Configuration files may not be a big deal, but binaries with md5sums that don't match is a dead give away of a compromised system.
