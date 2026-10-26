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
        tile_vals = np.ma.filled(ds.variables[var][:], np.nan) 
        gb_vals = np.ma.filled(ds.variables[f"{var}_gb"][:, 0, 0], np.nan) - 273.15

        canyon = tile_vals[:, canyon_idx, 0, 0] - 273.15
        roof = tile_vals[:, roof_idx, 0, 0] - 273.15

        out[f"{var}_gb"] = pd.Series(gb_vals, index=t)
        out[f"{var}_canyon"] = pd.Series(canyon, index=t)
        out[f"{var}_roof"] = pd.Series(roof, index=t)
        # Surface temperature only: canyon and roof t1p5m are kept apart, because
        # a fraction-weighted mean of them is not an urban 1.5 m air temperature.
        if var == "tstar":
            urban_only = (canyon_frac * canyon + roof_frac * roof) / (canyon_frac + roof_frac)
            out[f"{var}_urban_only"] = pd.Series(urban_only, index=t)

    ds.close()
    return out


if __name__ == "__main__":
    data = load_output(
        "output/kcl_default.hourly_output.nc",
        canyon_idx=8, roof_idx=9,               # tiles 9 and 10 in jules_surface_types.nml
        canyon_frac=0.5782, roof_frac=0.2118,   # KCL Default frac file
    )
    print("Gridbox-mean vs urban-only mean tstar (°C):")
    print(f"  _gb:         {data['tstar_gb'].mean():.2f}")
    print(f"  urban_only:  {data['tstar_urban_only'].mean():.2f}")
