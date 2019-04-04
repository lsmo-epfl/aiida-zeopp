from __future__ import absolute_import
from __future__ import print_function

import os
from aiida.orm import Float, Code
from aiida.orm.nodes.data.cif import CifData
from aiida.engine import submit
from aiida_zeopp.workflows import ZeoppBlockPocketsWorkChain

probe_radius = 1.8
pwd = os.path.dirname(os.path.realpath(__file__))
print((pwd + "/structure.cif"))
structure = CifData(file=pwd + "/structure.cif")

# replace 'network@localhost' with your zeo++ AiiDA code
code = Code.objects.get(
    label='network@localhost', input_plugin_name='zeopp.network')

future = submit(
    ZeoppBlockPocketsWorkChain,
    probe_radius=Float(probe_radius),
    structure=structure,
    zeopp_code=code,
)
print(future)
