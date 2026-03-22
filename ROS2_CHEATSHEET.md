# 📋 ROS 2 Jazzy & Simulation Cheatsheet

A quick-reference guide for common commands used in this workspace.

---

## 🏗️ Workspace & Build
Always run these from the root of your workspace (`/workspaces/ros`).

| Command | Description |
| :--- | :--- |
| `colcon build --symlink-install` | Build all packages (symlinks allow Python edits without rebuild). |
| `source install/setup.bash` | Source your local workspace (essential for every new terminal). |
| `rm -rf build/ install/ log/` | "Nuclear Clean" - use this if build errors persist. |

---

## 🚀 Execution
| Command | Description |
| :--- | :--- |
| `ros2 launch <pkg> <file.launch.py>` | Start a complex system (e.g., `my_robot_description display.launch.py`). |
| `ros2 run <pkg> <executable>` | Start a single node. |
| `ros2 node list` | List all active nodes. |
| `ros2 node info /<node_name>` | See a node's subscribers, publishers, and services. |

---

## 📡 Topics & Data (Introspection)
| Command | Description |
| :--- | :--- |
| `ros2 topic list` | List all active topics. |
| `ros2 topic echo /<topic>` | View data streaming on a topic in real-time. |
| `ros2 topic info /<topic>` | **Crucial:** Check the Message Type of a topic. |
| `ros2 interface show <type>` | See the structure of a message (e.g., `sensor_msgs/msg/JointState`). |
| `ros2 topic hz /<topic>` | Check the actual frequency of data. |

---

## ⚙️ Parameters (Runtime Tuning)
Great for tuning PID gains without restarting code.

| Command | Description |
| :--- | :--- |
| `ros2 param list` | List all parameters for all nodes. |
| `ros2 param get /<node> <param>` | View a specific value (e.g., `kp`). |
| `ros2 param set /<node> <param> <val>` | Change a value instantly (e.g., `ros2 param set /pid_node kp 15.0`). |

---

## 🎒 Data Collection (Bags)
| Command | Description |
| :--- | :--- |
| `ros2 bag record -o <name> /<topic>` | Record data to a folder. |
| `ros2 bag info <folder>/` | Check how many messages were recorded. |
| `ros2 bag play <folder>/` | Playback the recorded data to the ROS network. |

---

## 🌍 Simulation & Tools
| Command | Description |
| :--- | :--- |
| `rviz2` | Open the 3D visualizer. |
| `rqt_graph` | View the "map" of how your nodes are talking. |
| `ros2 run tf2_ros tf2_echo <source> <target>` | Check the transform between two links. |
| `ros2 run joint_state_publisher_gui ...` | Open sliders to move robot joints manually. |

---

## 🛠️ Permissions Fix (Docker Specific)
If you hit "Permission Denied" when creating or editing files:
```bash
sudo chown -R $(id -u):$(id -g) .
```
