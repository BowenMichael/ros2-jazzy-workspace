# 🌪️ The Double Pendulum Chaos Experiment

This experiment investigates the **determinism** of the Gazebo physics engine using a chaotic double pendulum system.

---

## 🧪 The Setup
We built a double pendulum robot in URDF with the following properties:
- **Link 1 (Green):** 0.5m length, 1.0kg mass.
- **Link 2 (Red):** 0.5m length, 1.0kg mass.
- **Joints:** Continuous rotation with low friction (`0.01`).
- **Initial State:** Both joints start at **90 degrees (1.57 rad)** to maximize potential energy.

## ❓ The Question
**Is the Gazebo simulation deterministic?**

If we run the exact same simulation twice, will the pendulum follow the **exact same path**? Or will tiny floating-point errors and solver iterations cause the trajectories to diverge?

## 📉 The Hypothesis
A double pendulum is a classic **Chaotic System**, meaning it is highly sensitive to initial conditions (The Butterfly Effect). We hypothesize that:
1.  **Short Term:** The trajectories will look identical for the first few seconds.
2.  **Long Term:** The paths will diverge significantly due to microscopic differences in the physics engine's time steps and constraint solver.

## 🛠️ The Experiment Plan
1.  **Instrument the Robot:** Add a Gazebo plugin to publish the exact joint angles to ROS 2 (`/joint_states`).
2.  **Run 1:** Launch the simulation and record the joint angles for 30 seconds.
3.  **Run 2:** Reset and repeat the recording.
4.  **Compare:** Plot the two datasets (Angle vs. Time) to see when they diverge.

---

## 🗺️ Experiment Roadmap

### Phase 1: Instrumentation (Current)
- [ ] **Add Gazebo Plugin:** Update `double_pendulum.urdf` to publish `/joint_states`.
- [ ] **Verify Topics:** Ensure joint angles are streaming to ROS 2.

### Phase 2: Data Collection
- [ ] **Run 1:** Record 30 seconds of `ros2 bag record` (Run A).
- [ ] **Run 2:** Record 30 seconds of `ros2 bag record` (Run B).

### Phase 3: Analysis
- [ ] **Visualize:** Use `rqt_plot` or Python to graph Angle vs. Time.
- [ ] **Compare:** Identify the exact time (t) where the trajectories diverge by > 1 degree.
