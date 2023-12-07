import socket
import subprocess
import logging
import yaml
import sys

# Loads the configuration from a YAML file.
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Checks if a connection to a specific host and port can be established.
def check_connection(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except:
        return False

# Determines if a majority of the provided hosts can be connected to on a specific port.
def majority_connected(hosts, port):
    successful_connections = sum(check_connection(host, port) for host in hosts)
    print(successful_connections)
    return successful_connections >= len(hosts) // 2 + 1

# Checks if the last line of a log file contains a specific message.
def check_last_log_entry(log_file, connection_failure_message):
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
            if not lines:
                return False
            last_line = lines[-1]
            return connection_failure_message in last_line
    except FileNotFoundError:
        return False

# Main function where the script execution begins.
def main():
    # Load configuration settings from the YAML file.
    config = load_config("config.yaml")

    # Set up logging with specified format and timestamps.
    logging.basicConfig(
        filename=config['log_file_location'], 
        level=logging.INFO, 
        format='%(asctime)s %(levelname)s: %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Define the message indicating a connection failure.
    connection_failure_message = "Majority of Ceph monitors are NOT reachable."

    # Checks if the 'reset' argument is provided in the command line.
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        print("Reset argument detected, skipping last log entry check...")
    else:
        # Check the last line of the log file for a specific failure message.
        if check_last_log_entry(config['log_file_location'], connection_failure_message):
            print("Exiting: The last script run detected a connection issue with Ceph monitors.")
            return

    # Check if the majority of Ceph monitors are reachable.
    if majority_connected(config['ceph_monitors'], config['port']):
        logging.info("The majority of Ceph monitors are reachable.")
    else:
        # Log and perform actions if the majority of Ceph monitors are not reachable.
        logging.info("The majority of Ceph monitors could not be reached. Stopping Tomcat and unmounting Ceph...")
        # Attempt to stop Tomcat using systemctl.
        result = subprocess.run(["sudo", "/usr/bin/systemctl", "stop", "tomcat9"], check=False, capture_output=True, text=True)
        # Log the result of the Tomcat stop attempt.
        if result.returncode == 0:
            logging.info("Tomcat has been stopped successfully.")
        elif result.returncode != 0:
            logging.error(f"Error stopping Tomcat: {result.stderr}")

        # Attempt to unmount CephFS using umount command.
        result = subprocess.run(["sudo", "/usr/bin/umount", "--lazy", config['cephfs_mount_path']], check=False, capture_output=True, text=True)
        # Log the result of the umount attempt.
        if result.returncode == 0:
            logging.info(f"CephFS at {config['cephfs_mount_path']} has been unmounted successfully.")
        elif result.returncode != 0:
            # Specific handling for the 'not mounted' scenario.
            if "not mounted" in result.stderr:
                logging.info(f"CephFS at {config['cephfs_mount_path']} is not mounted. No action needed.")
            else:
                logging.error(f"Error unmounting CephFS: {result.stderr}")

        # Log the need for manual intervention.
        logging.error("Majority of Ceph monitors are NOT reachable. This script needs to be manually run with the 'reset' argument to proceed.")

# Execute the main function.
main()
