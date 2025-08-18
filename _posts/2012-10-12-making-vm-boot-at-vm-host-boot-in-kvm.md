---
layout: post
title: Making a VM boot at VM host boot in KVM
date: '2012-10-12'
author: jtdub
tags:
- Linux
- Virtualization
- KVM
- packetgeek.net
---

<img height="320" src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/ce544fb0-1316-40cc-ee86-1dc66adea600/public"/>

From virt-manager, you can follow the screen shot:

You can also do it from the command line:

```bash
[root@jtdub-workstation ~]# virsh autostart
error: command 'autostart' requires  option
[root@jtdub-workstation ~]# virsh autostart 1
Domain 1 marked as autostarted
```
