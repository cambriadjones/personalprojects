"""
Build the small, committed sample dataset in data/sample/.

The full cleaned HREA CSVs are about 27 MB per country-year (tens of GB in
total), far too large for GitHub. This script takes Ghana's prplit CSVs for
2013-2020 and keeps a reproducible 5% random sample of rows from each, so the
analysis scripts can run straight after cloning.

Usage:
    python scripts/make_sample.py [folder containing GHA_set_prplit_<year>.csv]

The folder defaults to ~/Downloads.
"""

import sys
from pathlib import Path

import pandas as pd

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "data" / "sample" / "prplit"
YEARS = range(2013, 2021)
FRACTION = 0.05
SEED = 42


def main(source_dir):
    for year in YEARS:
        src = source_dir / f"GHA_set_prplit_{year}.csv"
        if not src.exists():
            print(f"Missing: {src}")
            continue

        df = pd.read_csv(src)
        if list(df.columns) != ["lat", "lon", "value"]:
            raise ValueError(f"{src.name}: unexpected columns {list(df.columns)}")

        sample = df.sample(frac=FRACTION, random_state=SEED).sort_index()

        out_dir = SAMPLE_DIR / f"prplit {year}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / src.name
        sample.to_csv(out, index=False)
        print(f"{src.name}: {len(df):,} rows -> {len(sample):,} rows "
              f"({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    folder = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "Downloads"
    main(folder)
