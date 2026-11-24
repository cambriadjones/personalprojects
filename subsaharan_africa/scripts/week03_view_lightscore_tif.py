"""
Week 3: Opening an HREA satellite raster

Opens a single HREA lightscore GeoTIFF (nighttime brightness) for Ghana
and renders it on latitude/longitude axes.

Note: the raster stores nodata cells as roughly -1,000,000. Left unmasked,
these stretch the color scale so far that the image looks almost entirely
dark. Later weeks mask the file's nodata value before analysis.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import rasterio

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TIF_FILE = DATA_DIR / "tif_files" / "GHA_set_lightscore_2013.tif"

with rasterio.open(TIF_FILE) as dataset:
    data = dataset.read(1)
    bounds = dataset.bounds

plt.figure(figsize=(10, 6))
plt.imshow(data, cmap="viridis", origin="upper",
           extent=[bounds.left, bounds.right, bounds.bottom, bounds.top])
plt.colorbar(label="Light Score Intensity")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Ghana Light Score (2013)")
plt.show()
