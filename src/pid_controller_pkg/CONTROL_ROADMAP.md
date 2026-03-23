# 🎯 Advanced Control & Setpoint Roadmap

This roadmap tracks the evolution of the PID controller from simple 1D linear movement to complex 3D end-effector positioning.

---

## 📍 Stage 1: 1D Linear Control (Linear Slide)
**Goal:** Control the `y` position of the base along the rail.
- [x] **Setup:** Connect ROS 2 `/slider_cmd` to Gazebo force plugin.
- [ ] **Dynamic Setpoint:** Create a node or use `ros2 param` to change the target `y` position at runtime.
- [ ] **Mapping:** Update the PID controller to use the dynamic setpoint for the `slider_joint`.
- **Success:** The blue box moves to and holds a specific `y` coordinate on the rail.

## 📍 Stage 2: 1D Angular Control (Single Pendulum)
**Goal:** Control the angle of the first arm.
- [ ] **Instrumentation:** Add a force plugin to the `pendulum_joint`.
- [ ] **PID Mapping:** Reconfigure the PID node to target a specific angle (e.g., "Balance at 0.0 rad").
- **Success:** The green arm moves to a set angle and resists gravity.

## 📍 Stage 3: Chained 1D Control (Double Pendulum)
**Goal:** Control the tip of the second arm using joint angles.
- [ ] **Nested Loops:** Implement two PID loops—one for each pendulum joint.
- [ ] **Sequential Setpoints:** Set a target angle for joint 1, then joint 2.
- **Success:** Both arms move to a specific "pose" defined by two angles.

## 📍 Stage 4: 2D Spatial Control (XY Plane)
**Goal:** Control the End-Effector (tip) position in 2D space.
- [ ] **Inverse Kinematics (IK):** Write a node that translates a desired `(x, y)` coordinate into required joint angles.
- [ ] **Setpoint Mapping:** Feed the IK output into the joint PID controllers.
- **Success:** The tip of the red arm moves to a specific `(x, y)` point in the plane.

## 📍 Stage 5: 3D Spatial Control (XYZ Space)
**Goal:** Full 3D positioning of the end-effector.
- [ ] **Full 3-Axis IK:** Expand the math to include the linear slide (`y`), and the two pendulum joints (`x`, `z`).
- [ ] **Dynamic Tracking:** Follow a moving 3D setpoint (e.g., a circle in space).
- **Success:** The robot tip follows a 3D trajectory across all three axes.

---

## 🛠️ Implementation Strategy
1.  **Phase 1 (Current):** Use `ros2 param set` for manual setpoint testing.
2.  **Phase 2:** Use `rqt_configure` for a GUI-based slider setpoint.
3.  **Phase 3:** Create a `teleop_setpoint` node to publish desired coordinates over a topic.
