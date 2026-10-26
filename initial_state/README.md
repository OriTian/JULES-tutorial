# Start states

```text
UK-KingsCollege_default_spinup_end_20120401.nc   KCL Default
UK-KingsCollege_usurf_spinup_end_20120401.nc     KCL U-Surf
```

JULES dump files: the model state (soil temperature and moisture, snow,
tile temperatures, ...) at 00:00 on 1 April 2012, at the end of each
configuration's spin-up. The spin-up repeated April 2011 – March 2012
forty times, so that soil temperature and moisture settled. That takes too
long on EC2, so each tutorial run starts from its own saved state, with
`max_spinup_cycles=0` in `timesteps.nml`.

`initial_conditions.nml` reads them:

```fortran
&jules_initial
  dump_file=.true.
  file='/path/to/UK-KingsCollege_default_spinup_end_20120401.nc'
  total_snow=.false.
/
```

`get_run.sh` replaces `/path/to/` with the absolute path.
`total_snow=.false.` reads the snow layers from the dump instead of
rebuilding them from a total.
