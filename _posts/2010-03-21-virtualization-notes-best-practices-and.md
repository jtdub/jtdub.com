---
layout: post
title: Virtualization Notes, Best Practices, and Gotcha's
date: '2010-03-21'
author: jtdub
tags:
- Virtualization
- Hyper-V
- VMware
- packetgeek.net
---

I spent last week attending the Virtualization Pro Summit. I came away with a wealth of information that I'm still compiling, wrapping my head around, and figuring out where and how I can implement what. Below are some of the notes that I took away from the conference.

#### General Virtualization

* Memory is the first bottle neck in virtualization.
  * When sizing a server, be sure to use servers that can handle at least 128GB of RAM. It doesn't mean that you will need to purchase a server with 128GB of RAM off the bat. It will allow for proper expansion.
  * If possible, use DDR3 RAM and buy in sticks of three.
  * Balance the memory allocations across the CPU channels.
  * Leave a buffer to the amount of logical RAM allocated to the amount of physical RAM in the server.
* The speed of your hard disk subsystem is probably the second bottleneck that will be encountered.
  * For iSCSI SANs, use multiple load balanced connections to the SAN to get the desired bandwidth.
  * For the best performance, purchase a SAN or DAS that uses newer SAS (serially attached SCSI) hard drives.
  * Fiber Channel over Ethernet (FCoE) will provide the better performance as it doesn't have the overhead of the IP protocol, but for the time being, iSCSI will provide the most bang for the buck.
  * SAS hard drives provide 384MBps throughput.
  * 15K SAS drives will provide the best performance.
  * You can allocate additional RAM for x64 guests for disk caching to compensate for an overloaded hard disk subsystem. This will greatly enhance performance for servers that are hard on disk I/O, such as Exchange, SQL, and Virtual Desktops (VDI).
* Processor Management:
  * Target CPU usage is around 60 - 70%, combined for all guest VMs and the VM host.
  * A four to one ratio of CPU core to guest VM vCPU is a good ratio to start off with after taking other factors into account (RAM, disk I/O, networking, etc). After that you can add or remove VMs as needed.
  * Multi-socket x64 processors provide the best performance.
  * For SMP Applications - vCPU's shouldn't out number the physical CPU's.
* Dynamic VM moves (VMWare vMotion / Microsoft Live Migration)
  * You will need to plan your VM clusters so that not any single VM host is over loaded. If a VM host goes down in a cluster, it will cause a domino effect.
* Network Management:
  * NIC teaming or 10GB Ethernet will provide the best performance for heavy usage.
  * Isolate the console network and protect the VM hosts at all costs.
  * Isolate the cluster heartbeat (vMotion / Live Migration) traffic on a physical separate switch.
  * The console network and cluster heartbeat network can be on the same network if need be.
* BIOS:
  * Enable:
    * Hyper-threading
    * Hardware assisted virtualization
    * Data Execution Prevention
  * Disable:
    * All power save settings
* Host / Guest Capacity Planning:
  * http://www.vkernal.com
  * http://www.teamquest.com/solutions-products/products/model/
* Disk Raid:
  * Raid 5 is a good compromise of performance and fault tollerance.
  * Raid 10 provides the best performance, but is costs more on disk usage.
  * Raid 1 can be used for VM hosts.

#### VMWare vSphere 4.0

* Memory Management:
  * ESX(i) will consolidate identical memory pools. Therefore it's better to  try to run the same types of operating systems and applications on a VM  host.
  * Balloon driver is a function that allows a VM host to dynamically allocate RAM to a guest. If this feature is used, careful planning will be needed as to not over-allocate RAM.
* Disk Provisioning:
  * Thin provisioning is an option, but may thick provisioning will provide better performance.
  * If thin provisioning is used, careful planning will be needed as it allows you to potentially over-allocate available disk space.
* Snapshots:
  * Don't leave snapshots active because you might need them.
  * Try to keep snapshot sizes and the number of them to a minimum.
  * Active snapshots may reduce performance on the VM.
  * Deleting snapshots (especially large ones) and playing them back into a base image reduces performance. Depending on the size, it can take a LONG time.
* General performance:
  * Minimize the number of vSwitches
  * Don't use the ESX(i) console to manage guests.
  * Consider using an iSCSI HBA on older hosts. On newer hosts it may be a detriment to performance. vSphere doesn't support TOE NIC cards.
  * Install VMware-Tools.
