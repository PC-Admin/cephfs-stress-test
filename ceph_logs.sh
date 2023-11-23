#!/bin/bash

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

    # Copy the Ceph log files from the host
    echo "Copying Ceph log files from $host"
    scp "$host:/var/log/ceph/*.log" "./$folder_name/$host"
    scp "$host:/var/log/ceph/*/*.log" "./$folder_name/$host"

    # Get the list of ceph container names from the host
    IFS=$'\n' read -r -d '' -a container_names < <( ssh "$host" "docker ps -a | grep 'ceph' | grep -E 'mgr|mds|crash|mon|osd' | awk '{print \$NF}'" && printf '\0' )

    # Iterate over each container name and extract the logs to the export folder
    for container_name in "${container_names[@]}"; do
        echo "Extracting logs for $container_name from $host"
        ssh "$host" "docker logs $container_name" > "./$folder_name/${host}/${container_name}.log" 2>&1
    done

done

echo "Logs have been copied to $folder_name"
