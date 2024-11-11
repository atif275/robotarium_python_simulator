import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator

# Define the number of robots
N = 1

# Define initial position for the single robot
initial_positions = np.array([
    [0.0],   # x-coordinates
    [0.0],   # y-coordinates
    [0.0]    # orientation angles
])

# Create Robotarium instance with initial conditions
r = Robotarium(number_of_robots=N, initial_conditions=initial_positions, show_figure=True, sim_in_real_time=True)
robot_configurator = RobotConfigurator(robotarium_instance=r)

# Set initial color
initial_color = '#FFD700'
robot_configurator.set_robot_colors_with_head(0, initial_color, outline_color='#000000', head_marker_color='#FFFFFF')

# Update color function
def update_color(color):
    print(f"[DEBUG] Changing face color to {color}")
    robot_configurator.set_robot_colors_with_head(0, color, outline_color='#000000', head_marker_color='#FFFFFF')
    r.get_poses()
    r.step()

# Predefined color buttons
color_buttons = {
    "Red": "#FF5733",
    "Green": "#33FF57",
    "Blue": "#3357FF",
    "Yellow": "#FFD700",
    "Pink": "#FF33A1"
}

# Adjust layout for Robotarium figure and control panel
plt.subplots_adjust(bottom=0.3)  # Make room for buttons without a subplot

# Create buttons for predefined colors
button_axes = []
buttons = []
for idx, (label, color) in enumerate(color_buttons.items()):
    ax_button = plt.axes([0.1 + idx * 0.15, 0.15, 0.1, 0.05])
    button = Button(ax_button, label)
    button.on_clicked(lambda event, c=color: update_color(c))
    button_axes.append(ax_button)
    buttons.append(button)

# Textbox for custom color code
ax_textbox = plt.axes([0.1, 0.05, 0.4, 0.075])
text_box = TextBox(ax_textbox, 'Custom Color Code', initial="#FFFFFF")

# Apply button for custom color
def apply_custom_color(event):
    color = text_box.text
    if color.startswith('#') and len(color) == 7:
        update_color(color)
    else:
        print("[ERROR] Invalid color code. Use format #RRGGBB.")

ax_apply_button = plt.axes([0.55, 0.05, 0.1, 0.075])
apply_button = Button(ax_apply_button, 'Apply')
apply_button.on_clicked(apply_custom_color)

# Simulation loop
def run_simulation():
    while True:
        r.get_poses()  # Ensure we get poses before calling step
        r.step()
        plt.pause(0.1)  # Small delay to allow interaction with the GUI

# Display Robotarium figure without a subplot
plt.ion()
r.figure.show()
run_simulation()
