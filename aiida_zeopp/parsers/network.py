# -*- coding: utf-8 -*-

#import json
from aiida.parsers.parser import Parser
from aiida.parsers.exceptions import OutputParsingError
from aiida.orm.data.parameter import ParameterData
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
        success = False
        node_list = ()

        # Check that the retrieved folder is there
        try:
            out_folder = retrieved['retrieved']
        except KeyError:
            self.logger.error("No retrieved folder found")
            return success, node_list

        # Check what is inside the folder
        list_of_files = out_folder.get_folder_list()
        output_files = self._calc.inp.parameters.output_files
        if set(output_files) < set(list_of_files):
            pass
        else:
            self.logger.error(
                "Not all output files {} were found".format(output_files))
            return success, node_list
        output_parsers = self.output_parsers(self._calc.inp.parameters)

        # parse output files
        node_list = []
        link_name = self.get_linkname_outparams()
        for fname, parser in list(zip(output_files, output_parsers)):
            if parser is None:
                continue

            try:
                with open(out_folder.get_abs_path(fname)) as f:
                    parsed_dict = parser.parse(f.read())
            except ValueError:
                self.logger.error(
                    "Error parsing file {} with parser {}".format(
                        fname, parser))
                return success, node_list

            node_list.append((link_name, ParameterData(dict=parsed_dict)))

        success = True
        return success, node_list

    def output_parsers(self, parameters):
        """ Determine parser objects to use

        parameters
        ----------
        parameters: aiida_zeopp.data.parameters.NetworkParameters object
            the parameters object used to generate the cmdline parameters

        returns
        -------
        parsers: list
            list of parsers to be used for each output file
            list element is None, if parser not implemented
        """
        import aiida_zeopp.parsers.plain as ps

        pm_dict = parameters.get_dict()
        parsers = []

        for k in pm_dict.keys():
            if k == 'vol':
                parsers += [ps.AVolumeParser]
            elif k == 'volpo':
                parsers += [ps.POVolumeParser]
            elif k == 'sa':
                parsers += [ps.SurfaceAreaParser]
            elif k == 'res':
                parsers += [ps.ResParser]
            else:
                parsers += [None]

        return parsers
