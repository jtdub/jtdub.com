---
layout: post
title: Network Lifecycle Management with Hierarchical Configuration
date: '2016-07-08'
author: jtdub
tags:
- Cisco Administration Python Scripting
- Python Tips
- Network Programmability
- DevOps
- Network DevOps
- packetgeek.net
---

In a [previous blog](https://www.packetgeek.net/2016/03/kicking-the-tires-on-the-new-ansible-network-modules-part-2/), I hinted at a network configuration life cycle management library called hierarchical_configuration. I've been meaning to write about it for a while, but we've been super busy at work. I also wanted to ensure that we get our latest version of the library out in the public for general consumption before I wrote about it.

As your fleet routers and switches grow, it becomes pretty natural to place these devices into a set of categories. For example, core, aggregation, and access. Each of these categories typically have a standard configuration. Hopefully each of these standard configurations exists as templates, so that new deployments can be rolled out quickly. But, what about making changes to the templates? Do you make changes to these templates, then continue to roll them out to new deployments, leaving the existing install base with an outdated configuration? Or do you return to the install base and remediate the devices with updated configurations? What if you have thousands of devices? This has been a problem that my colleagues and I have set out to solve. This is how hierarchical_configuration has evolved.

So, what is hierarchical_configuration? hierarchical_configuration is a python library that allows you to compare the running configuration and the intended configuration from a network device, then generate a set of commands that it will bring the network device into compliance with the intended configuration. hierarchical_configuration also has an extensive configuration file, so that you can define how specific commands or sections of commands get remediated.

Most utilities that performs a similar function as hierarchical_configuration, apply command remediation by negating a command, then applying the new command. For instance, if you wanted to change the interface description of an interface, most utilities will do something like:

```
interface Ethernet0/1
 no description ROUTER1
 description ROUTER2
```

That works, but it's wasteful on CPU cycles, which slows down the over all application run time when you are attempting to apply interface descriptions to thousands of interfaces. What if the command was something that could be impactful, if it were negated? Maybe something like changing 'transport input ssh telnet' to 'transport input ssh', under your line vty? Negating the command could potentially cause you to lose management access.

hierarchical_configuration gives you several configuration options for dealing with such scenarios. You define those as a [YAML](http://yaml.org/) file under hier_options. Here is a sample of hier_options:

```yaml
---
hier_tags:
- lineage:
  - startswith:
    - ip access-list extended TEST
    - no ip access-list extended TEST
  add_tags: NEW_ACL
- lineage:
  - startswith: interface
  - startswith: ip access-group TEST
  add_tags: NEW_ACL
- lineage:
  - startswith:
    - ip domain-name
    - no ip domain-name
    - ip domain-lookup
    - no ip domain-lookup
    - logging
    - no logging
    - snmp-server 
    - no snmp-server 
    - ntp server
    - no ntp server
    - ip tcp path-mtu-discovery
    - ip access-list resequence
  add_tags: safe 
- lineage:
  - startswith: line
  - startswith: exec-timeout
  add_tags: safe 
- lineage:
  - startswith: interface
  - startswith: ip access-group
  add_tags: unsafe 
- lineage:
  - startswith: router ospf
    new_in_config: false
  - startswith:
    - ispf
    - nsf
    - log
  add_tags: safe 
- lineage: 
  - startswith: router ospf
    new_in_config: false
  - startswith:
    - network 
    - area
  add_tags: unsafe 

hier_options:
  #Indicates the style of the configuration
  style: ios

  #if there is a delta, overwrite these parents instead of one of their children
  sectional_overwrite:
  - lineage:
    - startswith: ipv6 access-list

  ordering:
  - lineage:
    - startswith:
      - ip access-list
      - access-list
    order: 300
  - lineage:
    - startswith:
      - tacacs-server host
    order: 400
  - lineage:
    - startswith: interface
    - startswith:
      - ip access-group
      - no ip access-group
    order: 400
  - lineage:
    - startswith:
      - no ip access-list
      - no access-list
      - no ip prefix-list
      - no tacacs-server host
    order: 590 
  - lineage:
    - contains: ip spd queue min-threshold
    order: 601
  - lineage:
    - contains: ip spd queue max-threshold
    order: 602

  sectional_overwrite_no_negate: []

  #adds +1 indent to lines following start_expression and removes the +1 indent for lines following end_expression
  indent_adjust: []

  parent_allows_duplicate_child: []

  sectional_exiting:
  - lineage:
    - startswith: router bgp
    - startswith: template peer-policy
    exit_text: exit-peer-policy
  - lineage:
    - startswith: router bgp
    - startswith: template peer-session
    exit_text: exit-peer-session
  - lineage:
    - startswith: router bgp
    - startswith: address-family
    exit_text: exit-address-family

  #substitions against the full multi-line config text
  full_text_sub:
  - search: 'banner exec (\S+)\n(.*\n)+\\1\s*\n'
    replace: ''
  - search: 'banner motd (\S+)\n(.*\n)+\\1\s*\n'
    replace: ''

  #substitions against each line of the config text
  per_line_sub:
  - search: ^Building configuration.*
    replace: ''
  - search: ^Current configuration.*
    replace: ''
  - search: ^! Last configuration change.*
    replace: ''
  - search: ^! NVRAM config last updated.*
    replace: ''
  - search: ^ntp clock-period .*
    replace: ''
  - search: .*message-digest-key.*
    replace: ''
  - search: ^version.*
    replace: ''
  - search: .*password.*
    replace: ''
  - search: ^ logging event link-status$
    replace: ''
  - search: ^ logging event subif-link-status$
    replace: ''
  - search: ^\s*ipv6 unreachables disable$
    replace: ''
  - search: ^\s*key .*
    replace: ''
  - search: ^end$
    replace: ''
  - search: '^\s*[#!].*'
    replace: ''
  - search: ^ no ip address
    replace: ''
  - search: ^ exit-peer-policy
    replace: ''
  - search: ^ exit-peer-session
    replace: ''
  - search: ^ exit-address-family
    replace: ''
  - search: ^crypto key generate rsa general-keys.*$
    replace: ''
  - search: .*key-string.*
    replace: ''

  idempotent_commands_blacklist: []

  #These commands do not require negation, they simply overwrite themselves
  idempotent_commands:
  - lineage:
    - startswith: hostname
  - lineage:
    - startswith: logging source-interface
  - lineage:
    - startswith: interface
    - startswith: description
  - lineage:
    - startswith: interface
    - startswith: ip address
  - lineage:
    - startswith: line vty
    - startswith:
      - transport input
      - access-class
      - ipv6 access-class
  - lineage:
    - startswith: interface
    - re_search: standby \d+ (priority|authentication md5)
  - lineage:
    - startswith: router bgp
    - startswith: bgp router-id
  - lineage:
    - startswith: router ospf
    - startswith: router-id
  - lineage:
    - startswith: ipv6 router ospf
    - startswith: router-id
  - lineage:
    - startswith: router ospf
    - startswith: log-adjacency-changes
  - lineage:
    - startswith: ipv6 router ospf
    - startswith: log-adjacency-changes
  - lineage:
    - startswith: router bgp
    - re_search: neighbor \S+ description
  - lineage:
    - startswith: snmp-server community
  - lineage:
    - startswith: snmp-server location
  - lineage:
    - equals: line con 0
    - startswith: exec-timeout
  - lineage:
    - startswith: interface
    - startswith: ip ospf message-digest-key
  - lineage:
    - startswith: logging buffered
  - lineage:
    - startswith: tacacs-server key
  - lineage:
    - startswith: logging facility
  - lineage:
    - startswith: vlan internal allocation policy

  #Default when expression: list of expressions
  negation_default_when: []
  #- lineage:
  #  - startswith: interface

  #Negate substitutions: expression -> negate with
  negation_negate_with: []
  #- lineage:
  #  - startswith: interface
  #  use: command
```

Lets break down the individual sections of hier_options. The first section is 'sectional_overwrite'. sectional_overwrite does exactly like it sounds. It over-writes an entire section of configuration if there is a change. In the example, it tags ipv6 access-lists as a section of code that should use sectional_overwrite.  If any changes are made to the intended configuration for ipv6 access-list, then hierarchical_configuration over writes the entire section of configuration, rather than targeting individual lines of children configuration in the section.

The next section is 'ordering'. Ordering is a very handy configuration option. It allows you to weight the order in which commands are presented in hierarchical_configuration. The default weight is 500. The smaller the number, the higher up in the configuration the commands are presented. While the commands tagged with larger numbers are presented lower in the configuration.

For instance, assume that you have an access-list called TEST, which is applied to Ethernet0/1:

```
ip access-list TEST
 permit ip any host 1.1.1.1
interface Ethernet0/1
 ip access-group TEST in
```

Let's say that you want to create a new access-list called TESTING and apply it to Ethernet0/1, rendering the access-list TEST as un-needed. When you go to apply the configuration, you don't want to remove the access-list TEST before you've created access-list TESTING and applied it to interface Ethernet0/1. Doing so may impact traffic that is flowing across the interface. The preferable order of operation is:

* Create the new access-list
* Apply the new access-list to the interface
* Remove the old access-list

To do so, you will want to the command 'no ip access-list' closer to the bottom of the list of commands. You would do this, by setting the order of the negation of ip access-list higher than 500.

```
  ordering:
  - lineage:
    - startswith:
      - no ip access-list
    order: 525
```

In this example, any command generated that starts with 'no ip access-list' gets tagged with an order of 525, which moves that section of configuration lower into the generated config. The generated configuration would look like:

```
ip access-list TESTING
 permit ip any host 1.1.1.1
interface Ethernet0/1
 ip access-group TESTING in
no ip access-list TEST
```

The next two sections are 'full_text_sub' and 'per_line_sub'. When you pull a running config from a device, it will typically contain some fluff, such as:

```
#sh run
Building configuration...

Current configuration : 9574 bytes
!
! Last configuration change at 19:51:43 CST Mon Apr 25 2016 by jtdub
version 15.1
```

That kind of text is just back ground noise, when we are attempting to determine the difference between the running config and the intended config. So, per_line_sub attempts to resolve that by ignoring it when comparing the configurations.

```
  per_line_sub:
  - search: ^Building configuration.*
    replace: ''
```

As you can see, it will find any line that contains 'Building configuration" and replace it with no data, effectively deleting the line. full_text_sub performs a similar task, but for entire sections of code. In our example, we ignore the banners on the device, as those can have information that is unique to the device.

```
  full_text_sub:
  - search: 'banner exec (\S+)\n(.*\n)+\\1\s*\n'
    replace: ''
  - search: 'banner motd (\S+)\n(.*\n)+\\1\s*\n'
    replace: ''
```

Hierarchical_configuration understands sections of config. It does this by assuming that a line of configuration that doesn't have any indentation to be a parent and any lines of configuration under the parent that have indentation are children of the parent. When the config reaches another line without indentation, the section of configuration ends. An example would be an interface configuration.

```
interface Ethernet0/1       : Parent configuration section
 switchport                 : Child configuration section of interface Ethernet0/1
 switchport mode access     : Child configuration section of interface Ethernet0/1
 switchport access vlan 10  : Child configuration section of interface Ethernet0/1
interface Ethernet0/2       : Parent configuration section
 no switchport              : Child configuration section of interface Ethernet0/2
 ip address 10.0.0.0/31     : Child configuration section of interface Ethernet0/2
```

In some cases, there will be multiple tiers of parent / child configurations. An example would be peer templates in BGP.

```
router bgp 65000          : Parent configuration section
 template peer-session RR : Child configuration section of 'router bgp 65000'
  remote-as 65000         : Child configuration section of 'template peer-session RR'
  update-source loopback0 : Child configuration section of 'template peer-session RR'
 exit-peer-session        : Sectional exit
 template peer-policy RR  : Child configuration section of 'router bgp 65000'
  route-reflector-client  : Child configuration section of 'template peer-policy RR'
 exit-peer-policy         : Sectional exit
```

With 'sectional_exiting', you can define sections of configuration that have sub-children of children, as explained above.

```
  sectional_exiting:
  - lineage:
    - startswith: router bgp
    - startswith: template peer-policy
    exit_text: exit-peer-policy
  - lineage:
    - startswith: router bgp
    - startswith: template peer-session
    exit_text: exit-peer-session
  - lineage:
    - startswith: router bgp
    - startswith: address-family
    exit_text: exit-address-family
```

'idempotent_commands' is the section where you define what should be over-written, rather than negated, then re-applied with new configuration. Commands such as hostname, description, ip address, etc should all be over-written, rather than negated.

```
  idempotent_commands:
  - lineage:
    - startswith: hostname
  - lineage:
    - startswith: logging source-interface
  - lineage:
    - startswith: interface
    - startswith: description
  - lineage:
    - startswith: interface
    - startswith: ip address
```

Another very handy set of options is command tagging, which resides in a different config section from hier_options, called hier_tags. Being able to tag commands allows you to generate remediation commands which target very specific commands, such as creating a new access-list, applying it, then removing the old access-list. We'll continue to use the examples that I've have above with replacing the access-list TEST with TESTING. The first thing we need to do is set up our tagging, which will look like:

```
hier_tags:
- lineage:
  - startswith:
    - ip access-list extended TEST
    - no ip access-list extended TEST
  add_tags: NEW_ACL
- lineage:
  - startswith: interface
  - startswith: ip access-group TEST
  add_tags: NEW_ACL
```

Assume that your running config is:

```
hostname router
!
interface Ethernet0/1
 ip address 10.0.0.0/31
 ip access-group TEST in
!
interface Ethernet0/2
 ip address 10.0.0.2/31
!
ip access-list extended TEST
 permit ip any host 1.1.1.1
 permit ip any host 4.4.4.4
 permit ip any host 5.5.5.5
 permit ip any host 6.6.6.6
!
router ospf 1
 network 10.0.0.0 0.0.255.255 area 0
!
snmp-server community private
!
ntp server 11.22.33.44
```

and your intended config is:

```
hostname router
!
interface Ethernet0/1
 ip address 10.0.0.0/31
 ip access-group TESTING in
!
interface Ethernet0/2
 ip address 10.0.0.2/31
 ip access-group SOMEACL in
 ipv6 enable
 ipv6 filter TEST out 
!
ip access-list extended TESTING
 permit ip any host 1.1.1.1
 permit ip any host 4.4.4.4
 permit ip any host 5.5.5.5
 permit ip any host 6.6.6.6
!
ip access-list extended SOMEACL
 permit ip any host 7.7.7.7
!
ipv6 access-list TEST
 permit ipv6 any 2001::1/128
!
router ospf 1
 network 10.0.0.0 0.0.255.255 area 0
!
snmp-server community private
!
ntp server 11.22.33.44
```

We can use hierarchical_configuration compare the two configurations, make the appropriate configuration tag (NEW_ACL), then spit out a configuration plan based on the NEW_ACL tag.

Here is a sample output of the configuration comparison:

```
$ ./example.py 

{'comment': "new section, didn't exist before", 'text': 'ip access-list extended TESTING', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 10 permit ip any host 1.1.1.1', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 20 permit ip any host 4.4.4.4', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 30 permit ip any host 5.5.5.5', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 40 permit ip any host 6.6.6.6', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': "new section, didn't exist before", 'text': 'ip access-list extended SOMEACL', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' 10 permit ip any host 7.7.7.7', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': 'interface Ethernet0/1', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL', 'unsafe']}
{'comment': '', 'text': ' no ip access-group TEST in', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' ip access-group TESTING in', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL', 'unsafe']}
{'comment': '', 'text': 'interface Ethernet0/2', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['unsafe']}
{'comment': '', 'text': ' ip access-group SOMEACL in', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['unsafe']}
{'comment': '', 'text': ' ipv6 enable', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' ipv6 filter TEST out', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': "new section, didn't exist before", 'text': 'ipv6 access-list TEST', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' permit ipv6 any 2001::1/128', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': 'removes 6 lines', 'text': 'no ip access-list extended TEST', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
```

As you can see, only the parts of the config pertaining to the TESTING access-list are tagged with the NEW_ACL tag. We can now generate a config plan based on that tag.

```
$ ./example.py 

Python dictionary of the comparison results

{'comment': "new section, didn't exist before", 'text': 'ip access-list extended TESTING', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 10 permit ip any host 1.1.1.1', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 20 permit ip any host 4.4.4.4', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 30 permit ip any host 5.5.5.5', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': '', 'text': ' 40 permit ip any host 6.6.6.6', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}
{'comment': "new section, didn't exist before", 'text': 'ip access-list extended SOMEACL', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' 10 permit ip any host 7.7.7.7', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': 'interface Ethernet0/1', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL', 'unsafe']}
{'comment': '', 'text': ' no ip access-group TEST in', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' ip access-group TESTING in', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL', 'unsafe']}
{'comment': '', 'text': 'interface Ethernet0/2', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['unsafe']}
{'comment': '', 'text': ' ip access-group SOMEACL in', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['unsafe']}
{'comment': '', 'text': ' ipv6 enable', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' ipv6 filter TEST out', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': "new section, didn't exist before", 'text': 'ipv6 access-list TEST', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': '', 'text': ' permit ipv6 any 2001::1/128', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': []}
{'comment': 'removes 6 lines', 'text': 'no ip access-list extended TEST', 'post_exec_sleep': 0, 'post_exec_string': '', 'tags': ['NEW_ACL']}

Config plan based on NEW_ACL tag

ip access-list extended TESTING
 10 permit ip any host 1.1.1.1
 20 permit ip any host 4.4.4.4
 30 permit ip any host 5.5.5.5
 40 permit ip any host 6.6.6.6
interface Ethernet0/1
 ip access-group TESTING in
no ip access-list extended TEST
```

Here is the script that produced the output:

```
#!/usr/bin/env python

import yaml

from hierarchical_configuration import HierarchicalConfiguration

config_options = yaml.load(open('main.yml', 'r'))
hier_tags = config_options['hier_tags']
hier_options = config_options['hier_options']

running_config_hier = HierarchicalConfiguration(
                          options=hier_options)
running_config_hier.from_file('running.config')

compiled_config_hier = HierarchicalConfiguration(
                           options=hier_options)
compiled_config_hier.from_file('compiled.config')

remediation_config_hier = compiled_config_hier.deep_diff_tree_with(
                              running_config_hier)
remediation_config_hier.set_order_weight()
remediation_config_hier.add_sectional_exiting()
remediation_config_hier.add_tags(hier_tags)

print('\nPython dictionary of the comparison results\n')
for command in remediation_config_hier.to_detailed_ouput():
    print(command)

print('\nConfig plan based on NEW_ACL tag\n')
for command in remediation_config_hier.to_detailed_ouput():
    if 'NEW_ACL' in command['tags']:
        print(command['text'])
```

Let's break down the script. The very first thing we do is import yaml and hierarchical_configuration:

```python
import yaml

from hierarchical_configuration import HierarchicalConfiguration
```

Next, we read the hierarchical_configuration config file and define the options and tags variables:

```python
config_options = yaml.load(open('main.yml', 'r'))
hier_tags = config_options['hier_tags']
hier_options = config_options['hier_options']
```
Now, we define an instance of hierarchical_configuration for the running config and load the running config from a file:

```python
running_config_hier = HierarchicalConfiguration(
                          options=hier_options)
running_config_hier.from_file('running.config')
```

Then, we do the same for the intended config:

```
compiled_config_hier = HierarchicalConfiguration(
                           options=hier_options)
compiled_config_hier.from_file('compiled.config')
```

Once that is done, we can perform the comparison:

```
remediation_config_hier = compiled_config_hier.deep_diff_tree_with(
                              running_config_hier)
```

Now, we load the ordering, sectional exiting, and tags options:

```
remediation_config_hier.set_order_weight()
remediation_config_hier.add_sectional_exiting()
remediation_config_hier.add_tags(hier_tags)
```

At this point, everything is loaded into memory. The next two portions of code are simply to have a visual of what is happening. The first portion is a for-loop, which displays the raw list of dictionaries:

```
print('\nPython dictionary of the comparison results\n')
for command in remediation_config_hier.to_detailed_ouput():
    print(command)
```

Finally, the finished product. Generating a config plan, based on the NEW_ACL tag.

```
print('\nConfig plan based on NEW_ACL tag\n')
for command in remediation_config_hier.to_detailed_ouput():
    if 'NEW_ACL' in command['tags']:
        print(command['text'])
```

As you can see, hierarchical configuration is a very powerful life-cycle management tool for network gear. We've been using it successfully on IOS, IOS-XR, IOS-XE, NX-OS, and EOS devices. It has made our work less risky - from an outage perspective - more consistent, and allows us to automate and move faster than we have in previous years.

The code is available on Github [here](https://github.com/jtdub/hierarchical_configuration).
