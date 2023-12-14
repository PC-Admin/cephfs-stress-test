
# Ceph Monitor Connections 2

## Usage

1) Create a non-root user to run ceph-check-connections.py. (ceph-check-mounts.py will be run by root)


2) Then edit the variables found in config.yaml to match your environment.


3) Create a Crontab entry for that non-root user to run the ceph-check-connections.py script every minute:
```
* * * * * /usr/bin/python3 /home/pcadmin/ceph-monitor-connections.py >> /var/log/ceph-monitor-connections.log
```

Note that we're writing stdout to a log file here, this isn't required but I would recommend it.


4) Create a Crontab entry for root user to run the ceph-check-mounts.py script every 2 minutes:
```
*/2 * * * * /usr/bin/python3 /home/pcadmin/ceph-check-mounts.py >> /var/log/ceph-check-mounts.log
```


5) Do a manual test run of the scripts:
```
pcadmin@workstation:~/ceph-monitor-connections$ python3 ./ceph-monitor-connections.py
root@workstation:/home/pcadmin/ceph-monitor-connections# python3 ./ceph-check-mounts.py
```
