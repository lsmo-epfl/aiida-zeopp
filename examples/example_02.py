#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Submit a zeo++ test calculation."""
# pylint: disable=invalid-name
from __future__ import absolute_import
from __future__ import print_function

import os
import click
from aiida import cmdline


def test_submit(network_code):
    """Example of how to submit a zeo++ calculation.

    Simply copy the contents of this function into a script.
    """
    from aiida.plugins import DataFactory, CalculationFactory
    from aiida.engine import run_get_node

    if not network_code:
        from aiida_zeopp import tests
        network_code = tests.get_code(entry_point='zeopp.network')

    # Prepare input parameters
    NetworkParameters = DataFactory('zeopp.parameters')
    # For allowed keys, print(NetworkParameters.schema)
    parameters = NetworkParameters(
        dict={
            'ha': 'DEF',  #just for speed; use 'DEF' for prodution!
            'psd': [1.2, 1.2, 1000],  #compute pore size distribution
        })

    CifData = DataFactory('cif')
    this_dir = os.path.dirname(os.path.realpath(__file__))
    structure = CifData(file=os.path.join(this_dir, 'HKUST-1.cif'))

    # set up calculation
    inputs = {
        'code': network_code,
        'parameters': parameters,
        'structure': structure,
        'metadata': {
            'options': {
                'max_wallclock_seconds': 1 * 60,
            },
            'label': 'aiida_zeopp example calculation',
            'description': 'Compute PSD',
        },
    }

    NetworkCalculation = CalculationFactory('zeopp.network')
    print('Running NetworkCalculation: computing PSD ...')
    result, node = run_get_node(NetworkCalculation,
                                **inputs)  # or use aiida.engine.submit

    print('NetworkCalculation<{}> terminated.'.format(node.pk))

    print('\nComputed output_parameters {}\n'.format(
        str(result['output_parameters'])))


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ ./example_02.py --code network@localhost

    Alternative (creates network@localhost-test code): $ ./example_02.py

    Help: $ ./example_02.py --help
    """
    test_submit(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
