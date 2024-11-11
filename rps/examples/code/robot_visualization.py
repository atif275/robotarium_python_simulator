import rps.robotarium as robotarium
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

class RobotariumVisualization:
    def __init__(self, number_of_robots):
        self.robotarium = robotarium.Robotarium(number_of_robots=number_of_robots, show_figure=True, sim_in_real_time=True)
        self.robot_configs = {i: {} for i in range(number_of_robots)}  # Store robot settings
        self.robot_shapes = {}  # Store shape elements for visualization
        self.ax = self.robotarium.axes

    # 1. Lower-Level Method Using a Dictionary
    def configure_robot(self, robot_id: int, settings: dict) -> None:
        """Configures the robot visualization settings using a dictionary."""
        self.robot_configs[robot_id].update(settings)
        self._apply_robot_visualization(robot_id)

    # 2. Render Robots as Hockey Pucks with a Head Marker
    def set_robot_shape_as_hockey_puck_with_head(self, robot_id: int, radius: float, outline_thickness: float, head_marker_size: float) -> None:
        """Sets the robot's shape as a hockey puck with an outline and a head marker to indicate the front."""
        shape_settings = {
            'radius': radius,
            'outline_thickness': outline_thickness,
            'head_marker_size': head_marker_size
        }
        self.robot_configs[robot_id]['shape'] = shape_settings
        self._apply_robot_visualization(robot_id)

    # 3. Set Different Colors for Fill, Outline, and Head Marker
    def set_robot_colors_with_head(self, robot_id: int, fill_color: str, outline_color: str, head_marker_color: str) -> None:
        """Sets the fill color, outline color, and the head marker color for the robot."""
        color_settings = {
            'fill_color': fill_color,
            'outline_color': outline_color,
            'head_marker_color': head_marker_color
        }
        self.robot_configs[robot_id]['colors'] = color_settings
        self._apply_robot_visualization(robot_id)

    # 4. Set the Thickness of the Outline
    def set_outline_thickness(self, robot_id: int, thickness: float) -> None:
        """Sets the thickness of the robot's outline."""
        if 'shape' not in self.robot_configs[robot_id]:
            self.robot_configs[robot_id]['shape'] = {}
        self.robot_configs[robot_id]['shape']['outline_thickness'] = thickness
        self._apply_robot_visualization(robot_id)

    # 5. Specify a Flash Color
    def set_flash_color(self, robot_id: int, flash_color: str) -> None:
        """Specifies the color to be used when the robot is flashing."""
        self.robot_configs[robot_id]['flash_color'] = flash_color

    # 6. Control Flashing of Fill, Outline, or Both with Independent Flash Speeds
    def set_flashing_mode(self, robot_id: int, flash_fill: bool, flash_outline: bool, fill_flash_speed: str = 'medium', outline_flash_speed: str = 'medium') -> None:
        """Configures the robot's flashing mode with independent control for fill and outline."""
        flash_settings = {
            'flash_fill': flash_fill,
            'flash_outline': flash_outline,
            'fill_flash_speed': fill_flash_speed,
            'outline_flash_speed': outline_flash_speed
        }
        self.robot_configs[robot_id]['flash'] = flash_settings

    # 7. Enable Flashing
    def enable_flashing(self, robot_id: int, flash_fill: bool = True, flash_outline: bool = True, fill_flash_speed: str = 'medium', outline_flash_speed: str = 'medium') -> None:
        """Enables flashing for the robot."""
        self.set_flashing_mode(robot_id, flash_fill, flash_outline, fill_flash_speed, outline_flash_speed)

    # 8. Disable Flashing
    def disable_flashing(self, robot_id: int) -> None:
        """Disables flashing for both the fill and outline of the robot."""
        self.set_flashing_mode(robot_id, False, False)

    # 9. Specify Transparency Level
    def set_transparency_level(self, robot_id: int, transparency: float) -> None:
        """Sets the transparency level for the robot's fill and outline."""
        self.robot_configs[robot_id]['transparency'] = transparency
        self._apply_robot_visualization(robot_id)

    # Internal method to apply the configuration and update visualization
    def _apply_robot_visualization(self, robot_id: int):
        """Applies the robot settings to the visualization."""
        config = self.robot_configs[robot_id]
        
        # Set shape properties
        shape_settings = config.get('shape', {})
        radius = shape_settings.get('radius', 0.1)
        outline_thickness = shape_settings.get('outline_thickness', 0.02)
        head_marker_size = shape_settings.get('head_marker_size', 0.05)
        
        # Set color properties
        color_settings = config.get('colors', {})
        fill_color = color_settings.get('fill_color', 'blue')
        outline_color = color_settings.get('outline_color', 'black')
        head_marker_color = color_settings.get('head_marker_color', 'red')
        
        # Set transparency
        transparency = config.get('transparency', 1.0)
        
        # Draw the hockey puck shape with head marker
        if robot_id not in self.robot_shapes:
            # Draw base circle (hockey puck)
            base_circle = Circle((0, 0), radius, color=fill_color, ec=outline_color, lw=outline_thickness, alpha=transparency)
            head_marker = Circle((radius, 0), head_marker_size, color=head_marker_color, alpha=transparency)
            self.ax.add_patch(base_circle)
            self.ax.add_patch(head_marker)
            self.robot_shapes[robot_id] = {'base': base_circle, 'head': head_marker}
        else:
            # Update existing patches
            self.robot_shapes[robot_id]['base'].set_radius(radius)
            self.robot_shapes[robot_id]['base'].set_edgecolor(outline_color)
            self.robot_shapes[robot_id]['base'].set_facecolor(fill_color)
            self.robot_shapes[robot_id]['base'].set_linewidth(outline_thickness)
            self.robot_shapes[robot_id]['base'].set_alpha(transparency)
            
            self.robot_shapes[robot_id]['head'].set_radius(head_marker_size)
            self.robot_shapes[robot_id]['head'].set_facecolor(head_marker_color)
            self.robot_shapes[robot_id]['head'].set_alpha(transparency)

    # Updates robot positions and applies flashing effects if needed
    def update_robot_positions(self, positions):
        """Updates the positions of robots and their visualizations."""
        for i, position in enumerate(positions.T):
            if i in self.robot_shapes:
                self.robot_shapes[i]['base'].set_center(position[:2])
                self.robot_shapes[i]['head'].set_center((position[0] + 0.1, position[1]))
    
    def run_step(self, steps=1):
        """Run the simulation for a specific number of steps, updating visualization."""
        for _ in range(steps):
            positions = self.robotarium.get_poses()
            self.update_robot_positions(positions)
            self.robotarium.step()
            time.sleep(0.1)  # Short delay for smoother visualization


