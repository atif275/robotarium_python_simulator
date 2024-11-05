import rps.robotarium as robotarium
from rps.utilities.barrier_certificates import create_single_integrator_barrier_certificate
from rps.utilities.controllers import create_si_position_controller
import numpy as np

# Number of robots
N = 3

# Instantiate the Robotarium object
r = robotarium.Robotarium(number_of_robots=N, show_figure=True, sim_in_real_time=True)

# Barrier certificate to avoid collisions
si_barrier_cert = create_single_integrator_barrier_certificate()

# Position controller
si_position_controller = create_si_position_controller()

# Define the parking slot and initial positions
parking_entrance = np.array([[0.1], [0]])  # Entrance at left side
parking_size = np.array([0.3, 0.1])  # Length and width
parking_positions = np.array([
    [parking_entrance[0] + parking_size[0]/3, parking_entrance[1]],
    [parking_entrance[0] + 2*parking_size[0]/3, parking_entrance[1]],
    [parking_entrance[0] + parking_size[0], parking_entrance[1]]
]).T

# Simulation parameters
iterations = 300  # Number of iterations the simulation will run
goal_region_reached = np.full(N, False)
goals = parking_positions

# Main simulation loop
for _ in range(iterations):
    x = r.get_poses()  # Get current positions (2xN matrix)
    dxi = np.zeros((2, N))  # Initialize velocities (2xN matrix)

    for i in range(N):
        if not goal_region_reached[i]:
            # Ensure we're passing the correct shapes
            current_position = x[:2, [i]]  # 2x1 matrix
            goal_position = goals[:, [i]]  # 2x1 matrix
            dxi[:, i] = si_position_controller(current_position, goal_position).flatten()

    # Apply the barrier certificates to avoid collisions
    dxi = si_barrier_cert(dxi, x[:2, :])

    # Update the robots' velocities
    r.set_velocities(np.arange(N), dxi)
    r.step()

    # Check if goals are reached
    for i in range(N):
        if np.linalg.norm(x[:2, i:i+1] - goals[:, i:i+1]) < 0.05:
            goal_region_reached[i] = True

# Finish the simulation
r.call_at_scripts_end()
