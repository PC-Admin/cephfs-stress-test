
Installing and testing a second device class, should mimic another datacentre.

## Installation

First created 2 new Ceph hosts ceph04 and ceph05, then added 1x disk to each.


## Re-run the Ansible playbook to preflight the new hosts (Installs Ceph packages)

https://github.com/PC-Admin/cephadm-ansible

`~/cephadm-ansible$ ansible-playbook -i ./inventory/hosts cephadm-preflight.yml --flush-cache`

### Add the new hosts to the Ceph cluster

```bash
root@ceph04:~# sudo hostname ceph04
root@ceph05:~# sudo hostname ceph05

root@ceph01:~#  cat /etc/ceph/ceph.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDVj5fO2yoZLZrh5cxsZYG+8jH/iZRKaLxfiFgauAp8/qr4k5SGmesjMBMJYal4p+qk9sbZDqgcynKbP9kGj92nR1fq9KIO3iTR7aC2IbHWfEKCrYd/8sc4qGoeD+uLXlQa1FHma2Fdw+TASiQwlpfN7Xelo3XnVN9M6/Zs0GcbUD+0h0FLY1BiYv/bOd5p81yUHjv+g5iLmAUGFq0RURBeGul7M6J4JJ++v3AB1OJf620S0syXyGtGFvkyEJJwDzsdss1yJFKqNwyHR82om4OIlTIfmVEGOow5MARn07w9CFG8iwAB+WwNfy+VWxRIZWwNdYZf7ZCm3BCicfZ+UbVzu21KA4BmNxsvR8zEOZaMFqFzC3Y607Bp/NaxujwnwaR5sC1RgArSbySuZTsqkDq89X2s63zcZmZgJ69xK+7qXj8w4U3h5M6Vq/kDNjLNledG/CdWWCRCITZrn/wgKxobpI4ofpMU1Cpb7g7kWrs4Lj6jV4AR/YLXcjWv0CJm9IM= ceph-c4d01214-88f8-11ee-baa8-f1cf0a72cc11

root@ceph04:~# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDVj5fO2yoZLZrh5cxsZYG+8jH/iZRKaLxfiFgauAp8/qr4k5SGmesjMBMJYal4p+qk9sbZDqgcynKbP9kGj92nR1fq9KIO3iTR7aC2IbHWfEKCrYd/8sc4qGoeD+uLXlQa1FHma2Fdw+TASiQwlpfN7Xelo3XnVN9M6/Zs0GcbUD+0h0FLY1BiYv/bOd5p81yUHjv+g5iLmAUGFq0RURBeGul7M6J4JJ++v3AB1OJf620S0syXyGtGFvkyEJJwDzsdss1yJFKqNwyHR82om4OIlTIfmVEGOow5MARn07w9CFG8iwAB+WwNfy+VWxRIZWwNdYZf7ZCm3BCicfZ+UbVzu21KA4BmNxsvR8zEOZaMFqFzC3Y607Bp/NaxujwnwaR5sC1RgArSbySuZTsqkDq89X2s63zcZmZgJ69xK+7qXj8w4U3h5M6Vq/kDNjLNledG/CdWWCRCITZrn/wgKxobpI4ofpMU1Cpb7g7kWrs4Lj6jV4AR/YLXcjWv0CJm9IM= ceph-c4d01214-88f8-11ee-baa8-f1cf0a72cc11' >> ~/.ssh/authorized_keys
root@ceph05:~# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDVj5fO2yoZLZrh5cxsZYG+8jH/iZRKaLxfiFgauAp8/qr4k5SGmesjMBMJYal4p+qk9sbZDqgcynKbP9kGj92nR1fq9KIO3iTR7aC2IbHWfEKCrYd/8sc4qGoeD+uLXlQa1FHma2Fdw+TASiQwlpfN7Xelo3XnVN9M6/Zs0GcbUD+0h0FLY1BiYv/bOd5p81yUHjv+g5iLmAUGFq0RURBeGul7M6J4JJ++v3AB1OJf620S0syXyGtGFvkyEJJwDzsdss1yJFKqNwyHR82om4OIlTIfmVEGOow5MARn07w9CFG8iwAB+WwNfy+VWxRIZWwNdYZf7ZCm3BCicfZ+UbVzu21KA4BmNxsvR8zEOZaMFqFzC3Y607Bp/NaxujwnwaR5sC1RgArSbySuZTsqkDq89X2s63zcZmZgJ69xK+7qXj8w4U3h5M6Vq/kDNjLNledG/CdWWCRCITZrn/wgKxobpI4ofpMU1Cpb7g7kWrs4Lj6jV4AR/YLXcjWv0CJm9IM= ceph-c4d01214-88f8-11ee-baa8-f1cf0a72cc11' >> ~/.ssh/authorized_keys

root@ceph01:~# ceph orch host add ceph04
Added host 'ceph04' with addr '10.1.45.204'
root@ceph01:~# ceph orch host add ceph05
Added host 'ceph05' with addr '10.1.45.205'

root@ceph01:~# ceph df
--- RAW STORAGE ---
CLASS    SIZE   AVAIL    USED  RAW USED  %RAW USED
hdd    96 GiB  77 GiB  19 GiB    19 GiB      20.00
TOTAL  96 GiB  77 GiB  19 GiB    19 GiB      20.00
 
--- POOLS ---
POOL             ID  PGS   STORED  OBJECTS     USED  %USED  MAX AVAIL
.mgr              1    1  577 KiB        2  1.7 MiB      0     24 GiB
cephfs_data       2   32  6.1 GiB    2.07k   18 GiB  20.22     24 GiB
cephfs_metadata   3   32  7.6 MiB       24   23 MiB   0.03     24 GiB
.rgw.root         4   32      0 B        0      0 B      0     24 GiB
```

