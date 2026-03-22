# 🤖 My Robot Description Package

This package contains the **URDF** (Unified Robot Description Format) models for the Double Pendulum project.

---

## 🚀 How to Visualize a Robot

To see a robot model in RViz2, follow this "Two-Step" command pattern to avoid terminal parsing errors.

### 1. Load the URDF into a variable
```bash
MY_URDF=$(xacro src/my_robot_description/urdf/my_robot.urdf)
```

### 2. Start the Publisher
```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$MY_URDF"
```

### 3. Open RViz2 (In a new terminal)
```bash
rviz2
```
*Note: In RViz, you must change the **Fixed Frame** to `base_link` and add the **RobotModel** display.*

---

## 🛠 Lessons Learned & Troubleshooting

### 1. "Permission Denied" when running URDF
**Problem:** `ros2 run ... robot_description="$(path/to/file.urdf)"`
**Cause:** The shell tries to *execute* the XML file like a script.
**Solution:** Use the `xacro` tool to read the file contents: `$(xacro path/to/file.urdf)`.

### 2. Missing GUI Tools (rviz2, gazebo)
**Problem:** `rviz2: command not found`
**Cause:** The base `ros:jazzy-desktop` image is lightweight and missing several GUI packages.
**Solution:** Updated the `Dockerfile` to explicitly install `ros-jazzy-rviz2`, `ros-jazzy-ros-gz`, and `ros-jazzy-joint-state-publisher-gui`.

### 3. Invisible Robot in RViz
**Problem:** RViz opens but the 3D view is empty.
**Solution:** 
- Change **Fixed Frame** from `map` to `base_link`.
- Ensure the **RobotModel** display is added.
- Verify the `/robot_description` topic is active using `ros2 topic list`.

---

## 📂 File Structure
- `urdf/my_robot.urdf`: Milestone 1 - Simple floating box.
- `urdf/two_links.urdf`: Milestone 2 - Base box with a rotating cylinder arm.
