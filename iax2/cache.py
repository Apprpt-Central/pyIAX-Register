from datetime import datetime, timedelta
from functools import lru_cache, wraps

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


def timed_lru_cache(seconds: int, maxsize: int = 512):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            logger.verbose(f"Cache: {func.cache_info()}")

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
