
# Stretch Mode Ceph

In this guide, we'll try to create multiple failure domains and ensure data is redundant across them. We'll also be testing failover while mounting

See the following for more info:

https://docs.ceph.com/en/latest/cephadm/install/
https://www.ibm.com/docs/en/storage-ceph/6?topic=administration-stretch-clusters-ceph-storage


## Plan

7x virtual hosts, 3x in datacentre a1 (ceph01, ceph02, ceph03), 3x in datacentre b1 (ceph04, ceph05, ceph06), 1x in "virtual" datacentre c1 (ceph07)

5x monitors and managers, 2x in a1 (ceph01, ceph02), 2x in b1 (ceph04, ceph05), 1x in c1 (ceph07).

2x metadata servers, one on a1 (ceph03) and b1 (ceph06).

3x OSDs on each a1 host, 3x OSDS on each b1 host.


## Initial Setup

https://github.com/ceph/cephadm-ansible

Define an inventory at ./inventory/hosts like so:
```
# cat hosts
ceph[01:07].snowsupport.top ansible_ssh_user=root

[clients]
ceph[01:07].snowsupport.top ansible_ssh_user=root

[admin]
ceph[01:07].snowsupport.top ansible_ssh_user=root

[monitors]
ceph01.snowsupport.top ansible_ssh_user=root
```

Turns out we need Ubuntu 20.04! Jammy is not supported by this playbook... :P

`~/cephadm-ansible$ ansible-playbook -i ./inventory/hosts cephadm-preflight.yml --flush-cache`

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


## Cephadm Adding Hosts

https://docs.ceph.com/en/latest/cephadm/host-management/#cephadm-adding-hosts

First we need to copy over the clusters SSH key to every other hosts...

```
root@ceph01:~# cat /etc/ceph/ceph.pub
ssh-rsa AAAAB3NzaC1yc2...

root@ceph02:~# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDfUEzk17GtZsOqF2ZMmseRurb3m1n1HHuBfgWEz6HqMsjStF+Mu+AE0/rpeIkOM8oIisSGC2+4d4Wou1fRZPHRBiZPyWu1DyI7Uh68Dhcm6jbGvU3tsZfSz1jdNwoGiKwoZphLy9pw5rGgnH8JmPD4T10AR1IF1PL8Wm/pE+trsCcjbMRvoF0t8ia8r2tXTVYkT9dj4Bywc7SaPnKm2I4pv4wvhqqq9VZa8yqlSQeDtNifrkaxbdqXgQXdLt2u7ZG7aiaztINUSybA6r6gOakXw6hbVOGzJ6hd9Q43nSE+OxW6j3evcP34fQHWsSJKBAyTnHBzQgWOerIyGg+k873G0gtuRszhqfeqPd75mfzQJG6g4pHmtkaSR42XSc0/A8wD5TJaXZ/xp9PObXqMht6EuLhMTCGV+DDCnYbdI4wtCMiIzpAnndHgAuv1x9QKmem4z6huXz0Y/ygIVMHyGn1pEJL9kIL38+9gZ5e1FPbmB+vQ7nCyfslO+Q6cpqzqU1U= ceph-785e70c8-8d1d-11ee-a19d-d759444dce5d' >> ~/.ssh/authorized_keys

root@ceph03:~# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQChPJFH+zfVOPfEZjbQenCuRe2Gf430aSTDBmromg3qFc24DKX14zlH2TfHt+AgOQqX7yqFezGsa806YPRJpn5IigaqF0yla6btpGb6d2unaCqAUWvroUCbJNMrrRX4x8Sx2iW3jbA1cxMCU6ppL60jsWdr/5KSkahLHqztVfTb2ba9+pn+4zFfMl3vueWuaGX0BN2GSmj4pfB38ifjzjgeUJ6S2DfdJLkuijKNBU5seqp/nCub8+uZEoQ9DjaR6+883uJty9pQyKf/T7lNcCiOhYEhpaEBFWR7ALMficl4n28w2HKl03uWAnmG8lA2cZKlAk+l/V/Mrq1l/LocLM7ncRWdBd/VPQEU5VuvdNdkXAVOXEOXMOAT5EVKzSeL2WoRc63eNaMwTkrmcSSuZKsrjOqa3EpH+pMhCsAXK2HPZYEmK+PUcjbUCMaxGUvpRkZV8G5RgDZ3y4VZsvZC+psYCbF9Q825kSlY9nuzmpfGV10hhQce25BwglxR9/ObLZ8= ceph-856939ce-8cf5-11ee-9e4d-a5b4ee6bbf92' >> ~/.ssh/authorized_keys

root@ceph04:~# echo 'ssh...
root@ceph05:~# echo 'ssh...
root@ceph06:~# echo 'ssh...
root@ceph07:~# echo 'ssh...
```

