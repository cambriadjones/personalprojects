# Data

The script expects two CSVs in this folder.

### `epa-sea-level.csv`
- Yearly global mean sea level change since 1880, U.S. EPA (CSIRO and NOAA adjusted series)
- Source: https://github.com/datasets/sea-level-rise/tree/master/data (obtained 2023-11-27)
- Columns: `Year`, `CSIRO Adjusted Sea Level`, `Lower Error Bound`, `Upper Error Bound`, `NOAA Adjusted Sea Level`
- Units: **inches**, relative to the 1880 baseline. Complete years 1880–2013; CSIRO is missing for 2014.

### `monthly_in_situ_co2_mlo2.csv`
- Monthly average atmospheric CO₂ (ppm) measured at Mauna Loa Observatory, Hawaii
- Source: Scripps CO₂ Program, https://scrippsco2.ucsd.edu/ (obtained 2022-11-18)
- Columns: `Date` (decimal year, e.g. `1958.2027`), `CO2_ppm`
- `-99.99` marks missing months. Complete years 1959–2021.
