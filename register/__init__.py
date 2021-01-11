from random import randint
from iax2.helpers import IEDateTime, IEApparentAddr

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

    def __init__(self):
        self._iedatetime = None
        self._ieapparentaddr = None

    @property
    def Refresh(self):
        return randint(self.RegRefresh - self.RegRefreshSize, self.RegRefresh + self.RegRefreshSize)

    @property
    def IEDateTime(self):
        if self._iedatetime == None:
            self._iedatetime = IEDateTime()
        return self._iedatetime.result

    @IEDateTime.setter
    def IEDateTime(self, value):
        self._iedatetime = value

    @property
    def IEApparentAddr(self):
        if self._ieapparentaddr == None:
            self._ieapparentaddr = IEApparentAddr(self.host, self.port)
        return self._ieapparentaddr.result

    @IEApparentAddr.setter
    def IEApparentAddr(self, value):
        self._ieapparentaddr = value
