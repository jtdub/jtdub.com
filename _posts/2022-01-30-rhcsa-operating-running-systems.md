---
layout: post
title: 'RHCSA Version 8: Operating Running Systems'
date: '2022-01-30'
author: jtdub
tags:
- packetgeek.net 
- RHCSA Study Notes
- Linux
- Redhat
---

### Boot, reboot, and shut down a system normally

There are multiple ways to reboot and shutdown a system. Those are covered below.

- `shutdown`

```bash
[root@rhel-server ~]# shutdown --help
shutdown [OPTIONS...] [TIME] [WALL...]

Shut down the system.

     --help      Show this help
  -H --halt      Halt the machine
  -P --poweroff  Power-off the machine
  -r --reboot    Reboot the machine
  -h             Equivalent to --poweroff, overridden by --halt
  -k             Don't halt/power-off/reboot, just send warnings
     --no-wall   Don't send wall message before halt/power-off/reboot
  -c             Cancel a pending shutdown
``` 

- `reboot`

```bash
[root@rhel-server ~]# reboot --help
reboot [OPTIONS...] [ARG]

Reboot the system.

     --help      Show this help
     --halt      Halt the machine
  -p --poweroff  Switch off the machine
     --reboot    Reboot the machine
  -f --force     Force immediate halt/power-off/reboot
  -w --wtmp-only Don't halt/power-off/reboot, just write wtmp record
  -d --no-wtmp   Don't write wtmp record
     --no-wall   Don't send wall message before halt/power-off/reboot
```

- `poweroff`

```bash
[root@rhel-server ~]# poweroff --help
poweroff [OPTIONS...]

Power off the system.

     --help      Show this help
     --halt      Halt the machine
  -p --poweroff  Switch off the machine
     --reboot    Reboot the machine
  -f --force     Force immediate halt/power-off/reboot
  -w --wtmp-only Don't halt/power-off/reboot, just write wtmp record
  -d --no-wtmp   Don't write wtmp record
     --no-wall   Don't send wall message before halt/power-off/reboot
```

### Boot systems into different targets manually

You can list the system targets with `systemctl list-units --type=target`.

```bash
[root@rhel-server ~]# systemctl list-units --type=target
UNIT                   LOAD   ACTIVE SUB    DESCRIPTION
basic.target           loaded active active Basic System
cryptsetup.target      loaded active active Local Encrypted Volumes
getty.target           loaded active active Login Prompts
graphical.target       loaded active active Graphical Interface
local-fs-pre.target    loaded active active Local File Systems (Pre)
local-fs.target        loaded active active Local File Systems
multi-user.target      loaded active active Multi-User System
network-online.target  loaded active active Network is Online
network-pre.target     loaded active active Network (Pre)
network.target         loaded active active Network
nfs-client.target      loaded active active NFS client services
nss-user-lookup.target loaded active active User and Group Name Lookups
paths.target           loaded active active Paths
remote-fs-pre.target   loaded active active Remote File Systems (Pre)
remote-fs.target       loaded active active Remote File Systems
rpc_pipefs.target      loaded active active rpc_pipefs.target
rpcbind.target         loaded active active RPC Port Mapper
slices.target          loaded active active Slices
sockets.target         loaded active active Sockets
sound.target           loaded active active Sound Card
sshd-keygen.target     loaded active active sshd-keygen.target
swap.target            loaded active active Swap
sysinit.target         loaded active active System Initialization
timers.target          loaded active active Timers

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

24 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
```

You can list the default system target with `systemctl get-default`.

```bash
[root@rhel-server ~]# systemctl get-default
graphical.target
```

You can change the default system target with `systemctl set-default <target>`

```bash
[root@rhel-server ~]# systemctl set-default multi-user.target
Removed /etc/systemd/system/default.target.
Created symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/multi-user.target.
```

You can set the system target at boot time by modifying GRUB and adding `systemd.unit=<target>` at the end of the line that starts with `linux`. *Example*: `systemd.unit=rescue.target`.

