#!/bin/bash

# Go to our workspace
cd /home/ros_ws

# Create src if it doesn't exist
mkdir -p src

# Build the workspace
colcon build

# Add the local source to the .bashrc so we don't have to type it every time
if ! grep -q "source /home/ros_ws/install/setup.bash" ~/.bashrc; then
    echo "source /home/ros_ws/install/setup.bash" >> ~/.bashrc
fi

echo "Workspace built and sourced!"