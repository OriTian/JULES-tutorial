# Running JULES — a beginner's guide

By this point you should have two things ready. If you don't, this
script will fail immediately:

```text
1. a built jules.exe        -> scripts/setup/README.md, steps 2-3
2. a run directory          -> scripts/setup/README.md, step 4
                                (namelists/ + an empty output/ folder)
```

## What actually happens when you "run JULES"

There's no scheduler, no queue, nothing to submit — `jules.exe` is just an
ordinary program. You point it at a folder full of `.nml` files, it reads
them, simulates the period they describe, and writes NetCDF files into
`output/`, then exits. The tutorial's single-point KCL run (21 months in
30-minute steps) takes a minute or two.

```text
jules.exe  +  namelists/  ->  reads every .nml file in the folder
                           ->  simulates the period timesteps.nml describes
                           ->  writes output/*.nc
                           ->  exits
```

## The easy way: the script

```bash
cat > ~/run_jules.sh << 'EOF'
# ...paste run_jules.sh here...
EOF
bash ~/run_jules.sh
```

Safe to run from anywhere on the instance — the script `cd`s into the run
directory itself, so it doesn't matter whether you were already sitting in
it. Two environment variables let you point it elsewhere without editing
the script:

```text
RUN_DIR      which run directory to use      (default: ~/kcl_default)
JULES_EXE    which jules.exe to use          (default: ~/jules_build/build/bin/jules.exe)
```

```bash
RUN_DIR=~/kcl_usurf bash ~/run_jules.sh
```

## The manual way, one command at a time

If you'd rather see each step (or the script fails and you want to debug
by hand), this is exactly what it does underneath:

```bash
cd ~/kcl_default
mkdir -p output              # JULES does not create this itself --
                              # it errors out if the folder is missing
~/jules_build/build/bin/jules.exe namelists/ 2>&1 | tee run.log
```

## How do I know it worked?

No fancy success message — if there is no `[FATAL ERROR]` line and the
log ends by closing `output/kcl_default.hourly_output.nc`, it worked.
Check for output files:

```bash
ls output/
```

You should see one or more `.nc` files (named after `output.nml`'s
`run_id`/`profile` settings, e.g. `kcl_default.hourly_output.nc`). If `output/`
is empty or you got a Fortran error instead, see the "Common errors" table
in the main [`README.md`](../../README.md#chapter-17-common-errors).

## What's next

Once you have output, see
[`scripts/postprocessing/README.md`](../postprocessing/README.md) to plot
it and check it looks sensible.

---

[Back to main tutorial](../../README.md)