Then we can tell our bootstrap node add these other hosts.
```
root@ceph01:~# ceph orch host add ceph02 10.1.45.202 _admin
Added host 'ceph02' with addr '10.1.45.202'
root@ceph01:~# ceph orch host add ceph03 10.1.45.203 _admin
Added host 'ceph03' with addr '10.1.45.203'
root@ceph01:~# ceph orch host add ceph04 10.1.45.204 _admin
Added host 'ceph04' with addr '10.1.45.204'
root@ceph01:~# ceph orch host add ceph05 10.1.45.205 _admin
Added host 'ceph05' with addr '10.1.45.205'
root@ceph01:~# ceph orch host add ceph06 10.1.45.206 _admin
Added host 'ceph06' with addr '10.1.45.206'
root@ceph01:~# ceph orch host add ceph07 10.1.45.207 _admin
Added host 'ceph07' with addr '10.1.45.207'

root@ceph01:~# ceph orch host ls
HOST    ADDR         LABELS  STATUS  
ceph01  10.1.45.201  _admin          
ceph02  10.1.45.202  _admin          
ceph03  10.1.45.203  _admin          
ceph04  10.1.45.204  _admin          
ceph05  10.1.45.205  _admin          
ceph06  10.1.45.206  _admin          
ceph07  10.1.45.207  _admin          
7 hosts in cluster
```


## Ensure 5 Monitors Exist on the Right Hosts
```
root@ceph01:~# ceph orch daemon add mon ceph04:10.1.45.204
Deployed mon.ceph04 on host 'ceph04'
root@ceph01:~# ceph orch daemon add mon ceph05:10.1.45.205
Deployed mon.ceph05 on host 'ceph05'

root@ceph01:~# ceph orch daemon rm mon.ceph03 --force
Removed mon.ceph03 from host 'ceph03'
root@ceph01:~# ceph orch daemon rm mon.ceph06 --force
Removed mon.ceph03 from host 'ceph06'

root@ceph01:~# ceph -s
  cluster:
    id:     9e9df6b0-8d26-11ee-a935-1b3a85021dcf
    health: HEALTH_WARN
            1 stray daemon(s) not managed by cephadm
            OSD count 0 < osd_pool_default_size 3
 
  services:
    mon: 5 daemons, quorum ceph01,ceph02,ceph04,ceph05,ceph07 (age 36s)
    mgr: ceph01.qjcoxf(active, since 9m), standbys: ceph02.hzxnsv
    osd: 0 osds: 0 up, 0 in
 
  data:
    pools:   0 pools, 0 pgs
    objects: 0 objects, 0 B
    usage:   0 B used, 0 B / 0 B avail
    pgs:     
```

Now we see 5x monitors in the right places.


## Cool, Let's Add Some OSDs!

/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1 on 6x hosts in a1 and b1.

```
root@ceph01:~# ceph orch daemon add osd ceph01:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 0 on host 'ceph01'
root@ceph01:~# ceph orch daemon add osd ceph02:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 1 on host 'ceph02'
root@ceph01:~# ceph orch daemon add osd ceph03:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 2 on host 'ceph03'
root@ceph01:~# ceph orch daemon add osd ceph04:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 3 on host 'ceph04'
root@ceph01:~# ceph orch daemon add osd ceph05:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 4 on host 'ceph05'
root@ceph01:~# ceph orch daemon add osd ceph06:/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi1
Created osd(s) 5 on host 'ceph06'

root@ceph01:~# ceph -s
  cluster:
    id:     9e9df6b0-8d26-11ee-a935-1b3a85021dcf
    health: HEALTH_WARN
            1 stray daemon(s) not managed by cephadm
 
  services:
    mon: 5 daemons, quorum ceph01,ceph02,ceph04,ceph05,ceph07 (age 9m)
    mgr: ceph01.qjcoxf(active, since 19m), standbys: ceph02.hzxnsv, ceph05.ehhdix, ceph04.ncskvs, ceph07.npfojd
    mds: 1/1 daemons up, 1 standby
    osd: 6 osds: 6 up (since 114s), 6 in (since 2m)
 
  data:
    volumes: 1/1 healthy
    pools:   3 pools, 123 pgs
    objects: 24 objects, 579 KiB
    usage:   1.7 GiB used, 190 GiB / 192 GiB avail
    pgs:     123 active+clean
 
  progress:
```


## Looks good, lets make all 5 hosts a manager
```
root@ceph01:~# ceph orch apply mgr ceph01,ceph02,ceph04,ceph05,ceph07
Scheduled mgr update...
```


