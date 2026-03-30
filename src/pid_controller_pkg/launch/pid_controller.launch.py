import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():
    pkg_name = 'pid_controller_pkg'
    
    # 0. Launch Arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Path to your custom world and models
    pkg_share = get_package_share_directory(pkg_name)
    world_file_path = os.path.join(pkg_share, 'worlds', 'pid_balancer.sdf')
    models_dir_path = os.path.join(pkg_share, 'models')

    # 1. Environment Variable: Tell Gazebo where to find your models
    # This is crucial for the 'model://' URI in the SDF world file to work.
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[models_dir_path]
    )

    # 2. Robot State Publisher Node
    urdf_file_path = os.path.join(pkg_share, 'urdf', 'single_pendulum.urdf')
    robot_description_config = xacro.process_file(urdf_file_path)
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_config.toxml(),
            'use_sim_time': use_sim_time
        }]
    )

    # 3. Gazebo Sim Launch (Using our CUSTOM world)
    node_gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': f'-r {world_file_path}'}.items() 
    )

    # 4. Set Initial Joint Positions (Still useful for specific tests)
    node_set_initial_pose = ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/chaos_robot/joint_state_publisher/set_parameters',
            'rcl_interfaces/srv/SetParameters',
            '{"parameters": [{"name": "initial_pose", "value": {"double_value": 3.14}}]}'
        ],
        output='screen'
    )

    # 5. ROS GZ Bridge (The "Translator")
    node_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model',
            '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/world/pid_balancer_world/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            '/model/chaos_robot/joint/slider_joint/cmd_force@std_msgs/msg/Float64@ignition.msgs.Double'
        ],
        remappings=[
            ('/model/chaos_robot/joint/slider_joint/cmd_force', '/slider_cmd'),
            ('/world/pid_balancer_world/clock', '/clock')
        ]
    )

    # 6. PID Controller Nodes (Angle and Velocity)
    angle_pid_node = Node(
        name='angle_pid_node',
        package='pid_controller_pkg',
        executable='pid_controller',
        output='screen',
        parameters=[{
            'kp': 0.0, 'ki': 0.0, 'kd': 0.0,
            'joint_name': 'pendulum_joint',
            'use_velocity': False,
            'setpoint': 3.14,
        }],
        remappings=[('control_effort', '/desired_velocity')]
    )

    velocity_pid_node = Node(
        name='velocity_pid_node',
        package='pid_controller_pkg',
        executable='pid_controller',
        output='screen',
        parameters=[{
            'kp': 10.0, 'ki': 0.0, 'kd': 1.0,
            'joint_name': 'slider_joint',
            'use_velocity': True,
            'setpoint': 0.0,
        }],
        remappings=[
            ('setpoint_topic', '/desired_velocity'),
            ('control_effort', '/slider_cmd')
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        set_gz_resource_path,
        node_robot_state_publisher,
        node_gazebo_sim,
        # node_set_initial_pose, # Optionally keep this
        node_bridge,
        angle_pid_node,
        velocity_pid_node
    ])
