# cephfs-stress-test

An fio test for stress testing cephfs.

## Usage

1) Mount your CephFS locally, first collect the admin key and IP of a Ceph node:
```
pcadmin@workstation:~/$ ping ceph01.penholder.xyz
PING ceph01.penholder.xyz (10.1.45.201) 56(84) bytes of data.

root@ceph01:/# cat /etc/ceph/ceph.keyring 
[client.admin]
	key = REDACTED
	caps mds = "allow *"
	caps mgr = "allow *"
	caps mon = "allow *"
	caps osd = "allow *"
```

Then mount the CephFS:
```
pcadmin@workstation:~/cephfs-stress-test$ sudo mount -t ceph 10.1.45.201:6789:/ /mnt/cephfs -o name=admin,secret=REDACTED
pcadmin@workstation:~/cephfs-stress-test$ sudo chown pcadmin:pcadmin /mnt/cephfs/
```

2) Check that the directory in fiotest.fio is actually the mount location of your CephFS.


3) Run the fio test:
`pcadmin@workstation:~/cephfs-stress-test$ fio ./fiotest.fio`


4) Run an ioping test:
`pcadmin@workstation:~/cephfs-stress-test$ ioping -W -D /mnt/cephfs/`

Run it while testing failover to examine the latency. You can also run it a set amount of times with -c:

`pcadmin@workstation:~/cephfs-stress-test$ ioping -W -D -c 10 /mnt/cephfs/`


## Extract Bulk Logs from Ceph

Using the provided script you can extract all the logs from the Ceph cluster and copy them to your local machine.

1) First edit the script and add the host names for every ceph node in your cluster:
```
# List of hosts
hosts=('ceph01.penholder.xyz' 'ceph02.penholder.xyz' 'ceph03.penholder.xyz')
```

2) Then run the script:
`pcadmin@workstation:~/cephfs-stress-test$ ./ceph_logs.sh`


