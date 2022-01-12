---
layout: post
title: Quick intro to Puppet
date: '2014-02-09'
author: jtdub
tags:
- Linux
- Puppet
- packetgeek.net
---

I've been using puppet for a while to automate several things within the Linux servers that I manage. It's also one of those things that if I don't use it in a while, I forget it. So, I'm going to do a quick run through of registering a puppet agent with a puppet master. I'll also show some of the things that every Linux install gets pushed, aka the default settings.

Here is my default manifest that every system gets:

```bash
[root@bastion ~]# cat /etc/puppet/manifests/site.pp 
node default {
	file { "/etc/yum.repos.d/drivesrvr.repo":
		mode => '644',
		owner => root,
		group => root,
		source => "puppet:///files/drivesrvr.repo",
	}
        file { "/etc/hosts":
		mode => '644',
		owner => root,
		group => root,
                source => "puppet:///files/hosts",
        }
        file { "/etc/ssh/sshd_config":
                mode => '600',
                owner => root,
                group => root,
                source => "puppet:///files/sshd_config",
        }
        file { "/etc/pam.d/su":
                mode => '644',
                owner => root,
                group => root,
                source => "puppet:///files/su",
        }
	file { "/etc/sudoers":
                mode => '440',
                owner => root,
                group => root,
		source => "puppet:///files/sudoers",
	}
	file { "/etc/selinux/config":
		mode => '644',
		owner => root,
		group => root,
		source => "puppet:///files/selinux",
	}
	file { "/etc/yum.repos.d/epel.repo":
		mode => '644',
		owner => root,
		group => root,
		source => "puppet:///files/epel.repo",
	}
        file { "/etc/yum.repos.d/epel-testing.repo":
                mode => '644',
                owner => root,
                group => root,
                source => "puppet:///files/epel-testing.repo",
        }
        file { "/etc/logrotate.conf":
                mode => '644',
                owner => root,
                group => root,
                source => "puppet:///files/logrotate.conf",
        }
        file { "/etc/sysconfig/clock":
                mode => '644',
                owner => root,
                group => root,
                source => "puppet:///files/clock",
        }
	package { "denyhosts": 
		ensure => installed,
	}
	package { "mailx":
		ensure => installed,
	}
	package { "vim-enhanced":
		ensure => installed,
	}
	package { "yum-cron":
		ensure => installed,
	}
        package { "driveclient":
		ensure => installed,
	}
	service { "yum-cron":
		ensure => running,
		enable => true,
		subscribe => [Package["yum-cron"]],
	}
	service { "denyhosts":
		ensure => running,
		enable => true,
		subscribe => [Package["denyhosts"]],
	}
	service { "driveclient":
		ensure => running,
		enable => true,
		subscribe => [Package["driveclient"]],
	}
	#class timezone-base {
    	#	package { "tzdata":
        #	ensure => installed
    	#	}
    	#	file { "/etc/localtime":
        #		source => "file:///usr/share/zoneinfo/America/Chicago",
        #		require => Package["tzdata"]
    	#	}
	#}
	#class timezone-central inherits timezone-base {
	#}
	user { "defaultuser":
		allowdupe => false,
		comment => "some default user",
		ensure => present,
		groups => ['wheel'],
		home => "/home/defaultuser",
		managehome => true,
		shell => '/bin/bash'
		#password => '', 
	}
}
```

The first thing that I do is install puppet on the new agent (client) node.

