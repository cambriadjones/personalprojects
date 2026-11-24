"""
Week 7: Distribution of electricity reliability, 2013-2020

prplit = proportion of nights a settlement is statistically brighter than
matched uninhabited areas (a proxy for power reliability).

For each year, combines all country CSVs and plots a kernel density
estimate. The result is bimodal (settlements are mostly dark or mostly lit)
and the high-reliability peak grows over the period.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
# one subfolder per year: "prplit 2013", ...
# Uses the full dataset if present, otherwise the committed Ghana sample.
PRPLIT_DIR = DATA_DIR / "prplit"
if not PRPLIT_DIR.exists():
    PRPLIT_DIR = DATA_DIR / "sample" / "prplit"
    print("Full data not found; using the Ghana 5% sample in data/sample/")

YEARS = list(range(2013, 2021))

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(12, 7))
colors = sns.color_palette("YlOrRd", n_colors=len(YEARS))

for color, year in zip(colors, YEARS):
    csv_files = sorted((PRPLIT_DIR / f"prplit {year}").glob("*.csv"))
    if not csv_files:
        print(f"Skipping {year}: no CSVs found")
        continue

    year_data = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)
    year_data = year_data.dropna(subset=["value"])
    year_data = year_data[year_data["value"].between(0, 1)]

    sns.kdeplot(data=year_data, x="value", ax=ax, label=str(year),
                bw_adjust=0.5, linewidth=2, color=color)

ax.set_title("KDE of prplit 2013–2020", fontsize=14)
ax.set_xlabel("Proportion of Nights Brighter than Uninhabited Areas (prplit)")
ax.set_ylabel("Density")
ax.legend(title="Year")
plt.tight_layout()
plt.show()
