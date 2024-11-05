import rps.robotarium as robotarium
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
from rps.robot_configuration import RobotConfigurator
import numpy as np
import time

# Define grid cell size
cell_width = 0.2
cell_height = 0.2

# Number of robots
N = 3  # Set to 3 for three robots

# Initial conditions for each robot, spread across the world
initial_conditions = np.array([
    [-1.5 + cell_width/2, 1.0 - cell_height/2, 0],  # Robot 1's starting position
    [-1.2 + cell_width/2, 0.5 - cell_height/2, 0],  # Robot 2's starting position
    [-0.9 + cell_width/2, 0.2 - cell_height/2, 0]   # Robot 3's starting position
]).T

# Instantiate Robotarium object
r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=False)

# Initialize configurator with the Robotarium instance
configurator = RobotConfigurator(r)

# Configuration settings for each robot
robot_settings = [
    {
        'shape': {'radius': 0.05, 'outline_thickness': 1.0, 'head_marker_size': 0.03},
        'colors': {'fill_color': '#FFD700', 'outline_color': 'k', 'head_marker_color': 'k'},
        'flash': {'flash_fill': False, 'flash_outline': False, 'fill_flash_speed': 'medium', 'outline_flash_speed': 'medium'},
        'transparency': 1.0,
        'flash_color': '#FFFFFF'
    },
    {
        'shape': {'radius': 0.06, 'outline_thickness': 2.0, 'head_marker_size': 0.04},
        'colors': {'fill_color': '#00FF00', 'outline_color': 'blue', 'head_marker_color': 'red'},
        'flash': {'flash_fill': True, 'flash_outline': True, 'fill_flash_speed': 'fast', 'outline_flash_speed': 'slow'},
        'transparency': 0.8,
        'flash_color': '#FF0000'
    },
    {
        'shape': {'radius': 0.05, 'outline_thickness': 1.0, 'head_marker_size': 0.03},
        'colors': {'fill_color': '#0000FF', 'outline_color': 'orange', 'head_marker_color': 'white'},
        'flash': {'flash_fill': False, 'flash_outline': False, 'fill_flash_speed': 'medium', 'outline_flash_speed': 'medium'},
        'transparency': 1.0,
        'flash_color': '#FFFFFF'
    }
]

# Configure and display each robot with a delay
for i in range(N):
    # Configure the robot with its settings
    configurator.configure_robot(i, robot_settings[i])
    
    # Print the launch info
    print(f"Launching robot {i} with settings: {robot_settings[i]}")
    
    # Run a short loop to display the robot in the world
    for _ in range(10):  # Loop for a brief time to show the robot's configuration
        r.get_poses()  # Update positions
        r.step()       # Render the current step
        time.sleep(0.1)
    
    # Wait for 5 seconds before launching the next robot
    time.sleep(5)

# End the simulation
r.call_at_scripts_end()