```bash
[root@puppet ~]# yum -y install puppet
Loaded plugins: fastestmirror
Determining fastest mirrors
base                                                                                                                                                                                        | 3.7 kB     00:00     
base/primary_db                                                                                                                                                                             | 4.4 MB     00:00     
epel                                                                                                                                                                                        | 4.2 kB     00:00     
epel/primary_db                                                                                                                                                                             | 5.9 MB     00:00     
extras                                                                                                                                                                                      | 3.4 kB     00:00     
extras/primary_db                                                                                                                                                                           |  19 kB     00:00     
updates                                                                                                                                                                                     | 3.4 kB     00:00     
updates/primary_db                                                                                                                                                                          | 1.4 MB     00:00     
Setting up Install Process
Resolving Dependencies
--> Running transaction check
---> Package puppet.noarch 0:2.7.23-1.el6 will be installed
--> Processing Dependency: facter < 1:2.0 for package: puppet-2.7.23-1.el6.noarch
--> Processing Dependency: ruby(abi) >= 1.8 for package: puppet-2.7.23-1.el6.noarch
--> Processing Dependency: ruby >= 1.8.5 for package: puppet-2.7.23-1.el6.noarch
--> Processing Dependency: facter >= 1.5 for package: puppet-2.7.23-1.el6.noarch
--> Processing Dependency: ruby-shadow for package: puppet-2.7.23-1.el6.noarch
--> Processing Dependency: ruby-augeas for package: puppet-2.7.23-1.el6.noarch
--> Processing Dependency: ruby(selinux) for package: puppet-2.7.23-1.el6.noarch
--> Processing Dependency: /usr/bin/ruby for package: puppet-2.7.23-1.el6.noarch
--> Running transaction check
---> Package facter.x86_64 0:1.6.18-3.el6 will be installed
--> Processing Dependency: virt-what for package: facter-1.6.18-3.el6.x86_64
--> Processing Dependency: pciutils for package: facter-1.6.18-3.el6.x86_64
--> Processing Dependency: dmidecode for package: facter-1.6.18-3.el6.x86_64
---> Package libselinux-ruby.x86_64 0:2.0.94-5.3.el6_4.1 will be installed
---> Package ruby.x86_64 0:1.8.7.352-13.el6 will be installed
---> Package ruby-augeas.x86_64 0:0.4.1-1.el6 will be installed
--> Processing Dependency: augeas-libs >= 0.8.0 for package: ruby-augeas-0.4.1-1.el6.x86_64
--> Processing Dependency: libaugeas.so.0(AUGEAS_0.8.0)(64bit) for package: ruby-augeas-0.4.1-1.el6.x86_64
--> Processing Dependency: libaugeas.so.0(AUGEAS_0.12.0)(64bit) for package: ruby-augeas-0.4.1-1.el6.x86_64
--> Processing Dependency: libaugeas.so.0(AUGEAS_0.11.0)(64bit) for package: ruby-augeas-0.4.1-1.el6.x86_64
--> Processing Dependency: libaugeas.so.0(AUGEAS_0.10.0)(64bit) for package: ruby-augeas-0.4.1-1.el6.x86_64
--> Processing Dependency: libaugeas.so.0(AUGEAS_0.1.0)(64bit) for package: ruby-augeas-0.4.1-1.el6.x86_64
--> Processing Dependency: libaugeas.so.0()(64bit) for package: ruby-augeas-0.4.1-1.el6.x86_64
---> Package ruby-libs.x86_64 0:1.8.7.352-13.el6 will be installed
--> Processing Dependency: libreadline.so.5()(64bit) for package: ruby-libs-1.8.7.352-13.el6.x86_64
---> Package ruby-shadow.x86_64 0:1.4.1-13.el6 will be installed
--> Running transaction check
---> Package augeas-libs.x86_64 0:1.0.0-5.el6_5.1 will be installed
---> Package compat-readline5.x86_64 0:5.2-17.1.el6 will be installed
---> Package dmidecode.x86_64 1:2.11-2.el6 will be installed
---> Package pciutils.x86_64 0:3.1.10-2.el6 will be installed
---> Package virt-what.x86_64 0:1.11-1.2.el6 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

===================================================================================================================================================================================================================
 Package                                                Arch                                         Version                                                   Repository                                     Size
===================================================================================================================================================================================================================
Installing:
 puppet                                                 noarch                                       2.7.23-1.el6                                              epel                                          3.0 M
Installing for dependencies:
 augeas-libs                                            x86_64                                       1.0.0-5.el6_5.1                                           updates                                       309 k
 compat-readline5                                       x86_64                                       5.2-17.1.el6                                              base                                          130 k
 dmidecode                                              x86_64                                       1:2.11-2.el6                                              base                                           71 k
 facter                                                 x86_64                                       1.6.18-3.el6                                              epel                                           62 k
 libselinux-ruby                                        x86_64                                       2.0.94-5.3.el6_4.1                                        base                                           99 k
 pciutils                                               x86_64                                       3.1.10-2.el6                                              base                                           85 k
 ruby                                                   x86_64                                       1.8.7.352-13.el6                                          updates                                       534 k
 ruby-augeas                                            x86_64                                       0.4.1-1.el6                                               epel                                           21 k
 ruby-libs                                              x86_64                                       1.8.7.352-13.el6                                          updates                                       1.6 M
 ruby-shadow                                            x86_64                                       1.4.1-13.el6                                              epel                                           11 k
 virt-what                                              x86_64                                       1.11-1.2.el6                                              base                                           24 k

Transaction Summary
===================================================================================================================================================================================================================
Install      12 Package(s)

Total download size: 6.0 M
Installed size: 15 M
Downloading Packages:
(1/12): augeas-libs-1.0.0-5.el6_5.1.x86_64.rpm                                                                                                                                              | 309 kB     00:00     
(2/12): compat-readline5-5.2-17.1.el6.x86_64.rpm                                                                                                                                            | 130 kB     00:00     
(3/12): dmidecode-2.11-2.el6.x86_64.rpm                                                                                                                                                     |  71 kB     00:00     
(4/12): facter-1.6.18-3.el6.x86_64.rpm                                                                                                                                                      |  62 kB     00:00     
(5/12): libselinux-ruby-2.0.94-5.3.el6_4.1.x86_64.rpm                                                                                                                                       |  99 kB     00:00     
(6/12): pciutils-3.1.10-2.el6.x86_64.rpm                                                                                                                                                    |  85 kB     00:00     
(7/12): puppet-2.7.23-1.el6.noarch.rpm                                                                                                                                                      | 3.0 MB     00:00     
(8/12): ruby-1.8.7.352-13.el6.x86_64.rpm                                                                                                                                                    | 534 kB     00:00     
(9/12): ruby-augeas-0.4.1-1.el6.x86_64.rpm                                                                                                                                                  |  21 kB     00:00     
(10/12): ruby-libs-1.8.7.352-13.el6.x86_64.rpm                                                                                                                                              | 1.6 MB     00:00     
(11/12): ruby-shadow-1.4.1-13.el6.x86_64.rpm                                                                                                                                                |  11 kB     00:00     
(12/12): virt-what-1.11-1.2.el6.x86_64.rpm                                                                                                                                                  |  24 kB     00:00     
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                                              9.8 MB/s | 6.0 MB     00:00     
warning: rpmts_HdrFromFdno: Header V3 RSA/SHA256 Signature, key ID 0608b895: NOKEY
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
Importing GPG key 0x0608B895:
 Userid : EPEL (6) <epel@fedoraproject.org>
 Package: epel-release-6-8.noarch (installed)
 From   : /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
Running rpm_check_debug
Running Transaction Test
Transaction Test Succeeded
Running Transaction
  Installing : 1:dmidecode-2.11-2.el6.x86_64                                                                                                                                                                  1/12 
  Installing : virt-what-1.11-1.2.el6.x86_64                                                                                                                                                                  2/12 
  Installing : augeas-libs-1.0.0-5.el6_5.1.x86_64                                                                                                                                                             3/12 
  Installing : compat-readline5-5.2-17.1.el6.x86_64                                                                                                                                                           4/12 
  Installing : ruby-libs-1.8.7.352-13.el6.x86_64                                                                                                                                                              5/12 
  Installing : ruby-1.8.7.352-13.el6.x86_64                                                                                                                                                                   6/12 
  Installing : ruby-augeas-0.4.1-1.el6.x86_64                                                                                                                                                                 7/12 
  Installing : ruby-shadow-1.4.1-13.el6.x86_64                                                                                                                                                                8/12 
  Installing : pciutils-3.1.10-2.el6.x86_64                                                                                                                                                                   9/12 
  Installing : facter-1.6.18-3.el6.x86_64                                                                                                                                                                    10/12 
  Installing : libselinux-ruby-2.0.94-5.3.el6_4.1.x86_64                                                                                                                                                     11/12 
  Installing : puppet-2.7.23-1.el6.noarch                                                                                                                                                                    12/12 
  Verifying  : libselinux-ruby-2.0.94-5.3.el6_4.1.x86_64                                                                                                                                                      1/12 
  Verifying  : ruby-augeas-0.4.1-1.el6.x86_64                                                                                                                                                                 2/12 
  Verifying  : facter-1.6.18-3.el6.x86_64                                                                                                                                                                     3/12 
  Verifying  : ruby-libs-1.8.7.352-13.el6.x86_64                                                                                                                                                              4/12 
  Verifying  : puppet-2.7.23-1.el6.noarch                                                                                                                                                                     5/12 
  Verifying  : 1:dmidecode-2.11-2.el6.x86_64                                                                                                                                                                  6/12 
  Verifying  : pciutils-3.1.10-2.el6.x86_64                                                                                                                                                                   7/12 
  Verifying  : ruby-1.8.7.352-13.el6.x86_64                                                                                                                                                                   8/12 
  Verifying  : virt-what-1.11-1.2.el6.x86_64                                                                                                                                                                  9/12 
  Verifying  : compat-readline5-5.2-17.1.el6.x86_64                                                                                                                                                          10/12 
  Verifying  : ruby-shadow-1.4.1-13.el6.x86_64                                                                                                                                                               11/12 
  Verifying  : augeas-libs-1.0.0-5.el6_5.1.x86_64                                                                                                                                                            12/12 

Installed:
  puppet.noarch 0:2.7.23-1.el6                                                                                                                                                                                     

Dependency Installed:
  augeas-libs.x86_64 0:1.0.0-5.el6_5.1     compat-readline5.x86_64 0:5.2-17.1.el6     dmidecode.x86_64 1:2.11-2.el6        facter.x86_64 0:1.6.18-3.el6            libselinux-ruby.x86_64 0:2.0.94-5.3.el6_4.1    
  pciutils.x86_64 0:3.1.10-2.el6           ruby.x86_64 0:1.8.7.352-13.el6             ruby-augeas.x86_64 0:0.4.1-1.el6     ruby-libs.x86_64 0:1.8.7.352-13.el6     ruby-shadow.x86_64 0:1.4.1-13.el6              
  virt-what.x86_64 0:1.11-1.2.el6         

Complete!
```

