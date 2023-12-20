
# Partition Alignment

Partition alignment is important for Ceph performance. Here is how we check alignment:

```bash

root@workstation:# sfdisk -d /dev/nvme0n1
label: gpt
label-id: 7A456478-878A-41F5-8ABE-8D9B4F701952
device: /dev/nvme0n1
unit: sectors
first-lba: 34
last-lba: 500118158
sector-size: 512

/dev/nvme0n1p1 : start=        2048, size=     1048576, type=C12A7328-F81F-11D2-BA4B-00A0C93EC93B, uuid=682F5B06-CA0B-4576-8F24-E089EDED051D, name="EFI System Partition"
/dev/nvme0n1p2 : start=     1050624, size=     3500032, type=0FC63DAF-8483-4772-8E79-3D69D8477DE4, uuid=9CD3CD07-38C3-4A86-8087-BB0956530F51
/dev/nvme0n1p3 : start=     4550656, size=   495566848, type=0FC63DAF-8483-4772-8E79-3D69D8477DE4, uuid=8B24358B-7C30-4A0C-8940-DE53F982AB00

root@workstation:# fdisk -l -u /dev/nvme0n1
Disk /dev/nvme0n1: 238.47 GiB, 256060514304 bytes, 500118192 sectors
Disk model: Sabrent                                 
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 7A456478-878A-41F5-8ABE-8D9B4F701952

Device           Start       End   Sectors   Size Type
/dev/nvme0n1p1    2048   1050623   1048576   512M EFI System
/dev/nvme0n1p2 1050624   4550655   3500032   1.7G Linux filesystem
/dev/nvme0n1p3 4550656 500117503 495566848 236.3G Linux filesystem
```

In both of these outputs we can see the physical sector size is 512 bytes.

Now we just need to divide the start sector by the physical sector size to see if it is aligned:

2048 / 512 = 4
1050624 / 512 = 2054
4550656 / 512 = 8878

All of these are whole numbers so the partitions are aligned. :)