sudo swapoff /swapfile 2>/dev/null
sudo rm -f /swapfile

rm -rf ~/miniforge3 ~/fcm ~/jules_source ~/jules_build

rm -rf ~/my_first_run /tmp/jules-tutorial-data /tmp/jules-tutorial-data.tar.gz

rm -f ~/setup_ec2.sh ~/build_jules.sh ~/get_run_directory.sh ~/run_jules.sh ~/plot_quicklook.py \
      ~/download_era5.py ~/build_frac_file.py \
      ~/London_StJamesPark_era5_2022_10-2023_12.nc \
      ~/London_StJamesPark_frac.nc \
      ~/London_StJamesPark_midas_tair_2020_2023.nc \
      ~/.cdsapirc

cd ~

echo "=== home ==="
ls -la ~/
echo "=== swap ==="
swapon --show
free -h
