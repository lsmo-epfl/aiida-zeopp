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
            'ha': 'LOW',  #just for speed; use 'DEF' for prodution!
            'cssr': True,  #converting to cssr
            'res': True,
            'sa': [1.86, 1.86, 1000],  #compute surface area
            'vol': [0.0, 0.0, 1000],  #compute gemetric pore volume
            #'block': [2.0, 100]  #compute blocking spheres for a big molecule
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
            'label':
            'aiida_zeopp example calculation',
            'description':
            'Converts .cif to .cssr format, computes surface area, and pore volume',
        },
    }

    NetworkCalculation = CalculationFactory('zeopp.network')
    print('Running NetworkCalculation: please wait...')
    result, node = run_get_node(NetworkCalculation,
                                **inputs)  # or use aiida.engine.submit

    print('NetworkCalculation<{}> terminated.'.format(node.pk))

    print('\nComputed output_parameters {}\n'.format(
        str(result['output_parameters'])))
    outputs = result['output_parameters'].get_dict()

    print('Density ({}): {:.3f}'.format(outputs['Density_unit'],
                                        outputs['Density']))

    print('Largest free sphere ({}): {:.3f}'.format(
        outputs['Largest_free_sphere_unit'], outputs['Largest_free_sphere']))

    print('Largest included sphere ({}): {:.3f}'.format(
        outputs['Largest_included_sphere_unit'],
        outputs['Largest_included_sphere']))

    print('Nitrogen accessible surface area ({}): {:.3f}'.format(
        outputs['ASA_m^2/g_unit'], outputs['ASA_m^2/g']))

    print('Geometric pore volume ({}): {:.3f}'.format(
        outputs['AV_cm^3/g_unit'], outputs['AV_cm^3/g']))

    # print('Number of blocking spheres needed for probe radius of {:.2f}A: {}'.
    #       format(
    #           outputs['Input_block'][0],
    #           outputs['Number_of_blocking_spheres']))
    # print('Blocking spheres file: SinglefileData<{}>'.format(
    #     node.outputs.block.pk))

    print('CSSR structure: SinglefileData<{}>'.format(
        node.outputs.structure_cssr.pk))


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ ./example_01.py --code network@localhost

    Alternative (creates network@localhost-test code): $ ./example_01.py

    Help: $ ./example_01.py --help
    """
    test_submit(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
