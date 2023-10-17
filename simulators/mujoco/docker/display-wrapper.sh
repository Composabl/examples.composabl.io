#!/bin/bash

# Check if the script argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <script-to-execute>"
    exit 1
fi

# Set the path to your script
script="$1"

# Start a virtual X server using Xvfb
Xvfb :99 -screen 0 1024x768x24 -ac &

# Set the DISPLAY environment variable to the virtual screen
export DISPLAY=:99

# Run the specified script
bash "$script"

# Terminate the virtual X server when the script is done
killall Xvfb
