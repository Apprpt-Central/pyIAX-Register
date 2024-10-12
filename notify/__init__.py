from random import randint
from os.path import dirname, basename, isfile, join
import glob

__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"

# source: https://stackoverflow.com/q/58082592
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


class baseNotify():
    def __init__(self, *args, **kwargs):
        self.args = kwargs['args']

class notify():
    def __init__(self, *args, **kwargs):
        pass