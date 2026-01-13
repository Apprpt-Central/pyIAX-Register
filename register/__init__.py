"""Base classes and helpers for registration backends.

Provides a small framework that registration backends extend. The
`baseRegister` class is used for components that need access to parsed
CLI args at initialization time. The `register` class supplies common
helpers and properties used during verification (supply `host` and
`port` on the handler instances before accessing IE helpers).
"""

from random import randint
from iax2.helpers import IEDateTime, IEApparentAddr
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


class baseRegister():
    """Simple initializer that stores parsed CLI args for initializers."""

    def __init__(self, *args, **kwargs):
        self.args = kwargs['args']


class register():
    """Base class for per-request handlers used by the IAX2 parser.

    Subclasses should set `self.host` and `self.port` before accessing
    `IEDateTime` or `IEApparentAddr` which derive IAX-specific IEs used
    when building responses.
    """

    CauseCode = 0x01
    Cause = "Error"
    RegRefresh = 120
    RegRefreshSize = 10

    def __init__(self, *args, **kwargs):
        if 'args' in kwargs:
            self.args = kwargs['args']
        self._iedatetime = None
        self._ieapparentaddr = None

    @property
    def Refresh(self):
        # randomized refresh interval within configured bounds
        return randint(self.RegRefresh - self.RegRefreshSize, self.RegRefresh + self.RegRefreshSize)

    @property
    def IEDateTime(self):
        # lazily construct IEDateTime helper when first requested
        if self._iedatetime is None:
            self._iedatetime = IEDateTime()
        return self._iedatetime.result

    @IEDateTime.setter
    def IEDateTime(self, value):
        self._iedatetime = value

    @property
    def IEApparentAddr(self):
        # lazily construct IEApparentAddr using host/port from the handler
        if self._ieapparentaddr is None:
            self._ieapparentaddr = IEApparentAddr(self.host, self.port)
        return self._ieapparentaddr.result

    @IEApparentAddr.setter
    def IEApparentAddr(self, value):
        self._ieapparentaddr = value
