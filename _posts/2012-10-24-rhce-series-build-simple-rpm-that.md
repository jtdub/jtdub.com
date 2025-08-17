---
layout: post
title: 'RHCE Series: Build a simple RPM that packages a single file.'
date: '2012-10-24'
author: jtdub
tags:
- Linux
- RHCE Study Notes
- OpenNHRP
- RPM
- packetgeek.net
---


<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>

Alright, so this is a little more in depth than creating a simple package, but I figured I could full-fill the Red Hat requirement and create a little bit of documentation on how to create the rpm for OpenNHRP in one swoop. :)

```bash
[root@build ~]# yum install rpmdevtools
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: centos.mirror.lstn.net
 * extras: centos.mirror.lstn.net
 * updates: centos.mirror.lstn.net

...

Installed:
  rpmdevtools.noarch 0:7.5-1.el6                                                                                            
Complete!

[root@build ~]# adduser rpmuser
[root@build ~]# su - rpmuser
[rpmuser@build ~]$ rpmdev-setuptree 
[rpmuser@build ~]$ ls
rpmbuild
[rpmuser@build ~]$ ls rpmbuild/
BUILD  RPMS  SOURCES  SPECS  SRPMS
[rpmuser@build ~]$ cd rpmbuild/SOURCES/
[rpmuser@build SOURCES]$ ls
opennhrp-0.13.1.tar.bz2

[root@build ~]# yum -y install c-ares-devel
[root@build ~]# yum -y groupinstall "Development Tools"

[rpmuser@build rpmbuild]$ cd SPECS/
[rpmuser@build SPECS]$ 
[rpmuser@build SPECS]$ vim opennhrp.spec
[rpmuser@build SPECS]$ cat opennhrp.spec 
Name:  opennhrp
Version: 0.13.1
Release: 1%{?dist}
Summary: OpenNHRP implements NBMA Next Hop Resolution Protocol (as defined in RFC 2332). It makes it possible to create dynamic multipoint VPN Linux router using NHRP, GRE and IPsec. It aims to be Cisco DMVPN compatible.

#Group:  
License: GNU GPL
URL:  http://sourceforge.net/projects/opennhrp
Source0: ~/rpmbuild/SOURCES/opennhrp-0.13.1.tar.bz2 
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires: 
#Requires: 

%description


%prep
%setup -q
touch ~/rpmbuild/BUILD/%{name}-%{version}/configure && chmod +x ~/rpmbuild/BUILD/%{name}-%{version}/configure 

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc
%config(noreplace) /etc/opennhrp/*
/usr/sbin/opennhrp
/usr/sbin/opennhrpctl
/usr/share/doc/opennhrp/README
/usr/share/man/man5/*
/usr/share/man/man8/*

%changelog


[rpmuser@build SPECS]$ rpmbuild -bb opennhrp.spec

[rpmuser@build SPECS]$ cd ../RPMS/
[rpmuser@build RPMS]$ ls
x86_64
[rpmuser@build RPMS]$ cd x86_64/
[rpmuser@build x86_64]$ ls
opennhrp-0.13.1-1.el6.x86_64.rpm  opennhrp-debuginfo-0.13.1-1.el6.x86_64.rpm
```
