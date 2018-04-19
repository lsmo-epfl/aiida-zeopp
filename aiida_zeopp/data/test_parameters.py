from aiida.utils.fixtures import PluginTestCase
from aiida_zeopp.tests import get_backend


class TestNetworkParameters(PluginTestCase):

    BACKEND = get_backend()

    def test_cssr(self):
        from aiida_zeopp.data.parameters import NetworkParameters

        d = {'cssr': True}
        p = NetworkParameters(d)

        self.assertEqual(p.cmdline_params(), ['-cssr', 'out.cssr'])
