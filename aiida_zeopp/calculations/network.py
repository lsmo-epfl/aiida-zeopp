from aiida.orm.calculation.job import JobCalculation
from aiida.orm.data.singlefile import SinglefileData
from aiida.common.utils import classproperty
from aiida.common.exceptions import (InputValidationError, ValidationError)
from aiida.common.datastructures import (CalcInfo, CodeInfo)
from aiida.orm import DataFactory

NetworkParameters = DataFactory('zeopp.parameters')


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
                'docstring': "specifies command line parameters",
            },
            "file": {
                'valid_types': SinglefileData,
                'additional_parameter': "linkname",
                'linkname': cls._get_linkname_file,
                'docstring': "input file",
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

        try:
            inputfile = inputdict.pop(self.get_linkname('file'))
        except KeyError:
            raise InputValidationError(
                "No input file specified for calculation")
        if not isinstance(inputfile, SinglefileData):
            raise InputValidationError("file not of type SinglefileData")

        # Check that nothing is left unparsed
        if inputdict:
            raise ValidationError("Unknown inputs")

        return parameters, code, inputfile

    def _prepare_for_submission(self, tempfolder, inputdict):
        """
        Create input files.

            :param tempfolder: aiida.common.folders.Folder subclass where
                the plugin should put all its files.
            :param inputdict: dictionary of the input nodes as they would
                be returned by get_inputs_dict
        """

        parameters, code, inputfile = self._validate_inputs(inputdict)

        # Prepare CalcInfo to be returned to aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = [
            inputfile.get_file_abs_path(), inputfile.filename
        ]
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = parameters.output_files

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = parameters.cmdline_params(
            input_file_name=inputfile.filename)
        codeinfo.code_uuid = code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
