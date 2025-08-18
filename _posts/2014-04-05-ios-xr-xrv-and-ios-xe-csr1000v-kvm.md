---
layout: post
title: IOS-XR (XRv) and IOS-XE (CSR1000v) KVM Config Generation
date: '2014-04-05'
author: jtdub
tags:
- Innovative
- Virtualization
- Miscellaneous Hacking
- MySQL
- CCNP SP Study Notes
- training
- IOS-XE
- PHP
- IOS-XR
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

As I'm mostly going to be using XRv and the CSR1000v to create my Service Provider Lab Environment to study for the CCNP Service Provider exams, I thought that I would throw together a quick script so that I can build lab environments quickly. If you've played with XRv or CSR1000v in KVM at all, you know that it's a hassle to generate your topologies. I've made that way easier with the "Virtual Network Lab Config Generator". Note that this doesn't generate device configs, but rather the KVM configuration that you use to spin up and connect your virtual devices. The code is on github.com. It was written hastily, so it's very rough. :)

[Virtual Network Lab Config Generator](https://github.com/jtdub/vnlcg)

Here is a screen shot:

{% include optimized_image.html
   src="https://imagedelivery.net/KfNXtSV3XH0tLyWKv3PbRw/a44fc1e7-5743-4b94-d3f9-d4c37292b400/public"
   alt="Image related to the article content"
   width="320"
   loading="lazy" %}

When used, it can generate complex KVM configs in a matter of minutes, rather than an hour or more. Here is an example:

```bash
# p1
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/p1-xr.raw 
 -serial telnet::8110,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:10 
 -net nic,model=virtio,vlan=10,macaddr=00:01:00:ff:10:10 
 -net socket,vlan=10,listen=127.0.0.1:7010 
 -net nic,model=virtio,vlan=11,macaddr=00:01:00:ff:10:11 
 -net socket,vlan=11,listen=127.0.0.1:7011 
 -net nic,model=virtio,vlan=12,macaddr=00:01:00:ff:10:12 
 -net socket,vlan=12,listen=127.0.0.1:7012 
 -net nic,model=virtio,vlan=13,macaddr=00:01:00:ff:10:13 
 -net socket,vlan=13,listen=127.0.0.1:7013 
 -net nic,model=virtio,vlan=14,macaddr=00:01:00:ff:10:14 
 -net socket,vlan=14,listen=127.0.0.1:7014 
 -net tap,ifname=tap10,vlan=1000,script=no &

# p2
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/p2-xr.raw 
 -serial telnet::8111,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:11 
 -net nic,model=virtio,vlan=10,macaddr=00:01:00:ff:11:10 
 -net socket,vlan=10,connect=127.0.0.1:7010 
 -net nic,model=virtio,vlan=15,macaddr=00:01:00:ff:11:15 
 -net socket,vlan=15,listen=127.0.0.1:7015 
 -net nic,model=virtio,vlan=16,macaddr=00:01:00:ff:11:16 
 -net socket,vlan=16,listen=127.0.0.1:7016 
 -net nic,model=virtio,vlan=17,macaddr=00:01:00:ff:11:17 
 -net socket,vlan=17,listen=127.0.0.1:7017 
 -net nic,model=virtio,vlan=18,macaddr=00:01:00:ff:11:18 
 -net socket,vlan=18,listen=127.0.0.1:7018 
 -net tap,ifname=tap11,vlan=1000,script=no &

# pe1
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/pe1-xr.raw 
 -serial telnet::8112,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:12 
 -net nic,model=virtio,vlan=11,macaddr=00:01:00:ff:12:11 
 -net socket,vlan=11,connect=127.0.0.1:7011 
 -net nic,model=virtio,vlan=15,macaddr=00:01:00:ff:12:15 
 -net socket,vlan=15,connect=127.0.0.1:7015 
 -net nic,model=virtio,vlan=19,macaddr=00:01:00:ff:12:19 
 -net socket,vlan=19,listen=127.0.0.1:7019 
 -net nic,model=virtio,vlan=20,macaddr=00:01:00:ff:12:20 
 -net socket,vlan=20,listen=127.0.0.1:7020 
 -net nic,model=virtio,vlan=27,macaddr=00:01:00:ff:12:27 
 -net socket,vlan=27,listen=127.0.0.1:7027 
 -net tap,ifname=tap12,vlan=1000,script=no &

# pe2
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/pe2-xr.raw 
 -serial telnet::8113,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:13 
 -net nic,model=virtio,vlan=12,macaddr=00:01:00:ff:13:12 
 -net socket,vlan=12,connect=127.0.0.1:7012 
 -net nic,model=virtio,vlan=16,macaddr=00:01:00:ff:13:16 
 -net socket,vlan=16,connect=127.0.0.1:7016 
 -net nic,model=virtio,vlan=21,macaddr=00:01:00:ff:13:21 
 -net socket,vlan=21,listen=127.0.0.1:7021 
 -net nic,model=virtio,vlan=22,macaddr=00:01:00:ff:13:22 
 -net socket,vlan=22,listen=127.0.0.1:7022 
 -net nic,model=virtio,vlan=27,macaddr=00:01:00:ff:13:27 
 -net socket,vlan=27,connect=127.0.0.1:7027 
 -net tap,ifname=tap13,vlan=1000,script=no &

# pe3
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/pe3-xe.raw 
 -serial telnet::8114,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:14 
 -net nic,model=virtio,vlan=13,macaddr=00:01:00:ff:14:13 
 -net socket,vlan=13,connect=127.0.0.1:7013 
 -net nic,model=virtio,vlan=17,macaddr=00:01:00:ff:14:17 
 -net socket,vlan=17,connect=127.0.0.1:7017 
 -net nic,model=virtio,vlan=23,macaddr=00:01:00:ff:14:23 
 -net socket,vlan=23,listen=127.0.0.1:7023 
 -net nic,model=virtio,vlan=24,macaddr=00:01:00:ff:14:24 
 -net socket,vlan=24,listen=127.0.0.1:7024 
 -net tap,ifname=tap14,vlan=1000,script=no &

# pe4
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/pe4-xe.raw 
 -serial telnet::8115,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:15 
 -net nic,model=virtio,vlan=14,macaddr=00:01:00:ff:15:14 
 -net socket,vlan=14,connect=127.0.0.1:7014 
 -net nic,model=virtio,vlan=18,macaddr=00:01:00:ff:15:18 
 -net socket,vlan=18,connect=127.0.0.1:7018 
 -net nic,model=virtio,vlan=25,macaddr=00:01:00:ff:15:25 
 -net socket,vlan=25,listen=127.0.0.1:7025 
 -net nic,model=virtio,vlan=26,macaddr=00:01:00:ff:15:26 
 -net socket,vlan=26,listen=127.0.0.1:7026 
 -net tap,ifname=tap15,vlan=1000,script=no &

# ce1
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/ce1-xe.raw 
 -serial telnet::8116,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:16 
 -net nic,model=virtio,vlan=19,macaddr=00:01:00:ff:16:19 
 -net socket,vlan=19,connect=127.0.0.1:7019 
 -net nic,model=virtio,vlan=21,macaddr=00:01:00:ff:16:21 
 -net socket,vlan=21,connect=127.0.0.1:7021 
 -net tap,ifname=tap16,vlan=1000,script=no &

# ce2
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/ce2-xe.raw 
 -serial telnet::8117,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:17 
 -net nic,model=virtio,vlan=20,macaddr=00:01:00:ff:17:20 
 -net socket,vlan=20,connect=127.0.0.1:7020 
 -net nic,model=virtio,vlan=22,macaddr=00:01:00:ff:17:22 
 -net socket,vlan=22,connect=127.0.0.1:7022 
 -net tap,ifname=tap17,vlan=1000,script=no &

# ce3
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/ce3-xr.raw 
 -serial telnet::8118,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:18 
 -net nic,model=virtio,vlan=23,macaddr=00:01:00:ff:18:23 
 -net socket,vlan=23,connect=127.0.0.1:7023 
 -net nic,model=virtio,vlan=25,macaddr=00:01:00:ff:18:25 
 -net socket,vlan=25,connect=127.0.0.1:7025 
 -net tap,ifname=tap18,vlan=1000,script=no &

# ce4
/bin/qemu-kvm -cpu kvm64 -nographic -m 2548 -hda /var/lib/libvirt/images/ce4-xr.raw 
 -serial telnet::8119,server,nowait 
 -net nic,model=virtio,vlan=1000,macaddr=00:01:00:ff:66:19 
 -net nic,model=virtio,vlan=24,macaddr=00:01:00:ff:19:24 
 -net socket,vlan=24,connect=127.0.0.1:7024 
 -net nic,model=virtio,vlan=26,macaddr=00:01:00:ff:19:26 
 -net socket,vlan=26,connect=127.0.0.1:7026 
 -net tap,ifname=tap19,vlan=1000,script=no &
```

The above configuration was completely generated automatically. Super simple. :)
