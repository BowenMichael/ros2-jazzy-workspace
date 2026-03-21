# 🛡️ ROS 2 Development Best Practices

Guidelines for building robust, professional-grade ROS 2 systems.

---

## 🚦 The Topic Safety Hierarchy

When designing nodes, prioritize flexibility and reliability in how you handle topic names:

1.  **Hard-coded Strings** (❌ Avoid): `self.create_subscription(Pose, "/turtle1/pose", ...)`
    - *Problem:* Fragile. If the topic name changes in the simulator, you must change your source code.
2.  **Class Constants** (⚠️ Better): `TOPIC_NAME = "/turtle1/pose"`
    - *Benefit:* Changes happen in one place, but still requires a rebuild.
3.  **ROS 2 Parameters** (✅ Recommended): `self.declare_parameter("pose_topic", "/turtle1/pose")`
    - *Benefit:* Configurable at runtime without touching the code. Demonstrates high-level ROS 2 knowledge.
4.  **Launch File Remapping** (🏆 Best): Use a generic name like `"pose"` in code and "map" it in a launch file.
    - *Benefit:* Centralizes all configuration. Allows one node to be reused for many different robots.

---

## 🔍 The "Triple Check" Workflow

Before writing any subscriber or publisher, run these three commands to avoid **Message Type Mismatch** errors:

1.  **List Topics:** `ros2 topic list`
    - *Verify:* Is the topic actually active?
2.  **Check Type:** `ros2 topic info <topic_name>`
    - *Verify:* What is the **exact** message type? (e.g., `turtlesim/msg/Pose` vs. `geometry_msgs/msg/Pose`)
3.  **Inspect Interface:** `ros2 interface show <type_name>`
    - *Verify:* What are the internal fields? (`x`, `y`, `theta`, etc.)

---

## 🛠️ Debugging "Invisible" Messages

If your node is connected in `rqt_graph` but not printing logs:
- **Check for Type Mismatch:** Use `ros2 topic info` on both the publisher and subscriber side.
- **Check QoS Settings:** Sometimes incompatible Quality of Service (QoS) profiles (e.g., Reliable vs. Best Effort) can block data flow.
- **Echo the Topic:** Run `ros2 topic echo <topic_name>` to confirm data is actually being published.
