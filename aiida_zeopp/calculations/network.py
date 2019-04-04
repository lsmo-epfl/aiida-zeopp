from __future__ import absolute_import
from aiida.engine import CalcJob
from aiida.common import (CalcInfo, CodeInfo)
from aiida.plugins import DataFactory
from aiida.orm import Data
import six

NetworkParameters = DataFactory('zeopp.parameters')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')
Dict = DataFactory('dict')


class NetworkCalculation(CalcJob):
    """
    AiiDA calculation plugin for the zeo++ network binary
    """
    _DEFAULT_PARSER = 'zeopp.network'

    @classmethod
    def define(cls, spec):
        super(NetworkCalculation, cls).define(spec)

        spec.input(
            'metadata.options.parser_name',
            valid_type=six.string_types,
            default=cls._DEFAULT_PARSER)
        spec.input(
            'parameters',
            valid_type=NetworkParameters,
            help='command line parameters for zeo++')
        spec.input(
            'structure',
            valid_type=CifData,
            help='input structure to be analyzed')
        spec.input(
            'atomic_radii',
            valid_type=SinglefileData,
            help='atomic radii file',
            required=False)

        spec.exit_code(
            0, 'SUCCESS', message='Calculation completed successfully.')
        spec.exit_code(
            101,
            'ERROR_OUTPUT_FILES_MISSING',
            message='Not all expected output files were found.')
        spec.exit_code(
            102,
            'WARNING_EMPTY_BLOCK_FILE',
            message=
            'Empty block file. This indicates the calculation of blocked pockets did not finish.'
        )

        spec.outputs.dynamic = True
        spec.outputs.valid_type = Data
        spec.output(
            'output_parameters',
            valid_type=Dict,
            help='key-value pairs parsed from zeo++ output file(s).')

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
        calcinfo.local_copy_list = [(self.inputs.structure.uuid,
                                     self.inputs.structure.filename,
                                     self.inputs.structure.filename)]

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
            structure_file_name=self.inputs.structure.filename,
            radii_file_name=radii_file_name)
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.withmpi = False
        calcinfo.codes_info = [codeinfo]

        return calcinfo
