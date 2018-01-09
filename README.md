## aiida-zeopp

AiiDA plugin for [Zeo++](http://www.zeoplusplus.org/)

# Installation

```shell
$ git clone https://github.com/ltalirz/aiida-zeopp aiida-zeopp
$ cd aiida-zeopp
$ pip install -e .  # also installs aiida, if missing (but not postgres)
$ reentry scan -r aiida  
```

# Usage
A complete example of how to submit a test calculation using this plugin.

```shell
$ verdi computer setup   # set up localhost for testing
At any prompt, type ? to get some help.
---------------------------------------
=> Computer name: localhost
Creating new computer with name 'localhost'
=> Fully-qualified hostname: localhost
=> Description: my local computer
=> Enabled: True
=> Transport type: local
=> Scheduler type: direct
=> AiiDA work directory: /tmp
=> mpirun command:
=> Default number of CPUs per machine: 4
=> Text to prepend to each command execution:
   # This is a multiline input, press CTRL+D on a
   # empty line when you finish
   # ------------------------------------------
   # End of old input. You can keep adding
   # lines, or press CTRL+D to store this value
   # ------------------------------------------
=> Text to append to each command execution:
   # This is a multiline input, press CTRL+D on a
   # empty line when you finish
   # ------------------------------------------
   # End of old input. You can keep adding
   # lines, or press CTRL+D to store this value
   # ------------------------------------------
Computer 'localhost' successfully stored in DB.
pk: 1, uuid: a5b452f0-ec1e-4ec2-956a-10a416f60ed3
Note: before using it with AiiDA, configure it using the command
  verdi computer configure localhost
(Note: machine_dependent transport parameters cannot be set via
the command-line interface at the moment)

$ verdi computer configure localhost
Configuring computer 'localhost' for the AiiDA user 'leopold.talirz@epfl.ch'
Computer localhost has transport of type local
There are no special keys to be configured. Configuration completed.

verdi code setup
At any prompt, type ? to get some help.
---------------------------------------
=> Label: aiida_zeopp
=> Description: zeo++ 0.3
=> Local: False
=> Default input plugin: zeopp.network
=> Remote computer name: localhost
=> Remote absolute path: /Users/leopold/Personal/Postdoc-MARVEL/Projects/2017-09-15_pawel_plugin/zeo++-0.3/network
=> Text to prepend to each command execution
FOR INSTANCE, MODULES TO BE LOADED FOR THIS CODE:
   # This is a multiline input, press CTRL+D on a
   # empty line when you finish
   # ------------------------------------------
   # End of old input. You can keep adding
   # lines, or press CTRL+D to store this value
   # ------------------------------------------
=> Text to append to each command execution:
   # This is a multiline input, press CTRL+D on a
   # empty line when you finish
   # ------------------------------------------
   # End of old input. You can keep adding
   # lines, or press CTRL+D to store this value
   # ------------------------------------------
Code 'aiida_zeopp' successfully stored in DB.
pk: 73, uuid: c89510a9-735f-4cd2-8421-bdf1da42f044

$ verdi daemon start  # may need to 'verdi daemon configureuser'
Clearing all locks ...
Starting AiiDA Daemon ...
Daemon started

$ cd examples

$ verdi run submit.py
submitted calculation; calc=Calculation(uuid='ac86b1a4-ccf1-489d-80ba-17c4e3304cb0') # ID=76

$ verdi calculation list -a
# Last daemon state_updater check: 0h:00m:28s ago (at 21:16:07 on 2018-01-09)
  PK  Creation    State             Sched. state    Computer    Type
----  ----------  ----------------  --------------  ----------  -------------
  76  19s ago     WITHSCHEDULER                     localhost   zeopp.network

Total results: 1

$ verdi calculation list -a
# Last daemon state_updater check: 0h:00m:05s ago (at 21:23:37 on 2018-01-09)
  PK  Creation    State             Sched. state    Computer    Type
----  ----------  ----------------  --------------  ----------  -------------
  76  7m ago      FINISHED          DONE            localhost   zeopp.network

Total results: 1

$ verdi calculation show 76
-----------  ------------------------------------
type         NetworkCalculation
pk           76
uuid         ac86b1a4-ccf1-489d-80ba-17c4e3304cb0
label        aiida_zeopp format conversion
description  Test converting .cif to .cssr format
ctime        2018-01-09 20:16:16.522201+00:00
mtime        2018-01-09 20:16:41.107759+00:00
computer     [1] localhost
code         zeopp
-----------  ------------------------------------
##### INPUTS:
Link label         PK  Type
---------------  ----  -----------------
input_structure    74  SinglefileData
parameters         75  NetworkParameters
##### OUTPUTS:
Link label       PK  Type
-------------  ----  ----------
remote_folder    77  RemoteData
retrieved        78  FolderData

$ verdi calculation outputls 76
_scheduler-stderr.txt
_scheduler-stdout.txt
out.cssr

$ verdi calculation outputcat 76 -p _scheduler-stdout.txtOpening File: HKUST-1.cif
Starting Voronoi decomposition
Box dimensions:
  va=(26.343000 0 0)
  vb=(0.000000 26.343000 0)
  vc=(0.000000 0.000000 26.343000)

Total particles = 624

Internal grid size = (5 5 5)

Using voro++ with radii for particles.
Performing Voronoi decomposition.
Volume check:
  Total domain volume  = 18280.820976
  Total Voronoi volume = 18280.820976
Voronoi decomposition finished. Rerouting Voronoi network information.
Finished rerouting information.
Finished Voronoi decomposition
Command 0  -cssr
Writing atom network information to out.cssr
