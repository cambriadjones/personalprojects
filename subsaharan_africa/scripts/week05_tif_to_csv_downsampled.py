"""
Week 5: Making the raster-to-table pipeline scale

Revises Week 4 so the output is small enough to analyze on a laptop:
  - resamples each raster to 25% resolution (average resampling)
  - adjusts the affine transform to match the new pixel size
  - masks the file's declared nodata value
  - writes CSVs to a dedicated output folder

Week 8 checks how much this downsampling changes the data's distribution.
"""

import os
from pathlib import Path

import pandas as pd
import rasterio
from rasterio.enums import Resampling

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TIF_DIR = DATA_DIR / "tif_files"
OUTPUT_DIR = DATA_DIR / "csv_outputs"

MAX_ROWS = 1_000_000  # rows per output CSV
SCALE_FACTOR = 0.25   # 25% resolution = fewer rows


def convert_tiff_csv(file_path):
    """Downsample one GeoTIFF and write its valid pixels to CSV."""
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    with rasterio.open(file_path) as dataset:
        new_height = int(dataset.height * SCALE_FACTOR)
        new_width = int(dataset.width * SCALE_FACTOR)

        data = dataset.read(1, out_shape=(1, new_height, new_width),
                            resampling=Resampling.average)

        # rescale the transform so pixel -> coordinate mapping stays correct
        new_transform = dataset.transform * dataset.transform.scale(
            dataset.width / new_width,
            dataset.height / new_height,
        )

        data_list = []
        for row in range(new_height):
            for col in range(new_width):
                value = data[row, col]
                if not pd.isnull(value) and value != dataset.nodata:
                    lon, lat = new_transform * (col, row)
                    data_list.append((lat, lon, value))

    df = pd.DataFrame(data_list, columns=["lat", "lon", "value"])

    # split into multiple files if exceeding MAX_ROWS
    for file_number, start in enumerate(range(0, len(df), MAX_ROWS)):
        suffix = f"({file_number})" if file_number > 0 else ""
        out_path = OUTPUT_DIR / f"{base_name}{suffix}.csv"
        df.iloc[start:start + MAX_ROWS].to_csv(out_path, index=False)
        print(f"Saved: {out_path}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for tif in sorted(TIF_DIR.glob("*.tif")):
        convert_tiff_csv(tif)
