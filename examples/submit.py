# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import click

from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run_get_node

NetworkCalculation = CalculationFactory('zeopp.network')

@click.command('cli')
@click.argument('network_code_string')
def main(network_code_string):
    """Example usage:
    $ verdi run submit.py network@localhost
    Alternative use (creates network@localhost-test code):
    $ verdi run submit.py createcode
    """
    if network_code_string=='createcode':
        from aiida_zeopp import tests
        code = tests.get_code(entry_point='zeopp.network')
    else:
        from aiida.orm import Code
        code = Code.get_from_string(network_code_string)

    # Prepare input parameters
    NetworkParameters = DataFactory('zeopp.parameters')
    # For allowed keys, print(NetworkParameters.schema)
    parameters = NetworkParameters(dict={
        'ha': 'LOW',                #just for speed up the test: use 'DEF' for any other case!
        'cssr': True,               #converting to cssr
        'sa': [1.86, 1.86, 1000],   #computing surface area
        'vol': [0.0, 0.0, 1000],  #computing gemetric pore volume
    })

    CifData = DataFactory('cif')
    this_dir = os.path.dirname(os.path.realpath(__file__))
    structure = CifData(file=os.path.join(this_dir, 'HKUST-1.cif'))

    # set up calculation
    inputs = {
        'code': code,
        'parameters': parameters,
        'structure': structure,
        'metadata': {
            'options': {
                "max_wallclock_seconds": 1 * 60,
            },
            'label':
            "aiida_zeopp example calculation",
            'description':
            "Converts .cif to .cssr format, computes surface area, and pore volume",
        },
    }

    # or use aiida.engine.submit
    print("Running NetworkCalculation: wait...")
    result, node = run_get_node(NetworkCalculation, **inputs)

    print("Nitrogen accessible surface area (m^2/g): {:.3f}".format(
        node.outputs.output_parameters.get_attribute('ASA_m^2/g')))
    print("Geometric pore volume (cm^3/g): {:.3f}".format(
        node.outputs.output_parameters.get_attribute('AV_cm^3/g')))
    print("CSSR structure: SinglefileData<{}>".format(
        node.outputs.structure_cssr.pk))

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
