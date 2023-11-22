#!/bin/bash

# Define the mode variable ('all' or 'today')
mode=$1

# Today's date in the format that matches your log files
today=$(date +"%Y-%m-%d")

# Create a datetime stamped folder
folder_name="export_$(date +"%Y-%m-%d_%H:%M:%S")"
mkdir "$folder_name"

# List of hosts
hosts=('ceph01.penholder.xyz' 'ceph02.penholder.xyz' 'ceph03.penholder.xyz')

# Loop through each host
for host in "${hosts[@]}"; do
    echo "Processing host: $host"

    # Create a local folder for the host
    echo "Creating local folder for $host"
    mkdir "$folder_name/$host"

    # Copy the remote script to the host
    echo "Copying remote script to $host"
    scp remote_script.sh "$host:/tmp/"

    # Execute the remote script on the host
    echo "Executing remote script on $host"
    ssh "$host" "bash /tmp/remote_script.sh $mode"

    # Copy the logs from the remote host
    echo "Copying logs from $host"
    scp -r "$host:/tmp/logs/*.log" "./$folder_name/$host"

    # Remove the logs from the remote host
    echo "Removing logs from $host"
    ssh "$host" "rm -f /tmp/logs/*.log"

    # Remove the remote script from the remote host
    echo "Removing remote script from $host"
    ssh "$host" "rm -f /tmp/remote_script.sh"
done

echo "Logs have been copied to $folder_name"
