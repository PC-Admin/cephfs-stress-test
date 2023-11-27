
# First cephadm-ansible run!

Defined an inventory... ./inventory/hosts

Turns out we need Ubuntu 20.04! Jammy is not supported by this playbook... :P

https://github.com/PC-Admin/cephadm-ansible

`~/cephadm-ansible$ ansible-playbook -i ./inventory/hosts cephadm-preflight.yml --flush-cache`

Okay this playbook won't actually set the cluster up, we have to use cephadm for that!

NOTE: These instructions assume your node hostnames are not FQDNs. If they are you should edit them to be short hostnames.


# Creating a Cluster with cephadm

https://docs.ceph.com/en/latest/cephadm/install/


## Running the Bootstrap Command

```
root@ceph01:~# cephadm bootstrap --mon-ip 10.1.45.201
...

Ceph Dashboard is now available at:

	     URL: https://ceph01:8443/
	    User: admin
	Password: PASSWORD

...

You can access the Ceph CLI as following in case of multi-cluster or non-default config:

	sudo /usr/sbin/cephadm shell --fsid c4d01214-88f8-11ee-baa8-f1cf0a72cc11 -c /etc/ceph/ceph.conf -k /etc/ceph/ceph.client.admin.keyring

Or, if you are only running a single cluster on this host:

	sudo /usr/sbin/cephadm shell 
```

## Access Ceph Shell

```
root@ceph01:~# cephadm shell
Inferring fsid c4d01214-88f8-11ee-baa8-f1cf0a72cc11
Inferring config /var/lib/ceph/c4d01214-88f8-11ee-baa8-f1cf0a72cc11/mon.ceph01/config
Using ceph image with id 'ab461d68c4ca' and tag 'v17' created on 2023-11-14 18:37:34 +0000 UTC
quay.io/ceph/ceph@sha256:d76bc96661daa8642ac6f34e2b999bcc5c20d4e4ce99bf49dfb1aacd8fd729f7
root@ceph01:/# ceph -s
  cluster:
    id:     c4d01214-88f8-11ee-baa8-f1cf0a72cc11
    health: HEALTH_WARN
            OSD count 0 < osd_pool_default_size 3
 
  services:
    mon: 1 daemons, quorum ceph01 (age 4m)
    mgr: ceph01.eldgxw(active, since 108s)
    osd: 0 osds: 0 up, 0 in
 
  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   0 B used, 0 B / 0 B avail
    pgs:  
```

## Cephadm Adding Hosts

https://docs.ceph.com/en/latest/cephadm/host-management/#cephadm-adding-hosts

First we need to copy over the clusters SSH key to the other hosts...

```
root@ceph01:~# cat /etc/ceph/ceph.pub
ssh-rsa AAAAB3NzaC1yc...

root@ceph02:~# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDVj5fO2yoZLZrh5cxsZYG+8jH/iZRKaLxfiFgauAp8/qr4k5SGmesjMBMJYal4p+qk9sbZDqgcynKbP9kGj92nR1fq9KIO3iTR7aC2IbHWfEKCrYd/8sc4qGoeD+uLXlQa1FHma2Fdw+TASiQwlpfN7Xelo3XnVN9M6/Zs0GcbUD+0h0FLY1BiYv/bOd5p81yUHjv+g5iLmAUGFq0RURBeGul7M6J4JJ++v3AB1OJf620S0syXyGtGFvkyEJJwDzsdss1yJFKqNwyHR82om4OIlTIfmVEGOow5MARn07w9CFG8iwAB+WwNfy+VWxRIZWwNdYZf7ZCm3BCicfZ+UbVzu21KA4BmNxsvR8zEOZaMFqFzC3Y607Bp/NaxujwnwaR5sC1RgArSbySuZTsqkDq89X2s63zcZmZgJ69xK+7qXj8w4U3h5M6Vq/kDNjLNledG/CdWWCRCITZrn/wgKxobpI4ofpMU1Cpb7g7kWrs4Lj6jV4AR/YLXcjWv0CJm9IM= ceph-c4d01214-88f8-11ee-baa8-f1cf0a72cc11' >> ~/.ssh/authorized_keys

root@ceph03:~# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDVj5fO2yoZLZrh5cxsZYG+8jH/iZRKaLxfiFgauAp8/qr4k5SGmesjMBMJYal4p+qk9sbZDqgcynKbP9kGj92nR1fq9KIO3iTR7aC2IbHWfEKCrYd/8sc4qGoeD+uLXlQa1FHma2Fdw+TASiQwlpfN7Xelo3XnVN9M6/Zs0GcbUD+0h0FLY1BiYv/bOd5p81yUHjv+g5iLmAUGFq0RURBeGul7M6J4JJ++v3AB1OJf620S0syXyGtGFvkyEJJwDzsdss1yJFKqNwyHR82om4OIlTIfmVEGOow5MARn07w9CFG8iwAB+WwNfy+VWxRIZWwNdYZf7ZCm3BCicfZ+UbVzu21KA4BmNxsvR8zEOZaMFqFzC3Y607Bp/NaxujwnwaR5sC1RgArSbySuZTsqkDq89X2s63zcZmZgJ69xK+7qXj8w4U3h5M6Vq/kDNjLNledG/CdWWCRCITZrn/wgKxobpI4ofpMU1Cpb7g7kWrs4Lj6jV4AR/YLXcjWv0CJm9IM= ceph-c4d01214-88f8-11ee-baa8-f1cf0a72cc11' >> ~/.ssh/authorized_keys
```

