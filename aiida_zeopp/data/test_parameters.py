from aiida_zeopp.tests import PluginTestCase


class TestNetworkParameters(PluginTestCase):
    def test_cssr(self):
        from aiida_zeopp.data.parameters import NetworkParameters

        d = {'cssr': True}
        p = NetworkParameters(d)

        self.assertEqual(p.cmdline_params(), ['-cssr', 'out.cssr'])
