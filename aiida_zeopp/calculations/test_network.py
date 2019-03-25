""" Tests for calculations

"""
from __future__ import absolute_import
import os
import io

import aiida_zeopp.tests as zt


class TestNetwork(zt.PluginTestCase):
    def setUp(self):
        self.code = zt.get_code(entry_point='zeopp.network')

    def test_submit_HKUST1(self):
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

        # set up calculation
        options = {
            "resources": {
                "num_machines": 1,
                "num_mpiprocs_per_machine": 1,
            },
            "max_wallclock_seconds": 3 * 60,
        }

        inputs = {
            'code': self.code,
            'parameters': parameters,
            'structure': structure,
            'metadata': {
                'options': options,
                'label': "aiida_zeopp format conversion",
                'description': "Test converting .cif to .cssr format",
            },
        }

        _result, node = run_get_node(NetworkCalculation, **inputs)

        cssr = io.open(
            os.path.join(TEST_DIR, 'HKUST-1.cssr'), 'r',
            encoding='utf8').read()
        self.assertEqual(cssr, node.outputs.structure_cssr.get_content())

    def test_submit_MgO(self):
        """Test submitting a calculation

        This includes a radii file.
        """
        from aiida_zeopp.tests import TEST_DIR
        from aiida_zeopp.calculations.network import NetworkCalculation
        from aiida.engine import run_get_node
        from aiida.plugins import DataFactory

        # Prepare input parameters
        parameters = DataFactory('zeopp.parameters')(
            dict={
                'cssr': True,
                'res': True,
                'sa': [1.82, 1.82, 5000],
                'vsa': [1.82, 1.82, 5000],
                'volpo': [1.82, 1.82, 5000],
                'chan': 1.2,
                'ha': False,
                'strinfo': True,
                #    'gridG': True,
            })

        structure = DataFactory('cif')(
            file=os.path.join(TEST_DIR, 'MgO.cif'), parse_policy='lazy')

        atomic_radii = DataFactory('singlefile')(
            file=os.path.join(TEST_DIR, 'MgO.rad'))

        # set up calculation
        options = {
            "resources": {
                "num_machines": 1,
                "num_mpiprocs_per_machine": 1,
            },
            "max_wallclock_seconds": 30,
        }

        inputs = {
            'code': self.code,
            'parameters': parameters,
            'structure': structure,
            'atomic_radii': atomic_radii,
            'metadata': {
                'options': options,
                'label': "aiida_zeopp format conversion",
                'description': "Test converting .cif to .cssr format",
            },
        }

        _result, node = run_get_node(NetworkCalculation, **inputs)

        self.assertAlmostEqual(
            node.outputs.output_parameters.get_attribute('Density'),
            3.18223,
            places=4)
        self.assertEqual(
            node.outputs.output_parameters.get_attribute('ASA_m^2/g'), 0.0)
