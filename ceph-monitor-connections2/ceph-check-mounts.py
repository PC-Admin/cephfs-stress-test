#!/usr/bin/env python3

import yaml
import sys
import os
import subprocess
from datetime import datetime, timedelta

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
    except OSError as e:
        print(f"OS error occurred while executing the command: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error occurred while executing the command: {e}")
        return 1

# Check and write to mount points.
def check_mounts(mount_points):
    for mount_point in mount_points:
        # Check if the mount point is mounted.
        if not os.path.ismount(mount_point):
            print(f"Warning: Mount point {mount_point} is not mounted.")
        # If it is mounted, check if the mount point is also writable.
        else:
            test_file_path = os.path.join(mount_point, "testCeph.txt")
            try:
                print(f"Checking and writing to mount point: {mount_point}")
                # Running the write test as a separate process with a 30 second timeout
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

# Load the lockdown file state.
def load_lockdown_state(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
            if data:
                return yaml.safe_load(data)
            else:
                return {"attempts": 0, "last_attempt": datetime.min}
    return None

# Save the lockdown file state.
def save_lockdown_state(file_path, state):
    with open(file_path, 'w') as file:
        yaml.dump(state, file)

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return b

# Load configuration from the YAML file.
config = load_config("config.yaml")

ceph_connections_status_file = config["ceph_connections_status_file"]
ceph_shutdown_commands = config["ceph_shutdown_commands"]
ceph_startup_commands = config["ceph_startup_commands"]
ceph_mount_points = config["ceph_mount_points"]

lockdown_file = './lockdown.file'
lockdown_state = load_lockdown_state(lockdown_file)

print("Checking last lines in ceph-connections.status file for SUCCESS or FAIL.")
fail_once = check_last_n_lines(ceph_connections_status_file, 'FAIL', 1)
success_once = check_last_n_lines(ceph_connections_status_file, 'SUCCESS', 1)
success_thrice = check_last_n_lines(ceph_connections_status_file, 'SUCCESS', 3)

lockdown_mode = os.path.exists(lockdown_file)

# If the last line of the log file contains 'FAIL' and ./lockdown.file does not exist, attempt to run the shutdown commands
if fail_once and not lockdown_mode:
    print("Last line contains 'FAIL' and lockdown file does not exist. Initiating shutdown sequence.")
    if run_commands(ceph_shutdown_commands) == 0:
        open(lockdown_file, 'a').close()
        print("Lockdown file created.")
        sys.exit(0)
    else:
        print("Failed to run shutdown commands.")
        sys.exit(1)

# If the last 3 lines of the log file contains 'SUCCESS' and ./lockdown.file exists, attempt to run the startup commands
elif success_thrice and lockdown_mode:
    print("Last line contains 'SUCCESS' and lockdown file exists.")
    # Calculate the next attempt time based on Fibonacci with a max of 13 minutes
    print(f'Backoff of {min(fibonacci(lockdown_state["attempts"]), 13)} minutes is required.')
    next_attempt = lockdown_state["last_attempt"] + timedelta(minutes=min(fibonacci(lockdown_state["attempts"]), 13))
    # If the next attempt time is in the past, run the startup commands
    if datetime.now() >= next_attempt:
        print("Attempting to run startup commands.")
        lockdown_state["attempts"] += 1
        lockdown_state["last_attempt"] = datetime.now()
        save_lockdown_state(lockdown_file, lockdown_state)
        # If the startup commands succeed, delete the lockdown file
        if run_commands(ceph_startup_commands) == 0:
            os.remove(lockdown_file)
            print("Lockdown file removed.")
            sys.exit(0)
        else:
            print("Failed to run startup commands.")
            sys.exit(1)
    else:
        print(f"Waiting for the next startup attempt based on the Fibonacci backoff schedule. Next attempt is allowed at: {next_attempt}")

# If the last line of the log file contains 'SUCCESS' and ./lockdown.file does not exist, check the mount points
elif success_once and not lockdown_mode:
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

# If the last line of the log file contains 'FAIL' and ./lockdown.file exists, we are already in lockdown mode and connections are still failing.
elif fail_once and lockdown_mode:
    print("Already in lockdown mode and connections are still failing.")
    sys.exit(0)

# If the last 3 lines of the log file don't contain 'SUCCESS' and ./lockdown.file exists, there hasn't been enough successful connections yet to enable startup.
elif not success_thrice and lockdown_mode:
    print("Not enough successful connections yet to enable startup.")
    sys.exit(0)