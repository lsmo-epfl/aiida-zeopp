## v1.1.2

### Improvements

 * Add support for undocumented `-allowAdjustCoordsAndCell` flag  [[#54]](https://github.com/ltalirz/aiida-zeopp/pull/54)

## v1.1.1

### Improvements

 * Bump `aiida-core` dependency to 1.1.0 and fix use of deprecated API
 * Drop `monty` dependency

## v1.1.0

### Improvements

 * Drop python2 support in view of upcoming aiida 1.1.0 [[#54]](https://github.com/ltalirz/aiida-zeopp/pull/54)
 * Add default value for `tot_num_mpiprocs` [[#54]](https://github.com/ltalirz/aiida-zeopp/pull/54)


## v1.0.3

### Bug fixes

 * make sure input file has .cif extension [[#50]](https://github.com/ltalirz/aiida-zeopp/pull/50)


## v1.0.2

### Bug fixes

 * reintroduce parsing of ASA output [[#49]](https://github.com/ltalirz/aiida-zeopp/pull/49)


## v1.0.1

### Bug fixes

 * fix PSD parser for non-porous materials [[#48]](https://github.com/ltalirz/aiida-zeopp/pull/48)

## v1.0.0

### Improvements

 * migrate to aiida-core 1.0 (including exit codes)
 * add default output node [[`1a31e3ba`]](https://github.com/ltalirz/aiida-zeopp/commit/1a31e3bcea4301dfb6ad8bc6db74e5ff76eec5e4)
 * add trove classifier [[#26]](https://github.com/ltalirz/aiida-zeopp/pull/26)
 * support undocumented "string" argument to `-ha` option [[#27]](https://github.com/ltalirz/aiida-zeopp/pull/27)
 * add cli to example + print information on outputs produced [[#33]](https://github.com/ltalirz/aiida-zeopp/pull/33)
 * add units to output parameters and count blocking spheres [[#43]](https://github.com/ltalirz/aiida-zeopp/pull/43)


### Bug fixes

 * fix bugs when boolean flags set to `False` [[#25]](https://github.com/ltalirz/aiida-zeopp/pull/25) [[#38]](https://github.com/ltalirz/aiida-zeopp/pull/38)
 * fix bug in validation of (empty) block file [[#28]](https://github.com/ltalirz/aiida-zeopp/pull/28)
 * fix pymatgen pythyon2.7 dependency [[#40]](https://github.com/ltalirz/aiida-zeopp/pull/40)
 * fix `get_code` utility to find existing codes [[#44]](https://github.com/ltalirz/aiida-zeopp/pull/44)

### Testing

 * move to pytest for testing [[`03e939d`]](https://github.com/ltalirz/aiida-zeopp/commit/03e939dba6f050e6f9811aebe0377df1512f89ab)
 * add automatic deployment to PyPI [[`80f8032`]](https://github.com/ltalirz/aiida-zeopp/commit/80f8032edcc1d778f2781b36263aefc33f0b8357)
 * include full integration test usind zeo++ executable built on travis [[#37]](https://github.com/ltalirz/aiida-zeopp/pull/37)
 * include example script in test suite [[#43]](https://github.com/ltalirz/aiida-zeopp/pull/43)

## v0.2.1

### Improvements

 * add schema for NetworkParameters and document how to access it [[#17]](https://github.com/ltalirz/aiida-zeopp/pull/17)
 * check if blocked pockets file is empty [[#18]](https://github.com/ltalirz/aiida-zeopp/pull/18)
 * add parser for pore size distribution [[#19]](https://github.com/ltalirz/aiida-zeopp/pull/19)

## v0.2.0

### Improvements

 * add parsing of channel output [[#7]](https://github.com/ltalirz/aiida-zeopp/pull/7)
 * add ZeoppGeometryWorkChain [[#8]](https://github.com/ltalirz/aiida-zeopp/pull/8)
 * join dictionary outputs in `output_params` [[#9]](https://github.com/ltalirz/aiida-zeopp/pull/9)
 * support more cli options of `network` [[#13]](https://github.com/ltalirz/aiida-zeopp/pull/13)

### Bug fixes

 * fix channel parser when zero channels [[#12]](https://github.com/ltalirz/aiida-zeopp/pull/12)

## v0.1.1

### Improvements

 * add support for undocumented `-vsa` option [[`fb3d99b`]](https://github.com/ltalirz/aiida-zeopp/commit/fb3d99bcf73c9f92db833f08e2450256c36dd7ea)
 * simplify running tests [[`4d045f8`]](https://github.com/ltalirz/aiida-zeopp/commit/4d045f8050b868fcd50933a791440b1c6b5da7bd) [[`a69a614`]](https://github.com/ltalirz/aiida-zeopp/commit/a69a6144e6ce71ce523ee55d816380a9c0078c93)

## v0.1

First release.
