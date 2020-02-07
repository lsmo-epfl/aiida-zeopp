""" Tests for calculations

"""
import os
import io
import pytest

from aiida_zeopp.tests import TEST_DIR
from aiida.engine import run_get_node
from aiida.plugins import DataFactory, CalculationFactory

NetworkCalculation = CalculationFactory('zeopp.network')
NetworkParameters = DataFactory('zeopp.parameters')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')


def test_submit_HKUST1(network_code, basic_options):  # pylint: disable=unused-argument,invalid-name,invalid-name
    """Test submitting a calculation"""
    # Prepare input parameters
    parameters = NetworkParameters(dict={'cssr': True})
    structure = CifData(file=os.path.join(TEST_DIR, 'HKUST-1.cif'),
                        parse_policy='lazy')

    inputs = {
        'code': network_code,
        'parameters': parameters,
        'structure': structure,
        'metadata': {
            'options': basic_options,
            'label': 'aiida_zeopp format conversion',
            'description': 'Test converting .cif to .cssr format',
        },
    }

    _result, node = run_get_node(NetworkCalculation, **inputs)

    cssr = io.open(os.path.join(TEST_DIR, 'HKUST-1.cssr'),
                   'r',
                   encoding='utf8').read()
    assert cssr == node.outputs.structure_cssr.get_content()


def test_submit_MgO(network_code, basic_options):  # pylint: disable=unused-argument,invalid-name
    """Test submitting a calculation

    This includes a radii file.
    """

    # Prepare input parameters
    parameters = DataFactory('zeopp.parameters')(dict={
        'cssr': True,
        'res': True,
        'sa': [1.82, 1.82, 5000],
        'vsa': [1.82, 1.82, 5000],
        'volpo': [1.82, 1.82, 5000],
        'chan': 1.2,
        'ha': False,
        'strinfo': True,
        'gridG': True,
        'oms': False,
    })

    structure = CifData(file=os.path.join(TEST_DIR, 'MgO.cif'),
                        parse_policy='lazy')

    atomic_radii = SinglefileData(file=os.path.join(TEST_DIR, 'MgO.rad'))

    # set up calculation
    inputs = {
        'code': network_code,
        'parameters': parameters,
        'structure': structure,
        'atomic_radii': atomic_radii,
        'metadata': {
            'options': basic_options,
            'label': 'aiida_zeopp format conversion',
            'description': 'Test converting .cif to .cssr format',
        },
    }

    _result, node = run_get_node(NetworkCalculation, **inputs)

    assert pytest.approx(
        node.outputs.output_parameters.get_attribute('Density'),
        0.01) == 3.18223
    assert node.outputs.output_parameters.get_attribute('ASA_m^2/g') == 0.0


def test_filename(network_code, basic_options):  # pylint: disable=unused-argument,invalid-name
    """Test submitting a calculation from autogenerated CifData.

    Note: filenames of CifData generated from ASE may miss the .cif extension.
    """
    from ase.build import bulk

    # Prepare input parameters
    parameters = NetworkParameters(dict={
        'cssr': True,
    })
    atoms = bulk('Mg', 'fcc', a=3.6)
    cif = CifData(ase=atoms)

    atomic_radii = SinglefileData(file=os.path.join(TEST_DIR, 'MgO.rad'))

    # set up calculation
    inputs = {
        'code': network_code,
        'parameters': parameters,
        'structure': cif,
        'atomic_radii': atomic_radii,
        'metadata': {
            'options': basic_options,
        },
    }
    input_filename = cif.filename if cif.filename.endswith(
        '.cif') else cif.filename + '.cif'

    result, node = run_get_node(NetworkCalculation, **inputs)
    assert 'structure_cssr' in result
    assert node.res.Input_structure_filename == input_filename
