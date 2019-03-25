# -*- coding: utf-8 -*-

from __future__ import absolute_import
from aiida.parsers.parser import Parser
from aiida.orm import Dict
from six.moves import zip
from aiida.common import exceptions


class NetworkParser(Parser):
    """
    Parser class for output of zeo++ network binary
    """

    def parse(self, **kwargs):
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
        # pylint: disable=too-many-locals
        from aiida.orm.nodes.data.singlefile import SinglefileData

        # Check that the retrieved folder is there
        try:
            output_folder = self.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER

        # Check the folder content is as expected
        list_of_files = output_folder.list_object_names()

        # pylint: disable=protected-access
        inp_params = self.node.inputs.parameters
        output_files = inp_params.output_files
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if set(output_files) <= set(list_of_files):
            pass
        else:
            s = "Expected output files {}; found only {}."\
                .format(output_files, list_of_files)
            self.logger.error(s)
            return self.exit_codes.ERROR_OUTPUT_FILES_MISSING

        # Parse output files
        output_parsers = inp_params.output_parsers
        output_links = inp_params.output_links
        output_parameters = Dict(dict={})

        empty_block = False

        for fname, parser, link in list(
                zip(output_files, output_parsers, output_links)):

            # hack - to be removed
            handle = output_folder.open(fname)

            if parser is None:

                # just add file, if no parser implemented
                parsed = SinglefileData(file=handle)
                self.out(link, parsed)

                # workaround: if block pocket file is empty, raise an error
                # (it indicates the calculation did not finish)
                if link == 'block':
                    content = handle.read()

                    if not content.strip():
                        self.logger.error(
                            "Empty block file. This indicates the calculation of blocked pockets did not finish."
                        )
                        empty_block = True

            else:
                # else parse and add keys to output_parameters
                try:
                    # Note: We join it to the output_params
                    #parsed = parser.parse_aiida(f.read())
                    parsed_dict = parser.parse(handle.read())
                except ValueError:
                    self.logger.error(
                        "Error parsing file {} with parser {}".format(
                            fname, parser))

                output_parameters.update_dict(parsed_dict)

            handle.close()

        # add name of input structures as parameter
        output_parameters.set_attribute('Input_structure_filename',
                                        self.node.inputs.structure.filename)
        # add input parameters for convenience
        # note: should be added at top-level in order to allow tab completion
        # of <calcnode>.res.Input_...
        for k in inp_params.keys():
            output_parameters.set_attribute('Input_{}'.format(k),
                                            inp_params.get_attribute(k))

        self.out('output_parameters', output_parameters)

        if empty_block:
            return self.exit_codes.ERROR_EMPTY_BLOCK

        return self.exit_codes.SUCCESS
