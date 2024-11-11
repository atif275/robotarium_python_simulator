import rps.robotarium as robotarium
import numpy as np
import time

# Instantiate the Robotarium object with one robot (required by the library)
r = robotarium.Robotarium(number_of_robots=1, show_figure=True, sim_in_real_time=True)

# Define start and end points for the line
start_point = np.array([-1, -1])
end_point = np.array([1, 1])

slope = (end_point[1]-(start_point[1]))/(end_point[0]-(start_point[0]))

y_intercept = ((-1)*((slope)*(start_point[0])))+(start_point[1])

# Draw the line on the Robotarium
r.axes.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color="blue")



# Render the line and keep the screen open for a while
for _ in range(100):  # Adjust this range to control the display duration
    _ = r.get_poses()  # Call get_poses in each iteration
    r.step()
    time.sleep(0.1)  # Delay to keep the screen open

# Finalize the script
r.call_at_scripts_end()
