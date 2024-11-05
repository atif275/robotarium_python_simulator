import rps.robotarium as robotarium
from rps.robot_configuration import RobotConfigurator
import time
import numpy as np

# Instantiate the Robotarium and configurator
N = 1  # One robot for testing
initial_conditions = np.array([[0], [0], [0]])  # Start position at the center

r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=False)
r.axes.set_xlim(-1.8, 1.8)  # Set x-axis limits
r.axes.set_ylim(-1.2, 1.2)  # Set y-axis limits

configurator = RobotConfigurator(r)

# Set colors for the robot at intervals
configurator.set_robot_colors_with_head(0, '#FF0000', 'black', 'white')  # Red with black outline and white head
print("Color set to red with black outline and white head")
r.get_poses()
r.step()
time.sleep(5)

configurator.set_robot_colors_with_head(0, '#00FF00', 'blue', 'yellow')  # Green with blue outline and yellow head
print("Color set to green with blue outline and yellow head")
r.get_poses()
r.step()
time.sleep(5)

configurator.set_robot_colors_with_head(0, '#0000FF', 'orange', 'black')  # Blue with orange outline and black head
print("Color set to blue with orange outline and black head")
r.get_poses()
r.step()
time.sleep(5)

# End the simulation
r.call_at_scripts_end()
