from __future__ import absolute_import
from aiida.orm import CalculationFactory, DataFactory
from aiida.orm.code import Code
from aiida.orm.data.base import Float
from aiida.work.run import submit
from aiida.work.workchain import WorkChain, ToContext, if_, Outputs

# import base data classes
ZeoppCalculation = CalculationFactory('zeopp.network')
ParameterData = DataFactory('parameter')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')

options = {
    "resources": {
        "num_machines": 1,
        "tot_num_mpiprocs": 1,
    },
    "max_wallclock_seconds": 30 * 60,
    "withmpi": False,
}


class ZeoppGeometryWorkChain(WorkChain):
    """Workchain that for a computing geometry properties using zeo++."""

    @classmethod
    def define(cls, spec):
        """Define inputs, logic and outputs of ZeoppGeometryWorkChain"""
        super(ZeoppGeometryWorkChain, cls).define(spec)

        # Define the inputs, specifying the type we expect
        spec.input("probe_radius", valid_type=Float, required=True)
        spec.input("structure", valid_type=CifData, required=True)
        spec.input("zeopp_code", valid_type=Code, required=True)
        spec.input(
            "_options", valid_type=dict, required=False, default=options)

        # Define the outputs, specifying the type we expect
        spec.output("block", valid_type=SinglefileData, required=False)
        spec.output("pore_volume_volpo", valid_type=ParameterData)
        spec.output("surface_area_sa", valid_type=ParameterData)
        spec.output("free_sphere_res", valid_type=ParameterData)

        # Define workflow logic
        spec.outline(
            cls.run_geom_zeopp,
            if_(cls.should_run_block_zeopp)(cls.run_block_zeopp, ),
            cls.return_result,
        )

    def run_geom_zeopp(self):
        """This function will perform geometry analysis using zeo++."""
        NetworkParameters = DataFactory('zeopp.parameters')
        sigma = self.inputs.probe_radius.value
        params = {
            'ha': True,
            'res': True,
            'sa': [sigma, sigma, 10000],
            'volpo': [sigma, sigma, 10000],
        }
        inputs = {
            'code': self.inputs.zeopp_code,
            'structure': self.inputs.structure,
            'parameters': NetworkParameters(dict=params),
            '_options': self.inputs._options,
            '_label': "run_geom_zeopp",
        }

        # Create the calculation process and launch it
        future = submit(ZeoppCalculation.process(), **inputs)
        self.report("pk: {} | Running geometry analysis with zeo++".format(
            future.pid))
        return ToContext(zeopp_geometry=Outputs(future))

    def should_run_block_zeopp(self):
        """If the pore non-accessible volume is 0 - there is no need to run block pocket calculation."""
        return self.ctx.zeopp_geometry[
            "pore_volume_volpo"].dict.PONAV_Volume_fraction > 0.001

    def run_block_zeopp(self):
        """This is the main function that will perform a zeo++ block pocket calculation."""
        NetworkParameters = DataFactory('zeopp.parameters')
        sigma = self.inputs.probe_radius.value
        params = {
            'ha': True,
            'block': [sigma, 200],
        }
        inputs = {
            'code': self.inputs.zeopp_code,
            'structure': self.inputs.structure,
            'parameters': NetworkParameters(dict=params),
            '_options': self.inputs._options,
            '_label': "run_block_zeopp",
        }

        # Create the calculation process and launch it
        future = submit(ZeoppCalculation.process(), **inputs)
        self.report("pk: {} | Running zeo++ block volume calculation".format(
            future.pid))
        return ToContext(zeopp_block=Outputs(future))

    def return_result(self):
        """Attach the results of the raspa calculation and the initial structure to the outputs."""
        # pylint: disable=bare-except
        try:
            self.out("block", self.ctx.zeopp_block["block"])
        except:
            self.report("No block pocket calculation performed")
        self.out("pore_volume_volpo",
                 self.ctx.zeopp_geometry["pore_volume_volpo"])
        self.out("surface_area_sa", self.ctx.zeopp_geometry["surface_area_sa"])
        self.out("free_sphere_res", self.ctx.zeopp_geometry["free_sphere_res"])
        self.report("Workchain <{}> completed successfully".format(
            self.calc.pk))
        return


# EOF
