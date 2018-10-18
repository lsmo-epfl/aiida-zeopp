from __future__ import absolute_import
from aiida_zeopp.tests import PluginTestCase


class TestNetworkParameters(PluginTestCase):
    def test_cmdline_cssr(self):
        from aiida_zeopp.data.parameters import NetworkParameters

        d = {'cssr': True}
        p = NetworkParameters(d)

        self.assertEqual(p.cmdline_params(), ['-cssr', 'out.cssr'])

    def test_output_parsers(self):
        from aiida_zeopp.data.parameters import NetworkParameters
        from aiida_zeopp.parsers.plain import SurfaceAreaParser, PoreVolumeParser
        #from aiida_zeopp.parsers.structure import CssrParser

        d = {
            'cssr': True,
            'sa': [1.82, 1.82, 10000],
            'volpo': [1.82, 1.82, 100000]
        }
        p = NetworkParameters(d)

        self.assertEqual(p.output_parsers,
                         [None, SurfaceAreaParser, PoreVolumeParser])
