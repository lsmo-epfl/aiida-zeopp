"""Atomic structure parsers."""
from __future__ import absolute_import
import pymatgen


class CssrParser(object):
    """Parser class for CSSR structure format."""
    @classmethod
    def parse(cls, string):
        """ Parse .cssr string using pymatgen

        parameters
        ----------
        string: string
          string in cssr file format

        return
        ------
        results: structure
          corresponding AiiDA structure
        """
        return pymatgen.Structure.from_str(string, fmt='cssr')

    @classmethod
    def parse_aiida(cls, string):
        from aiida.orm.nodes.data.structure import StructureData
        pym_struct = cls.parse(string)
        return StructureData(pymatgen_structure=pym_struct)
