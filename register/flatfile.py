"""Flatfile registration backend.

Loads username/password pairs from a CSV file (default: `useraccess.csv`)
and verifies incoming challenges against the stored plaintext password
using the md5(challenge + password) scheme expected by the IAX client.
"""

from hashlib import md5
from register import register, baseRegister
from os import path
import logging
import verboselogs
import csv

__author__ = "Jason Kendall VE3YCA"
__copyright__ = "Copyright 2020-2021, Jason Kendall"
__credits__ = ["Jason Kendall"]
__license__ = "AGPL 3.0 or Later"
__version__ = "1.0.0"
__maintainer__ = "Jason Kendall"
__email__ = "ve3yca@ve3yca.com"
__status__ = "Dev"


verboselogs.install()
logger = logging.getLogger(__name__)


class flatfile(baseRegister):
    """Initializer that loads accounts into memory at startup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not path.exists(self.args.REGISTER_USERFILE):
            logger.error(f"User file {self.args.REGISTER_USERFILE} does not exist!")
            exit()
        # Load CSV rows into a dict mapping username -> password
        with open(self.args.REGISTER_USERFILE, mode='r') as infile:
            accounts = csv.reader(infile)
            self.accounts = dict((rows[0], rows[1]) for rows in accounts)

    def get_handler(self):
        return registerHandler(self.accounts)


class registerHandler(register):
    """Per-request handler verifying the provided challenge response."""

    def __init__(self, accounts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = accounts

    def verify(self, user, challenge, secret, method, host, port):
        """Return True when the md5(challenge + password) matches `secret`."""
        self.host = host
        self.port = port
        if user in self.accounts:
            password = self.accounts[user]
            if md5(challenge.encode('utf-8') + password.encode('ascii')).hexdigest().lower() == secret.lower():
                logger.success(f"Authentication Success from {host}:{port} for user {user}")
                return True

        logging.warning("Authentication Failed")
        self.CauseCode = 0x0d
        self.Cause = f"User/Password Incorrect from {host}:{port} for user {user}"
        return False


def help(parser):
    group = parser.add_argument_group('Flatfile Registration Module')
    group.add_argument('--file', dest="REGISTER_USERFILE", default='useraccess.csv', help='The file used for registration (Default: useraccess.csv)')
