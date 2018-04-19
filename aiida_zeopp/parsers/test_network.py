""" Tests for parsers

"""
import os

from aiida.utils.fixtures import PluginTestCase
import aiida_zeopp.tests as zt


class TestNetwork(PluginTestCase):

    BACKEND = zt.get_backend()

    def setUp(self):

        # set up test computer
        self.computer = zt.get_localhost_computer().store()
        self.code = zt.get_network_code().store()

    def get_calc(self, parameters):
        """Test parsing a simple calculation

        Uses example cif file.
        
        :param parameters:  A zeopp.parameters object
        :return calc: A zeopp.calculation object
        """
        # Prepare input parameters
        from aiida.orm import DataFactory
        CifData = DataFactory('cif')
        structure = CifData(
            file=os.path.join(zt.TEST_DIR, 'HKUST-1.cif'), parse_policy='lazy')

        # set up calculation
        calc = self.code.new_calc()
        calc.label = "aiida_zeopp format conversion"
        calc.set_max_wallclock_seconds(30)
        # This line is only needed for local codes, otherwise the computer is
        # automatically set from the code
        calc.set_computer(self.computer)
        calc.set_withmpi(False)
        calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})
        calc.use_parameters(parameters)
        calc.use_input_structure(structure)

        return calc

    def test_parser_selection(self):
        """Test correct selection of output parsers"""
        from aiida_zeopp.parsers.network import NetworkParser
        from aiida_zeopp.parsers.plain import SurfaceAreaParser, PoreVolumeParser
        from aiida_zeopp.parsers.structure import CssrParser
        from aiida.orm import DataFactory

        NetworkParameters = DataFactory('zeopp.parameters')

        params1 = NetworkParameters(dict={
            'cssr': True,
            'sa': [1.82, 1.82, 10000],
            'volpo': [1.82, 1.82, 100000]
        })

        parser1 = NetworkParser(self.get_calc(params1))
        output_parsers = parser1.output_parsers(params1)
        self.assertItemsEqual(
            output_parsers, [CssrParser, SurfaceAreaParser, PoreVolumeParser])
