FROM osrf/ros:jazzy-desktop

# Install basic GUI and Gazebo dependencies
# Install basic GUI, Gazebo, RViz, and Poetry dependencies
RUN apt-get update && apt-get install -y \
    mesa-utils \
    curl \
    ros-jazzy-ros-gz \
    ros-jazzy-xacro \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-rqt-plot \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set up the same environment variables WSLg uses
ENV DISPLAY=:0
ENV WAYLAND_DISPLAY=wayland-0
ENV XDG_RUNTIME_DIR=/mnt/wslg/runtime-dir
ENV PULSE_SERVER=unix:/mnt/wslg/PulseServer

# 3. Automatically source ROS 2 and the local workspace for every new bash shell
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "if [ -f /home/ros_ws/install/setup.bash ]; then source /home/ros_ws/install/setup.bash; fi" >> ~/.bashrc
RUN echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc

# Standard ROS entrypoint
CMD ["bash"]
