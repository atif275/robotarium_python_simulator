import rps.robotarium as robotarium
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
from rps.robot_configuration import RobotConfigurator
import numpy as np

# Instantiate Robotarium object
N = 3  # Number of robots
initial_conditions = np.array([
    [0.0, -0.5, 0.5],  # x-coordinates for each robot
    [0.0,  0.5, -0.5],  # y-coordinates for each robot
    [0.0,  0.0, 0.0]    # orientation for each robot (e.g., facing forward)
])

# Instantiate the Robotarium object
r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=False)

# Initialize RobotConfigurator with the Robotarium instance
configurator = RobotConfigurator(r)

# Configure each robot with default settings or customize as needed
for robot_id in range(N):
    configurator.configure_robot(robot_id)  # Uses default settings

# Example: Update settings for robot 1 after initialization
custom_settings = {
    'shape': {'radius': 0.06, 'outline_thickness': 2.0, 'head_marker_size': 0.04},
    'colors': {'fill_color': '#00FF00', 'outline_color': 'blue', 'head_marker_color': 'red'},
    'flash': {'flash_fill': True, 'flash_outline': True, 'fill_flash_speed': 'fast', 'outline_flash_speed': 'slow'},
    'transparency': 0.8,
    'flash_color': '#FF0000'
}
configurator.configure_robot(1, custom_settings)

# Print settings for all robots
configurator.print_all_robot_settings()