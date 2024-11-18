import os
import math
import requests
from geopy.geocoders import Nominatim

class MapDownloader:
    def __init__(self, area_name=None, center_lat=None, center_lon=None, radius_meters=500, zoom=15):
        self.area_name = area_name
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.radius_meters = radius_meters
        self.zoom = zoom
        print(f"[INFO] MapDownloader initialized with area_name={self.area_name}, center_lat={self.center_lat}, center_lon={self.center_lon}, radius_meters={self.radius_meters}, zoom={self.zoom}")

    def get_coordinates(self):
        """Fetches coordinates for the specified area name."""
        print(f"[INFO] Fetching coordinates for area: {self.area_name}")
        geolocator = Nominatim(user_agent="map_downloader")
        location = geolocator.geocode(self.area_name)
        if location:
            print(f"[SUCCESS] Found coordinates: Latitude {location.latitude}, Longitude {location.longitude}")
            return location.latitude, location.longitude
        else:
            print("[ERROR] Could not find location.")
            return None, None

    def latlon_to_tile(self, lat, lon, zoom):
        """Converts latitude/longitude to tile coordinates at the specified zoom level."""
        print(f"[INFO] Converting coordinates (Lat: {lat}, Lon: {lon}) to tile coordinates at zoom level {zoom}")
        tile_x = int((lon + 180) / 360 * (2**zoom))
        tile_y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (2**zoom))
        print(f"[SUCCESS] Converted to tile coordinates: X {tile_x}, Y {tile_y}")
        return tile_x, tile_y

    def download_tile(self, x, y, zoom, area_directory):
        """Downloads a single tile at the specified x, y, and zoom level."""
        url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
        headers = {"User-Agent": "MapTileDownloader/1.0 (+https://ru-novel.ru)"}
        print(f"[INFO] Downloading tile from URL: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            path = f"Images/{area_directory}/tile_{zoom}_{x}_{y}.png"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as file:
                file.write(response.content)
            print(f"[SUCCESS] Downloaded and saved tile {zoom}/{x}/{y} to {path}")
        else:
            print(f"[ERROR] Failed to download tile {zoom}/{x}/{y} (HTTP Status: {response.status_code})")

    def download_tiles(self, area_name=None, center_lat=None, center_lon=None, radius_meters=500, zoom=None):
        zoom = zoom if zoom is not None else self.zoom  # Use the passed zoom or the default value
        area_name = area_name if area_name else self.area_name
        center_lat = center_lat if center_lat else self.center_lat
        center_lon = center_lon if center_lon else self.center_lon
        radius_meters = radius_meters if radius_meters else self.radius_meters

        """Downloads all tiles within the specified radius for the current zoom level."""
        print(f"[INFO] Downloading tiles for zoom level {self.zoom}")
        
        # Step 1: Determine Center Coordinates
        if self.center_lat is None or self.center_lon is None:
            self.center_lat, self.center_lon = self.get_coordinates()
            if self.center_lat is None or self.center_lon is None:
                print("[ERROR] Coordinates could not be determined. Exiting download.")
                return
        
        # Step 2: Set Directory and Get Center Tile Coordinates
        tile_x, tile_y = self.latlon_to_tile(self.center_lat, self.center_lon, self.zoom)
        area_directory = self.area_name if self.area_name else f"Coordinates_{self.center_lat}_{self.center_lon}"

        # Step 3: Calculate Number of Tiles to Cover Radius
        meters_per_tile = 40075016.686 / (2**self.zoom)
        tiles_needed = int(self.radius_meters / meters_per_tile)
        print(f"[INFO] Radius covers approximately {tiles_needed * 2 + 1} tiles in each direction from center tile.")

        # Step 4: Download All Tiles in Range
        for x in range(tile_x - tiles_needed, tile_x + tiles_needed + 1):
            for y in range(tile_y - tiles_needed, tile_y + tiles_needed + 1):
                print(f"[INFO] Downloading tile at position X: {x}, Y: {y}")
                self.download_tile(x, y, self.zoom, area_directory)

        print(f"[SUCCESS] Finished downloading tiles for area '{area_directory}'.")

# Example usage
# if __name__ == "__main__":
#     downloader = MapDownloader(area_name="Home", center_lat=31.397010972295938, center_lon=74.28682653254526, radius_meters=500, zoom=16)
#     downloader.download_tiles()