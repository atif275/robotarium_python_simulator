# outline_thickness_slider_sim.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator

# Define the number of robots
N = 1

# Define initial positions for the robot
initial_positions = np.array([
    [0.0],  # x-coordinate
    [0.0],  # y-coordinate
    [0.0]   # orientation angle
])

# Create Robotarium instance with initial conditions
r = Robotarium(number_of_robots=N, initial_conditions=initial_positions, show_figure=True, sim_in_real_time=True)

# Create the RobotConfigurator instance
robot_configurator = RobotConfigurator(robotarium_instance=r)

# Set initial outline thickness
initial_thickness = 2.0
robot_configurator.set_outline_thickness(0, initial_thickness)
print(f"[DEBUG] Initial outline thickness set to {initial_thickness} units for robot 0")


# Function to update outline thickness based on slider value
def update_thickness(val):
    thickness = slider.val
    robot_configurator.set_outline_thickness(0, thickness)
    print(f"[DEBUG] Outline thickness updated to {thickness:.2f} units for robot 0")  # Debugging message with units
    r.get_poses()
    r.step()

# Adjust figure layout for Robotarium display and add slider
fig = r.figure
plt.subplots_adjust(bottom=0.25)  # Adjust to make room for slider

# Add slider to control outline thickness
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Outline Thickness', 1.0, 5.0, valinit=initial_thickness)

# Attach the update function to the slider
slider.on_changed(update_thickness)

# Run the simulation with the slider control active
while True:   # Adjust the range for how long you want the simulation to run
    r.get_poses()
    r.step()

plt.show()

# Finalize the simulation
r.call_at_scripts_end()
