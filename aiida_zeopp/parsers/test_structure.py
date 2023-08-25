import os

import aiida_zeopp.parsers.structure as parsers
import aiida_zeopp.tests as zt

"""Test CSSR parser"""


def test_parse_hkust():
    with open(os.path.join(zt.TEST_DIR, "MgO.cssr")) as f:
        string = f.read()

    parser = parsers.CssrParser
    parser.parse(string)
