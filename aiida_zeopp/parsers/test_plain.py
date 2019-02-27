from __future__ import absolute_import
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


class ChannelParserTestCase(unittest.TestCase):
    def test_parse_p8bal_p1(self):
        """Test case with channels."""

        string = """
        P8bal_P1.chan   2 channels identified of dimensionality 3 3
        Channel  0  9.92223  3.85084  9.92223
        Channel  1  9.92222  3.85084  9.92222
        P8bal_P1.chan summary(Max_of_columns_above)   9.92223 3.85084  9.92223  probe_rad: 1.8  probe_diam: 3.6
        """

        parser = parsers.ChannelParser
        channels = parser.parse(string)['Channels']

        self.assertEquals(channels['Dimensionalities'][1], 3)
        self.assertAlmostEquals(channels['Largest_included_spheres'][1],
                                9.92222)

    def test_parse_IPO3_no_channel(self):
        """Test case with zero channels."""

        string = """
        out.chan   0 channels identified of dimensionality
        out.chan summary(Max_of_columns_above)   0 0  0  probe_rad: 1.525  probe_diam: 3.05
        """

        parser = parsers.ChannelParser
        channels = parser.parse(string)['Channels']

        self.assertEquals(len(channels['Dimensionalities']), 0)


class PoresSizeDistParserTestCase(unittest.TestCase):
    def test_parse_hkust_psd(self):
        string = ('Pore size distribution histogram\n'
                  'Bin size (A): 0.1\n'
                  'Number of bins: 1000\n'
                  'From: 0\n'
                  'To: 100\n'
                  'Total samples: 100000\n'
                  'Accessible samples: 33376\n'
                  'Fraction of sample points in node spheres: 0.33376\n'
                  'Fraction of sample points outside node spheres: 0\n'
                  '\n'
                  'Bin Count Cumulative_dist Derivative_dist\n'
                  '0 0 1 0\n'
                  '0.1 0 1 0\n'
                  '0.2 0 1 0\n')

        parser = parsers.PoresSizeDistParser
        histogram = parser.parse(string)

        bins = [0.0, 0.1, 0.2]
        counts = [0, 0, 0]
        cumulatives = [1.0, 1.0, 1.0]
        derivatives = [0.0, 0.0, 0.0]

        self.assertEquals(bins, histogram['psd']['bins'])
        self.assertEquals(counts, histogram['psd']['counts'])
        self.assertEquals(cumulatives, histogram['psd']['cumulatives'])
        self.assertEquals(derivatives, histogram['psd']['derivatives'])
