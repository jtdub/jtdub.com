---
layout: post
title: Bash Shell Enumerator - Command Not Found
date: '2013-02-22'
author: jtdub
tags:
- Bash Tips
- Pranks
- packetgeek.net
---

Make this script run when ever a user logs into their system and watch them freak out as it tells them that all their commands aren't found. :)

```bash
#!/bin/sh

h=`hostname | cut -d . -f 1`;
u=`id -un`;
shell="[$u@$h ~]$";

while true;
do
    echo -n "$shell "; read cmd;
    echo "bash: $cmd: command not found...";
done;
```
