#!/usr/bin/env python
"""Submit a zeo++ test calculation."""
# pylint: disable=invalid-name

import click
from aiida import cmdline, orm
from aiida.engine import run_get_node
from aiida.plugins import CalculationFactory, DataFactory
from importlib_resources import files

import aiida_zeopp
from aiida_zeopp import tests


def test_submit(network_code):
    """Example of how to submit a zeo++ calculation.

    Simply copy the contents of this function into a script.
    """

    if not network_code:
        network_code = tests.get_code(entry_point="zeopp.network")

    # Prepare input parameters
    NetworkParameters = DataFactory("zeopp.parameters")
    # For allowed keys, print(NetworkParameters.schema)
    parameters = NetworkParameters(
        dict={
            "ha": "LOW",  # just for speed; use 'DEF' for prodution!
            "psd": [1.2, 1.2, 1000],  # compute pore size distribution
        }
    )
    structure = orm.CifData(file=(files(aiida_zeopp).parent / "examples" / "HKUST-1.cif").as_posix())

    # set up calculation
    inputs = {
        "code": network_code,
        "parameters": parameters,
        "structure": structure,
        "metadata": {
            "options": {
                "max_wallclock_seconds": 1 * 60,
            },
            "label": "aiida_zeopp example calculation",
            "description": "Compute PSD",
        },
    }

    NetworkCalculation = CalculationFactory("zeopp.network")
    print("Running NetworkCalculation: computing PSD ...")
    result, node = run_get_node(NetworkCalculation, **inputs)  # or use aiida.engine.submit

    print(f"NetworkCalculation<{node.pk}> terminated.")
    print(f"\nComputed output_parameters {result['output_parameters'].get_dict()}\n")


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


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