To change the system target live, use `systemctl isolate <target>`.

```bash
[root@rhel-server ~]# systemctl isolate multi-user.target
```

### Interrupt the boot process in order to gain access to a system

TLDR; 
1. Reboot
2. At Grub Menu, select rescue kernel and press `e`
3. At the end of the `linux` kernel line, remove `rhgb quiet` and add `rd.break enforcing=0`

In order to recover the root password of a system, you must have console access to the server in order to modify the boot loader to boot into single user mode. 

When you're first prompted with the boot menu, press down down arrow on the keyboard to stop the boot timer. Then scroll through your boot menu options until the rescue kernel is highlighted. With the rescue kernel highlighted, press the `e` button to edit the rescue boot options.

<img src="/images/rhcsa/grub-menu1.png" alt="Grub Menu" width=600>

In the Grub edit menu, locate the line that starts with `linux`. The command may span multiple lines and will end with `rhgb quiet`. Go to the end of the line.

<img src="/images/rhcsa/grub-menu2.png" alt="Grub Menu: Edit" width=600>

Remove `rhgb quiet` from the command and add `rd.break enforcing=0`. Once complete, press the `Ctrl-X` key sequence to continue booting to the rescue mode.

<img src="/images/rhcsa/grub-menu3.png" alt="Grub Menu:Single User Mode" width=600>

At this point, the system will boot into single user mode and will boot into a `switch_root:/#` prompt. The `/sysroot` filesystem will mount in read-only mode. This can be verified by executing: `mount | grep /sysroot`. You'll need to remount the filesystem as read-write. To to this execute, `mount -o rw,remount /sysroot`. The `mount | grep /sysroot` command will verify that it's mounted as read-write.

With the system booted into single user mode and the `/sysroot` volume mounted with read-write permissions, you will need to change the root to /sysroot. This can be done by executing `chroot /sysroot`. Once completed, execute the `passwd` command to change the root password. Once completed type `exit` twice and the system will reboot. At this point, you will be able to login with the new root password.

When the system has booted back to normal, the security context must be restored for the shadow file. This can be done by executing `restorecon /etc/shadow`. `ls -Z /etc/shadow` can be used to view the current security context.

### Identify CPU/memory intensive processes and kill processes

The `top` command can be used to identify CPU/memory intensive processes. In the `top` command, the `m` key can be pressed to toggle between processes using least and most memory. The `c` key can be pressed to toggle between processes using the least and most cpu usage. The `1` key can be used to toggle between showing the aggregate CPU usage and CPU usage on individual CPU's.

```
top - 21:00:39 up 19 days,  9:08,  2 users,  load average: 0.00, 0.00, 0.00
Tasks: 155 total,   1 running, 154 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   3736.5 total,   1628.1 free,    315.5 used,   1792.9 buff/cache
MiB Swap:   2048.0 total,   2047.2 free,      0.8 used.   3155.7 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 373934 root      20   0       0      0      0 I   0.3   0.0   0:00.96 kworker/0:1-events
      1 root      20   0  183712  14068   9076 S   0.0   0.4   0:14.09 systemd
      2 root      20   0       0      0      0 S   0.0   0.0   0:00.24 kthreadd
      3 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_gp
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_par_gp
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker/0:0H-events_highpri
      9 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 mm_percpu_wq
     10 root      20   0       0      0      0 S   0.0   0.0   0:01.51 ksoftirqd/0
```

The `kill` command can be used to kill processes.

```
[root@rhel-server ~]# kill --help
kill: kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... or kill -l [sigspec]
    Send a signal to a job.

    Send the processes identified by PID or JOBSPEC the signal named by
    SIGSPEC or SIGNUM.  If neither SIGSPEC nor SIGNUM is present, then
    SIGTERM is assumed.

    Options:
      -s sig	SIG is a signal name
      -n sig	SIG is a signal number
      -l	list the signal names; if arguments follow `-l' they are
    		assumed to be signal numbers for which names should be listed
      -L	synonym for -l

    Kill is a shell builtin for two reasons: it allows job IDs to be used
    instead of process IDs, and allows processes to be killed if the limit
    on processes that you can create is reached.

    Exit Status:
    Returns success unless an invalid option is given or an error occurs.
