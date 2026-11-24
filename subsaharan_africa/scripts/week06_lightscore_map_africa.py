"""
Week 6: Lightscore across Africa

Combines every converted country CSV from Week 5 and plots lightscore as a
color gradient over Natural Earth country borders, giving a continent-wide
view of electricity access on the same frame as the Week 2 facility maps.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CSV_DIR = DATA_DIR / "csv_outputs"  # produced by week05
# Natural Earth Admin 0 Countries:
# https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/
SHAPEFILE = DATA_DIR / "ne_110m_admin_0_countries" / "ne_110m_admin_0_countries.shp"

world = gpd.read_file(SHAPEFILE)
africa = world[world["CONTINENT"] == "Africa"]

# combine all country CSVs into one DataFrame
frames = []
for csv_file in sorted(CSV_DIR.glob("*.csv")):
    df = pd.read_csv(csv_file)
    if {"lat", "lon", "value"}.issubset(df.columns):
        frames.append(df)

if not frames:
    raise FileNotFoundError(f"No lat/lon/value CSVs found in {CSV_DIR}")

combined_df = pd.concat(frames, ignore_index=True)

fig, ax = plt.subplots(figsize=(12, 12))
africa.boundary.plot(ax=ax, linewidth=1, edgecolor="black")

sc = ax.scatter(combined_df["lon"], combined_df["lat"], c=combined_df["value"],
                cmap="viridis_r", s=2, alpha=0.7)
plt.colorbar(sc, ax=ax, label="Lightscore Value")

ax.set_title("Lightscore Gradient Over Africa", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.show()