## Let's create 2x Metadata Servers on both a1 and b1 datacentres
```
root@ceph01:~# ceph orch apply mds cephfs --placement="2 ceph03 ceph06"
Scheduled mds.cephfs update...

root@ceph01:~# ceph mds stat
 2 up:standby
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


## Create the 2x datacentres and add them to the CRUSH map

```
root@ceph01:~# ceph osd crush add-bucket a1 datacenter
added bucket a1 type datacenter to crush map
root@ceph01:~# ceph osd crush add-bucket b1 datacenter
added bucket b1 type datacenter to crush map

root@ceph01:~# ceph osd crush move ceph01 datacenter=a1
moved item id -7 name 'ceph01' to location {datacenter=a1} in crush map
root@ceph01:~# ceph osd crush move ceph02 datacenter=a1
moved item id -9 name 'ceph02' to location {datacenter=a1} in crush map
root@ceph01:~# ceph osd crush move ceph03 datacenter=a1
moved item id -11 name 'ceph03' to location {datacenter=a1} in crush map
root@ceph01:~# ceph osd crush move ceph04 datacenter=b1
moved item id -13 name 'ceph04' to location {datacenter=b1} in crush map
root@ceph01:~# ceph osd crush move ceph05 datacenter=b1
moved item id -15 name 'ceph05' to location {datacenter=b1} in crush map
root@ceph01:~# ceph osd crush move ceph06 datacenter=b1
moved item id -17 name 'ceph06' to location {datacenter=b1} in crush map
```


## Note the current CRUSH tree and map/rule

```
root@ceph01:~# ceph osd crush tree
ID   CLASS  WEIGHT   TYPE NAME      
 -3         0.09357  datacenter b1  
-13         0.03119      host ceph04
  3    hdd  0.03119          osd.3  
-15         0.03119      host ceph05
  4    hdd  0.03119          osd.4  
-17         0.03119      host ceph06
  5    hdd  0.03119          osd.5  
 -2         0.09357  datacenter a1  
 -7         0.03119      host ceph01
  0    hdd  0.03119          osd.0  
 -9         0.03119      host ceph02
  1    hdd  0.03119          osd.1  
-11         0.03119      host ceph03
  2    hdd  0.03119          osd.2  
 -1               0  root default 

root@ceph01:~# apt install ceph-base -y

root@ceph01:~# ceph osd getcrushmap -o crushmap.temp
16
root@ceph01:~# crushtool -d crushmap.temp -o editable.map
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
device 3 osd.3 class hdd
device 4 osd.4 class hdd
device 5 osd.5 class hdd

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
root default {
	id -1		# do not change unnecessarily
	id -6 class hdd		# do not change unnecessarily
	# weight 0.00000
	alg straw2
	hash 0	# rjenkins1
}
host ceph01 {
	id -7		# do not change unnecessarily
	id -8 class hdd		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.0 weight 0.03119
}
host ceph02 {
	id -9		# do not change unnecessarily
	id -10 class hdd		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.1 weight 0.03119
}
host ceph03 {
	id -11		# do not change unnecessarily
	id -12 class hdd		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.2 weight 0.03119
}
datacenter a1 {
	id -2		# do not change unnecessarily
	id -5 class hdd		# do not change unnecessarily
	# weight 0.09357
	alg straw2
	hash 0	# rjenkins1
	item ceph01 weight 0.03119
	item ceph02 weight 0.03119
	item ceph03 weight 0.03119
}
host ceph04 {
	id -13		# do not change unnecessarily
	id -14 class hdd		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.3 weight 0.03119
}
host ceph05 {
	id -15		# do not change unnecessarily
	id -16 class hdd		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.4 weight 0.03119
}
host ceph06 {
	id -17		# do not change unnecessarily
	id -18 class hdd		# do not change unnecessarily
	# weight 0.03119
	alg straw2
	hash 0	# rjenkins1
	item osd.5 weight 0.03119
}
datacenter b1 {
	id -3		# do not change unnecessarily
	id -4 class hdd		# do not change unnecessarily
	# weight 0.09357
	alg straw2
	hash 0	# rjenkins1
	item ceph04 weight 0.03119
	item ceph05 weight 0.03119
	item ceph06 weight 0.03119
}

# rules
rule replicated_rule {
	id 0
	type replicated
	step take default
	step chooseleaf firstn 0 type host
	step emit
}

# end crush map
```

# Entering Stretch Mode

So now we want to transform this cluster into a 'stretched mode' cluster, which will perform better with higher latency and in the event of a datacenter failure.


## First we define the location of our monitors:
```
root@ceph01:~# ceph mon set_location ceph01 datacentre=a1
root@ceph01:~# ceph mon set_location ceph02 datacentre=a1
root@ceph01:~# ceph mon set_location ceph04 datacentre=b1
root@ceph01:~# ceph mon set_location ceph05 datacentre=b1
```


## Now add a stretch_rule to the end of the CRUSH map by again editing it

Note that the 'id' needs to be set to a positive integer that isn't used by other rules. Note that your datacentre names need to be entered here on the 'take' lines:
```
root@ceph01:~# nano ./editable.map