### Add OSDs on new hosts and label with device class

```bash
root@ceph01:~# ceph orch daemon add osd ceph04:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 3 on host 'ceph04'
root@ceph01:~# ceph orch daemon add osd ceph05:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 4 on host 'ceph05'

root@ceph01:~# ceph osd tree
ID   CLASS  WEIGHT   TYPE NAME        STATUS  REWEIGHT  PRI-AFF
 -1         0.15594  root default                              
 -3         0.03119      host ceph01                           
  0    hdd  0.03119          osd.0        up   1.00000  1.00000
 -5         0.03119      host ceph02                           
  1    hdd  0.03119          osd.1        up   1.00000  1.00000
 -7         0.03119      host ceph03                           
  2    hdd  0.03119          osd.2        up   1.00000  1.00000
 -9         0.03119      host ceph04                           
  3    hdd  0.03119          osd.3        up   1.00000  1.00000
-11         0.03119      host ceph05                           
  4    hdd  0.03119          osd.4        up   1.00000  1.00000

root@ceph01:~# ceph osd crush rm-device-class osd.3
done removing class of osd(s): 3
root@ceph01:~# ceph osd crush set-device-class hdd_rs osd.3
set osd(s) 3 to class 'hdd_rs'

root@ceph01:~# ceph osd crush rm-device-class osd.4
done removing class of osd(s): 4
root@ceph01:~# ceph osd crush set-device-class hdd_rs osd.4
set osd(s) 4 to class 'hdd_rs'

root@ceph01:~# ceph osd tree
ID   CLASS   WEIGHT   TYPE NAME        STATUS  REWEIGHT  PRI-AFF
 -1          0.15594  root default                              
 -3          0.03119      host ceph01                           
  0     hdd  0.03119          osd.0        up   1.00000  1.00000
 -5          0.03119      host ceph02                           
  1     hdd  0.03119          osd.1        up   1.00000  1.00000
 -7          0.03119      host ceph03                           
  2     hdd  0.03119          osd.2        up   1.00000  1.00000
 -9          0.03119      host ceph04                           
  3  hdd_rs  0.03119          osd.3        up   1.00000  1.00000
-11          0.03119      host ceph05                           
  4  hdd_rs  0.03119          osd.4        up   1.00000  1.00000

```

### Create a new CRUSH rule that uses the new device class

```bash
root@ceph01:~# sudo apt install ceph-base

root@ceph01:~# ceph osd crush rule create-replicated custom_replicated_rule default host hdd
root@ceph01:~# ceph osd crush rule dump custom_replicated_rule

root@ceph01:~# ceph osd getcrushmap -o downloaded.map
root@ceph01:~# crushtool -d downloaded.map -o editable.map

root@ceph01:~# nano ./editable.map 
```

