"""Input parameter class for network executable."""
from voluptuous import Schema, ExactSequence, Any
from aiida.orm import Dict
from aiida.plugins import DataFactory
import aiida_zeopp.parsers.plain as pp

# These options allow specifying the name of the output file
# key : [ accepted values, labels ]
OUTPUT_OPTIONS = {
    'cssr': (bool, ['structure_cssr']),
    'v1': (bool, ['structure_v1']),
    'xyz': (bool, ['structure_xyz']),
    'nt2': (bool, ['network_nt2']),
    'res': (bool, ['free_sphere_res']),
    'zvis': (bool, ['network_zvis']),
    'axs': (float, ['nodes_axs']),
    'visVoro': (float, ['voro', 'voro_accessible', 'voro_nonaccessible']),
    'sa': (ExactSequence([float, float, int]), ['surface_area_sa']),
    'vsa': (ExactSequence([float, float, int]), ['surface_sample_vsa']),
    'vol': (ExactSequence([float, float, int]), ['volume_vol']),
    'volpo': (ExactSequence([float, float, int]), ['pore_volume_volpo']),
    'ray_atom': (ExactSequence([float, float, int]), ['ray_atom']),
    'block': (ExactSequence([float, int]), ['block']),
    'psd': (ExactSequence([float, float, int]), ['psd']),
    'chan': (float, ['channels_chan']),
    'gridG': (bool, ['grid_gaussian']),
    'gridGBohr': (bool, ['grid_gaussian_bohr']),
    'strinfo': (bool, ['str_info']),
    'oms': (bool, ['open_metal_sites']),
}

# Currently NOT implemented
# These options produce an output file with a hardcoded name
# key : [ accepted values, [ output file name(s) ], label ]
#fixed_OUTPUT_OPTIONS = {
#    'gridBOV': (bool, ['{}_f.bov', '{}_f.distances'], 'grid_bov'),
#}

HA_OPTIONS = [
    'OCC',
    'FCC',
    'ACC',
    'AQC',
    'DDH',
    'TIH',
    'ICH',
    'ICC',
    'RIH',
    'S4',
    'S10',
    'S20',
    'S30',
    'S40',
    'S50',
    'S100',
    'S500',
    'S1000',
    'S10000',
    'DEF',
    'HI',
    'MED',
    'LOW',
]

# These options modify the output of other options
# key : [ accepted values, label ]
MODIFIER_OPTIONS = {
    'ha': (Any(bool, *HA_OPTIONS), ['high_accuracy']),
    'stripatomnames': (bool, ['strip_atom_names']),
    'nor': (bool, ['no_radial']),
}

ALL_OPTIONS = dict(
    list(OUTPUT_OPTIONS.items()) + list(MODIFIER_OPTIONS.items()))


class NetworkParameters(Dict):
    """ Command line parameters for zeo++ network binary
    """

    _schema = Schema({k: ALL_OPTIONS[k][0] for k in ALL_OPTIONS})
    schema = _schema.schema  # alias for easier printing

    _OUTPUT_FILE_PREFIX = 'out.{}'

    # pylint: disable=redefined-builtin, too-many-function-args
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        :param dict: the dictionary to set

        Usage: ``NetworkParameters(dict={'cssr': True})``
        """
        dict = self.validate(dict)
        super(NetworkParameters, self).__init__(dict=dict, **kwargs)

    @classmethod
    def validate(cls, parameters_dict):
        """validate parameters"""
        return cls._schema(parameters_dict)

    def cmdline_params(self, structure_file_name=None, radii_file_name=None):
        """Synthesize command line parameters

        e.g. [ '-axs', '0.4', 'out.axs', 'structure.cif']
        """
        parameters = []

        if radii_file_name is not None:
            parameters += ['-r', radii_file_name]

        pm_dict = self.get_dict()
        output_keys = self.output_keys

        for k, val in pm_dict.items():

            parameter = ['-{}'.format(k)]
            if isinstance(val, bool):
                # if boolean is false, no parameter to add
                if not val:
                    continue
            elif isinstance(val, list):
                parameter += val
            else:
                parameter += [val]

            # add output file name(s)
            # Note: For visVoro option, only one (prefix) can be specified
            if k in output_keys:
                parameter += [self._OUTPUT_FILE_PREFIX.format(k)]

            parameters += parameter

        if structure_file_name is not None:
            parameters += [structure_file_name]

        return list(map(str, parameters))

    @property
    def output_dict(self):
        """Return dictionary of specified options requiring an output file name.

        Keys are the selected options that require an output file name,
        values are the file names.
        """
        output_dict = {}

        parameters_dict = self.get_dict()

        for k in parameters_dict:
            if k not in OUTPUT_OPTIONS:
                continue

            if parameters_dict[k] is False:
                continue

            nfiles = len(OUTPUT_OPTIONS[k][1])
            if nfiles == 1:
                output_dict[k] = [self._OUTPUT_FILE_PREFIX.format(k)]
            else:
                # if multiple files, append link labels
                labels = OUTPUT_OPTIONS[k][1]
                output_dict[k] = [
                    self._OUTPUT_FILE_PREFIX.format(k) + '.{}'.format(label)
                    for label in labels
                ]

        return output_dict

    @property
    def output_keys(self):
        """Return subset of specified options requiring an output file name.

        Out of the selected options, return those that you need to specify an
        output file name for.
        """
        return list(self.output_dict.keys())

    @property
    def output_files(self):
        """Return list of output files to be retrieved"""
        # Note: This flattens list(self.output_dict.values())
        return [item for files in self.output_dict.values() for item in files]

    @property
    def output_parsers(self):
        """Return list of output parsers to use.

        :param parameters:  the parameters object used to generate the cmdline parameters
        :type parameters: aiida_zeopp.data.parameters.NetworkParameters

        :returns: List of parsers to be used for each output file.
            List element is None, if parser is not implemented.
        :rtype: list
        """
        parsers = []
        for k in self.output_dict:
            if k == 'vol':
                parsers += [pp.AVolumeParser]
            elif k == 'volpo':
                parsers += [pp.PoreVolumeParser]
            elif k == 'sa':
                parsers += [pp.SurfaceAreaParser]
            elif k == 'res':
                parsers += [pp.ResParser]
            elif k == 'chan':
                parsers += [pp.ChannelParser]
            elif k == 'psd':
                parsers += [pp.PoresSizeDistParser]
            elif k == 'visVoro':
                parsers += [None for _f in OUTPUT_OPTIONS[k][1]]
            #elif k == 'cssr':
            #    parsers += [sp.CssrParser]
            else:
                parsers += [None]

        return parsers

    @property
    def output_links(self):
        """Return list of output link names"""
        output_links = []
        for k in self.output_keys:
            output_links += OUTPUT_OPTIONS[k][1]
        return output_links

    def get_structure_file_name(self, structure):  # pylint: disable=no-self-use
        """Get file name of input structure.

        The 'network;  binary detects file formats by file extension.
        We therefore need to make sure that the file extension of the input file matches its format.

        :param structure: Structure input of plugin
        :returns: input file name
        :rtype: str

        """

        # treating only CifData for the moment - could extend to other formats in the future
        if isinstance(structure, DataFactory('cif')):
            return structure.filename if structure.filename.endswith(
                '.cif') else structure.filename + '.cif'

        raise ValueError('Input structure has unknown type {}'.format(
            type(structure)))
