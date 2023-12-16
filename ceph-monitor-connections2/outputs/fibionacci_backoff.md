
# FIBIONACCI BACKOFF (Multiple remount failures.)

## Simulate conenction failure

First I add a 'FAIL' line to ceph-connections.status to simulate a connection failure and trigger shutdown:
```
SUCCESS OK Thu  7 Dec 02:11:31 AWST 2023
SUCCESS OK Thu  7 Dec 05:11:15 AWST 2023
SUCCESS OK Thu  7 Dec 08:11:12 AWST 2023
SUCCESS OK Thu  7 Dec 11:11:16 AWST 2023
SUCCESS OK Thu  7 Dec 14:11:18 AWST 2023 
FAIL ERROR Thu  7 Dec 14:12:18 AWST 2023 
```

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
Already in lockdown mode and connections are still failing.
```


## Simulate startup command Error

So I then remove that fail line AND remove the connection password from config.yaml to simulate an error with startup:
```
ceph_startup_commands: 
  - "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
  - "/usr/bin/systemctl start tomcat9"
```

```bash
# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 0 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T10:49:03.124+0800 7feef843ff40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.
```


## Simulate repeated errors and observe the backoff schedule

```bash
# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 1 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T11:16:36.434+0800 7fee3ceb7f40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 1 minutes is required.
Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: 2023-12-16 11:17:36.371693

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 1 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T11:17:40.257+0800 7f41b78abf40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 2 minutes is required.
Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: 2023-12-16 11:19:40.179627

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 2 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T11:21:32.995+0800 7fcf63e2ff40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 3 minutes is required.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 3 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T11:25:02.607+0800 7f43f5440f40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 5 minutes is required.
Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: 2023-12-16 11:30:02.485412

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 5 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T11:31:12.537+0800 7fb2308f0f40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 8 minutes is required.
Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: 2023-12-16 11:39:12.429087

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 8 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T11:42:08.512+0800 7fb20fab9f40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 13 minutes is required.
Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: 2023-12-16 11:55:08.241615

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 13 minutes is required.
Attempting to run startup commands.
Running command: "/usr/bin/mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REMOVED"
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-12-16T11:55:46.303+0800 7f5ee6c66f40 -1 failed for service _ceph-mon._tcp
adding ceph secret key to kernel failed: Invalid argument
couldn't append secret option: -22
Error occurred while executing commands: Command '['/usr/bin/mount', '-t', 'ceph', '10.1.45.201:6789,10.1.45.202:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.207:6789:/', '/mnt/cephfs', '-o', 'name=admin,secret=REMOVED']' returned non-zero exit status 1.
Failed to run startup commands.

# ./ceph-check-mounts.py 
Loading configuration from config.yaml
Checking last lines in ceph-connections.status file for SUCCESS or FAIL.
Last line contains 'SUCCESS' and lockdown file exists.
Backoff of 13 minutes is required.
Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: 2023-12-16 12:08:46.135647
```
