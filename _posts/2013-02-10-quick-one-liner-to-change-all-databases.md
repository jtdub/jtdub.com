---
layout: post
title: Quick one-liner to change all databases tables to InnoDB in MySQL.
date: '2013-02-10'
author: jtdub
tags:
- Bash Tips
- System Administration
- MySQL
- packetgeek.net
---

I've been attempting to get a better understanding of the operations of MySQL. For me, the best way to do that is hands on. I had a database, with a lot of tables, that I wanted to change the engine type to InnoDB. Obviously, being a lazy sys admin, I didn't want to change them all by hand. So, I made a quick one-liner to do the job for me.

```bash
for i in `mysql somedb -e 'show tables\G' | grep -v ^* | awk '{print $2}'`; do 
    mysql somedb -e "ALTER TABLE $i ENGINE=INNODB"; 
done
```
