# 🚧 Work in Progress: Advanced Control Project

This file tracks the transition from physics analysis to active robotic control.

---

## ✅ Completed Recently
1.  **Chaos Experiment:** Successfully proved determinism in Gazebo via automated MCAP recordings and Python analysis.
2.  **PID Setup:** Created `pid_controller_pkg` and successfully established a bridge between ROS 2 `/slider_cmd` and Gazebo's `ApplyJointForce` plugin.
3.  **1D Control:** Confirmed the blue base can move along the rail via manual force commands and basic PID logic.
4.  **Roadmap:** Created `CONTROL_ROADMAP.md` to track Stage 1-5 of the control evolution.

## ⏸️ Current Status
-   **Stage 1 (1D Linear Control):** The PID loop is active but currently oscillating ("yo-yoing"). 
-   **Tuning needed:** Current gains are `kp=10.0`, `ki=0.0`, `kd=1.0`. High overshoot detected.

## ⏭️ Next Steps
1.  **Tune Stage 1:** Stabilize the slider joint by increasing `kd` (D-gain) to dampen oscillations.
2.  **Implement Stage 2:** Add force control to the first pendulum joint (`pendulum_joint`) to begin angular control.
3.  **Refactor:** Add a GUI (rqt_configure) to make setpoint changes easier during tuning.

---

## 📝 Notes
-   The bridge for the slider is: `/model/chaos_robot/joint/slider_joint/cmd_force` remapped to `/slider_cmd`.
-   Remember to unpause Gazebo before testing PID!
