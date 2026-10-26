"""Run 1 quick look: the 1.5 m air temperature of KCL Default.

Run from anywhere:   python "$DATA_DIR/scripts/quicklook.py"
Reads  ~/kcl_default/output/kcl_default.hourly_output.nc
Writes ~/kcl_default/run1_t1p5m.png
(An optional argument replaces ~ as the folder that holds kcl_default.)
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

root = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~")
run = os.path.join(root, "kcl_default")

ds = xr.open_dataset(f"{run}/output/kcl_default.hourly_output.nc")
print(ds)                                      # variables, sizes, units
print("time values:", ds.sizes["time"])

t = ds["t1p5m_gb"].squeeze() - 273.15          # K -> degC; squeeze drops the 1 x 1 grid
# each value is the mean of the hour ENDING at its time stamp: use the middle of the hour for daily means
mid = t.assign_coords(time=t["time"] - np.timedelta64(30, "m"))
daily = mid.resample(time="1D").mean()

plt.rcParams.update({"font.size": 18})
fig, ax = plt.subplots(figsize=(10, 4.6), layout="constrained")
ax.plot(t["time"], t, color="#5E6670", lw=0.4, alpha=0.5, label="Every hour")
ax.plot(daily["time"] + np.timedelta64(12, "h"), daily, color="#16302B", lw=2.0, label="Daily mean")
ax.set_ylabel("T$_{1.5\\,m}$ gridbox (°C)")
ax.set_xlim(np.datetime64("2012-04-01"), np.datetime64("2014-01-01"))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
lo, hi = float(t.min()), float(t.max())
ax.set_ylim(lo - 1, hi + 0.18 * (hi - lo))
ax.grid(axis="y", color="#D9E0DC", lw=0.8)
ax.set_axisbelow(True)
ax.legend(loc="upper left", frameon=False, ncol=2)
fig.savefig(f"{run}/run1_t1p5m.png", dpi=200)
print("saved", f"{run}/run1_t1p5m.png")
