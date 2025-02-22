---
layout: post
title: 'RHCE Series: Configure SELinux to support the service.'
date: '2012-10-25'
author: jtdub
tags:
- SELinux
- Linux
- RHCE Study Notes
- packetgeek.net
---

* Every process or object has a SELinux context:
  * identity:role:domain/type
* The SELinux policy controls:
  * What identities can use which roles
  * What roles can enter which domains
  * What domains can access which types
* To change the context of a file, you can use the chcon command:
  * chcon -R --reference=/var/www/html
* To restore the default labeling from the policy and apply the contexts to file:
  * restorecon -R
* To change the SELinux mode during boot, you can pass the ‘enforcing=0’ option to the kernel in GRUB.
  * sestatus
  * setenforce | getenforce
  * policycoreutils
  * setroubleshoot
  * system-config-selinux <- part of policycoreutils-gui in RHEL.
  * setsebool | getsebool
  * chcon
  * restorecon
When troubleshooting potential SELinux issues, you can turn off SELinux while troubleshooting.

```bash
[root@server1 ~]# sestatus 
SELinux status:                 enabled
SELinuxfs mount:                /selinux
Current mode:                   enforcing
Mode from config file:          enforcing
Policy version:                 24
Policy from config file:        targeted
[root@server1 ~]# curl -I localhost
HTTP/1.1 403 Forbidden
Date: Fri, 26 Oct 2012 13:23:10 GMT
Server: Apache/2.2.15 (CentOS)
Accept-Ranges: bytes
Content-Length: 5039
Connection: close
Content-Type: text/html; charset=UTF-8

[root@server1 ~]# setenforce 0
[root@server1 ~]# curl -I localhost
HTTP/1.1 200 OK
Date: Fri, 26 Oct 2012 13:23:18 GMT
Server: Apache/2.2.15 (CentOS)
Last-Modified: Fri, 26 Oct 2012 13:22:45 GMT
ETag: "4401a-0-4ccf637181f21"
Accept-Ranges: bytes
Connection: close
Content-Type: text/html; charset=UTF-8

[root@server1 ~]# ls -Z /var/www/html/
-rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 index.html
[root@server1 ~]# chcon --reference=/var/www/html/ /var/www/html/index.html 
[root@server1 ~]# ls -Z /var/www/html/
-rw-r--r--. root root system_u:object_r:httpd_sys_content_t:s0 index.html
[root@server1 ~]# setenforce 1
[root@server1 ~]# curl -I localhost
HTTP/1.1 200 OK
Date: Fri, 26 Oct 2012 13:24:06 GMT
Server: Apache/2.2.15 (CentOS)
Last-Modified: Fri, 26 Oct 2012 13:22:45 GMT
ETag: "4401a-0-4ccf637181f21"
Accept-Ranges: bytes
Connection: close
Content-Type: text/html; charset=UTF-8
```
You can also use the 'restorecon' command to restore default context values to the contents of a folder or file.

You can use booleans to enable or disable specific actions. To view the booleans and their status, use the getsebool command.

