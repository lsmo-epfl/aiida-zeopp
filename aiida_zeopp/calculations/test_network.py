""" Tests for calculations

"""
from __future__ import absolute_import
import os

import aiida_zeopp.tests as zt


class TestNetwork(zt.PluginTestCase):
    def setUp(self):
        self.code = zt.get_code(entry_point='zeopp.network')

    def test_submit_HKUST1(self):
        """Test submitting a calculation"""
        from aiida_zeopp.tests import TEST_DIR

        code = self.code

        # Prepare input parameters
        from aiida.orm import DataFactory
        NetworkParameters = DataFactory('zeopp.parameters')
        parameters = NetworkParameters(dict={'cssr': True})
        CifData = DataFactory('cif')
        structure = CifData(
            file=os.path.join(TEST_DIR, 'HKUST-1.cif'), parse_policy='lazy')

        # set up calculation
        calc = code.new_calc()
        calc.label = "aiida_zeopp format conversion"
        calc.description = "Test converting .cif to .cssr format"
        calc.set_max_wallclock_seconds(30)
        calc.set_withmpi(False)
        calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})
        calc.use_parameters(parameters)
        calc.use_structure(structure)

        calc.store_all()
        #calc.submit()
        calc.submit_test(folder=zt.get_temp_folder())
        #print("submitted calculation; calc=Calculation(uuid='{}') # ID={}"\
        #        .format(calc.uuid,calc.dbnode.pk))

    def test_submit_MgO(self):
        """Test submitting a calculation
        
        This includes a radii file.
        """
        from aiida_zeopp.tests import TEST_DIR

        # set up calculation
        calc = self.code.new_calc()
        calc.label = "aiida_zeopp format conversion"
        calc.description = "Test converting .cif to .cssr format"
        calc.set_max_wallclock_seconds(30)
        calc.set_withmpi(False)
        calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

        # Prepare input parameters
        from aiida.orm import DataFactory
        NetworkParameters = DataFactory('zeopp.parameters')
        parameters = NetworkParameters(
            dict={
                'cssr': True,
                'res': True,
                'sa': [1.82, 1.82, 5000],
                'vsa': [1.82, 1.82, 5000],
                'volpo': [1.82, 1.82, 5000],
                'chan': 1.2,
                'ha': False,
                'strinfo': True,
                'gridG': True,
            })
        calc.use_parameters(parameters)

        CifData = DataFactory('cif')
        structure = CifData(
            file=os.path.join(TEST_DIR, 'MgO.cif'), parse_policy='lazy')
        calc.use_structure(structure)

        SinglefileData = DataFactory('singlefile')
        atomic_radii = SinglefileData(file=os.path.join(TEST_DIR, 'MgO.rad'))
        calc.use_atomic_radii(atomic_radii)

        calc.store_all()
        #calc.submit()
        calc.submit_test(folder=zt.get_temp_folder())
        #print("submitted calculation; calc=Calculation(uuid='{}') # ID={}"\
        #        .format(calc.uuid,calc.dbnode.pk))