```

`kill -9 <pid>` to kill a process.

### Adjust process scheduling

The `nice` command can be used to adjust process scheduling and priority. Nice values can be between `-20 through +19`. 

To use `nice`, you use execute it as a prerequisite to starting a command. Example: `nice -n 10 sleep 10&`

```bash
[root@rhel-server ~]# nice -n 10 sleep 60&
[1] 374487
[root@rhel-server ~]# ps -lp $(pgrep sleep)
F S   UID     PID    PPID  C PRI  NI ADDR SZ WCHAN  TTY        TIME CMD
0 S     0  374486  298049  0  80   0 -  1827 hrtime ?          0:00 sleep 60
0 S     0  374487  373261  0  90  10 -  1827 hrtime pts/0      0:00 sleep 60
```

The `renice` command can be used to change the priority of a currently running command.

```bash
[root@rhel-server ~]# sleep 60&
[1] 374524
[root@rhel-server ~]# ps -lp $(pgrep sleep)
F S   UID     PID    PPID  C PRI  NI ADDR SZ WCHAN  TTY        TIME CMD
0 S     0  374517  298049  0  80   0 -  1827 hrtime ?          0:00 sleep 60
0 S     0  374524  373261  0  80   0 -  1827 hrtime pts/0      0:00 sleep 60
[root@rhel-server ~]# renice -n 10 374524
374524 (process ID) old priority 0, new priority 10
[root@rhel-server ~]# ps -lp $(pgrep sleep)
F S   UID     PID    PPID  C PRI  NI ADDR SZ WCHAN  TTY        TIME CMD
0 S     0  374517  298049  0  80   0 -  1827 hrtime ?          0:00 sleep 60
0 S     0  374524  373261  0  90  10 -  1827 hrtime pts/0      0:00 sleep 60
```

### Manage tuning profiles

You can see the current tuning profile:

```bash
[root@rhel-server ~]# tuned-adm active
Current active profile: virtual-guest
```

Retrieve a list of tuning profiles:

```bash
[root@rhel-server ~]# tuned-adm list
Available profiles:
- accelerator-performance     - Throughput performance based tuning with disabled higher latency STOP states
- balanced                    - General non-specialized tuned profile
- desktop                     - Optimize for the desktop use-case
- hpc-compute                 - Optimize for HPC compute workloads
- intel-sst                   - Configure for Intel Speed Select Base Frequency
- latency-performance         - Optimize for deterministic performance at the cost of increased power consumption
- network-latency             - Optimize for deterministic performance at the cost of increased power consumption, focused on low latency network performance
- network-throughput          - Optimize for streaming network throughput, generally only necessary on older CPUs or 40G+ networks
- optimize-serial-console     - Optimize for serial console use.
- powersave                   - Optimize for low power consumption
- throughput-performance      - Broadly applicable tuning that provides excellent performance across a variety of common server workloads
- virtual-guest               - Optimize for running inside a virtual guest
- virtual-host                - Optimize for running KVM guests
Current active profile: virtual-guest
```

Change the tuning profile:

```bash
[root@rhel-server ~]# tuned-adm profile desktop
[root@rhel-server ~]#
```

### Locate and interpret system log files and journals

System logs are located in `/var/log`. Journal logs exist only in memory. They can be viewed via `systemctl status` or `journalctl`.

The `logger` command can be used to test logging functionality.

```bash
[root@rhel-server ~]# logger -p local0.info "test message" && tail -n 1 /var/log/messages
Jan 19 15:15:18 rhel-server jtdub[154526]: test message

