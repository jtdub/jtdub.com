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

After creating a Linux server that I would use as the backup server, I setup SSH with a public key exchange.

To do this, I typed "ssh-keygen" on my Linux backup server.
```bash
root@linuxbackup:~# ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
c3:81:ee:64:5b:d0:8c:8e:5a:ff:68:49:be:f4:ff:68 root@linuxbackup
root@linuxbackup:~#
```

After creating a public key on my Linux backup server, I moved the public key over to the servers that the server would be accessing.

```bash
root@linuxbackup:~# ssh-copy-id -i .ssh/id_rsa.pub root@server01
```
To automate the process, I created a custom perl script.

```perl
#!/usr/bin/perl

use Time::localtime;

## Date and Time Configuration
$tm                     = localtime;
($day,$month,$year)     = ($tm->mday,$tm->mon,$tm->year);
$year                   += 1900;
$month                  += 1;

## User Changeable Variables
$archiveDir             = "/data/archive";
@server                 = ("server01", "server02");

## The Nitty Gritty
$args = $ARGV[0];
if(!$args) {
        print "Error: Invalid Option.\n";
        print "$0 help\n";
} else {
        arguments();
}
sub arguments {
        if($args eq "help") {
                print "\n$0 help | auto | list\n\n";
                print "help     - Lists all available options.\n";
                print "auto     - Automatically runs the backup functions on the servers listed in the database.\n";
        } elsif($args eq "auto") {
                foreach $box (@server) {
                        chomp($box);
                        `rsync -ae ssh --delete $box:/root /data/$box`;
                        `rsync -ae ssh --delete $box:/home /data/$box`;
                        `rsync -ae ssh --delete $box:/etc /data/$box`;
                        `rsync -ae ssh --delete $box:/var /data/$box`;
                        if($box eq "server02") {
                                `rsync -ae ssh --delete $box:/customdir /data/$box`;
                        }
                        `tar -cpjf $archiveDir/$box-$month$day$year.tar.bz2 /data/$box/`;
                }
        } else {
                print "Error: Invalid Option.\n";
                print "Type: $0 help\n";
        }
}
```

You will notice that the perl script is pretty simple, but written in a way that it can be easily expanded upon. For example, you might get to the point where keeping up with the @server array is more maintenance than it's worth. You could easily have the perl script access a MySQL database to pull a list of servers and the directories that needed to be pulled over via rsync. You could also add options so that it automatically put the tar.bz2 archive files onto remote storage or even tape.

To automate the script, save the script in a place like `/usr/sbin/linuxbackup.pl` and then create a bash script in `/etc/cron.daily/` that executes the command `linuxbackup.pl auto`. It's really pretty simple.
