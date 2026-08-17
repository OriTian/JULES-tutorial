import numpy as np
import pandas as pd
import netCDF4 as nc


def load_output(nc_path, canyon_idx, roof_idx, canyon_frac, roof_frac):
    ds = nc.Dataset(nc_path)
    t = pd.to_datetime(nc.num2date(
        ds.variables["time"][:], ds.variables["time"].units,
        only_use_cftime_datetimes=False, only_use_python_datetimes=True))

    out = {}
    for var in ("tstar", "t1p5m"):
        if var not in ds.variables:
            continue
        tile_vals = np.ma.filled(ds.variables[var][:], np.nan)  # [time, ntile, 1, 1]
        gb_vals = np.ma.filled(ds.variables[f"{var}_gb"][:, 0, 0], np.nan) - 273.15

        canyon = tile_vals[:, canyon_idx, 0, 0] - 273.15
        roof = tile_vals[:, roof_idx, 0, 0] - 273.15
        urban_frac = canyon_frac + roof_frac
        urban_only = (canyon_frac * canyon + roof_frac * roof) / urban_frac

        out[f"{var}_gb"] = pd.Series(gb_vals, index=t)
        out[f"{var}_canyon"] = pd.Series(canyon, index=t)
        out[f"{var}_roof"] = pd.Series(roof, index=t)
        out[f"{var}_urban_only"] = pd.Series(urban_only, index=t)

    ds.close()
    return out


if __name__ == "__main__":
    data = load_output(
        "output/my_run.hourly_output.nc",
        canyon_idx=8, roof_idx=9,       # from THIS run's jules_surface_types.nml
        canyon_frac=0.36, roof_frac=0.41,  # from THIS run's frac.nc
    )
    print("Gridbox-mean vs urban-only monthly mean tstar (°C):")
    print(f"  _gb:         {data['tstar_gb'].mean():.2f}")
    print(f"  urban_only:  {data['tstar_urban_only'].mean():.2f}")
