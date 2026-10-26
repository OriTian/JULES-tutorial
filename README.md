# JULES/MORUSES Urban Climate Modelling on EC2

A step-by-step lab for running JULES with the MORUSES urban scheme on a
group EC2 instance — from first SSH connection through building JULES,
running King's College London (KCL) with two urban descriptions, Default
and U-Surf, and comparing their air temperature. No prior JULES experience
assumed.

Every command block below is complete and self-contained — copy the whole
block, paste it into the EC2 terminal, done. The one exception is JULES's
own source code, fetched with `git clone` in Chapter 8 — that's a real
external dependency, not part of this repo.

## Quick start: a new EC2 instance

Every tutorial instance starts empty. Log in (Chapter 1), then paste this
block once per instance — if two of you share an instance, only one of
you runs it:

```bash
curl -fsSL -o /tmp/jules-tutorial-data.tar.gz \
  https://github.com/OriTian/JULES-tutorial/archive/main.tar.gz
mkdir -p ~/jules-tutorial-data
tar -xzf /tmp/jules-tutorial-data.tar.gz -C ~/jules-tutorial-data --strip-components=1
nohup bash ~/jules-tutorial-data/scripts/setup/install.sh > ~/install.log 2>&1 &
```

The first three lines download this repo into `~/jules-tutorial-data`.
`install.sh` then does all of Chapters 3–9 (swap, compiler, Miniforge +
NetCDF-Fortran, FCM, JULES source, Python packages, compile `jules.exe`)
in the background, so it keeps going if your SSH connection drops. Check
on it with:

```bash
tail -n 3 ~/install.log
```

It is finished when the last line reads `INSTALL DONE in … min`. If it
reads `INSTALL FAILED`, look at the lines above it, then start the same
`nohup` line again: finished steps are skipped. Then go on with
Chapter 11.

---

## How to read this — a beginner's guide

Never used a GitHub repo before? Here's exactly what to click, in order.

**Step 0.** You're already looking at the right thing. When you open this
repo's page on GitHub, `README.md` (this file) is what's shown to you
automatically, scrollable top to bottom — you don't need to go hunting for
a "start here" file, this *is* it.

**Step 1.** Scroll down (or use the links below) and read the 18 chapters
**in order, top to bottom, the first time through**. Each chapter is one
`# Chapter N. ...` heading — don't skip ahead, later chapters assume
you've done the earlier ones. They fall into five groups:

```text
Chapter 1        Connect            get onto the EC2 instance over SSH
Chapter 2        Understand         the big picture before you type anything
Chapters 3–9     Build              swap, compiler, Miniforge, NetCDF-Fortran,
                                    FCM, JULES source, compile jules.exe
Chapters 10–12   Run                get the data, copy Run 1 (KCL Default),
                                    execute JULES
Chapters 13–14   Check the output   confirm it ran, read and plot it in Python
Chapters 15–16   Compare            Run 2 (KCL U-Surf), compare the 1.5 m air
                                    temperature of the two runs
Chapters 17–18   Reference          common-errors table + a final checklist —
                                    come back to these when something breaks,
                                    no need to read them in order
```

Click any chapter below to jump straight to it (these are just anchor
links to further down this same page):

