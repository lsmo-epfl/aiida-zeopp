""" Tests for calculations

"""
import os
import tempfile

from aiida.utils.fixtures import PluginTestCase
from aiida_zeopp.tests import get_backend, get_zeopp_binary


class TestNetwork(PluginTestCase):

    # load the backend to be tested from the environment variable:
    # TEST_AIIDA_BACKEND=django python -m unittest discover
    # TEST_AIIDA_BACKEND=sqlalchemy python -m unittest discover
    BACKEND = get_backend()

    def get_localhost(self):
        """Setup localhost computer"""
        from aiida.orm import Computer
        computer = Computer(
            name='localhost',
            description='my computer',
            hostname='localhost',
            workdir=tempfile.mkdtemp(),
            transport_type='local',
            scheduler_type='direct',
            enabled_state=True)
        return computer

    def get_code(self):
        """Setup code on localhost computer"""
        from aiida.orm import Code

        executable = get_zeopp_binary()

        code = Code(
            files=[executable],
            input_plugin_name='zeopp.network',
            local_executable='network')
        code.label = 'zeopp'
        code.description = 'zeo++'

        return code

    def setUp(self):

        # set up test computer
        self.computer = self.get_localhost().store()
        self.code = self.get_code().store()

    def test_submit(self):
        """Test submitting a calculation"""
        from aiida_zeopp.tests import TEST_DIR

        computer = self.computer
        code = self.code
        #from aiida.orm import Code, Computer, DataFactory
        #code = Code.get_from_string('plugin-template')
        #computer = Computer.get('localhost')

        # Prepare input parameters
        from aiida.orm import DataFactory
        NetworkParameters = DataFactory('zeopp.parameters')
        parameters = NetworkParameters(dict={'cssr': True})
        SinglefileData = DataFactory('singlefile')
        structure = SinglefileData(file=os.path.join(TEST_DIR, 'HKUST-1.cif'))

        # set up calculation
        calc = code.new_calc()
        calc.label = "aiida_zeopp format conversion"
        calc.description = "Test converting .cif to .cssr format"
        calc.set_max_wallclock_seconds(30)
        # This line is only needed for local codes, otherwise the computer is
        # automatically set from the code
        calc.set_computer(computer)
        calc.set_withmpi(False)
        calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})
        calc.use_parameters(parameters)
        calc.use_input_structure(structure)

        calc.store_all()
        calc.submit()
        #print("submitted calculation; calc=Calculation(uuid='{}') # ID={}"\
        #        .format(calc.uuid,calc.dbnode.pk))
