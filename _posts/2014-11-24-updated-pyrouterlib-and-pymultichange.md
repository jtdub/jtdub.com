---
layout: post
title: Updated pyRouterLib and pyMultiChange
date: '2014-11-24'
author: jtdub
tags:
- Cisco Administration Python Scripting
- Software Defined Networking
- Python Tips
- packetgeek.net
---

I've updated a two pieces of software that I've been writing and maintaining. The first is pyRouterLib. pyRouterLib is a library, written in Python, that takes the common functionality of managing a Cisco router or switch, via Python and makes it easy to implement.
<br/>
<br/>
Here is a list of it's functionality and a brief description:
<br/>
<ul>
 <br/>
 <li>
  User Credential Storage - This functionality is useful when scripting a task to run multiple commands on multiple devices. It will create and store your credentials in ~/.tacacslogin - which is admittedly insecure. I'll be working on something with a little more security when I have time.
 </li>
 <br/>
 <li>
  Telnet Module - This module allows you to quickly define the telnet method as a means of logging in and managing a device. It should be fully functional, but hasn't been tested thoroughly, yet.
 </li>
 <br/>
 <li>
  SSH Module - This module allows you to quickly define the ssh method as a means of logging in and managing a device. Currently it has a limitation of not being able to execute the 'enable' command and enter your enable credentials. I'm still working on this functionality. This module should suite you fine if you don't need to enter enable mode or if you automatically login as a privileged user.
 </li>
 <br/>
 <li>
  SNMP Module - This module is a work in progress and doesn't have any functionality, yet.
 </li>
 <br/>
</ul>
<br/>
In addition to updating its functionality, I updated the documentation, that explains how to use it. I also have a test script with both telnet and ssh functionality enabled - for demo purposes.
<br/>
<br/>
The second package that I updated with my pyMultiChange script. It's been updated to be fully integrated with the pyRouterLib library. I've also created two versions of the script. One for telnet and the second for ssh.
<br/>
<br/>
Both can be downloaded from my Github account.
<br/>
<ul>
 <br/>
 <li>
  <a href="https://github.com/jtdub/pyRouterLib" target="_blank" title="pyRouterLib">
   pyRouterLib
  </a>
 </li>
 <br/>
 <li>
  <a href="https://github.com/jtdub/pyMultiChange" target="_blank" title="pyMultiChange">
   pyMultiChange
  </a>
 </li>
 <br/>
</ul>