""" Tests for parsers

"""
from __future__ import absolute_import
import os

import aiida_zeopp.tests as zt
import six


class TestNetwork(zt.PluginTestCase):
    def setUp(self):

        # set up test computer
        self.code = zt.get_code(entry_point='zeopp.network')

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

        test_files = {
            'cssr': 'HKUST-1.cssr',
            'sa': 'HKUST-1.sa',
            'volpo': 'HKUST-1.volpo',
            'block': 'HKUST-1.block',
        }

        for out_key, out_file in six.iteritems(parameters.output_dict):
            shutil.copyfile(
                os.path.join(zt.TEST_DIR, test_files[out_key]),
                os.path.join(tmp_dir, out_file))

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

        # check that it parses successfully
        parser1 = NetworkParser(self.get_calc(params1))
        success, node_list = parser1.parse_with_retrieved(retrieved)

        self.assertTrue(success)

        # check that parsed nodes meet expectations
        expected_keys = set(['structure_cssr', 'output_parameters'])
        found_keys = {n[0] for n in node_list}
        self.assertEqual(expected_keys, found_keys)

    def test_parser_fail(self):
        """Test parsing a fake output.

        Providing empty .block file which should raise a ParsingError.
        """
        from aiida_zeopp.parsers.network import NetworkParser
        from aiida.parsers.exceptions import OutputParsingError
        from aiida.orm import DataFactory

        NetworkParameters = DataFactory('zeopp.parameters')

        params1 = NetworkParameters(dict={
            'volpo': [1.82, 1.82, 100000],
            'block': [1.82, 10000],
        })
        retrieved = self.get_retrieved(params1)

        # check that it parses successfully
        parser1 = NetworkParser(self.get_calc(params1))

        with self.assertRaises(OutputParsingError):
            parser1.parse_with_retrieved(retrieved)