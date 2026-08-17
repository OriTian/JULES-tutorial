# Postprocessing

- `plot_quicklook.py` — quick single-variable timeseries plot from a JULES output file, a sanity check before deeper analysis.
- `read_tile_output.py` — read gridbox-mean and per-tile output, compute an "urban-only" (canyon+roof frac-weighted) value that `_gb` blends away. Check the run's own `jules_surface_types.nml` for tile indices before using this on a run other than the tutorial's.
