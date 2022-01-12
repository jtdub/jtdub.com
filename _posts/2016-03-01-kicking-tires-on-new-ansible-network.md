---
layout: post
title: Kicking the tires on the new Ansible Network Modules, Part 2
date: '2016-03-01'
author: jtdub
tags:
- Python Tips
- Network Programmability
- DevOps
- Network DevOps
- Ansible
- packetgeek.net
---

In the [previous blog](http://www.packetgeek.net/2016/02/kicking-the-tires-with-the-new-ansible-network-modules/), I kicked the tires on the ios_command and ios_config Ansible modules. I still had my development environment set up from then, so I decided that I wanted to kick the tires on the ios_template module.

The [online documentation](http://docs.ansible.com/ansible/ios_template_module.html) currently has several errors, with the module documentation in the same state, which is undesirable. However, after some experimentation, I feel that I can adequately describe what the module does.

You feed the module a candidate configuration for a device, the module will then reach out to the device, pull its current running configuration, compare the running configuration to the candidate configuration, determine what configuration needs to be added to the device based upon the comparison, then add the configuration to the device.

I've noted two caveats with this module. First, it will not negate any commands, so if you update your configuration template to remove a swath of configuration, the module will not make those changes. Second, the module isn't intelligent enough to determine the risk associated with a command, thus it's unable to take preemptive actions, such as bleeding traffic from a link or device.

With that in mind, let's get to the playbook.

Here is what my playbook looks like:

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

  - name: TEST IOS_TEMPLATE 
    ios_template:
      provider: "{{ provider }}"
      authorize: true
      backup: true
      src: "{{ inventory_hostname }}.candidate_config.txt"
    register: template

  - debug: var=template
```

In this playbook, the src file *{{ "{{" }} inventory_hostname }}.candidate_config.txt*, which are referenced, contain the running configuration of each of my devices in inventory, with the exception that I've added an access-list called TEST. Given what we know of the module, it will compare the running config to the candidate config, determine that the access-list called TEST is missing from the running config, and attempt to add the access-list to the device.

You can see below that there is an access-list at the tail end of both of the configurations.

```
(env)jtdub-macbook:ansible2.0 jtdub$ tail edge1.candidate_config.txt 
!
ntp source Vlan2
ntp access-group peer NAT kod
ntp master 3
ntp update-calendar
ntp server 17.151.16.21
ntp server 17.151.16.34 prefer
ip access-list standard TEST
 permit host 1.1.1.1
end
(env)jtdub-macbook:ansible2.0 jtdub$ tail aggr1a.candidate_config.txt 
 exec-timeout 15 0
 login authentication auth_local
 transport input ssh
line vty 5 15
!
ntp source Vlan2
ntp server 172.16.1.1 prefer
ip access-list standard TEST
 permit host 1.1.1.1
end
```

Now, if we run the playbook, you can see the results.

```
(env)jtdub-macbook:ansible2.0 jtdub$ ansible-playbook -i hosts ios_template.yaml 

PLAY [ios] *********************************************************************

TASK [OBTAIN LOGIN CREDENTIALS] ************************************************
ok: [edge1]
ok: [aggr1a]

TASK [DEFINE PROVIDER] *********************************************************
ok: [aggr1a]
ok: [edge1]

TASK [TEST IOS_TEMPLATE] *******************************************************
changed: [aggr1a]
changed: [edge1]

TASK [debug] *******************************************************************
ok: [edge1] => {
    "template": {
        "changed": true, 
        "responses": [
            "", 
            "", 
            ""
        ], 
        "updates": [
            "clock summer-time CST recurring", 
            "ip access-list standard TEST", 
            "permit host 1.1.1.1"
        ]
    }
}
ok: [aggr1a] => {
    "template": {
        "changed": true, 
        "responses": [
            "", 
            ""
        ], 
        "updates": [
            "ip access-list standard TEST", 
            "permit host 1.1.1.1"
        ]
    }
}

PLAY RECAP *********************************************************************
aggr1a                     : ok=4    changed=1    unreachable=0    failed=0   
edge1                      : ok=4    changed=1    unreachable=0    failed=0   

(env)jtdub-macbook:ansible2.0 jtdub$
```

That is definitely cool! Though, it's also definitely lacking from a configuration intent perspective. I'm sure that it will improve with time.

Some colleagues and I have been attempting to solve this configuration intent problem. It's a difficult problem to solve for, but we have a working code base. Soon, I'll try to write about configuration intent and how we are approaching the problem.
