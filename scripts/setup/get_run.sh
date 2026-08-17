set -e

RUN_DIR="${RUN_DIR:-$HOME/my_first_run}"

git clone --depth 1 https://github.com/OriTian/JULES-tutorial.git ~/jules-tutorial-data
mkdir -p "$RUN_DIR"
cp -r ~/jules-tutorial-data/namelists/London_StJamesPark "$RUN_DIR/namelists"
mkdir -p "$RUN_DIR/output"   # JULES does not create this itself

FRAC_FILE=$(find ~/jules-tutorial-data -iname "*frac*.nc" | head -1)
FORCING_FILE=$(find ~/jules-tutorial-data -iname "*era5*.nc" | head -1)
sed -i "s|file='.*frac.*\.nc'|file='$FRAC_FILE'|" "$RUN_DIR/namelists/ancillaries.nml"
sed -i "s|file='.*era5.*\.nc'|file='$FORCING_FILE'|" "$RUN_DIR/namelists/drive.nml"

echo "Run directory ready: $RUN_DIR"
echo "Namelist file count (should be ~41):"
ls "$RUN_DIR/namelists" | wc -l
