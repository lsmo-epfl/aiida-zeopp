""" Tests for parsers

"""
import os

import aiida_zeopp.tests as zt


class TestNetwork(zt.PluginTestCase):
    def setUp(self):

        # set up test computer
        self.computer = zt.get_localhost_computer().store()
        self.code = zt.get_network_code().store()

    def get_calc(self, parameters):
        """Set up a simple calculation

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
        calc.use_structure(structure)

        return calc

    def get_retrieved(self, parameters):
        """Set up a fake 'retrieved' dict.

        As well as an output folder.
        """
        import tempfile
        import shutil
        from aiida.orm.data.folder import FolderData

        tmp_dir = tempfile.mkdtemp()

        test_files = ['HKUST-1.cssr', 'HKUST-1.sa', 'HKUST-1.volpo']
        output_files = parameters.output_files
        for ftest, fout in list(zip(test_files, output_files)):
            shutil.copyfile(
                os.path.join(zt.TEST_DIR, ftest), os.path.join(tmp_dir, fout))

        res = FolderData()
        res.replace_with_folder(tmp_dir)
        shutil.rmtree(tmp_dir)

        retrieved = {'retrieved': res}

        return retrieved

    def test_parser(self):
        """Test parsing a fake output."""
        from aiida_zeopp.parsers.network import NetworkParser
        from aiida.orm import DataFactory

        NetworkParameters = DataFactory('zeopp.parameters')

        params1 = NetworkParameters(dict={
            'cssr': True,
            'sa': [1.82, 1.82, 10000],
            'volpo': [1.82, 1.82, 100000]
        })
        retrieved = self.get_retrieved(params1)

        parser1 = NetworkParser(self.get_calc(params1))
        parser1.parse_with_retrieved(retrieved)
