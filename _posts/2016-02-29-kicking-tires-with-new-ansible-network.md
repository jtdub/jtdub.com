---
layout: post
title: Kicking the tires with the new Ansible Network Modules
date: '2016-02-29'
author: jtdub
tags:
- Python Tips
- Network Programmability
- DevOps
- Network DevOps
- Ansible
- packetgeek.net
---

Ansible [recently announced](http://www.redhat.com/en/about/press-releases/red-hat-brings-devops-network-new-ansible-capabilities) support for multi-vendor network modules, natively within Ansible. There are many examples on the Internet where individuals have taken the initiative to create their own modules to work with their favorite vendor. Some of these examples are Arista [supplied modules](https://github.com/arista-eosplus/ansible-eos), [NX-OS modules](https://github.com/jedelman8/nxos-ansible) created by Jason Edelman, [NTC](https://github.com/networktocode/ntc-ansible), and [NAPALM](https://github.com/napalm-automation/napalm-ansible). While these are all good, it's nice to see that Ansible is taking some initiative to create some native functionality.

These modules aren't yet in the stable release of Ansible, but they do make an appearance in the development version, so I decided to kick the tires a bit.

First thing I did was set up an development environment using python's virtualenv.

```bash
mkdir -p ansible2.0/env
cd ansible2.0
virtualenv env
source env/bin/activate
git clone git@github.com:ansible/ansible.git
cd ansible
git submodule init
git submodule update
python setup.py install
```

Next, I verified the version of Ansible that I'm running in my development environment, as well as verifying that I have the new modules available to me.

```bash
(env)jtdub-macbook:ansible jtdub$ ansible --version
ansible 2.1.0
  config file = 
  configured module search path = Default w/o overrides
(env)jtdub-macbook:ansible jtdub$ ansible-doc --list | egrep ^'ios|eos|junos|nxos'
eos_command                     Run arbitrary command on EOS device                                                                    
eos_config                      Manage Arista EOS configuration sections                                                               
eos_eapi                        Manage and configure EAPI. Requires EOS v4.12 or greater.                                              
eos_template                    Manage Arista EOS device configurations                                                                
ios_command                     Run arbitrary commands on ios devices.                                                                 
ios_config                      Manage Cisco IOS configuration sections                                                                
ios_template                    Manage Cisco IOS device configurations over SSH                                                        
iosxr_command                   Run arbitrary commands on ios devices.                                                                 
iosxr_config                    Manage Cisco IOS XR configuration sections                                                             
iosxr_template                  Manage Cisco IOS device configurations over SSH                                                        
junos_command                   Execute arbitrary commands on Juniper JUNOS devices                                                    
junos_config                    Manage Juniper JUNOS configuration sections                                                            
junos_template                  Manage Juniper JUNOS device configurations                                                             
nxos_command                    Run arbitrary command on Cisco NXOS devices                                                            
nxos_config                     Manage Cisco NXOS configuration sections                                                               
nxos_nxapi                      Manage NXAPI configuration on an NXOS device.                                                          
nxos_template                   Manage Cisco NXOS device configurations
```

At the time of this writing. It looks like the [online documentation](http://docs.ansible.com/ansible/list_of_network_modules.html) has been updated, which would infer that the new modules may soon be in the stable release.

So, let's create a sample playbook!

The first thing I did was create an inventory file. I kept it simple and created a file called 'hosts'

```
[ios]
edge1
aggr1a
```

Then I created a secrets.yaml file to store my credentials without having to put them in a playbook. While I won't share my credentials here, I will share the format that I used. :)

```yaml
---
creds:
  username: cisco
  password: cisco
  auth_pass: cisco
```

Lastly, I created a sample playbook. I wanted a task that  utilized each module type - (ios|eos|junos|nxos)_(command|template|config). Currently, I have easy access to a couple of IOS devices, so I stuck with using those modules, but I played with each ios_(command|config) module. I plan on spending time and playing with the ios_template module more at a later time.

Here is my sample playbook:

```yaml
---
- hosts: ios
  gather_facts: no
  connection: local

  tasks:
  - name: OBTAIN LOGIN CREDENTIALS
    include_vars: secrets.yaml

  - name: DEFINE PROVIDER
    set_fact:
      provider:
        host: "{{ inventory_hostname }}"
        username: "{{ creds['username'] }}"
        password: "{{ creds['password'] }}"
        auth_pass: "{{ creds['auth_pass'] }}"

  - name: RUN 'SHOW VERSION'
    ios_command:
      provider: "{{ provider }}"
      commands:
        - show version
    register: version

  - debug: var=version.stdout_lines

  - name: RUN 'SHOW ACCESS-LIST TEST'
    ios_command:
      provider: "{{ provider }}"
      commands:
        - show access-list TEST 
    register: before_acl

  - debug: var=before_acl.stdout_lines

  - name: CREATE 'TEST' ACCESS-LIST
    ios_config:
      provider: "{{ provider }}"
      authorize: yes
      lines:
        - 10 permit ip host 1.1.1.1 any
        - 20 deny ip any any
      parents: ['ip access-list extended TEST']
      before: ['no ip access-list extended TEST']
      match: exact

  - name: RUN 'SHOW ACCESS-LIST TEST'
    ios_command:
      provider: "{{ provider }}"
      commands:
        - show access-list TEST 
    register: after_acl

  - debug: var=after_acl.stdout_lines
```

In this playbook, I first import my secrets.yaml variables, which includes my credentials to log into the devices. I then define the 'provider' variable. The provider variable allows you to create a host, username, password, and auth_pass key value in a single place and call it as a single variable, rather than defining each individually for each task. It's a nice little time saver! Finally, I started doing work on the devices themselves.
<br/>
<br/>
Here is my playbook run:

```
(env)jtdub-macbook:ansible2.0 jtdub$ ansible-playbook -i hosts ios.yaml 

PLAY [ios] *********************************************************************

TASK [OBTAIN LOGIN CREDENTIALS] ************************************************
ok: [edge1]
ok: [aggr1a]

TASK [DEFINE PROVIDER] *********************************************************
ok: [edge1]
ok: [aggr1a]

TASK [RUN 'SHOW VERSION'] ******************************************************
ok: [edge1]
ok: [aggr1a]

TASK [debug] *******************************************************************
ok: [edge1] => {
    "version.stdout_lines": [
        [
            "Cisco IOS Software, C181X Software (C181X-ADVENTERPRISEK9-M), Version 15.1(4)M8, RELEASE SOFTWARE (fc2)", 
            "Technical Support: http://www.cisco.com/techsupport", 
            "Copyright (c) 1986-2014 by Cisco Systems, Inc.", 
            "Compiled Fri 07-Mar-14 07:42 by prod_rel_team", 
            "", 
            "ROM: System Bootstrap, Version 12.3(8r)YH13, RELEASE SOFTWARE (fc1)", 
            "", 
            "edge1.sat uptime is 3 days, 22 hours, 3 minutes", 
            "System returned to ROM by reload at 22:18:54 CST Thu Feb 25 2016", 
            "System restarted at 22:19:35 CST Thu Feb 25 2016", 
            "System image file is \"flash:c181x-adventerprisek9-mz.151-4.M8.bin\"", 
            "Last reload type: Normal Reload", 
            "", 
            "", 
            "This product contains cryptographic features and is subject to United", 
            "States and local country laws governing import, export, transfer and", 
            "use. Delivery of Cisco cryptographic products does not imply", 
            "third-party authority to import, export, distribute or use encryption.", 
            "Importers, exporters, distributors and users are responsible for", 
            "compliance with U.S. and local country laws. By using this product you", 
            "agree to comply with applicable laws and regulations. If you are unable", 
            "to comply with U.S. and local laws, return this product immediately.", 
            "", 
            "A summary of U.S. laws governing Cisco cryptographic products may be found at:", 
            "http://www.cisco.com/wwl/export/crypto/tool/stqrg.html", 
            "", 
            "If you require further assistance please contact us by sending email to", 
            "export@cisco.com.", 
            "", 
            "Cisco 1811 (MPC8500) processor (revision 0x400) with 236544K/25600K bytes of memory.", 
            "Processor board ID FTX15110094, with hardware revision 0000", 
            "", 
            "10 FastEthernet interfaces", 
            "1 Serial interface", 
            "1 terminal line", 
            "1 Virtual Private Network (VPN) Module", 
            "62720K bytes of ATA CompactFlash (Read/Write)", 
            "", 
            "", 
            "License Info:", 
            "", 
            "License UDI:", 
            "", 
            "-------------------------------------------------", 
            "Device#\t  PID\t\t\tSN", 
            "-------------------------------------------------", 
            "*0  \t  CISCO1811/K9          FTX15110094     ", 
            "", 
            "", 
            "", 
            "Configuration register is 0x2102", 
            ""
        ]
    ]
}
ok: [aggr1a] => {
    "version.stdout_lines": [
        [
            "Cisco IOS Software, C3750 Software (C3750-IPSERVICESK9-M), Version 12.2(55)SE9, RELEASE SOFTWARE (fc1)", 
            "Technical Support: http://www.cisco.com/techsupport", 
            "Copyright (c) 1986-2014 by Cisco Systems, Inc.", 
            "Compiled Mon 03-Mar-14 22:45 by prod_rel_team", 
            "Image text-base: 0x01000000, data-base: 0x02F00000", 
            "", 
            "ROM: Bootstrap program is C3750 boot loader", 
            "BOOTLDR: C3750 Boot Loader (C3750-HBOOT-M) Version 12.2(44)SE5, RELEASE SOFTWARE (fc1)", 
            "", 
            "aggr1a.sat uptime is 1 week, 3 days, 21 hours, 24 minutes", 
            "System returned to ROM by power-on", 
            "System restarted at 22:58:01 CST Thu Feb 18 2016", 
            "System image file is \"flash:c3750-ipservicesk9-mz.122-55.SE9.bin\"", 
            "", 
            "", 
            "This product contains cryptographic features and is subject to United", 
            "States and local country laws governing import, export, transfer and", 
            "use. Delivery of Cisco cryptographic products does not imply", 
            "third-party authority to import, export, distribute or use encryption.", 
            "Importers, exporters, distributors and users are responsible for", 
            "compliance with U.S. and local country laws. By using this product you", 
            "agree to comply with applicable laws and regulations. If you are unable", 
            "to comply with U.S. and local laws, return this product immediately.", 
            "", 
            "A summary of U.S. laws governing Cisco cryptographic products may be found at:", 
            "http://www.cisco.com/wwl/export/crypto/tool/stqrg.html", 
            "", 
            "If you require further assistance please contact us by sending email to", 
            "export@cisco.com.", 
            "", 
            "cisco WS-C3750-24TS (PowerPC405) processor (revision L0) with 131072K bytes of memory.", 
            "Processor board ID CAT1042ZGKL", 
            "Last reset from power-on", 
            "2 Virtual Ethernet interfaces", 
            "24 FastEthernet interfaces", 
            "2 Gigabit Ethernet interfaces", 
            "The password-recovery mechanism is enabled.", 
            "", 
            "512K bytes of flash-simulated non-volatile configuration memory.", 
            "Base ethernet MAC Address       : 00:19:E7:5F:8F:80", 
            "Motherboard assembly number     : 73-9677-10", 
            "Power supply part number        : 341-0034-01", 
            "Motherboard serial number       : CAT10415NLR", 
            "Power supply serial number      : DTH1037117A", 
            "Model revision number           : L0", 
            "Motherboard revision number     : A0", 
            "Model number                    : WS-C3750-24TS-S", 
            "System serial number            : CAT1042ZGKL", 
            "Top Assembly Part Number        : 800-25857-02", 
            "Top Assembly Revision Number    : D0", 
            "Version ID                      : V05", 
            "CLEI Code Number                : CNMV100CRE", 
            "Hardware Board Revision Number  : 0x01", 
            "", 
            "", 
            "Switch Ports Model              SW Version            SW Image                 ", 
            "------ ----- -----              ----------            ----------               ", 
            "*    1 26    WS-C3750-24TS      12.2(55)SE9           C3750-IPSERVICESK9-M     ", 
            "", 
            "", 
            "Configuration register is 0xF", 
            ""
        ]
    ]
}

TASK [RUN 'SHOW ACCESS-LIST TEST'] *********************************************
ok: [edge1]
ok: [aggr1a]

TASK [debug] *******************************************************************
ok: [edge1] => {
    "before_acl.stdout_lines": [
        [
            ""
        ]
    ]
}
ok: [aggr1a] => {
    "before_acl.stdout_lines": [
        [
            ""
        ]
    ]
}

TASK [CREATE 'TEST' ACCESS-LIST] ***********************************************
changed: [edge1]
changed: [aggr1a]

TASK [RUN 'SHOW ACCESS-LIST TEST'] *********************************************
ok: [edge1]
ok: [aggr1a]

TASK [debug] *******************************************************************
ok: [edge1] => {
    "after_acl.stdout_lines": [
        [
            "Extended IP access list TEST", 
            "    10 permit ip host 1.1.1.1 any", 
            "    20 deny ip any any"
        ]
    ]
}
ok: [aggr1a] => {
    "after_acl.stdout_lines": [
        [
            "Extended IP access list TEST", 
            "    10 permit ip host 1.1.1.1 any", 
            "    20 deny ip any any"
        ]
    ]
}

PLAY RECAP *********************************************************************
aggr1a                     : ok=9    changed=1    unreachable=0    failed=0   
edge1                      : ok=9    changed=1    unreachable=0    failed=0
```

As you can see, I was able to successfully execute a 'show version', verify that I had no access-list called TEST, create it, then verify that it was indeed created.

I'm thrilled that Ansible is finally getting around to recognizing the benefit of supporting the networking community. It's a basic start and it will only get better from here! Soon, I'll post a blog walking through the ios_template module. The documentation on that one looks interesting!