Then we can tell our bootstrap node add these other hosts.
```
root@ceph02:~# sudo hostname ceph02
root@ceph03:~# sudo hostname ceph03


root@ceph01:~# ceph orch host add ceph02 10.1.45.202 _admin
Added host 'ceph02' with addr '10.1.45.202'
root@ceph01:~# ceph orch host add ceph03 10.1.45.203 _admin
Added host 'ceph03' with addr '10.1.45.203'

root@ceph01:/# ceph -s
  cluster:
    id:     c4d01214-88f8-11ee-baa8-f1cf0a72cc11
    health: HEALTH_WARN
            OSD count 0 < osd_pool_default_size 3
 
  services:
    mon: 3 daemons, quorum ceph01,ceph02,ceph03 (age 3m)
    mgr: ceph01.eldgxw(active, since 13m), standbys: ceph02.dgiljp
    osd: 0 osds: 0 up, 0 in
 
  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   0 B used, 0 B / 0 B avail
    pgs:  
```

Seems like I already have 3 monitors... cool let's add some OSDs!

/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1 on all 3 hosts :)

```
root@ceph01:/# ceph orch daemon add osd ceph01:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 0 on host 'ceph01'
root@ceph01:/# ceph orch daemon add osd ceph02:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 1 on host 'ceph02'
root@ceph01:/# ceph orch daemon add osd ceph03:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 2 on host 'ceph03'

root@ceph01:/# ceph -s
  cluster:
    id:     c4d01214-88f8-11ee-baa8-f1cf0a72cc11
    health: HEALTH_OK
 
  services:
    mon: 3 daemons, quorum ceph01,ceph02,ceph03 (age 13m)
    mgr: ceph01.eldgxw(active, since 24m), standbys: ceph02.dgiljp
    osd: 3 osds: 3 up (since 26s), 3 in (since 44s)
 
  data:
    pools:   1 pools, 1 pgs
    objects: 2 objects, 577 KiB
    usage:   875 MiB used, 95 GiB / 96 GiB avail
    pgs:     1 active+clean
```

## Looks good, lets add a 3rd Manager
```
root@ceph01:/# ceph orch apply mgr ceph01,ceph02,ceph03
Scheduled mgr update...
```

DONE!


## Let's create 3x Metadata Servers!
```
root@ceph01:/# ceph orch apply mds cephfs --placement="3 ceph01 ceph02 ceph03"
Scheduled mds.cephfs update...

root@ceph01:/# ceph mds stat
 3 up:standby
```

## Creating a Ceph Filesystem

Create 2 pools, one for data and one for metadata
```
root@ceph01:~# ceph osd pool create cephfs_data 128
pool 'cephfs_data' created
root@ceph01:~# ceph osd pool create cephfs_metadata 32
pool 'cephfs_metadata' created

root@ceph01:/# ceph osd pool ls
.mgr
cephfs_data
cephfs_metadata
```

Create a Filesystem: Create the CephFS filesystem:
```
root@ceph01:/# ceph fs new cephfs cephfs_metadata cephfs_data
  Pool 'cephfs_data' (id '2') has pg autoscale mode 'on' but is not marked as bulk.
  Consider setting the flag by running
    # ceph osd pool set cephfs_data bulk true
new fs with metadata pool 3 and data pool 2
```


## Mounting CephFS on Local Machine
```
root@ceph01:/# cat /etc/ceph/ceph.keyring 
[client.admin]
	key = REDACTED
	caps mds = "allow *"
	caps mgr = "allow *"
	caps mon = "allow *"
	caps osd = "allow *"

pcadmin@workstation:~/cephadm-ansible$ sudo mount -t ceph 10.1.45.201:6789:/ /mnt/cephfs -o name=admin,secret=REDACTED
did not load config file, using default settings.
2023-11-22T14:52:20.107+0800 7fcd9a8fdf40 -1 Errors while parsing config file!
2023-11-22T14:52:20.107+0800 7fcd9a8fdf40 -1 can't open ceph.conf: (2) No such file or directory
2023-11-22T14:52:20.107+0800 7fcd9a8fdf40 -1 Errors while parsing config file!
2023-11-22T14:52:20.107+0800 7fcd9a8fdf40 -1 can't open ceph.conf: (2) No such file or directory
unable to get monitor info from DNS SRV with service name: ceph-mon2023-11-22T14:52:20.267+0800 7fcd9a8fdf40 -1 failed for service _ceph-mon._tcp

2023-11-22T14:52:20.267+0800 7fcd9a8fdf40 -1 auth: unable to find a keyring on /etc/ceph/ceph.client.admin.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin: (2) No such file or directory
```

MOUNTED :) NICELY DONE!


## View Ceph Dashboard & Grafana

Logged into:
https://ceph01:8443/

admin
NEWPASSWORD

Grafana:
https://ceph01:3000