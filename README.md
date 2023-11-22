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
`pcadmin@workstation:~/cephfs-stress-test$ sudo mount -t ceph 10.1.45.201:6789:/ /mnt/cephfs -o name=admin,secret=REDACTED`

`pcadmin@workstation:~/cephfs-stress-test$ sudo chown pcadmin:pcadmin /mnt/cephfs/`

2) Check that the directory in fiotest.fio is actually the mount location of your CephFS.


3) Run the test:

`pcadmin@workstation:~/cephfs-stress-test$ fio ./fiotest.fio`


## Extract Bulk Logs from Ceph

Using the provided script you can extract all the logs from the Ceph cluster and copy them to your local machine.

`pcadmin@workstation:~/cephfs-stress-test$ ./ceph_logs.sh all`


