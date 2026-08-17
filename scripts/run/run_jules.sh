#!/bin/bash
# Run JULES locally -- no scheduler needed, a single-point/few-month run
# finishes in minutes.
set -e

mkdir -p output   # JULES does not create this itself
${JULES_EXE:-$HOME/jules_build/build/bin/jules.exe} namelists/
