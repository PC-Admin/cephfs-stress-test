#!/bin/bash

# Define the mode variable ('all' or 'today')
mode=$1

# Make a local folder for the logs
mkdir /tmp/logs/

# Find and copy Ceph log files
cp /var/log/ceph/*.log /tmp/logs/
cp /var/log/ceph/*/*.log /tmp/logs/

# Extract and copy Docker container logs
docker ps -a | grep 'ceph' | grep -E 'mgr|mds|crash|mon' | awk '{print $NF}' | while read container_name; do
    # Extract logs from each container and save them to a temporary file
    if docker logs "$container_name" >& "/tmp/logs/${container_name}.log"; then
        echo "Logs extracted for $container_name"
    else
        echo "Failed to extract logs for $container_name"
    fi
done

echo "All logs have been copied to /tmp/logs/ on the remote host."
