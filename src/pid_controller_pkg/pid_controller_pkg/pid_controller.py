#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

class PIDController(Node):
    def __init__(self):
        super().__init__('pid_controller')

        # 1. Parameters (Tunable via ROS 2 CLI or YAML)
        self.declare_parameter('kp', 10.0)
        self.declare_parameter('ki', 0.0)
        self.declare_parameter('kd', 1.0)
        self.declare_parameter('setpoint', 0.0)
        self.declare_parameter('loop_rate', 50.0)  # Hz

        # 2. Internal State
        self.current_pos = 0.0
        self.last_error = 0.0
        self.integral = 0.0
        self.last_loop_time = None

        # 3. Subscribers and Publishers
        self.joint_state_sub = self.create_subscription(
            JointState, 
            '/joint_states', 
            self.joint_state_callback, 
            10
        )

        self.cmd_pub = self.create_publisher(
            Float64, 
            '/slider_cmd', 
            10
        )

        # 4. Control Loop Timer
        timer_period = 1.0 / self.get_parameter('loop_rate').value
        self.timer = self.create_timer(timer_period, self.control_loop)

        self.get_logger().info("PID Controller Node has been initialized.")

    def joint_state_callback(self, msg: JointState):
        # Find the slider_joint index
        try:
            idx = msg.name.index('slider_joint')
            self.current_pos = msg.position[idx]
        except ValueError:
            pass

    def control_loop(self):
        current_time = self.get_clock().now()
    
        if self.last_loop_time is None:
            self.last_loop_time = current_time
            return
        
        dt = (current_time - self.last_loop_time).nanoseconds / 1e9
        
        if dt <= 0.0:
            return
        
        self.handle_pid(dt)
        self.last_loop_time = current_time

    def handle_pid(self, dt):
        # Fetch latest parameters
        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value
        setpoint = self.get_parameter('setpoint').value

        # PID Logic
        error = setpoint - self.current_pos
        
        # Proportional
        p_term = kp * error
        
        # Integral
        self.integral += error * dt
        i_term = ki * self.integral
        
        # Derivative
        derivative = (error - self.last_error) / dt
        d_term = kd * derivative

        # Combined Output (Effort/Force)
        output = p_term + i_term + d_term

        # Publish command
        msg = Float64()
        msg.data = output
        self.cmd_pub.publish(msg)
        
        self.last_error = error

def main(args=None):
    rclpy.init(args=args)
    node = PIDController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
if __name__ == '__main__':
    main()
