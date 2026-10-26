# Forcing data

## `UK-KingsCollege_era5_ml134_point_forcing_201103-201401.nc` (tutorial)

Hourly ERA5 forcing for King's College London (KCL), 1 March 2011 to
31 January 2014 (25632 hours), interpolated to the KCL point:

```text
Tair, Qair, Wind   ERA5 model level 134, about 78 m above the ground at KCL (instantaneous)
Pstar              surface pressure (instantaneous)
SwDown, LwDown,    mean over the hour ENDING at each time stamp
Precip
```

`drive.nml` reads it with `interp='nb','nb','i','i','i','nb','i'`
(radiation and rain `nb`, the rest `i`) and `data_start='2011-03-01 00:00:00'`,
`data_end='2014-02-01 00:00:00'`. JULES does not read the time variable:
it gives the first record the time `data_start` and counts forward, so
`data_start` must be the time of the first record.

`z1_tq_in`/`z1_uv_in` are the forcing height above the displacement height
`d`: 74.1389 m for Default, 57.1836 m for U-Surf.

## `London_StJamesPark_era5_2022_10-2023_12.nc` (older example)

Hourly ERA5 forcing for London St James's Park, October 2022 to
December 2023; used by `namelists/London_StJamesPark`.
