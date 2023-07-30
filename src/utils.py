from functools import wraps
from time import time

from logger_factory import get_logger

logger = get_logger(__name__)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.debug(
            f"Execution of function {f.__name__} took {f.__name__}_execution_time={te-ts} seconds."
        )
        return result

    return wrap
