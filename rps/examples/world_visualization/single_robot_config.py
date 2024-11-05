import rps.robotarium as robotarium
from rps.robot_configuration import RobotConfigurator
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
import numpy as np
import time

# Define the robot configurations
robot_configurations = [
    {
        'shape': {'radius': 0.05, 'outline_thickness': 1.0, 'head_marker_size': 0.03},
        'colors': {'fill_color': '#FFD700', 'outline_color': 'black', 'head_marker_color': 'black'},
        'flash': {'flash_fill': False, 'flash_outline': False, 'fill_flash_speed': 'medium', 'outline_flash_speed': 'medium'},
        'transparency': 1.0,
        'flash_color': '#FFFFFF'
    },
    {
        'shape': {'radius': 0.06, 'outline_thickness': 2.0, 'head_marker_size': 0.04},
        'colors': {'fill_color': '#00FF00', 'outline_color': 'blue', 'head_marker_color': 'red'},
        'flash': {'flash_fill': True, 'flash_outline': True, 'fill_flash_speed': 'fast', 'outline_flash_speed': 'slow'},
        'transparency': 0.8,
        'flash_color': '#FF0000'
    },
    {
        'shape': {'radius': 0.05, 'outline_thickness': 1.5, 'head_marker_size': 0.05},
        'colors': {'fill_color': '#0000FF', 'outline_color': 'orange', 'head_marker_color': 'white'},
        'flash': {'flash_fill': False, 'flash_outline': False, 'fill_flash_speed': 'medium', 'outline_flash_speed': 'medium'},
        'transparency': 1.0,
        'flash_color': '#FFFFFF'
    },
    {
        'shape': {'radius': 0.07, 'outline_thickness': 2.5, 'head_marker_size': 0.06},
        'colors': {'fill_color': '#FF00FF', 'outline_color': 'green', 'head_marker_color': 'yellow'},
        'flash': {'flash_fill': True, 'flash_outline': False, 'fill_flash_speed': 'slow', 'outline_flash_speed': 'medium'},
        'transparency': 0.9,
        'flash_color': '#00FFFF'
    },
    {
        'shape': {'radius': 0.05, 'outline_thickness': 2.0, 'head_marker_size': 0.04},
        'colors': {'fill_color': '#FFFF00', 'outline_color': 'purple', 'head_marker_color': 'black'},
        'flash': {'flash_fill': False, 'flash_outline': True, 'fill_flash_speed': 'medium', 'outline_flash_speed': 'fast'},
        'transparency': 1.0,
        'flash_color': '#FF00FF'
    }
]

# Instantiate the Robotarium and configurator
N = 1  # Only one robot
initial_conditions = np.array([[-1.5], [0.0], [0]])  # Initial position of the robot

r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=False)
configurator = RobotConfigurator(r)

# Set initial controller and barrier certificate
single_integrator_position_controller = create_si_position_controller()
si_barrier_cert = create_single_integrator_barrier_certificate_with_boundary()
si_to_uni_dyn, uni_to_si_states = create_si_to_uni_mapping()

# Define the waypoint for the robot (just stays in one spot)
waypoints = np.array([[-1.5], [0.0]])

# Function to update robot configuration
def update_robot_config(robot_id, config):
    print(f"Applying new configuration for robot {robot_id}: {config}")
    configurator.configure_robot(robot_id, config)

# Main simulation loop with configuration changes
for config_index, config in enumerate(robot_configurations):
    print(f"Configuration {config_index + 1}")
    update_robot_config(0, config)  # Update configuration for the robot

    # Run for 5 seconds with this configuration
    start_time = time.time()
    while time.time() - start_time < 3:
        # Get current poses
        x = r.get_poses()
        x_si = uni_to_si_states(x)

        # Compute control inputs and apply safe barrier certificates
        dxi = single_integrator_position_controller(x_si, waypoints)
        dxi = si_barrier_cert(dxi, x_si)
        dxu = si_to_uni_dyn(dxi, x)

        # Set velocities and step
        r.set_velocities(np.arange(N), dxu)
        r.step()

# End simulation
r.call_at_scripts_end()
