import os
import datetime
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, Shutdown, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():
    pkg_name = 'pid_controller_pkg'
    
    # Path to your Experiment URDF file
    urdf_file_path = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'double_pendulem.urdf')
    
    # Process URDF with xacro
    robot_description_config = xacro.process_file(urdf_file_path)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # 1. Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )


    # 3. Gazebo Sim Launch (Empty World)
    node_gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': 'empty.sdf'}.items() 
    )

    # 5. Spawn Robot in Gazebo
    node_spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'chaos_robot',
            '-z', '0.0'
        ]
    )

    # 6. Set Initial Joint Positions (Service Call)
    # This sends a service call to the Gazebo simulation to set joint positions
    node_set_initial_pose = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/chaos_robot/joint_state_publisher/set_parameters',
            'rcl_interfaces/srv/SetParameters',
            '{"parameters": [{"name": "initial_pose", "value": {"double_value": 1.57}}]}'
        ],
        output='screen'
    )

    # 6. ROS GZ Bridge (The "Translator")
    node_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model',
            '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            # Bridge ROS /slider_cmd to the specific Gazebo joint force topic
            '/model/chaos_robot/joint/slider_joint/cmd_force@std_msgs/msg/Float64@ignition.msgs.Double'
        ],
        remappings=[
            ('/model/chaos_robot/joint/slider_joint/cmd_force', '/slider_cmd')
        ]
    )

    #     package='pid_controller_pkg',
    #     executable='pid_controller',
    #     output='screen'
    # )

    return LaunchDescription([
        node_robot_state_publisher,
        node_gazebo_sim,
        node_spawn_robot,
        node_set_initial_pose,
        node_bridge,
        # node_pid_controller
    ])

