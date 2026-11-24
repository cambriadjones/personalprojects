"""
Week 4: Converting rasters to tables

Loops over every pixel in each GeoTIFF, converts row/column positions to
latitude/longitude with the raster's affine transform, drops null values,
and writes `lat, lon, value` CSVs split into 1-million-row chunks.

Raw data was bulk-downloaded from HREA's AWS S3 bucket (see data/README.md).
At full resolution the output was too large to work with, which led to the
downsampled version in Week 5.
"""

import os
from pathlib import Path

import pandas as pd
import rasterio

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TIF_DIR = DATA_DIR / "tif_files"
OUTPUT_DIR = DATA_DIR / "csv_full_resolution"

MAX_ROWS = 1_000_000  # rows per output CSV


def process_tiff(file_path):
    """Write the non-null pixels of one GeoTIFF to one or more CSVs."""
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    with rasterio.open(file_path) as dataset:
        band = dataset.read(1)
        transform = dataset.transform

        data_list = []
        for row in range(dataset.height):
            for col in range(dataset.width):
                value = band[row, col]
                if value > 0:  # exclude null / nodata values
                    lon, lat = transform * (col, row)
                    data_list.append((lat, lon, value))

    df = pd.DataFrame(data_list, columns=["lat", "lon", "value"])

    # split into multiple files if exceeding MAX_ROWS
    for file_number, start in enumerate(range(0, len(df), MAX_ROWS)):
        suffix = f"({file_number})" if file_number > 0 else ""
        output_file = OUTPUT_DIR / f"{base_name}{suffix}.csv"
        df.iloc[start:start + MAX_ROWS].to_csv(output_file, index=False)
        print(f"Saved: {output_file}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for tif in sorted(TIF_DIR.glob("*.tif")):
        process_tiff(tif)
