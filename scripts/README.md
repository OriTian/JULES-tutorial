# Scripts

## Where to start

This folder has four subfolders plus this file. If you're new here, open
them in this order:

1. **`setup/README.md`** first — explains the EC2 build environment, why
   each package/env-var is needed, and what `setup_ec2.sh`,
   `build_jules.sh`, and `get_run.sh` each do.
2. **`run/README.md`** next — explains `run_jules.sh`, i.e. actually
   running the model once you have a build and a run directory.
3. **`quicklook.py`** and **`compare.py`** (in this folder) — the Run 1
   plot and the Default vs U-Surf comparison; **`postprocessing/README.md`**
   explains two more general helpers, `plot_quicklook.py` and
   `read_tile_output.py`.
4. **`preprocessing/`** last, and only if you need it — `build_frac_file.py`
   and `download_era5.py` build the tile-fraction and forcing inputs for a
   *new* site. Skip this on a first pass; the tutorial's site (KCL)
   already ships with these files pre-built in `forcing_data/`,
   `ancillary_data/` and `initial_state/`.

Once you've read those and understand what each step does, come back to
**this file** — it's the fast path: the same four steps (build,
get-a-run-directory, run, plot) as ready-to-paste shell blocks, with no
detours through the explanations above.

## Copy in this order

Each block below is complete and self-contained — copy the whole block,
paste it into the EC2 terminal, done. No need to open any other file.
(The one exception is JULES's own source code, which step 1's script
fetches with `git clone` — that's a real external dependency, not part of
this repo.)

## 1. Environment setup

```bash
cat > ~/setup_ec2.sh << 'EOF'
#!/bin/bash
# One-time environment setup for building JULES on the group's EC2 instance.
# See setup/README.md in this repo for what each step does and why.
set -e

# 1. swap
swapon --show | grep -q swapfile || {
  sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
}

# 2. compiler, git, make, perl modules FCM needs
sudo dnf install -y git make gcc gcc-gfortran \
  perl-FindBin perl-File-Copy perl-File-Compare perl-Sys-Hostname \
  perl-IO-Compress perl-Digest-SHA perl-Text-Balanced perl-Time-Piece perl-filetest

# 3. Miniforge, for netcdf-fortran
[ -d "$HOME/miniforge3" ] || {
  curl -sL -o /tmp/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
  bash /tmp/miniforge.sh -b -p "$HOME/miniforge3"
}
source "$HOME/miniforge3/bin/activate"
conda install -y -c conda-forge netcdf-fortran

# 4. FCM
[ -d "$HOME/fcm" ] || git clone -q https://github.com/metomi/fcm.git "$HOME/fcm"

# 5. JULES source
[ -d "$HOME/jules_source" ] || git clone -q --depth 1 https://github.com/MetOffice/jules.git "$HOME/jules_source"

# 6. Python plotting/analysis stack -- pip, not conda (see setup/README.md)
pip install --quiet matplotlib pandas netCDF4 xarray

echo "Setup complete. Next: build_jules.sh"
EOF
bash ~/setup_ec2.sh
```

## 2. Build JULES

```bash
cat > ~/build_jules.sh << 'EOF'
#!/bin/bash
# Builds JULES after setup_ec2.sh has been run once.
# See setup/README.md in this repo for what each variable/flag does and why.
set -e

source ~/miniforge3/bin/activate
export PATH=$HOME/fcm/bin:$HOME/miniforge3/bin:$PATH
export JULES_PLATFORM=custom
export JULES_COMPILER=gfortran
export JULES_BUILD=normal
export JULES_OMP=noomp
export JULES_NETCDF=netcdf
export JULES_NETCDF_PATH=$HOME/miniforge3
export JULES_MPI=nompi
export JULES_FFLAGS_EXTRA="-fallow-argument-mismatch -Wno-error"

mkdir -p ~/jules_build && cd ~/jules_build
fcm make -f ~/jules_source/etc/fcm-make/make.cfg -j 1

ls -la ~/jules_build/build/bin/jules.exe
EOF
bash ~/build_jules.sh
```

## 3. Get the two KCL run directories

```bash
DATA_DIR="$HOME/jules-tutorial-data"
bash "$DATA_DIR/scripts/setup/get_run.sh" default    # Run 1 -> ~/kcl_default
bash "$DATA_DIR/scripts/setup/get_run.sh" usurf      # Run 2 -> ~/kcl_usurf
diff -qr ~/kcl_default/namelists ~/kcl_usurf/namelists
```

`get_run.sh` downloads this repo into `~/jules-tutorial-data` the first
time; see `setup/get_run.sh` for what it does.

## 4. Run JULES

```bash
cd ~/kcl_default && ~/jules_build/build/bin/jules.exe namelists/ 2>&1 | tee run.log
cd ~/kcl_usurf   && ~/jules_build/build/bin/jules.exe namelists/ 2>&1 | tee run.log
```

## 5. Plot and compare

```bash
source ~/miniforge3/bin/activate
DATA_DIR="$HOME/jules-tutorial-data"
python "$DATA_DIR/scripts/quicklook.py"   # -> ~/kcl_default/run1_t1p5m.png
python "$DATA_DIR/scripts/compare.py"     # -> ~/kcl_default/compare.png
```

See `setup/README.md`, `run/README.md`, `postprocessing/README.md` for
what each step does and why — this file is just the copy-paste blocks in
order.

---

[Back to main tutorial](../README.md)
