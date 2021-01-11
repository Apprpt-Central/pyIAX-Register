__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


class call:
    def __init__(self, ID):
        self.id = ID
        self.cache = {}

    def set_entry(self, key, value):
        self.cache[key] = value

    def get_entry(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            None
