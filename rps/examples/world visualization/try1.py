import rps.robotarium as robotarium
from rps.utilities.barrier_certificates import create_unicycle_barrier_certificate
from rps.utilities.controllers import create_clf_unicycle_pose_controller
import numpy as np
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run Robotarium simulation with optional robot color.")
parser.add_argument('--color', type=str, help="Set the robot color in hex (e.g., '#FF0000' for red).")
args = parser.parse_args()

# Number of robots
N = 3

# Instantiate the Robotarium object with initial conditions (positions around the boundary)
initial_conditions = np.array([[0.8, 0, -0.8], [0.5, -0.5, 0.5], [0, 0, 0]])  # x, y, theta
r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=True)

# Set robot color only if a color argument is provided
if args.color:
    r.set_robot_color(args.color)

# Define parking slot entrance and positions (all 3 robots head to the same entrance)
parking_entrance = np.array([[0.1, 0.1, 0.1],  # x positions for all robots
                             [0, 0, 0],        # y positions for all robots
                             [0, 0, 0]])       # orientation for all robots

# Define the final parking positions (each robot will park in its own spot)
parking_positions = np.array([[0.3, 0.5, 0.7],  # x positions (parking spots)
                              [0, 0, 0],        # y positions (aligned)
                              [0, 0, 0]])       # orientation (0 for straight face)

# Create unicycle pose controller
unicycle_pose_controller = create_clf_unicycle_pose_controller()

# Create barrier certificates to avoid collision
uni_barrier_cert = create_unicycle_barrier_certificate()

# Visualization: Add parking slot (3 walls and entrance)
# Wall coordinates: bottom, right, and top (entrance on the left side)
bottom_wall = [[0, 0.8], [-0.1, -0.1]]   # Bottom wall
right_wall = [[0.8, 0.8], [-0.1, 0.1]]   # Right wall
top_wall = [[0, 0.8], [0.1, 0.1]]        # Top wall

# Plot the walls of the parking slot (left side is the entrance)
r.axes.plot(bottom_wall[0], bottom_wall[1], color='k', linewidth=4)  # Bottom wall
r.axes.plot(right_wall[0], right_wall[1], color='k', linewidth=4)    # Right wall
r.axes.plot(top_wall[0], top_wall[1], color='k', linewidth=4)        # Top wall

# Step to make the walls visible before starting the simulation
x = r.get_poses()
r.step()

# Main simulation loop
for i in range(1000):  # Limiting the simulation steps to 1000
    # Get current positions of robots
    x = r.get_poses()  # Make sure to get poses before each step

    # Move robots towards the parking entrance first
    if i < 300:  # The robots will move towards the entrance for the first 300 steps
        dxu = unicycle_pose_controller(x, parking_entrance)
    else:
        # After reaching the entrance, move them to their respective parking spots
        dxu = unicycle_pose_controller(x, parking_positions)

    # Ensure collision-free inputs using barrier certificates
    dxu = uni_barrier_cert(dxu, x)

    # Set the velocities and step the simulation forward
    r.set_velocities(np.arange(N), dxu)
    r.step()

    # Check if all robots are parked and stop them
    if i >= 300 and np.allclose(x[:2, :], parking_positions[:2, :], atol=0.05):
        break  # End the simulation when all robots have parked

# Finalize the simulation
r.call_at_scripts_end()
