import os
from argparse import ArgumentParser
from aiida.common.example_helpers import test_and_get_code  
from aiida.orm.data.base import Float
from aiida.orm.data.cif import CifData
from aiida.orm.data.parameter import ParameterData
from aiida.work.run import submit
from aiida_zeopp.workflows import ZeoppBlockPocketsWorkChain

probe_radius = 1.8
pwd = os.path.dirname(os.path.realpath(__file__))
print(pwd+"/structure.cif")
structure = CifData(file=pwd+"/structure.cif")

# replace 'zeopp@deneb' with your zeo++ AiiDA code
code = test_and_get_code('zeopp@deneb', expected_code_type='zeopp.network')

'''
# Optional inputs that must be specified inside submit(): 

# Inside submit() :  _num_samples = num_samples_dict
num_samples_dict = {
    'sa': 100,
    'volpo': 100,
    'block': 50,
}

# Inside submit() :  _options = options_dict
options_dict = {
    "resources": {
        "num_machines": 1,
        "tot_num_mpiprocs": 1,
    },
    "max_wallclock_seconds": 30 * 60,
    "withmpi": False,
}

# Inside submit() :  _flag = True 
(If needed to compute Surface Area, Pore Diameter and Channel Dimensionality use _flag=True)

'''

submit(ZeoppBlockPocketsWorkChain,
        probe_radius=Float(probe_radius),
        structure=structure,
        zeopp_code=code,
        )
