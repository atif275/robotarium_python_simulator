import numpy as np
import time
import math
from rps.robotarium import Robotarium

# Set up parameters
N = 1  # Number of robots
initial_conditions = np.array([[0.0], [0.0], [0.0]])  # Start position in the center

# Instantiate Robotarium object
r = Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=False)

# Add a grid pattern to the world background
r.add_grid(cell_width=0.5, cell_height=0.5)

# Run the circle movement for 10 seconds
start_time = time.time()
while time.time() - start_time < 10:
    # Get current positions of robots
    x = r.get_poses()

    # Define circular velocity (constant angular speed, small linear speed)
    linear_speed = 0.05  # Adjust to control radius of the circle
    angular_speed = math.pi / 4  # radians per second
    
    # Set velocity to make robot move in a circle
    dxu = np.array([[linear_speed], [angular_speed]])

    # Apply velocities and step
    r.set_velocities(np.arange(N), dxu)
    r.step()

# End of the script (Robotarium requirement)
r.call_at_scripts_end()
