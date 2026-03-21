# ROS 2 Jazzy Development Environment (AMD GPU + WSLg)

## 🛠 System Requirements
- **Host:** Windows 11 with WSL2 (Ubuntu 22.04 or 24.04).
- **GPU:** AMD Radeon (RX 580) via `/dev/dxg` passthrough.
- **Docker Image:** `ros2-jazzy-gpu` (built from our custom Dockerfile).

## 🚀 How to Start Environment

### 1. Recommended: VS Code Dev Containers (Best Experience)
1. Open the project in VS Code.
2. Press `F1` or `Ctrl+Shift+P`.
3. Select **"Dev Containers: Reopen in Container"**.
   - *This automatically starts the container and sources your workspace.*

### 2. Manual: Terminal (Interactive or Background)
- **Interactive:**
  ```bash
  bash run_ros.sh
  ```
- **Background (Detached):**
  ```bash
  bash run_ros.sh -d
  ```

---

## 📦 Workspace & Packages
... (rest of the file)

### Packages
- **my_robot_controller**: A Python package containing basic ROS 2 nodes.
    - `test_node`: A simple node that logs "Hello ROS2!" and has a 1-second timer callback.

### Building the Workspace
Inside the container, run:
```bash
colcon build --packages-select my_robot_controller
```

### Running the Node
1. **Source the workspace:**
   ```bash
   source install/setup.bash
   ```
2. **Run the test node:**
   ```bash
   ros2 run my_robot_controller test_node
   ```

### Setup Scripts
1. **`run_ros.sh`**: Starts the Docker container with GPU support.
2. **`setup_workspace.sh`**: (If available) Initial workspace configuration.

### How to use these right now:
1. Save the scripts in `~/repos/ros/`.
2. Make them executable:
   ```bash
   chmod +x ~/repos/ros/run_ros.sh
   chmod +x ~/repos/ros/setup_workspace.sh
   ```