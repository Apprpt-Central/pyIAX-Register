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


class lagrp(baseclass):
    fType = 1
    frameType = frameTypes.IAX
    subClass = 0x0c

    format = (
    )

    def __init__(self, data=None, **kwargs):
        super().__init__(data, **kwargs)

    def parse(self, data):
        # Use the baseClass parser then work with the data
        super().parse(data)

    def generate(self):
        data = {}
        super().generate(data)
