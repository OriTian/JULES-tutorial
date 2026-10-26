#!/bin/bash
# Everything a new EC2 instance needs for the tutorial, in one go:
# setup_ec2.sh (swap, compiler, Miniforge + netcdf-fortran, FCM, JULES source,
# Python packages), then build_jules.sh (compile jules.exe).
# Run it once per instance, in the background, so that a dropped SSH
# connection does not stop it:
#   nohup bash ~/jules-tutorial-data/scripts/setup/install.sh > ~/install.log 2>&1 &
#   tail -n 3 ~/install.log      # progress; the last line says INSTALL DONE when finished
# Safe to rerun after a failure: finished steps are skipped.
set -e

# one install at a time: a second copy (e.g. the line pasted twice) stops here
exec 9> "$HOME/.install.lock"
if ! flock -n 9; then
  echo "install.sh is already running: wait for it (tail -n 3 ~/install.log)"
  exit 1
fi
trap 'echo "INSTALL FAILED: read the lines above, then rerun install.sh"' ERR

HERE="$(cd "$(dirname "$0")" && pwd)"
START=$(date +%s)
echo "install.sh started $(date)"

bash "$HERE/setup_ec2.sh"
echo "== setup done after $(( ($(date +%s) - START) / 60 )) min; building JULES"
bash "$HERE/build_jules.sh"

source "$HOME/miniforge3/bin/activate"
python -c "import xarray, matplotlib, netCDF4; print('Python packages OK')"
echo "INSTALL DONE in $(( ($(date +%s) - START) / 60 )) min"
