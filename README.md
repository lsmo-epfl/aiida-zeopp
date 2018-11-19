[![Build Status](https://travis-ci.org/ltalirz/aiida-zeopp.svg?branch=master)](https://travis-ci.org/ltalirz/aiida-zeopp)
[![Coverage Status](https://coveralls.io/repos/github/ltalirz/aiida-zeopp/badge.svg?branch=master)](https://coveralls.io/github/ltalirz/aiida-zeopp?branch=master)
[![Docs status](https://readthedocs.org/projects/aiida-zeopp/badge)](http://aiida-zeopp.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/aiida-zeopp.svg)](https://badge.fury.io/py/aiida-zeopp)

# aiida-zeopp

AiiDA plugin for [Zeo++](http://www.zeoplusplus.org/)

## Installation

```shell
git clone https://github.com/ltalirz/aiida-zeopp aiida-zeopp
cd aiida-zeopp
pip install -e .  # also installs aiida, if missing (but not postgres)
reentry scan
verdi quicksetup  # better to set up a new profile
verdi calculation plugins  # should now show your calclulation plugins
```

## Usage

 * Use `CifData` to specify input structure
 * (optional) Use `SinglefileData` to specify atomic radii file
 * Use `NetworkParameters` dictionary to specify other command line options

A quick demo of how to submit a calculation:
```shell
verdi daemon start         # make sure the daemon is running
cd examples
verdi run submit.py        # submit test calculation
verdi calculation list -a  # check status of calculation
```

For a complete list of supported command line options, see [here](aiida_zeopp/calculations/network.py)

## Tests

The following will discover and run all unit test:
```shell
pip install -e .[testing]
python manage.py
```

## Analyzing output

```shell
$ verdi calculation show 88
-----------  ------------------------------------------------------------------------------
type         NetworkCalculation
pk           88
uuid         deb63433-4dcd-4ca1-9165-cb97877496b3
label        aiida_zeopp example calculation
description  Converts .cif to .cssr format, computes surface area, pore volume and channels
ctime        2018-11-19 09:12:55.259776+00:00
mtime        2018-11-19 09:15:15.708275+00:00
computer     [1] localhost
code         network
-----------  ------------------------------------------------------------------------------
##### INPUTS:
Link label      PK  Type
------------  ----  -----------------
parameters      87  NetworkParameters
structure       86  CifData
##### OUTPUTS:
Link label           PK  Type
-----------------  ----  --------------
remote_folder        89  RemoteData
retrieved            90  FolderData
structure_cssr       91  SinglefileData
output_parameters    92  ParameterData

$ verdi calculation res 88
{
  "ASA_A^2": 3532.09,
  "ASA_m^2/cm^3": 1932.13,
  "ASA_m^2/g": 2197.86,
  "Channel_surface_area_A^2": 3532.09,
  "Channels": {
    "Dimensionalities": [
      3
    ],
    "Largest_free_spheres": [
      6.74621
    ],
    "Largest_included_free_spheres": [
      13.1994
    ],
    "Largest_included_spheres": [
      13.1994
    ]
  },
  "Density": 0.879097,
  "Input_chan": 1.2,
  "Input_cssr": true,
  "Input_sa": [
    1.82,
    1.82,
    1000
  ],
  "Input_structure_filename": "HKUST-1.cif",
  "Input_volpo": [
    1.82,
    1.82,
    1000
  ],
  "NASA_A^2": 0.0,
  "NASA_m^2/cm^3": 0.0,
  "NASA_m^2/g": 0.0,
  "Number_of_channels": 1,
  "Number_of_pockets": 0,
  "POAV_A^3": 9049.01,
  "POAV_Volume_fraction": 0.495,
  "POAV_cm^3/g": 0.563078,
  "PONAV_A^3": 0.0,
  "PONAV_Volume_fraction": 0.0,
  "PONAV_cm^3/g": 0.0,
  "Pocket_surface_area_A^2": 0.0,
  "Unitcell_volume": 18280.8
}

$ verdi calculation outputls 88
_scheduler-stderr.txt
_scheduler-stdout.txt
out.chan
out.cssr
out.sa
out.volpo

$ verdi calculation outputcat 88 -p out.sa
@ out.sa Unitcell_volume: 18280.8   Density: 0.879097   ASA_A^2: 3532.09 ASA_m^2/cm^3: 1932.13 ASA_m^2/g: 2197.86 NASA_A^2: 0 NASA_m^2/cm^3: 0 NASA_m^2/g: 0
Number_of_channels: 1 Channel_surface_area_A^2: 3532.09
Number_of_pockets: 0 Pocket_surface_area_A^2:
```

## License

MIT

## Contact
leopold.talirz@gmail.com
