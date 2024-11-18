import matplotlib.pyplot as plt
import numpy as np
import time
from PIL import Image
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator

# Path to your background map image
background_image_path = "./img2.png"

# Load the image
bg_image = Image.open(background_image_path)

# Create Robotarium instance with one invisible robot
r = Robotarium(number_of_robots=1, show_figure=True, sim_in_real_time=True)
robot_configurator = RobotConfigurator(robotarium_instance=r)

# Set transparency to 0 for the robot to make it invisible
robot_configurator.set_transparency_level(0, 0.0)

# Set up the plot with Robotarium's figure and axes
fig, ax = r.figure, r.axes

# Display the image as background
ax.imshow(bg_image, extent=[-1, 1, -1, 1])  # Adjust extent as needed

# Simulation loop for 10 seconds
simulation_duration = 10  # seconds
start_time = time.time()

while time.time() - start_time < simulation_duration:
    r.get_poses()  # Get poses for the invisible robot
    r.step()       # Step forward in the simulation
    plt.pause(0.1)

r.call_at_scripts_end()
