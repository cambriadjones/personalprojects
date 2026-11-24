# Data

## Included sample

`sample/prplit/prplit <year>/GHA_set_prplit_<year>.csv` holds a 5% random sample of Ghana's cleaned prplit data for 2013–2020: 29,209 of 584,175 settlement pixels per year, using the same pixels every year (seed 42). It's about 10 MB in total and is enough to run Week 7 with no downloads.

To rebuild it, put the full Ghana CSVs in a folder and run:

```bash
python scripts/make_sample.py ~/Downloads
```

Check against the full data: a two-sample Kolmogorov–Smirnov test gives D ≈ 0.005 and p > 0.3 for every year, and means agree to within 0.003. In KDE plots the sample's peak at 1.0 looks lower only because a smaller sample gets a wider default bandwidth.

## Full data

The full raw and processed data isn't committed: cleaned CSVs are about 27 MB per country-year, tens of GB in total. To reproduce the full analysis:

### 1. HREA electricity access & reliability (GeoTIFF)

- Source: https://hrea.isr.umich.edu/data.html
- [`hrea_catalog.json`](hrea_catalog.json) is the STAC catalog for the dataset and lists every country folder.
- Bulk download through the AWS CLI (the bucket can only be downloaded from the terminal), for example Ghana:

```bash
aws s3 cp s3://globalnightlight/HREAv1.1_COGs/GHA/ ./tif_files/ --recursive --no-sign-request
```

Variables used:
- `set_lightscore_<year>`: nighttime brightness score per settlement
- `set_prplit_<year>`: proportion of nights a settlement is statistically brighter than matched uninhabited areas (reliability)

### 2. Health facility locations

- File: `sub-saharan_health_facilities.xlsx` (columns include `Country`, `Lat`, `Long`)

### 3. Country boundaries

- Natural Earth Admin 0 Countries: https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/

### Expected local layout

All scripts read from this `data/` folder, so no paths need editing. Place files here:

```
data/
├── sub-saharan_health_facilities.xlsx
├── tif_files/                  # raw HREA GeoTIFFs
├── csv_full_resolution/        # produced by week04_tif_to_csv.py
├── csv_outputs/                # produced by week05_tif_to_csv_downsampled.py
├── prplit/prplit 2013/ …       # week05 prplit CSVs grouped by year, for week07
└── ne_110m_admin_0_countries/  # Natural Earth shapefile
```

Everything except this README and `hrea_catalog.json` is ignored by git.
