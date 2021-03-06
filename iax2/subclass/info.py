from iax2.subclass import baseclass, frameTypes, VERSION


__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


class info(baseclass):
    fType = 1
    frameType = frameTypes.IAX
    subClass = 0x42

    format = (
        (0x42, True, VERSION),  # Version
        (0x43, False, ""),      # Client Count
    )

    def __init__(self, data=None, **kwargs):
        if 'call_count' in kwargs:
            self.call_count = kwargs['call_count']

        if 'initial' in kwargs:
            self.initial = kwargs['initial']
        else:
            self.initial = False
        super().__init__(data, **kwargs)

    def parse(self, data):
        # Use the baseClass parser then work with the data
        super().parse(data)
        self.response = info

    def generate(self):
        data = {}
        if not self.initial:
            data[0x43] = self.nodes.currsize
        super().generate(data)
