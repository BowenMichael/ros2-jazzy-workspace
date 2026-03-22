from glob import glob
import os

from setuptools import  setup

package_name = 'pid_controller_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'pid_controller = pid_controller_pkg.pid_controller:main'
        ],
    },
    # REMOVED: description, license, maintainer, and scripts.
    # These are now read from pyproject.toml automatically.
)