import argparse
import numpy as np
import netCDF4 as nc

TILE_NAMES = ["brd_leaf", "ndl_leaf", "c3_grass", "c4_grass", "shrub",
              "lake", "soil", "ice", "urban_canyon", "urban_roof"]


def build_frac(out_path, fractions):
    assert len(fractions) == 10, "need exactly 10 tile fractions"
    assert abs(sum(fractions) - 1.0) < 1e-6, f"fractions sum to {sum(fractions)}, must be 1.0"

    with nc.Dataset(out_path, "w") as ds:
        ds.createDimension("tile", 10)
        ds.createDimension("y", 1)
        ds.createDimension("x", 1)
        v = ds.createVariable("frac", "f8", ("tile", "y", "x"))
        v[:] = np.array(fractions).reshape(10, 1, 1)
        v.tile_order = ", ".join(TILE_NAMES)
    print(f"Saved: {out_path}")
    for name, frac in zip(TILE_NAMES, fractions):
        if frac > 0:
            print(f"  {name}: {frac}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("out_path")
    p.add_argument("fractions", type=float, nargs=10,
                    help="10 values in TILE_NAMES order, summing to 1.0")
    args = p.parse_args()
    build_frac(args.out_path, args.fractions)
