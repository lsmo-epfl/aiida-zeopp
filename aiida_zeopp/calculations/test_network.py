""" Tests for calculations

"""
from __future__ import absolute_import
import os
import io
import pytest


def test_submit_HKUST1(clear_database, network_code, basic_options):  # pylint: disable=unused-argument
    """Test submitting a calculation"""
    from aiida_zeopp.tests import TEST_DIR
    from aiida_zeopp.calculations.network import NetworkCalculation
    from aiida.engine import run_get_node

    # Prepare input parameters
    from aiida.plugins import DataFactory
    NetworkParameters = DataFactory('zeopp.parameters')
    parameters = NetworkParameters(dict={'cssr': True})

    CifData = DataFactory('cif')
    structure = CifData(
        file=os.path.join(TEST_DIR, 'HKUST-1.cif'), parse_policy='lazy')

    inputs = {
        'code': network_code,
        'parameters': parameters,
        'structure': structure,
        'metadata': {
            'options': basic_options,
            'label': "aiida_zeopp format conversion",
            'description': "Test converting .cif to .cssr format",
        },
    }

    _result, node = run_get_node(NetworkCalculation, **inputs)

    cssr = io.open(
        os.path.join(TEST_DIR, 'HKUST-1.cssr'), 'r', encoding='utf8').read()
    assert (cssr == node.outputs.structure_cssr.get_content())


def test_submit_MgO(clear_database, network_code, basic_options):  # pylint: disable=unused-argument
    """Test submitting a calculation

    This includes a radii file.
    """
    from aiida_zeopp.tests import TEST_DIR
    from aiida_zeopp.calculations.network import NetworkCalculation
    from aiida.engine import run_get_node
    from aiida.plugins import DataFactory

    # Prepare input parameters
    parameters = DataFactory('zeopp.parameters')(dict={
        'cssr': True,
        'res': True,
        'sa': [1.82, 1.82, 5000],
        'vsa': [1.82, 1.82, 5000],
        'volpo': [1.82, 1.82, 5000],
        'chan': 1.2,
        'ha': True,
        'strinfo': True,
        'gridG': True,
    })

    structure = DataFactory('cif')(
        file=os.path.join(TEST_DIR, 'MgO.cif'), parse_policy='lazy')

    atomic_radii = DataFactory('singlefile')(
        file=os.path.join(TEST_DIR, 'MgO.rad'))

    # set up calculation
    inputs = {
        'code': network_code,
        'parameters': parameters,
        'structure': structure,
        'atomic_radii': atomic_radii,
        'metadata': {
            'options': basic_options,
            'label': "aiida_zeopp format conversion",
            'description': "Test converting .cif to .cssr format",
        },
    }

    _result, node = run_get_node(NetworkCalculation, **inputs)

    assert pytest.approx(
        node.outputs.output_parameters.get_attribute('Density'),
        0.01) == 3.18223
    assert node.outputs.output_parameters.get_attribute('ASA_m^2/g') == 0.0
