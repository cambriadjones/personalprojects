"""
Week 8: Validating the downsampling

Compares the prplit distribution from the original full-resolution Ghana
GeoTIFF with the distribution from the 25%-resolution CSV made in Week 5.

Result: the overall shape holds, but averaging pixels pulls values off the
1.0 peak and into the low-reliability tail.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import seaborn as sns

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TIF_FILE = DATA_DIR / "tif_files" / "GHA_set_prplit_2013.tif"
CSV_FILE = DATA_DIR / "csv_outputs" / "GHA_set_prplit_2013.csv"

# ---------------- full-resolution GeoTIFF ----------------
with rasterio.open(TIF_FILE) as dataset:
    tif_data = dataset.read(1).flatten()

# vectorized filtering: drop NaN, keep valid proportions in [0, 1]
tif_data = tif_data[~np.isnan(tif_data)]
tif_data = tif_data[(tif_data >= 0) & (tif_data <= 1)]

# ---------------- downsampled CSV ----------------
csv_data = pd.read_csv(CSV_FILE)["value"].dropna()
csv_data = csv_data[csv_data.between(0, 1)]

# ---------------- plot ----------------
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))

sns.kdeplot(tif_data, ax=ax, label="tif (full resolution)", color="orangered",
            bw_adjust=0.5, linewidth=2)
sns.kdeplot(csv_data, ax=ax, label="csv (25% resolution)", color="goldenrod",
            bw_adjust=0.5, linewidth=2)

ax.set_title("Ghana prplit KDE: .tif vs .csv", fontsize=14)
ax.set_xlabel("prplit")
ax.set_ylabel("Density")
ax.legend(title="File type")
plt.tight_layout()
plt.show()
