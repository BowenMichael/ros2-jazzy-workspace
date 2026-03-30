# 🧪 Lab Assignment: Modular Cascaded Control

This worksheet focuses on building a professional, modular control architecture by "stringing together" generic PID building blocks to solve the Cart-Pole balancing problem.

---

## 🏗️ The Modular Architecture
Instead of one "smart" node, we use two "generic" nodes:
1.  **Outer Node (Angle):** Listens to Angle -> Outputs Desired Cart Velocity.
2.  **Inner Node (Velocity):** Listens to Desired Cart Velocity -> Outputs Motor Force.

---

## 🚀 Phase 1: The Universal PID Upgrade
**Goal:** Upgrade the `pid_controller` node to be a "Plug-and-Play" component.

### 1.1 Dynamic Setpoint Input
Currently, the node only reads a static `setpoint` parameter. To "string" them together, it must be able to listen to a topic.
- **Task:** Add a subscriber to a generic topic called `setpoint_topic` using the `std_msgs/msg/Float64` type.
- **Initialization Logic:** Use the `setpoint` parameter to set the **initial** value of an internal variable (e.g., `self.setpoint`) in the `__init__` method.
- **Callback Logic:** Create a `setpoint_callback` that overwrites `self.setpoint` whenever a new message arrives. This allows the topic to override the parameter at runtime.
- **PID Loop Logic:** Update the `handle_pid` function to use the internal `self.setpoint` variable instead of calling `get_parameter('setpoint')` on every tick.

### 1.2 Multi-Input Support (Position vs. Velocity)
This update allows the node to act as either a "GPS" (Position) or a "Cruise Control" (Velocity).
- **Task:** Declare a boolean parameter named `use_velocity_feedback` (default: `False`) in the `__init__` method.
- **Callback Logic:** Update the `joint_state_callback` to check this parameter:
  - If **False**: Read feedback from `msg.position[idx]`.
  - If **True**: Read feedback from `msg.velocity[idx]`.
- **Naming Note:** Ensure your internal variable (e.g., `self.current_state`) receives whichever value is selected. The PID math will then automatically calculate either "Distance Error" or "Speed Error."
- **Logging:** Update the initialization log to state which mode the node is starting in (e.g., "PID initialized in VELOCITY mode").

### 1.3 The "Pass-Through" Publisher (Relative Topic Naming)
This is the final step in making the node a modular building block. It allows the output of the math loop to be "piped" into anything.
- **Task:** Update the `cmd_pub` initialization to use a **Relative Topic Name**.
- **The Detail:** Change the topic string from `/slider_cmd` (global) to `control_effort` (relative - no leading slash).
- **Why Relative?** Global topics (starting with `/`) are hard to remap because they ignore namespaces. Relative topics can be easily redirected in the launch file to either a hardware command topic (like `/slider_cmd`) or another node's input (like `setpoint_topic`).
- **Interface Logic:** Ensure the output remains a `std_msgs/msg/Float64`. This common interface is what allows Node A to talk to Node B without any specialized "handshake" code.
- **Result:** You have now created a **Transformation Node** that consumes a setpoint and feedback, and produces a control signal that can be remapped to any destination.

---

## 🚀 Phase 2: The Cascaded Wiring Challenge
**Goal:** Wire two PID nodes together in a single launch file to balance the pole.

### 2.1 Launch Configuration (The Wiring Diagram)
In ROS 2, `remappings` act like a "Patch Panel." They allow you to change the "Topic Name" of a node from the **outside** (in the launch file) without changing the Python code.

**The Cascaded Goal:**
Connect the **Output** of the Angle node to the **Input** of the Velocity node.

#### 🗺️ The Wiring Map:
| Connection | Node A (Angle) topic | Node B (Velocity) topic | Shared ROS Topic |
| :--- | :--- | :--- | :--- |
| **Feedback 1** | `joint_states` | | `/joint_states` |
| **Inter-loop** | `control_effort` (Output) | `setpoint_topic` (Input) | `/desired_velocity` |
| **Feedback 2** | | `joint_states` | `/joint_states` |
| **Final Output** | | `control_effort` (Output) | `/slider_cmd` |

#### 🛠️ Implementation Steps:
1.  **Unique Node Names:** You MUST give each node a unique name (e.g., `name='angle_pid_node'` and `name='velocity_pid_node'`). If they have the same name, ROS will get confused.
2.  **Angle Node Configuration:**
    - `joint_name`: "pendulum_joint"
    - `use_velocity`: False
    - `remappings`: `[('control_effort', '/desired_velocity')]`
