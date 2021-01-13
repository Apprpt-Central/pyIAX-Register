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


# Initializer, add any connections you need here as they initialize at startup
class flatfile(baseRegister):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not path.exists(self.args.REGISTER_USERFILE):
            logger.error(f"User file {self.args.REGISTER_USERFILE} does not exist!")
            exit()
        with open(self.args.REGISTER_USERFILE, mode='r') as infile:
            accounts = csv.reader(infile)
            self.accounts = dict((rows[0], rows[1]) for rows in accounts)

    def get_handler(self):
        return registerHandler(self.accounts)


# Handlers are initialized at time of use,
class registerHandler(register):
    def __init__(self, accounts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = accounts

    # hashed === md5(challenge+plaintext) -> success
    def verify(self, user, challenge, secret, method, host, port):
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