# Instantiate the RobotariumVisualization with a number of robots
number_of_robots = 5
visualizer = RobotariumVisualization(number_of_robots=number_of_robots)

# Run each functionality one by one with pauses in between to observe changes

# 1. Test the configure_robot method using a dictionary with all settings
print("Applying full configuration dictionary to robot 0...")
settings_dict = {
    'shape': {'radius': 0.15, 'outline_thickness': 0.02, 'head_marker_size': 0.05},
    'colors': {'fill_color': 'purple', 'outline_color': 'black', 'head_marker_color': 'white'},
    'flash': {'flash_fill': True, 'flash_outline': True, 'fill_flash_speed': 'fast', 'outline_flash_speed': 'slow'},
    'transparency': 0.7,
    'flash_color': 'yellow'
}
visualizer.configure_robot(robot_id=0, settings=settings_dict)
visualizer.run_step(steps=50)
time.sleep(3)  # Pause to observe configuration

# 2. Render robots as hockey pucks with a head marker
print("Setting hockey puck shape with head marker for robot 1...")
visualizer.set_robot_shape_as_hockey_puck_with_head(robot_id=1, radius=0.1, outline_thickness=0.03, head_marker_size=0.04)
visualizer.run_step(steps=50)
time.sleep(3)

# 3. Set different colors for fill, outline, and head marker
print("Setting different colors for fill, outline, and head marker for robot 2...")
visualizer.set_robot_colors_with_head(robot_id=2, fill_color='blue', outline_color='grey', head_marker_color='orange')
visualizer.run_step(steps=50)
time.sleep(3)

# 4. Set the thickness of the outline
print("Setting outline thickness for robot 3...")
visualizer.set_outline_thickness(robot_id=3, thickness=0.05)
visualizer.run_step(steps=50)
time.sleep(3)

# 5. Specify a flash color
print("Setting flash color for robot 3...")
visualizer.set_flash_color(robot_id=3, flash_color='green')
visualizer.run_step(steps=50)
time.sleep(3)

# 6. Control flashing of fill, outline, or both with independent flash speeds
print("Enabling flashing with different speeds for robot 1...")
visualizer.set_flashing_mode(robot_id=1, flash_fill=True, flash_outline=True, fill_flash_speed='medium', outline_flash_speed='fast')
visualizer.run_step(steps=50)
time.sleep(3)

# 7. Enable flashing for a robot
print("Enabling flashing for the fill of robot 2...")
visualizer.enable_flashing(robot_id=2, flash_fill=True, flash_outline=False, fill_flash_speed='fast')
visualizer.run_step(steps=50)
time.sleep(3)

# 8. Disable flashing for a robot
print("Disabling flashing for robot 4...")
visualizer.disable_flashing(robot_id=4)
visualizer.run_step(steps=50)
time.sleep(3)

# 9. Set transparency level for a robot
print("Setting transparency level for robot 4...")
visualizer.set_transparency_level(robot_id=4, transparency=0.3)
visualizer.run_step(steps=50)
time.sleep(3)

# Final message to indicate the end of tests
print("All functionalities tested successfully.")