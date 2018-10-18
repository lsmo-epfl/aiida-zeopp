# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function
import os
import aiida_zeopp.tests as tests
from aiida.orm import DataFactory

code = tests.get_code(entry_point='zeopp.network')

# set up calculation
calc = code.new_calc()
calc.label = "aiida_zeopp example calculation"
calc.description = "Converts .cif to .cssr format, computes surface area, pore volume and channels"
calc.set_max_wallclock_seconds(1 * 60)
calc.set_withmpi(False)
calc.set_resources({"num_machines": 1})

# Prepare input parameters
NetworkParameters = DataFactory('zeopp.parameters')
d = {
    'cssr': True,
    'sa': [1.82, 1.82, 1000],
    'volpo': [1.82, 1.82, 1000],
    'chan': 1.2,
}
parameters = NetworkParameters(dict=d)
calc.use_parameters(parameters)

CifData = DataFactory('cif')
this_dir = os.path.dirname(os.path.realpath(__file__))
structure = CifData(file=os.path.join(this_dir, 'HKUST-1.cif'))
calc.use_structure(structure)

calc.store_all()
calc.submit()
print("submitted calculation; calc=Calculation(uuid='{}') # ID={}".format(
    calc.uuid, calc.dbnode.pk))
