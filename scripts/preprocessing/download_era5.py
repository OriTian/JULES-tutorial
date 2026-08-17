"""
Download and process ERA5 forcing for ONE point, no JASMIN account needed --
just a free Copernicus CDS account.

Setup (one-time, on your own machine or JASMIN, doesn't matter which):
  1. Register: https://cds.climate.copernicus.eu/
  2. Get your API key: https://cds.climate.copernicus.eu/how-to-api
  3. pip install cdsapi

Usage:
  python download_era5.py --lat 53.4808 --lon -2.2426 \
      --start 2013-02-01 --end 2013-07-31 --out my_site_forcing.nc

Downloads a small box (~0.25 degrees) around your point rather than a single
exact coordinate -- CDS doesn't support point requests -- then picks the
nearest grid cell locally. The box is small enough that a few months of
hourly data is a few tens of MB, not the multi-GB size of a full-UK request.
"""
import argparse
import numpy as np
import xarray as xr
import cdsapi


def download_raw(lat, lon, start, end, raw_path, pad=0.25):
    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "surface_pressure",
            "total_precipitation",
            "surface_solar_radiation_downwards",
            "surface_thermal_radiation_downwards",
        ],
        "date": f"{start}/{end}",
        "time": [f"{h:02d}:00" for h in range(24)],
        "data_format": "netcdf",
        "download_format": "unarchived",
        # [North, West, South, East] -- a small box around the point
        "area": [lat + pad, lon - pad, lat - pad, lon + pad],
    }
    client = cdsapi.Client()
    client.retrieve(dataset, request).download(raw_path)


def accum_to_hourly(da):
    diff = da.diff("valid_time")
    first = da.isel(valid_time=slice(0, 1))
    result = xr.concat([first, diff], dim="valid_time")
    return result.clip(min=0)  # accumulation resets at 00 UTC each day


def process_to_point(raw_path, lat, lon, out_path):
    ds = xr.open_dataset(raw_path)
    point = ds.sel(latitude=lat, longitude=lon, method="nearest")

    wind = np.sqrt(point["u10"] ** 2 + point["v10"] ** 2)

    d2m, sp = point["d2m"], point["sp"]
    e = 611.2 * np.exp(17.67 * (d2m - 273.15) / (d2m - 29.65))
    q = 0.622 * e / (sp - 0.378 * e)

    ssrd = accum_to_hourly(point["ssrd"])
    strd = accum_to_hourly(point["strd"])
    tp = accum_to_hourly(point["tp"]) * 1000.0 / 3600.0  # m/hr -> kg m-2 s-1

    out = xr.Dataset({
        "Tair": point["t2m"],
        "Qair": q,
        "Wind": wind,
        "Pstar": sp,
        "SwDown": ssrd,
        "LwDown": strd,
        "Precip": tp,
    }).rename({"valid_time": "time"})
    out.to_netcdf(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    p.add_argument("--start", required=True, help="YYYY-MM-DD")
    p.add_argument("--end", required=True, help="YYYY-MM-DD")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    raw_path = args.out.replace(".nc", "_raw.nc")
    download_raw(args.lat, args.lon, args.start, args.end, raw_path)
    process_to_point(raw_path, args.lat, args.lon, args.out)
