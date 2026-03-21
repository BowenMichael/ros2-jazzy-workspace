#!/usr/bin/env python3

# Import every time for ROS2
import rclpy
from rclpy.node import Node

class MyFirstNode(Node):
    def __init__(self):
        super().__init__('first_node')
        self.get_logger().info('Hello ROS2!')
        self.counter = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.counter += 1
        self.get_logger().info('Timer callback called! ' + str(self.counter))


# main function for ROS2 nodes
def main(args=None):

    rclpy.init(args=args)
    node = MyFirstNode()
    rclpy.spin(node)
    rclpy.shutdown()


# command line entry point
if __name__ == '__main__':
    main()