# rules
rule replicated_rule {
	id 0
	type replicated
	step take default
	step chooseleaf firstn 0 type host
	step emit
}
rule stretch_rule {
	id 1
	type replicated
	step take a1
	step chooseleaf firstn 2 type host
	step emit
	step take b1
	step chooseleaf firstn 2 type host
	step emit
}

root@ceph01:~# crushtool -c ./editable.map -o ./crushmap.compiled

root@ceph01:~# ceph osd setcrushmap -i crushmap.compiled 
19
```


## Change Existing Monitors to 'Connectivity Mode'

root@ceph01:~# ceph mon set election_strategy connectivity


## Command the cluster to enter stretch mode.

In this example, ceph03 is the tiebreaker monitor and we are splitting across data centers. The tiebreaker monitor must be assigned a data center that is neither a1 nor b1.

First we need to add the 'tiebreaker' node to a 3rd virtual datacentre c1 **that isn't defined** in the CRUSH map.

`root@ceph01:~# ceph mon set_location ceph07 datacenter=c1`

Then finally we enable stretch mdoe and declate ceph07 to be the tiebreaker node:

`root@ceph01:~# ceph mon enable_stretch_mode ceph07 stretch_rule datacenter`


## Weird Monitor Location Bug!!!

You might notice an 'Error EINVAL' bug that you can basically wrestle with by reassigning monitor locations like so:
```
root@ceph01:~# ceph mon set_location ceph01 datacentre=a1
root@ceph01:~# ceph mon enable_stretch_mode ceph07 stretch_rule datacenter
Error EINVAL: Could not find location entry for datacenter on monitor ceph01
root@ceph01:~# ceph mon set_location ceph01 datacenter=a1
root@ceph01:~# ceph mon enable_stretch_mode ceph07 stretch_rule datacenter
Error EINVAL: Could not find location entry for datacenter on monitor ceph02
root@ceph01:~# ceph mon set_location ceph02 datacenter=a1
root@ceph01:~# ceph mon enable_stretch_mode ceph07 stretch_rule datacenter
Error EINVAL: Could not find location entry for datacenter on monitor ceph04
root@ceph01:~# ceph mon set_location ceph04 datacenter=b1
root@ceph01:~# ceph mon enable_stretch_mode ceph07 stretch_rule datacenter
Error EINVAL: Could not find location entry for datacenter on monitor ceph05
root@ceph01:~# ceph mon set_location ceph05 datacenter=b1
root@ceph01:~# ceph mon enable_stretch_mode ceph07 stretch_rule datacenter
```


## Set Replication Levels per Pool

Replication levels are applied at the pool level these days, not in the CRUSH map. Adjust your pool replication levels like so:

```
root@ceph01:~# ceph osd pool set cephfs_data min_size 2
set pool 2 min_size to 2
root@ceph01:~# ceph osd pool set cephfs_data size 4
set pool 2 size to 4
root@ceph01:~# ceph osd pool set cephfs_metadata min_size 2
set pool 3 min_size to 2
root@ceph01:~# ceph osd pool set cephfs_metadata size 4
set pool 3 size to 4
```

You did it! Congradulations! You now have a stretch mode cluster!


## Examine Stretch Mode Settings

You can view cluster settings related to stretch mode by running:
```
root@ceph01:~# ceph mon dump
epoch 34
fsid 9e9df6b0-8d26-11ee-a935-1b3a85021dcf
last_changed 2023-11-27T13:48:26.488503+0000
created 2023-11-27T13:12:59.336441+0000
min_mon_release 17 (quincy)
election_strategy: 3
stretch_mode_enabled 1
tiebreaker_mon ceph07
disallowed_leaders ceph07
0: [v2:10.1.45.201:3300/0,v1:10.1.45.201:6789/0] mon.ceph01; crush_location {datacenter=a1}
1: [v2:10.1.45.202:3300/0,v1:10.1.45.202:6789/0] mon.ceph02; crush_location {datacenter=a1}
2: [v2:10.1.45.204:3300/0,v1:10.1.45.204:6789/0] mon.ceph04; crush_location {datacenter=b1}
3: [v2:10.1.45.205:3300/0,v1:10.1.45.205:6789/0] mon.ceph05; crush_location {datacenter=b1}
4: [v2:10.1.45.207:3300/0,v1:10.1.45.207:6789/0] mon.ceph07; crush_location {datacenter=c1}
dumped monmap epoch 34
```

Here we can see the cluster is in stretch mode, and that ceph07 is the tiebreaker.