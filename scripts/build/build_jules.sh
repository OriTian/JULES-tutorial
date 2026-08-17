#!/bin/bash
# Builds JULES after setup_ec2_amazonlinux.sh has been run once.
# See README.md in this directory for what each variable/flag does and why.
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
