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
        from aiida.orm.data.structure import StructureData
        pym_struct = pymatgen.Structure.from_str(string, fmt='cssr')
        aiida_struct = StructureData(pymatgen_structure=pym_struct)
        return aiida_struct
