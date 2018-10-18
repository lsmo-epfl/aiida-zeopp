from __future__ import absolute_import
from aiida.orm.calculation.job import JobCalculation
from aiida.common.utils import classproperty
from aiida.common.exceptions import (InputValidationError, ValidationError)
from aiida.common.datastructures import (CalcInfo, CodeInfo)
from aiida.orm import DataFactory

NetworkParameters = DataFactory('zeopp.parameters')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')


class NetworkCalculation(JobCalculation):
    """
    AiiDA calculation plugin for the zeo++ network binary
    
    """

    def _init_internal_params(self):
        """
        Init internal parameters at class load time
        """
        # reuse base class function
        super(NetworkCalculation, self)._init_internal_params()
        self._default_parser = 'zeopp.network'

    @classproperty
    def _use_methods(cls):
        """
        Add use_* methods for calculations.
        
        Code below enables the usage
        my_calculation.use_parameters(my_parameters)
        """
        use_dict = JobCalculation._use_methods
        use_dict.update({
            "parameters": {
                'valid_types': NetworkParameters,
                'additional_parameter': None,
                'linkname': 'parameters',
                'docstring': "add command line parameters",
            },
            "structure": {
                'valid_types': CifData,
                'additional_parameter': None,
                'linkname': 'structure',
                'docstring': "add input structure to be analyzed",
            },
            "atomic_radii": {
                'valid_types': SinglefileData,
                'additional_parameter': None,
                'linkname': 'atomic_radii',
                'docstring': "file specifying atomic radii",
            },
        })
        return use_dict

    def _validate_inputs(self, inputdict):
        """ Validate input links.
        """
        # Check inputdict
        try:
            parameters = inputdict.pop(self.get_linkname('parameters'))
        except KeyError:
            raise InputValidationError(
                "No parameters specified for calculation")
        if not isinstance(parameters, NetworkParameters):
            raise InputValidationError(
                "parameters not of type NetworkParameters")

        # Check code
        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError("No code specified for calculation")

        # Check input files

        try:
            structure = inputdict.pop(self.get_linkname('structure'))
            if not isinstance(structure, CifData):
                raise InputValidationError("structure not of type CifData")
        except KeyError:
            raise InputValidationError(
                "No input structure specified for calculation")

        try:
            atomic_radii = inputdict.pop(self.get_linkname('atomic_radii'))
        except KeyError:
            # this will use internally defined atomic radii
            atomic_radii = None

        # Check that nothing is left unparsed
        if inputdict:
            raise ValidationError("Unrecognized inputs: {}".format(inputdict))

        return parameters, code, structure, atomic_radii

    def _prepare_for_submission(self, tempfolder, inputdict):
        """
        Create input files.

            :param tempfolder: aiida.common.folders.Folder subclass where
                the plugin should put all its files.
            :param inputdict: dictionary of the input nodes as they would
                be returned by get_inputs_dict
        """

        parameters, code, structure, atomic_radii = \
                self._validate_inputs(inputdict)

        # Prepare CalcInfo to be returned to aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = [[
            structure.get_file_abs_path(), structure.filename
        ]]

        if atomic_radii is not None:
            radii_file_name = atomic_radii.filename
            calcinfo.local_copy_list.append(
                [atomic_radii.get_file_abs_path(), radii_file_name])
        else:
            radii_file_name = None

        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = parameters.output_files

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = parameters.cmdline_params(
            structure_file_name=structure.filename,
            radii_file_name=radii_file_name)
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
