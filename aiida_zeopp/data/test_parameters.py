from __future__ import absolute_import
from aiida_zeopp.tests import PluginTestCase


class TestNetworkParameters(PluginTestCase):
    def test_cmdline_cssr(self):
        from aiida_zeopp.data.parameters import NetworkParameters

        d = {'cssr': True}
        self.assertEqual(
            NetworkParameters(d).cmdline_params(), ['-cssr', 'out.cssr'])
        d = {'cssr': False}
        self.assertEqual(NetworkParameters(d).cmdline_params(), [])
        d = {}
        self.assertEqual(NetworkParameters(d).cmdline_params(), [])

    def test_output_parsers(self):
        from aiida_zeopp.data.parameters import NetworkParameters
        from aiida_zeopp.parsers.plain import SurfaceAreaParser, PoreVolumeParser

        d = {
            'cssr': True,
            'sa': [1.82, 1.82, 10000],
            'volpo': [1.82, 1.82, 100000]
        }
        p = NetworkParameters(d)

        self.assertEqual(p.output_parsers,
                         [None, SurfaceAreaParser, PoreVolumeParser])

    def test_validation(self):
        """Test that validation raises an exception for wrong input."""
        from aiida_zeopp.data.parameters import NetworkParameters
        from voluptuous import MultipleInvalid

        d = {
            'cssr2': True,
        }

        with self.assertRaises(MultipleInvalid):
            NetworkParameters(d)
