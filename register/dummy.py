"""Dummy registration backend for testing.

This backend accepts a single shared password (configured via
`--password`) and verifies incoming challenges against it. Useful for
local development when a real user store is not available.
"""

from hashlib import md5
from register import register, baseRegister

import logging
import verboselogs

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


class dummy(baseRegister):
    """Initializer for dummy backend (no external resources)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_handler(self):
        return registerHandler(args=self.args)


class registerHandler(register):
    """Per-request handler that validates using a configured password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def verify(self, user, challenge, secret, method, host, port):
        """Check if `secret` matches md5(challenge + configured_password)."""
        self.host = host
        self.port = port
        password = self.args.REGISTER_PASSWORD
        if md5(challenge.encode('utf-8') + password.encode('ascii')).hexdigest().lower() == secret.lower():
            logger.success(f"Authentication Success from {host}:{port} for user {user}")
            return True

        logging.warning("Authentication Failed")
        self.CauseCode = 0x0d
        self.Cause = f"User/Password Incorrect from {host}:{port} for user {user}"
        return False


def help(parser):
    group = parser.add_argument_group('Dummy Registration Module')
    group.add_argument('--password', dest='REGISTER_PASSWORD', default='password', help='The password to always accept (Default: password)')
