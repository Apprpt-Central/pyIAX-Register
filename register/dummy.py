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


# Initializer, add any connections you need here as they initialize at startup
class dummy(baseRegister):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_handler(self):
        return registerHandler(args=self.args)


# Handlers are initialized at time of use,
class registerHandler(register):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # hashed === md5(challenge+plaintext) -> success
    def verify(self, user, challenge, secret, method, host, port):
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
