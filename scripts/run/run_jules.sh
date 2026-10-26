#!/bin/bash
# Run JULES in one run directory -- no scheduler needed, the KCL run finishes
# in a minute or two. Safe to run from anywhere: it cds into RUN_DIR itself.
#   bash run_jules.sh                       # ~/kcl_default
#   RUN_DIR=~/kcl_usurf bash run_jules.sh
set -e

RUN_DIR="${RUN_DIR:-$HOME/kcl_default}"
cd "$RUN_DIR"
mkdir -p output   # JULES does not create this itself
${JULES_EXE:-$HOME/jules_build/build/bin/jules.exe} namelists/ 2>&1 | tee run.log
