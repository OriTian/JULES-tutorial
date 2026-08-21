# JULES/MORUSES Urban Climate Modelling on EC2
---

# Chapter 1. Connect to EC2

## Learning Objective

Connect from a local computer to a remote EC2 Linux server.

```text
Local Computer
      ↓
SSH
      ↓
EC2 Instance
```

## Step 1. Check the information

You need:

```text
Public IP address
Username
Private key (.pem)
```

Example:

```text
54.xx.xx.xx
ec2-user
course-key.pem
```

## Step 2. Connect to EC2

```bash
ssh -i course-key.pem ec2-user@54.xx.xx.xx
```

### Purpose

Create a secure remote connection.

### Command breakdown

```text
ssh            Secure Shell
-i             identity file
course-key.pem private key
ec2-user       login account
54.xx.xx.xx    server IP
```

### Success indicator

```bash
❯ ssh -i "jules.pem" ec2-user@ec2-18-130-30-147.eu-west-2.compute.amazonaws.com
The authenticity of host 'ec2-18-130-30-147.eu-west-2.compute.amazonaws.com (18.130.30.147)' can't be established.
ED25519 key fingerprint is: SHA256:5NZ8f8ZXknpalfUBdCbjI+Wh0jV9HTNF2QwMLeUgaSU
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'ec2-18-130-30-147.eu-west-2.compute.amazonaws.com' (ED25519) to the list of known hosts.
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
** The server may need to be upgraded. See https://openssh.com/pq.html
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
    ~~~         /
      ~~._.   _/
         _/ _/
       _/m/'
[ec2-user@ip-172-31-46-208 ~]$
```

---

# Chapter 2. Understand the JULES Workflow

## What is JULES?

```text
Joint UK Land Environment Simulator
```

A land-surface model that simulates:

```text
Energy balance
Water balance
Carbon balance
Land-atmosphere exchange
```

```
Meteorology 
        ↓

     JULES

 ┌─────────────┐
 │ Radiation   │
 │ Heat Flux   │
 │ Soil Water  │
 │ Carbon      │
 └─────────────┘

        ↓

  Air Temperature
  Surface Temperature
  Sensible Heat
  Latent Heat

```

## What is MORUSES?

```text
Multi-layer Urban Surface Exchange Scheme
```

Urban representation inside JULES.

```text
Urban Roof Tile
Urban Canyon Tile

roof
-------|        |-------
       |        |
       | canyon |
       |--------|
```

---

# Chapter 3. Prepare Memory

## Why?

Small EC2 instances often run out of memory when compiling JULES.

## Step 3. Check memory

```bash
free -h
```

Look for:

```text
Mem
Swap
```

### Success indicator
```
               total        used        free      shared  buff/cache   available
Mem:           957Mi       161Mi       552Mi       0.0Ki       243Mi       663Mi
Swap:             0B          0B          0B

```

## Step 4. Create a 2 GB swap file

```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
```

### Input

```text
/dev/zero
```

### Output

```text
/swapfile
```

### Size

```text
2048 × 1 MB
=
2 GB
```

## Step 5. Enable swap

```bash
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Verify:

```bash
free -h
```

Expected:

```text
               total        used        free      shared  buff/cache   available
Mem:           957Mi       122Mi        83Mi       0.0Ki       751Mi       702Mi
Swap:          2.0Gi          0B       2.0Gi
```

---

# Chapter 4. Install Build Tools

## Step 6. Install GCC

```bash
sudo dnf install gcc
```

Purpose:

```text
Compile C libraries
```

## Step 7. Install GNU Fortran

```bash
sudo dnf install gcc-gfortran
```

Purpose:

```text
Compile JULES source code
```

Verify:

```bash
gfortran --version
```

## Step 8. Install Git, Make, and Perl

```bash
sudo dnf install -y git make \
  perl-FindBin perl-File-Copy perl-File-Compare perl-Sys-Hostname \
  perl-IO-Compress perl-Digest-SHA perl-Text-Balanced perl-Time-Piece perl-filetest
```

Purpose:

```text
git  → download code
make → build software
perl → read config
```

---

# Chapter 5. Install Miniforge

## Why?

To obtain:

```text
Conda
Python
NetCDF libraries
```

## Step 9. Download Miniforge

```bash
curl -L -o miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
```

## Step 10. Install Miniforge

```bash
bash miniforge.sh -b -p ~/miniforge3
```

Result:

```text
~/miniforge3
```

Expected:

```text
Linking conda-package-handling-2.4.0-pyh7900ff3_2
Linking conda-26.3.2-py313h78bf25f_1

Transaction finished

