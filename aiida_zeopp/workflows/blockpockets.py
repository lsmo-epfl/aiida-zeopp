from __future__ import absolute_import
from aiida.orm import CalculationFactory, DataFactory
from aiida.orm.code import Code
from aiida.orm.data.base import Float
from aiida.work.run import submit
from aiida.work.workchain import WorkChain, ToContext, if_, Outputs
from aiida.work.workfunction import workfunction

# import base data classes
ZeoppCalculation = CalculationFactory('zeopp.network')
ParameterData = DataFactory('parameter')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')
NetworkParameters = DataFactory('zeopp.parameters')

# optional inputs
options = {
    "resources": {
        "num_machines": 1,
        "tot_num_mpiprocs": 1,
    },
    "max_wallclock_seconds": 30 * 60,
    "withmpi": False,
}

num_samples = {
    'sa': 10000,
    'volpo': 100000,
    'block': 100,
}


@workfunction
def get_zeopp_geometry_parameters(probe_radius):
    """Create NetworkParameters from probe radius.

    """
    sigma = probe_radius.value

    params = {
        'ha': True,
        'res': True,
        'sa': [sigma, sigma, num_samples['sa']],
        'chan': sigma,
        'volpo': [sigma, sigma, num_samples['volpo']],
    }
    return NetworkParameters(dict=params)


@workfunction
def get_zeopp_block_parameters(probe_radius):
    """Create NetworkParameters from probe radius.

    :param sigma: Probe radius (A)
    """
    sigma = probe_radius.value

    params = {
        'ha': True,
        'block': [sigma, num_samples['block']],
    }

    return NetworkParameters(dict=params)


class ZeoppBlockPocketsWorkChain(WorkChain):
    """Workchain for computing block pockets if necessary and, optionally, geometry properties using zeo++."""

    @classmethod
    def define(cls, spec):
        """Define inputs, logic and outputs of ZeoppGeometryWorkChain"""
        super(ZeoppBlockPocketsWorkChain, cls).define(spec)

        # Define the inputs, specifying the type we expect
        spec.input("probe_radius", valid_type=Float, required=True)
        spec.input("structure", valid_type=CifData, required=True)
        spec.input("zeopp_code", valid_type=Code, required=True)
        spec.input(
            "_options", valid_type=dict, required=False, default=options)

        # Define the outputs, specifying the type we expect
        spec.output("block", valid_type=SinglefileData, required=False)
        spec.output(
            "output_parameters", valid_type=ParameterData, required=True)

        # Define workflow logic
        spec.outline(
            cls.run_geom_zeopp,
            if_(cls.should_run_block_zeopp)(cls.run_block_zeopp, ),
            cls.return_result,
        )

    def run_geom_zeopp(self):
        """This function will perform geometry analysis using zeo++."""
        # pylint: disable=protected-access
        inputs = {
            'code': self.inputs.zeopp_code,
            'structure': self.inputs.structure,
            'parameters':
            get_zeopp_geometry_parameters(self.inputs.probe_radius),
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
            "output_parameters"].dict.PONAV_Volume_fraction > 0.001

    def run_block_zeopp(self):  # pylint: disable=protected-access
        """This is the main function that will perform a zeo++ block pocket calculation."""
        # pylint: disable=protected-access
        inputs = {
            'code': self.inputs.zeopp_code,
            'structure': self.inputs.structure,
            'parameters': get_zeopp_block_parameters(self.inputs.probe_radius),
            '_options': self.inputs._options,
            '_label': "run_block_zeopp",
        }

        # Create the calculation process and launch it
        future = submit(ZeoppCalculation.process(), **inputs)
        self.report("pk: {} | Running zeo++ block volume calculation".format(
            future.pid))
        return ToContext(zeopp_block=Outputs(future))

    def return_result(self):
        """Attach the results of the zeopp calculations to the outputs."""
        try:
            self.out("block", self.ctx.zeopp_block["block"])
        except AttributeError:
            self.report("No block pocket calculation performed")

        self.out("output_parameters",
                 self.ctx.zeopp_geometry["output_parameters"])

        self.report("Workchain <{}> completed successfully".format(
            self.calc.pk))
        return


# EOF