[root@rhel-server ~]# journalctl -n3
-- Logs begin at Mon 2022-01-10 11:52:12 EST, end at Wed 2022-01-19 15:15:31 EST. --
Jan 19 15:15:15 rhel-server jtdub[154524]: test message
Jan 19 15:15:18 rhel-server jtdub[154526]: test message
Jan 19 15:15:31 rhel-server jtdub[154528]: test message
```

Rsyslogd is a syslog daemon and is what is used in RHEL for logging.

Custom syslog parameters can be created by adding `.conf` files in `/etc/rsyslog.d/`.

```bash
[root@rhel-server log]# grep 'rsyslog.d' /etc/rsyslog.conf
# Include all config files in /etc/rsyslog.d/
include(file="/etc/rsyslog.d/*.conf" mode="optional")
```

After adding a custom log configuration, restart rsyslogd: `systemctl restart rsyslog`.

`man syslog` for logging facilities and severities.

### Preserve system journals

The journal logs aren't application specific. They encompass all system logs. The `journalctl` command is used to display the system journals.

```bash
[root@rhel-server ~]# journalctl --help
journalctl [OPTIONS...] [MATCHES...]

Query the journal.

Options:
     --system                Show the system journal
     --user                  Show the user journal for the current user
  -M --machine=CONTAINER     Operate on local container
  -S --since=DATE            Show entries not older than the specified date
  -U --until=DATE            Show entries not newer than the specified date
  -c --cursor=CURSOR         Show entries starting at the specified cursor
     --after-cursor=CURSOR   Show entries after the specified cursor
     --show-cursor           Print the cursor after all the entries
  -b --boot[=ID]             Show current boot or the specified boot
     --list-boots            Show terse information about recorded boots
  -k --dmesg                 Show kernel message log from the current boot
  -u --unit=UNIT             Show logs from the specified unit
     --user-unit=UNIT        Show logs from the specified user unit
  -t --identifier=STRING     Show entries with the specified syslog identifier
  -p --priority=RANGE        Show entries with the specified priority
  -g --grep=PATTERN          Show entries with MESSAGE matching PATTERN
     --case-sensitive[=BOOL] Force case sensitive or insenstive matching
  -e --pager-end             Immediately jump to the end in the pager
  -f --follow                Follow the journal
  -n --lines[=INTEGER]       Number of journal entries to show
     --no-tail               Show all lines, even in follow mode
  -r --reverse               Show the newest entries first
  -o --output=STRING         Change journal output mode (short, short-precise,
                               short-iso, short-iso-precise, short-full,
                               short-monotonic, short-unix, verbose, export,
                               json, json-pretty, json-sse, cat, with-unit)
     --output-fields=LIST    Select fields to print in verbose/export/json modes
     --utc                   Express time in Coordinated Universal Time (UTC)
  -x --catalog               Add message explanations where available
     --no-full               Ellipsize fields
  -a --all                   Show all fields, including long and unprintable
  -q --quiet                 Do not show info messages and privilege warning
     --no-pager              Do not pipe output into a pager
     --no-hostname           Suppress output of hostname field
  -m --merge                 Show entries from all available journals
  -D --directory=PATH        Show journal files from directory
     --file=PATH             Show journal file
     --root=ROOT             Operate on files below a root directory
     --interval=TIME         Time interval for changing the FSS sealing key
     --verify-key=KEY        Specify FSS verification key
     --force                 Override of the FSS key pair with --setup-keys

Commands:
  -h --help                  Show this help text
     --version               Show package version
  -N --fields                List all field names currently used
  -F --field=FIELD           List all values that a specified field takes
     --disk-usage            Show total disk usage of all journal files
     --vacuum-size=BYTES     Reduce disk usage below specified size
     --vacuum-files=INT      Leave only the specified number of journal files
     --vacuum-time=TIME      Remove journal files older than specified time
     --verify                Verify journal file consistency
     --sync                  Synchronize unwritten journal messages to disk
     --flush                 Flush all journal data from /run into /var
     --rotate                Request immediate rotation of the journal files
     --header                Show journal header information
     --list-catalog          Show all message IDs in the catalog
     --dump-catalog          Show entries in the message catalog
     --update-catalog        Update the message catalog database
     --new-id128             Generate a new 128-bit ID
     --setup-keys            Generate a new FSS key pair
