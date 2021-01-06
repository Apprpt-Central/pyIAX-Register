from hashlib import md5
from register import register

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
class dummy():
    def get_handler(self):
        return registerHandler()


# Handlers are initialized at time of use,
class registerHandler(register):
    # hashed === md5(challenge+plaintext) -> success
    def verify(self, user, challenge, secret, method, host, port):
        password = "password"
        if md5(challenge.encode('utf-8') + password.encode('ascii')).hexdigest().lower() == secret.lower():
            self.DateTime = ""          # https://tools.ietf.org/html/rfc5456#section-8.6.28
            self.ApparentAddress = ""   # https://tools.ietf.org/html/rfc5456#section-8.6.17
            logger.info(f"Authentication Success")
            return True

        logging.debug("Authentication Failed")
        self.CauseCode = 0x0d
        self.Cause = "User/Password Incorrect"
        return False
