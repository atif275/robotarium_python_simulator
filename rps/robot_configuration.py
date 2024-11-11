# robot_configuration.py

import matplotlib.patches as patches

class RobotConfigurator:
    def __init__(self, robotarium_instance, default_settings=None):
        self.robotarium_instance = robotarium_instance
        self.robot_settings = {}  # Stores settings for each robot by ID
        
        # Default settings for robots
        self.default_settings = default_settings or {
            'shape': {
                'radius': 0.05,
                'outline_thickness': 1.0,
                'head_marker_size': 0.03
            },
            'colors': {
                'fill_color': '#FFD700',  # Default fill color
                'outline_color': 'k',     # Default outline color
                'head_marker_color': 'k'  # Default head marker color
            },
            'flash': {
                'flash_fill': False,      # Fill flashing enabled/disabled
                'flash_outline': False,   # Outline flashing enabled/disabled
                'fill_flash_speed': 'medium',   # Flash speed for fill
                'outline_flash_speed': 'medium' # Flash speed for outline
            },
            'transparency': 1.0,         # Default transparency level (fully opaque)
            'flash_color': '#FFFFFF'     # Default flash color
        }

    # def configure_robot(self, robot_id, settings=None):
    #     """
    #     Configures a robot with the provided settings or applies default settings if none provided.
    #     This method merges the incoming settings with defaults, allowing partial updates.
        
    #     Parameters:
    #     - robot_id: Unique identifier for the robot.
    #     - settings: Dictionary containing settings for shape, colors, flashing, transparency, etc.
    #     """
    #     settings = settings or self.default_settings.copy()
    #     self.robot_settings[robot_id] = settings  # Store settings for each robot

    #     # Apply settings for visual elements
    #     shape = settings.get('shape', self.default_settings['shape'])
    #     colors = settings.get('colors', self.default_settings['colors'])
    #     transparency = settings.get('transparency', self.default_settings['transparency'])

    #     # Update shape and color properties in the Robotarium instance
    #     self._apply_visual_settings(robot_id, shape, colors, transparency)
        
    def configure_robot(self, robot_id, settings=None):
        """
        Configures a robot with the provided settings or applies default settings if none provided.
        This method merges the incoming settings with defaults, allowing partial updates.
        
        Parameters:
        - robot_id: Unique identifier for the robot.
        - settings: Dictionary containing settings for shape, colors, flashing, transparency, etc.
        """
        settings = settings or {}
        
        # Merge default shape settings if not all provided
        shape_settings = self.default_settings['shape'].copy()
        shape_settings.update(settings.get('shape', {}))
        
        # Merge default color settings if not all provided
        color_settings = self.default_settings['colors'].copy()
        color_settings.update(settings.get('colors', {}))
        
        # Other settings
        transparency = settings.get('transparency', self.default_settings['transparency'])
        flash_settings = settings.get('flash', self.default_settings['flash'])

        # Combine all settings
        full_settings = {
            'shape': shape_settings,
            'colors': color_settings,
            'transparency': transparency,
            'flash': flash_settings,
            'flash_color': settings.get('flash_color', self.default_settings['flash_color'])
        }
        
        self.robot_settings[robot_id] = full_settings  # Store settings for each robot
        
        # Apply settings for visual elements
        self._apply_visual_settings(robot_id, full_settings['shape'], full_settings['colors'], full_settings['transparency'])

    def _apply_visual_settings(self, robot_id, shape, colors, transparency):
        """
        Internal helper to apply visual settings like shape, color, and transparency to the robot's Matplotlib patches.
        
        Parameters:
        - robot_id: The identifier of the robot.
        - shape: Dictionary containing shape settings (radius, outline thickness, head marker size).
        - colors: Dictionary containing color settings (fill color, outline color, head marker color).
        - transparency: Transparency level for the robot.
        """
        # Set chassis (main body) colors and transparency
        fill_color = colors['fill_color']
        outline_color = colors['outline_color']
        head_marker_color = colors['head_marker_color']
        
        # Apply settings to the robot's chassis patch
        chassis = self.robotarium_instance.chassis_patches[robot_id]
        chassis.set_facecolor(fill_color)
        chassis.set_edgecolor(outline_color)
        chassis.set_alpha(transparency)
        chassis.set_linewidth(shape['outline_thickness'])
        
        # Configure the head marker
        head_marker = patches.Circle(
            self.robotarium_instance.poses[:2, robot_id],
            shape['head_marker_size'],
            facecolor=head_marker_color,
            edgecolor=outline_color
        )
        # Remove any existing head marker, then add the new one
        if len(self.robotarium_instance.left_led_patches) > robot_id:
            self.robotarium_instance.left_led_patches[robot_id].remove()
        self.robotarium_instance.left_led_patches[robot_id] = head_marker
        self.robotarium_instance.axes.add_patch(head_marker)

    def set_robot_colors_with_head(self, robot_id: int, fill_color: str, outline_color: str, head_marker_color: str) -> None:
        """
        Sets the fill color, outline color, and head marker color for the robot.
        
        Parameters:
        - robot_id: The identifier of the robot.
        - fill_color: Color for the main body (fill).
        - outline_color: Color for the outline.
        - head_marker_color: Color for the head marker.
        """
        # Update only color settings
        color_settings = {
            'colors': {
                'fill_color': fill_color,
                'outline_color': outline_color,
                'head_marker_color': head_marker_color
            }
        }
        self.configure_robot(robot_id, color_settings)  # Update the configuration with new colors

    def set_outline_thickness(self, robot_id: int, thickness: float) -> None:
        """
        Sets the thickness of the robot's outline.
        
        Parameters:
        - robot_id: The identifier of the robot.
        - thickness: Outline thickness value.
        """
        outline_settings = {
            'shape': {
                'outline_thickness': thickness
            }
        }
        self.configure_robot(robot_id, outline_settings)

    def set_flash_color(self, robot_id: int, flash_color: str) -> None:
        """
        Specifies the flash color to be used when flashing is enabled.
        
        Parameters:
        - robot_id: The identifier of the robot.
        - flash_color: The color to be used for flashing.
        """
        flash_settings = {
            'flash_color': flash_color
        }
        self.configure_robot(robot_id, flash_settings)

    def enable_flashing(self, robot_id: int, flash_fill=True, flash_outline=True, fill_flash_speed='medium', outline_flash_speed='medium') -> None:
        """
        Enables flashing for the robot with specified flash speed settings.
        
        Parameters:
        - robot_id: The identifier of the robot.
        - flash_fill: If True, the fill will flash.
        - flash_outline: If True, the outline will flash.
        - fill_flash_speed: Flash speed for the fill ('slow', 'medium', 'fast').
        - outline_flash_speed: Flash speed for the outline ('slow', 'medium', 'fast').
        """
        flash_settings = {
            'flash': {
                'flash_fill': flash_fill,
                'flash_outline': flash_outline,
                'fill_flash_speed': fill_flash_speed,
                'outline_flash_speed': outline_flash_speed
            }
        }
        self.configure_robot(robot_id, flash_settings)

    def disable_flashing(self, robot_id: int) -> None:
        """
        Disables flashing for both the fill and outline.
        
        Parameters:
        - robot_id: The identifier of the robot.
        """
        flash_settings = {
            'flash': {
                'flash_fill': False,
                'flash_outline': False
            }
        }
        self.configure_robot(robot_id, flash_settings)

    def set_transparency_level(self, robot_id: int, transparency: float) -> None:
        """
        Sets the transparency level for the robot.
        
        Parameters:
        - robot_id: The identifier of the robot.
        - transparency: Transparency level (0.0 to 1.0).
        """
        transparency_settings = {
            'transparency': transparency
        }
        self.configure_robot(robot_id, transparency_settings)

    def get_robot_settings(self, robot_id: int) -> dict:
        """
        Returns the current configuration settings for a specific robot.
        
        Parameters:
        - robot_id: The identifier of the robot.
        
        Returns:
        - A dictionary containing the robot's configuration settings.
        """
        return self.robot_settings.get(robot_id, self.default_settings)

    def print_all_robot_settings(self) -> None:
        """
        Prints out the settings for each robot in the Robotarium environment.
        """
        if not self.robot_settings:
            print("No robot settings available.")
            return
        
        for robot_id, settings in self.robot_settings.items():
            print(f"Robot {robot_id} settings:")
            for category, values in settings.items():
                print(f"  {category.capitalize()}:")
                for key, value in values.items() if isinstance(values, dict) else [(None, values)]:
                    if key is not None:
                        print(f"    {key}: {value}")
                    else:
                        print(f"    {values}")
            print()  # Blank line between robots for readability
