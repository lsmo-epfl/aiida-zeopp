from __future__ import absolute_import
from __future__ import print_function
import os
from aiida.common.example_helpers import test_and_get_code
from aiida.orm.data.base import Float
from aiida.orm.data.cif import CifData
from aiida.work.run import submit
from aiida_zeopp.workflows import ZeoppBlockPocketsWorkChain

probe_radius = 1.8
pwd = os.path.dirname(os.path.realpath(__file__))
print((pwd + "/structure.cif"))
structure = CifData(file=pwd + "/structure.cif")

# replace 'network@localhost' with your zeo++ AiiDA code
code = test_and_get_code(
    'network@localhost', expected_code_type='zeopp.network')

future = submit(
    ZeoppBlockPocketsWorkChain,
    probe_radius=Float(probe_radius),
    structure=structure,
    zeopp_code=code,
)
print(future)
