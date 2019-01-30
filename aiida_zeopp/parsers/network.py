# -*- coding: utf-8 -*-

#import json
from __future__ import absolute_import
from aiida.parsers.parser import Parser
from aiida.parsers.exceptions import OutputParsingError
from aiida_zeopp.calculations.network import NetworkCalculation
from aiida.orm.data.parameter import ParameterData
from six.moves import zip


class NetworkParser(Parser):
    """
    Parser class for output of zeo++ network binary
    """

    def __init__(self, calculation):
        """
        Initialize Parser instance
        """
        super(NetworkParser, self).__init__(calculation)

        # check for valid input
        if not isinstance(calculation, NetworkCalculation):
            raise OutputParsingError("Can only parse NetworkCalculation")

    # pylint: disable=protected-access,too-many-locals
    def parse_with_retrieved(self, retrieved):
        """
        Parse output data folder, store results in database.

        :param retrieved: a dictionary of retrieved nodes, where
          the key is the link name
        :returns: a tuple with two values ``(bool, node_list)``, 
          where:

          * ``bool``: variable to tell if the parsing succeeded
          * ``node_list``: list of new nodes to be stored in the db
            (as a list of tuples ``(link_name, node)``)
        """
        from aiida.orm.data.singlefile import SinglefileData
        success = False
        node_list = []

        # Check that the retrieved folder is there
        try:
            out_folder = retrieved['retrieved']
        except KeyError:
            self.logger.error("No retrieved folder found")
            return success, node_list

        # Check the folder content is as expected
        list_of_files = out_folder.get_folder_list()
        inp_params = self._calc.inp.parameters
        output_files = inp_params.output_files
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if set(output_files) <= set(list_of_files):
            pass
        else:
            self.logger.error("Not all expected output files {} were found".
                              format(output_files))
            return success, node_list

        # Parse output files
        output_parsers = inp_params.output_parsers
        output_links = inp_params.output_links
        output_parameters = ParameterData(dict={})

        for fname, parser, link in list(
                zip(output_files, output_parsers, output_links)):

            abspath = out_folder.get_abs_path(fname)

            if parser is None:

                # just add file, if no parser implemented
                parsed = SinglefileData(file=out_folder.get_abs_path(fname))
                node_list.append((link, parsed))

                # workaround: if block pocket file is empty, raise an error
                # (it indicates the calculation did not finish)
                if link == 'block':
                    with open(abspath) as f:
                        content = f.read()

                    if not content.strip():
                        raise OutputParsingError(
                            "Empty block file. This indicates the calculation of blocked pockets did not finish."
                        )

            else:
                # else parse and add keys to output_parameters
                try:
                    with open(abspath) as f:
                        # Note: We join it to the output_params
                        #parsed = parser.parse_aiida(f.read())
                        parsed_dict = parser.parse(f.read())
                except ValueError:
                    self.logger.error(
                        "Error parsing file {} with parser {}".format(
                            fname, parser))

                output_parameters.update_dict(parsed_dict)

        # add name of input structures as parameter
        output_parameters._set_attr('Input_structure_filename',
                                    self._calc.inp.structure.filename)
        # add input parameters for convenience
        # note: should be added at top-level in order to allow tab completion
        # of <calcnode>.res.Input_...
        for k in inp_params.keys():
            output_parameters._set_attr('Input_{}'.format(k),
                                        inp_params.get_attr(k))

        node_list.append(('output_parameters', output_parameters))

        success = True
        return success, node_list
