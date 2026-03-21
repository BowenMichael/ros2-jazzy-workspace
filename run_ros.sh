#!/bin/bash

# Default mode is interactive
MODE="-it --rm"
NAME="ros_dev"

# Check for -d flag
if [[ "$1" == "-d" ]]; then
  MODE="-d"
  echo "Starting container in background (detached mode)..."
fi

# 1. Kill any old 'zombie' containers using this name
docker rm -f $NAME 2>/dev/null

# 2. Launch the container with GPU, GUI, and Volume support
docker run $MODE \
  --name $NAME \
  --net=host \
  --device /dev/dxg \
  -v /usr/lib/wsl:/usr/lib/wsl \
  -v /mnt/wslg:/mnt/wslg \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ~/repos/ros:/home/ros_ws \
  --env="DISPLAY=$DISPLAY" \
  ros2-jazzy-gpu