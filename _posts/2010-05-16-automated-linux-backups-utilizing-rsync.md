---
layout: post
title: Automated Linux Backups utilizing rsync over SSH
date: '2010-05-16'
author: jtdub
tags:
- Linux
- System Administration
- Perl Tips
- packetgeek.net
---

I was recently tasked with coming up with a backup solution for our Linux based servers. My solution was to use rsync over SSH to pull the data that we wanted over and then use tar to create daily archives, which we can then pull off the server to some other type of storage media or a remote server.
<br/>
<br/>
After creating a Linux server that I would use as the backup server, I setup SSH with a public key exchange.
<br/>
<br/>
To do this, I typed "ssh-keygen" on my Linux backup server.
<br/>
<br/>
<pre>root@linuxbackup:~# ssh-keygen<br/>Generating public/private rsa key pair.<br/>Enter file in which to save the key (/root/.ssh/id_rsa):<br/>Enter passphrase (empty for no passphrase):<br/>Enter same passphrase again:<br/>Your identification has been saved in /root/.ssh/id_rsa.<br/>Your public key has been saved in /root/.ssh/id_rsa.pub.<br/>The key fingerprint is:<br/>c3:81:ee:64:5b:d0:8c:8e:5a:ff:68:49:be:f4:ff:68 root@linuxbackup<br/>root@linuxbackup:~#<br/></pre>
<br/>
After creating a public key on my Linux backup server, I moved the public key over to the servers that the server would be accessing.
<br/>
<br/>
<pre>root@linuxbackup:~# ssh-copy-id -i .ssh/id_rsa.pub root@server01<br/></pre>
<br/>
To automate the process, I created a custom perl script.
<br/>
<br/>
<pre>#!/usr/bin/perl<br/><br/>use Time::localtime;<br/><br/>## Date and Time Configuration<br/>$tm                     = localtime;<br/>($day,$month,$year)     = ($tm-&gt;mday,$tm-&gt;mon,$tm-&gt;year);<br/>$year                   += 1900;<br/>$month                  += 1;<br/><br/>## User Changeable Variables<br/>$archiveDir             = "/data/archive";<br/>@server                 = ("server01", "server02");<br/><br/>## The Nitty Gritty<br/>$args = $ARGV[0];<br/>if(!$args) {<br/>        print "Error: Invalid Option.\n";<br/>        print "$0 help\n";<br/>} else {<br/>        arguments();<br/>}<br/>sub arguments {<br/>        if($args eq "help") {<br/>                print "\n$0 help | auto | list\n\n";<br/>                print "help     - Lists all available options.\n";<br/>                print "auto     - Automatically runs the backup functions on the servers listed in the database.\n";<br/>        } elsif($args eq "auto") {<br/>                foreach $box (@server) {<br/>                        chomp($box);<br/>                        `rsync -ae ssh --delete $box:/root /data/$box`;<br/>                        `rsync -ae ssh --delete $box:/home /data/$box`;<br/>                        `rsync -ae ssh --delete $box:/etc /data/$box`;<br/>                        `rsync -ae ssh --delete $box:/var /data/$box`;<br/>                        if($box eq "server02") {<br/>                                `rsync -ae ssh --delete $box:/customdir /data/$box`;<br/>                        }<br/>                        `tar -cpjf $archiveDir/$box-$month$day$year.tar.bz2 /data/$box/`;<br/>                }<br/>        } else {<br/>                print "Error: Invalid Option.\n";<br/>                print "Type: $0 help\n";<br/>        }<br/>}<br/></pre>
<br/>
You will notice that the perl script is pretty simple, but written in a way that it can be easily expanded upon. For example, you might get to the point where keeping up with the @server array is more maintenance than it's worth. You could easily have the perl script access a MySQL database to pull a list of servers and the directories that needed to be pulled over via rsync. You could also add options so that it automatically put the tar.bz2 archive files onto remote storage or even tape.
<br/>
<br/>
To automate the script, save the script in a place like /usr/sbin/linuxbackup.pl and then create a bash script in /etc/cron.daily/ that executes the command "linuxbackup.pl auto". It's really pretty simple.
