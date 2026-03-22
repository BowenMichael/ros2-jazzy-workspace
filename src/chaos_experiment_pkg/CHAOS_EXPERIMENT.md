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

### Phase 1: Instrumentation (Complete)
- [x] **Add Gazebo Plugin:** Added `gz::sim::systems::JointStatePublisher` to `chaos_experiment.urdf`.
- [x] **Verify Topics:** Confirm streaming with: 
  `ros2 topic echo /joint_states`

### Phase 2: Data Collection (Pro Workflow)
- [x] **Record Run A:** Record 30 seconds of `/joint_states`.
  `ros2 bag record -o run_a /joint_states`
- [x] **Record Run B:** Reset Gazebo, then record a second run.
  `ros2 bag record -o run_b /joint_states`
- [x] **Inspect Bag Data:** Verify both bag files were created.
  `ros2 bag info run_a/`

### Phase 3: Analysis + automation
- [x] **Automate:** created a reliable automated test by starting gazebo automatically with -r
- [x] **Visualize:** Use matplotlib to plot the signals and measure the diverages
- [x] **Compare:** Compared angle graphs to see that the simulation is very repeatable and deterministic with the same inital conditions