installation finished.
```

## Step 11. Activate Miniforge

```bash
source ~/miniforge3/bin/activate
```

Verify:

```bash
conda --version
```

---

# Chapter 6. Install NetCDF Fortran

## Why?

JULES reads:

```text
ERA5.nc
```

and writes:

```text
output.nc
```

## Step 12. Install NetCDF Fortran

```bash
conda install -y -c conda-forge netcdf-fortran xarray
```

## Step 13. Verify

```bash
nf-config --version
```

Expected:

```bash
$ nf-config --version                                                            
4.6.4 
```

---

# Chapter 7. Install FCM

## What is FCM?

```text
Flexible Configuration Management
```

JULES build system.

## Step 14. Download FCM

```bash
git clone https://github.com/metomi/fcm.git ~/fcm
```

## Step 15. Verify

```bash
~/fcm/bin/fcm --version
#FCM 2021.05.0-12-g3b045b3 (/home/ec2-user/fcm)
```

---

# Chapter 8. Download JULES

## Step 16. Clone JULES

```bash
git clone --depth 1 https://github.com/MetOffice/jules.git ~/jules_source
```

## Important folders

```text
src/       source code
etc/       build configuration
docs/      documentation
```

---

# Chapter 9. Build JULES

## Step 17. Activate environment

```bash
source ~/miniforge3/bin/activate
export PATH=$HOME/fcm/bin:$HOME/miniforge3/bin:$PATH
```

## Step 18. Select compiler

```bash
export JULES_COMPILER=gfortran
```

Meaning:

```text
Use GNU Fortran
```

## Step 19. Disable MPI

```bash
export JULES_MPI=nompi
```

Meaning:

```text
Single-process build
```

## Step 20. Disable OpenMP

```bash
export JULES_OMP=noomp
```

Meaning:

```text
No shared-memory parallelism
```

## Step 21. Enable NetCDF

```bash
export JULES_NETCDF=netcdf
export JULES_NETCDF_PATH=$HOME/miniforge3
```

Meaning:

```text
Read and write NetCDF files
```

## Step 22. Build the executable

```bash
mkdir -p ~/jules_build
cd ~/jules_build

fcm make -f ~/jules_source/etc/fcm-make/make.cfg -j 1
```

Internally:

```text
Fortran Source
      ↓
Object Files
      ↓
Link Libraries
      ↓
jules.exe
```

Expected:
```text
[info] sources: total=617, analysed=0, elapsed-time=0.1s, total-time=0.0s
[info] target-tree-analysis: elapsed-time=0.8s
[info] compile   targets: modified=7, unchanged=485, failed=0, total-time=52.0s
[info] compile+  targets: modified=6, unchanged=484, failed=0, total-time=0.1s
[info] install   targets: modified=0, unchanged=1, failed=0, total-time=0.0s
[info] link      targets: modified=1, unchanged=0, failed=0, total-time=0.9s
[info] TOTAL     targets: modified=14, unchanged=970, failed=0, elapsed-time=55.1s
[done] make build          # 55.2s
[done] make                # 55.7s
```

## Step 23. Verify compilation

```bash
ls ~/jules_build/build/bin/jules.exe
```

Expected:

```text
jules.exe
```

---

# Chapter 10. Download Tutorial Data

## Step 24. Download tutorial repository

```bash
RUN_DIR="${RUN_DIR:-$HOME/my_first_run}"
TMP_TAR="/tmp/jules-tutorial-data.tar.gz"
TMP_DIR="/tmp/jules-tutorial-data"

wget -q -O "$TMP_TAR" https://github.com/OriTian/JULES-tutorial/archive/refs/heads/main.tar.gz
rm -rf "$TMP_DIR" && mkdir -p "$TMP_DIR"
tar -xzf "$TMP_TAR" -C "$TMP_DIR" --strip-components=1
```

Breakdown:

- `wget` downloads a remote file.
- `-q` reduces output.
- `-O "$TMP_TAR"` writes the download to the selected filename.
- The URL provides a compressed archive of the `main` branch.

Repository structure:

```text
ancillary_data/
forcing_data/
namelists/
```

### forcing_data

```text
Meteorological forcing
```

### namelists

```text
Model configuration
```

---

# Chapter 11. Prepare Run Directory

## Step 25. Create working directory

```bash
mkdir -p "$RUN_DIR"
```

Purpose:

```text
Keep tutorial files unchanged
```

## Step 26. Copy London StJamesPark case

```
cp -r "$TMP_DIR/namelists/London_StJamesPark" "$RUN_DIR/namelists"
mkdir -p "$RUN_DIR/output"   # JULES does not create this itself
```

expected:
```text
London_StJamesPark
      ↓
~/my_first_run/namelists
```

## Step 27. Create output directory

```bash
mkdir -p ~/my_first_run/output
```



---

# Chapter 12. Run JULES

## Step 28. Start the model

```bash
RUN_DIR="${RUN_DIR:-$HOME/my_first_run}"
cd "$RUN_DIR"
mkdir -p output   # JULES does not create this itself
${JULES_EXE:-$HOME/jules_build/build/bin/jules.exe} namelists/
```

What happens?

```text
Read namelists
      ↓
