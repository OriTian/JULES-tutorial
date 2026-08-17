#!/bin/bash
# One-time environment setup for building JULES on an Amazon Linux 2023 EC2
# instance (verified on a t3.micro: 913MB RAM, 2 vCPU, x86_64).
#
# Run this ONCE per instance, then see scripts/build/README.md for the
# actual build command.
set -e

echo "=== 1. Add 2GB swap (t3.micro has no swap by default, and only ~900MB RAM -- compiling will OOM without this) ==="
if ! swapon --show | grep -q swapfile; then
  sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
fi
free -h

echo "=== 2. System packages: compiler, git, make, and the perl modules FCM needs (not all present on a minimal AL2023 image) ==="
sudo dnf install -y git make gcc gcc-gfortran \
  perl-FindBin perl-File-Copy perl-File-Compare perl-Sys-Hostname \
  perl-IO-Compress perl-Digest-SHA perl-Text-Balanced perl-Time-Piece perl-filetest

echo "=== 3. Miniforge (conda-forge) -- AL2023's dnf repos have no netcdf-fortran package at all, so this is the practical way to get one that matches gfortran's ABI ==="
if [ ! -d "$HOME/miniforge3" ]; then
  curl -sL -o /tmp/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
  bash /tmp/miniforge.sh -b -p "$HOME/miniforge3"
fi
source "$HOME/miniforge3/bin/activate"
conda install -y -c conda-forge netcdf-fortran
nf-config --version

echo "=== 4. FCM (the build tool JULES uses) ==="
if [ ! -d "$HOME/fcm" ]; then
  git clone -q https://github.com/metomi/fcm.git "$HOME/fcm"
fi
"$HOME/fcm/bin/fcm" --version

echo "=== 5. JULES source (public read-only GitHub mirror, no registration needed) ==="
if [ ! -d "$HOME/jules_source" ]; then
  git clone -q --depth 1 https://github.com/MetOffice/jules.git "$HOME/jules_source"
fi

echo "=== 6. Python packages for reading/plotting output (matplotlib, pandas, netCDF4, xarray) ==="
echo "    Installed with pip, NOT conda/mamba install -- verified: conda's dependency"
echo "    solver OOM-kills on this instance's ~900MB RAM even with swap; pip (prebuilt"
echo "    wheels, no solving) installs the same packages cleanly in well under 200MB."
pip install --quiet matplotlib pandas netCDF4 xarray
python -c "import matplotlib, pandas, netCDF4, xarray; print('plotting stack OK:', matplotlib.__version__, pandas.__version__, netCDF4.__version__, xarray.__version__)"

echo "=== Setup complete. Add this to your ~/.bashrc: ==="
cat <<'EOF'

export PATH=$HOME/fcm/bin:$HOME/miniforge3/bin:$PATH
export JULES_PLATFORM=custom
export JULES_COMPILER=gfortran
export JULES_BUILD=normal
export JULES_OMP=noomp
export JULES_NETCDF=netcdf
export JULES_NETCDF_PATH=$HOME/miniforge3
export JULES_MPI=nompi
export JULES_FFLAGS_EXTRA="-fallow-argument-mismatch -Wno-error"
EOF

echo "Then build with: mkdir -p ~/jules_build && cd ~/jules_build && fcm make -f ~/jules_source/etc/fcm-make/make.cfg -j 1"
echo "(-j 1, not -j 4 -- this instance is too small for parallel compilation)"
echo "(JULES_FFLAGS_EXTRA is needed -- gfortran 11 is stricter than older versions about"
echo " argument-consistency checks and flags JULES's dummy MPI stub (utils/mpi_dummy/,"
echo " which deliberately has no explicit interface) as a hard error under -Werror,"
echo " even though it's harmless in practice. Verified: build completes cleanly with"
echo " these flags, producing a working ~55MB jules.exe.)"
