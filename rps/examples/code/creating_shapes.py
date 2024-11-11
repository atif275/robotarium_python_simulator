import time
import numpy as np
import yaml
from shapely.geometry import LineString, Point, Polygon
import rps.robotarium as robotarium
from matplotlib.patches import Circle, Rectangle

class LayerNotFoundError(Exception):
    pass

class WorldSpecification:
    def __init__(self, visualizer):
        self.layers = {}
        self.visualizer = visualizer  # Pass Robotarium visualization instance

    def add_layers_in_order(self, layer_names: list) -> None:
        """
        Adds layers in the order specified by the list of layer names.
        """
        for name in layer_names:
            self.layers[name] = []
        print(f"Layers added in order: {layer_names}")
        self.visualizer.display_layers(layer_names)

    def add_geometric_feature_to_layer(self, feature_id: str, primitives: list, layer_name: str, constraints: dict) -> None:
        """
        Adds a geometric feature with constraints to a specific layer.
        """
        if layer_name not in self.layers:
            raise LayerNotFoundError(f"Layer '{layer_name}' does not exist.")
        
        feature = {
            "id": feature_id,
            "primitives": primitives,
            "constraints": constraints
        }
        self.layers[layer_name].append(feature)
        print(f"Geometric feature '{feature_id}' added to layer '{layer_name}' with constraints: {constraints}")
        self.visualizer.display_feature(layer_name, feature)

    def save_world_to_yaml(self, filename: str, number_of_robots: int) -> None:
        """
        Saves the current world representation to a YAML file, including number_of_robots.
        """
        data = {
            "number_of_robots": number_of_robots,
            **{
                layer: [
                    {
                        "id": feature["id"],
                        "primitives": [{**primitive, "center": list(primitive["center"])} if "center" in primitive else 
                                       {**primitive, "corner": list(primitive["corner"])} if "corner" in primitive else 
                                       {**primitive, "vertices": [list(vertex) for vertex in primitive["vertices"]]} if "vertices" in primitive else
                                       primitive
                                       for primitive in feature["primitives"]],
                        "constraints": feature["constraints"]
                    } for feature in features
                ] for layer, features in self.layers.items()
            }
        }
        with open(filename, 'w') as file:
            yaml.dump(data, file)
        print(f"World configuration saved to {filename}")

    def load_world_from_yaml(self, filename: str) -> int:
        """
        Loads a world representation from a YAML file and returns the number of robots.
        """
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)

        # Extract number of robots
        number_of_robots = data.get("number_of_robots", 1)

        # Add layers in the specified order from YAML data
        self.add_layers_in_order([key for key in data.keys() if key != "number_of_robots"])

        # Add each feature in each layer
        for layer_name, features in data.items():
            if layer_name == "number_of_robots":
                continue
            for feature in features:
                feature_id = feature["id"]
                primitives = feature["primitives"]
                constraints = feature.get("constraints", {})

                # Convert lists back to tuples for primitives (coordinates)
                for primitive in primitives:
                    if "center" in primitive:
                        primitive["center"] = tuple(primitive["center"])
                    if "corner" in primitive:
                        primitive["corner"] = tuple(primitive["corner"])
                    if "vertices" in primitive:
                        primitive["vertices"] = [tuple(vertex) for vertex in primitive["vertices"]]

                self.add_geometric_feature_to_layer(feature_id, primitives, layer_name, constraints)

        print(f"World configuration loaded from {filename}")
        return number_of_robots

