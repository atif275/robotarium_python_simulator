# transparency_example.py

import time
import numpy as np
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator

# Define the number of robots (just one for this example)
N = 1

# Define initial position for the single robot (center)
initial_position = np.array([
    [0.0],  # x-coordinate
    [0.0],  # y-coordinate
    [0.0]   # orientation angle
])

# Create Robotarium instance with initial conditions
r = Robotarium(number_of_robots=N, initial_conditions=initial_position, show_figure=True, sim_in_real_time=True)

# Create the RobotConfigurator instance
robot_configurator = RobotConfigurator(robotarium_instance=r)

# Define a sequence of transparency levels from high to low
transparency_levels = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]  # Fully opaque to fully transparent

# Apply each transparency level to the robot with a delay
for transparency in transparency_levels:
    print(f"[DEBUG] Setting transparency level to {transparency} for robot 0")
    robot_configurator.set_transparency_level(0, transparency)
    
    # Update the simulation to visualize the change
    r.get_poses()
    r.step()
    
    # Delay for 2 seconds to observe each transparency level
    time.sleep(2)

# Finalize the simulation
r.call_at_scripts_end()

