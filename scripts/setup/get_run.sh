#!/bin/bash
# Set up one of the tutorial's KCL runs:
#   bash get_run.sh default    Run 1, KCL Default  -> ~/kcl_default
#   bash get_run.sh usurf      Run 2, KCL U-Surf   -> ~/kcl_usurf
#   bash get_run.sh london     older London St James's Park example -> ~/london_stjamespark
# Data live in $HOME/jules-tutorial-data, not /tmp: on Amazon Linux 2023 /tmp is a
# RAM-backed tmpfs (capped at half the memory) and is emptied on reboot. Only the
# download archive goes in /tmp. The absolute paths of the input files
# (e.g. /home/ec2-user/jules-tutorial-data/...) are written into the namelists.
set -e

CASE="$1"
DATA_DIR="${DATA_DIR:-$HOME/jules-tutorial-data}"
TMP_TAR="/tmp/jules-tutorial-data.tar.gz"
FORCING="forcing_data/UK-KingsCollege_era5_ml134_point_forcing_201103-201401.nc"

case "$CASE" in
  default)
    NML=KCL_Default
    FRAC="ancillary_data/UK-KingsCollege_default_frac.nc"
    INIT="initial_state/UK-KingsCollege_default_spinup_end_20120401.nc" ;;
  usurf)
    NML=KCL_USurf
    FRAC="ancillary_data/UK-KingsCollege_usurf_frac.nc"
    INIT="initial_state/UK-KingsCollege_usurf_spinup_end_20120401.nc" ;;
  london)
    NML=London_StJamesPark
    FORCING="forcing_data/London_StJamesPark_era5_2022_10-2023_12.nc"
    FRAC="ancillary_data/London_StJamesPark_frac.nc"
    INIT="" ;;
  *)
    echo "usage: bash get_run.sh default|usurf|london" >&2
    exit 1 ;;
esac
if [ "$CASE" = london ]; then RUN_DIR="$HOME/london_stjamespark"; else RUN_DIR="$HOME/kcl_$CASE"; fi

if [ ! -d "$DATA_DIR/namelists/$NML" ]; then
  curl -fsSL -o "$TMP_TAR" https://github.com/OriTian/JULES-tutorial/archive/main.tar.gz
  mkdir -p "$DATA_DIR"
  tar -xzf "$TMP_TAR" -C "$DATA_DIR" --strip-components=1
fi

if [ -e "$RUN_DIR" ]; then
  echo "$RUN_DIR already exists: to start again, rm -rf $RUN_DIR and rerun" >&2
  exit 1
fi
mkdir -p "$RUN_DIR/output"   # JULES does not create this itself
cp -r "$DATA_DIR/namelists/$NML" "$RUN_DIR/namelists"
rm -f "$RUN_DIR/namelists/README.md"

# the namelists name each input file as '/path/to/<file name>'
set_path() {   # set_path <namelist file> <data file>
  sed -i "s|file='/path/to/$(basename "$2")'|file='$DATA_DIR/$2'|" "$RUN_DIR/namelists/$1"
  grep -q "file='$DATA_DIR/$2'" "$RUN_DIR/namelists/$1" || { echo "could not set $2 in $1" >&2; exit 1; }
}
set_path drive.nml "$FORCING"
set_path ancillaries.nml "$FRAC"
[ -n "$INIT" ] && set_path initial_conditions.nml "$INIT"

echo "Run directory ready: $RUN_DIR"
grep -h "file='/" "$RUN_DIR/namelists/drive.nml" "$RUN_DIR/namelists/ancillaries.nml" "$RUN_DIR/namelists/initial_conditions.nml" | sed 's/^ *//'
echo "Namelist files: $(ls "$RUN_DIR/namelists" | wc -l)"
