---
layout: post
title: Bash - Random Password Changer
date: '2013-02-22'
author: jtdub
tags:
- Bash Tips
- Pranks
- packetgeek.net
---

Here's a script that will change a user's password at random internals with a randomly generated 30 character password. :)

```bash
#!/bin/sh
while true;
do
    for i in `< /dev/urandom tr -dc A-Za-z0-9_ | head -c30`;
    do
        echo 'someuser:$i' | sudo chpasswd;
        time=`< /dev/urandom tr -dc 0-9 | head -c5`;   
        sleep $time;
    done
done
```
