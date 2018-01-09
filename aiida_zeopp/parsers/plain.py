# pylint: disable=useless-super-delegation
import re
import six


class KeywordParser(object):

    keywords = {
        'keyword1': float,
        'keyword2': int,
    }

    def parse(self, string):
        """ Parse zeo++ keyword format

        Example string:

        keyword1: 12234.32312  keyword2: 1

        parameters
        ----------
        string: string
          string with keywords
        
        return
        ------
        results: dict
          dictionary of output values
        """
        results = {}

        regex = "{}: ([\d\.]*)"
        for keyword, ktype in six.iteritems(self.keywords):
            regex_rep = regex.format(re.escape(keyword))
            match = re.search(regex_rep, string)
            if match is None:
                raise ValueError("Keyword {} not specified".format(keyword))

            value = match.group(1)
            if value == "":
                raise ValueError(
                    "No value specified for keyword {}".format(keyword))

            results[keyword] = ktype(value)

        return results


class POVolumeParser(KeywordParser):

    keywords = {
        'Unitcell_volume': float,
        'Density': float,
        'POAV_A^3': float,
        'POAV_Volume_fraction': float,
        'POAV_cm^3/g': float,
        'PONAV_A^3': float,
        'PONAV_Volume_fraction': float,
        'PONAV_cm^3/g': float,
    }

    def parse(self, string):
        """ Parse zeo++ .volpo format

        Example volpo string:

        @ EDI.volpo Unitcell_volume: 307.484   Density: 1.62239 
        POAV_A^3: 131.284 POAV_Volume_fraction: 0.42696 POAV_cm^3/g: 0.263168 
        PONAV_A^3: 0 PONAV_Volume_fraction: 0 PONAV_cm^3/g: 0

        parameters
        ----------
        string: string
          string in volpo format
        
        return
        ------
        results: dict
          dictionary of output values
        """
        return super(POVolumeParser, self).parse(string)


class AVolumeParser(KeywordParser):

    keywords = {
        'Unitcell_volume': float,
        'Density': float,
        'AV_A^3': float,
        'AV_Volume_fraction': float,
        'AV_cm^3/g': float,
        'NAV_A^3': float,
        'NAV_Volume_fraction': float,
        'NAV_cm^3/g': float,
    }

    def parse(self, string):
        """ Parse zeo++ .vol format

        Example vol string:

        @ EDI.vol Unitcell_volume: 307.484   Density: 1.62239
        AV_A^3: 22.6493 AV_Volume_fraction: 0.07366 AV_cm^3/g: 0.0454022
        NAV_A^3: 0 NAV_Volume_fraction: 0 NAV_cm^3/g: 0

        parameters
        ----------
        string: string
          string in volpo format
        
        return
        ------
        results: dict
          dictionary of output values
        """
        return super(AVolumeParser, self).parse(string)


class SurfaceAreaParser(KeywordParser):

    keywords = {
        'Unitcell_volume': float,
        'Density': float,
        'ASA_A^2': float,
        'ASA_m^2/cm^3': float,
        'ASA_m^2/g': float,
        'NASA_A^2': float,
        'NASA_m^2/cm^3': float,
        'NASA_m^2/g': float,
        'Number_of_channels': int,
        'Channel_surface_area_A^2': float,
        'Number_of_pockets': int,
        'Pocket_surface_area_A^2': float,
    }

    def parse(self, string):
        """ Parse zeo++ .sa format

        Example sa string:

        @ HKUST-1.sa Unitcell_volume: 18280.8   Density: 0.879097   ASA_A^2:
        3545.59 ASA_m^2/cm^3: 1939.51 ASA_m^2/g: 2206.26 NASA_A^2: 0
        NASA_m^2/cm^3: 0 NASA_m^2/g: 0 Number_of_channels: 1
        Channel_surface_area_A^2: 3545.59 Number_of_pockets: 0
        Pocket_surface_area_A^2:

        parameters
        ----------
        string: string
          string in sa format
        
        return
        ------
        results: dict
          dictionary of output values
        """
        return super(SurfaceAreaParser, self).parse(string)


class ResParser(KeywordParser):

    keywords = (
        'Largest_included_sphere',
        'Largest_free_sphere',
        'Largest_included_free_sphere',
    )

    def parse(self, string):
        """ Parse zeo++ .res format

        Example res string:

        HKUST-1.res    13.19937 6.74621  13.19937

        Containing the diameters of 
         * the largest included sphere
         * the largest free sphere
         * the largest included sphere along free sphere path

        parameters
        ----------
        string: string
          string in res format
        
        return
        ------
        res: dict
          dictionary of output values
        """
        res = {}

        values = string.split()

        if len(values) != 4:
            raise ValueError("Found more than 4 fields in .res format")

        for i in (0, 1, 2):
            res[self.keywords[i]] = float(values[i + 1])

        return res
