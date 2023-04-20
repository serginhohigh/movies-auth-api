import logging
import time
from functools import wraps

import psycopg
import redis

logger = logging.getLogger(__name__)


def backoff(start_sleep_time=2, factor=2, border_sleep_time=600):

    sleep_time = start_sleep_time

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (
                psycopg.OperationalError,
                psycopg.errors.ConnectionException,
                redis.exceptions.ConnectionError,
            ):
                nonlocal sleep_time
                logger.exception(
                    'Connection error! Sleep on %s seconds',
                    sleep_time,
                )
                time.sleep(sleep_time)
                if sleep_time <= border_sleep_time:
                    sleep_time = sleep_time * factor
                return inner(*args, **kwargs)
        return inner
    return func_wrapper
