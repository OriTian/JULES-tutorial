# Urban U-Surf template (advanced / optional)

Same as `urban_default/`, except:

- `urban.nml`: set `l_urban_empirical=.false.`
- `ancillaries.nml`: `const_val` for `wrr`/`hwr`/`hgt` are then **used directly** (not overridden) — fill in real measured values for your site from the [U-Surf dataset](https://zenodo.org/) or a field survey, instead of `0, 0, 0`.

Everything else (`ancillaries.nml`'s `&jules_frac` block, `drive.nml`, `timesteps.nml`, `output.nml`) is unchanged from `urban_default/`.

Start with `urban_default/` unless you specifically need real per-site geometry rather than the UKV empirical estimate.
