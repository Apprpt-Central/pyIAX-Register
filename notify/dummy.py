from notify import notify, baseNotify

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
class dummy(baseNotify):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_handler(self):
        return notifyHandler(args=self.args)


# Handlers are initialized at time of use,
class notifyHandler(notify):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # hashed === md5(challenge+plaintext) -> success
    def notify(self, *args, **kwargs):
        logger.success("GOT IT")
#        logger.success(f"Authentication Success from {host}:{port} for user {user}")

def help(parser):
    group = parser.add_argument_group('Dummy Notify Module')
#    group.add_argument('--password', dest='REGISTER_PASSWORD', default='password', help='The password to always accept (Default: password)')
