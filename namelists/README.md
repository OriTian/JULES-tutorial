# JULES Namelists

This directory contains complete JULES namelist sets used in the tutorial.

Each subdirectory corresponds to one runnable example case and contains the full set of `.nml` files required by JULES.

## Available cases

* `London_StJamesPark/`
  Tutorial example for London St James's Park.

## Usage

Copy the full namelist directory for the case you want to run:

```bash
mkdir -p ~/my_first_run
cp -r namelists/London_StJamesPark ~/my_first_run/namelists
```

JULES should then be run by pointing `jules.exe` to this directory:

```bash
~/jules_build/build/bin/jules.exe ~/my_first_run/namelists/
```

## Important files

Although JULES requires the complete namelist set, the following files contain most of the case-specific settings used in this tutorial:

* `jules_surface_types.nml` — surface tile definitions
* `jules_surface.nml` — main surface and urban switches
* `urban.nml` — MORUSES urban scheme options
* `ancillaries.nml` — surface fractions, soil properties and urban properties
* `drive.nml` — meteorological forcing configuration
* `timesteps.nml` — simulation period and timestep
* `output.nml` — output directory, frequency and variables

The remaining namelist files provide supporting JULES configuration and should normally be kept unchanged for the tutorial case.

## Creating a new case

For a new site, the recommended approach is to copy an existing working case:

```bash
cp -r namelists/London_StJamesPark namelists/My_New_Site
```

Then modify only the site-specific settings, particularly:

* forcing file path and period in `drive.nml`
* simulation dates in `timesteps.nml`
* output settings in `output.nml`
* surface fractions and urban properties in `ancillaries.nml`
