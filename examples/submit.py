# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import aiida_zeopp.tests as tests
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run_get_node

NetworkCalculation = CalculationFactory('zeopp.network')
code = tests.get_code(entry_point='zeopp.network')

# Prepare input parameters
NetworkParameters = DataFactory('zeopp.parameters')
# For allowed keys, print(NetworkParameters.schema)
d = {
    'cssr': True,
    'sa': [1.82, 1.82, 1000],
    'volpo': [1.82, 1.82, 1000],
    'chan': 1.2,
}
parameters = NetworkParameters(dict=d)

CifData = DataFactory('cif')
this_dir = os.path.dirname(os.path.realpath(__file__))
structure = CifData(file=os.path.join(this_dir, 'HKUST-1.cif'))

# set up calculation
options = {
    "resources": {
        "num_machines": 1,
        "num_mpiprocs_per_machine": 1,
    },
    "max_wallclock_seconds": 1 * 60,
}

inputs = {
    'code': code,
    'parameters': parameters,
    'structure': structure,
    'metadata': {
        'options':
        options,
        'label':
        "aiida_zeopp example calculation",
        'description':
        "Converts .cif to .cssr format, computes surface area, pore volume and channels",
    },
}

# or use aiida.engine.submit
result, node = run_get_node(NetworkCalculation, **inputs)

print("Computed density: {:.3f}".format(
    node.outputs.output_parameters.get_attribute('Density')))
