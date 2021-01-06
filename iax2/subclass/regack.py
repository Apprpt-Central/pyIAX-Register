from iax2.subclass import baseclass
from iax2.subclass import frameTypes


__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


class regack(baseclass):
    fType = 1
    frameType = frameTypes.IAX
    subClass = 0x0f

    format = (
        (0x06, True, ""),    # Username
        (0x1f, True, ""),    # DateTime
        (0x12, True, ""),    # Apparent Address
        (0x18, False, ""),   # Message Count
        (0x02, False, ""),   # Calling Number
        (0x04, False, ""),   # Calling Name
        (0x13, False, ""),   # Refresh Time
    )

    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)

    def parse(self, data):
        # Use the baseClass parser then work with the data
        super().parse(data)

    def generate(self):
        data = {}
        data[0x06] = self.call.get_entry('UserName')
        data[0x1f] = ""
        data[0x12] = ""
        data[0x13] = self.call.get_entry('RegRefresh')
        super().generate(data)
