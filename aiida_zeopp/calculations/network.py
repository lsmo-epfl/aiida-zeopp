"""AiiDA calculation class for network executable."""
from aiida.engine import CalcJob
from aiida.common import (CalcInfo, CodeInfo)
from aiida.plugins import DataFactory
from aiida.orm import Data

NetworkParameters = DataFactory('zeopp.parameters')  # pylint: disable=invalid-name
CifData = DataFactory('cif')  # pylint: disable=invalid-name
SinglefileData = DataFactory('singlefile')  # pylint: disable=invalid-name
Dict = DataFactory('dict')  # pylint: disable=invalid-name


class NetworkCalculation(CalcJob):
    """
    AiiDA calculation plugin for the zeo++ network binary
    """
    @classmethod
    def define(cls, spec):
        super(NetworkCalculation, cls).define(spec)

        spec.input('metadata.options.resources',
                   valid_type=dict,
                   default={
                       'num_machines': 1,
                       'num_mpiprocs_per_machine': 1,
                       'tot_num_mpiprocs': 1,
                   })
        spec.input('metadata.options.parser_name',
                   valid_type=str,
                   default='zeopp.network')
        spec.input('parameters',
                   valid_type=NetworkParameters,
                   help='command line parameters for zeo++')
        spec.input('structure',
                   valid_type=CifData,
                   help='input structure to be analyzed')
        spec.input('atomic_radii',
                   valid_type=SinglefileData,
                   help='atomic radii file',
                   required=False)

        spec.exit_code(0,
                       'SUCCESS',
                       message='Calculation completed successfully.')
        spec.exit_code(101,
                       'ERROR_OUTPUT_FILES_MISSING',
                       message='Not all expected output files were found.')
        spec.exit_code(
            102,
            'ERROR_EMPTY_BLOCK',
            message=
            'Empty block file. This indicates the calculation of blocked pockets did not finish.'
        )

        spec.outputs.dynamic = True
        spec.outputs.valid_type = Data
        spec.output('output_parameters',
                    valid_type=Dict,
                    help='key-value pairs parsed from zeo++ output file(s).')
        spec.output('block',
                    valid_type=SinglefileData,
                    help='Blocked pockets fileoutput file.',
                    required=False)

        spec.default_output_node = 'output_parameters'

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` to temporarily write files on disk
        :return: `aiida.common.datastructures.CalcInfo` instance

        """

        # Prepare CalcInfo to be returned to aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid

        # network infers file format from file extension
        structure = self.inputs.structure
        structure_filename = self.inputs.parameters.get_structure_file_name(
            structure)
        calcinfo.local_copy_list = [(structure.uuid, structure.filename,
                                     structure_filename)]

        if 'atomic_radii' in self.inputs:
            atomic_radii = self.inputs.atomic_radii
            radii_file_name = atomic_radii.filename
            calcinfo.local_copy_list.append(
                (atomic_radii.uuid, atomic_radii.filename,
                 atomic_radii.filename))
        else:
            radii_file_name = None

        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = self.inputs.parameters.output_files

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(
            structure_file_name=structure_filename,
            radii_file_name=radii_file_name)
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.withmpi = False
        calcinfo.codes_info = [codeinfo]

        return calcinfo
