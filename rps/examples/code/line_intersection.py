import time
import numpy as np
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

        Parameters:
        - layer_names: List of layer names to be added in order.
        """
        for name in layer_names:
            self.layers[name] = []
        print(f"Layers added in order: {layer_names}")
        self.visualizer.display_layers(layer_names)

    def add_geometric_feature_to_layer(self, feature_id: str, primitives: list, layer_name: str, constraints: dict) -> None:
        """
        Adds a geometric feature with constraints to a specific layer. Raises an error if the layer does not exist.
        
        Parameters:
        - feature_id: The identifier of the geometric feature.
        - primitives: A list of geometric primitives (points, rectangles, circles, polygons).
        - layer_name: The name of the layer to which the geometric feature will be added.
        - constraints: A dictionary defining constraints such as:
            - 'min_linear_velocity': float
            - 'max_linear_velocity': float
            - 'min_altitude': float
            - 'max_altitude': float
            - 'min_angular_velocity': float
            - 'max_angular_velocity': float
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

    def get_intersections_with_geometric_features(self, point_a: tuple, point_b: tuple) -> list:
        intersections = []
        line = LineString([point_a, point_b])
        
        for layer_name, features in self.layers.items():
            for feature in features:
                for primitive in feature["primitives"]:
                    if primitive["type"] == "circle":
                        cx, cy = primitive["center"]
                        radius = primitive["radius"]
                        circle = Point(cx, cy).buffer(radius).boundary
                        if line.intersects(circle):
                            intersect_points = line.intersection(circle)
                            intersections.extend(self._format_intersection_points("Circle", intersect_points))

                    elif primitive["type"] == "rectangle":
                        x, y = primitive["corner"]
                        width, height = primitive["width"], primitive["height"]
                        rect = Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])
                        if line.intersects(rect.boundary):
                            intersect_points = line.intersection(rect.boundary)
                            intersections.extend(self._format_intersection_points("Rectangle", intersect_points))

                    elif primitive["type"] == "polygon":
                        poly_points = primitive["vertices"]
                        polygon = Polygon(poly_points)
                        if line.intersects(polygon.boundary):
                            intersect_points = line.intersection(polygon.boundary)
                            intersections.extend(self._format_intersection_points("Polygon", intersect_points))

        print(f"Intersections found: {intersections}")
        return intersections

    def _format_intersection_points(self, feature_type, intersect_points):
        points = []
        if intersect_points.geom_type == 'MultiPoint':
            points = [(feature_type, (point.x, point.y)) for point in intersect_points.geoms]
        elif intersect_points.geom_type == 'Point':
            points.append((feature_type, (intersect_points.x, intersect_points.y)))
        return points

    def is_point_in_geometric_object(self, point: tuple, geometric_object_id: str) -> bool:
        for layer_features in self.layers.values():
            for feature in layer_features:
                if feature["id"] == geometric_object_id:
                    for primitive in feature["primitives"]:
                        if self._is_point_in_primitive(point, primitive):
                            return True
        return False

    def get_geometric_features_for_point(self, point: tuple) -> list:
        features_containing_point = []
        for layer_features in self.layers.values():
            for feature in layer_features:
                for primitive in feature["primitives"]:
                    if self._is_point_in_primitive(point, primitive):
                        features_containing_point.append(feature["id"])
                        break
        return features_containing_point

    def _is_point_in_primitive(self, point: tuple, primitive: dict) -> bool:
        p = Point(point)
        if primitive["type"] == "circle":
            cx, cy = primitive["center"]
            radius = primitive["radius"]
            return p.distance(Point(cx, cy)) <= radius
        elif primitive["type"] == "rectangle":
            x, y = primitive["corner"]
            width, height = primitive["width"], primitive["height"]
            rect = Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])
            return rect.contains(p)
        elif primitive["type"] == "polygon":
            poly_points = primitive["vertices"]
            polygon = Polygon(poly_points)
            return polygon.contains(p)
        return False


class RobotariumVisualization:
    def __init__(self, number_of_robots):
        self.robotarium = robotarium.Robotarium(number_of_robots=number_of_robots, show_figure=True, sim_in_real_time=True)
        self.ax = self.robotarium.axes

    def display_layers(self, layer_names):
        # for i, name in enumerate(layer_names):
        #     self.ax.text(-1.5, 1.2 - i * 0.1, f"Layer {i+1}: {name}", fontsize=10, color='black')
        self.robotarium.get_poses()  # Ensure poses are obtained before calling step()
        self.robotarium.step()

    def display_feature(self, layer_name, feature):
        color_map = {"Landmarks": "green", "RestrictedZones": "red"}
        feature_color = color_map.get(layer_name, "blue")
        
        for primitive in feature["primitives"]:
            if primitive["type"] == "circle":
                cx, cy = primitive["center"]
                radius = primitive["radius"]
                circle = Circle((cx, cy), radius, fill=True, color=feature_color, alpha=0.2, edgecolor="black", linewidth=1.5)
                self.ax.add_patch(circle)
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
        self.robotarium.get_poses()  # Ensure poses are obtained before calling step()
        self.robotarium.step()

    def draw_line_segment(self, point_a, point_b):
        """Draw a line segment from point A to point B in the visualization."""
        x_values = [point_a[0], point_b[0]]
        y_values = [point_a[1], point_b[1]]
        self.ax.plot(x_values, y_values, color="blue", linestyle="--", linewidth=1)
        self.robotarium.get_poses()  # Ensure poses are obtained before calling step()
        self.robotarium.step()

    def display_point(self, point, color="orange", size=50):
        """Displays a point on the visualization."""
        self.ax.plot(point[0], point[1], 'o', color=color, markersize=size)
        self.robotarium.get_poses()  # Ensure poses are obtained before calling step()
        self.robotarium.step()


# Example usage
visualizer = RobotariumVisualization(number_of_robots=5)
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

# Check for intersections
intersections = world.get_intersections_with_geometric_features((0, 0), (1, 1))
print("Intersection points:", intersections)

# Draw the line segment
visualizer.draw_line_segment((0, 0), (1, 1))

# Display a specific point on the plot
point_to_check = (0.2, 0.2)
visualizer.display_point(point_to_check, color="purple", size=10)

# Check if point is in a specific geometric object
is_in_restricted_zone = world.is_point_in_geometric_object(point_to_check, "restricted_zone_1")
print(f"Point {point_to_check} inside 'restricted_zone_1':", is_in_restricted_zone)

# Get all features containing the point
features_containing_point = world.get_geometric_features_for_point(point_to_check)
print(f"Geometric features containing point {point_to_check}:", features_containing_point)

# Run Robotarium visualization loop
for _ in range(500):
    visualizer.robotarium.get_poses()  # Call get_poses() before each step
    visualizer.robotarium.step()

visualizer.robotarium.call_at_scripts_end()
