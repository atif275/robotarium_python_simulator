# robot_visualization_test.py

import numpy as np
import time
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator

# Initialize the Robotarium environment with a single robot for testing
N = 1
initial_conditions = np.array([[0.0], [0.0], [0]])  # Start position for the robot in the center

# Create Robotarium instance
r = Robotarium(number_of_robots=N, show_figure=True, sim_in_real_time=True, initial_conditions=initial_conditions)

# Initialize the RobotConfigurator
configurator = RobotConfigurator(r)

# Configure robot appearance settings with initial colors and shape
configurator.configure_robot(
    robot_id=0,
    settings={
        'shape': {'radius': 0.1, 'outline_thickness': 1.5, 'head_marker_size': 0.05},
        'colors': {'fill_color': '#00FF00', 'outline_color': 'blue', 'head_marker_color': 'red'},
        'flash': {'flash_fill': True, 'flash_outline': True, 'fill_flash_speed': 'fast', 'outline_flash_speed': 'slow'},
        'transparency': 0.8,
        'flash_color': '#FF0000'
    }
)

# Define angular speed and radius for circular motion
angular_speed = 0.1  # Angular speed in radians per step
radius = 0.5         # Radius of the circular path

# Start the simulation loop to test flashing and color settings
for i in range(500):  # Increased loop steps for prolonged observation
    poses = r.get_poses()
    
    # Calculate velocities for circular motion around the center point
    vx = -radius * angular_speed * np.sin(angular_speed * i)
    vy = radius * angular_speed * np.cos(angular_speed * i)
    velocities = np.array([[vx], [vy]])

    r.set_velocities(np.arange(N), velocities)
    r.step()
    
    # Periodically change color to observe dynamic updates
    if i % 200 == 0:
        configurator.set_robot_colors_with_head(0, fill_color='#FF00FF', outline_color='yellow', head_marker_color='green')
    elif i % 200 == 100:
        configurator.set_robot_colors_with_head(0, fill_color='#00FF00', outline_color='blue', head_marker_color='red')

# Finalize the simulation
r.call_at_scripts_end()
