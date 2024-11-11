import yaml
import rps.robotarium as robotarium
from shapely.geometry import Polygon
from matplotlib.patches import Circle, Rectangle

class LayerNotFoundError(Exception):
    pass

class WorldSpecification:
    def __init__(self, visualizer):
        self.layers = {}
        self.visualizer = visualizer  # Pass Robotarium visualization instance

    def add_layers_in_order(self, layer_names: list) -> None:
        for name in layer_names:
            self.layers[name] = []
        self.visualizer.display_layers(layer_names)

    def add_geometric_feature_to_layer(self, feature_id: str, primitives: list, layer_name: str, constraints: dict) -> None:
        if layer_name not in self.layers:
            raise LayerNotFoundError(f"Layer '{layer_name}' does not exist.")
        
        feature = {
            "id": feature_id,
            "primitives": primitives,
            "constraints": constraints
        }
        self.layers[layer_name].append(feature)
        self.visualizer.display_feature(layer_name, feature)

    def load_world_from_yaml(self, filename: str) -> int:
        """
        Loads a world representation from a YAML file and dynamically adds layers and features.
        Returns the number of robots specified in the YAML file.
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
                continue  # Skip robot count as it's already processed
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

# Main script to load world from YAML and visualize it
yaml_filename = "world_config.yaml"

# Temporary loading the YAML to get the robot count
with open(yaml_filename, 'r') as file:
    number_of_robots = yaml.safe_load(file).get("number_of_robots", 1)

# Initialize visualization with dynamically loaded robot count
visualizer = RobotariumVisualization(number_of_robots=number_of_robots)
world = WorldSpecification(visualizer)

# Load world configuration from YAML file
world.load_world_from_yaml(yaml_filename)

# Run the visualization loop to display the loaded world
for _ in range(500):
    visualizer.robotarium.get_poses()
    visualizer.robotarium.step()

visualizer.robotarium.call_at_scripts_end()
