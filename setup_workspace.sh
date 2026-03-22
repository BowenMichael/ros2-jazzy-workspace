#!/bin/bash

# Define the workspace directory inside the container
WORKSPACE_DIR="/home/ros_ws"
cd $WORKSPACE_DIR

# 1. Ensure the source directory exists
mkdir -p src

# 2. Build the entire workspace using colcon
# This creates the 'build', 'install', and 'log' directories
colcon build

# 3. Automatic Sourcing (The "Quality of Life" step)
# This adds a line to your .bashrc so that every new terminal automatically
# knows about your local packages (source install/setup.bash)
if ! grep -q "source $WORKSPACE_DIR/install/setup.bash" ~/.bashrc; then
    echo "source $WORKSPACE_DIR/install/setup.bash" >> ~/.bashrc
    echo "Successfully added workspace sourcing to .bashrc"
fi

# Explicitly source in the current session
source $WORKSPACE_DIR/install/setup.bash

echo "Workspace build complete! Open a new terminal to start using your packages."