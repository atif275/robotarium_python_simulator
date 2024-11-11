# transparency_slider_simulation.py

import numpy as np
import time
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the number of robots (only one for this example)
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

# Set initial color and visibility settings for the robot
robot_configurator.set_robot_colors_with_head(0, fill_color='#FF5733', outline_color='#000000', head_marker_color='#FFFFFF')
robot_configurator.set_transparency_level(0, 1.0)  # Start fully opaque

# Set up a slider within the same figure to control transparency
fig = plt.figure(r.figure.number)  # Use Robotarium's figure
ax_slider = plt.axes([0.25, 0.03, 0.65, 0.03], facecolor='lightgrey')
transparency_slider = Slider(
    ax=ax_slider,
    label='Transparency',
    valmin=0,
    valmax=1,
    valinit=1,  # Start with fully opaque
)

# Function to update the transparency level based on the slider
def update_transparency(val):
    transparency_level = transparency_slider.val  # Get slider value
    print(f"[DEBUG] Updating transparency level to {transparency_level:.2f}")
    
    # Set transparency for the robot
    robot_configurator.set_transparency_level(0, transparency_level)
    
    # Update the simulation to reflect transparency change
    r.get_poses()
    r.step()

# Attach the update function to the slider
transparency_slider.on_changed(update_transparency)

# Run the simulation, allowing transparency changes via the slider
try:
    while True:
        plt.pause(0.05)  # Small delay to allow real-time updates
        r.get_poses()  # Ensure the simulation updates continuously
        r.step()
except KeyboardInterrupt:
    pass

# Finalize the simulation
r.call_at_scripts_end()
