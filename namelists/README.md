# JULES Namelists — a beginner's guide

If you've never seen a `.nml` file before, start here. This page assumes
nothing.

## What even is a "namelist"?

A namelist is just a Fortran config file — JULES is written in Fortran, and
Fortran programs read their settings from files shaped like this:

```fortran
&jules_time
  main_run_start = '2012-04-01 00:00:00'
  main_run_end   = '2014-01-01 00:00:00'
  timestep_len   = 1800
/
```

Read it like a dictionary:

```text
&jules_time    the name of this block of settings
main_run_start   a setting inside it, with a value
main_run_end     another setting
timestep_len     another setting
/              end of the block
```

That's the whole syntax. A `.nml` file is just one or more of these blocks,
one after another. JULES opens a folder full of these files at startup,
reads every block, and configures itself accordingly — no code, no
compiling, just editing text.

## Why are there so many files?

Because JULES is one program that can simulate almost anything (forests,
crops, snow, rivers, cities...), and each of those has its own settings.
Rather than one giant file, JULES splits them into ~45 small files by
topic — `jules_snow.nml` for snow, `jules_rivers.nml` for river routing,
`urban.nml` for the urban scheme, and so on. **You only ever need to touch
a handful of them.** The rest exist because JULES insists on finding every
file it expects, even if the physics in it is switched off for your run.

## What's in this folder

```text
namelists/
├── KCL_Default/            Run 1: KCL, Default urban form (45 .nml files)
├── KCL_USurf/              Run 2: KCL, U-Surf urban form and materials (45 .nml files)
└── London_StJamesPark/     older example (43 .nml files)
```

Each subfolder here is one complete, ready-to-run **case** — a full set of
namelists for one site. `KCL_Default/` and `KCL_USurf/` differ in five
files: `ancillaries.nml`, `drive.nml`, `initial_conditions.nml`,
`output.nml` and `urban.nml`.

The input files are named `'/path/to/<file name>'`. `get_run.sh` copies a
case and replaces those with the absolute paths.

## Try it: copy a case and run it

```bash
DATA_DIR="$HOME/jules-tutorial-data"
bash "$DATA_DIR/scripts/setup/get_run.sh" default
cd ~/kcl_default
~/jules_build/build/bin/jules.exe namelists/ 2>&1 | tee run.log
```

That's it — no arguments, no flags, just a folder. `jules.exe` reads the
`.nml` files it needs from that folder and starts simulating.

## Fixed file names

JULES opens each namelist block from a fixed file name, so some files in
the folder are look-alikes that are never read:

```text
&jules_initial                      initial_conditions.nml   (not jules_initial.nml)
&jules_time, &jules_spinup          timesteps.nml            (not jules_time.nml, jules_spinup.nml)
&jules_frac, &urban_properties      ancillaries.nml          (not jules_frac.nml, urban.nml)
&jules_nvegparm                     nveg_params.nml          (not jules_nvegparm.nml)
```

Keep the tested directory together, but edit only the files JULES reads.

## The 7 files worth actually understanding

Of the 45 files, these seven carry essentially all of the tutorial's
site-specific and science-specific settings. Everything else can stay as
it is.

| File | What it controls | Plain-English example |
|---|---|---|
| `drive.nml` | the weather driving the model | "here's the ERA5 file, hourly; T and wind are 74.1 m above d" |
| `timesteps.nml` | simulation clock and spin-up | "run from 1 Apr 2012 to 1 Jan 2014, 30 minutes per step, no spin-up" |
| `initial_conditions.nml` | the start state | "start from the dump saved at the end of the spin-up" |
| `jules_surface_types.nml` | how many surface tiles exist, and which number is which | "this run has 10 tile types; canyon is #9, roof #10" |
| `ancillaries.nml` | tile fractions (`&jules_frac`) and urban form and materials (`&urban_properties`) | "this grid cell is 58% canyon and 21% roof" |
| `urban.nml` | MORUSES urban-scheme options (`&jules_urban`) | "work out building height and canyon shape from the urban fraction" |
| `output.nml` | what to save, and where | "save 11 variables, hourly, to `output/kcl_default.hourly_output.nc`" |

If you're only skimming one file to understand what a case *does*, read
`drive.nml` + `timesteps.nml` (what weather, what period) and `output.nml`
(what you'll get back).

## Making your own site

Don't write a case from scratch — copy the working one and change only
what needs to change:

```bash
cp -r namelists/KCL_Default namelists/My_New_Site
```

Then edit just these, in this order:

1. **`drive.nml`** — point `file=` at your own forcing `.nc`, and set the
   period to match the data you actually have.
2. **`timesteps.nml`** — set `main_run_start`/`main_run_end` to the period
   you want to simulate (must be inside the forcing file's coverage).
3. **`ancillaries.nml`** — point at your site's own fraction/urban-property
   file, or set new `const_val` numbers directly.
4. **`initial_conditions.nml`** and **`timesteps.nml`** — a new site has no
   saved start state: start from a constant state (`dump_file=.false.`)
   and switch the spin-up back on.
5. **`output.nml`** — change `run_id` so you don't overwrite the previous
   run's output.

Everything else in the folder can be left exactly as copied.
