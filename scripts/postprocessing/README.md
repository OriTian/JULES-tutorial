# Postprocessing — a beginner's guide

JULES just finished and wrote a `.nc` file into `output/`. Now what? This
folder has two small scripts for looking at what came out — nothing fancy,
just enough to sanity-check a run and pull out the one number the urban
tutorial actually cares about.

## What's a `.nc` file, and how do I even open one?

JULES output is NetCDF — a binary file format for scientific data, not
something you can `cat` and read. Both scripts below use the Python
`netCDF4` library to open it; think of the file as a dictionary of
variables (`t1p5m_gb`, `tstar`, ...), each one an array of numbers indexed
by time (and, for per-tile variables, by tile too).

```bash
source ~/miniforge3/bin/activate   # or wherever your Python env lives
```

Both scripts need that first, since `netCDF4`/`matplotlib`/`pandas` live
there, not in the system Python.

## `plot_quicklook.py` — "did the run actually work?"

The first thing to run after any JULES simulation, before any real
analysis. Plots one variable over time and saves a PNG — if the line looks
like a plausible temperature curve (not all zeros, not `NaN`, not a flat
line), the run worked.

```bash
python plot_quicklook.py output/kcl_default.hourly_output.nc \
    --var t1p5m_gb --out quicklook.png
```

```text
nc_path    the JULES output file to read
--var      which variable to plot (default: t1p5m_gb, 1.5m air temperature)
--out      where to save the PNG (default: quicklook.png)
```

Kelvin variables (`t1p5m_gb`, `tstar_gb`, `t1p5m`, `tstar`) are
automatically converted to Celsius for the plot — everything else is
plotted in whatever units JULES wrote it in.

## `read_tile_output.py` — canyon and roof, one tile at a time

`_gb` variables (e.g. `t1p5m_gb`, `tstar_gb`) are **gridbox means** —
JULES has blended all 10 tile types (vegetation, lake, soil, ice, canyon,
roof) into one number, weighted by how much of the point each tile covers.

This script reads the **per-tile** output (`tstar`, `t1p5m` — no `_gb`
suffix, one value per tile) and returns the canyon and roof tiles
separately. For the surface temperature `tstar` it also returns a
canyon+roof mean weighted by the two fractions:

```text
tstar_urban_only = (frac_canyon * tstar_canyon + frac_roof * tstar_roof) / (frac_canyon + frac_roof)
```

It does **not** do this for `t1p5m`: canyon and roof 1.5 m temperatures
are kept apart, because a fraction-weighted mean of them is not an urban
1.5 m air temperature. Use `t1p5m_gb`, or each tile on its own.

Unlike `plot_quicklook.py`, this one isn't a ready-to-run command-line
tool — it's a small function (`load_output(...)`) you call with four
numbers specific to your run. The example at the bottom is set for KCL
Default; run it from `~/kcl_default`:

```python
data = load_output(
    "output/kcl_default.hourly_output.nc",
    canyon_idx=8, roof_idx=9,               # tiles 9 and 10 in jules_surface_types.nml
    canyon_frac=0.5782, roof_frac=0.2118,   # KCL Default frac file
)
print(data["tstar_urban_only"].mean())
```

```bash
cd ~/kcl_default && python ~/jules-tutorial-data/scripts/postprocessing/read_tile_output.py
```

**Before running this on any other run**, check that run's own
`jules_surface_types.nml` for `canyon_idx`/`roof_idx` (Python counts from
0, so tile 9 is index 8), and its frac file for `canyon_frac`/`roof_frac`
(KCL U-Surf: 0.3918 and 0.3982) — **tile order is not fixed across run
directories**, and the wrong index silently reads the wrong tile, with no
error.

## Which one do I run first?

```text
1. plot_quicklook.py    every time, right after a run -- did it work at all?
2. read_tile_output.py  only once you want the canyon and roof tiles
                         separately, not the gridbox mean
```

---

[Back to main tutorial](../../README.md)