Next, I'll modify the /etc/hosts file and /etc/sysconfig/puppet file to specify my puppet master (puppet server).

```bash
[root@puppet ~]# history | grep vi
    2  vi /etc/hosts
    3  vi /etc/sysconfig/puppet 
    4  history | grep vi
[root@puppet ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

172.17.0.5	puppet.test

172.17.0.1	puppetmaster
[root@puppet ~]# cat /etc/sysconfig/puppet 
# The puppetmaster server
PUPPET_SERVER=puppetmaster

# If you wish to specify the port to connect to do so here
#PUPPET_PORT=8140

# Where to log to. Specify syslog to send log messages to the system log.
#PUPPET_LOG=/var/log/puppet/puppet.log

# You may specify other parameters to the puppet client here
#PUPPET_EXTRA_OPTS=--waitforcert=500
```

After that, I need to generate a ssl cert from the puppet agent to the puppet master.

```bash
root@puppet ~]# puppet agent --test --server puppetmaster
info: Creating a new SSL key for puppet.test
info: Caching certificate for ca
info: Creating a new SSL certificate request for puppet.test
info: Certificate Request fingerprint (md5): 1D:89:5C:D3:DD:A4:47:53:5B:A4:A2:BB:17:6A:55:B0
Exiting; no certificate found and waitforcert is disabled
[root@puppet ~]# 
```

