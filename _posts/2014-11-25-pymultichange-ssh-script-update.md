---
layout: post
title: pyMultiChange - SSH Script Update
date: '2014-11-25'
author: jtdub
tags:
- Cisco Administration Python Scripting
- Software Defined Networking
- Python Tips
- packetgeek.net
---

I updated the ssh-multi.py script from my pyMultiChange repository. It's now fully functional and allows you to enter 'enable' mode on Cisco routers and switches. As I'm using the paramiko library to interact with routers and switches via SSH, I had to switch from using the 'exec_command' API to invoke_shell, send, and recv API's. It took a little more work - and I'm not completely thrilled with how the 'recv' API is implemented in paramiko, but it's what we have to work with for now.

The pyMuliChange repository is available on my [github](https://github.com/jtdub/pyMultiChange).

<img src="/images/Screen-Shot-2014-11-26-at-2.49.55-AM.png"/>
