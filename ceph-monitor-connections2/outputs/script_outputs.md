
# Script Outputs

## Connection Tests

```bash
# ./ceph-check-connections.py
Successful connections: 5 out of 5
The majority of Ceph monitors are reachable.

# ./ceph-check-connections.py
Failed to connect to ceph01.snowsupport.top
Failed to connect to ceph02.snowsupport.top
Failed to connect to ceph07.snowsupport.top
Successful connections: 2 out of 5
Majority of Ceph monitors are NOT reachable.
```


## Mount Tests

```bash
# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'FAIL' and lockdown file does not exist. Initiating shutdown sequence.
Running command: "/usr/bin/systemctl stop tomcat9"
Running command: "umount -l /mnt/cephfs"
All commands executed successfully.
Lockdown file created.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: 2023-12-16 10:17:13.067680

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REDACTED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T10:12:39.462+0800 7fde118bbf40 -1 failed for service _ceph-mon._tcp
Running command: "/usr/bin/systemctl start tomcat9"
All commands executed successfully.
Lockdown file removed.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file does not exist. Checking mount points.
Checking and writing to mount point: /mnt/cephfs
Successfully wrote to mount point: /mnt/cephfs
Warning: Mount point /mnt/cephfs2 is not mounted.
All mount points checked successfully.
Mount point check succeeded.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Already in lockdown mode and connections are still failing.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Not enough successful connections yet to enable startup.
```


## Unmounted Test

```bash
# ./ceph-list-unmounted.py 
Unmounted Ceph mount points:
/mnt/cephfs2
```