- [Chapter 1. Connect to EC2](#chapter-1-connect-to-ec2)
- [Chapter 2. Understand the JULES workflow](#chapter-2-understand-the-jules-workflow)
- [Chapter 3. Prepare swap memory](#chapter-3-prepare-swap-memory)
- [Chapter 4. Install build tools](#chapter-4-install-build-tools)
- [Chapter 5. Install Miniforge](#chapter-5-install-miniforge)
- [Chapter 6. Install NetCDF-Fortran](#chapter-6-install-netcdf-fortran)
- [Chapter 7. Install FCM](#chapter-7-install-fcm)
- [Chapter 8. Download JULES](#chapter-8-download-jules)
- [Chapter 9. Build JULES](#chapter-9-build-jules)
- [Chapter 10. Get the tutorial data](#chapter-10-get-the-tutorial-data)
- [Chapter 11. Prepare Run 1 (KCL Default)](#chapter-11-prepare-run-1-kcl-default)
- [Chapter 12. Run JULES](#chapter-12-run-jules)
- [Chapter 13. Verify the output](#chapter-13-verify-the-output)
- [Chapter 14. Read and plot Run 1](#chapter-14-read-and-plot-run-1)
- [Chapter 15. Run 2: KCL U-Surf](#chapter-15-run-2-kcl-u-surf)
- [Chapter 16. Compare Default and U-Surf](#chapter-16-compare-default-and-u-surf)
- [Chapter 17. Common errors](#chapter-17-common-errors)
- [Chapter 18. Checklist](#chapter-18-checklist)

**Step 2.** Once you understand *why* each step works (that's what this
file is for), the actual copy-paste commands also live in the `scripts/`
folder, one subfolder per group above, each with its own beginner-friendly
README:

- [`scripts/setup/README.md`](scripts/setup/README.md) — Chapters 1–9's connect/build steps, and `install.sh`
- [`scripts/run/README.md`](scripts/run/README.md) — Chapter 12's run step
- [`scripts/postprocessing/README.md`](scripts/postprocessing/README.md) — more plotting helpers, beyond `quicklook.py` and `compare.py`
- [`scripts/preprocessing/README.md`](scripts/preprocessing/README.md) — only if you're building a *new* site, not the tutorial's example
- [`scripts/clearup/README.md`](scripts/clearup/README.md) — freeing disk space on the instance, any time

Or [`scripts/README.md`](scripts/README.md) itself bundles all of the
above into one page of ready-to-paste blocks, in order, with no
explanation — the fast path once you already know what each step does.

**In short: read this file for the *why*, use `scripts/` for the
commands.**
# Chapter 1. Connect to EC2

## Learning objective

Connect from your local computer to a remote EC2 Linux server over SSH.

```text
Local computer
      ↓
     SSH
      ↓
EC2 instance
```

## Step 1. Get your connection details

You need three things — ask in the group chat for the current instance IP
and the shared `.pem` key file if you don't have them yet:

```text
Public IP address   e.g. 54.xx.xx.xx
Username             ec2-user
Private key (.pem)   e.g. jules.pem
```

Put the `.pem` file somewhere on your **local machine** (not on EC2), e.g.
`~/Desktop/jules.pem`. On macOS/Linux, fix its permissions once:

```bash
chmod 400 ~/Desktop/jules.pem
```

## Step 2. Connect

Open a terminal on your **local machine** (Terminal.app, iTerm, Windows
Terminal + WSL, etc.) and run:

```bash
ssh -i ~/Desktop/jules.pem ec2-user@54.xx.xx.xx
```

### Command breakdown

```text
ssh          Secure Shell — opens an encrypted remote session
-i           "identity file" — which private key to authenticate with
jules.pem    the shared private key for this instance
ec2-user     the login account on the EC2 instance
54.xx.xx.xx  the instance's public IP
```

### Success indicator

The first time you connect to a given instance you'll be asked to confirm
its fingerprint — type `yes`. You'll know it worked when the prompt changes
to `[ec2-user@ip-... ~]$`:

```text
❯ ssh -i "jules.pem" ec2-user@ec2-18-130-30-147.eu-west-2.compute.amazonaws.com
The authenticity of host 'ec2-18-130-30-147.eu-west-2.compute.amazonaws.com (18.130.30.147)' can't be established.
ED25519 key fingerprint is: SHA256:5NZ8f8ZXknpalfUBdCbjI+Wh0jV9HTNF2QwMLeUgaSU
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'ec2-18-130-30-147.eu-west-2.compute.amazonaws.com' (ED25519) to the list of known hosts.
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
[ec2-user@ip-172-31-46-208 ~]$
```

**Everything from here on happens inside this one SSH session** — no need
to go back to your local machine until Chapter 16 (downloading plots).

---

# Chapter 2. Understand the JULES workflow

## What is JULES?

```text
Joint UK Land Environment Simulator
```

A land-surface model that simulates the exchange of energy, water and
carbon between the land surface and the atmosphere:

```
Meteorology
    ↓
  JULES
 ┌─────────────┐
 │ Radiation   │
 │ Heat flux   │
 │ Soil water  │
 │ Carbon      │
 └─────────────┘
    ↓
Air temperature, surface temperature,
sensible heat, latent heat
```

## What is MORUSES?

```text
Met Office - Reading Urban Surface Exchange Scheme
```

JULES's two-tile representation of a city: instead of one blended "urban"
surface, a city point is split into a **canyon** tile (streets + walls) and
a **roof** tile, each with its own energy balance:

```text
       roof
-------|    |-------
       |    |
       |canyon|
       |------|
```

## The workflow at a glance

```text
Set up the environment  →  Build JULES  →  Get a run directory  →  Run  →  Plot
     (once)                  (once)         (per site)          (per run)
```

Everything you do after the first two steps is just editing small text
config files ("namelists") and re-running — no need to touch the source
code again.

---

# Chapter 3. Prepare swap memory

Chapters 3–9 explain, step by step, what `scripts/setup/install.sh` does
in one go (see the Quick start at the top). Read them to understand the
setup, or to repair a step by hand.

## Why

This group's EC2 instances are small (~900MB–1GB RAM). Compiling JULES
without extra swap space reliably runs out of memory partway through.

## Step 3. Check current memory

```bash
free -h
```

Look at the `Mem` and `Swap` rows:

```text
               total        used        free      shared  buff/cache   available
Mem:           957Mi       161Mi       552Mi       0.0Ki       243Mi       663Mi
Swap:             0B          0B          0B
```

If `Swap` is `0B`, you need the next two steps.

## Step 4. Create a 2GB swap file

```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
```

```text
Input:  /dev/zero          (an endless stream of zero bytes)
Output: /swapfile           (the file being created)
Size:   2048 × 1MB = 2GB
```

## Step 5. Enable the swap file

```bash
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Verify:

```bash
free -h
```

Expected:

```text
               total        used        free      shared  buff/cache   available
Mem:           957Mi       122Mi        83Mi       0.0Ki       751Mi       702Mi
Swap:          2.0Gi          0B       2.0Gi
```

These three commands are idempotent — safe to paste again later without
creating a second swap file (the setup script in Chapter 4 skips this step
automatically if swap is already on).

---

# Chapter 4. Install build tools

## Step 6–8. Compiler, git, make, perl

JULES is written in Fortran and built with FCM (Chapter 7), which needs a
handful of Perl modules a minimal Amazon Linux image doesn't ship by
default.

```bash
sudo dnf install -y git make gcc gcc-gfortran \
  perl-FindBin perl-File-Copy perl-File-Compare perl-Sys-Hostname \
  perl-IO-Compress perl-Digest-SHA perl-Text-Balanced perl-Time-Piece perl-filetest
```

```text
git           → download source code
make          → build software from source
gcc-gfortran  → the Fortran compiler that will compile JULES
perl-*        → modules FCM's build scripts assume are present
```

Verify the Fortran compiler is there:

```bash
gfortran --version
```

---

# Chapter 5. Install Miniforge

## Why

Miniforge gives you `conda`, Python, and — critically — a working
`netcdf-fortran` library, which Amazon Linux's own package repos don't
ship at all.

## Step 9–10. Download and install

```bash
curl -sL -o /tmp/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash /tmp/miniforge.sh -b -p ~/miniforge3
```

Expected tail of the output:

```text
Linking conda-26.3.2-py313h78bf25f_1
Transaction finished
installation finished.
```

## Step 11. Activate it

```bash
source ~/miniforge3/bin/activate
```

Verify:

```bash
conda --version
```

You'll need to re-run this `source` line in any new terminal session where
you want `conda` on your `PATH` — it isn't permanent by default.

---

# Chapter 6. Install NetCDF-Fortran

## Why

JULES reads its meteorological forcing from `.nc` (NetCDF) files and writes
its output as `.nc` files too — it needs the Fortran NetCDF library to do
either.

## Step 12. Install

```bash
conda install -y -c conda-forge "netcdf-fortran=4.6.4=nompi_*_100"
```

> **Why this exact build:** JULES is compiled with the system gfortran 11,
> and it must read the `netcdf.mod` file that comes with `netcdf-fortran`.
> conda-forge builds since September 2026 are compiled with gfortran 15,
> whose `.mod` files gfortran 11 cannot read (`Cannot read module file
> 'netcdf.mod' ... created by a different version of GNU Fortran`). Build
> `_100` of 4.6.4 was compiled with gfortran 14 and works.

> **Only `netcdf-fortran` here — not `xarray` or other Python packages.**
> Installing more packages alongside it makes conda's dependency solver do
> much more work, and on an instance this small the solver process has been
> observed to get OOM-killed partway through. Python packages for plotting
> come later, via `pip` (Chapter 4 of the script bundle), which uses
> prebuilt wheels instead of solving a dependency graph.

## Step 13. Verify

```bash
nf-config --version
```

Expected:

```text
$ nf-config --version
4.6.4
```

---

# Chapter 7. Install FCM

## What is FCM?

```text
Flexible Configuration Management
```

The Met Office's own build tool — JULES compiles with `fcm make`, not a
plain `Makefile`.

## Step 14. Download

```bash
git clone -q https://github.com/metomi/fcm.git ~/fcm
```

## Step 15. Verify

```bash
~/fcm/bin/fcm --version
```

```text
FCM 2021.05.0-12-g3b045b3 (/home/ec2-user/fcm)
```

---

# Chapter 8. Download JULES

## Step 16. Clone the JULES source

This is the one genuine external dependency in the whole setup — everything
else so far has been generic Linux tooling. `--branch vn8.1` fixes the
version: the tutorial namelists were tested with JULES vn8.1, and the
`main` branch keeps changing.

```bash
git -c advice.detachedHead=false clone -q --depth 1 --branch vn8.1 \
  https://github.com/MetOffice/jules.git ~/jules_source
```

## Important folders inside it

```text
src/    Fortran source code
etc/    build configuration (fcm-make/make.cfg — used in Chapter 9)
docs/   JULES's own documentation
```

---

# Chapter 9. Build JULES

## Step 17. Put the tools on your PATH

```bash
source ~/miniforge3/bin/activate
export PATH=$HOME/fcm/bin:$HOME/miniforge3/bin:$PATH
```

## Step 18–21. Tell `fcm make` how to build

```bash
export JULES_PLATFORM=custom
export JULES_COMPILER=gfortran
export JULES_BUILD=normal
export JULES_OMP=noomp
export JULES_MPI=nompi
export JULES_NETCDF=netcdf
export JULES_NETCDF_PATH=$HOME/miniforge3
export JULES_FFLAGS_EXTRA="-fallow-argument-mismatch -Wno-error -std=gnu"
```

```text
JULES_PLATFORM=custom   JULES ships ready-made configs for JASMIN/Met
                         Office clusters, not a plain EC2 box — this tells
                         it to use its generic path instead
JULES_COMPILER=gfortran use the GNU Fortran compiler
JULES_MPI=nompi         single-process build, no MPI
JULES_OMP=noomp         no shared-memory (OpenMP) parallelism
JULES_NETCDF=netcdf     enable NetCDF file I/O, pointed at Miniforge's copy
JULES_FFLAGS_EXTRA       gfortran 11 is strict about JULES's dummy-MPI
                         stub's implicit interface; without the first two
                         flags the build fails with a hard compiler error.
                         -std=gnu overrides the strict -std=f2003 in
                         JULES's gfortran settings (the JASMIN gfortran
                         build of the same source also drops it)
```

## Step 22. Compile

```bash
mkdir -p ~/jules_build && cd ~/jules_build
fcm make -f ~/jules_source/etc/fcm-make/make.cfg -j 1
```

```text
Fortran source
    ↓
Object files
    ↓
Link libraries
    ↓
jules.exe
```

Use `-j 1`, not a higher number — these instances are too small for
parallel compilation. Expect ~1 minute for all 617 source files:

```text
[info] sources: total=617, analysed=0, elapsed-time=0.1s, total-time=0.0s
[info] compile   targets: modified=7, unchanged=485, failed=0, total-time=52.0s
[info] link      targets: modified=1, unchanged=0, failed=0, total-time=0.9s
[done] make                # 55.7s
```

## Step 23. Verify

```bash
ls -la ~/jules_build/build/bin/jules.exe
```

You should see a ~55MB executable. This step only needs to be done once —
everything after this is per-run, not per-build.

---

# Chapter 10. Get the tutorial data

## Today's case: KCL, two runs

The tutorial runs JULES at King's College London (KCL, central London)
twice and compares the 1.5 m air temperature:

```text
Run 1   KCL Default   urban form from the empirical formulas (l_urban_empirical)
Run 2   KCL U-Surf    urban form and materials from the U-Surf dataset
```

Both runs use the same ERA5 forcing, period, soil, non-urban parameters
and output variables. Run 2 replaces the urban description and the
settings that depend on it: the canyon/roof fractions, the forcing height
above the displacement height, and the start state.

## Step 24. Download this tutorial's data

Already done if you used the Quick start at the top. Otherwise:

```bash
TMP_TAR="/tmp/jules-tutorial-data.tar.gz"     # download archive only
DATA_DIR="$HOME/jules-tutorial-data"          # unpacked data live in $HOME

curl -fsSL -o "$TMP_TAR" https://github.com/OriTian/JULES-tutorial/archive/main.tar.gz
rm -rf "$DATA_DIR" && mkdir -p "$DATA_DIR"
tar -xzf "$TMP_TAR" -C "$DATA_DIR" --strip-components=1
```

```text
curl -fsSL -o "$TMP_TAR"   download this tutorial repo as a .tar.gz archive
tar --strip-components=1   unpack it, dropping the repo-name folder level
```

This downloads a snapshot via `curl` (not `git clone`) — no repo history,
no git metadata, just the files this tutorial needs.

Only the download archive goes in `/tmp`. The unpacked data live in
`$HOME/jules-tutorial-data`: on Amazon Linux 2023, `/tmp` is a RAM-backed
tmpfs (capped at half the memory) and is emptied on reboot.

Repository layout, once unpacked:

```text
forcing_data/     ERA5 forcing for KCL, hourly, March 2011 – January 2014
ancillary_data/   tile-fraction files, one for Default and one for U-Surf
initial_state/    start states: the end of each configuration's 40-cycle spin-up
namelists/        KCL_Default/, KCL_USurf/ (45 files each), London_StJamesPark/
scripts/          get_run.sh, quicklook.py, compare.py, setup and cleanup helpers
```

---

# Chapter 11. Prepare Run 1 (KCL Default)

## Step 25. Copy the run and write the paths

```bash
DATA_DIR="$HOME/jules-tutorial-data"
bash "$DATA_DIR/scripts/setup/get_run.sh" default
cd ~/kcl_default
ls output
```

`get_run.sh default` copies `namelists/KCL_Default` into
`~/kcl_default/namelists`, creates an empty `~/kcl_default/output`, and
writes the absolute paths of the three input files into the namelists.
It downloads the data itself if Step 24 was skipped.

Expected:

```text
Run directory ready: /home/ec2-user/kcl_default
file='/home/ec2-user/jules-tutorial-data/forcing_data/UK-KingsCollege_era5_ml134_point_forcing_201103-201401.nc'
file='/home/ec2-user/jules-tutorial-data/ancillary_data/UK-KingsCollege_default_frac.nc'
file='/home/ec2-user/jules-tutorial-data/initial_state/UK-KingsCollege_default_spinup_end_20120401.nc'
Namelist files: 45
```

and `ls output` prints nothing. To start again, `rm -rf ~/kcl_default` and
rerun `get_run.sh`: it refuses to overwrite an existing run.

## Step 26. Look at the settings

The directory holds 45 namelist files, including compatibility and
look-alike files. Keep the tested directory together and focus on the
seven files used today:

| File | What it sets |
|---|---|
| `drive.nml` | forcing file, variables, `interp`, forcing height `z1_tq_in`/`z1_uv_in` |
| `timesteps.nml` | run period, 30-minute timestep, spin-up (`max_spinup_cycles=0`) |
| `initial_conditions.nml` | start state: the dump at the end of the spin-up |
| `jules_surface_types.nml` | tile numbers: lake 6, soil 7, urban canyon 9, urban roof 10 |
| `ancillaries.nml` | fraction file (`&jules_frac`) and urban materials (`&urban_properties`) |
| `urban.nml` | `&jules_urban`: Default uses `l_urban_empirical=.true.` |
| `output.nml` | 11 hourly variables in `output/kcl_default.hourly_output.nc` |

Three fixed-name traps: JULES reads `&jules_initial` only from
`initial_conditions.nml`, `&jules_time`/`&jules_spinup` only from
`timesteps.nml`, and `&jules_frac`/`&urban_properties` only from
`ancillaries.nml`. The look-alike files (`jules_initial.nml`,
`jules_time.nml`, `jules_spinup.nml`, `jules_frac.nml`, `jules_nvegparm.nml`)
are never opened.

```bash
grep z1_ namelists/drive.nml           # 74.1389: forcing height above d
grep main_run namelists/timesteps.nml  # 2012-04-01 to 2014-01-01
FRAC=$(awk -F"'" '/_frac.nc/{print $2}' namelists/ancillaries.nml)
ncdump -v frac "$FRAC"                 # canyon 0.58 + roof 0.21, lake 0.14, grass 0.04, trees 0.03
cat namelists/output.nml
```

`data_start`/`data_end` in `drive.nml` describe the forcing file, not the
run: JULES does not read the time variable in the file, it gives the first
record the time `data_start` and counts forward.

---

# Chapter 12. Run JULES

## Step 27. Start Run 1

```bash
cd ~/kcl_default
~/jules_build/build/bin/jules.exe namelists/ 2>&1 | tee run.log
tail -n 3 run.log
ls output
```

The only argument is the namelist folder. There is no job scheduler on
EC2: you start `jules.exe` yourself. The run is 30720 half-hour steps
(1 April 2012 to 1 January 2014); expect a minute or two.

## What happens internally

```text
Read namelists
    ↓
Read forcing, fractions and the start state
    ↓
Time integration, 30-minute steps
    ↓
Write NetCDF output and dump files
```

## Success indicator

No `[FATAL ERROR]` line, and the log ends by closing the output files:

```text
[INFO] file_ncdf_close: Closing file output/kcl_default.dump.20140101.0.nc
[INFO] file_ncdf_close: Closing file /home/ec2-user/jules-tutorial-data/forcing_data/UK-KingsCollege_era5_ml134_point_forcing_201103-201401.nc
[INFO] file_ncdf_close: Closing file output/kcl_default.hourly_output.nc
```

This JULES version prints no "finished" message: the closed hourly output
and the final dump are the sign that the run reached the end.

**Worried about your SSH connection dropping mid-run?** Start it inside
`tmux` so it keeps going even if you disconnect: `tmux new -s jules_run`,
run the command above inside that session, detach with `Ctrl-b` then `d`,
reconnect later with `tmux attach -t jules_run`.

---

# Chapter 13. Verify the output

## Step 28. List the output files

```bash
ls output
```

```text
kcl_default.dump.20120401.0.nc  kcl_default.dump.20130101.0.nc
kcl_default.dump.20140101.0.nc  kcl_default.hourly_output.nc
```

The `dump.*` files are snapshots of the model state: one at the start, one
at each new year and one at the end. `hourly_output.nc` holds the
variables listed in `output.nml`.

## Step 29. Inspect its structure

```bash
ncdump -h output/kcl_default.hourly_output.nc
```

Look for `dimensions`, `variables`, `units`, and `time` in the header —
this tells you what's inside without opening it in Python.

---

# Chapter 14. Read and plot Run 1

## Step 30. Run the provided script

```bash
source ~/miniforge3/bin/activate
DATA_DIR="$HOME/jules-tutorial-data"
python "$DATA_DIR/scripts/quicklook.py"
```

`quicklook.py` works from any folder. It reads
`~/kcl_default/output/kcl_default.hourly_output.nc`, prints the dataset and
the number of time values, and saves `~/kcl_default/run1_t1p5m.png`.

Expected: 11 variables plus `time_bounds`, then `time values: 15360`
(each hourly value is the mean of two 30-minute steps).

The key lines inside it:

```python
ds = xr.open_dataset(f"{run}/output/kcl_default.hourly_output.nc")
print(ds)                                  # variables, sizes, units
t = ds["t1p5m_gb"].squeeze() - 273.15      # K -> °C; squeeze drops the 1 x 1 grid
```

```text
t1p5m_gb   1.5 m air temperature, gridbox mean (kelvin in the file)
- 273.15   convert kelvin to °C before plotting
```

## Step 30b. See the plot on your laptop

EC2 has no screen. In a **new terminal window on your laptop** (keep the
EC2 window), run this one line; it copies the plots to your Desktop:

```bash
scp -i ~/Desktop/jules.pem "ec2-user@<your-ec2-ip>:kcl_default/*.png" ~/Desktop/
open ~/Desktop/run1_t1p5m.png
```

Replace `<your-ec2-ip>`, including the `< >`, with the address you use for
`ssh`. If your key is not on the Desktop, change `~/Desktop/jules.pem`. On
Windows PowerShell, write `$HOME\Desktop` instead of `~/Desktop`, and
`start` instead of `open`.

**Expected plot:** two summers and one winter, monthly means from about
3.7 °C (February–March 2013) to 20.0 °C (July 2013), with a daily cycle on
every day. A curve around 270–300 means the kelvin conversion is missing.

If `python` cannot find `xarray` or `netCDF4`:
`pip install --quiet matplotlib pandas netCDF4 xarray` — `pip`, not
`conda install`; see the callout in Chapter 6.

---

# Chapter 15. Run 2: KCL U-Surf

## Step 31. Copy Run 2 and see what differs

```bash
DATA_DIR="$HOME/jules-tutorial-data"
bash "$DATA_DIR/scripts/setup/get_run.sh" usurf

cd ~
diff -qr kcl_default/namelists kcl_usurf/namelists
```

`diff -qr` names the five files that differ:

| File | Default | U-Surf |
|---|---|---|
| `urban.nml` | `l_urban_empirical=.true.` | `.false.`: use the values in `ancillaries.nml` |
| `ancillaries.nml`, form | from the urban fraction 0.79: `hgt` 8.0 m, `hwr` 0.39, `wrr` 0.73 | KCL: `hgt` 27.5 m, `hwr` 1.50, `wrr` 0.50 |
| `ancillaries.nml`, materials | albedo 0.25, 0.08; emissivity 0.90, 0.95 | albedo 0.12, 0.10; emissivity 0.97, 0.97 |
| `ancillaries.nml`, frac file | canyon 0.58, roof 0.21 | canyon 0.39, roof 0.40 |
| `drive.nml` | `z1_tq_in = z1_uv_in = 74.1389` | `57.1836` |
| `initial_conditions.nml` | Default end-of-spin-up state | U-Surf end-of-spin-up state |
| `output.nml` | `run_id='kcl_default'` | `run_id='kcl_usurf'` |

The fractions differ because the canyon/roof split follows each
configuration's `wrr` (same urban total, 0.79); the frac files were
precomputed, and JULES reads canyon and roof directly. The forcing height
differs because `z1` is measured above the displacement height `d`, which
depends on the buildings: 78.2 − 4.1 = 74.1 m for Default and
78.2 − 21.0 = 57.2 m for U-Surf. The start state differs because each
configuration ran its own spin-up.

## Step 32. Run it

```bash
cd ~/kcl_usurf
~/jules_build/build/bin/jules.exe namelists/ 2>&1 | tee run.log
ls output
```

Expected: `kcl_usurf.hourly_output.nc` and three dump files, no
`[FATAL ERROR]`.

---

# Chapter 16. Compare Default and U-Surf

## Step 33. Run the comparison

```bash
DATA_DIR="$HOME/jules-tutorial-data"
python "$DATA_DIR/scripts/compare.py"
```

Expected:

```text
U-Surf - Default, all hours: -0.21 K
  daytime -0.27 K, night-time -0.14 K
  U-Surf is cooler in 98 % of hours
saved /home/ec2-user/kcl_default/compare.png
```

`compare.png` has three panels: (a) the daily mean of both runs, (b) the
hourly and daily U-Surf − Default difference with its mean, and (c) the
mean difference by hour of day (largest, about −0.34 K, around 13–14 UTC).

The key lines inside it:

```python
td = d["t1p5m_gb"].squeeze() - 273.15   # Run 1
tu = u["t1p5m_gb"].squeeze() - 273.15   # Run 2
diff = tu - td                          # U-Surf − Default, every hour
by_hour = diff.groupby("time.hour").mean()
```

This is a model-to-model comparison; observations are not evaluated here.

## Download your plots

From your **local machine**:

```bash
scp -i ~/Desktop/jules.pem "ec2-user@<your-ec2-ip>:kcl_default/*.png" ~/Desktop/
open ~/Desktop/compare.png
```

The quotes stop your laptop's shell (zsh on macOS) from expanding `*.png`
itself.

Run this on your laptop's terminal, not inside the SSH session — it's
copying files *from* EC2 *to* your machine.

## After class

- Add `'latent_heat'` (gridbox latent heat flux, W m⁻²) to `var` in
  `output.nml`, and change `nvars`, `output_type` and `var_name` together
  to 12; rerun and check that it is close to `fqw_gb` × 2.5 × 10⁶.
- Plot other variables (`ftl_gb`, `tstar_gb`, `rad_net`) for both runs.
- Compare both runs with the KCL tower measurements.
- Run the 40-cycle spin-up yourself: in `timesteps.nml`, set the
  `&jules_spinup` block back to a spin-up period and cycle count, and start
  from a constant initial state in `initial_conditions.nml`.
- Your own site: U-Surf values in `urban.nml`/`ancillaries.nml` and a frac
  file for that site.

Use **AI** to help, and **save the prompts you used**.

---

# Chapter 17. Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `Permission denied` on `ssh` | wrong username, key, or IP | double-check all three against Step 1 |
| `gfortran: command not found` | compiler not installed | `sudo dnf install gcc-gfortran` |
| `fcm: command not found` | FCM not on `PATH` | `export PATH=$HOME/fcm/bin:$PATH` |
| build fails with an MPI-interface compiler error | missing `JULES_FFLAGS_EXTRA` | re-export the full variable list in Chapter 9, Step 18–21, before rebuilding |
| `Cannot read module file '.../netcdf.mod'` | `netcdf-fortran` compiled by a newer gfortran | install the build in Chapter 6, `rm -rf ~/jules_build`, rebuild |
| `nf-config: command not found` | NetCDF-Fortran not installed / conda not activated | `source ~/miniforge3/bin/activate`, then Chapter 6 |
| `[FATAL ERROR]` naming a file at startup | wrong path in a namelist | `ls` the path named in the message; or `rm -rf ~/kcl_default` and rerun `get_run.sh default` (Chapter 11) |
| `get_run.sh`: `already exists` | the run directory is already there | `rm -rf ~/kcl_default` (or `~/kcl_usurf`) and rerun |
| run is fine, but an edit did nothing | edited a file JULES never opens | edit the fixed-name file (Chapter 11, Step 26) |
| `ModuleNotFoundError: xarray` | environment not loaded | `source ~/miniforge3/bin/activate` |
| temperatures around 290 | still in kelvin | subtract 273.15 |
| conda hangs or gets killed while installing | too many packages requested via `conda install` at once on a small instance | only ever `conda install` `netcdf-fortran` alone; get Python plotting packages via `pip` |
| out-of-memory during compile | no swap configured | Chapter 3 |

Check current memory/swap state any time with:

```bash
free -h
swapon --show
```

---

# Chapter 18. Checklist

After completing this lab, you should be able to:

- [ ] Explain what JULES is and what MORUSES adds to it
- [ ] Connect to the EC2 instance over SSH
- [ ] Create and verify swap memory
- [ ] Install NetCDF-Fortran without triggering the conda OOM issue
- [ ] Install FCM and build JULES from source
- [ ] Explain what each `JULES_*` build environment variable does
- [ ] Say what a KCL run needs: forcing, tile fractions, an urban description, a start state
- [ ] Name the seven main namelists and the fixed-name traps
- [ ] Start JULES on EC2 and tell from the log and the dump files that it worked
- [ ] Inspect NetCDF output with `ncdump` and `xarray`
- [ ] Plot `t1p5m_gb` and get a sensible-looking diurnal cycle
- [ ] List what differs between KCL Default and U-Surf, and compare their 1.5 m air temperature
- [ ] Diagnose the common failures in Chapter 17 without help

---

## Where the rest of this repo lives

```text
scripts/README.md         the same commands above, as copy-paste blocks in order
scripts/setup/            install.sh (= setup_ec2.sh + build_jules.sh), get_run.sh
scripts/quicklook.py      Run 1 plot (Chapter 14)
scripts/compare.py        Default vs U-Surf comparison (Chapter 16)
scripts/run/              run_jules.sh
scripts/postprocessing/   plot_quicklook.py, read_tile_output.py
scripts/preprocessing/    build_frac_file.py, prepare_era5_point_forcing.py
scripts/clearup/          clearup_ec2.sh
namelists/README.md       what a namelist is, and the seven files worth understanding
```

Full JULES documentation: [jules-lsm.github.io](https://jules-lsm.github.io/)
— the namelist reference there covers every option this lab didn't.

```text
enjoy your life and use AI
```
