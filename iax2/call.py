"""Small helper to represent an ongoing IAX call/session.

`call` stores arbitrary key/value entries that are used by parsers and
response builders to maintain state across packets belonging to the
same call number.
"""

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
        # simple dict to hold call-scoped state (host, timestamps, auth info, etc.)
        self.cache = {}

    def set_entry(self, key, value):
        self.cache[key] = value

    def get_entry(self, key):
        """Return stored entry or None if missing."""
        return self.cache.get(key)
