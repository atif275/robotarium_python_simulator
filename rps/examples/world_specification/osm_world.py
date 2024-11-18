import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import time
from rps.robotarium import Robotarium

# Define location and download the map
location = "Central Park, New York, USA"  # Change this to your location of interest
G = ox.graph_from_place(location, network_type='all')  # Retrieve the full street network

# Create Robotarium instance with zero robots to display an empty world with the map
r = Robotarium(number_of_robots=1, show_figure=True, sim_in_real_time=True)

# Integrate the OSM map plot with the Robotarium figure
fig, ax = r.figure, r.axes  # Use Robotarium's figure and axes
ox.plot_graph(G, ax=ax, show=False, close=False, bgcolor='white')  # Overlay OSM graph on Robotarium plot

# Simulation loop
simulation_duration = 10  # seconds
start_time = time.time()

while time.time() - start_time < simulation_duration:
    r.get_poses()  # Dummy call to get poses (needed even with zero robots)
    r.step()       # Step forward in the simulation
    plt.pause(0.1)

r.call_at_scripts_end()
