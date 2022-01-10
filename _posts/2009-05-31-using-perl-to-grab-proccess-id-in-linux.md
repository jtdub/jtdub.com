---
layout: post
title: Using Perl to grab a proccess id in Linux
date: '2009-05-31'
author: jtdub
tags:
- Perl Tips
- packetgeek.net
---

Ever since I first started doing Linux system administration, I've used perl scripts to automate some basic tasks. I've never really been that great at writing scripts because I never took the time to sit down and really learn the intricate details of the language. Here recently, I've written some of my most complex and detail oriented scripts, where I've had to really learn a little bit about regular expressions. Along the way I also learned how to pick very specific data out of a array and feed it to my script for processing.
<br/>
<br/>
Here is a simple script that utilizes the 'ps' command, grabs the process id (PID) from the array, and prints as an output.
<br/>
<pre><br/>#!/usr/bin/perl<br/><br/>@ps = `ps ax | grep sshd`;<br/>foreach $proc (@ps) {<br/>        @pid = split(/ +/,$proc);<br/>        print "PID: $pid[0]\n";<br/>}<br/></pre>
<br/>
The things that you can with this sort of script are endless in automating system administration.
