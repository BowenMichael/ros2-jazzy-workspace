# 🤖 ROS 2 & Poetry Workflow

This repository uses a hybrid dependency management strategy to keep your ROS 2 environment clean and your analysis scripts powerful.

---

## 🏗️ The "Two-World" Architecture

We maintain a separation between the ROS 2 system-level environment and your project-specific Python dependencies.

### 1. The ROS 2 Layer (Communication)
Managed by `colcon`. Used for your robot nodes (publishers, subscribers, services). 
- These rely on the system-level Python environment provided by ROS 2 Jazzy.
- **Run with:** `ros2 run <package> <node>` or `ros2 launch <package> <launch_file>`

### 2. The Poetry Layer (Analysis & Logic)
Managed by `poetry`. Used for your heavy data-science/analysis scripts (e.g., `compare_runs.py`).
- These rely on specific versions of libraries like `pandas`, `numpy`, and `matplotlib`.
- **Run with:** `poetry run python3 <script.py>`

---

## 🚀 How to Combine Both (The "Bridge" Workflow)

When you need an analysis script to *also* be a ROS 2 node (or use ROS 2 messages), combine the environments:

```bash
# 1. Source your ROS 2 workspace to get ROS 2 libraries (e.g., rclpy)
source /home/ros_ws/install/setup.bash

# 2. Run your script via Poetry to get your data science libraries (e.g., pandas)
poetry run python3 src/chaos_experiment_pkg/scripts/compare_runs.py
```

---

## 🛠️ How to Add Dependencies

### ROS 2 Dependencies
Add these to your `package.xml` so `colcon` can manage them:
```xml
<depend>rclpy</depend>
<depend>sensor_msgs</depend>
```

### Python/Data Science Dependencies
Add these to your `pyproject.toml` using Poetry:
```bash
cd src/chaos_experiment_pkg
poetry add pandas matplotlib numpy rosbags
```
