# pylint: disable=useless-super-delegation
from __future__ import absolute_import
from __future__ import print_function
import re
import six
from six.moves import map
from six.moves import range


class KeywordParser(object):

    keywords = {
        'keyword1': float,
        'keyword2': int,
    }

    @classmethod
    def parse(cls, string):
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

        regex = r"{}: ([\d\.]*)"
        for keyword, ktype in six.iteritems(cls.keywords):
            regex_rep = regex.format(re.escape(keyword))
            match = re.search(regex_rep, string)
            if match is None:
                raise ValueError("Keyword {} not specified".format(keyword))

            value = match.group(1)
            if value == "":
                value = 0
                # uncomment this when #1 is fixed
                #raise ValueError(
                #    "No value specified for keyword {}".format(keyword))

            results[keyword] = ktype(value)

        return results

    @classmethod
    def parse_aiida(cls, string):
        from aiida.orm.data.parameter import ParameterData
        return ParameterData(dict=cls.parse(string))


class PoreVolumeParser(KeywordParser):

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

    @classmethod
    def parse(cls, string):
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
        return super(PoreVolumeParser, cls).parse(string)


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

    @classmethod
    def parse(cls, string):
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
        return super(AVolumeParser, cls).parse(string)


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

    @classmethod
    def parse(cls, string):
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
        return super(SurfaceAreaParser, cls).parse(string)


class ResParser(KeywordParser):

    keywords = (
        'Largest_included_sphere',
        'Largest_free_sphere',
        'Largest_included_free_sphere',
    )

    @classmethod
    def parse(cls, string):
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
            res[cls.keywords[i]] = float(values[i + 1])

        return res


class PoresSizeDistParser(object):
    @classmethod
    def parse(cls, string):  # pylint: disable=too-many-locals
        """
        Parse zeo++ .psd format, using routines similar to other parsers to avoid additional pandas dependency

        Parameters
        ----------
        string: str
            string in psd format

        Returns
        -------
        results: dict
            dictionary of output values
        """
        lines = string.splitlines()
        # remove empty lines
        lines = [l for l in lines if l.strip()]

        # find line where histogram data begins
        header_line = 'Bin Count'
        i = 0
        for i, line in enumerate(lines):
            if header_line in line:
                break
        else:
            raise ValueError('Did not find header line in data')
        # extract histogram data
        bins, counts, cumulatives, derivatives = [], [], [], []
        for line in lines[i + 1:]:
            b, count, cumulative, derivative = line.split()
            bins.append(float(b))
            counts.append(int(count))
            cumulatives.append(float(cumulative))
            derivatives.append(float(derivative))

        psd_dict = {
            'psd': {
                'bins': bins,
                'counts': counts,
                'cumulatives': cumulatives,
                'derivatives': derivatives
            }
        }

        return psd_dict


class ChannelParser(object):
    @classmethod
    def parse(cls, string):  # pylint: disable=too-many-locals
        """ Parse zeo++ .chan format

        Example chan string::

            P8bal_P1.chan   2 channels identified of dimensionality 3 3
            Channel  0  9.92223  3.85084  9.92223
            Channel  1  9.92222  3.85084  9.92222
            P8bal_P1.chan summary(Max_of_columns_above)   9.92223 3.85084  9.92223  probe_rad: 1.8  probe_diam: 3.6


        parameters
        ----------
        string: string
          string in chan format
        
        return
        ------
        results: list
          dictionary of output values
        """
        lines = string.splitlines()
        # remove empty lines
        lines = [l for l in lines if l.strip()]
        nlines = len(lines)

        # parse header line
        match = re.search(
            r'(\d+) channels identified of dimensionality([\d\s]*)', lines[0])
        if not match:
            raise ValueError(
                "The following string was not recognized as a valid header of the .chan format:\n"
                + lines[0])

        nchannels = int(match.group(1))

        if nchannels == 0:
            dimensionalities = []
        else:
            dimensionalities = list(map(int, match.group(2).split()))

        if nchannels != len(dimensionalities):
            raise ValueError(
                "Number of channels {} does not match number of dimensionalities {}"
                .format(nchannels, len(dimensionalities)))

        if nchannels != nlines - 2:
            raise ValueError(
                "Number of lines in file {} does not equal number of channels {}+2"
                .format(nlines, nchannels))

        # parse remaining lines (last line is discarded)
        dis, dfs, difs = [], [], []
        for i in range(1, nchannels + 1):
            _c, _i, di, df, dif = lines[i].split()
            dis.append(float(di))
            dfs.append(float(df))
            difs.append(float(dif))

        pm_dict = {
            'Channels': {
                'Largest_included_spheres': dis,
                'Largest_free_spheres': dfs,
                'Largest_included_free_spheres': difs,
                'Dimensionalities': dimensionalities,
            }
        }
        return pm_dict

    @classmethod
    def parse_aiida(cls, string):
        from aiida.orm.data.parameter import ParameterData
        return ParameterData(dict=cls.parse(string))
