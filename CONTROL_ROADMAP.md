# 🎓 Control Masterclass: From PID to LQR

This roadmap is a step-by-step curriculum to move from simple feedback loops to modern optimal control.

---

## 📘 Phase 1: The PID "Deep-Dive"
**Goal:** Master the Proportional, Integral, and Derivative components in isolation.

1.  **Stage 1: 1D Linear Control (Complete)**
    - [x] **Task:** Move the blue box to a `y` position on the rail.
    - [x] **Lesson:** Learn how **D-Gain** acts as a "virtual shock absorber" to stop oscillations.

2.  **Stage 2: 1D Angular Control (Pendulum Angle)**
    - [ ] **Task:** Move the green arm to a specific angle (e.g., 45 degrees).
    - [ ] **Lesson:** Learn about **"Gravity Compensation."** A basic PID will struggle to hold a steady angle against gravity; you'll need the **Integral (I)** term to "push back."

---

## 📗 Phase 2: Advanced PID Architectures
**Goal:** Control systems with multiple interconnected parts.

3.  **Stage 3: Cascaded (Nested) PID (The Balancer)**
    - [ ] **Task:** Balance the pendulum straight up (0.0 rad) by moving the cart.
    - [ ] **Lesson:** Learn how to "Nest" two PIDs. The **Outer Loop** (Angle) tells the **Inner Loop** (Velocity) how fast to move the cart to catch the falling pole.

4.  **Stage 4: Anti-Windup & Saturation**
    - [ ] **Task:** Prevent the robot from "exploding" when it hits the 1.5m rail limit.
    - [ ] **Lesson:** Implement code to "clamp" the PID output so it stays within safe physical limits.

---

## 📙 Phase 3: The Leap to Modern Control (LQR)
**Goal:** Move beyond "Error-Correction" and into "State-Space" physics.

5.  **Stage 5: State-Space Modeling**
    - [ ] **Task:** Calculate the **A** and **B** matrices of your robot.
    - [ ] **Lesson:** Instead of just looking at "Error," we now look at the **"State"**: `[position, velocity, angle, angular_velocity]`.

6.  **Stage 6: LQR (Linear Quadratic Regulator)**
    - [ ] **Task:** Implement the LQR balancer.
    - [ ] **Lesson:** Learn why LQR is "Optimal." It finds the mathematically "perfect" balance between moving fast and saving energy.

---

## 🛠️ Your Current Lab Assignment
To prepare for **Phase 2**, we must "Open the Hood" of your robot's joints. 

**Next Steps:**
1.  **Instrumentation:** Update the `double_pendulem.urdf` to allow the cart to "push" the pendulum joints.
2.  **Feedback:** Ensure the PID node can see **both** the cart's position and the pendulum's angle at the same time.
