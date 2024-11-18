from map import MapDownloader
from stich_map import MapStitcher

# Define parameters for map downloading and stitching
area_name = "Home"
center_lat = 31.397010972295938
center_lon = 74.28682653254526
radius_meters = 500
start_zoom = 15
end_zoom = 19

# Initialize the MapDownloader with the defined parameters

# Initialize the MapStitcher for the specified area
stitcher = MapStitcher(area_name=area_name)

# Loop through the range of zoom levels and process each level
for zoom in range(start_zoom, end_zoom + 1):
    print(f"[INFO] Processing zoom level {zoom}")
    downloader = MapDownloader(area_name=area_name, center_lat=center_lat, center_lon=center_lon, radius_meters=radius_meters,zoom=zoom)
    # Download tiles for the current zoom level
    downloader.download_tiles()
    # Stitch tiles for the current zoom level
    stitcher.stitch_tiles(zoom=zoom)

print("[SUCCESS] All zoom levels downloaded and stitched.")
