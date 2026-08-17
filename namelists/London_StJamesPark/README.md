# London St James's Park Namelist Case

This directory contains the complete JULES namelist configuration used for the London St James's Park tutorial example.

## Site

* **Site:** London St James's Park
* **Latitude:** 51.5081
* **Longitude:** -0.1338
* **Model:** JULES
* **Urban scheme:** MORUSES two-tile urban scheme

## Forcing data

The corresponding meteorological forcing file is:

```text
data/forcing/London_StJamesPark_era5_2022_10-2023_12.nc
```

The forcing data are derived from ERA5 and contain hourly:

* air temperature
* specific humidity
* wind speed
* surface pressure
* precipitation
* downward shortwave radiation
* downward longwave radiation

The forcing period covers October 2022 to December 2023.

For the tutorial run, the configuration uses:

```text
data_start = 2023-02-01 00:00:00
data_end   = 2023-07-31 23:00:00
```

## Simulation period

The main simulation period is:

```text
2023-03-01 00:00:00
to
2023-07-31 23:00:00
```

The February forcing period provides approximately one month of additional forcing before the main analysis period.

The model timestep is:

```text
3600 seconds
```

## Surface fractions

The corresponding surface fraction file is:

```text
data/frac/London_StJamesPark_frac.nc
```

The tutorial fraction configuration contains 10 surface tiles:

1. Broadleaf vegetation
2. Needleleaf vegetation
3. C3 grass
4. C4 grass
5. Shrub
6. Lake
7. Bare soil
8. Ice
9. Urban canyon
10. Urban roof

For this example, the dominant surface type is urban, with separate canyon and roof fractions used by the two-tile urban scheme.

## Urban configuration

The tutorial enables the JULES two-tile urban scheme:

```fortran
l_urban2t=.true.
```

MORUSES urban parameterisations are enabled in `urban.nml`.

The tutorial also uses:

```fortran
l_urban_empirical=.true.
```

so the urban geometry is estimated using the empirical MORUSES configuration rather than manually prescribed geometry.

The radiative urban parameters used in `ancillaries.nml` are:

```text
Wall albedo:       0.25
Road albedo:       0.08
Wall emissivity:   0.90
Road emissivity:   0.95
```

## Main namelist files

The most important case-specific files are:

* `ancillaries.nml`
* `drive.nml`
* `jules_surface.nml`
* `jules_surface_types.nml`
* `urban.nml`
* `timesteps.nml`
* `output.nml`

However, the full directory should be kept together because JULES requires additional supporting namelist files.

## Running the example

Copy this directory into a working run directory:

```bash
mkdir -p ~/my_first_run
cp -r namelists/London_StJamesPark ~/my_first_run/namelists
```

Create the output directory:

```bash
mkdir -p ~/my_first_run/output
```

Then run JULES:

```bash
cd ~/my_first_run
~/jules_build/build/bin/jules.exe namelists/
```

## Expected output

The tutorial configuration produces hourly output containing variables including:

* `ftl_gb`
* `fqw_gb`
* `tstar_gb`
* `t1p5m_gb`
* `sw_down`
* `lw_down`
* `rad_net`
* `tstar`
* `t1p5m`
* `ftl`

