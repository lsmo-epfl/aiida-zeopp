#!/usr/bin/env python
"""Submit a zeo++ test calculation."""

import os
import click
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
from aiida_zeopp import tests


def test_submit(network_code, submit=True):
    """Example of how to submit a zeo++ calculation.

    Simply copy the contents of this function into a script.
    """

    if not network_code:
        network_code = tests.get_code(entry_point='zeopp.network')

    # For allowed keys, print(NetworkParameters.schema)
    parameters = DataFactory('zeopp.parameters')(
        dict={
            'ha': 'LOW',  #just for speed; use 'DEF' for prodution!
            'cssr': True,  #converting to cssr
            'res': True,
            'sa': [1.86, 1.86, 1000],  #compute surface area
            'vol': [0.0, 0.0, 1000],  #compute gemetric pore volume
            #'block': [2.0, 100]  #compute blocking spheres for a big molecule
        })

    this_dir = os.path.dirname(os.path.realpath(__file__))
    structure = DataFactory('cif')(file=os.path.join(this_dir, 'HKUST-1.cif'))

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

    NetworkCalculation = CalculationFactory('zeopp.network')  # pylint: disable=invalid-name
    print('Running NetworkCalculation: please wait...')
    if submit:
        engine.submit(NetworkCalculation, **inputs)
    else:
        result, node = engine.run_get_node(
            NetworkCalculation, **inputs)  # or use aiida.engine.submit

        print('NetworkCalculation<{}> terminated.'.format(node.pk))

        print('\nComputed output_parameters {}\n'.format(
            str(result['output_parameters'])))
        outputs = result['output_parameters'].get_dict()

        print('Density ({}): {:.3f}'.format(outputs['Density_unit'],
                                            outputs['Density']))

        print('Largest free sphere ({}): {:.3f}'.format(
            outputs['Largest_free_sphere_unit'],
            outputs['Largest_free_sphere']))

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