In this file we can edit the custom_replicated_rule at the end of the file:
```
# begin crush map
tunable choose_local_tries 0
tunable choose_local_fallback_tries 0
tunable choose_total_tries 50
tunable chooseleaf_descend_once 1
tunable chooseleaf_vary_r 1
tunable chooseleaf_stable 1
tunable straw_calc_version 1
tunable allowed_bucket_algs 54

# devices
device 0 osd.0 class hdd
device 1 osd.1 class hdd
device 2 osd.2 class hdd
device 3 osd.3 class hdd_rs
device 4 osd.4 class hdd_rs

# types
type 0 osd
type 1 host
type 2 chassis
type 3 rack
type 4 row
type 5 pdu
type 6 pod
type 7 room
type 8 datacenter
type 9 zone
type 10 region
type 11 root

# buckets
host ceph01 {
	id -3		# do not change unnecessarily
	id -4 class hdd		# do not change unnecessarily
	id -13 class hdd_rs		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.0 weight 0.03119
}
host ceph02 {
	id -5		# do not change unnecessarily
	id -6 class hdd		# do not change unnecessarily
	id -14 class hdd_rs		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.1 weight 0.03119
}
host ceph03 {
	id -7		# do not change unnecessarily
	id -8 class hdd		# do not change unnecessarily
	id -15 class hdd_rs		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.2 weight 0.03119
}
host ceph04 {
	id -9		# do not change unnecessarily
	id -10 class hdd		# do not change unnecessarily
	id -16 class hdd_rs		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.3 weight 0.03119
}
host ceph05 {
	id -11		# do not change unnecessarily
	id -12 class hdd		# do not change unnecessarily
	id -17 class hdd_rs		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.4 weight 0.03119
}
root default {
	id -1		# do not change unnecessarily
	id -2 class hdd		# do not change unnecessarily
	id -18 class hdd_rs		# do not change unnecessarily
	# weight 0.15594
	alg straw2
	hash 0	# rjenkins1
	item ceph01 weight 0.03119
	item ceph02 weight 0.03119
	item ceph03 weight 0.03119
	item ceph04 weight 0.03119
	item ceph05 weight 0.03119
}

# rules
rule replicated_rule {
	id 0
	type replicated
	step take default
	step chooseleaf firstn 0 type host
	step emit
}
rule custom_replicated_rule {
    id 1
    type replicated
    step take default class hdd
    step chooseleaf firstn 1 type host
    step emit
    step take default class hdd_rs
    step chooseleaf firstn 1 type host
    step emit
}

# end crush map
```

```bash
root@ceph01:~# crushtool -c editable.map -o compiled.map

root@ceph01:~# ceph osd setcrushmap -i compiled.map
26

root@ceph01:~# ceph osd pool ls
.mgr
cephfs_data
cephfs_metadata
.rgw.root

root@ceph01:~# ceph osd pool set cephfs_data crush_rule custom_replicated_rule
set pool 2 crush_rule to custom_replicated_rule
root@ceph01:~# ceph osd pool set cephfs_metadata crush_rule custom_replicated_rule
set pool 3 crush_rule to custom_replicated_rule


root@ceph01:~# ceph osd pool set cephfs_data min_size 2
set pool 2 min_size to 2
root@ceph01:~# ceph osd pool set cephfs_data size 4
set pool 2 size to 4

root@ceph01:~# ceph osd pool set cephfs_metadata min_size 2
set pool 3 min_size to 2
root@ceph01:~# ceph osd pool set cephfs_metadata size 4
set pool 3 size to 4

root@ceph01:~# ceph -s
  cluster:
    id:     c4d01214-88f8-11ee-baa8-f1cf0a72cc11
    health: HEALTH_WARN
            Degraded data redundancy: 64 pgs undersized
 
  services:
    mon: 5 daemons, quorum ceph01,ceph02,ceph03,ceph04,ceph05 (age 75m)
    mgr: ceph03.wdfaxa(active, since 100m), standbys: ceph01.ekvjin, ceph02.irnygv
    mds: 1/1 daemons up, 2 standby
    osd: 5 osds: 5 up (since 70m), 5 in (since 72m); 64 remapped pgs
 
  data:
    volumes: 1/1 healthy
    pools:   4 pools, 97 pgs
    objects: 2.35k objects, 7.1 GiB
    usage:   23 GiB used, 137 GiB / 160 GiB avail
    pgs:     4694/9394 objects misplaced (49.968%)
             64 active+undersized+remapped
             33 active+clean

```