```

The `journalctl -n5` command can be used to display the newest five lines of journal logs.

```bash
[root@rhel-server ~]# journalctl -n5
-- Logs begin at Mon 2022-01-10 11:52:12 EST, end at Sun 2022-01-30 16:01:01 EST. --
Jan 30 15:38:25 rhel-server systemd[1]: systemd-tmpfiles-clean.service: Succeeded.
Jan 30 15:38:25 rhel-server systemd[1]: Started Cleanup of Temporary Directories.
Jan 30 16:01:01 rhel-server CROND[384047]: (root) CMD (run-parts /etc/cron.hourly)
Jan 30 16:01:01 rhel-server run-parts[384050]: (/etc/cron.hourly) starting 0anacron
Jan 30 16:01:01 rhel-server run-parts[384056]: (/etc/cron.hourly) finished 0anacron
```

`journalctl --since yesterday` will display all journal logs for the previous day.

`journalctl --since -6h --unit ssh` will display all sshd journal logs for the previous six hours.

The journal logs exist soley in RAM. To make these logs persistent, you need to uncomment the `Storage=auto` line and change `auto` to `persistent`.

```bash
[root@rhel-server ~]# grep '#Storage' /etc/systemd/journald.conf
#Storage=auto
[root@rhel-server ~]# sed -i 's/#Storage=auto/Storage=persistent/g' /etc/systemd/journald.conf
[root@rhel-server ~]# grep '#Storage' /etc/systemd/journald.conf
[root@rhel-server ~]# grep 'Storage' /etc/systemd/journald.conf
Storage=persistent
```

### Start, stop, and check the status of network services

- Start a service: `systemctl start <service>`
- Stop a service: `systemctl stop <service>`
- Check the status of a service: `systemctl status <service>`
- Enable a service to start at boot: `systemctl enable <service>`
- Stop a service from starting at boot: `systemctl disable <service>`

### Securely transfer files between systems

SFTP or SCP can be used to securely transfer files between systems.

SFTP is more like traditional FTP in its usage.

```
[root@rhel-server ~]# sftp localhost
root@localhost's password:
Connected to localhost.
sftp> ?
Available commands:
bye                                Quit sftp
cd path                            Change remote directory to 'path'
chgrp [-h] grp path                Change group of file 'path' to 'grp'
chmod [-h] mode path               Change permissions of file 'path' to 'mode'
chown [-h] own path                Change owner of file 'path' to 'own'
df [-hi] [path]                    Display statistics for current directory or
                                   filesystem containing 'path'
exit                               Quit sftp
get [-afPpRr] remote [local]       Download file
reget [-fPpRr] remote [local]      Resume download file
reput [-fPpRr] [local] remote      Resume upload file
help                               Display this help text
lcd path                           Change local directory to 'path'
lls [ls-options [path]]            Display local directory listing
lmkdir path                        Create local directory
ln [-s] oldpath newpath            Link remote file (-s for symlink)
lpwd                               Print local working directory
ls [-1afhlnrSt] [path]             Display remote directory listing
lumask umask                       Set local umask to 'umask'
mkdir path                         Create remote directory
progress                           Toggle display of progress meter
put [-afPpRr] local [remote]       Upload file
pwd                                Display remote working directory
quit                               Quit sftp
rename oldpath newpath             Rename remote file
rm path                            Delete remote file
rmdir path                         Remove remote directory
symlink oldpath newpath            Symlink remote file
version                            Show SFTP version
!command                           Execute 'command' in local shell
!                                  Escape to local shell
?                                  Synonym for help
sftp>
```

SCP:

```
[root@rhel-server ~]# scp --help
unknown option -- -
usage: scp [-346BCpqrTv] [-c cipher] [-F ssh_config] [-i identity_file]
            [-J destination] [-l limit] [-o ssh_option] [-P port]
            [-S program] source ... target
```
