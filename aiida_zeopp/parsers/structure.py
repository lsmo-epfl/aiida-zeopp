"""Atomic structure parsers."""
try:
    from pymatgen import Structure
except ImportError:
    from pymatgen.core import Structure

from aiida.orm import StructureData


class CssrParser():
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
        return Structure.from_str(string, fmt='cssr')

    @classmethod
    def parse_aiida(cls, string):
        """Parse .cssr string to AiiDA StructureData"""
        pym_struct = cls.parse(string)
        return StructureData(pymatgen_structure=pym_struct)
