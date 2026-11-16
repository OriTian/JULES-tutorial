"""Compare any two runs of the same site: TEST minus BASE, for one variable (default t1p5m_gb).

Run from anywhere:
    python "$DATA_DIR/scripts/compare_two.py" BASE.nc TEST.nc [VARIABLE]
e.g. the road-albedo exercise:
    python "$DATA_DIR/scripts/compare_two.py" \
        ~/kcl_default/output/kcl_default.hourly_output.nc \
        ~/kcl_albedo/output/kcl_albedo.hourly_output.nc
Writes <TEST run folder>/<test>_minus_<base>.png, e.g. ~/kcl_albedo/kcl_albedo_minus_kcl_default.png
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

if len(sys.argv) < 3:
    sys.exit("usage: python compare_two.py BASE.nc TEST.nc [VARIABLE]")
base_file, test_file = sys.argv[1], sys.argv[2]
var = sys.argv[3] if len(sys.argv) > 3 else "t1p5m_gb"


def run_name(path):                            # output/kcl_albedo.hourly_output.nc -> kcl_albedo
    return os.path.basename(path).split(".")[0]


b, t = xr.open_dataset(base_file), xr.open_dataset(test_file)
for name, ds in ((run_name(base_file), b), (run_name(test_file), t)):
    print(f"{name}: {ds.sizes['time']} time values, {str(ds['time'].values[0])[:16]} to {str(ds['time'].values[-1])[:16]}")
if b.sizes["time"] != t.sizes["time"] or not (b["time"].values == t["time"].values).all():
    sys.exit("the two files have different time stamps: compare runs with the same period and output_period")

xb, xt = b[var].squeeze(), t[var].squeeze()
units = b[var].attrs.get("units", "")
diff = xt - xb                                 # TEST minus BASE, every output time
day = b["sw_down"].squeeze() > 10              # daytime: sunlight above 10 W m-2
label = f"{run_name(test_file)} − {run_name(base_file)}"

# each value is the mean of the hour ENDING at its time stamp: use the middle of the hour
def middle(x):
    return x.assign_coords(time=x["time"] - np.timedelta64(30, "m"))


by_hour = middle(diff).groupby("time.hour").mean()
peak = int(abs(by_hour).argmax())
print(f"{label}, {var}: all hours {float(diff.mean()):+.3f} {units}")
print(f"  daytime {float(diff.where(day).mean()):+.3f}, night-time {float(diff.where(~day).mean()):+.3f} {units}")
print(f"  largest mean difference at {int(by_hour['hour'][peak]):02d}–{int(by_hour['hour'][peak]) + 1:02d} UTC: "
      f"{float(by_hour[peak]):+.3f} {units}")

# a few summer days, to see the daily cycle; the first five days if the run has no July 2013
start = np.datetime64("2013-07-15")
if not (diff["time"].values[0] <= start <= diff["time"].values[-1]):
    start = diff["time"].values[0]
week = slice(start, start + np.timedelta64(5, "D"))
dw, sw = middle(diff).sel(time=week), middle(b["sw_down"].squeeze()).sel(time=week)

plt.rcParams.update({"font.size": 17})
fig = plt.figure(figsize=(11, 5.2), layout="constrained")
grid = fig.add_gridspec(2, 2, width_ratios=[2, 1])
a = fig.add_subplot(grid[0, 0])
s = fig.add_subplot(grid[1, 0], sharex=a)
c = fig.add_subplot(grid[:, 1])

a.plot(dw["time"], dw, color="#A84A12", lw=2.0)
a.axhline(0, color="#55615C", lw=1.0)
a.set_ylabel(f"Δ ({units})")
a.set_title(f"a  {label}, five days", loc="left", fontweight="bold", fontsize=16)
a.tick_params(labelbottom=False)

s.fill_between(sw["time"], sw, color="#E9B949", alpha=0.6, lw=0)
s.plot(sw["time"], sw, color="#8A6A12", lw=1.2)
s.set_ylabel("SW↓ (W m⁻²)")
s.set_title("b  Sunlight, same days", loc="left", fontweight="bold", fontsize=16)
s.xaxis.set_major_locator(mdates.DayLocator())
s.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))

c.bar(by_hour["hour"] + 0.5, by_hour, width=0.8, color="#A84A12")
c.axhline(0, color="#55615C", lw=1.0)
c.set_xlim(0, 24)
c.set_xticks([0, 6, 12, 18, 24])
c.set_xlabel("Hour (UTC)")
c.set_ylabel(f"Δ ({units})")
c.set_title("c  By hour, whole run", loc="left", fontweight="bold", fontsize=16)

for ax in (a, s, c):
    ax.grid(axis="y", color="#D9E0DC", lw=0.8)
    ax.set_axisbelow(True)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(test_file))),
                   f"{run_name(test_file)}_minus_{run_name(base_file)}.png")
fig.savefig(out, dpi=200)
print("saved", out)
