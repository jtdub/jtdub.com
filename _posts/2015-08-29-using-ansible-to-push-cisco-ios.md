---
layout: post
title: Using Ansible to PUSH Cisco IOS Configurations
date: '2015-08-29'
author: jtdub
tags:
- Cisco Administration Python Scripting
- IOS
- Python Tips
- Network Programmability
- DevOps
- Network DevOps
- Ansible
- IOS-XE
- IOS-XR
- packetgeek.net
---

There are a lot of very good articles on the Internet about how Network Engineers can use Ansible to create standardized network device configurations or use Ansible with existing network vendor API's to make changes to network devices. Some of my favorites can be found on the [Python for Network Engineers](https://pynet.twb-tech.com/blog/) and [Jason Edelman's](http://jedelman.com/) sites.

However, what if you have [older, legacy] network devices or are running on software revisions that don't support the newer vendor API's? What if you need to push a common configuration among a multi-vendor or multi-platform of devices quickly? Pushing configurations quickly is easy with my [pyMultiChange](https://github.com/jtdub/pyMultiChange) tool, but one of its biggest limitations is a multi-[vendor, platform] support - where common configurations may have differing syntax, by [vendor, platform] to accomplish the same task. I have yet to find any blogs on Google that share ideas of this category.

For a while, this led me to believe that it it just wasn't possible, unless you invested the time in developing the appropriate Ansible modules.  However, I had an idea the other day, which proved that it is possible to push configurations to this category of network devices.

Here is my example playbook:

```yaml
---
- hosts: netdevices
  connection: local
  gather_facts: no
  
  tasks:
  - name: Create SNMP Configuration
    template:
      src=templates/snmp-contact.j2
      dest=input/{{ hostname }}.conf
    delegate_to: 127.0.0.1

  - name: Configure SNMP Contact on network device
    command: scripts/netsible.py {{ hostname }} input/{{ hostname }}.conf 
    delegate_to: 127.0.0.1
```

In this playbook, you can see that I call a group of devices call 'netdevices'. The first play is to generate the configuration. In this case, I am modifying the snmp-server contact information. It calls a source template called snmp-contact.j2. Here is what the template looks like:

```jinja2
config t
snmp-server contact {{ contact_name }}
end
copy run start
```

The template calls the 'contact_name' variable and destination of the template is in the input directory and named using the 'hostname' variable.

The hostname variable is called from host_vars. Here is the host_var for a test device, called core1a:

```
hostname: core1a
```

The contact_name variable is called from group_vars/all. Here is what my group_var/all looks like:

```
contact_name: netdude@packetgeek.net
```

The result is a file in the input directory called core1a.conf, with the following configuration:

```
config t
snmp-server contact netdude@packetgeek.net
end
copy run start
```

Once the configuration file has been created, the next play is called. This play is responsible for pushing the configuration to each device. It runs a local script called netsible.py. The script takes two arguments. The first is the hostname of the device to access. The second is the location of the configuration file that was created.

In the background, the script connects to the network device, via SSH, accesses enable mode, reads the configuration file, then executes each command on the router. The script utilizes my netlib library, to make this process simple. Here is the code for the netsible.py script:

```python
#!/usr/bin/env python

from netlib.netlib.user_creds import simple_yaml
from netlib.netlib.conn_type import SSH

from os.path import expanduser
import sys

creds = simple_yaml()
base_dir = expanduser("~/net-ansible")
hostname = sys.argv[1]
command_file = sys.argv[2]
ssh = SSH(hostname, creds['username'], creds['password'])

ssh.connect()
ssh.set_enable(creds['enable'])

with open(base_dir + "/" + command_file) as f:
    for line in f.readlines():
        line = line.strip()
        ssh.command(line)
f.close()

ssh.close()
```

If your device is running on a version of code that doesn't support ssh, it would be easy, with the netlib library, to utilize telnet. All you would have to do is import the Telnet library via:


```
from netlib.netlib.conn_type import Telnet
```

Then replace the ssh variable with the Telnet Library.

```
ssh = Telnet(hostname, creds['username'], creds['password'])
```

In the playbook, the 'delegate_to' call tells Ansible to run the command locally on the Ansible master, rather than Ansible connecting to the remote devices directly.

Here is what it looks like when I run the playbook:

```bash
net-ansible]$ ansible-playbook -i hosts push.yml 

PLAY [netdevices] ************************************************************* 

TASK: [Create SNMP Configuration] ********************************************* 
ok: [darkstar -> 127.0.0.1]
ok: [core1a -> 127.0.0.1]

TASK: [Configure SNMP Contact on network device] ****************************** 
changed: [darkstar -> 127.0.0.1]
changed: [core1a -> 127.0.0.1]

PLAY RECAP ******************************************************************** 
core1a                     : ok=2    changed=1    unreachable=0    failed=0   
darkstar                   : ok=2    changed=1    unreachable=0    failed=0   

net-ansible]$
```

This obviously works, but it does have a couple limitations, currently the playbook is not multi-[vendor, platform] ready. To do this, I would need to specify host_vars that define each device by vendor or platoform.

For example, I could define a variable called 'network_platform' in the host_vars and define each host by platform. I could use the values of IOS, NX-OS, IOS-XR, EOS, or JUN-OS defined as the 'network_platform' in the host_vars. Then when I called my playbooks, it could look like:


```yaml
---
- hosts: netdevices
  connection: local
  gather_facts: no
  
  tasks:
  - name: IOS | Create SNMP Configuration
    template:
      src=templates/ios/snmp-contact.j2
      dest=input/{{ hostname }}.conf
    delegate_to: 127.0.0.1
    when: network_platform == IOS

  - name: NX-OS | Create SNMP Configuration
    template:
      src=templates/nx-os/snmp-contact.j2
      dest=input/{{ hostname }}.conf
    delegate_to: 127.0.0.1
    when: network_platform == NX-OS

  - name: IOS-XR | Create SNMP Configuration
    template:
      src=templates/ios-xr/snmp-contact.j2
      dest=input/{{ hostname }}.conf
    delegate_to: 127.0.0.1
    when: network_platform == IOS-XR

  - name: EOS | Create SNMP Configuration
    template:
      src=templates/eos/snmp-contact.j2
      dest=input/{{ hostname }}.conf
    delegate_to: 127.0.0.1
    when: network_platform == EOS

  - name: JUN-OS | Create SNMP Configuration
    template:
      src=templates/jun-os/snmp-contact.j2
      dest=input/{{ hostname }}.conf
    delegate_to: 127.0.0.1
    when: network_platform == JUN-OS

  - name: Configure SNMP Contact on network device
    command: scripts/netsible.py {{ hostname }} input/{{ hostname }}.conf 
    delegate_to: 127.0.0.1
```

The other limitation that is that the script writes the configuration to the network devices every time that the playbook is ran, regardless of whether it's needed or not. For creating an snmp contact, this isn't a huge deal, with the exception of taking extra CPU cycles. However, what if you ran a playbook that was entirely roll based, and it called a role to define BGP route reflectors. Obviously, this would bounce BGP neighbors every time that you ran the playbook. Basically, it boils down to needing a method of checking whether the configuration is actually needed before the script applies it. This is something that I hope to be able to work on. In the mean time, I hope that you've enjoyed this. If you have any ideas, please feel free to share them with me!

I have a generic Github repository that I've been using to play with [Ansible Network Engineering](https://github.com/jtdub/net-ansible) functionality. Feel free to play with it and contribute to it! Note that '[netlib](https://github.com/jtdub/netlib)' is called as a submodule. :) Enjoy!