```
root@ceph01:~# ceph -w
  cluster:
    id:     c4d01214-88f8-11ee-baa8-f1cf0a72cc11
    health: HEALTH_WARN
            Degraded data redundancy: 64 pgs undersized
 
  services:
    mon: 5 daemons, quorum ceph01,ceph02,ceph03,ceph04,ceph05 (age 81m)
    mgr: ceph03.wdfaxa(active, since 106m), standbys: ceph01.ekvjin, ceph02.irnygv
    mds: 1/1 daemons up, 2 standby
    osd: 5 osds: 5 up (since 77m), 5 in (since 78m); 64 remapped pgs
 
  data:
    volumes: 1/1 healthy
    pools:   4 pools, 97 pgs
    objects: 2.35k objects, 7.1 GiB
    usage:   23 GiB used, 137 GiB / 160 GiB avail
    pgs:     4694/9394 objects misplaced (49.968%)
             64 active+undersized+remapped
             33 active+clean
 
  io:
    client:   682 KiB/s rd, 0 op/s rd, 0 op/s wr
 
root@ceph01:~# ceph osd df
ID  CLASS   WEIGHT   REWEIGHT  SIZE     RAW USE  DATA     OMAP    META     AVAIL    %USE   VAR   PGS  STATUS
 0     hdd  0.03119   1.00000   32 GiB  5.4 GiB  5.1 GiB     0 B  302 MiB   27 GiB  16.89  1.19   63      up
 1     hdd  0.03119   1.00000   32 GiB  4.4 GiB  4.1 GiB  42 KiB  313 MiB   28 GiB  13.90  0.98   57      up
 2     hdd  0.03119   1.00000   32 GiB  4.5 GiB  4.2 GiB  29 KiB  309 MiB   27 GiB  14.10  0.99   54      up
 3  hdd_rs  0.03119   1.00000   32 GiB  5.4 GiB  5.1 GiB     0 B  298 MiB   27 GiB  16.79  1.18   62      up
 4  hdd_rs  0.03119   1.00000   32 GiB  3.0 GiB  2.7 GiB     0 B  302 MiB   29 GiB   9.34  0.66   55      up
                        TOTAL  160 GiB   23 GiB   21 GiB  71 KiB  1.5 GiB  137 GiB  14.20                   
MIN/MAX VAR: 0.66/1.19  STDDEV: 2.74

root@ceph01:~# ceph osd df tree
ID   CLASS   WEIGHT   REWEIGHT  SIZE     RAW USE  DATA     OMAP    META     AVAIL    %USE   VAR   PGS  STATUS  TYPE NAME      
 -1          0.15594         -  160 GiB   23 GiB   21 GiB  71 KiB  1.5 GiB  137 GiB  14.20  1.00    -          root default   
 -3          0.03119         -   32 GiB  5.4 GiB  5.1 GiB     0 B  302 MiB   27 GiB  16.89  1.19    -              host ceph01
  0     hdd  0.03119   1.00000   32 GiB  5.4 GiB  5.1 GiB     0 B  302 MiB   27 GiB  16.89  1.19   63      up          osd.0  
 -5          0.03119         -   32 GiB  4.4 GiB  4.1 GiB  42 KiB  313 MiB   28 GiB  13.90  0.98    -              host ceph02
  1     hdd  0.03119   1.00000   32 GiB  4.4 GiB  4.1 GiB  42 KiB  313 MiB   28 GiB  13.90  0.98   57      up          osd.1  
 -7          0.03119         -   32 GiB  4.5 GiB  4.2 GiB  29 KiB  309 MiB   27 GiB  14.10  0.99    -              host ceph03
  2     hdd  0.03119   1.00000   32 GiB  4.5 GiB  4.2 GiB  29 KiB  309 MiB   27 GiB  14.10  0.99   54      up          osd.2  
 -9          0.03119         -   32 GiB  5.4 GiB  5.1 GiB     0 B  298 MiB   27 GiB  16.79  1.18    -              host ceph04
  3  hdd_rs  0.03119   1.00000   32 GiB  5.4 GiB  5.1 GiB     0 B  298 MiB   27 GiB  16.79  1.18   62      up          osd.3  
-11          0.03119         -   32 GiB  3.0 GiB  2.7 GiB     0 B  302 MiB   29 GiB   9.34  0.66    -              host ceph05
  4  hdd_rs  0.03119   1.00000   32 GiB  3.0 GiB  2.7 GiB     0 B  302 MiB   29 GiB   9.34  0.66   55      up          osd.4  
                         TOTAL  160 GiB   23 GiB   21 GiB  71 KiB  1.5 GiB  137 GiB  14.20                                    
MIN/MAX VAR: 0.66/1.19  STDDEV: 2.74

root@ceph01:~# ceph osd pool ls detail
pool 1 '.mgr' replicated size 3 min_size 2 crush_rule 0 object_hash rjenkins pg_num 1 pgp_num 1 autoscale_mode on last_change 21 flags hashpspool stripe_width 0 pg_num_max 32 pg_num_min 1 application mgr
pool 2 'cephfs_data' replicated size 4 min_size 2 crush_rule 1 object_hash rjenkins pg_num 32 pgp_num 32 autoscale_mode on last_change 693 lfor 0/492/490 flags hashpspool stripe_width 0 application cephfs
pool 3 'cephfs_metadata' replicated size 4 min_size 2 crush_rule 1 object_hash rjenkins pg_num 32 pgp_num 32 autoscale_mode on last_change 696 flags hashpspool stripe_width 0 pg_autoscale_bias 4 pg_num_min 16 recovery_priority 5 application cephfs
pool 4 '.rgw.root' replicated size 3 min_size 2 crush_rule 0 object_hash rjenkins pg_num 32 pgp_num 32 autoscale_mode on last_change 506 lfor 0/0/504 flags hashpspool stripe_width 0 application rgw
```

