import os
from aiida.common.example_helpers import test_and_get_code  # noqa
from aiida.orm.data.base import Float
from aiida.orm.data.cif import CifData
from aiida.work.run import submit
from aiida_zeopp.workflows import ZeoppGeometryWorkChain

probe_radius = 1.8
pwd = os.getcwd()
print(pwd+"/structure.cif")
structure = CifData(file=pwd+"/structure.cif")
code = test_and_get_code('zeopp@deneb', expected_code_type='zeopp.network')
submit(ZeoppGeometryWorkChain,
        probe_radius=Float(probe_radius),
        structure=structure,
        zeopp_code=code,
        )
