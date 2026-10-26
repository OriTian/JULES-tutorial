"""Compare Run 1 (KCL Default) and Run 2 (KCL U-Surf): the 1.5 m air temperature.

Run from anywhere:   python "$DATA_DIR/scripts/compare.py"
Reads  ~/kcl_default/output/kcl_default.hourly_output.nc and ~/kcl_usurf/output/kcl_usurf.hourly_output.nc
Writes ~/kcl_default/compare.png
(An optional argument replaces ~ as the folder that holds both runs.)
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


def open_run(name):
    return xr.open_dataset(f"{root}/{name}/output/{name}.hourly_output.nc")


d, u = open_run("kcl_default"), open_run("kcl_usurf")
td = d["t1p5m_gb"].squeeze() - 273.15          # K -> degC
tu = u["t1p5m_gb"].squeeze() - 273.15
diff = tu - td                                 # U-Surf minus Default, every hour
day = d["sw_down"].squeeze() > 10              # daytime: sunlight above 10 W m-2

print(f"U-Surf - Default, all hours: {float(diff.mean()):+.2f} K")
print(f"  daytime {float(diff.where(day).mean()):+.2f} K, night-time {float(diff.where(~day).mean()):+.2f} K")
print(f"  U-Surf is cooler in {100 * float((diff < 0).mean()):.0f} % of hours")

# each value is the mean of the hour ENDING at its time stamp: use the middle of the hour
def middle(x):
    return x.assign_coords(time=x["time"] - np.timedelta64(30, "m"))


dd, du = middle(td).resample(time="1D").mean(), middle(tu).resample(time="1D").mean()
ddiff = middle(diff).resample(time="1D").mean()
by_hour = middle(diff).groupby("time.hour").mean()
noon = np.timedelta64(12, "h")

plt.rcParams.update({"font.size": 17})
fig = plt.figure(figsize=(11, 5.2), layout="constrained")
grid = fig.add_gridspec(2, 2, width_ratios=[2, 1])
a = fig.add_subplot(grid[0, 0])
b = fig.add_subplot(grid[1, 0], sharex=a)
c = fig.add_subplot(grid[:, 1])

a.plot(dd["time"] + noon, dd, color="#5E6670", lw=2.4, label="Default")
a.plot(du["time"] + noon, du, color="#1F6FB2", lw=1.3, label="U-Surf")
a.set_ylabel("T$_{1.5\\,m}$ (°C)")
a.set_title("a  Daily mean, both runs", loc="left", fontweight="bold", fontsize=16)
a.set_ylim(float(dd.min()) - 1, float(dd.max()) + 0.45 * float(dd.max() - dd.min()))
a.legend(loc="upper left", frameon=False, ncol=2, fontsize=15)
a.tick_params(labelbottom=False)

b.plot(diff["time"], diff, color="#A84A12", lw=0.3, alpha=0.45)
b.plot(ddiff["time"] + noon, ddiff, color="#A84A12", lw=1.8)
b.axhline(0, color="#55615C", lw=1.0)
b.axhline(float(diff.mean()), color="#16302B", lw=1.4, ls=(0, (5, 3)))
b.text(0.98, 0.06, f"mean {float(diff.mean()):+.2f} K".replace("-", "−"), transform=b.transAxes,
       ha="right", va="bottom", fontweight="bold", fontsize=15)
b.set_ylabel("U − D (K)")
b.set_title("b  U-Surf − Default, hourly and daily", loc="left", fontweight="bold", fontsize=16)
b.set_xlim(np.datetime64("2012-04-01"), np.datetime64("2014-01-01"))
b.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
b.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

c.bar(by_hour["hour"] + 0.5, by_hour, width=0.8, color="#A84A12")
c.axhline(0, color="#55615C", lw=1.0)
c.set_xlim(0, 24)
c.set_xticks([0, 6, 12, 18, 24])
c.set_xlabel("Hour (UTC)")
c.set_ylabel("U-Surf − Default (K)")
c.set_title("c  By hour of day", loc="left", fontweight="bold", fontsize=16)

for ax in (a, b, c):
    ax.grid(axis="y", color="#D9E0DC", lw=0.8)
    ax.set_axisbelow(True)
fig.savefig(f"{root}/kcl_default/compare.png", dpi=200)
print("saved", f"{root}/kcl_default/compare.png")