hmmm... seems the pool groups are undersized because there are only 2 and 3 OSDs in each class.

It must be trying to put 8 copies in both classes? (totaling 8?) Yep! :) Set max and min size to 2 since I have limited OSDs here to test with.


### Remove osd.2 to mimic rs2 site
```bash
root@ceph01:~# ceph osd out osd.2
marked out osd.2.

root@ceph01:~# ceph -w
  cluster:
    id:     c4d01214-88f8-11ee-baa8-f1cf0a72cc11
    health: HEALTH_OK
...

root@ceph01:~# ceph orch daemon rm osd.2 --force
Removed osd.2 from host 'ceph03'
root@ceph01:~# ceph osd crush remove osd.2
removed item id 2 name 'osd.2' from crush map

root@ceph01:~# ceph auth del osd.2
root@ceph01:~# ceph osd rm osd.2
removed osd.2
```

## Tests

Is there an equal amount of data on both device classes? Yep!

```bash

sum  2349  0  0  0  0  7586367896  0  0  7950  7950
OSD_STAT  USED     AVAIL    USED_RAW  TOTAL    HB_PEERS  PG_SUM  PRIMARY_PG_SUM
3         4.9 GiB   27 GiB   4.9 GiB   32 GiB   [0,1,4]      65               9
4         2.7 GiB   29 GiB   2.7 GiB   32 GiB   [0,1,3]      53              15
0         4.9 GiB   27 GiB   4.9 GiB   32 GiB   [1,3,4]      60              41
1         2.7 GiB   29 GiB   2.7 GiB   32 GiB   [0,3,4]      49              32
sum        15 GiB  113 GiB    15 GiB  128 GiB ```
```

Is this really all the data? Yep!
```bash
/mnt/cephfs$ du -sh .
7.1G	.
```

Is the data still available if we take down one datacentre? (ceph01 and ceph02)

```bash
root@ceph01:~# ceph osd tree
ID   CLASS   WEIGHT   TYPE NAME        STATUS  REWEIGHT  PRI-AFF
 -1          0.12476  root default                              
 -3          0.03119      host ceph01                           
  0     hdd  0.03119          osd.0        up   1.00000  1.00000
 -5          0.03119      host ceph02                           
  1     hdd  0.03119          osd.1        up   1.00000  1.00000
 -7                0      host ceph03                           
 -9          0.03119      host ceph04                           
  3  hdd_rs  0.03119          osd.3        up   1.00000  1.00000
-11          0.03119      host ceph05                           
  4  hdd_rs  0.03119          osd.4        up   1.00000  1.00000

