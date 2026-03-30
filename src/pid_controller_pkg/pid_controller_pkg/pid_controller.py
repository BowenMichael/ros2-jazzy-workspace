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
        self.declare_parameter('loop_rate', 50.0)  # Hz
        self.declare_parameter('joint_name', 'slider_joint')
        self.declare_parameter('use_velocity', False)
        self.declare_parameter('setpoint', 0.0)

        # 2. Internal State
        self.current_pos = 0.0
        self.last_error = 0.0
        self.integral = 0.0
        self.last_loop_time = None

        # add setpoint subscriber
        self.setpoint = self.get_parameter('setpoint').value
        self.setpoint_topic = self.create_subscription(
            Float64,
            'setpoint_topic',
            self.setpoint_callback,
            10
        )

        # 3. Subscribers and Publishers
        self.joint_state_sub = self.create_subscription(
            JointState, 
            '/joint_states', 
            self.joint_state_callback, 
            10
        )

        # We publish to a generic 'control_effort' topic, which can be remapped in launch
        self.cmd_pub = self.create_publisher(
            Float64, 
            'control_effort', 
            10
        )

        # 4. Control Loop Timer
        timer_period = 1.0 / self.get_parameter('loop_rate').value
        self.timer = self.create_timer(timer_period, self.control_loop)

        self.get_logger().info("PID Controller Node has been initialized.")

    def joint_state_callback(self, msg):
        """Callback for joint states. Type hint removed to avoid pybind11 conversion issues."""
        if not msg or not hasattr(msg, 'name'):
            return

        joint_name = self.get_parameter('joint_name').value

        # Find the target joint index
        try:
            if joint_name in msg.name:
                idx = msg.name.index(joint_name)
                # Ensure the position array is long enough
                if len(msg.position) > idx:
                    if self.get_parameter('use_velocity').value:
                        self.current_pos = msg.velocity[idx]
                    else:
                        self.current_pos = msg.position[idx]
        except Exception as e:
            self.get_logger().debug(f"Error in joint_state_callback: {e}")

    def setpoint_callback(self, msg):
        """Callback for setpoint updates."""
        if msg is not None:
            #self.get_logger().info(f"Received new setpoint: {msg.data}")
            self.setpoint = msg.data

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
        # Cap dt to prevent massive spikes during simulation lag
        dt = min(dt, 0.1) # Max 100ms per step

        # Fetch latest parameters
        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value

        # Dynamically set the setpoint from the latest received value
        setpoint = self.setpoint

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

        # SATURATION CLAMP: Prevent simulation from exploding
        max_effort = 1000.0 # Newtons
        output = max(min(output, max_effort), -max_effort)

        # Publish command
        msg = Float64()
        msg.data = float(output)
        self.cmd_pub.publish(msg)
        
        self.last_error = error


def main(args=None):
    rclpy.init(args=args)
    node = PIDController()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()
    
if __name__ == '__main__':
    main()
