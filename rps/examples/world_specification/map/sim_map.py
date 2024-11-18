import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from PIL import Image
from rps.robotarium import Robotarium
from rps.robot_configuration import RobotConfigurator
import time

# Define zoom levels and initial zoom
zoom_levels = [15, 16, 17, 18, 19]
initial_zoom = 15

# Set initial position for a single stationary, invisible robot
initial_positions = np.array([
    [0.0],   # x-coordinate
    [0.0],   # y-coordinate
    [0.0]    # orientation angle
])

# Create Robotarium instance with 1 robot
r = Robotarium(number_of_robots=1, initial_conditions=initial_positions, show_figure=True, sim_in_real_time=True)
robot_configurator = RobotConfigurator(robotarium_instance=r)
robot_configurator.set_transparency_level(0, 0.0)  # Set robot transparency to invisible

# Function to load and display the map at the selected zoom level
def load_map_image(zoom):
    """Loads and displays the map image for the given zoom level as the background."""
    try:
        map_path = f"Images/Home/stitched_map_{zoom}.png"  # Path to the stitched map for the given zoom
        map_image = Image.open(map_path)
        ax.imshow(map_image, extent=(-1, 1, -1, 1), aspect='auto')  # Display image as background
        print(f"[DEBUG] Loaded map at zoom level {zoom}")
    except FileNotFoundError:
        print(f"[ERROR] Map for zoom level {zoom} not found. Please ensure tiles are downloaded and stitched.")

# Initialize figure and axis without axes or margins
fig, ax = plt.subplots()
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margins around the figure
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axis('off')  # Turn off the axis for a clean background display

# Display initial map
load_map_image(initial_zoom)

# Slider for zoom control
ax_zoom_slider = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgoldenrodyellow')
zoom_slider = Slider(ax_zoom_slider, 'Zoom', valmin=zoom_levels[0], valmax=zoom_levels[-1], valinit=initial_zoom, valstep=1)

# Update map when slider is adjusted
def update_map(val):
    zoom_level = int(zoom_slider.val)
    ax.clear()  # Clear previous map
    ax.axis('off')  # Ensure the axis stays off
    load_map_image(zoom_level)
    fig.canvas.draw_idle()  # Update the canvas with the new map

zoom_slider.on_changed(update_map)

# Simulation loop
simulation_duration = 30  # Run simulation for 10 seconds
start_time = time.time()
while time.time() - start_time < simulation_duration:
    r.get_poses()  # Get robot poses to keep the simulation running smoothly
    r.step()
    plt.pause(0.1)

r.call_at_scripts_end()
