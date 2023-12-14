import yaml
import sys
import os
import subprocess
from datetime import datetime

# This script:
# - Loads a config file
# - Loads the cephfs_connections_status_file log file
# - If the last line of the log file contains 'FAIL' and ./lockdown.file does not exist:
#   - Run ceph_shutdown_commands
#   - Create ./lockdown.file
# - If the last 3 lines of the log file contains 'SUCCESS' and ./lockdown.file exists:
#   - Run ceph_startup_commands
#   - Delete ./lockdown.file
#   - return 0 on success and 1 on failure ??
# - If the last line of the log file contains 'SUCCESS' and ./lockdown.file does not exist:
#   - Check the mount points by:
#     - Try and write a file (testCeph.txt) to each mounted mount point containing "$(hostname) $(date)"
#     - If writing fails or times out (30sec) on any mount point, we:
#       - Run ceph_shutdown_commands
#       - Create ./lockdown.file
#       - return 0 on success and 1 on failure ??
#     - If writing succeeds on all mount points, we:
#       - return 0

# Checking Mount Points:
# Add the list of unmounted drives to a list ??

# Restart:
# Ideally we should have some sort of state record so we don't keep restarting if the connectivity works but mounting doesn't. ??

# Load the configuration from a YAML file.
def load_config(file_path):
    print(f"Loading configuration from {file_path}")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Check the last N lines of a log file for a specific string.
def check_last_n_lines(file_path, check_string, n):
    print(f"Checking the last {n} lines of {file_path} for '{check_string}'")
    with open(file_path, 'r') as file:
        lines = file.readlines()[-n:]
    # Check if all lines contain the string.
    return all(check_string in line for line in lines)

# Run a list of commands.
def run_commands(commands):
    try:
        for command in commands:
            print(f"Running command: \"{command}\"")
            # Split the command string into a list of arguments
            command_list = command.split()
            subprocess.run(command_list, check=True)
        print("All commands executed successfully.")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing commands: {e}")
        return 1

# Check and write to mount points.
def check_mounts(mount_points):
    for mount_point in mount_points:
        test_file_path = os.path.join(mount_point, "testCeph.txt")
        try:
            print(f"Checking and writing to mount point: {mount_point}")
            # Running the write test as a separate process with a timeout
            cmd = f"echo '{os.uname().nodename} {datetime.now()}' > {test_file_path} && rm {test_file_path}"
            subprocess.run(cmd, shell=True, timeout=30, check=True)
            print(f"Successfully wrote to mount point: {mount_point}")
        except subprocess.TimeoutExpired:
            print(f"Write test to mount point {mount_point} timed out.")
            return False
        except Exception as e:
            print(f"Error writing to or removing file at mount point {mount_point}: {e}")
            return False
    print("All mount points checked successfully.")
    return True

# Load configuration from the YAML file.
config = load_config("config.yaml")

ceph_connections_status_file = config["ceph_connections_status_file"]
ceph_shutdown_commands = config["ceph_shutdown_commands"]
ceph_startup_commands = config["ceph_startup_commands"]
ceph_mount_points = config["ceph_mount_points"]

lockdown_file = './lockdown.file'

# If the last line of the log file contains 'FAIL' and ./lockdown.file does not exist
if check_last_n_lines(ceph_connections_status_file, 'FAIL', 1) and not os.path.exists(lockdown_file):
    print("Last line contains 'FAIL' and lockdown file does not exist. Initiating shutdown sequence.")
    if run_commands(ceph_shutdown_commands) == 0:
        open(lockdown_file, 'a').close()
        print("Lockdown file created.")
    else:
        print("Failed to run shutdown commands.")

# If the last 3 lines of the log file contains 'SUCCESS' and ./lockdown.file exists
elif check_last_n_lines(ceph_connections_status_file, 'SUCCESS', 3) and os.path.exists(lockdown_file):
    print("Last 3 lines contain 'SUCCESS' and lockdown file exists. Initiating startup sequence.")
    if run_commands(ceph_startup_commands) == 0:
        os.remove(lockdown_file)
        print("Lockdown file removed.")
    else:
        print("Failed to run startup commands.")
        sys.exit(1)

# If the last line of the log file contains 'SUCCESS' and ./lockdown.file does not exist
elif check_last_n_lines(ceph_connections_status_file, 'SUCCESS', 1) and not os.path.exists(lockdown_file):
    print("Last line contains 'SUCCESS' and lockdown file does not exist. Checking mount points.")
    if not check_mounts(ceph_mount_points):
        print("Mount point check failed. Initiating shutdown sequence.")
        if run_commands(ceph_shutdown_commands) == 0:
            open(lockdown_file, 'a').close()
            print("Lockdown file created.")
        sys.exit(1)
    else:
        print("Mount point check succeeded.")
        sys.exit(0)
