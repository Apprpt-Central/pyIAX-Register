"""Dummy notify backend that logs notifications.

Useful for development when you want to see notification events without
publishing to Kafka or other external systems.
"""

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


class dummy(baseNotify):
    """No-op initializer; returns a handler that logs notifications."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_handler(self):
        return notifyHandler(args=self.args)


class notifyHandler(notify):
    """Handler that emits a success-level log for notify events."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def notify(self, *args, **kwargs):
        # Log a simple event to indicate notification reached this handler
        logger.success("GOT IT")


def help(parser):
    group = parser.add_argument_group('Dummy Notify Module')
