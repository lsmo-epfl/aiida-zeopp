import unittest
import aiida_zeopp.parsers.plain as parsers


class VolpoParserTestCase(unittest.TestCase):
    def test_parse_hkust(self):

        string = """
        @ EDI.volpo Unitcell_volume: 307.484   Density: 1.62239
        POAV_A^3: 131.284 POAV_Volume_fraction: 0.42696 POAV_cm^3/g: 0.263168
        PONAV_A^3: 0 PONAV_Volume_fraction: 0 PONAV_cm^3/g: 0
        """

        parser = parsers.PoreVolumeParser
        parser.parse(string)


class SaParserTestCase(unittest.TestCase):
    def test_parse_hkust(self):
        string = """
        HKUST-1.sa Unitcell_volume: 18280.8   Density: 0.879097
        ASA_A^2: 3545.59 ASA_m^2/cm^3: 1939.51 ASA_m^2/g: 2206.26 
        NASA_A^2: 0 NASA_m^2/cm^3: 0 NASA_m^2/g: 0 Number_of_channels: 1 
        Channel_surface_area_A^2: 3545.59 Number_of_pockets: 0
        Pocket_surface_area_A^2: 
        """

        parser = parsers.SurfaceAreaParser
        parser.parse(string)


class ResParserTestCase(unittest.TestCase):
    def test_parse_hkust(self):

        string = """
        HKUST-1.res    13.19937 6.74621  13.19937
        """

        parser = parsers.ResParser
        parser.parse(string)
