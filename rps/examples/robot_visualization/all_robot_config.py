# all_robot_config.py

import time
import numpy as np
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator

# Define the number of robots
N = 3

# Define initial positions for the three robots (left, middle, right)
initial_positions = np.array([
    [-1.0, 0.0, 1.0],  # x-coordinates (left, center, right)
    [0.0, 0.0, 0.0],   # y-coordinates (all start from the center)
    [0.0, 0.0, 0.0]    # orientation angles (facing upwards)
])

# Create Robotarium instance with initial conditions
r = Robotarium(number_of_robots=N, initial_conditions=initial_positions, show_figure=True, sim_in_real_time=True)

# Create the RobotConfigurator instance
robot_configurator = RobotConfigurator(robotarium_instance=r)

# Initial delay for setup and displaying robots before configuration starts
# time.sleep(2)
print("Config Testing is starting shortly...")

# Define colors and parameters for continuous changes
face_colors_sequence = ['#FF5733', '#33FF57', '#3357FF', '#FFD700', '#FF33A1']
flash_colors = ['#FFFF00', '#FF00FF', '#00FFFF']
transparency_sequence = [1.0, 0.8, 0.6, 0.4, 0.2]  # High to low transparency
outline_thicknesses = [2.0, 3.0, 4.0]

# Step 1: Chassis Color Changing for 10 seconds (2 seconds per color)
for color in face_colors_sequence:
    for i in range(N):
        print(f"[DEBUG] Changing face color to {color} for robot {i}")
        robot_configurator.set_robot_colors_with_head(i, color, outline_color='#000000', head_marker_color='#FFFFFF')
    r.get_poses()
    r.step()
    time.sleep(2)

# Step 2: Enable high-speed flashing with the current color for 10 seconds
for i in range(N):
    print(f"[DEBUG] Enabling high-speed flashing for robot {i}")
    robot_configurator.enable_flashing(i, flash_fill=True, flash_outline=True, fill_flash_speed='fast', outline_flash_speed='fast')
r.get_poses()
r.step()
time.sleep(2)  # Observe flashing effect for 10 seconds

# Step 3: Change transparency levels from high to low over 10 seconds
for transparency in transparency_sequence:
    for i in range(N):
        print(f"[DEBUG] Setting transparency level to {transparency} for robot {i}")
        robot_configurator.set_transparency_level(i, transparency)
    r.get_poses()
    r.step()
    time.sleep(2)

# Step 4: Update outline thickness for visual differentiation
for i in range(N):
    outline_thickness = outline_thicknesses[i]
    shape_settings = {
        'radius': robot_configurator.default_settings['shape']['radius'],
        'outline_thickness': outline_thickness,
        'head_marker_size': robot_configurator.default_settings['shape']['head_marker_size']
    }
    print(f"[DEBUG] Setting outline thickness to {outline_thickness} for robot {i}")
    robot_configurator.configure_robot(i, {'shape': shape_settings})
r.get_poses()
r.step()
time.sleep(5)

# Step 5: Disable flashing for all robots
for i in range(N):
    print(f"[DEBUG] Disabling flashing for robot {i}")
    robot_configurator.disable_flashing(i)
r.get_poses()
r.step()
time.sleep(1)

# Print final settings for confirmation
print("Final robot configurations:")
robot_configurator.print_all_robot_settings()

# Run a few steps of the simulation to observe final configurations
for _ in range(10):
    r.get_poses()  # Ensure we get poses before calling step
    r.step()
    time.sleep(0.5)

# Finalize the simulation
r.call_at_scripts_end()
