
# Ceph Monitor Connections 2

These scripts run via cron and check if the majority of Ceph monitors can be reached, if not it will log the failure then turn off Tomcat and unmount CephFS.

[ceph-check-connections.py](./ceph-check-connections.py)

This script checks if the majority of Ceph monitors can be reached and return a 0 for success or 1 for failure.

[ceph-check-mounts.py](./ceph-check-mounts.py)
``
- Loads a config file
- Loads the cephfs_connections_status_file log file
- If the last line of the log file contains 'FAIL' and ./lockdown.file does not exist:
  - Run ceph_shutdown_commands
  - Create ./lockdown.file
- If the last 3 lines of the log file contains 'SUCCESS' and ./lockdown.file exists:
  - Run ceph_startup_commands
  - Delete ./lockdown.file
  - return 0 on success and 1 on failure ??
- If the last line of the log file contains 'SUCCESS' and ./lockdown.file does not exist:
  - Check the mount points by:
    - Try and write a file (testCeph.txt) to each mounted mount point containing "$(hostname) $(date)"
    - If writing fails or times out (30sec) on any mount point, we:
      - Run ceph_shutdown_commands
      - Create ./lockdown.file
      - return 0 on success and 1 on failure ??
    - If writing succeeds on all mount points, we:
      - return 0

[ceph-list-unmounted.py](./ceph-list-unmounted.py)

This script checks and prints which Ceph mount points are unmounted


## Usage

1) Create a non-root user to run ceph-check-connections.py. (ceph-check-mounts.py will be run by root)


2) Then edit the variables found in config.yaml to match your environment.


3) Create a Crontab entry for that non-root user to run the ceph-check-connections.py script every minute:
```
* * * * * /home/pcadmin/ceph-monitor-connections.py >> /var/log/ceph-monitor-connections.log
```

Note that we're writing stdout to a log file here, this isn't required but I would recommend it.


4) Create a Crontab entry for root user to run the ceph-check-mounts.py script every 2 minutes:
```
*/2 * * * * /home/pcadmin/ceph-check-mounts.py >> /var/log/ceph-check-mounts.log
```


5) Do a manual test run of the scripts:
```
pcadmin@workstation:~/ceph-monitor-connections2$ ./ceph-monitor-connections.py
root@workstation:/home/pcadmin/ceph-monitor-connections2# ./ceph-check-mounts.py
```

## Checking for unmounted CephFS

The ceph-check-mounts.py script will print which mount points are currently unmounted:
```
root@workstation:/home/pcadmin/ceph-monitor-connections2# ./ceph-list-unmounted.py 
Unmounted Ceph mount points:
/mnt/cephfs2
```