```bash
[root@server1 ~]# getsebool -a
abrt_anon_write --> off
abrt_handle_event --> off
allow_console_login --> on
allow_cvs_read_shadow --> off
allow_daemons_dump_core --> on
allow_daemons_use_tcp_wrapper --> off
allow_daemons_use_tty --> on
allow_domain_fd_use --> on
allow_execheap --> off
allow_execmem --> on
allow_execmod --> on
allow_execstack --> on
allow_ftpd_anon_write --> off
allow_ftpd_full_access --> off
allow_ftpd_use_cifs --> off
allow_ftpd_use_nfs --> off
allow_gssd_read_tmp --> on
allow_guest_exec_content --> off
allow_httpd_anon_write --> off
allow_httpd_mod_auth_ntlm_winbind --> off
allow_httpd_mod_auth_pam --> off
allow_httpd_sys_script_anon_write --> off
allow_java_execstack --> off
allow_kerberos --> on
allow_mount_anyfile --> on
allow_mplayer_execstack --> off
allow_nsplugin_execmem --> on
allow_polyinstantiation --> off
allow_postfix_local_write_mail_spool --> on
allow_ptrace --> off
allow_rsync_anon_write --> off
allow_saslauthd_read_shadow --> off
allow_smbd_anon_write --> off
allow_ssh_keysign --> off
allow_staff_exec_content --> on
allow_sysadm_exec_content --> on
allow_unconfined_nsplugin_transition --> off
allow_user_exec_content --> on
allow_user_mysql_connect --> off
allow_user_postgresql_connect --> off
allow_write_xshm --> off
allow_xguest_exec_content --> off
allow_xserver_execmem --> off
allow_ypbind --> off
allow_zebra_write_config --> on
authlogin_radius --> off
cdrecord_read_content --> off
clamd_use_jit --> off
cobbler_anon_write --> off
cobbler_can_network_connect --> off
cobbler_use_cifs --> off
cobbler_use_nfs --> off
condor_domain_can_network_connect --> off
cron_can_relabel --> off
dhcpc_exec_iptables --> off
domain_kernel_load_modules --> off
exim_can_connect_db --> off
exim_manage_user_files --> off
exim_read_user_files --> off
fcron_crond --> off
fenced_can_network_connect --> off
fenced_can_ssh --> off
ftp_home_dir --> off
ftpd_connect_db --> off
ftpd_use_passive_mode --> off
git_cgit_read_gitosis_content --> off
git_session_bind_all_unreserved_ports --> off
git_system_enable_homedirs --> off
git_system_use_cifs --> off
git_system_use_nfs --> off
global_ssp --> off
gpg_agent_env_file --> off
gpg_web_anon_write --> off
httpd_builtin_scripting --> on
httpd_can_check_spam --> off
httpd_can_network_connect --> off
httpd_can_network_connect_cobbler --> off
httpd_can_network_connect_db --> off
httpd_can_network_memcache --> off
httpd_can_network_relay --> off
httpd_can_sendmail --> off
httpd_dbus_avahi --> on
httpd_enable_cgi --> on
httpd_enable_ftp_server --> off
httpd_enable_homedirs --> off
httpd_execmem --> off
httpd_manage_ipa --> off
httpd_read_user_content --> off
httpd_setrlimit --> off
httpd_ssi_exec --> off
httpd_tmp_exec --> off
httpd_tty_comm --> on
httpd_unified --> on
httpd_use_cifs --> off
httpd_use_gpg --> off
httpd_use_nfs --> on
httpd_use_openstack --> off
icecast_connect_any --> off
init_upstart --> on
irssi_use_full_network --> off
logging_syslogd_can_sendmail --> off
mmap_low_allowed --> off
mozilla_read_content --> off
mysql_connect_any --> off
named_write_master_zones --> off
ncftool_read_user_content --> off
nscd_use_shm --> on
nsplugin_can_network --> on
openvpn_enable_homedirs --> on
piranha_lvs_can_network_connect --> off
pppd_can_insmod --> off
pppd_for_user --> off
privoxy_connect_any --> on
puppet_manage_all_files --> off
puppetmaster_use_db --> off
qemu_full_network --> on
qemu_use_cifs --> on
qemu_use_comm --> off
qemu_use_nfs --> on
qemu_use_usb --> on
racoon_read_shadow --> off
rgmanager_can_network_connect --> off
rsync_client --> off
rsync_export_all_ro --> off
rsync_use_cifs --> off
rsync_use_nfs --> off
samba_create_home_dirs --> off
samba_domain_controller --> off
samba_enable_home_dirs --> off
samba_export_all_ro --> off
samba_export_all_rw --> off
samba_run_unconfined --> off
samba_share_fusefs --> off
samba_share_nfs --> off
sanlock_use_nfs --> off
sanlock_use_samba --> off
secure_mode --> off
secure_mode_insmod --> off
secure_mode_policyload --> off
sepgsql_enable_users_ddl --> on
sepgsql_unconfined_dbadm --> on
sge_domain_can_network_connect --> off
sge_use_nfs --> off
smartmon_3ware --> off
spamassassin_can_network --> off
spamd_enable_home_dirs --> on
squid_connect_any --> on
squid_use_tproxy --> off
ssh_chroot_rw_homedirs --> off
ssh_sysadm_login --> off
telepathy_tcp_connect_generic_network_ports --> off
tftp_anon_write --> off
tor_bind_all_unreserved_ports --> off
unconfined_login --> on
unconfined_mmap_zero_ignore --> off
unconfined_mozilla_plugin_transition --> off
use_fusefs_home_dirs --> off
use_lpd_server --> off
use_nfs_home_dirs --> on
use_samba_home_dirs --> off
user_direct_dri --> on
user_direct_mouse --> off
user_ping --> on
user_rw_noexattrfile --> on
user_setrlimit --> on
user_tcp_server --> off
user_ttyfile_stat --> off
varnishd_connect_any --> off
vbetool_mmap_zero_ignore --> off
virt_use_comm --> off
virt_use_fusefs --> off
virt_use_nfs --> off
virt_use_samba --> off
virt_use_sanlock --> off
virt_use_sysfs --> on
virt_use_usb --> on
virt_use_xserver --> off
webadm_manage_user_files --> off
webadm_read_user_files --> off
wine_mmap_zero_ignore --> off
xdm_exec_bootloader --> off
xdm_sysadm_login --> off
xen_use_nfs --> off
xguest_connect_network --> on
xguest_mount_media --> on
xguest_use_bluetooth --> on
xserver_object_manager --> off
```

To change a boolean, you can use the setsebool command.

```bash
[root@server1 ~]# getsebool httpd_use_nfs
httpd_use_nfs --> off
[root@server1 ~]# setsebool -P httpd_use_nfs=1
[root@server1 ~]# getsebool httpd_use_nfs
httpd_use_nfs --> on
[root@server1 ~]#
```