root@ceph01:~# shutdown -h now
root@ceph02:~# shutdown -h now
```

No seems to be hanging... :P

`pcadmin@workstation:~/$ sudo umount /mnt/cephfs`

...hanging?

Need to force it with:

`pcadmin@workstation:~/$ sudo umount -l /mnt/cephfs`

```
pcadmin@workstation:~$ sudo mount -t ceph 10.1.45.203:6789:/ /mnt/cephfs -o name=admin,secret=REDACTED
did not load config file, using default settings.
2023-11-25T04:52:27.168+0800 7f8ec9f2ef40 -1 Errors while parsing config file!
2023-11-25T04:52:27.168+0800 7f8ec9f2ef40 -1 can't open ceph.conf: (2) No such file or directory
2023-11-25T04:52:27.168+0800 7f8ec9f2ef40 -1 Errors while parsing config file!
2023-11-25T04:52:27.168+0800 7f8ec9f2ef40 -1 can't open ceph.conf: (2) No such file or directory
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-11-25T04:52:29.284+0800 7f8ec9f2ef40 -1 failed for service _ceph-mon._tcp
2023-11-25T04:52:29.284+0800 7f8ec9f2ef40 -1 auth: unable to find a keyring on /etc/ceph/ceph.client.admin.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin: (2) No such file or directory
mount error: no mds server is up or the cluster is laggy
```

hmmmm, what if we assign all 5x servers as MDS?


```bash
root@ceph03:~# ceph orch apply mds cephfs --placement="ceph01,ceph02,ceph03,ceph04,ceph05"
Scheduled mds.cephfs update...

root@ceph03:~# ceph mds stat
cephfs:1 {0=cephfs.ceph03.yttnns=up:active} 4 up:standby
root@ceph03:~# ceph -s
  cluster:
    id:     c4d01214-88f8-11ee-baa8-f1cf0a72cc11
    health: HEALTH_OK
 
  services:
    mon: 5 daemons, quorum ceph01,ceph02,ceph03,ceph04,ceph05 (age 5m)
    mgr: ceph01.ekvjin(active, since 5m), standbys: ceph02.irnygv, ceph03.wdfaxa
    mds: 1/1 daemons up, 4 standby
    osd: 4 osds: 4 up (since 5m), 4 in (since 5m)
```

Okay attempting to mount from ceph03 instead (which would be rs2):
```bash
pcadmin@workstation:~$ sudo mount -t ceph 10.1.45.203:6789:/ /mnt/cephfs -o name=admin,secret=REDACTED
did not load config file, using default settings.
2023-11-25T05:00:23.504+0800 7fcf234b1f40 -1 Errors while parsing config file!
2023-11-25T05:00:23.504+0800 7fcf234b1f40 -1 can't open ceph.conf: (2) No such file or directory
2023-11-25T05:00:23.504+0800 7fcf234b1f40 -1 Errors while parsing config file!
2023-11-25T05:00:23.504+0800 7fcf234b1f40 -1 can't open ceph.conf: (2) No such file or directory
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-11-25T05:00:25.508+0800 7fcf234b1f40 -1 failed for service _ceph-mon._tcp
2023-11-25T05:00:25.508+0800 7fcf234b1f40 -1 auth: unable to find a keyring on /etc/ceph/ceph.client.admin.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin: (2) No such file or directory

root@ceph01:~# shutdown -h now
root@ceph02:~# shutdown -h now

pcadmin@workstation:~$ ls /mnt/cephfs
 read_test                              'South Park - S25E02 - The Big Fix.mkv' ...
```

Cool this time we can still read the filesystem but not any files it seems...

Do we need 5x managers to maintain quorum?

```bash
root@ceph01:~# ceph orch apply mgr --placement="ceph01,ceph02,ceph03,ceph04,ceph05"
Scheduled mgr update...

root@ceph01:~# shutdown -h now
root@ceph02:~# shutdown -h now
```

Again we can still read the filesystem but not and files...

```
root@ceph04:~# shutdown -h now
root@ceph05:~# shutdown -h now
```

Again we can still read the filesystem but not and files...


## Conclusion

The data is properly replicated across both sites, but failover doesn't work.

The only reasonable solution seems to be to explore a proper multi-site setup:

https://docs.ceph.com/en/quincy/radosgw/multisite/#varieties-of-multi-site-configuration

