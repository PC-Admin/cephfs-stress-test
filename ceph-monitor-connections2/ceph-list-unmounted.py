import yaml
import os

#This script checks and prints which Ceph mount points are unmounted

# Load the configuration from a YAML file.
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Check if mount points are mounted.
def check_mount_points(mount_points):
    unmounted = []
    for mount_point in mount_points:
        if not os.path.ismount(mount_point):
            unmounted.append(mount_point)
    return unmounted

# Load configuration settings from the YAML file.
config = load_config("config.yaml")

# Extracting the Ceph mount points from the configuration
ceph_mount_points = config["ceph_mount_points"]

# Check which Ceph mount points are unmounted
unmounted_points = check_mount_points(ceph_mount_points)
if unmounted_points:
    print("Unmounted Ceph mount points:")
    for point in unmounted_points:
        print(point)
else:
    print("All Ceph mount points are mounted.")

