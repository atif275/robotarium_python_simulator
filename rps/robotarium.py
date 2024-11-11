import math
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rps.robotarium_abc import *
from rps.robot_configuration import RobotConfigurator

# Robotarium This object provides routines to interface with the Robotarium.
#
# THIS CLASS SHOULD NEVER BE MODIFIED OR SUBMITTED

class Robotarium(RobotariumABC):

        def __init__(self, number_of_robots=-1, show_figure=True, sim_in_real_time = True, initial_conditions=np.array([])):
            super().__init__(number_of_robots, show_figure, sim_in_real_time, initial_conditions)
            # Initialize RobotConfigurator for robot visualization control
            self.configurator = RobotConfigurator(self)
           
            #Initialize some rendering variables
            self.previous_render_time = time.time()
            self.sim_in_real_time = sim_in_real_time

            #Initialize checks for step and get poses calls
            self._called_step_already = True
            self._checked_poses_already = False

            #Initialization of error collection.
            self._errors = {}

            #Initialize steps
            self._iterations = 0 
            # Grid properties
            self.grid_added = False
            self.cell_width = 0.2
            self.cell_height = 0.2
        
        def add_grid(self, cell_width=0.2, cell_height=0.2):
            """Adds a grid pattern to the world background."""
            self.grid_added = True
            self.cell_width = cell_width
            self.cell_height = cell_height
            print("Adding grid to world background...")


            # Draw grid
            for x in np.arange(self.boundaries[0], self.boundaries[0] + self.boundaries[2], cell_width):
                self.axes.plot([x, x], [self.boundaries[1], self.boundaries[1] + self.boundaries[3]], 'k--', linewidth=0.5)
            
            for y in np.arange(self.boundaries[1], self.boundaries[1] + self.boundaries[3], cell_height):
                self.axes.plot([self.boundaries[0], self.boundaries[0] + self.boundaries[2]], [y, y], 'k--', linewidth=0.5)

            self.figure.canvas.draw_idle()
            self.figure.canvas.flush_events()

        def add_dynamic_grid(ax, robotarium_instance, cell_size):
            """
            Adds a grid to the background of the world with dynamic rows and columns based on cell size.
            """
            # Dynamically get the world boundaries
            world_width = robotarium_instance.boundaries[2]
            world_height = robotarium_instance.boundaries[3]
            
            # Calculate the number of rows and columns based on cell size
            num_cols = int(world_width / cell_size)
            num_rows = int(world_height / cell_size)
            
            # Draw vertical lines (columns)
            for i in range(num_cols + 1):
                x = i * cell_size - world_width / 2  # Adjust to center the grid
                ax.plot([x, x], [-world_height / 2, world_height / 2], 'gray', linewidth=0.5)

            # Draw horizontal lines (rows)
            for j in range(num_rows + 1):
                y = j * cell_size - world_height / 2  # Adjust to center the grid
                ax.plot([-world_width / 2, world_width / 2], [y, y], 'gray', linewidth=0.5)

            print(f"Added a dynamic grid with {num_cols} columns and {num_rows} rows based on cell size {cell_size}.")


        def get_poses(self):
            """Returns the states of the agents.

            -> 3xN numpy array (of robot poses)
            """

            assert(not self._checked_poses_already), "Can only call get_poses() once per call of step()."
            # Allow step() to be called again.
            self._called_step_already = False
            self._checked_poses_already = True 

            return self.poses

        def call_at_scripts_end(self):
            """Call this function at the end of scripts to display potentail errors.  
            Even if you don't want to print the errors, calling this function at the
            end of your script will enable execution on the Robotarium testbed.
            """
            print('##### DEBUG OUTPUT #####')
            print('Your simulation will take approximately {0} real seconds when deployed on the Robotarium. \n'.format(math.ceil(self._iterations*self.time_step)))
            # TODO: check collision string and boundary string
            if bool(self._errors):
                if "boundary" in self._errors:
                    boundary_violations = max(self._errors["boundary"].values())
                    print('\t Simulation had {0} {1}\n'.format(boundary_violations, self._errors["boundary_string"]))
                if "collision" in self._errors:
                    collision_violations = max(self._errors["collision"].values())
                    print('\t Simulation had {0} {1}\n'.format(collision_violations, self._errors["collision_string"]))
                if "actuator" in self._errors:
                    print('\t Simulation had {0} {1}'.format(self._errors["actuator"], self._errors["actuator_string"]))
            else:
                print('No errors in your simulation! Acceptance of your experiment is likely!')

            return

        def step(self):
            """Increments the simulation by updating the dynamics.
            """
            assert(not self._called_step_already), "Make sure to call get_poses before calling step() again."
            
            # Allow get_poses function to be called again.
            self._called_step_already = True
            self._checked_poses_already = False

            # Validate before thresholding velocities
            self._errors = self._validate()
            self._iterations += 1

            #Perform Thresholding of Motors
            self.velocities = self._threshold(self.velocities)

            # Update dynamics of agents
            self.poses[0, :] = self.poses[0, :] + self.time_step*np.cos(self.poses[2,:])*self.velocities[0, :]
            self.poses[1, :] = self.poses[1, :] + self.time_step*np.sin(self.poses[2,:])*self.velocities[0, :]
            self.poses[2, :] = self.poses[2, :] + self.time_step*self.velocities[1, :]
            # Ensure angles are wrapped
            self.poses[2, :] = np.arctan2(np.sin(self.poses[2, :]), np.cos(self.poses[2, :]))

            # Update graphics
            if(self.show_figure):
                if(self.sim_in_real_time):
                    t = time.time()
                    while(t - self.previous_render_time < self.time_step):
                        t=time.time()
                    self.previous_render_time = t

                for i in range(self.number_of_robots):
                    settings = self.configurator.get_robot_settings(i)
                    self.chassis_patches[i].xy = self.poses[:2, i]+self.robot_length/2*np.array((np.cos(self.poses[2, i]+math.pi/2), np.sin(self.poses[2, i]+math.pi/2)))+\
                                            0.04*np.array((-np.sin(self.poses[2, i]+math.pi/2), np.cos(self.poses[2, i]+math.pi/2)))  + self.robot_length/2*np.array((np.cos(self.poses[2, i]), np.sin(self.poses[2, i])))
                    
                    self.chassis_patches[i].angle = (self.poses[2, i] - math.pi/2) * 180/math.pi

                    self.chassis_patches[i].zorder = 2

                    self.right_wheel_patches[i].center = self.poses[:2, i]+self.robot_length/2*np.array((np.cos(self.poses[2, i]+math.pi/2), np.sin(self.poses[2, i]+math.pi/2)))+\
                                            0.04*np.array((-np.sin(self.poses[2, i]+math.pi/2), np.cos(self.poses[2, i]+math.pi/2)))  + self.robot_length/2*np.array((np.cos(self.poses[2, i]), np.sin(self.poses[2, i])))
                    self.right_wheel_patches[i].orientation = self.poses[2, i] + math.pi/4

                    self.right_wheel_patches[i].zorder = 2

                    self.left_wheel_patches[i].center = self.poses[:2, i]+self.robot_length/2*np.array((np.cos(self.poses[2, i]-math.pi/2), np.sin(self.poses[2, i]-math.pi/2)))+\
                                            0.04*np.array((-np.sin(self.poses[2, i]+math.pi/2), np.cos(self.poses[2, i]+math.pi/2))) + self.robot_length/2*np.array((np.cos(self.poses[2, i]), np.sin(self.poses[2, i])))
                    self.left_wheel_patches[i].orientation = self.poses[2,i] + math.pi/4

                    self.left_wheel_patches[i].zorder = 2
                    #  # Set chassis to green
                    # self.chassis_patches[i].set_facecolor([0, 1, 0])
                    # self.chassis_patches[i].set_edgecolor([0, 1, 0])

                    #  # Set LEDs to green as well (if they are currently set to a color)
                    # self.left_led_patches[i].set_facecolor([0, 1, 0])
                    # self.right_led_patches[i].set_facecolor([0, 1, 0])
                    # self.left_led_patches[i].set_edgecolor([0, 1, 0])
                    # self.right_led_patches[i].set_edgecolor([0, 1, 0])
                    
                    self.right_led_patches[i].center = self.poses[:2, i]+0.75*self.robot_length/2*np.array((np.cos(self.poses[2,i]), np.sin(self.poses[2,i])))-\
                                    0.04*np.array((-np.sin(self.poses[2, i]), np.cos(self.poses[2, i]))) + self.robot_length/2*np.array((np.cos(self.poses[2, i]), np.sin(self.poses[2, i])))
                    self.left_led_patches[i].center = self.poses[:2, i]+0.75*self.robot_length/2*np.array((np.cos(self.poses[2,i]), np.sin(self.poses[2,i])))-\
                                    0.015*np.array((-np.sin(self.poses[2, i]), np.cos(self.poses[2, i]))) + self.robot_length/2*np.array((np.cos(self.poses[2, i]), np.sin(self.poses[2, i])))
                    self.left_led_patches[i].zorder = 2
                    self.right_led_patches[i].zorder = 2 

                self.figure.canvas.draw_idle()
                self.figure.canvas.flush_events()

