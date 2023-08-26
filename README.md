[![Build Status](https://github.com/lsmo-epfl/aiida-zeopp/workflows/Build/badge.svg)](https://github.com/lsmo-epfl/aiida-zeopp/actions)
[![PyPI version](https://badge.fury.io/py/aiida-zeopp.svg)](https://badge.fury.io/py/aiida-zeopp)
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/ltalirz/aiida-zeopp/blob/master/LICENSE)

| Plugin | AiiDA | Python |
|-|-|-|
| `2.0.0` | ![Compatibility for v2.0][AiiDA v2.0] |  [![PyPI pyversions](https://img.shields.io/pypi/pyversions/aiida-zeopp.svg)](https://pypi.org/project/aiida-zeopp) |
| `1.1.0` | ![Compatibility for v1.1][AiiDA v1.1] |  ![PyPI pyversions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue) |


# aiida-zeopp

AiiDA plugin for [Zeo++](http://www.zeoplusplus.org/)

## Installation

```shell
pip install aiida-zeopp
reentry scan
verdi quicksetup  # better to set up a new profile
verdi calculation plugins  # should now show your calclulation plugins
```

## Features

 * Add input structure in CIF format
  ```python
  CifData = DataFactory('cif')
  inputs['structure'] = CifData(file='/path/to/file')
  ```
 * Specify command line options using a python dictionary and `NetworkParameters`
  ```python
  d = { 'sa': [1.82, 1.82, 1000], 'volpo': [1.82, 1.82, 1000], 'chan': 1.2 }
  NetworkParameters = DataFactory('zeopp.parameters')
  inputs['parameters'] = NetworkParameters(dict=d)
  ```
 * `NetworkParameters` validates the command line options using [voluptuous](https://github.com/alecthomas/voluptuous).
   Find out about supported options:
  ```python
  NetworkParameters = DataFactory('zeopp.parameters')
  print(NetworkParameters.schema)
  ```
 * Add alternative atomic radii file
  ```python
  SinglefileData = DataFactory('singlefile')
  inputs['atomic_radii'] = SinglefileData(file='/path/to/file')
  ```

## Examples

See `examples` folder for complete examples of setting up a calculation.

```shell
verdi daemon start         # make sure the daemon is running
cd examples
verdi run examples/example_01.py  # runs test calculatio
```

## Tests

`aiida_zeopp` comes with a number of tests that are run at every commit.

The following will discover and run all unit tests:
```shell
pip install -e .[testing]
pytest
```

## Analyzing output

```shell
$ verdi process show 88
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

$ verdi calcjob res 88
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

$ verdi calcjob outputls 88
_scheduler-stderr.txt
_scheduler-stdout.txt
out.chan
out.cssr
out.sa
out.volpo

$ verdi calcjob outputcat 88 -p out.sa
@ out.sa Unitcell_volume: 18280.8   Density: 0.879097   ASA_A^2: 3532.09 ASA_m^2/cm^3: 1932.13 ASA_m^2/g: 2197.86 NASA_A^2: 0 NASA_m^2/cm^3: 0 NASA_m^2/g: 0
Number_of_channels: 1 Channel_surface_area_A^2: 3532.09
Number_of_pockets: 0 Pocket_surface_area_A^2:
```

## License

MIT

## Contact
leopold.talirz@gmail.com


## Acknowledgements
This work is supported by:
* the [MARVEL National Centre for Competency in Research](<http://nccr-marvel.ch>) funded by the [Swiss National Science Foundation](<http://www.snf.ch/en>);
* the [swissuniversities P-5 project "Materials Cloud"](<https://www.materialscloud.org/swissuniversities>).

<img src="miscellaneous/logos/MARVEL.png" alt="MARVEL" style="padding:10px;" width="150"/>
<img src="miscellaneous/logos/swissuniversities.png" alt="swissuniversities" style="padding:10px;" width="250"/>

[AiiDA v1.1]: https://img.shields.io/badge/AiiDA->=1.4.4,<2.0.0-007ec6.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAhCAYAAABTERJSAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAFhgAABYYBG6Yz4AAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAUbSURBVFiFzZhrbFRVEMd%2Fc%2B5uu6UUbIFC%2FUAUVEQCLbQJBIiBDyiImJiIhmohYNCkqJAQxASLF8tDgYRHBLXRhIcKNtFEhVDgAxBJqgmVh4JEKg3EIn2QYqBlt917xg%2BFss%2ByaDHOtzsz5z%2B%2FuZl7ztmF%2F5HJvxVQN6cPYX8%2FPLnOmsvNAvqfwuib%2FbNIk9cQeQnLcKRL5xLIV%2Fic9eJeunjPYbRs4FjQSpTB3aS1IpRKeeOOewajy%2FKKEO8Q0DuVdKy8IqsbPulxGHUfCBBu%2BwUYGuFuBTK7wQnht6PEbf4tlRomVRjCbXNjQEB0AyrFQOL5ENIJm7dTLZE6DPJCnEtFZVXDLny%2B4Sjv0PmmYu1ZdUek9RiMgoDmJ8V0L7XJqsZ3UW8YsBOwEeHeeFce7jEYXBy0m9m4BbXqSj2%2Bxnkg26MCVrN6DEZcwggtd8pTFx%2Fh3B9B50YLaFOPwXQKUt0tBLegtSomfBlfY13PwijbEnhztGzgJsK5h9W9qeWwBqjvyhB2iBs1Qz0AU974DciRGO8CVN8AJhAeMAdA3KbrKEtvxhsI%2B9emWiJlGBEU680Cfk%2BSsVqXZvcFYGXjF8ABVJ%2BTNfVXehyms1zzn1gmIOxLEB6E31%2FWBe5rnCarmo7elf7dJEeaLh80GasliI5F6Q9cAz1GY1OJVNDxTzQTw7iY%2FHEZRQY7xqJ9RU2LFe%2FYqakdP911ha0XhjjiTVAkDwgatWfCGeYocx8M3glG8g8EXhSrLrHnEFJ5Ymow%2FkhIYv6ttYUW1iFmEqqxdVoUs9FmsDYSqmtmJh3Cl1%2BVtl2s7owDUdocR5bceiyoSivGTT5vzpbzL1uoBpmcAAQgW7ArnKD9ng9rc%2BNgrobSNwpSkkhcRN%2BvmXLjIsDovYHHEfmsYFygPAnIDEQrQPzJYCOaLHLUfIt7Oq0LJn9fxkSgNCb1qEIQ5UKgT%2Fs6gJmVOOroJhQBXVqw118QtWLdyUxEP45sUpSzqP7RDdFYMyB9UReMiF1MzPwoUqHt8hjGFFeP5wZAbZ%2F0%2BcAtAAcji6LeSq%2FMYiAvSsdw3GtrfVSVFUBbIhwRWYR7yOcr%2FBi%2FB1MSJZ16JlgH1AGM3EO2QnmMyrSbTSiACgFBv4yCUapZkt9qwWVL7aeOyHvArJjm8%2Fz9BhdI4XcZgz2%2FvRALosjsk1ODOyMcJn9%2FYI6IrkS5vxMGdUwou2YKfyVqJpn5t9aNs3gbQMbdbkxnGdsr4bTHm2AxWo9yNZK4PXR3uzhAh%2BM0AZejnCrGdy0UvJxl0oMKgWSLR%2B1LH2aE9ViejiFs%2BXn6bTjng3MlIhJ1I1TkuLdg6OcAbD7Xx%2Bc3y9TrWAiSHqVkbZ2v9ilCo6s4AjwZCzFyD9mOL305nV9aonvsQeT2L0gVk4OwOJqXXVRW7naaxswDKVdlYLyMXAnntteYmws2xcVVZzq%2BtHPAooQggmJkc6TLSusOiL4RKgwzzYU1iFQgiUBA1H7E8yPau%2BZl9P7AblVNebtHqTgxLfRqrNvZWjsHZFuqMqKcDWdlFjF7UGvX8Jn24DyEAykJwNcdg0OvJ4p5pQ9tV6SMlP4A0PNh8aYze1ArROyUNTNouy8tNF3Rt0CSXb6bRFl4%2FIfQzNMjaE9WwpYOWQnOdEF%2BTdJNO0iFh7%2BI0kfORzQZb6P2kymS9oTxzBiM9rUqLWr1WE5G6ODhycQd%2FUnNVeMbcH68hYkGycNoUNWc8fxaxfwhDbHpfwM5oeTY7rUX8QAAAABJRU5ErkJggg%3D%3D

[AiiDA v2.0]: https://img.shields.io/badge/AiiDA->=2.3.1,<3.0.0-007ec6.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAhCAYAAABTERJSAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAFhgAABYYBG6Yz4AAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAUbSURBVFiFzZhrbFRVEMd%2Fc%2B5uu6UUbIFC%2FUAUVEQCLbQJBIiBDyiImJiIhmohYNCkqJAQxASLF8tDgYRHBLXRhIcKNtFEhVDgAxBJqgmVh4JEKg3EIn2QYqBlt917xg%2BFss%2ByaDHOtzsz5z%2B%2FuZl7ztmF%2F5HJvxVQN6cPYX8%2FPLnOmsvNAvqfwuib%2FbNIk9cQeQnLcKRL5xLIV%2Fic9eJeunjPYbRs4FjQSpTB3aS1IpRKeeOOewajy%2FKKEO8Q0DuVdKy8IqsbPulxGHUfCBBu%2BwUYGuFuBTK7wQnht6PEbf4tlRomVRjCbXNjQEB0AyrFQOL5ENIJm7dTLZE6DPJCnEtFZVXDLny%2B4Sjv0PmmYu1ZdUek9RiMgoDmJ8V0L7XJqsZ3UW8YsBOwEeHeeFce7jEYXBy0m9m4BbXqSj2%2Bxnkg26MCVrN6DEZcwggtd8pTFx%2Fh3B9B50YLaFOPwXQKUt0tBLegtSomfBlfY13PwijbEnhztGzgJsK5h9W9qeWwBqjvyhB2iBs1Qz0AU974DciRGO8CVN8AJhAeMAdA3KbrKEtvxhsI%2B9emWiJlGBEU680Cfk%2BSsVqXZvcFYGXjF8ABVJ%2BTNfVXehyms1zzn1gmIOxLEB6E31%2FWBe5rnCarmo7elf7dJEeaLh80GasliI5F6Q9cAz1GY1OJVNDxTzQTw7iY%2FHEZRQY7xqJ9RU2LFe%2FYqakdP911ha0XhjjiTVAkDwgatWfCGeYocx8M3glG8g8EXhSrLrHnEFJ5Ymow%2FkhIYv6ttYUW1iFmEqqxdVoUs9FmsDYSqmtmJh3Cl1%2BVtl2s7owDUdocR5bceiyoSivGTT5vzpbzL1uoBpmcAAQgW7ArnKD9ng9rc%2BNgrobSNwpSkkhcRN%2BvmXLjIsDovYHHEfmsYFygPAnIDEQrQPzJYCOaLHLUfIt7Oq0LJn9fxkSgNCb1qEIQ5UKgT%2Fs6gJmVOOroJhQBXVqw118QtWLdyUxEP45sUpSzqP7RDdFYMyB9UReMiF1MzPwoUqHt8hjGFFeP5wZAbZ%2F0%2BcAtAAcji6LeSq%2FMYiAvSsdw3GtrfVSVFUBbIhwRWYR7yOcr%2FBi%2FB1MSJZ16JlgH1AGM3EO2QnmMyrSbTSiACgFBv4yCUapZkt9qwWVL7aeOyHvArJjm8%2Fz9BhdI4XcZgz2%2FvRALosjsk1ODOyMcJn9%2FYI6IrkS5vxMGdUwou2YKfyVqJpn5t9aNs3gbQMbdbkxnGdsr4bTHm2AxWo9yNZK4PXR3uzhAh%2BM0AZejnCrGdy0UvJxl0oMKgWSLR%2B1LH2aE9ViejiFs%2BXn6bTjng3MlIhJ1I1TkuLdg6OcAbD7Xx%2Bc3y9TrWAiSHqVkbZ2v9ilCo6s4AjwZCzFyD9mOL305nV9aonvsQeT2L0gVk4OwOJqXXVRW7naaxswDKVdlYLyMXAnntteYmws2xcVVZzq%2BtHPAooQggmJkc6TLSusOiL4RKgwzzYU1iFQgiUBA1H7E8yPau%2BZl9P7AblVNebtHqTgxLfRqrNvZWjsHZFuqMqKcDWdlFjF7UGvX8Jn24DyEAykJwNcdg0OvJ4p5pQ9tV6SMlP4A0PNh8aYze1ArROyUNTNouy8tNF3Rt0CSXb6bRFl4%2FIfQzNMjaE9WwpYOWQnOdEF%2BTdJNO0iFh7%2BI0kfORzQZb6P2kymS9oTxzBiM9rUqLWr1WE5G6ODhycQd%2FUnNVeMbcH68hYkGycNoUNWc8fxaxfwhDbHpfwM5oeTY7rUX8QAAAABJRU5ErkJggg%3D%3D
