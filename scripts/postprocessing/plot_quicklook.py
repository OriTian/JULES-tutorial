"""
Quick single-variable timeseries plot from a JULES output file -- sanity
check that a run produced sensible-looking output before deeper analysis.

Usage:
  python plot_quicklook.py output/my_run.hourly_output.nc --var t1p5m_gb --out quicklook.png
"""
import argparse

import matplotlib

matplotlib.use("Agg")  # no display on a headless machine (e.g. EC2)
import matplotlib.pyplot as plt
import netCDF4 as nc
import pandas as pd

KELVIN_VARS = {"t1p5m_gb", "tstar_gb", "t1p5m", "tstar"}


def plot_quicklook(nc_path, var, out_path):
    ds = nc.Dataset(nc_path)
    t = pd.to_datetime(
        nc.num2date(
            ds.variables["time"][:],
            ds.variables["time"].units,
            only_use_cftime_datetimes=False,
        )
    )
    values = ds.variables[var][:, 0, 0]
    ylabel = var
    if var in KELVIN_VARS:
        values = values - 273.15
        ylabel = f"{var} (\N{DEGREE SIGN}C)"

    plt.figure(figsize=(10, 4))
    plt.plot(t, values)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("nc_path", help="JULES output NetCDF file")
    p.add_argument("--var", default="t1p5m_gb", help="Variable to plot (default: t1p5m_gb)")
    p.add_argument("--out", default="quicklook.png", help="Output PNG path")
    args = p.parse_args()
    plot_quicklook(args.nc_path, args.var, args.out)
