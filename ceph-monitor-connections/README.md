
# Ceph Monitor Connections

Checks if the majority of Ceph monitors can be reached, if not it will log the failure then turn off Tomcat and unmount CephFS.

This script is meant to be run as a non-root user with command specific sudo privileges, 


## Usage

1) Create a non-root user and adjust their sudo privileges so that user can only run the following commands without specifying a password:

```bash
$ sudo visudo
---------------------------- visudo ----------------------------
# Command specific sudo privileges for ceph-monitor-connections.sh
pcadmin ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop tomcat9
pcadmin ALL=(ALL) NOPASSWD: /usr/bin/umount --lazy /mnt/cephfs
-----------------------------------------------------------------
```

Make sure the username and mount point in the script match your environment.


2) Then edit the variables found in config.yaml to match your environment.


3) Create a Crontab entry for that user to run the script every minute:
```
* * * * * /usr/bin/python3 /home/pcadmin/ceph-monitor-connections/ceph-monitor-connections.py
```

4) Do a manual test run of the script:
```
pcadmin@workstation:~/ceph-monitor-connections$ python3 ./ceph-monitor-connections.py
```


5) If the script has logged a connection failure it won't run again until you manually run it with the reset argument:
```
pcadmin@workstation:~/ceph-monitor-connections$ python3 ./ceph-monitor-connections.py reset
```
