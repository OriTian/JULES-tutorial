# Tile-fraction files

Ten tile fractions per file, in the order of `jules_surface_types.nml`
(1–5 PFTs, 6 lake, 7 bare soil, 8 ice, 9 urban canyon, 10 urban roof).

## KCL (tutorial)

```text
                                   tree  grass  lake  canyon  roof
UK-KingsCollege_default_frac.nc    0.03  0.04   0.14  0.5782  0.2118
UK-KingsCollege_usurf_frac.nc      0.03  0.04   0.14  0.3918  0.3982
```

The urban total is 0.79 in both files. The canyon/roof split was
precomputed from each configuration's `wrr` (canyon = 0.79 × wrr):
0.732 for Default, 0.496 for U-Surf. JULES reads canyon and roof directly
and does not split them again. The 0.14 lake is the Thames.

## `London_StJamesPark_frac.nc` (older example)

London St James's Park (lat 51.5081, lon −0.1338), from the UKV 10-tile
fraction ancillary at the nearest grid cell:

```text
0.0, 0.0, 0.0377, 0.0, 0.0, 0.0083, 0.0137, 0.0, 0.2052, 0.7351
```
