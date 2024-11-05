import rps.robotarium as robotarium
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
import numpy as np
import time
import matplotlib.pyplot as plt

# Define grid cell size
cell_size = 0.5  # Adjust cell size here

# Instantiate Robotarium object
N = 1  # One robot
r = robotarium.Robotarium(number_of_robots=N, show_figure=True, sim_in_real_time=False)

# Retrieve world boundaries for dynamic grid setup
world_width = r.boundaries[2]
world_height = r.boundaries[3]

# Calculate number of columns and rows based on cell size
grid_cols = int(world_width / cell_size)
grid_rows = int(world_height / cell_size)

# Calculate initial robot position (top-left corner of the grid)
initial_x = -world_width / 2 + cell_size / 2
initial_y = world_height / 2 - cell_size / 2
initial_conditions = np.array([[initial_x], [initial_y], [0]])  # Start in the top-left corner

r.initial_conditions = initial_conditions  # Set initial position
r.set_robot_color('#00FF00')  # Set robot color to green

# Create controller
single_integrator_position_controller = create_si_position_controller()

# Define barrier certificates to avoid collisions
si_barrier_cert = create_single_integrator_barrier_certificate_with_boundary()

# Initialize the mappings
si_to_uni_dyn, uni_to_si_states = create_si_to_uni_mapping()

# Define dynamic grid pattern
def add_grid_pattern():
    print("Adding grid to world background...")
    for row in range(grid_rows):
        for col in range(grid_cols):
            x = -world_width / 2 + col * cell_size + cell_size / 2
            y = world_height / 2 - row * cell_size - cell_size / 2
            r.axes.add_patch(plt.Rectangle((x - cell_size / 2, y - cell_size / 2), cell_size, cell_size, 
                                           fill=None, edgecolor='gray', linestyle='--'))

add_grid_pattern()

# Function to generate a list of waypoints based on grid traversal
def generate_waypoints():
    waypoints = []
    for row in range(grid_rows):
        # Move from left to right on even rows, and right to left on odd rows
        cols = range(grid_cols) if row % 2 == 0 else range(grid_cols - 1, -1, -1)
        for col in cols:
            x = -world_width / 2 + col * cell_size + cell_size / 2
            y = world_height / 2 - row * cell_size - cell_size / 2
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
