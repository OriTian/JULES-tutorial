#!/bin/bash
# One-time environment setup for building JULES on the group's EC2 instance.
# See README.md in this directory for what each step does and why.
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

# 6. Python plotting/analysis stack -- pip, not conda (see README.md)
pip install --quiet matplotlib pandas netCDF4 xarray

echo "Setup complete. Next: scripts/setup/build_jules.sh"