When the key has been generated, hop on the puppetmaster server and sign the key.

```bash
[root@puppetmaster ~]# puppet cert list
  "puppet.test" (1D:89:5C:D3:DD:A4:47:53:5B:A4:A2:BB:17:6A:55:B0)
[root@puppetmaster ~]# puppet cert sign puppet.test
notice: Signed certificate request for puppet.test
notice: Removing file Puppet::SSL::CertificateRequest puppet.test at '/var/lib/puppet/ssl/ca/requests/puppet.test.pem'
```

Now hop back onto the puppet agent and test the newly sign certificate. If all is good, it should push your default config to the server. For brevity, I'll leave out the output of everything that it set up.

```bash
[root@puppet ~]# puppet agent --test --server puppetmaster
info: Caching certificate for puppet.test
info: Caching certificate_revocation_list for ca
info: Caching catalog for puppet.test
info: Applying configuration version '1392021450'
……..
info: Creating state file /var/lib/puppet/state/state.yaml
notice: Finished catalog run in 19.31 seconds
```

Finally, the last thing to do is start the puppet service, on the agent, and verify that its running.

```bash
[root@puppet ~]# service puppet start
Starting puppet:                                           [  OK  ]
[root@puppet ~]# chkconfig puppet on
[root@puppet ~]# ps ax | grep puppet
 3330 ?        Ss     0:01 /usr/bin/ruby /usr/sbin/puppetd --server=puppetmaster
 3538 pts/0    S+     0:00 grep puppet
```

Now you should have a fully functional puppet installation. Now you can create puppet manifests to automate your server(s) even more!
