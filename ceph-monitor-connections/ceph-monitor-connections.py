import socket
import subprocess
import logging
import yaml
import sys

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_connection(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except:
        return False

def majority_connected(hosts, port):
    successful_connections = sum(check_connection(host, port) for host in hosts)
    print(successful_connections)
    return successful_connections >= len(hosts) // 2 + 1

def check_last_log_entry(log_file, connection_failure_message):
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
            if not lines:
                return False
            last_line = lines[-1]
            #print("last line: " + last_line)
            return connection_failure_message in last_line
    except FileNotFoundError:
        return False

def main():
    # Load config file
    config = load_config("config.yaml")

    # Configure logging with timestamps
    logging.basicConfig(
        filename=config['log_file_location'], 
        level=logging.INFO, 
        format='%(asctime)s %(levelname)s: %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    connection_failure_message = "Majority of Ceph monitors are NOT reachable."

    # Check for optional 'reset' argument
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        print("Reset argument detected, skipping last log entry check...")
    else:
        # Check if the last script run detected a connection issue with Ceph monitors
        if check_last_log_entry(config['log_file_location'], connection_failure_message):
            print("Exiting: The last script run detected a connection issue with Ceph monitors.")
            return

    if majority_connected(config['ceph_monitors'], config['port']):
        logging.info("The majority of Ceph monitors are reachable.")
    else:
        logging.info("The majority of Ceph monitors could not be reached. Stopping Tomcat and unmounting Ceph...")
        result = subprocess.run(["sudo", "/usr/bin/systemctl", "stop", "tomcat9"], check=False, capture_output=True, text=True) # Collect command output and avoid raising errors
        if result.returncode == 0:
            logging.info("Tomcat has been stopped successfully.")
        elif result.returncode != 0:
            logging.error(f"Error stopping Tomcat: {result.stderr}")

        result = subprocess.run(["sudo", "/usr/bin/umount", "--lazy", config['cephfs_mount_path']], check=False, capture_output=True, text=True) # Collect command output and avoid raising errors
        if result.returncode == 0:
            logging.info(f"CephFS at {config['cephfs_mount_path']} has been unmounted successfully.")
        elif result.returncode != 0:  # Check if there was an error
            if "not mounted" in result.stderr:
                logging.info(f"CephFS at {config['cephfs_mount_path']} is not mounted. No action needed.")
            else:
                logging.error(f"Error unmounting CephFS: {result.stderr}")

        logging.error("Majority of Ceph monitors are NOT reachable. This script needs to be manually run with the 'reset' argument to proceed.")

main()