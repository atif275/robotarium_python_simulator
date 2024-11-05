import rps.robotarium as robotarium
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
import numpy as np
import time
import matplotlib.pyplot as plt

# Define grid movement parameters
cell_width = 0.2
cell_height = 0.2
grid_cols = 10
grid_rows = 5

# Instantiate Robotarium object
N = 1  # One robot
initial_conditions = np.array([[(-1.5 + cell_width/2)], [1.0 - cell_height/2], [0]])  # Start in the top-left corner

r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=False)
r.set_robot_color('#00FF00')  # Set robot color to green

# Create controller
single_integrator_position_controller = create_si_position_controller()

# Define barrier certificates to avoid collisions
si_barrier_cert = create_single_integrator_barrier_certificate_with_boundary()

# Initialize the mappings
si_to_uni_dyn, uni_to_si_states = create_si_to_uni_mapping()

# Define initial grid pattern
def add_grid_pattern():
    print("Adding grid to world background...")
    for row in range(grid_rows):
        for col in range(grid_cols):
            x = -1.6 + col * cell_width + cell_width / 2
            y = 1.0 - row * cell_height - cell_height / 2
            r.axes.add_patch(plt.Rectangle((x - cell_width / 2, y - cell_height / 2), cell_width, cell_height, fill=None, edgecolor='gray', linestyle='--'))

add_grid_pattern()

# Function to generate a list of waypoints based on grid traversal
def generate_waypoints():
    waypoints = []
    for row in range(grid_rows):
        # Move from left to right on even rows, and right to left on odd rows
        cols = range(grid_cols) if row % 2 == 0 else range(grid_cols - 1, -1, -1)
        for col in cols:
            x = -1.6 + col * cell_width + cell_width / 2
            y = 1.0 - row * cell_height - cell_height / 2
            waypoints.append([x, y])
    return np.array(waypoints).T

# Generate waypoints based on grid pattern
waypoints = generate_waypoints()
goal_index = 0

# Main loop for robot grid traversal
while goal_index < waypoints.shape[1]:
    # Get current poses and determine single integrator state
    x = r.get_poses()
    x_si = uni_to_si_states(x)

    # Update goal point
    goal_points = waypoints[:, goal_index:goal_index + 1]

    # Check if robot has reached the current waypoint
    if np.linalg.norm(x_si[:2, 0] - goal_points[:2, 0]) < 0.05:
        goal_index += 1  # Move to next waypoint

    # Create control inputs
    dxi = single_integrator_position_controller(x_si, goal_points)

    # Ensure safe inputs
    dxi = si_barrier_cert(dxi, x_si)

    # Convert single integrator to unicycle dynamics
    dxu = si_to_uni_dyn(dxi, x)

    # Set velocities and update simulation
    r.set_velocities(np.arange(N), dxu)
    r.step()

# Call at end of script for Robotarium server compatibility
r.call_at_scripts_end()
