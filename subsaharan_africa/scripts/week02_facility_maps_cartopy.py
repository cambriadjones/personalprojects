"""
Week 2: Cartographic facility maps

Rebuilds the Week 1 scatter plots with cartopy so facilities are shown
against country borders and coastlines in a geographic projection.

Observations: facilities are concentrated in West Africa and along
coastlines, with coverage gaps in the Sahel, Namibia and Angola.
"""

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FACILITIES_FILE = DATA_DIR / "sub-saharan_health_facilities.xlsx"

DAKAR_LAT, DAKAR_LON = 14.6928, -17.4467

# load facilities and filter to Senegal
df = pd.read_excel(FACILITIES_FILE)
df_senegal = df[df["Country"].str.strip().str.lower() == "senegal"]

# ---------------------------------------------------------------
# Healthcare facilities in Senegal
# ---------------------------------------------------------------
lat0, lat1 = 11.5, 17.5
lon0, lon1 = -18.5, -10.0

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": ccrs.PlateCarree()})
ax.add_feature(cfeature.BORDERS, edgecolor="black")
ax.add_feature(cfeature.COASTLINE, edgecolor="gray")

ax.scatter(df_senegal["Long"], df_senegal["Lat"], s=10, c="red", alpha=0.6,
           marker="o", label="Healthcare Facilities", transform=ccrs.PlateCarree())
ax.scatter(DAKAR_LON, DAKAR_LAT, color="limegreen", s=100, label="Dakar",
           transform=ccrs.PlateCarree())

ax.set_extent([lon0, lon1, lat0, lat1])
ax.set_title("Healthcare Facilities in Senegal")
ax.legend()
plt.show()

# ---------------------------------------------------------------
# Healthcare facilities across Africa
# ---------------------------------------------------------------
lat0, lat1 = -30, 30
lon0, lon1 = -30, 60

fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={"projection": ccrs.PlateCarree()})
ax.add_feature(cfeature.BORDERS, edgecolor="black")
ax.add_feature(cfeature.COASTLINE, edgecolor="gray")

ax.scatter(df["Long"], df["Lat"], s=5, c="blue", alpha=0.5, marker="o",
           label="Healthcare Facilities", transform=ccrs.PlateCarree())

ax.set_extent([lon0, lon1, lat0, lat1])
ax.set_title("Healthcare Facilities Across Africa")
ax.legend()
plt.show()
