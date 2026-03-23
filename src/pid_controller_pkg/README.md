# 🎮 PID Controller Package

This package is dedicated to the implementation and tuning of **PID (Proportional-Integral-Derivative)** controllers for robotic systems in ROS 2.

---

## 🧠 What is a PID Controller?

A PID controller is a control loop feedback mechanism widely used in industrial control systems and robotics. It continuously calculates an **error value** as the difference between a desired setpoint and a measured process variable.

### The Three Terms:
1.  **P (Proportional):** Produces an output that is proportional to the current error. If the error is large, the control output is large.
    -   *Formula:* `output = Kp * error`
2.  **I (Integral):** Concerned with the accumulation of past errors. If the error has been persisting for a long time, the integral term increases the output to eliminate the residual error.
    -   *Formula:* `output = Ki * Σ(error * dt)`
3.  **D (Derivative):** Predicts future error based on its current rate of change. It provides "damping" to reduce overshoot and oscillation.
    -   *Formula:* `output = Kd * (d_error / dt)`

**Total Output:** `Effort = (Kp * error) + (Ki * integral) + (Kd * derivative)`

---

## 🛠 Lessons Learned: Bridging the ROS-Gazebo Gap

Connecting a ROS 2 node to a Gazebo simulation is often the most difficult part of robot development due to **Namespace Isolation**.

### 1. The "Hidden Ear" (Gazebo Transport)
Gazebo plugins (like `ApplyJointForce`) listen to internal **Gazebo Transport** topics, not ROS 2 topics. 
- **The Discovery:** We used `gz topic -l` to see every "ear" inside the simulation.
- **The Finding:** The plugin was actually listening at `/model/chaos_robot/joint/slider_joint/cmd_force`, regardless of what we named our ROS topic.

### 2. The Bridge as a "Translator"
The `ros_gz_bridge` doesn't just copy data; it acts as a mapping layer.
- **Remapping:** By using `remappings=[('/long/gazebo/path', '/short_ros_topic')]`, we kept our ROS code clean while satisfying Gazebo's strict naming requirements.

### 3. Physics vs. Control
- **Collision is Key:** A link without a `<collision>` tag may be ignored by the physics solver even if it has mass.
- **Zero-Friction Testing:** When a joint won't move, always zero out `<dynamics damping="0" friction="0"/>` to determine if the issue is your **Control Signal** (the bridge) or **Mechanical Resistance** (friction).

---

## 📂 Package Structure
- `pid_node.py`: The main Python node implementing the PID logic.
- `launch/`: Launch files for starting the controller and simulation.
- `urdf/`: Robot models specifically configured for effort control.

---

## 🚀 Getting Started

### 1. Build the package
```bash
colcon build --packages-select pid_controller_pkg
source install/setup.bash
```

### 2. Run the PID Node
```bash
ros2 run pid_controller_pkg pid_node
```

### 3. Tuning Parameters at Runtime
We use ROS 2 Parameters so you can tune your gains without restarting the node:
```bash
ros2 param set /pid_controller kp 15.0
ros2 param set /pid_controller ki 0.2
ros2 param set /pid_controller kd 1.0
```

---

## 🛠 Lessons Learned
- **Sampling Time (dt):** Real-time stability depends on a consistent time step.
- **Saturation:** Real motors have limits. It's important to "cap" the output effort so the simulation doesn't explode.
- **Wind-up:** Large integral values can cause issues; "Integral Anti-Windup" is a key professional concept to implement.
