# 🐳 Docker & VS Code Setup Guide

This guide explains how to set up, build, and run your ROS 2 Jazzy environment using Docker and VS Code.

---

## 📋 Prerequisites
- **Windows 11 with WSL2** (Ubuntu 22.04 or 24.04 recommended).
- **AMD GPU** (RX 580 or similar) for hardware acceleration via `/dev/dxg`.
- **Docker Desktop** or **Docker Engine** installed in WSL2.

---

## 🛠 Step 1: Build the Docker Image

Before running the container, you must build the image from the provided `Dockerfile`. Open your WSL terminal and run:

```bash
cd ~/repos/ros
docker build -t ros2-jazzy-gpu .
```

---

## 🚀 Step 2: Run the ROS 2 Container

Use the `run_ros.sh` script to start the container. This script handles all the necessary volume mappings for GPU support and GUI (WSLg) passthrough.

### Interactive Mode
```bash
bash run_ros.sh
```

### Background (Detached) Mode
To start the container in the background and use it later:
```bash
bash run_ros.sh -d
```
Then access it with:
```bash
docker exec -it ros_dev bash
```

---

## 💻 Step 3: VS Code Dev Containers (Best Practice)

To get IntelliSense, debugging, and an integrated terminal inside the container:

1. **Install Extensions:**
   - [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - [ROS](https://marketplace.visualstudio.com/items?itemName=ms-iot.vscode-ros) (Optional, but highly recommended)

2. **Open the Project:**
   - Open `~/repos/ros` in VS Code.

3. **Reopen in Container:**
   - Press `F1` or `Ctrl+Shift+P`.
   - Select **"Dev Containers: Reopen in Container"**.
   - VS Code will use your `Dockerfile` to create a dedicated development environment.

---

## 📦 Step 4: Building & Running Nodes

Once inside the container (either via `run_ros.sh` or VS Code), follow these steps:

### Initial Workspace Setup
If it's your first time, run the setup script:
```bash
bash setup_workspace.sh
```

### Build a Specific Package
```bash
colcon build --packages-select my_robot_controller
```

### Source the Workspace
```bash
source install/setup.bash
```

### Run the Test Node
```bash
ros2 run my_robot_controller test_node
```

---

## 💡 Troubleshooting

- **"Command not found" for `ros2`:** Make sure you've sourced the setup files. The `Dockerfile` handles the main ROS install, and `install/setup.bash` handles your local packages.
- **GUI not appearing:** Ensure WSLg is working correctly by running `xeyes` in your WSL terminal before starting the container.
- **GPU issues:** Verify `/dev/dxg` exists in your WSL environment (`ls /dev/dxg`).
