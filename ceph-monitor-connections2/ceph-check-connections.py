import socket
import yaml
import sys

# This script checks if the majority of Ceph monitors can be reached and return a 0 for success or 1 for failure.

# Loads the configuration from a YAML file.
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Checks if a connection to a specific host and port can be established.
def check_connection(host):
    try:
        with socket.create_connection((host, 6789), timeout=5):
            return True
    except:
        return False

# Determines if a majority of the provided hosts can be connected to on a port 6789.
def majority_connected(hosts):
    successful_connections = sum(check_connection(host) for host in hosts)
    print(f"Successful connections: {successful_connections} out of {len(hosts)}")
    return successful_connections >= len(hosts) // 2 + 1

# Load configuration settings from the YAML file.
config = load_config("config.yaml")

# Check if the majority of Ceph monitors are reachable.
if majority_connected(config['ceph_monitors']):
    print("The majority of Ceph monitors are reachable.")
    sys.exit(0)
else:
    print("Majority of Ceph monitors are NOT reachable.")
    sys.exit(1)