class RobotariumVisualization:
    def __init__(self, number_of_robots):
        self.robotarium = robotarium.Robotarium(number_of_robots=number_of_robots, show_figure=True, sim_in_real_time=True)
        self.ax = self.robotarium.axes

    def display_layers(self, layer_names):
        # for i, name in enumerate(layer_names):
        #     self.ax.text(-1.5, 1.2 - i * 0.1, f"Layer {i+1}: {name}", fontsize=10, color='black')
        self.robotarium.get_poses()
        self.robotarium.step()

    def display_feature(self, layer_name, feature):
        if layer_name == "RestrictedZones":
            feature_color = "red"
            label = "Restricted Zone"
        else:
            color_map = {"Landmarks": "green"}
            feature_color = color_map.get(layer_name, "blue")
            label = "Feature"

        for primitive in feature["primitives"]:
            if primitive["type"] == "circle":
                cx, cy = primitive["center"]
                radius = primitive["radius"]
                circle = Circle((cx, cy), radius, fill=True, color=feature_color, alpha=0.2, edgecolor="black", linewidth=1.5)
                self.ax.add_patch(circle)
                if layer_name == "RestrictedZones":
                    self.ax.text(cx, cy, label, ha='center', va='center', color="black", fontsize=8, weight='bold')
            elif primitive["type"] == "rectangle":
                x, y = primitive["corner"]
                width, height = primitive["width"], primitive["height"]
                rect = Rectangle((x, y), width, height, fill=True, color=feature_color, alpha=0.2, edgecolor="black", linewidth=1.5)
                self.ax.add_patch(rect)
            elif primitive["type"] == "polygon":
                poly_points = primitive["vertices"]
                polygon = Polygon(poly_points)
                x, y = polygon.exterior.xy
                self.ax.fill(x, y, alpha=0.2, color=feature_color)
            print(f"Visualizing '{feature['id']}' in layer '{layer_name}' with color {feature_color}.")
        self.robotarium.get_poses()
        self.robotarium.step()

    def draw_line_segment(self, point_a, point_b):
        x_values = [point_a[0], point_b[0]]
        y_values = [point_a[1], point_b[1]]
        self.ax.plot(x_values, y_values, color="blue", linestyle="--", linewidth=1)
        self.robotarium.get_poses()
        self.robotarium.step()

    def display_point(self, point, color="orange", size=50):
        self.ax.plot(point[0], point[1], 'o', color=color, markersize=size)
        self.robotarium.get_poses()
        self.robotarium.step()


# Example usage
number_of_robots = 5
visualizer = RobotariumVisualization(number_of_robots=number_of_robots)
world = WorldSpecification(visualizer)

# Define layers
world.add_layers_in_order(["Base", "Landmarks", "RestrictedZones"])

# Add features with constraints
restricted_zone_constraints = {
    'min_linear_velocity': 1.0,
    'max_linear_velocity': 10.0,
    'min_altitude': 0.0,
    'max_altitude': 100.0,
    'min_angular_velocity': 0.5,
    'max_angular_velocity': 2.0
}
restricted_zone = [{'type': 'circle', 'radius': 0.1, 'center': (0.5, 0.5)}]
world.add_geometric_feature_to_layer("restricted_zone_1", restricted_zone, "RestrictedZones", restricted_zone_constraints)

landmark_constraints = {'min_altitude': 0.0, 'max_altitude': 50.0}
landmark = [{'type': 'rectangle', 'corner': (-0.5, -0.5), 'width': 0.2, 'height': 0.1}]
world.add_geometric_feature_to_layer("landmark_1", landmark, "Landmarks", landmark_constraints)

polygon_constraints = {'max_linear_velocity': 5.0, 'min_altitude': 5.0, 'max_altitude': 30.0}
polygon_feature = [{'type': 'polygon', 'vertices': [(0, 0), (0.3, 0), (0.3, 0.3), (0, 0.3)]}]
world.add_geometric_feature_to_layer("polygon_1", polygon_feature, "Landmarks", polygon_constraints)

# Save and load world configuration to/from YAML
yaml_filename = "world_config.yaml"
world.save_world_to_yaml(yaml_filename, number_of_robots)
loaded_number_of_robots = world.load_world_from_yaml(yaml_filename)

# Update the RobotariumVisualization instance if needed based on loaded robot count
if loaded_number_of_robots != number_of_robots:
    visualizer = RobotariumVisualization(number_of_robots=loaded_number_of_robots)

# Visualization loop
for _ in range(500):
    visualizer.robotarium.get_poses()
    visualizer.robotarium.step()

visualizer.robotarium.call_at_scripts_end()
