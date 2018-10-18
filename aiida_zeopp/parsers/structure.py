from __future__ import absolute_import
import pymatgen


class CssrParser(object):
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
        from aiida.orm.data.structure import StructureData
        pym_struct = cls.parse(string)
        return StructureData(pymatgen_structure=pym_struct)
