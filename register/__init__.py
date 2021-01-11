from random import randint

__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


class register():
    CauseCode = 0x01
    Cause = "Error"
    RegRefresh = 120
    RegRefreshSize = 10

    def get_refresh(self):
        return randint(self.RegRefresh - self.RegRefreshSize, self.RegRefresh + self.RegRefreshSize)