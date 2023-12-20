
# Creating a user and secret key

client.admin must first create users and securely distribute the keys to those users out of band.

The following commands will create a user named user1 and give them read access to the cluster.
```bash
root@ceph02:~# ceph auth get-or-create-key client.user1 mon 'allow r' osd 'allow r'
AQAcsYJlXPC6ChAAlvZm7F65jrMF21+kfzRB5A==

root@ceph02:~# ceph auth print-key client.user1 > /etc/ceph/ceph.client.user1.keyring

root@ceph02:~# ceph auth ls
...
client.user1
	key: AQAcsYJlXPC6ChAAlvZm7F65jrMF21+kfzRB5A==
	caps: [mon] allow r
	caps: [osd] allow r
```
