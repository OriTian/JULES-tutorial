import argparse
import numpy as np
import xarray as xr


def extract_point(era5_path, out_path, lat, lon):
    ds = xr.open_dataset(era5_path)
    point = ds.interp(latitude=lat, longitude=lon) 

    rename_map = {
        "ssrd": "SwDown", "strd": "LwDown", "t2m": "Tair",
        "sp": "Pstar", "tp": "Precip",
    }
    point = point.rename({k: v for k, v in rename_map.items() if k in point})

    if "u10" in point and "v10" in point:
        point["Wind"] = np.sqrt(point["u10"] ** 2 + point["v10"] ** 2)

    point.attrs["source"] = f"ERA5 bilinearly interpolated to {lat},{lon}"
    point.to_netcdf(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("era5_path")
    p.add_argument("out_path")
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    args = p.parse_args()
    extract_point(args.era5_path, args.out_path, args.lat, args.lon)
