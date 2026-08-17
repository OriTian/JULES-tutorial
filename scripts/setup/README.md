# Setting up and building JULES on the group's EC2 instance

No JASMIN account needed. The group has a small AWS EC2 instance
(Amazon Linux 2023, t3.micro) set up for this — ask in the group for the
`.pem` key and the instance's public DNS name.

## 1. Connect

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<instance-public-dns>
```

## 2. One-time environment setup

`jules-urban-workflow` isn't on GitHub yet, so paste `setup_ec2.sh`'s
contents directly into the terminal rather than copying the file over — see
`docs/running_on_ec2.md` §2 for the exact paste-able block. Then:

```bash
bash ~/setup_ec2.sh
```

Installs, in order: 2GB swap (the instance only has ~900MB RAM), `gfortran`
+ `git` + `make` + the perl modules FCM needs, `netcdf-fortran` via
Miniforge/conda-forge (not in AL2023's own `dnf` repos), FCM itself, the
JULES source (public read-only mirror, no registration needed), and
`matplotlib`/`pandas`/`netCDF4`/`xarray` via **`pip`, not `conda install`**
— conda's dependency solver OOM-kills on this instance even with swap; pip
(prebuilt wheels) doesn't. Use `pip install` for any future Python packages
too.

Safe to re-run — every step skips work that's already done. **Verified
end-to-end**, including the full build below.

## 3. Build

```bash
bash ~/jules-urban-workflow/scripts/setup/build_jules.sh
```

Sets the `JULES_*` env vars (`custom` platform — JULES ships configs for
JASMIN/Met Office clusters but not a plain EC2 box, so `custom` reads these
vars instead of assuming a specific module system), then runs `fcm make -j
1` (not `-j 4` — too little RAM for parallel compilation). Takes ~1 minute
for all 617 source files. Executable ends up at
`~/jules_build/build/bin/jules.exe` (~55MB).

Includes `JULES_FFLAGS_EXTRA="-fallow-argument-mismatch -Wno-error"` —
needed because gfortran 11 (on this instance) enforces stricter
argument-consistency checks than older versions and flags JULES's dummy MPI
stub (`utils/mpi_dummy/`, deliberately interface-free) as a hard error under
`-Werror`. Harmless in practice; these flags downgrade it back to a
warning. **Verified**: build completes cleanly and produces a working
`jules.exe`.

Once built, see `scripts/run/README.md` for running JULES.