Read forcing
      ↓
Initialise state variables
      ↓
Time integration
      ↓
Write NetCDF output
```

## Success indicator

Output files appear in:

```text
output/
```

expected:
```
[INFO] WRITE_DUMP: sathh
[INFO] WRITE_DUMP: satcon
[INFO] WRITE_DUMP: sm_sat
[INFO] WRITE_DUMP: sm_crit
[INFO] WRITE_DUMP: sm_wilt
[INFO] WRITE_DUMP: hcap
[INFO] WRITE_DUMP: hcon
[INFO] WRITE_DUMP: albsoil
[INFO] WRITE_DUMP: frac_agr
[INFO] WRITE_DUMP: co2_mmr
[INFO] WRITE_DUMP: latitude
[INFO] WRITE_DUMP: longitude
[INFO] file_ncdf_close: Closing file output/my_first_run.dump.20230731.82800.nc
[INFO] file_ncdf_close: Closing file /tmp/jules-tutorial-data/forcing_data/London_StJamesPark_era5_2022_10-2023_12.nc
[INFO] file_ncdf_close: Closing file output/my_first_run.hourly_output.nc
```
---

# Chapter 13. Verify Output

## Step 29. Check files

```bash
ls output
```

Typical output:

```text
ls output
my_first_run.dump.20230301.0.nc  my_first_run.dump.20230731.82800.nc  my_first_run.hourly_output.nc
```

## Step 30. Inspect NetCDF structure

```bash
ncdump -h output/file.nc
```

Look for:

```text
dimensions
variables
units
time
```

---

# Chapter 14. Read Model Output in Python

## Step 31. Open NetCDF

set python environment
```bash
pip install --quiet matplotlib pandas netCDF4 xarray
```

In python
```python
import xarray as xr

ds = xr.open_dataset('output.nc')
```

Meaning:

```text
Load JULES output
```

## Step 32. Explore contents

```python
print(ds)
```

Look at:

```text
Dimensions
Coordinates
Variables
```

---

# Chapter 15. Plot Air Temperature

## Step 33. Plot t1p5m_gb

```python
ds['t1p5m_gb'].plot()
```

Meaning:

```text
1.5 m air temperature
```

If units are Kelvin:

```python
ds['t1p5m_gb'] - 273.15
```

Convert to Celsius.

---

# Chapter 16. Your tasks 

Use **AI** to help and **save the prompt that you used**.

## Task 1: Explore Output Variables

Instructions: Activate conda, start Python, load the output file, and answer the questions.

```
source ~/miniforge3/bin/activate
python
```

Q1: How many variables are in the output file?

Q2: How many time steps (hours) are in the output?


## Task 2: Plot Radiation Components
Instructions: Use Python to plot and compare shortwave and longwave radiation.

Variables
```
'sw_down','lw_down','rad_net'
```

## Task 3: Modify Urban Emissivity
Instructions: Edit the urban properties file `ancillaries.nml`, rerun the model, and compare results.

Modify the 'emisw','emisr' to 0.98
```
&urban_properties
  nvars=7
  use_file=7*.false.
  var='wrr','hwr','hgt','albwl','albrd','emisw','emisr'
  const_val=0, 0, 0, 0.25, 0.08, 0.90, 0.95
/
```

rerun model and plot the temperature and radiation components

```
Question:

Urban emissivity:
0.95 → 0.98

Do you expect:

A) Higher roof temperature

B) Lower roof temperature

C) No change
```

## Download the plots, and share your plots and AI prompts

```
# Download to your local machine
scp -i your-key.pem ec2-user@your-ec2-ip:~/my_first_run/*.png ~/Downloads/
```

You may do more experiments.

---

# Chapter 17. Common Errors

## SSH Failure

```text
Permission denied
```

Check:

```text
Username
Private key
IP address
```

## Compiler Missing

```text
gfortran: command not found
```

Install:

```bash
sudo dnf install gcc-gfortran
```

## FCM Missing

```text
fcm: command not found
```

Check:

```bash
export PATH=$HOME/fcm/bin:$PATH
```

## NetCDF Not Found

Check:

```bash
nf-config --version
```

## Memory Problems

Check:

```bash
free -h
swapon --show
```

---

# Chapter 18. Student Checklist

After completing the practical, students should be able to:

- Explain what JULES is
- Explain what MORUSES is
- Connect to EC2 using SSH
- Create and verify swap memory
- Install NetCDF Fortran
- Install FCM
- Compile JULES
- Prepare a run directory
- Run the London St James's Park example
- Inspect NetCDF output
- Plot t1p5m_gb
- Diagnose common model failures

---

# Final Remark

```text
enjoy your life and use AI
```
