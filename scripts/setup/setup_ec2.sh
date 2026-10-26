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
# build _100 was compiled with gfortran 14; conda-forge builds since Sept 2026 use
# gfortran 15, whose netcdf.mod the system gfortran 11 cannot read
conda install -y -c conda-forge "netcdf-fortran=4.6.4=nompi_*_100"

# 4. FCM
[ -d "$HOME/fcm" ] || git clone -q https://github.com/metomi/fcm.git "$HOME/fcm"

# 5. JULES source
# vn8.1: the JULES version the tutorial namelists were tested with. Another
# version in ~/jules_source is replaced, and its build directory removed.
JULES_REF=vn8.1
if [ "$(cat "$HOME/jules_source/.tutorial_ref" 2>/dev/null)" != "$JULES_REF" ]; then
  rm -rf "$HOME/jules_source" "$HOME/jules_build"
  git -c advice.detachedHead=false clone -q --depth 1 --branch "$JULES_REF" \
    https://github.com/MetOffice/jules.git "$HOME/jules_source"
  echo "$JULES_REF" > "$HOME/jules_source/.tutorial_ref"
fi

# 6. Python plotting/analysis stack -- pip, not conda (see README.md)
pip install --quiet matplotlib pandas netCDF4 xarray

echo "Setup complete. Next: scripts/setup/build_jules.sh"