3.  **Velocity Node Configuration:**
    - `joint_name`: "slider_joint"
    - `use_velocity`: True
    - `remappings`: `[('setpoint_topic', '/desired_velocity'), ('control_effort', '/slider_cmd')]`
4.  **The Bridge Connection:** Ensure your ROS bridge is still mapping the ROS `/slider_cmd` to the Gazebo force topic!

### 2.2 Tuning the Cascade (The Strategy)
1.  **Step 1:** Disable Node A. Manually send a velocity setpoint to Node B. Ensure the cart moves at exactly the speed you requested.
2.  **Step 2:** Enable Node A. Watch as the Angle loop "commands" the Velocity loop to catch the falling pole.

### 2.3 Cascaded Tuning Masterclass (The "How-To")
Tuning is an **iterative process**. To find the perfect gains, you need to be able to fail, reset, and try again in seconds.

#### 🔄 The Iteration Cycle
1.  **Hot-Reload Gains:** Do NOT restart the launch file to change gains. Use `ros2 param set` or `rqt_reconfigure`. The changes take effect the instant you hit Enter.
2.  **Reset the World:** If the pole falls or the cart hits the wall, use the Gazebo **"Reset World"** button (the rewind icon) or press `Ctrl+Shift+R`. This snaps the pendulum back to the top (3.14 rad) and the cart to the center (0.0m) instantly.
3.  **Analyze the "Why":** Before resetting, look at the cart. Did it move the *wrong* way? (Flip KP sign). Did it move but too slowly? (Increase KP). Did it shake? (Decrease KP or increase KD).

---

#### 🚦 Step 1: The Inner Loop (Velocity - "The Actuator")
*   **Concept:** You are making sure your "motor" can accurately hit a target speed.
*   **Action:** In your launch file, set all `angle_pid_node` gains to 0.0.
*   **Goal:** Make the cart responsive and "crisp" to velocity commands.
*   **Test:** `ros2 topic pub /desired_velocity std_msgs/msg/Float64 "{data: 0.5}"`
*   **Tuning Pattern:**
    - Increase **KP** until the cart moves quickly but doesn't "buzz."
    - Increase **KI** if the cart can't maintain speed against the rail friction.
    - Increase **KD** if the cart "jerks" when changing direction.

#### 🚦 Step 2: The Outer Loop (Angle - "The Balancer")
*   **Concept:** The angle node calculates how fast the cart *should* move to catch the pole.
*   **Action:** Keep the Inner Loop gains locked. Slowly increase `kp` on the `angle_pid_node`.
*   **Goal:** "Catch" the falling pendulum.
*   **The "Wobble" Test:**
    - **Too little KP:** The cart moves toward the fall, but the pole still hits the ground.
    - **Just right KP:** The pole stays up, but the system "hunts" (swings back and forth).
    - **Too much KP:** The cart vibrates violently, making a "chattering" sound.

#### 🚦 Step 3: Finding the "Golden Balance" (Derivative Damping)
*   **Action:** Increase **KD** on the `angle_pid_node` to stop the hunting/wobbling.
*   **The Brake:** KD acts like a virtual shock absorber. If the cart is "nervous," KD will calm it down.
*   **Success:** The pole stays vertical (3.14 rad) and the cart only makes tiny, smooth adjustments.

#### 🛠️ Troubleshooting Guide:
| Symptom | Diagnosis | Fix |
| :--- | :--- | :--- |
| **"The Slam"** | Cart hits the rail limit instantly. | Reverse the sign of your Angle KP (you might be pushing *away* from the fall). |
| **"The Jitter"** | Cart vibrates in place. | Lower the Inner Loop (Velocity) KP. |
| **"The Drift"** | Pole balances but the cart slowly wanders off the rail. | Add a tiny bit of "Position" feedback to the Outer Loop (Advanced). |

---

## 📝 Lab Progress Tracking
- [x] **Phase 1.1:** Dynamic Setpoint Subscriber Added
- [x] **Phase 1.2:** Velocity Feedback Support Added
- [x] **Phase 1.3:** Pass-Through Publisher Implemented
- [ ] **Phase 2.1:** Dual-Node Launch File Created
- [ ] **Phase 2.2:** System Balanced!
