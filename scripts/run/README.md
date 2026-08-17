# Running JULES

Requires JULES already built — see `scripts/setup/README.md`.

```bash
cd my_run_directory/
bash ~/jules-urban-workflow/scripts/run/run_jules.sh
```

Or by hand:

```bash
cd my_run_directory/
mkdir -p output   # JULES does not create this itself
~/jules_build/build/bin/jules.exe namelists/
```

No job scheduler, no queue — it just runs and writes to `output/` when done.
Set `JULES_EXE` to override the default `jules.exe` path
(`$HOME/jules_build/build/bin/jules.exe`).
