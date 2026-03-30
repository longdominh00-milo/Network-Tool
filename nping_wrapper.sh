#!/bin/bash

# Parse arguments
TARGET=$1
COUNT=$2
PORT=4200  # Change this to the desired port

# Run NPing and capture the output
OUTPUT=$(nping --udp -p $PORT -c $COUNT $TARGET 2>&1)

# Extract the average RTT (in milliseconds)
AVG_RTT=$(echo "$OUTPUT" | grep -oP 'Avg rtt: \K[0-9.]+')

# Output the result in SmokePing format
if [[ -n "$AVG_RTT" ]]; then
	    echo "$AVG_RTT"
    else
	        echo "U"
fi
