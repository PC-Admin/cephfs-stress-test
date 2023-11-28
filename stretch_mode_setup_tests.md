
# Stretch Mode Setup Tests!

## Mounting CephFS on Local Machine

```
root@ceph01:~# sudo /usr/sbin/cephadm shell
root@ceph01:/# cat /etc/ceph/ceph.keyring
[client.admin]
	key = REDACTED
	caps mds = "allow *"
	caps mgr = "allow *"
	caps mon = "allow *"
	caps osd = "allow *"
pcadmin@workstation:~$ sudo mount -t ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ /mnt/cephfs -o name=admin,secret=REDACTED
did not load config file, using default settings.
2023-11-28T12:43:46.122+0800 7f864bcf8f40 -1 Errors while parsing config file!
2023-11-28T12:43:46.122+0800 7f864bcf8f40 -1 can't open ceph.conf: (2) No such file or directory
2023-11-28T12:43:46.122+0800 7f864bcf8f40 -1 Errors while parsing config file!
2023-11-28T12:43:46.122+0800 7f864bcf8f40 -1 can't open ceph.conf: (2) No such file or directory
unable to get monitor info from DNS SRV with service name: ceph-mon
2023-11-28T12:43:46.362+0800 7f864bcf8f40 -1 failed for service _ceph-mon._tcp
2023-11-28T12:43:46.362+0800 7f864bcf8f40 -1 auth: unable to find a keyring on /etc/ceph/ceph.client.admin.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin: (2) No such file or directory
pcadmin@workstation:~$ sudo chown -R pcadmin:pcadmin /mnt/cephfs/
```


## Initial Test With ioping and fio

Before we do anything else. Test the file creation and write speed of the CephFS by using ioping.

```
pcadmin@workstation:~$ 
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 22.6 GiB): request=1 time=12.1 ms (warmup)
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 22.6 GiB): request=2 time=8.07 ms
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 22.6 GiB): request=3 time=6.49 ms
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 22.6 GiB): request=4 time=5.86 ms
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 22.6 GiB): request=5 time=7.90 ms

--- /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 22.6 GiB) ioping statistics ---
4 requests completed in 28.3 ms, 16 KiB written, 141 iops, 564.8 KiB/s
generated 5 requests in 4.01 s, 20 KiB, 1 iops, 4.99 KiB/s
min/avg/max/mdev = 5.86 ms / 7.08 ms / 8.07 ms / 935.9 us
```


## Adding Files

Time to add some more files we can examine during failures. I like video files as it's obvious when they aren't readable anymore.
```
pcadmin@workstation:~$ df -h
Filesystem                                                                                                                Size  Used Avail Use% Mounted on
/dev/mapper/MyVault                                                                                                        16G  3.7G   12G  25% /home/pcadmin/MyVault
10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/   26G  7.0G   19G  27% /mnt/cephfs
```


## Are the Files Duplicated Across Datacenters?

```
root@ceph01:~# ceph osd df
ID  CLASS  WEIGHT   REWEIGHT  SIZE     RAW USE  DATA     OMAP    META     AVAIL    %USE   VAR   PGS  STATUS
 3    hdd  0.03119   1.00000   32 GiB  5.0 GiB  4.7 GiB  11 KiB  299 MiB   27 GiB  15.65  1.02   45      up
 4    hdd  0.03119   1.00000   32 GiB  4.7 GiB  4.4 GiB   5 KiB  291 MiB   27 GiB  14.55  0.95   42      up
 5    hdd  0.03119   1.00000   32 GiB  5.1 GiB  4.8 GiB  11 KiB  295 MiB   27 GiB  15.93  1.04   43      up
 0    hdd  0.03119   1.00000   32 GiB  5.1 GiB  4.8 GiB   6 KiB  295 MiB   27 GiB  15.96  1.04   42      up
 1    hdd  0.03119   1.00000   32 GiB  5.2 GiB  4.9 GiB  12 KiB  295 MiB   27 GiB  16.33  1.06   48      up
 2    hdd  0.03119   1.00000   32 GiB  4.4 GiB  4.1 GiB  11 KiB  299 MiB   28 GiB  13.85  0.90   40      up
                       TOTAL  192 GiB   30 GiB   28 GiB  58 KiB  1.7 GiB  162 GiB  15.38                   
MIN/MAX VAR: 0.90/1.06  STDDEV: 0.88

root@ceph01:~# ceph osd pool ls detail
pool 1 'cephfs_data' replicated size 4 min_size 2 crush_rule 1 object_hash rjenkins pg_num 32 pgp_num 32 autoscale_mode on last_change 475 lfor 0/475/473 flags hashpspool stripe_width 0 application cephfs
pool 2 'cephfs_metadata' replicated size 4 min_size 2 crush_rule 1 object_hash rjenkins pg_num 32 pgp_num 32 autoscale_mode on last_change 347 flags hashpspool stripe_width 0 pg_autoscale_bias 4 pg_num_min 16 recovery_priority 5 application cephfs
pool 3 '.mgr' replicated size 4 min_size 2 crush_rule 1 object_hash rjenkins pg_num 1 pgp_num 1 autoscale_mode on last_change 236 flags hashpspool stripe_width 0 pg_num_max 32 pg_num_min 1 application mgr
```

Yes. :)


## Testing Datacenter Failure

For the first failover test we'll examine if an entire datacenter goes down. In this case we'll be "stopping" all 3 nodes in the a1 datacenter on Proxmox. (ceph01, ceph02, ceph03)

ceph01 = VMID 122 (gastly)
ceph02 = VMID 128 (eevee)
ceph03 = VMID 129 (jigglypuff)

```
pcadmin@workstation:~$ ssh gastly sudo qm stop 122;
ssh eevee sudo qm stop 128;
ssh jigglypuff sudo qm stop 129;
```

