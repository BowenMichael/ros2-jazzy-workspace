# 🤖 My Robot Description Package

This package contains the **URDF** (Unified Robot Description Format) models for the Double Pendulum project.

---

## 🚀 How to Visualize a Robot

### Option 1: Automatic Launch (Recommended)
This single command starts the `robot_state_publisher`, the `joint_state_publisher_gui`, and `rviz2` with your saved configuration.

```bash
ros2 launch my_robot_description display.launch.py
```

### Option 2: Manual Visualization
If you want to run things manually (for debugging):
1. **Load URDF:** `MY_URDF=$(xacro src/my_robot_description/urdf/two_links.urdf)`
2. **Start Publisher:** `ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$MY_URDF"`
3. **Open RViz:** `rviz2`

---

## 🎨 Saving Your Workspace State
1. Open RViz and configure your displays (Fixed Frame, RobotModel, TF).
2. Go to **File > Save Config As**.
3. Save to: `src/my_robot_description/config/view_robot.rviz`.
4. The launch file will now automatically load this state every time!

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

## 📂 File Structure (Iterative Progress)
- `urdf/my_robot.urdf`: **Milestone 1** - Simple floating box (Visuals only).
- `urdf/two_links.urdf`: **Milestone 2** - Base box with a rotating cylinder arm (Visuals only).
- `urdf/m3_drop_test.urdf`: **Milestone 3** - Added `<inertial>` and `<collision>` tags for physical simulation in Gazebo.
