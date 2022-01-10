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
<br/>
<br/>
Here is the playbook:
<br/>
<pre class="lang:yaml decode:true">---<br/>- hosts: localhost<br/>  connection: local<br/>  gather_facts: false<br/><br/>  tasks:<br/>  - set_fact:<br/>      domainname: example.com<br/>      hostname: dynamichost.example.com<br/>      rax_username: rackspace_username<br/>      rax_apikey: rackspace_apikey<br/>      update_dns: False<br/><br/>  - name: Identify current public IPv4 address of network<br/>    command: curl -4 icanhazip.com<br/>    register: ipv4_address<br/><br/>  - name: Identify current DNS A record of Dynamic DNS host<br/>    command: dig +short {{ "{{" }} hostname }}<br/>    register: dyndns_host<br/><br/>  - name: Determine if DNS A record needs to be updated <br/>    set_fact:<br/>      update_dns: True <br/>    when: ipv4_address.stdout != dyndns_host.stdout<br/><br/>  - name: Update DNS A record<br/>    local_action:<br/>      module: rax_dns_record<br/>      username: "{{ "{{" }} rax_username }}"  <br/>      api_key: "{{ "{{" }} rax_apikey }}" <br/>      domain: "{{ "{{" }} domainname }}"<br/>      name: "{{ "{{" }} hostname }}"<br/>      data: "{{ "{{" }} ipv4_address.stdout }}"<br/>      type: A<br/>    register: a_record<br/>    when: update_dns == True</pre>
<br/>
As you can see it's pretty straight forward. I define several facts up front, mostly dealing with the Rackspace Cloud DNS Authentication, domain, and hostname settings. Then I run plays to determine what my current IP Address is, what the DNS A record is, comparing the two, then updating the DNS as needed.
<br/>
<br/>
It should be simple enough to run the playbook as a cron-job. So far, it works great!
<br/>
<br/>
The playbook is available via my
<a href="https://github.com/jtdub/ansible-rax-dyndns" target="_blank">
 github
</a>
.
