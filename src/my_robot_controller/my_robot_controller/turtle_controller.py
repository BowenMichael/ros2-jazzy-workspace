#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        

        self.get_logger().info('Turtle Controller Node has been started.')

    def pose_callback(self, msg : Pose):
        cmd = Twist()

        if msg.x > 9.0 or msg.x < 1.0 or msg.y > 9.0 or msg.y < 1.0:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.9
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0

        if msg.x > 5.0 and msg.y > 5.0:
            self.call_set_pen_service(255, 0, 0, 3, 0)
        elif msg.x < 5.0 and msg.y > 5.0:
            self.call_set_pen_service(0, 255, 0, 3, 0)
        elif msg.x < 5.0 and msg.y < 5.0:
            self.call_set_pen_service(0, 0, 255, 3, 0)
        else:
            self.call_set_pen_service(255, 255, 0, 3, 0)

        self.cmd_vel_publisher.publish(cmd)

    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, '/turtle1/set_pen')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for SetPen service...')
        
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request)
        future.add_done_callback(self.callback_set_pen_response)
        
    def callback_set_pen_response(self, future):
        try:
            response = future.result()
            self.get_logger().info('SetPen service call succeeded')
        except Exception as e:
            self.get_logger().error(f'SetPen service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()