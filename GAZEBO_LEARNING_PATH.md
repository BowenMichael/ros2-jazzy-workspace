# 🎓 Gazebo & URDF Learning Path

This guide breaks down the complex world of ROS 2 simulation into achievable milestones.

---

## 📍 Milestone 1: The Floating Box (Complete)
**Goal:** Create a URDF and see it in RViz.
- [x] Create `my_robot_description` package.
- [x] Write a basic `.urdf` file with a single `<link>`.
- [x] Launch RViz and visualize the 3D shape.
- **Concepts:** `<link>`, `<visual>`, `<geometry>`, `<mesh>`.

## 📍 Milestone 2: The Hinge (In Progress)
**Goal:** Connect two links and move them manually.
- [x] Add a second link and a `<joint>`.
- [ ] Use `joint_state_publisher_gui` to rotate the joint.
- **Concepts:** `<joint>`, `revolute` vs `fixed`, `<axis>`, `<origin>`.

## 📍 Milestone 3: The "Drop Test"
**Goal:** Move from visualization to physics simulation.
- [ ] Add `<inertial>` (mass) and `<collision>` tags.
- [ ] Spawn the URDF into a Gazebo world.
- [ ] Watch the object fall due to gravity.
- **Concepts:** Physics, Mass, Inertia, Friction.

## 📍 Milestone 4: The Single Pendulum
**Goal:** A controlled simulation.
- [ ] Add a "base" link fixed to the world.
- [ ] Add a Gazebo plugin to the URDF.
- [ ] Observe the pendulum swinging naturally.
- **Concepts:** Gazebo Plugins, ROS-GZ Bridge, URDF vs SDF.

---

## 🏁 Final Goal: The Double Pendulum PID
Once these milestones are complete, we will combine everything to build and control the double pendulum.
