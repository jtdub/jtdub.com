---
layout: post
title: Python with Multiple Threads
date: '2014-11-20'
author: jtdub
tags:
- Python Tips
- packetgeek.net
---

I have a need to have a script to execute the same task, among many devices, as close to the same time as possible. As a non-programmer, whom happens to write code in an effort to make my job easier, I thought the task would be easier than it actually is. Spawning multiple threads is pretty easy. However, hitting resource limits is a limiting factor - as is how you output your data.

Here is an example of how I'm using BoundedSemaphores, within Python to limit the number of threads that I spawn.

```python
#!/usr/bin/env python

from threading import Thread
from threading import BoundedSemaphore
from os import system
import time

threads = []
max_threads = 1
sema = BoundedSemaphore(value=max_threads)
hosts = ['host1', 'host2', 'host3', 'host4', 'host5', 'host6']

def ping_pong(host, sema):
	ping_pong_host = system('ping -c 100 -t 1 -m 1 %s > /dev/null 2>&1' % host)
	sema.release()
	
	return ping_pong_host
	
if __name__ == '__main__':
	print "Start: %s" % time.time()
	print "Max Threads: %s" % max_threads
	tr = 1
	for host in hosts:
		print "Thread: %s - %s" % (tr, time.time())
		sema.acquire()
		t = Thread(target=ping_pong, args=[host, sema])
		t.start()
		threads.append(t)
		tr += 1
	for t in threads:
		t.join()
	print "End: %s" % time.time()
```

With the 'max_threads' variable set to '1', here is the output:

```
Start: 1416558663.05
Max Threads: 1
Thread: 1 - 1416558663.05
Thread: 2 - 1416558663.05
Thread: 3 - 1416558664.07
Thread: 4 - 1416558665.08
Thread: 5 - 1416558666.1
Thread: 6 - 1416558667.12
End: 1416558669.15
```

With the 'max_threads' variable set to '6', here is the output:

```
Start: 1416558829.13
Max Threads: 6
Thread: 1 - 1416558829.13
Thread: 2 - 1416558829.13
Thread: 3 - 1416558829.13
Thread: 4 - 1416558829.13
Thread: 5 - 1416558829.13
Thread: 6 - 1416558829.13
End: 1416558835.23
```

With the max_threads set to one, it essentially disable's threading - in that it doesn't spawn multiple threads to complete a task. You can see that it took approximately five seconds to spawn all threads and another two seconds to complete the tasks.

With the max_threads set to six, it spawned all threads in less than a millisecond and took approximately six seconds to complete the tasks.
