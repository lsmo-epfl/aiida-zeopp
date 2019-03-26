"""
AiiDA Zeo++ Plugin

"""

from __future__ import absolute_import
__version__ = "0.2.0"

# disable psycopg2 warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='psycopg2')
warnings.filterwarnings("ignore", category=UserWarning, module='pymatgen')
