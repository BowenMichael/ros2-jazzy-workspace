# 🚧 Work in Progress: Advanced Control Project

This file tracks the transition from physics analysis to active robotic control.

---

## ✅ Completed Recently
1.  **Universal PID Node:** Upgraded the controller to be joint-agnostic with dynamic setpoints and multi-input (Pos/Vel) support.
2.  **Robust Simulation:** Successfully "baked" the robot into a custom Gazebo world (`pid_balancer.sdf`) to solve the "vanish on reset" issue.
3.  **PID Safeguards:** Implemented `dt` capping and effort saturation to handle simulation lag and prevent "math explosions."
4.  **Lab Curriculum:** Created `ADVANCED_CONTROL_LAB.md` to track the modular cascaded control roadmap.

## ⏸️ Current Status
-   **Stage 2 (Cascaded Control):** Architecture is implemented (Angle -> Velocity -> Force), but stability and communication issues with the linear slide were encountered.
-   **Strategic Decision:** The linear slide (Cart-Pole) adds significant complexity. We are moving to a **Fixed-Base Single Pendulum** for the next session to master basic 1D angular control before returning to the mobile base.

## ⏭️ Next Steps
1.  **Simpler Model:** Create a URDF/SDF for a pendulum arm mounted to a fixed point in space.
2.  **1D Tuning:** Use the universal PID node to hold the fixed pendulum at a set angle against gravity.
3.  **Re-Integrate Slide:** Once 1D angular control is rock-solid, re-introduce the linear slide for the full balancing challenge.

---

## 📝 Notes
-   The current "Baked-In" setup is working perfectly for rapid world resets.
-   Disabling Shared Memory (SHM) via `fastdds_noshm.xml` fixed the persistent `RuntimeError` in the PID node.
