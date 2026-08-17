set -e

mkdir -p output  
${JULES_EXE:-$HOME/jules_build/build/bin/jules.exe} namelists/
