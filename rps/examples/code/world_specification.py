import time
import yaml
import numpy as np
from PIL import Image
from matplotlib.patches import Circle, Rectangle
import rps.robotarium as robotarium

class LayerNotFoundError(Exception):
    """Custom error raised when attempting to add a geometric feature to a non-existing layer."""
    pass

class WorldSpecification:
    def __init__(self, visualizer):
        self.layers = {}
        self.base_layer_image = None
        self.visualizer = visualizer  # Pass Robotarium visualization instance

    def add_layers_in_order(self, layer_names: list) -> None:
        for name in layer_names:
            self.layers[name] = []
        print(f"Layers added in order: {layer_names}")
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
        print(f"Geometric feature '{feature_id}' added to layer '{layer_name}' with constraints: {constraints}")
        self.visualizer.display_feature(layer_name, feature)

    def is_point_in_geometric_object(self, point: tuple, geometric_object_id: str) -> bool:
        for layer_features in self.layers.values():
            for feature in layer_features:
                if feature["id"] == geometric_object_id:
                    for primitive in feature["primitives"]:
                        if self._is_point_in_primitive(point, primitive):
                            print(f"Point {point} is inside geometric object '{geometric_object_id}'")
                            self.visualizer.highlight_point(point, color="green")  # Highlight point
                            return True
        print(f"Point {point} is not inside geometric object '{geometric_object_id}'")
        self.visualizer.highlight_point(point, color="red")  # Highlight point in red if not inside
        return False

    def get_geometric_features_for_point(self, point: tuple) -> list:
        features_containing_point = []
        for layer_features in self.layers.values():
            for feature in layer_features:
                for primitive in feature["primitives"]:
                    if self._is_point_in_primitive(point, primitive):
                        features_containing_point.append(feature["id"])
                        break
        print(f"Features containing point {point}: {features_containing_point}")
        return features_containing_point

    def save_world_to_yaml(self, filename: str) -> None:
        data = {
            layer: [
                {
                    "id": feature["id"],
                    "primitives": [{**primitive, "center": list(primitive["center"])} if "center" in primitive else primitive
                                   for primitive in feature["primitives"]],
                    "constraints": feature["constraints"]
                } for feature in features
            ] for layer, features in self.layers.items()
        }
        with open(filename, 'w') as file:
            yaml.dump(data, file)
        print(f"World configuration saved to {filename}")

    def load_world_from_yaml(self, filename: str) -> None:
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
            self.layers = {
                layer: [
                    {
                        "id": feature["id"],
                        "primitives": [{**primitive, "center": tuple(primitive["center"])} if "center" in primitive else primitive
                                       for primitive in feature["primitives"]],
                        "constraints": feature["constraints"]
                    } for feature in features
                ] for layer, features in data.items()
            }
        print(f"World configuration loaded from {filename}")

    def set_base_layer_image(self, image_path: str) -> None:
        try:
            self.base_layer_image = Image.open(image_path)
            print(f"Base layer image set from {image_path}")
            self.visualizer.display_base_layer(image_path)
        except FileNotFoundError:
            print(f"Image file '{image_path}' not found.")

    def _is_point_in_primitive(self, point: tuple, primitive: dict) -> bool:
        if primitive["type"] == "circle":
            x, y = point
            cx, cy = primitive["center"]
            return (x - cx) ** 2 + (y - cy) ** 2 <= primitive["radius"] ** 2
        return False

class RobotariumVisualization:
    def __init__(self, number_of_robots):
        self.robotarium = robotarium.Robotarium(number_of_robots=number_of_robots, show_figure=True, sim_in_real_time=True)
        self.ax = self.robotarium.axes

    def display_layers(self, layer_names):
        print(f"Displaying layers: {layer_names}")
        for i, name in enumerate(layer_names):
            self.ax.text(-1.5, 1.2 - i * 0.1, f"Layer {i+1}: {name}", fontsize=10, color='black')
        self.robotarium.get_poses()  # Ensure poses are obtained before calling step()
        self.robotarium.step()

    def display_feature(self, layer_name, feature):
        # Set colors and boundary styles for specific layers
        color_map = {
            "Landmarks": ("green", "Landmark"),
            "RestrictedZones": ("red", "Restricted Zone")
        }
        feature_color, label = color_map.get(layer_name, ("blue", "Feature"))  # Default color and label

        for primitive in feature["primitives"]:
            if primitive["type"] == "circle":
                cx, cy = primitive["center"]
                radius = primitive["radius"]
                # Add circle with boundary and label
                circle = Circle((cx, cy), radius, fill=True, color=feature_color, alpha=0.2, edgecolor="black", linewidth=1.5)
                self.ax.add_patch(circle)
                self.ax.text(cx, cy, label, ha='center', va='center', color="black", fontsize=8, weight='bold')
                print(f"Visualizing {label} '{feature['id']}' in layer '{layer_name}' with color {feature_color}.")
        self.robotarium.get_poses()  # Ensure poses are obtained before calling step()
        self.robotarium.step()

    def display_base_layer(self, image_path):
        print(f"Setting base layer from image: {image_path}")
        base_img = Image.open(image_path)
        self.ax.imshow(base_img, extent=[-1, 1, -1, 1])
        self.robotarium.get_poses()  # Ensure poses are obtained before calling step()
        self.robotarium.step()

    def highlight_point(self, point, color):
        x, y = point
        self.ax.plot(x, y, 'o', color=color, markersize=8)
        self.robotarium.get_poses()
        self.robotarium.step()

# Initialize visualization
visualizer = RobotariumVisualization(number_of_robots=5)

# Initialize world specification with the visualizer
world = WorldSpecification(visualizer)

# Run each functionality with a time delay
time.sleep(1)
world.add_layers_in_order(["Base", "Landmarks", "RestrictedZones"])

time.sleep(1)
# Add a restricted zone
restricted_zone = [{'type': 'circle', 'radius': 50.0, 'center': (100, 100)}]
constraints = {
    'min_linear_velocity': 1.0,
    'max_linear_velocity': 10.0,
    'min_altitude': 0.0,
    'max_altitude': 100.0,
    'min_angular_velocity': 0.5,
    'max_angular_velocity': 2.0
}
try:
    world.add_geometric_feature_to_layer("restricted_zone_1", restricted_zone, "RestrictedZones", constraints)
except LayerNotFoundError as e:
    print(e)

time.sleep(1)
# Add a landmark
landmark = [{'type': 'circle', 'radius': 20.0, 'center': (50, 50)}]
try:
    world.add_geometric_feature_to_layer("landmark_1", landmark, "Landmarks", {})
except LayerNotFoundError as e:
    print(e)

time.sleep(1)
world.get_geometric_features_for_point((105, 105))

time.sleep(1)
world.save_world_to_yaml("world_config.yaml")

time.sleep(1)
world.load_world_from_yaml("world_config.yaml")

time.sleep(1)
world.set_base_layer_image("sample_map_image.png")
