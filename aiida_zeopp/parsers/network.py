# -*- coding: utf-8 -*-

#import json
from aiida.parsers.parser import Parser
from aiida.parsers.exceptions import OutputParsingError
from aiida_zeopp.calculations.network import NetworkCalculation


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

    # pylint: disable=protected-access
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
        output_files = self._calc.inp.parameters.output_files
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if set(output_files) <= set(list_of_files):
            pass
        else:
            self.logger.error(
                "Not all expected output files {} were found".format(
                    output_files))
            return success, node_list

        # Parse output files
        output_parsers = self._calc.inp.parameters.output_parsers
        output_links = self._calc.inp.parameters.output_links
        for fname, parser, link in list(
                zip(output_files, output_parsers, output_links)):

            if parser is None:
                parsed = SinglefileData(file=out_folder.get_abs_path(fname))

            else:
                try:
                    with open(out_folder.get_abs_path(fname)) as f:
                        parsed = parser.parse_aiida(f.read())
                except ValueError:
                    self.logger.error(
                        "Error parsing file {} with parser {}".format(
                            fname, parser))

            node_list.append((link, parsed))

        success = True
        return success, node_list
