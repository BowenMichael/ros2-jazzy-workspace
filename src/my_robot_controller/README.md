# 🎮 My Robot Controller Package

This package contains Python-based ROS 2 nodes developed while following the **[Robotics Back-end](https://www.youtube.com/watch?v=od3JwOeyEXc)** ROS 2 tutorials. It serves as my primary learning workspace for mastering ROS 2 fundamentals.

---

## 🎓 Course Acknowledgement
The following nodes were developed as part of the Robotics Back-end curriculum. While I have typed, tested, and troubleshot every line of code myself, the architectural design and logic are guided by the course's teaching materials.

---

## 🚀 Nodes in this Package

### 1. `my_first_node`
- **Purpose:** A basic "Hello ROS2" node.
- **Key Concepts:** Node initialization, logging (`get_logger`), and simple timers.
- **Run:** `ros2 run my_robot_controller first_node`

### 2. `draw_circle`
- **Purpose:** Publishes velocity commands to make the turtle move in a circle.
- **Key Concepts:** Publishers, `geometry_msgs/Twist`.
- **Run:** `ros2 run my_robot_controller draw_circle`

### 3. `pose_subscriber`
- **Purpose:** Subscribes to the turtle's pose and logs its position.
- **Key Concepts:** Subscribers, `turtlesim/msg/Pose`.
- **Run:** `ros2 run my_robot_controller pose_subscriber`

### 4. `turtle_controller` (Most Advanced)
- **Purpose:** Combines publishing and subscribing with service calls. It changes the turtle's pen color based on its position and forces it to turn when it hits a "wall."
- **Key Concepts:** Complex logic, `SetPen` service calls, multiple topics.
- **Run:** `ros2 run my_robot_controller turtle_controller`

---

## 🛠 Lessons Learned & Troubleshooting

### 1. Message Type Mismatches
**Problem:** `pose_subscriber` was connected to `/turtle1/pose` in `rqt_graph` but nothing was printing.
**Cause:** We were using `geometry_msgs/Pose` instead of the specialized `turtlesim/msg/Pose`.
**Solution:** Always check the exact message type using `ros2 topic info <topic_name>` before writing code.

### 2. File Naming & Permissions
**Problem:** Typo in filename (`pose_subsriber.py`) and "Permission denied" errors.
**Cause:** ROS 2 packages created with `ros2 pkg create` or within Docker may have root ownership.
**Solution:** Use `sudo chown -R $(id -u):$(id -g) src/` to regain ownership of your files.

---

## 📂 Common ROS 2 Debugging Commands

Use these to verify your nodes are working correctly:
- **List Topics:** `ros2 topic list`
- **Check Topic Info:** `ros2 topic info /turtle1/pose`
- **View Message Data:** `ros2 topic echo /turtle1/pose`
- **Visualize Graph:** `rqt_graph`
