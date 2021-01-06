from iax2.subclass import baseclass
from iax2.subclass import frameTypes
from secrets import choice
from string import ascii_letters


__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


class regauth(baseclass):
    fType = 1
    frameType = frameTypes.IAX
    subClass = 0x0e

    format = (
        (0x06, True, ""),    # Username
        (0x0e, True, 0x02),  # Auth Method - Currently only MD5 is supported
        (0x0f, True, ""),    # Challenge
    )

    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)

    def parse(self, data):
        # Use the baseClass parser then work with the data
        super().parse(data)

    def generate(self):
        self.call.set_entry('challengeSecret', "".join(choice(ascii_letters) for i in range(12)))
        data = {}
        data[0x06] = self.call.get_entry('UserName')
        data[0x0f] = self.call.get_entry('challengeSecret')
        super().generate(data)
