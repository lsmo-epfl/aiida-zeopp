"""
AiiDA Zeo++ Plugin

"""

__version__ = '1.1.0'

# disable psycopg2 warning
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='psycopg2')
warnings.filterwarnings('ignore', category=UserWarning, module='pymatgen')
