import matplotlib.patches as patches

class RobotConfigurator:
    def __init__(self, robotarium_instance, default_settings=None):
        self.robotarium_instance = robotarium_instance
        self.robot_settings = {}
        self.default_settings = default_settings or {
            'shape': {'radius': 0.05, 'outline_thickness': 1.0, 'head_marker_size': 0.03},
            'colors': {'fill_color': '#FFD700', 'outline_color': 'k', 'head_marker_color': 'k'},
            'flash': {'flash_fill': False, 'flash_outline': False, 'fill_flash_speed': 'medium', 'outline_flash_speed': 'medium'},
            'transparency': 1.0,
            'flash_color': '#FFFFFF'
        }

    def configure_robot(self, robot_id, settings=None):
            """Configures a robot with the provided settings or applies default settings if none provided."""
            settings = settings or self.default_settings
            self.robot_settings[robot_id] = settings  # Store settings for each robot

            # Apply settings
            shape = settings.get('shape', self.default_settings['shape'])
            colors = settings.get('colors', self.default_settings['colors'])
            flash = settings.get('flash', self.default_settings['flash'])
            transparency = settings.get('transparency', self.default_settings['transparency'])
            flash_color = settings.get('flash_color', self.default_settings['flash_color'])

            # Configure shape and color properties
            fill_color = colors['fill_color']
            outline_color = colors['outline_color']
            self.robotarium_instance.chassis_patches[robot_id].set_facecolor(fill_color)
            self.robotarium_instance.chassis_patches[robot_id].set_edgecolor(outline_color)
            self.robotarium_instance.chassis_patches[robot_id].set_alpha(transparency)
            self.robotarium_instance.chassis_patches[robot_id].set_linewidth(shape['outline_thickness'])

            # Configure head marker
            head_marker_color = colors['head_marker_color']
            head_marker_size = shape['head_marker_size']
            head_marker = patches.Circle(self.robotarium_instance.poses[:2, robot_id], head_marker_size, facecolor=head_marker_color, edgecolor=outline_color)
            self.robotarium_instance.axes.add_patch(head_marker)

            print(f"Configured robot {robot_id} with settings: {settings}")

    def get_robot_settings(self, robot_id):
        """Returns the settings for a specific robot."""
        return self.robot_settings.get(robot_id, self.default_settings)

    def print_all_robot_settings(self):
        """Prints out the settings for each robot."""
        for robot_id, settings in self.robot_settings.items():
            print(f"Robot {robot_id} settings: {settings}")

    def set_robot_colors_with_head(self, robot_id: int, fill_color: str, outline_color: str, head_marker_color: str) -> None:
        """Sets the fill color, outline color, and head marker color for the robot."""
        color_settings = {
            'colors': {
                'fill_color': fill_color,
                'outline_color': outline_color,
                'head_marker_color': head_marker_color
            }
        }
        
        # Use the `configure_robot` method to apply the color settings
        self.configure_robot(robot_id, color_settings)
        print(f"Updated colors for robot {robot_id}: fill_color={fill_color}, outline_color={outline_color}, head_marker_color={head_marker_color}")