Examine the state of the remaining cluster:
```
root@ceph04:~# ceph -s
  cluster:
    id:     9e9df6b0-8d26-11ee-a935-1b3a85021dcf
    health: HEALTH_WARN
            3 hosts fail cephadm check
            We are missing stretch mode buckets, only requiring 1 of 2 buckets to peer
            insufficient standby MDS daemons available
            2/5 mons down, quorum ceph04,ceph05,ceph07
            1 datacenter (3 osds) down
            3 osds down
            3 hosts (3 osds) down
            Degraded data redundancy: 4630/9260 objects degraded (50.000%), 48 pgs degraded, 65 pgs undersized
 
  services:
    mon: 5 daemons, quorum ceph04,ceph05,ceph07 (age 5m), out of quorum: ceph01, ceph02
    mgr: ceph07.npfojd(active, since 4m), standbys: ceph04.ncskvs, ceph05.ehhdix
    mds: 1/1 daemons up
    osd: 6 osds: 3 up (since 5m), 6 in (since 15h)
 
  data:
    volumes: 1/1 healthy
    pools:   3 pools, 65 pgs
    objects: 2.31k objects, 6.9 GiB
    usage:   15 GiB used, 81 GiB / 96 GiB avail
    pgs:     4630/9260 objects degraded (50.000%)
             48 active+undersized+degraded
             17 active+undersized
 
  io:
    client:   1.5 MiB/s rd, 85 B/s wr, 375 op/s rd, 0 op/s wr
 
root@ceph04:~# ceph health
HEALTH_WARN 3 hosts fail cephadm check; We are missing stretch mode buckets, only requiring 1 of 2 buckets to peer; insufficient standby MDS daemons available; 2/5 mons down, quorum ceph04,ceph05,ceph07; 1 datacenter (3 osds) down; 3 osds down; 3 hosts (3 osds) down; Degraded data redundancy: 4630/9260 objects degraded (50.000%), 48 pgs degraded, 65 pgs undersized
```

Can the filesystem still be read? **Yes, but it's quite slow to return results. (~1min)**
```
pcadmin@workstation:~$ ls -la /mnt/cephfs/
total 6376652
drwxr-xr-x 3 pcadmin pcadmin     1025 Nov 28 12:56  .
drwxr-xr-x 9 root    root        4096 Nov 21 15:49  ..
-rw-r--r-- 1 pcadmin pcadmin  3305472 Nov 28 12:53  read-test.0.0
-rw-r--r-- 1 pcadmin pcadmin  4702208 Nov 28 12:53  read-test.0.1
-rw-r--r-- 1 pcadmin pcadmin  3088384 Nov 28 12:53  read-test.0.10
-rw-r--r-- 1 pcadmin pcadmin 10326016 Nov 28 12:53  read-test.0.100
-rw-r--r-- 1 pcadmin pcadmin  6270976 Nov 28 12:56  read-test.0.1000
-rw-r--r-- 1 pcadmin pcadmin  9347072 Nov 28 12:56  read-test.0.1001
-rw-r--r-- 1 pcadmin pcadmin  7229440 Nov 28 12:56  read-test.0.1002
```

Can files be read? **Yes, but it is quite slow to start reading. (~1min)**

Can files be written? **Yes, seems to be no lag now it's reading...**

What are the ioping results?
```
$ ioping -c 5 -W -D /mnt/cephfs/
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 25.9 GiB): request=1 time=15.2 ms (warmup)
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 25.9 GiB): request=2 time=18.0 ms
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 25.9 GiB): request=3 time=58.2 ms
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 25.9 GiB): request=4 time=18.0 ms
4 KiB >>> /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 25.9 GiB): request=5 time=18.4 ms

--- /mnt/cephfs/ (ceph 10.1.45.201:6789,10.1.45.202:6789,10.1.45.203:6789,10.1.45.204:6789,10.1.45.205:6789,10.1.45.206:6789,10.1.45.207:6789:/ 25.9 GiB) ioping statistics ---
4 requests completed in 112.6 ms, 16 KiB written, 35 iops, 142.1 KiB/s
generated 5 requests in 4.02 s, 20 KiB, 1 iops, 4.98 KiB/s
min/avg/max/mdev = 18.0 ms / 28.2 ms / 58.2 ms / 17.3 ms
```

After flipping hosts back on:
```
root@ceph04:~# ceph -s
  cluster:
    id:     9e9df6b0-8d26-11ee-a935-1b3a85021dcf
    health: HEALTH_WARN
            clock skew detected on mon.ceph02
 
  services:
    mon: 5 daemons, quorum ceph01,ceph02,ceph04,ceph05,ceph07 (age 7s)
    mgr: ceph07.npfojd(active, since 7m), standbys: ceph04.ncskvs, ceph05.ehhdix, ceph02.hzxnsv, ceph01.qjcoxf
    mds: 1/1 daemons up, 1 standby
    osd: 6 osds: 6 up (since 20s), 6 in (since 15h)
 
  data:
    volumes: 1/1 healthy
    pools:   3 pools, 65 pgs
    objects: 2.31k objects, 6.9 GiB
    usage:   30 GiB used, 162 GiB / 192 GiB avail
    pgs:     65 active+clean
 
root@ceph04:~# ceph health
HEALTH_WARN clock skew detected on mon.ceph02
```


## Testing Datacenter Isolation

To test the more challenging scenario where one datacenter is still up but isolated from the other datacenter we'll be quickly erecting firewall rules to block a1 off from the rest of the cluster.

```

```

Examine the state of the remaining cluster:

```

```

Can the filesystem still be read?

Can files be read?

Can files be written?

What are the ioping and fio results?

```

```