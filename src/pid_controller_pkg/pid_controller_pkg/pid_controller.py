#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float64

class PIDController(Node):
    def __init__(self):
        super().__init__('pid_controller')
        # Here you would initialize your PID controller parameters and subscribers/publishers

        # Subscribe to the necessary topics (e.g., joint states, desired positions)
        # self.subscription = self.create_subscription(...)

        self.joint_state_sub = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)

        # Create publishers for control commands
        # self.publisher = self.create_publisher(...)

        self.double_pendulum_pub = self.create_publisher(Float64, '/slider_control_command', 10)

        # 1. Parameters (Tunable via ROS 2 CLI or YAML)
        self.declare_parameter('kp', 1.0)
        self.declare_parameter('ki', 0.0)
        self.declare_parameter('kd', 0.05)
        self.declare_parameter('setpoint', 10.0)
        self.declare_parameter('loop_rate', 20.0)  # Hz

        # 2. Internal State (The "State Buffer")
        self.current_pos = 0.0
        self.last_error = 0.0
        self.integral = 0.0
        
        # Timing state
        self.last_loop_time = None

        # initalize heartbeat timer to log that the node is alive
        timer_period = 1.0 / self.get_parameter('loop_rate').value
        self.timer = self.create_timer(timer_period, self.control_loop)

        self.get_logger().info("PID Controller Node has been initialized.")
    
    def setpoint_callback(self, msg ):
        # Handle setpoint updates
        pass

    def joint_state_callback(self, msg : JointState):
        # This callback will be called whenever a new joint state message is received
        # Here you would implement your PID control logic to compute the control commands
        # based on the current joint states and the desired setpoints

        # Example (pseudocode):
        # error = desired_position - current_position
        # integral += error * dt
        # derivative = (error - previous_error) / dt
        # control_command = Kp * error + Ki * integral + Kd * derivative

        

        # Then publish the control command to the appropriate topic
        # self.get_logger().info("Received joint state message, computing control command...")
        # self.publisher.publish(control_command)
        pass
    
    def control_loop(self):
        # This method will be called at a fixed rate defined by loop_rate
        # You can use this to perform any periodic tasks, such as logging or safety checks
        """The actual PID math happens here at a fixed interval."""
        # A. Calculate actual elapsed time (Considering processing time)
        
        current_time = self.get_clock().now()
    
        # Handle the very first tick
        if self.last_loop_time is None:
            self.last_loop_time = current_time
            self.get_logger().info("First timer tick - initializing time.")
            return
        
        dt = (current_time - self.last_loop_time).nanoseconds / 1e9
        
        if dt <= 0.0:
            self.get_logger().warn("Non-positive dt calculated, skipping this loop iteration.")
            return
        
        self.get_logger().debug(f"Control loop dt: {dt:.6f} seconds")

        self.handle_pid(dt)
        
        self.last_loop_time = current_time

    def handle_pid(self, dt):
       # B. Fetch latest parameters (Allows live tuning)
        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value
        setpoint = self.get_parameter('setpoint').value

        # C. PID Logic
        error = setpoint - self.current_pos
        
        # Proportional
        p_term = kp * error
        
        # Integral (with basic anti-windup: only accumulate if error is small)
        self.integral += error * dt
        i_term = ki * self.integral
        
        # Derivative
        derivative = (error - self.last_error) / dt
        d_term = kd * derivative

        # D. Combined Output
        output = p_term + i_term + d_term

        # E. Execution & Housekeeping
       # Create a simple Float64 message
        msg = Float64()
        msg.data = output
        
        self.cmd_pub.publish(msg)
        self.get_logger().info(f"Sent Force: {output:.2f} to /slider_cmd")
        
        self.last_error = error
        pass

def main():
    rclpy.init()
    node = PIDController()
    node.get_logger().info("PID Controller Node has started.")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
if __name__ == '__main__':
    main()