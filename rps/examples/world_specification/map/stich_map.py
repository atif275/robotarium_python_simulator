# stitch_map.py
import os
from PIL import Image

class MapStitcher:
    def __init__(self, area_name):
        self.area_name = area_name
        print(f"[INFO] MapStitcher initialized for area: {area_name}")

    def get_tile_paths(self, zoom):
        """Gets file paths for tiles at a specified zoom level in sequence."""
        print(f"[INFO] Gathering tile paths for zoom level {zoom}")
        tile_dir = f"Images/{self.area_name}/"
        tile_files = [f for f in os.listdir(tile_dir) if f.startswith(f"tile_{zoom}_")]
        tiles = []
        for tile_file in tile_files:
            try:
                _, _, x, y = tile_file.split('_')
                x, y = int(x), int(y.split('.')[0])
                tiles.append((x, y, os.path.join(tile_dir, tile_file)))
                print(f"[DEBUG] Found tile at ({x}, {y}) - Path: {tile_file}")
            except ValueError:
                print(f"[WARNING] Skipping unrecognized file format: {tile_file}")
        sorted_tiles = sorted(tiles, key=lambda t: (t[1], t[0]))
        print(f"[INFO] Total tiles found for stitching: {len(sorted_tiles)}")
        return sorted_tiles

    def stitch_tiles(self, zoom):
        """Stitches all tiles at a specified zoom level into a single image."""
        print(f"[INFO] Stitching tiles for zoom level {zoom}")
        tiles = self.get_tile_paths(zoom)
        if not tiles:
            print(f"[ERROR] No tiles found for zoom level {zoom}.")
            return

        # Determine map dimensions
        min_x = min(t[0] for t in tiles)
        min_y = min(t[1] for t in tiles)
        max_x = max(t[0] for t in tiles)
        max_y = max(t[1] for t in tiles)
        
        num_tiles_x = max_x - min_x + 1
        num_tiles_y = max_y - min_y + 1
        print(f"[INFO] Map dimensions in tiles: {num_tiles_x} x {num_tiles_y}")

        # Get tile size and create a blank canvas
        tile_width, tile_height = Image.open(tiles[0][2]).size
        print(f"[INFO] Tile dimensions (width x height): {tile_width} x {tile_height}")
        full_map = Image.new('RGB', (tile_width * num_tiles_x, tile_height * num_tiles_y))

        # Place each tile in the correct position
        for x, y, tile_path in tiles:
            tile_image = Image.open(tile_path)
            x_offset = (x - min_x) * tile_width
            y_offset = (y - min_y) * tile_height
            full_map.paste(tile_image, (x_offset, y_offset))
            print(f"[DEBUG] Pasted tile {zoom}/{x}/{y} at position ({x_offset}, {y_offset})")

        # Save the stitched map
        output_path = f"Images/{self.area_name}/stitched_map_{zoom}.png"
        full_map.save(output_path)
        print(f"[SUCCESS] Stitched map saved as {output_path}")

# Example usage
# if __name__ == "__main__":
#     # Define the area name and the zoom level you want to stitch
#     area_name = "Home"
#     zoom_level = 16

#     # Initialize the MapStitcher with the area name
#     stitcher = MapStitcher(area_name=area_name)

#     # Run the stitch_tiles method for the specified zoom level
#     stitcher.stitch_tiles(zoom=zoom_level)