# general_env_sim.py

import numpy as np
from rps.robotarium import Robotarium
from rps.utilities.controllers import create_si_position_controller
from rps.utilities.barrier_certificates import create_single_integrator_barrier_certificate_with_boundary
from rps.utilities.transformations import create_si_to_uni_mapping

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

# Define a simple position controller
si_position_controller = create_si_position_controller()
si_barrier_cert = create_single_integrator_barrier_certificate_with_boundary()
si_to_uni_dyn, uni_to_si_states = create_si_to_uni_mapping()

# Define target positions for upward movement
target_positions = np.array([
    [-1.0, 0.0, 1.0],  # x-coordinates remain the same for each robot
    [0.8, 0.8, 0.8]    # y-coordinates moved upwards
])

# Function to move each robot up to its target position and stop
def move_robot_up(robot_index):
    while True:
        # Call step to ensure get_poses can be called
        

        # Get current poses and convert to single integrator states
        x = r.get_poses()
        r.step()
        x_si = uni_to_si_states(x)

        # Check if the robot is near the target position
        if np.linalg.norm(x_si[:, robot_index] - target_positions[:, robot_index]) <= 0.05:
            break

        # Initialize dxi for all robots
        dxi = np.zeros((2, N))

        # Set movement for the current robot
        dxi[:, robot_index] = si_position_controller(
            x_si[:, robot_index].reshape(2, 1),
            target_positions[:, robot_index].reshape(2, 1)
        ).flatten()

        # Apply barrier certificate
        dxi = si_barrier_cert(dxi, x_si)

        # Map to unicycle dynamics and set velocities for all robots
        dxu = si_to_uni_dyn(dxi, x)
        r.set_velocities(np.arange(N), dxu)
        
        # Step forward in the simulation
        

# Main simulation loop
for i in range(N):
    move_robot_up(i)

# Finalize the simulation
r.call_at_scripts_end()
