from __future__ import absolute_import
from voluptuous import Schema, ExactSequence
from aiida.orm.data.parameter import ParameterData
import six
from six.moves import map

# These options allow specifying the name of the output file
# key : [ accepted values, label ]
output_options = {
    'cssr': (bool, 'structure_cssr'),
    'v1': (bool, 'structure_v1'),
    'xyz': (bool, 'structure_xyz'),
    'nt2': (bool, 'network_nt2'),
    'res': (bool, 'free_sphere_res'),
    'zvis': (bool, 'network_zvis'),
    'axs': (float, 'nodes_axs'),
    'sa': (ExactSequence([float, float, int]), 'surface_area_sa'),
    'vsa': (ExactSequence([float, float, int]), 'surface_sample_vsa'),
    'vol': (ExactSequence([float, float, int]), 'volume_vol'),
    'volpo': (ExactSequence([float, float, int]), 'pore_volume_volpo'),
    'ray_atom': (ExactSequence([float, float, int]), 'ray_atom'),
    'block': (ExactSequence([float, int]), 'block'),
    'psd': (ExactSequence([float, float, int]), 'psd'),
    'chan': (float, 'channels_chan'),
    'gridG': (bool, 'grid_gaussian'),
    'gridGBohr': (bool, 'grid_gaussian_bohr'),
    'strinfo': (bool, 'str_info'),
    'oms': (bool, 'open_metal_sites'),
}

# Currently NOT implemented
# These options produce an output file with a hardcoded name
# key : [ accepted values, [ output file name(s) ], label ]
#fixed_output_options = {
#    'gridBOV': (bool, ['{}_f.bov', '{}_f.distances'], 'grid_bov'),
#}

# These options modify the output of other options
# key : [ accepted values, label ]
modifier_options = {
    'ha': (bool, 'high_accuracy'),
    'stripatomnames': (bool, 'strip_atom_names'),
    'nor': (bool, 'no_radial'),
}

all_options = dict(
    list(output_options.items()) + list(modifier_options.items()))


class NetworkParameters(ParameterData):
    """ Command line parameters for zeo++ network binary
    """

    _schema = Schema({k: all_options[k][0] for k in all_options})
    schema = _schema.schema  # alias for easier printing

    _OUTPUT_FILE_PREFIX = "out.{}"

    # pylint: disable=redefined-builtin, too-many-function-args
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``NetworkParameters(dict={'cssr': True})``

        .. note:: As of 2017-09, the constructor must also support a single dbnode
          argument (to reconstruct the object from a database node).
          For this reason, positional arguments are not allowed.
        """
        if 'dbnode' in kwargs:
            super(NetworkParameters, self).__init__(**kwargs)
        else:
            # set dictionary of ParameterData
            dict = self.validate(dict)
            super(NetworkParameters, self).__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """validate parameters"""
        return NetworkParameters._schema(parameters_dict)

    def cmdline_params(self, structure_file_name=None, radii_file_name=None):
        """Synthesize command line parameters
        
        e.g. [ ['-axs', '0.4', 'out.axs'], ['structure.cif']]
        """
        parameters = []

        if radii_file_name is not None:
            parameters += ['-r', radii_file_name]

        pm_dict = self.get_dict()
        output_keys = self.output_keys
        for k, v in six.iteritems(pm_dict):

            parameter = ['-{}'.format(k)]
            if isinstance(v, bool):
                pass
            elif isinstance(v, list):
                parameter += v
            else:
                parameter += [v]

            # add output file name
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
        return {
            k: self._OUTPUT_FILE_PREFIX.format(k)
            for k in self.get_dict() if k in list(output_options.keys())
        }

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
        return list(self.output_dict.values())

    @property
    def output_parsers(self):
        """Return list of output parsers to use.

        parameters
        ----------
        parameters: aiida_zeopp.data.parameters.NetworkParameters object
            the parameters object used to generate the cmdline parameters

        returns
        -------
        parsers: list
            List of parsers to be used for each output file.
            List element is None, if parser is not implemented.
        """
        import aiida_zeopp.parsers.plain as pp
        #import aiida_zeopp.parsers.structure as sp

        parsers = []
        for k in self.output_keys:
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
            output_links += [output_options[k][1]]

        return output_links
