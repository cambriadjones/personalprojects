"""
Ocean Sea Level and Atmospheric CO2

Question: is there a proportionality between sea level and atmospheric CO2?

Hypothesis: the recent rise in atmospheric CO2, driven by fossil fuel use
since the Industrial Revolution, is proportional to the rise in sea level.

Steps
  1. Plot sea level vs. year and CO2 concentration vs. year.
  2. Fit a quadratic (degree 2) model to each series and plot the residuals.
  3. For 1983-1993, 1993-2003 and 2003-2013, estimate the average rate of
     change with linear regression and with LOWESS smoothing
     (frac = 0.2, 0.5, 0.8).
  4. Project CO2 and sea level to 2050, 2100 and 2200 from the linear trend.
  5. Compare the relative growth of the two series.

Data (see data/README.md)
  - epa-sea-level.csv: EPA yearly sea level, 1880-2014. "CSIRO Adjusted Sea
    Level" is in INCHES relative to the 1880 baseline.
  - monthly_in_situ_co2_mlo2.csv: Scripps monthly CO2 (ppm) at Mauna Loa,
    1958-2021. -99.99 marks missing months.

Run:  python scripts/sea_level_co2_analysis.py
Figures are written to figures/ and a results summary is printed.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"
INTERVAL_DIR = FIG_DIR / "intervals"

SEA_LEVEL_FILE = DATA_DIR / "epa-sea-level.csv"
CO2_FILE = DATA_DIR / "monthly_in_situ_co2_mlo2.csv"

SL_COL = "CSIRO Adjusted Sea Level"  # inches above the 1880 baseline
IN_TO_MM = 25.4

INTERVALS = [(2003, 2013), (1993, 2003), (1983, 1993)]
LOWESS_FRACS = (0.2, 0.5, 0.8)
PROJECTION_YEARS = (2020, 2050, 2100, 2200)

lowess = sm.nonparametric.lowess


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def save(path):
    """Save the current figure and close it."""
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()


def fitrms(data, model):
    """Root-mean-square of the residuals (data - model)."""
    resid = np.asarray(data) - np.asarray(model)
    return float(np.sqrt(np.mean(resid ** 2)))


def lowess_rate(smoothed):
    """Rate of change between consecutive points of a LOWESS curve."""
    x, y = smoothed[:, 0], smoothed[:, 1]
    return x[:-1], np.diff(y) / np.diff(x)


def load_data():
    sea = pd.read_csv(SEA_LEVEL_FILE).dropna(subset=[SL_COL])

    co2 = pd.read_csv(CO2_FILE)
    co2 = co2[co2["CO2_ppm"] != -99.99].reset_index(drop=True)
    co2["Year"] = co2["Date"].astype(int)
    return sea, co2


# ---------------------------------------------------------------------------
# (1) raw series
# ---------------------------------------------------------------------------
def plot_raw_series(sea, co2):
    plt.scatter(sea["Year"], sea[SL_COL], label="Sea level rise as a function of year")
    plt.xlim(1960, 2014)
    plt.ylim(0, 12)
    plt.xlabel("Year")
    plt.ylabel("Sea level change (in, vs. 1880)")
    plt.legend()
    save(FIG_DIR / "01_sea_level_by_year.png")

    plt.scatter(co2["Date"], co2["CO2_ppm"], color="red", alpha=0.1,
                label="CO2 concentration as a function of year")
    plt.xlim(1960, 2014)
    plt.xlabel("Year")
    plt.ylabel("CO2 concentration (ppm)")
    plt.legend()
    save(FIG_DIR / "02_co2_by_year.png")


# ---------------------------------------------------------------------------
# (2) quadratic fits
# ---------------------------------------------------------------------------
def quadratic_fit(x, y, fit_mask, ylabel, color, alpha, out_name):
    """Fit y = a*x^2 + b*x + c on fit_mask, plot data, fit and residuals."""
    coeffs = np.polyfit(x[fit_mask], y[fit_mask], 2)
    model = np.polyval(coeffs, x)
    rms = fitrms(y[fit_mask], model[fit_mask])

    plt.figure(figsize=(6.4, 6))
    plt.subplot(2, 1, 1)
    plt.scatter(x, y, color=color, alpha=alpha)
    plt.plot(x, model, color="black")
    plt.xlim(1960, 2013)
    plt.title("Data and a polynomial degree 2 fit")
    plt.xlabel("Year")
    plt.ylabel(ylabel)

    plt.subplot(2, 1, 2)
    plt.scatter(x, y - model, color=color, alpha=min(alpha * 3, 1))
    plt.xlim(1960, 2013)
    plt.title("Residuals of a polynomial degree 2 fit")
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    save(FIG_DIR / out_name)
    return coeffs, rms


# ---------------------------------------------------------------------------
# (3) interval rates of change
# ---------------------------------------------------------------------------
def analyze_interval(x, y, resid_x, start, end, *, name, ylabel, rate_unit, color):
    """Linear and LOWESS rate of change of y over [start, end]."""
    mask = (x >= start) & (x <= end)
    xi, yi, rxi = x[mask].to_numpy(), y[mask].to_numpy(), resid_x[mask].to_numpy()
    prefix = INTERVAL_DIR / f"{name}_{start}_{end}"
    results = {}

    # linear regression: slope = average rate of change
    slope = np.polyfit(xi, yi, 1)
    plt.plot(xi, yi, ".", color=color)
    plt.plot(xi, np.polyval(slope, xi), "-", color="black")
    plt.title(f"Linear fit {start}–{end}")
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    save(f"{prefix}_linear.png")
    results["linear"] = slope[0]

    # LOWESS smoothing at three bandwidths, then rate of change of the curve
    residuals = {}
    for frac in LOWESS_FRACS:
        smoothed = lowess(yi, xi, frac=frac)
        rate_x, rate = lowess_rate(smoothed)

        plt.plot(rate_x, rate, label=f"LOWESS (frac={frac})")
        plt.xlabel("Year")
        plt.ylabel(f"Rate of change ({rate_unit})")
        plt.legend()
        save(f"{prefix}_lowess_{int(frac * 10):02d}.png")

        results[f"lowess_{frac}"] = rate.mean()
        residuals[frac] = yi - smoothed[:, 1]

    for frac, resid in residuals.items():
        plt.plot(rxi, resid, ".", label=f"frac={frac}")
    plt.axhline(0.0, color="red")
    plt.title("Residuals")
    plt.legend()
    save(f"{prefix}_residuals.png")

    return results


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    INTERVAL_DIR.mkdir(parents=True, exist_ok=True)
    sea, co2 = load_data()

    # (1)
    plot_raw_series(sea, co2)

    # (2)
    sl_mask = (sea["Year"] >= 1960) & (sea["Year"] <= 2013)
    _, sl_rms = quadratic_fit(sea["Year"], sea[SL_COL], sl_mask,
                              "Sea level change (in)", "tab:blue", 1.0,
                              "03_sea_level_quadratic_fit.png")
    _, co2_rms = quadratic_fit(co2["Date"], co2["CO2_ppm"],
                               np.ones(len(co2), dtype=bool),
                               "CO2 concentration (ppm)", "red", 0.1,
                               "04_co2_quadratic_fit.png")
    print("Quadratic fit RMS")
    print(f"  sea level (1960-2013): {sl_rms:.3f} in")
    print(f"  CO2 (1958-2021):       {co2_rms:.3f} ppm\n")

    # (3)
    print("Average rate of change by interval")
    for start, end in INTERVALS:
        sl = analyze_interval(sea["Year"], sea[SL_COL], sea["Year"], start, end,
                              name="sea_level", ylabel="Sea level change (in)",
                              rate_unit="in/year", color="tab:blue")
        c = analyze_interval(co2["Date"], co2["CO2_ppm"], co2["Year"], start, end,
                             name="co2", ylabel="CO2 concentration (ppm)",
                             rate_unit="ppm/year", color="red")
        lw_sl = ", ".join(f"{sl[f'lowess_{f}']:.4f}" for f in LOWESS_FRACS)
        lw_c = ", ".join(f"{c[f'lowess_{f}']:.4f}" for f in LOWESS_FRACS)
        print(f"  {start}-{end}")
        print(f"    sea level: linear {sl['linear']:.2f} in/yr "
              f"(~{sl['linear'] * IN_TO_MM:.1f} mm/yr) | LOWESS {lw_sl}")
        print(f"    CO2:       linear {c['linear']:.2f} ppm/yr | LOWESS {lw_c}")
    print()

    # (4) linear-trend projections
    co2_trend = np.polyfit(co2["Date"], co2["CO2_ppm"], 1)
    sl_trend = np.polyfit(sea.loc[sl_mask, "Year"], sea.loc[sl_mask, SL_COL], 1)
    co2_proj = {yr: np.polyval(co2_trend, yr) for yr in PROJECTION_YEARS}
    sl_proj = {yr: np.polyval(sl_trend, yr) for yr in PROJECTION_YEARS}

    print("Linear-trend projections")
    for yr in PROJECTION_YEARS:
        print(f"  {yr}: CO2 {co2_proj[yr]:.2f} ppm | sea level {sl_proj[yr]:.2f} in "
              f"(~{sl_proj[yr] * IN_TO_MM:.0f} mm) above 1880")
    print()

    # (5) relative growth: a lower ratio means faster relative growth
    print("Relative growth (earlier / later value)")
    for a, b in [(2020, 2050), (2100, 2200)]:
        print(f"  {a}->{b}: sea level {sl_proj[a] / sl_proj[b]:.2f} | "
              f"CO2 {co2_proj[a] / co2_proj[b]:.2f}")


if __name__ == "__main__":
    main()
