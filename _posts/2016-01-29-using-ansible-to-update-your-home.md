---
layout: post
title: Using Ansible to update your Home Dynamic DNS via Rackspace Cloud DNS
date: '2016-01-29'
author: jtdub
tags:
- DevOps
- Ansible
- packetgeek.net
---

Like most home Internet users, my home Internet has a dynamic IP Address. For many years, I used DynDNS to keep a hostname associated to my home Internet, so that I could access my home resources remotely. After DynDNS started charging for the service, I just created a sub-domain off one of the domains that I own. The problem has always been that I would only find out about my IP Address changing after a failed login attempt. Since then, I have created a couple scripts. However, as I go down the Ansible journey, I try to apply the same problems to Ansible to see how it can solve problems. So, I decided to write a playbook to have Ansible automatically update my DNS record as needed.

Here is the playbook:

```yaml
---
- hosts: localhost
  connection: local
  gather_facts: false

  tasks:
  - set_fact:
      domainname: example.com
      hostname: dynamichost.example.com
      rax_username: rackspace_username
      rax_apikey: rackspace_apikey
      update_dns: False

  - name: Identify current public IPv4 address of network
    command: curl -4 icanhazip.com
    register: ipv4_address

  - name: Identify current DNS A record of Dynamic DNS host
    command: dig +short {{ hostname }}
    register: dyndns_host

  - name: Determine if DNS A record needs to be updated 
    set_fact:
      update_dns: True 
    when: ipv4_address.stdout != dyndns_host.stdout

  - name: Update DNS A record
    local_action:
      module: rax_dns_record
      username: "{{ rax_username }}"  
      api_key: "{{ rax_apikey }}" 
      domain: "{{ domainname }}"
      name: "{{ hostname }}"
      data: "{{ ipv4_address.stdout }}"
      type: A
    register: a_record
    when: update_dns == True
```

As you can see it's pretty straight forward. I define several facts up front, mostly dealing with the Rackspace Cloud DNS Authentication, domain, and hostname settings. Then I run plays to determine what my current IP Address is, what the DNS A record is, comparing the two, then updating the DNS as needed.

It should be simple enough to run the playbook as a cron-job. So far, it works great!

The playbook is available via my [github](https://github.com/jtdub/ansible-rax-dyndns).
