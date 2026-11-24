"""
Week 0: Scoping the research question

Objective: study the effect of power reliability on the performance of
healthcare facilities using large-scale satellite data, by combining
electricity reliability estimates (HREA) with facility performance data
(DHS Service Provision Assessments).

This first sketch loads the facility location dataset and plots it over a
base map of Africa to confirm the data is usable.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FACILITIES_FILE = DATA_DIR / "sub-saharan_health_facilities.xlsx"
SHAPEFILE = DATA_DIR / "ne_110m_admin_0_countries" / "ne_110m_admin_0_countries.shp"

# load facility locations
df = pd.read_excel(FACILITIES_FILE, sheet_name="Subsaharan_health_facilities")
print(df.head())

# convert to a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Long"], df["Lat"]),
                       crs="EPSG:4326")

# base map of Africa
world = gpd.read_file(SHAPEFILE)
africa = world[world["CONTINENT"] == "Africa"]

fig, ax = plt.subplots(figsize=(10, 10))
africa.plot(ax=ax, color="lightgrey", edgecolor="black")
gdf.plot(ax=ax, color="red", markersize=10, alpha=0.6, label="Healthcare Facility")

ax.set_title("Healthcare Facilities in Sub-Saharan Africa", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.legend()
plt.show()
