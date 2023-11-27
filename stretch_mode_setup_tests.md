
# Stretch Mode Setup Tests!

## Mounting CephFS on Local Machine

```
```


## Initial Test With ioping and fio

Before we do anything else. Test the file creation and write speed of the CephFS by using ioping.

```

```



## Adding Files

Time to add some more files we can examine during failures. I like video files as it's obvious when they aren't readable anymore.



## Testing Datacenter Failure

For the first failover test we'll examine if an entire datacenter goes down. In this case we'll be "stopping" all 3 nodes in the a1 datacenter on Proxmox. (ceph01, ceph02, ceph03)

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