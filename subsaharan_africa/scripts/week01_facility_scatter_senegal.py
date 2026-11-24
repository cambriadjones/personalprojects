"""
Week 1: Mapping healthcare facilities (Senegal test case)

Loads the Sub-Saharan health facility dataset, filters it to Senegal, and
plots facilities by latitude/longitude with Dakar as a reference point.
Then plots every facility in the dataset to check coordinate coverage.

Observations: facilities are concentrated in West Africa and along
coastlines, and sparse across the Sahara and Namibia.
"""

from pathlib import Path

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
lat0, lat1 = 12.0, 17.0
lon0, lon1 = -17.5, -11.0

plt.figure(figsize=(10, 10))
plt.scatter(df_senegal["Long"], df_senegal["Lat"], s=10, c="red", alpha=0.6,
            marker="o", label="Healthcare Facilities")
plt.scatter(DAKAR_LON, DAKAR_LAT, color="limegreen", s=100, label="Dakar")

plt.xlim(lon0, lon1)
plt.ylim(lat0, lat1)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Healthcare Facilities in Senegal")
plt.legend()
plt.grid(True)
plt.show()

# ---------------------------------------------------------------
# Healthcare facilities across the full dataset
# ---------------------------------------------------------------
plt.figure(figsize=(15, 10))
plt.scatter(df["Long"], df["Lat"], s=5, c="blue", alpha=0.5, marker="o",
            label="Healthcare Facilities")

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Distribution of Healthcare Facilities in Sub-Saharan Africa")
plt.legend()
plt.grid(True)
plt.show()
