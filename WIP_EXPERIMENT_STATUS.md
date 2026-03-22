# 🚧 Work in Progress: Chaos Experiment

This file tracks the current state of the Double Pendulum Chaos Experiment.

---

## ✅ Completed Today
1.  **URDF Setup:** Created `chaos_experiment.urdf` with the `libgazebo_ros_joint_state_publisher.so` plugin added.
2.  **Launch File:** Created `chaos_experiment.launch.py` which:
    -   Starts Gazebo in a **PAUSED** state.
    -   Removes the manual `joint_state_publisher_gui`.
    -   Launches RViz and the Robot State Publisher.
3.  **Documentation:** Created `CHAOS_EXPERIMENT.md` with a full roadmap and hypothesis.

## ⏸️ Current Status
-   The simulation launches correctly.
-   **Verification Pending:** We need to confirm that `/joint_states` topic is actually streaming data when Gazebo is unpaused.

## ⏭️ Next Steps (Tomorrow)
1.  **Create Separate Testing Package:**
    -   Create `chaos_experiment_pkg` to isolate the experiment logic from the robot description.
    -   Ideally, this package will depend on `my_robot_description` but allow for rapid iteration on data collection scripts without rebuilding the entire workspace.

2.  **Verify Data Flow:**
    -   Run: `ros2 launch my_robot_description chaos_experiment.launch.py`
    -   Hit "Play" in Gazebo.
    -   Run: `ros2 topic echo /joint_states` to confirm numbers are changing.

2.  **Phase 2: Data Collection**
    -   Record Run 1: `ros2 bag record -o run1 /joint_states`
    -   Record Run 2: `ros2 bag record -o run2 /joint_states`

3.  **Phase 3: Analysis**
    -   Plot the results to prove the "Butterfly Effect."

---

## 📝 Notes
-   The URDF has damping `0.01` and friction `0.01` for maximum chaos.
-   Both joints start at 90 degrees (1.57 rad).
