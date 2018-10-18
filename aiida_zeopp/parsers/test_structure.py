from __future__ import absolute_import
import os
import aiida_zeopp.parsers.structure as parsers
import aiida_zeopp.tests as zt


class CssrParserTestCase(zt.PluginTestCase):

    BACKEND = zt.get_backend()

    def test_parse_hkust(self):

        with open(os.path.join(zt.TEST_DIR, 'MgO.cssr'), 'r') as f:
            string = f.read()

        parser = parsers.CssrParser
        parser.parse(string)
