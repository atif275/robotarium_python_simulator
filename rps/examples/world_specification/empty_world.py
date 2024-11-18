import numpy as np
import matplotlib.pyplot as plt
import time
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator

# Define a single invisible robot to simulate an empty world
r = Robotarium(number_of_robots=1, show_figure=True, sim_in_real_time=True)
robot_configurator = RobotConfigurator(robotarium_instance=r)

# Set the single robot to be fully transparent to simulate an empty world
robot_configurator.set_transparency_level(0, 0.0)  # Set transparency to 0 (fully invisible)

# Set the simulation duration
simulation_duration = 10  # seconds
start_time = time.time()

# Initialize the figure and axes

# Run the simulation loop for 10 seconds
while time.time() - start_time < simulation_duration:
    r.get_poses()  # Get robot poses (even though it's invisible)
    r.step()       # Step forward in the simulation
    plt.pause(0.1) # Pause to update the figure in real time

# Finalize the simulation
r.call_at_scripts_end()
print("Simulation completed.")
